# lecture32.py — RAG TOOL + INTEGRATED LANGCHAIN AGENT: retriever tool, a second tool,
# multi-turn memory, and a compact eval pack (Session 32)
#
# In Session 31 you built a LangChain RAG PIPELINE on an employee handbook: loaders, chunking,
# Chroma, a retriever, and an LCEL retrieve-then-generate chain. That pipeline ALWAYS searched
# documents. A real HR helpdesk also needs NON-DOCUMENT tools (for example a weekday helper for
# leave forms) and MEMORY for follow-ups like "And what about after confirmation?".
#
# Today those skills meet in ONE agent:
#   * Wrap the handbook retriever as a TOOL (create_retriever_tool) with a clear contract.
#   * Add a SECOND, non-retrieval tool (weekday_for_date) so the agent must ARBITRATE.
#   * Keep MULTI-TURN memory (chat_history + MessagesPlaceholder) so follow-ups work.
#   * Score the whole agent with a COMPACT EVAL PACK (in-domain, out-of-domain, tool-first).
#
# Front-desk analogy: the receptionist has a POLICY BINDER (handbook_search_tool) and a CALENDAR
# WIDGET (weekday_for_date) on the desk. She opens the binder only for policy questions, the
# calendar only for date questions, and politely declines sports trivia. Choosing the right tool
# (or none) is ARBITRATION — driven entirely by the text the model reads in each tool's contract.
#
# The three failure signatures you learn to read:
#   WRONG TOOL      -> searched the handbook for a weekday question (or vice versa)
#   WEAK RETRIEVAL  -> right tool, thin/wrong passages, fuzzy answer
#   OVER-REFUSAL    -> the handbook HAS the answer, but the agent refused
#
# What this file demonstrates (one script, self-contained so it runs end-to-end):
#   STAGE 1 — CREATE the employee-handbook corpus (same .md files as Session 31)
#   STAGE 2 — INGEST: load -> split -> embed -> PERSIST vectors in Chroma on disk
#   STAGE 3 — TOOLS: wrap the retriever as handbook_search_tool + add weekday_for_date
#   STAGE 4 — AGENT: create_tool_calling_agent + AgentExecutor + chat_history + demo_multi_turn
#   STAGE 5 — EVAL PACK: compact scored cases spanning the three scenario types
#
# PREREQUISITES (do these in the terminal BEFORE running this file):
#   python3 -m venv venv && source venv/bin/activate      # (Windows: venv\Scripts\activate)
#   pip install langchain langchain-groq langchain-huggingface langchain-community \
#               langchain-chroma langchain-text-splitters chromadb sentence-transformers python-dotenv
#   echo "GROQ_API_KEY=your-key-here" > .env              # LLM key, loaded via python-dotenv at startup
# Embeddings run LOCALLY (BAAI/bge-small-en-v1.5), so only the Groq LLM needs an API key.
# Run order matters: this script performs all stages in sequence, so a single
#   python3 main.py
# creates the corpus, ingests it into Chroma, builds the integrated agent, runs a multi-turn
# demo, and then runs the compact eval pack.

# Standard library — path building, a clean reset of the vector store, and date parsing.
import os  # os.environ check so we can fail early with a friendly message if the key is missing
import shutil  # shutil.rmtree deletes an old chroma_db so stale vectors never answer from old text
from datetime import datetime  # parse date strings and compute weekday names for the aux tool
from pathlib import Path  # Path builds folder/file paths cleanly across operating systems

# Load environment variables from a local .env file (so GROQ_API_KEY is picked up automatically).
from dotenv import load_dotenv  # reads .env into os.environ before we check for the Groq key
load_dotenv()  # call once at import time so GROQ_API_KEY is available everywhere below

# LangChain agent runtime + retriever-tool wrapper.
# In LangChain 1.x the classic AgentExecutor/create_tool_calling_agent APIs moved out of
# langchain.agents into the separate langchain-classic package (imported as langchain_classic).
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent  # managed tool-calling agent
from langchain_classic.tools.retriever import create_retriever_tool  # wrap a retriever as an agent tool

