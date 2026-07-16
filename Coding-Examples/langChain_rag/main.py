# lecture31.py — LangChain RAG PIPELINE: loaders, chunking, Chroma, retriever, and an LCEL RAG chain (Session 31)
#
# In Session 30 you attached ROLLING CONVERSATIONAL MEMORY to a LangChain agent: a second
# MessagesPlaceholder (chat_history), manual human/AI append, and RunnableWithMessageHistory.
# Memory keeps a chat COHERENT across turns — but it still cannot answer COMPANY-SPECIFIC
# questions. An agent that remembers your name can still INVENT a leave rule that is wrong for
# your organisation, because the handbook was never in front of it.
#
# Today you re-express the RAG idea you met earlier (load -> chunk -> embed -> store -> retrieve
# -> generate) as a concrete LANGCHAIN pipeline, and then you PROVE it matters by asking the same
# questions WITH retrieval and WITHOUT retrieval.
#
# Filing-cabinet analogy: memory is the running notepad of a conversation; RAG is the FILING
# CABINET of policy documents the assistant is allowed to open before it speaks. "Search first,
# speak second." An HR bot must quote YOUR casual-leave rule — not a confident internet guess.
#
# Two paths, two different jobs (the distinction that makes RAG click):
#   OFFLINE prepare path (run once, or when documents change):
#       handbook files -> loader -> splitter -> embeddings -> Chroma (persist to disk)
#   ONLINE answer path (every user question):
#       question -> retriever -> prompt + context -> LLM -> grounded answer
#
# What this file demonstrates (one script, three escalating stages that mirror the three files
# in the lecture notes — kept together here so the whole pipeline runs end-to-end):
#   STAGE 1 — CREATE the employee-handbook corpus (.md files written from a Python dict)
#   STAGE 2 — INGEST: load -> split -> embed -> PERSIST vectors in Chroma on disk
#   STAGE 3 — RAG APP: an LCEL chain (retriever | prompt | llm | parser) + a WITH-vs-WITHOUT
#             retrieval grounding comparison across three representative queries
#
# PREREQUISITES (do these in the terminal BEFORE running this file):
#   python3 -m venv venv && source venv/bin/activate      # (Windows: venv\Scripts\activate)
#   pip install langchain langchain-groq langchain-huggingface langchain-community \
#               langchain-chroma langchain-text-splitters chromadb sentence-transformers python-dotenv
#   echo 'GROQ_API_KEY=your-key-here' > .env             # loaded via python-dotenv; needed at QUERY time
# Embeddings run LOCALLY via a free sentence-transformer (BGE-small) — no API key or cost for them.
# Run order matters: this script performs the three stages in sequence, so a single
#   python3 main.py
# creates the corpus, ingests it into Chroma, and then runs the grounding comparison.
# (Do not name this file code.py — that shadows the stdlib `code` module and breaks torch.)

# Standard library — path building and an optional clean reset of the vector store.
import os  # os.environ check so we can fail early with a friendly message if the key is missing
import shutil  # shutil.rmtree deletes an old chroma_db so stale vectors never answer from old text
from pathlib import Path  # Path builds folder/file paths cleanly across operating systems

# python-dotenv — load key/value pairs from a local .env file into the process environment.
from dotenv import load_dotenv  # reads .env so GROQ_API_KEY lives in a file, not a shell export

# LangChain vector store + loaders + splitter + Groq chat model + local embeddings.
from langchain_chroma import Chroma  # LangChain wrapper around the Chroma vector database
from langchain_community.document_loaders import DirectoryLoader, TextLoader  # read many .md files
from langchain_text_splitters import RecursiveCharacterTextSplitter  # split long text into chunks
from langchain_groq import ChatGroq  # chat model wrapper for Groq-hosted LLMs (fast inference)
from langchain_huggingface import HuggingFaceEmbeddings  # free, local sentence-transformer embeddings