# LangChain vector store + loaders + splitter + model wrappers.
from langchain_chroma import Chroma  # LangChain wrapper around the Chroma vector database
from langchain_community.document_loaders import DirectoryLoader, TextLoader  # read many .md files
from langchain_text_splitters import RecursiveCharacterTextSplitter  # split long text into chunks
from langchain_huggingface import HuggingFaceEmbeddings  # local BAAI/bge embedding model wrapper
from langchain_groq import ChatGroq  # Groq-hosted chat model wrapper (fast open LLMs)

# LangChain Core — typed messages, prompt template with history slots, and the @tool decorator.
from langchain_core.messages import AIMessage, HumanMessage  # typed messages for chat_history append
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # prompt layout + slots
from langchain_core.tools import tool  # decorator for the auxiliary weekday tool

# ---------------------------------------------------------------------------
# SHARED CONSTANTS — used by BOTH ingest and the agent so they can never drift apart.
# ---------------------------------------------------------------------------
# The golden rule of RAG reproducibility: the SAME embedding model, the SAME collection name, and
# the SAME persist directory must be used at ingest AND at query time, or retrieval silently breaks.
DATA_DIR = Path("handbook_docs")  # folder that will hold the handbook .md files
CHROMA_DIR = Path("chroma_db")  # local folder where Chroma persists vectors between runs
COLLECTION_NAME = "employee_handbook_docs"  # named bucket inside Chroma (like a SQL table name)
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"  # local HuggingFace embedding model (384 dims) used everywhere