# LangChain Core — prompt template, string parser, and the passthrough runnable for LCEL.
from langchain_core.prompts import ChatPromptTemplate  # build a chat prompt with {context}/{question}
from langchain_core.output_parsers import StrOutputParser  # turn the LLM message into a plain string
from langchain_core.runnables import RunnablePassthrough  # forward the question through unchanged

# ---------------------------------------------------------------------------
# SHARED CONSTANTS — used by BOTH ingest and the RAG app so they can never drift apart.
# ---------------------------------------------------------------------------
# The golden rule of RAG reproducibility: the SAME embedding model, the SAME collection name, and
# the SAME persist directory must be used at ingest AND at query time, or retrieval silently breaks.
DATA_DIR = Path("handbook_docs")  # folder that will hold the handbook .md files
CHROMA_DIR = Path("chroma_db")  # local folder where Chroma persists vectors between runs
COLLECTION_NAME = "employee_handbook_docs"  # named bucket inside Chroma (like a SQL table name)
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"  # free local sentence-transformer (384 dims) used everywhere


# ===========================================================================
# STAGE 1 — CREATE THE HANDBOOK CORPUS
# ===========================================================================
# A CORPUS is the collection of source documents your RAG system is allowed to search — here, the
# folder of policy files the bot may read. In production this text usually arrives as API text or a
# dictionary, NOT as files already on disk. This stage simulates that: it WRITES three Markdown
# files from a Python dict so the loaders in Stage 2 have something real to read.
DOCUMENTS = {  # file name -> policy text (stands in for data pulled from an HR system or API)
    "leave_policy.md": """
# Leave Policy

Probation employees can take up to 6 casual leaves in the first six months.

Confirmed employees get 12 casual leaves and 15 earned leaves per calendar year.

Sick leave requires a medical certificate if absence exceeds 2 consecutive working days.

Apply leave in the HR portal at least 2 working days before the leave start date for planned leave.
""",
    "wfh_policy.md": """
# Work From Home Policy

Confirmed employees may take up to 8 WFH days per month with manager approval.

WFH is not allowed during the first 30 days of joining unless the manager grants a written exception.

On WFH days, employees must be reachable on company chat between 10:00 AM and 6:00 PM IST.

Festival week WFH needs prior approval from both the manager and HR.
""",
    "reimbursement_policy.md": """
# Reimbursement Policy

Internet reimbursement is capped at 1000 rupees per month for confirmed remote-eligible roles.

Submit bills in the expense tool within 30 days of the bill date.

Cash claims without a GST invoice are rejected for amounts above 500 rupees.
""",
}


def create_corpus() -> None:
    """Write the handbook .md files to disk so the loaders have a real corpus to read."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)  # create handbook_docs/ on the first run
    for file_name, content in DOCUMENTS.items():  # loop over each file name and its policy text
        file_path = DATA_DIR / file_name  # build a path like handbook_docs/leave_policy.md
        file_path.write_text(content.strip(), encoding="utf-8")  # write UTF-8 text to disk
        print(f"Created: {file_path}")  # confirm which file was written


# ===========================================================================
# STAGE 2 — INGEST: LOAD -> SPLIT -> EMBED -> PERSIST IN CHROMA
# ===========================================================================
# This is the OFFLINE prepare path. It turns files into searchable vectors saved on disk, so a
# later run (or the RAG app) can RELOAD them without paying to re-embed every time.
#
#   DocumentLoader  -> read .md files into LangChain Document objects (text + metadata)
#   TextSplitter    -> cut each document into overlapping CHUNKS (one idea per card, when possible)
#   Embeddings      -> map each chunk to a fixed-length vector (similar meaning -> nearby vectors)
#   Chroma          -> store those vectors and support similarity search, PERSISTED to disk
#
# Editing a .md file does NOT update the vectors until you RE-RUN this ingest step. That lag is the
# single most common source of "why is it still answering with the old number?" confusion.

def ingest() -> None:
    """Load the corpus, split it into chunks, embed them, and persist the vectors in Chroma."""
    if CHROMA_DIR.exists():  # only clean up if a chroma_db already exists from a previous run
        shutil.rmtree(CHROMA_DIR)  # delete old vectors so edited policies do not answer from stale text

    loader = DirectoryLoader(  # reads every matching file inside DATA_DIR
        str(DATA_DIR),  # path to the handbook folder, as a string
        glob="**/*.md",  # load ONLY Markdown files (recursively)
        loader_cls=TextLoader,  # treat each matched file as plain text / Markdown
        loader_kwargs={"encoding": "utf-8"},  # read the English text with UTF-8 encoding
    )
    documents = loader.load()  # returns a list of LangChain Document objects (usually 3 here)
    print(f"Original documents loaded: {len(documents)}")

    text_splitter = RecursiveCharacterTextSplitter(  # smart scissors: prefer paragraph/sentence breaks
        chunk_size=800,  # maximum characters per chunk (demo value)
        chunk_overlap=120,  # ~15% shared tail between neighbours so split sentences stay whole somewhere
        add_start_index=True,  # tag each chunk with where it began in the source file
    )
    chunks = text_splitter.split_documents(documents)  # apply the split to the loaded documents
    # With small files, chunk_size=800 may yield ONE chunk per file. Lower it to 100-200 to see
    # multi-chunk splits. Rule: chunk_overlap must always be SMALLER than chunk_size.
    print(f"Chunks generated: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)  # runs the BGE model locally (no API cost)

    vector_store = Chroma(  # connect to (or create) a PERSISTED Chroma database
        collection_name=COLLECTION_NAME,  # the named collection for these handbook chunks
        embedding_function=embeddings,  # model used to embed chunks now and queries later
        persist_directory=str(CHROMA_DIR),  # save vectors under chroma_db/ for reuse
    )
    vector_store.add_documents(chunks)  # embed each chunk and store it in Chroma (persisted to disk)
    print(f"Stored chunks in collection '{COLLECTION_NAME}' at '{CHROMA_DIR}'")


# ===========================================================================
# STAGE 3 — RAG APP: LCEL CHAIN + WITH-vs-WITHOUT RETRIEVAL COMPARISON
# ===========================================================================
# This is the ONLINE answer path. It RELOADS the persisted Chroma (no re-ingest), turns it into a
# retriever, and wires an LCEL chain: retriever -> prompt (+context) -> LLM -> string.
#
# LCEL (LangChain Expression Language) composes components with the pipe (|) operator like LEGO.
# RunnablePassthrough forwards the ORIGINAL question unchanged while the retriever fetches context.
#
# To show WHY retrieval matters, we build a SECOND chain with NO retriever and NO handbook context,
# then run the SAME queries through both and score the answers on grounding.

def format_docs(docs) -> str:
    """Join retrieved Document objects into one context string (a blank line between chunks)."""
    return "\n\n".join(doc.page_content for doc in docs)  # readable separation between chunks


# Grounded prompt: answer ONLY from retrieved context, admit ignorance, and cite the source file.
# These guardrails are what let a manager AUDIT an answer against a real file, not model confidence.
RAG_PROMPT = ChatPromptTemplate.from_template(
    """You are a helpful HR assistant for one company.
Use only the retrieved context to answer the user's question.
If the answer is present in the context, answer clearly.
If the answer is not present in the context, say: I don't know based on the provided documents.
Do not use outside knowledge.
Mention the source file name wherever possible.

Context:
{context}

Question:
{question}
"""
)

# No-retrieval baseline: the SAME model, but with NO handbook context and no honesty guardrail —
# on purpose, so its confident, ungrounded guessing is visible next to the grounded answer.
PLAIN_PROMPT = ChatPromptTemplate.from_template(
    """You are a helpful HR assistant for one company.
Answer the user's question about company policy.
Be clear and confident.