# ===========================================================================
# STAGE 1 — CREATE THE HANDBOOK CORPUS (same corpus as Session 31)
# ===========================================================================
# A CORPUS is the collection of source documents your RAG system is allowed to search — here, the
# folder of policy files the agent may read via handbook_search_tool. In production this text
# usually arrives as API text or a dictionary, NOT as files on disk. This stage simulates that: it
# WRITES three Markdown files from a Python dict so the loaders in Stage 2 have something to read.
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
# This is the OFFLINE prepare path (from Session 31). It turns files into searchable vectors saved
# on disk, so the agent can RELOAD them without paying to re-embed every time. Editing a .md file
# does NOT update the vectors until you RE-RUN this ingest step.

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
    print(f"Chunks generated: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)  # runs BAAI/bge locally to embed chunks

    vector_store = Chroma(  # connect to (or create) a PERSISTED Chroma database
        collection_name=COLLECTION_NAME,  # the named collection for these handbook chunks
        embedding_function=embeddings,  # model used to embed chunks now and queries later
        persist_directory=str(CHROMA_DIR),  # save vectors under chroma_db/ for reuse
    )
    vector_store.add_documents(chunks)  # embed each chunk and store it in Chroma (persisted to disk)
    print(f"Stored chunks in collection '{COLLECTION_NAME}' at '{CHROMA_DIR}'")


# ===========================================================================
# STAGE 3 — TOOLS: RETRIEVER TOOL + AUXILIARY WEEKDAY TOOL
# ===========================================================================
# In Session 31 retrieval was ALWAYS ON inside the LCEL chain. Here retrieval becomes OPTIONAL — the
# agent calls handbook_search_tool only when the question needs handbook text. A TOOL CONTRACT is
# the name + description the model reads before choosing: sharp contracts improve ARBITRATION
# (which tool to pick), vague contracts cause WRONG-TOOL failures.

def build_tools() -> list:
    """Reload persisted Chroma, wrap its retriever as a tool, and pair it with a weekday helper."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)  # SAME model as ingest, or retrieval breaks

    vector_store = Chroma(  # reload the persisted Chroma — no re-ingest happens here
        collection_name=COLLECTION_NAME,  # same collection name as ingest
        embedding_function=embeddings,  # same embedding function as ingest
        persist_directory=str(CHROMA_DIR),  # same folder as ingest
    )

    retriever = vector_store.as_retriever(  # similarity search over handbook chunks
        search_type="similarity",  # rank chunks by vector similarity to the query
        search_kwargs={"k": 3},  # top 3 passages for each handbook search call
    )

    handbook_search_tool = create_retriever_tool(  # turn the retriever into a named agent tool
        retriever,
        name="handbook_search_tool",
        description=(  # the CONTRACT — when to use, when NOT to use, what it returns
            "Search the company employee handbook for leave, WFH, laptop, reimbursement, "
            "and travel policies. Use only for policy and handbook questions. "
            "Do NOT use for weekday names, date math, or general trivia."
        ),
    )

    TOOLS = [handbook_search_tool, weekday_for_date]  # both tools sit side by side -> real arbitration
    return TOOLS


@tool  # register a non-retrieval helper the agent can choose INSTEAD of search
def weekday_for_date(date_text: str) -> str:
    """Return the weekday name for a date. Prefer YYYY-MM-DD. Use for leave-form date questions, not policy search."""
    cleaned = date_text.strip()  # remove accidental spaces around the date
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):  # accept a few common Indian date formats
        try:
            parsed = datetime.strptime(cleaned, fmt)  # try parsing with this format
            return f"{cleaned} falls on a {parsed.strftime('%A')}."  # e.g. Friday
        except ValueError:
            continue  # try the next format
    return "Could not parse the date. Please use YYYY-MM-DD (example: 2026-06-12)."  # clear failure message


# ===========================================================================
# STAGE 4 — AGENT, MEMORY, AND MULTI-TURN HANDBOOK Q&A
# ===========================================================================
# Memory without retrieval forgets the handbook. Retrieval without memory forgets "that leave
# limit" from the last turn. Together they support real chat. The system prompt tells the model
# WHICH TOOL for which job and WHEN to refuse; chat_history carries context across turns.

# Module-level handles so demo_multi_turn() and run_eval_pack() share one agent + memory.
agent_executor: AgentExecutor  # bounded runtime for the tool loop (built in build_agent)
chat_history: list = []  # rolling short-term memory for this process


def build_agent() -> AgentExecutor:
    """Build a tool-calling agent with a history-aware prompt and a bounded executor."""
    tools = build_tools()  # handbook_search_tool + weekday_for_date

    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)  # Groq-hosted LLM, low temp for factual HR answers

    prompt = ChatPromptTemplate.from_messages([  # prompt with history and scratchpad slots
        (
            "system",
            (
                "You are an HR helpdesk assistant for one company. "
                "Use handbook_search_tool for leave, WFH, laptop, reimbursement, and travel policy questions. "
                "Use weekday_for_date for weekday or date-format questions on leave forms. "
                "Ground policy answers in retrieved handbook text and mention the source file when possible. "
                "If the handbook does not contain the answer, say you do not know based on the documents. "
                "Refuse politely for unrelated trivia (sports results, celebrity news, stock tips). "
                "Remember facts from earlier turns in this chat."
            ),
        ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),  # past user/assistant turns
        ("human", "{input}"),  # current user message
        MessagesPlaceholder(variable_name="agent_scratchpad"),  # current-run tool steps (filled by executor)
    ])

    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)  # build tool-aware agent

    return AgentExecutor(  # bounded runtime for the tool loop
        agent=agent,
        tools=tools,
        verbose=False,  # print tool names and observations so you can diagnose choices
        max_iterations=4,  # hard stop so the loop cannot run forever
        handle_parsing_errors=True,  # recover from malformed tool calls when possible
    )


def ask(user_text: str) -> str:
    """Run one user turn, then append both sides to chat_history."""
    result = agent_executor.invoke(  # pass current input plus prior turns
        {"input": user_text, "chat_history": chat_history}
    )
    answer = result["output"]  # final natural-language reply
    chat_history.append(HumanMessage(content=user_text))  # store user turn
    chat_history.append(AIMessage(content=answer))  # store assistant turn
    return answer


def demo_multi_turn() -> None:
    """Show retrieval + memory + auxiliary tool in one conversation."""
    chat_history.clear()  # start a fresh conversation for the demo
    print("\n--- Turn 1: in-domain handbook (expect handbook_search_tool) ---")
    print("Q: According to our handbook, how many casual leaves can a probation employee take in the first six months? ")
    print(ask("According to our handbook, how many casual leaves can a probation employee take in the first six months?"))
    print("\n--- Turn 2: follow-up (needs memory + retrieval again) ---")
    print("Q: And what about after confirmation?")
    print(ask("And what about after confirmation?"))
    print("\n--- Turn 3: tool-first weekday question ---")
    print("Q: For my leave form, what weekday is 2026-06-12?")
    print(ask("For my leave form, what weekday is 2026-06-12?"))


# ===========================================================================
# STAGE 5 — COMPACT EVAL PACK AND FAILURE SIGNATURES
# ===========================================================================
# Building is exciting; JUDGING is what makes the workflow professional. An eval pack is a small
# fixed list of cases with expected behaviour across in-domain, out-of-domain, and tool-first
# scenarios. For out-of-domain handbook questions, calling handbook_search_tool and then saying
# "I don't know based on the documents" is often CORRECT — the failure is inventing a fake policy.

EVAL_PACK = [  # compact cases spanning the three scenario types
    {
        "id": "in_domain_leave",
        "input": "How many casual leaves can a probation employee take in the first six months?",
        "expect_tool": "handbook_search_tool",  # should search the handbook
        "scenario": "in-domain",
    },
    {
        "id": "tool_first_weekday",
        "input": "What weekday is 2026-06-12?",
        "expect_tool": "weekday_for_date",  # should NOT search policies
        "scenario": "tool-first",
    },
    {
        "id": "out_of_domain_pets",
        "input": "How many pet-care leaves does a confirmed employee get?",
        "expect_tool": None,  # search-then-admit-unknown is OK; inventing pet-care leave fails
        "scenario": "out-of-domain",
    },
    {
        "id": "out_of_domain_trivia",
        "input": "Who won the IPL auction this year?",
        "expect_tool": None,  # polite refusal — not a handbook question
        "scenario": "out-of-domain",
    },
]


def run_eval_pack() -> None:
    """Run each case on a fresh history so memory bleed cannot fake a pass."""
    print("\n" + "=" * 72)
    print("===== EVAL PACK =====")
    for case in EVAL_PACK:
        chat_history.clear()  # isolate cases — history from case A must not help case B
        print(f"\nCase: {case['id']} ({case['scenario']})")
        print("Q:", case["input"])
        print("Expected tool:", case["expect_tool"])
        answer = ask(case["input"])  # verbose=True shows actual tool calls in the log
        print("A:", answer)
        # Read the verbose log and score: tool choice | grounding | refusal honesty | failure signature.
        # Failure signatures: WRONG TOOL | WEAK RETRIEVAL | OVER-REFUSAL.
        print("Score mentally: tool choice | grounding | refusal honesty | failure signature")


# ===========================================================================
# DRIVER — run every stage back to back so the whole agent works end-to-end.
# ===========================================================================
def main() -> None:
    global agent_executor  # so ask() can reach the executor built here

    if not os.environ.get("GROQ_API_KEY"):  # fail early with a friendly message, not a stack trace
        raise SystemExit("GROQ_API_KEY is not set. Add it to a .env file: GROQ_API_KEY='your-key-here'")

    # STAGE 1 — write the handbook .md files (the corpus the agent may read).
    create_corpus()

    # STAGE 2 — load, split, embed, and persist the vectors in Chroma (the offline prepare path).
    ingest()

    # STAGE 3 + 4 — build the integrated agent (tools + memory + bounded executor).
    agent_executor = build_agent()

    # STAGE 4 — multi-turn demo: memory + retrieval + the weekday tool in one conversation.
    demo_multi_turn()

    # STAGE 5 — compact evaluation set: in-domain, tool-first, and two out-of-domain shapes.
    run_eval_pack()

    # Try it:
    #   1) Weaken the weekday tool description (remove "not policy search") and re-run — watch the
    #      agent start SEARCHING the handbook for date questions (a WRONG-TOOL signature).
    #   2) Comment out the two chat_history.append lines in ask() — Turn 2 ("after confirmation?")
    #      loses context and the follow-up breaks even though the placeholder still exists.
    #   3) Add your own out-of-domain case to EVAL_PACK and confirm the agent refuses honestly
    #      instead of inventing a confident fake policy.
    print("\n" + "=" * 72)
    print("Unify (retrieval tool + aux tool + memory) and JUDGE the whole agent, not one chain.")


if __name__ == "__main__":
    main()  # create corpus, ingest, build the agent, run the multi-turn demo, then the eval pack