Question:
{question}
"""
)


def run_rag_comparison() -> None:
    """Build the RAG chain and a no-retrieval chain, then contrast them on three queries."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)  # SAME model as ingest, or retrieval breaks

    vector_store = Chroma(  # reload the persisted Chroma — no re-ingest happens in this stage
        collection_name=COLLECTION_NAME,  # same collection name as ingest
        embedding_function=embeddings,  # same embedding function as ingest
        persist_directory=str(CHROMA_DIR),  # same folder as ingest
    )

    retriever = vector_store.as_retriever(  # the search button used inside the LCEL chain
        search_type="similarity",  # rank chunks by vector similarity to the query
        search_kwargs={"k": 3},  # return the top 3 most relevant chunks
    )

    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)  # temperature 0 = stable, factual policy answers

    rag_chain = (  # FULL LCEL RAG pipeline — WITH retrieval
        {
            "context": retriever | format_docs,  # retrieve top-k chunks, then format them into one string
            "question": RunnablePassthrough(),  # forward the user's question unchanged
        }
        | RAG_PROMPT  # fill {context} + {question} into the grounded template
        | llm  # generate the answer under the guardrails
        | StrOutputParser()  # return a plain string (the parentheses are required)
    )

    no_retrieval_chain = (  # SAME model, but NO retriever and NO handbook context
        {"question": RunnablePassthrough()}  # only the question flows forward
        | PLAIN_PROMPT  # a prompt with no context block
        | llm  # generate from the model's own memory alone
        | StrOutputParser()  # return a plain string
    )

    queries = [
        "How many casual leaves can a probation employee take in the first six months?",  # in corpus
        "What is the monthly internet reimbursement cap?",  # in corpus
        "How many pet-care leaves does a confirmed employee get?",  # OUT of corpus (never defined)
    ]

    print("=" * 72)
    print("GROUNDING COMPARISON: WITH vs WITHOUT RETRIEVAL")

    for question in queries:  # run each question through BOTH chains for a side-by-side contrast
        with_rag = rag_chain.invoke(question)  # answer conditioned on retrieved passages
        without_rag = no_retrieval_chain.invoke(question)  # answer with no handbook context at all

        print("\nQ:", question)
        print("\n--- WITH retrieval ---")
        print(with_rag)
        print("\n--- WITHOUT retrieval ---")
        print(without_rag)
        # Score each answer on: source fidelity | citation | refusal honesty | hallucination risk.
        # Style is NOT truth: a fluent wrong number is more expensive than a short grounded answer.
        print("\nScore: source fidelity | citation | refusal honesty | hallucination risk")


# ===========================================================================
# DRIVER — run the three stages back to back so the whole pipeline works end-to-end.
# ===========================================================================
def main() -> None:
    load_dotenv()  # read a local .env file and load its values (e.g. GROQ_API_KEY) into os.environ
    if not os.environ.get("GROQ_API_KEY"):  # fail early with a friendly message, not a stack trace
        raise SystemExit("GROQ_API_KEY is not set. Add it to a .env file: GROQ_API_KEY=your-key-here")

    # STAGE 1 — write the handbook .md files (the corpus the bot may read).
    create_corpus()

    # STAGE 2 — load, split, embed, and persist the vectors in Chroma (the offline prepare path).
    ingest()

    # STAGE 3 — reload Chroma and compare WITH vs WITHOUT retrieval (the online answer path).
    run_rag_comparison()

    # Try it:
    #   1) Change "6 casual leaves" to "8" in handbook_docs/leave_policy.md, then RE-RUN this file.
    #      Watch the probation answer update ONLY after ingest re-embeds — vectors lag raw files.
    #   2) Lower chunk_size to 100-200 in ingest() and re-run — see "Chunks generated" climb above 3.
    #   3) Ask an out-of-corpus question (e.g. pet-care leave) and confirm the RAG chain honestly
    #      says "I don't know..." while the no-retrieval chain may invent a whole fake policy.
    print("=" * 72)
    print("Edit the .md policies, re-run to re-ingest, and the LCEL wiring stays exactly the same.")


if __name__ == "__main__":
    main()  # create the corpus, ingest into Chroma, then run the grounding comparison