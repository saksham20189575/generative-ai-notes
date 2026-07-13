# LangChain RAG Pipeline

## Context of This Session

In the **previous** session you attached **rolling conversational memory** to a LangChain agent: **`MessagesPlaceholder`**, **`chat_history`**, multi-turn demos, and **`RunnableWithMessageHistory`**. Memory keeps a chat coherent across turns.

Memory alone still cannot answer company-specific questions. A bot that remembers your name may still invent a leave rule that is wrong for your organisation.

Earlier you learnt **RAG** ideas — load, chunk, embed, store, retrieve, generate. This session re-expresses that idea as a **LangChain** pipeline: **loaders**, **chunking**, **Chroma**, a **retriever**, and an **LCEL RAG chain**, then compares answers **with** versus **without** retrieval.

**In this session, you will:**

- Ingest a small **employee handbook** corpus with LangChain loaders and chunking
- Embed and **persist** vectors in **Chroma** so retrieval stays reproducible across runs
- Build an **LCEL** retrieval-augmented answering chain
- Critique **grounding** by running the **same queries** with and without retrieval

---

## Why RAG Belongs Next to Agent Memory

- **Official Definition:** **Retrieval-Augmented Generation (RAG)** connects an LLM to an external knowledge store so answers can use **your** documents at query time.
- **In Simple Words:** The model **looks up** the right handbook lines before it writes the reply.
- **Real-Life Example:** An HR chatbot must quote **your** casual-leave rule, not a generic internet guess.

| Need | Memory | RAG |
|---|---|---|
| Follow-up like *“What about that leave?”* | Helps — history carries context | Not enough by itself |
| *“How many casual leaves in probation?”* | Does not load the handbook | Retrieves the probation section |
| Trust / audit | Soft — depends on past chat | Stronger — tied to retrieved passages |

**Common doubt:** *Can I just fine-tune on the handbook PDF?* Fine-tuning tweaks style; it is a poor fit for a large, changing policy folder. **RAG** keeps policies searchable and updates when files change.

Both skills matter: **memory** for dialogue continuity, **RAG** for document truth.

![Why RAG looks up the handbook — memory alone may invent leave rules; RAG opens the Leave Policy and answers from it](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session31/session31-why-rag-handbook.png)

---

## The Typical RAG Flow

- **Official Definition:** A RAG pipeline turns a user query into a grounded answer by **retrieving** relevant chunks and **conditioning** generation on that context.
- **In Simple Words:** **Search first, speak second.**
- **Real-Life Example:** Before answering “Can I take WFH on a festival week?”, the bot opens the WFH policy, finds matching lines, then replies.

**Offline prepare path** (once, or when documents change):

```
Handbook files → Document loader → Text splitter → Embeddings → Chroma (persist)
```

**Online answer path** (every user question):

```
User question → Retriever → Prompt + context → LLM → Final answer
```

You will implement both paths, then run the online path **without** retrieval to see grounding quality drop.

![RAG offline prepare path vs online answer path — handbook becomes a vector filing cabinet; each question retrieves passages before the reply](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session31/session31-rag-offline-online.png)

---

## Chunkification — Why Big Handbooks Become Small Chunks

- **Official Definition:** **Chunking** splits long documents into smaller segments suitable for embedding and retrieval.
- **In Simple Words:** You cut a thick rulebook into **index cards**, not one giant card.
- **Real-Life Example:** One embedding for an entire PDF blends leave rules with laptop rules, so a leave question may match the wrong section.

**Why chunk?** Large files are hard to search precisely; one vector for a whole handbook **mixes** topics; retrieval should return a **focused** passage.

**Habits from earlier corpus work:** keep **one idea** per chunk when possible; use **10–20% overlap**; re-chunk and re-ingest when source files change.

![Chunkification — a thick handbook becomes overlapping index cards so each policy idea can be searched precisely](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session31/session31-chunkification.png)

---

## LangChain Components and File Layout

| # | Component | Role |
|---|---|---|
| 1 | **Document loader** | Read `.md` / text files into LangChain **Document** objects |
| 2 | **Text splitter** | Split documents into chunks (`chunk_size`, `chunk_overlap`) |
| 3 | **Embeddings** | Convert each chunk into a numeric vector |
| 4 | **Chroma** | Store vectors and run **similarity search** |
| 5 | **Retriever** | Accepts a query and returns top-k chunks |
| 6 | **LCEL RAG chain** | Pipe retriever → prompt → LLM → output parser |

**Ingest once** until policies change; the **RAG app** reloads persisted Chroma without re-embedding every time.

| File | Purpose |
|---|---|
| `handbook_create_corpus.py` | Write handbook text from a dictionary into `.md` files |
| `handbook_ingest.py` | Load, split, embed, and persist chunks in Chroma |
| `handbook_rag_app.py` | LCEL RAG chain + **with vs without retrieval** comparison |

**Run order:** `python3 handbook_create_corpus.py` → `python3 handbook_ingest.py` (needs `OPENAI_API_KEY`) → `python3 handbook_rag_app.py`

---

## Step 1 — Create the Handbook Corpus

- **Official Definition:** A **corpus** is the collection of source documents your RAG system will search.
- **In Simple Words:** The **folder of policy files** your bot is allowed to read.
- **Real-Life Example:** HR keeps separate files for leave, WFH, and reimbursement — same idea here.

In production, data often arrives as **API text** or a **dictionary**. The first script **writes** Markdown files to disk.

### Install dependencies (once per environment)

```bash
pip install langchain langchain-openai langchain-community langchain-chroma langchain-text-splitters chromadb
```

### Full code — `handbook_create_corpus.py`

```python
from pathlib import Path  # Helps build folder and file paths cleanly

BASE_DIR = Path("handbook_docs")  # Folder where all handbook .md files will live
BASE_DIR.mkdir(parents=True, exist_ok=True)  # Create folder if it does not exist yet

DOCUMENTS = {  # Dictionary: file name -> policy text (simulates data from an API or HR system)
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

for file_name, content in DOCUMENTS.items():  # Loop over each handbook file name and its text
    file_path = BASE_DIR / file_name  # Build full path like handbook_docs/leave_policy.md
    file_path.write_text(content.strip(), encoding="utf-8")  # Write text to disk using UTF-8
    print(f"Created: {file_path}")  # Confirm which file was written
```

**How the code works:**

- **`Path("handbook_docs")`** + **`mkdir(...)`** — creates the target folder on first run.
- **`DOCUMENTS` dictionary** — mimics real HR data that is not already saved as files.
- **`write_text(..., encoding="utf-8")`** — writes three `.md` files ready for LangChain loaders.

### Simple Activity — Inspect Your Corpus

Open `handbook_docs/leave_policy.md`. Underline the **6 casual leaves** rule for probation and the **12 / 15** rule for confirmed employees. You will query these lines later.

---

## Step 2 — Load, Split, Embed, and Persist in Chroma

This is the **ingest** step: turn files into searchable vectors saved on disk so tomorrow’s run can reload them.

### Document loaders

- **Official Definition:** A **document loader** reads external files and returns LangChain **Document** objects (text + metadata).
- **In Simple Words:** A **file reader** that speaks LangChain’s language.
- **Real-Life Example:** A librarian scanning each policy booklet into a standard catalogue card format.

| Class | What it does |
|---|---|
| **`DirectoryLoader`** | Loads **many files** from one folder |
| **`TextLoader`** | Reads **plain text / Markdown** from each matched file |

**Glob `**/*.md`:** load only Markdown. Understand the **step** (load folder → filter → read); look up loader args when formats change (PDF, CSV).

### Text splitter — `RecursiveCharacterTextSplitter`

- **Official Definition:** A **recursive character text splitter** breaks text into chunks using character boundaries, trying sensible separators before hard cuts.
- **In Simple Words:** Smart scissors that prefer breaking at paragraphs or sentences, not mid-word when possible.
- **Real-Life Example:** Cutting a notebook into revision cards — keep one full rule per card when you can.

| Parameter | Demo value | Meaning |
|---|---|---|
| `chunk_size` | `800` | Maximum characters per chunk |
| `chunk_overlap` | `120` | ~15% overlap so split sentences still appear whole somewhere |
| `add_start_index` | `True` | Tags each chunk with its start position in the source file |

Overlap must be **smaller than** chunk size. With small files, `chunk_size=800` may yield **one chunk per file**; try `100` or `200` later to see multi-chunk splits.

### Embeddings and Chroma

- **Official Definition:** **Embeddings** map text to fixed-length vectors so similar meaning → nearby vectors. **Chroma** stores those vectors and supports **similarity search** with optional **local persistence**.
- **In Simple Words:** Each paragraph becomes a **list of numbers**; Chroma is a **searchable filing cabinet** for those lists.
- **Real-Life Example:** *Casual leave* sits closer to *earned leave* than to *internet bill*. Chroma **collections** are like SQL tables (here: `employee_handbook_docs`).

**Same model rule:** use the **same** embedding model at ingest and at query time (`text-embedding-3-small` ≈ 1,536 dimensions).

```bash
export OPENAI_API_KEY="your-key-here"
```

| Term | Meaning |
|---|---|
| **`persist_directory`** | Folder where Chroma **saves** vectors (`chroma_db`) |
| **`collection_name`** | Named bucket inside the database |
| **Persist** | **Save** so the next script reloads without re-embedding |

Persistence makes retrieval **reproducible across runs**. Before re-ingest after policy edits, optionally delete old `chroma_db` with `shutil.rmtree` so stale vectors do not answer from outdated text.

![Ingest into Chroma — load policies, split, embed as vectors, then persist in a reusable filing cabinet](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session31/session31-ingest-chroma.png)

### Full code — `handbook_ingest.py`

```python
import shutil  # Used to optionally delete an old Chroma folder before re-ingest
from pathlib import Path  # Builds paths to handbook and chroma_db folders

from langchain_chroma import Chroma  # LangChain wrapper around Chroma vector database
from langchain_community.document_loaders import DirectoryLoader, TextLoader  # Load many .md files
from langchain_openai import OpenAIEmbeddings  # OpenAI embedding model wrapper
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Splits long text into chunks

DATA_DIR = Path("handbook_docs")  # Folder containing handbook .md files
CHROMA_DIR = Path("chroma_db")  # Local folder where Chroma will persist vectors
COLLECTION_NAME = "employee_handbook_docs"  # Collection name inside Chroma (like a table name)
EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI embedding model used in class

if CHROMA_DIR.exists():  # Only run cleanup if chroma_db already exists
    shutil.rmtree(CHROMA_DIR)  # Delete old vectors (use when handbook files changed)

loader = DirectoryLoader(  # Reads every matching file in DATA_DIR
    str(DATA_DIR),  # Path to handbook folder as a string
    glob="**/*.md",  # Load only Markdown files
    loader_cls=TextLoader,  # Treat each file as plain text / Markdown
    loader_kwargs={"encoding": "utf-8"},  # Read English text with UTF-8 encoding
)
documents = loader.load()  # Returns a list of LangChain Document objects
print(f"Original documents loaded: {len(documents)}")  # Usually 3 handbook files

text_splitter = RecursiveCharacterTextSplitter(  # Standard LangChain splitter
    chunk_size=800,  # Max characters per chunk (demo value)
    chunk_overlap=120,  # Shared tail between neighbouring chunks (~15%)
    add_start_index=True,  # Store where each chunk began in the source file
)
chunks = text_splitter.split_documents(documents)  # Apply splitting to loaded documents
print(f"Chunks generated: {len(chunks)}")  # May equal 3 if each file is shorter than 800 chars

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)  # Wrapper that calls OpenAI embeddings API

vector_store = Chroma(  # Connect to (or create) a persisted Chroma database
    collection_name=COLLECTION_NAME,  # Name of the collection for these handbook chunks
    embedding_function=embeddings,  # Model used to embed chunks and later queries
    persist_directory=str(CHROMA_DIR),  # Save vectors under chroma_db/ for reuse
)
vector_store.add_documents(chunks)  # Embed each chunk and store in Chroma
print(f"Stored chunks in collection '{COLLECTION_NAME}' at '{CHROMA_DIR}'")
```

**How the code works:**

- **`DirectoryLoader`** — batch-loads all `*.md` handbook files.
- **`split_documents`** — turns each file into one or more chunks.
- **`OpenAIEmbeddings` + `Chroma` + `add_documents`** — embeds and persists chunks locally.
- Editing `leave_policy.md` does **not** update vectors until you **re-run ingest**.

### Simple Activity — Re-Ingest After a Policy Change

1. Change **6 casual leaves** to **8** for probation in `leave_policy.md`.
2. Run ingest again.
3. Ask the same probation leave question in the RAG app.
4. Notice the answer still says **6** until you re-ingest — vectors lag behind raw files.

---

## Step 3 — LCEL RAG Chain and Grounding Comparison

### Retriever, LCEL, and guardrails

- **Official Definition:** A **retriever** returns the most relevant chunks for a query. **LCEL** composes components with the **pipe (`|`)** operator. **`RunnablePassthrough`** forwards the input unchanged.
- **In Simple Words:** The retriever is a **search button**; LCEL connects blocks like LEGO; passthrough keeps the **original question** while context is fetched.
- **Real-Life Example:** You ask HR a question verbatim while they pull the leave file.

**Retriever settings:** `search_type="similarity"`, `search_kwargs={"k": 3}` (top 3 chunks).

**RAG chain shape:**

```
{ context: retriever → format_docs, question: RunnablePassthrough() }
    → ChatPromptTemplate → ChatOpenAI → StrOutputParser()
```

**Prompt guardrails:** answer **only** from retrieved context; if missing, say **“I don’t know based on the provided documents.”**; do not use outside knowledge; mention **source file name** when possible.

**Citation:** when the model cites `leave_policy.md`, a manager can check the claim against a real file — not against model confidence alone.

### Grounding comparison criteria

- **Official Definition:** **Grounding** means the answer depends on retrieved context rather than free-form model memory.
- **In Simple Words:** An open-book answer you can check against the pages that were opened.
- **Real-Life Example:** A judge writing from *this* case file versus writing from general legal vibes.

| Criterion | What to check |
|---|---|
| **Source fidelity** | Does the answer match numbers / rules in the handbook? |
| **Citation** | Does it name a source file when possible? |
| **Refusal honesty** | When the corpus is silent, does it admit uncertainty? |
| **Hallucination risk** | Does the no-retrieval answer invent confident-sounding policy? |

| Situation | Typical behaviour |
|---|---|
| **With retrieval** (in-corpus) | Numbers match handbook; easier to audit |
| **Without retrieval** (same query) | Fluent guess; may invent leave counts |
| **With retrieval** (out-of-corpus) | Honest “I don’t know…” if prompt is strict |
| **Without retrieval** (out-of-corpus) | May invent a full fake policy |

![Grounding comparison — with retrieval cites the Leave Policy correctly; without retrieval may invent a fluent wrong leave count](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session31/session31-grounding-comparison.png)

### Full code — `handbook_rag_app.py`

```python
from pathlib import Path  # Path helper for chroma_db constants

from langchain_chroma import Chroma  # Load persisted vector store
from langchain_core.output_parsers import StrOutputParser  # Convert LLM message to plain string
from langchain_core.prompts import ChatPromptTemplate  # Build chat-style prompt with variables
from langchain_core.runnables import RunnablePassthrough  # Pass question through unchanged
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # Chat model + embeddings

CHROMA_DIR = Path("chroma_db")  # Same folder as ingest
COLLECTION_NAME = "employee_handbook_docs"  # Same collection name as ingest
EMBEDDING_MODEL = "text-embedding-3-small"  # Same embedding model as ingest

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)  # Needed to query Chroma with same vectors

vector_store = Chroma(  # Reload persisted Chroma (no re-ingest in this file)
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR),
)

retriever = vector_store.as_retriever(  # Retriever used inside the LCEL chain
    search_type="similarity",
    search_kwargs={"k": 3},
)

def format_docs(docs):  # Join retrieved Document objects into one context string
    return "\n\n".join(doc.page_content for doc in docs)  # Newline between chunks for readability

RAG_PROMPT = ChatPromptTemplate.from_template(  # Grounded prompt: context + question
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

PLAIN_PROMPT = ChatPromptTemplate.from_template(  # No-retrieval baseline: question only
    """You are a helpful HR assistant for one company.
Answer the user's question about company policy.
Be clear and confident.

Question:
{question}
"""
)

llm = ChatOpenAI(model="gpt-4o", temperature=0)  # Low temperature for factual policy answers

rag_chain = (  # Full LCEL RAG pipeline WITH retrieval
    {
        "context": retriever | format_docs,  # Retrieve chunks and format as one string
        "question": RunnablePassthrough(),  # Forward user question unchanged
    }
    | RAG_PROMPT  # Insert context + question into template
    | llm  # Generate answer
    | StrOutputParser()  # Return plain string (note the parentheses)
)

no_retrieval_chain = (  # Same LLM, but NO retriever and NO handbook context
    {"question": RunnablePassthrough()}  # Only the question flows forward
    | PLAIN_PROMPT  # Prompt without a context block
    | llm  # Generate from model knowledge alone
    | StrOutputParser()  # Return plain string
)

queries = [
    "How many casual leaves can a probation employee take in the first six months?",  # In corpus
    "What is the monthly internet reimbursement cap?",  # In corpus
    "How many pet-care leaves does a confirmed employee get?",  # Out of corpus
]

print("GROUNDING COMPARISON: WITH vs WITHOUT RETRIEVAL")

for question in queries:  # Run each question through both chains
    with_rag = rag_chain.invoke(question)  # Answer conditioned on retrieved passages
    without_rag = no_retrieval_chain.invoke(question)  # Answer with no handbook context

    print("\nQ:", question)
    print("\n--- WITH retrieval ---")
    print(with_rag)
    print("\n--- WITHOUT retrieval ---")
    print(without_rag)
    print("\nScore: source fidelity | citation | refusal honesty | hallucination risk")
```

**How the code works:**

- **`rag_chain`** — retrieve top-k chunks, fill `{context}`, generate under guardrails.
- **`no_retrieval_chain`** — same model, **empty of handbook context**, so you see ungrounded fluency.
- **Three queries** — two answerable from corpus; one **pet-care leave** question the handbook never defines.
- **`StrOutputParser()`** needs `()`; policy file edits require **re-running ingest**, not only the app.

### Simple Activity — Fill the Comparison Grid

Run `handbook_rag_app.py`. For each query, tick the criteria:

| Query | With retrieval: fidelity? | Without retrieval: invents? | Better grounded side |
|---|---|---|---|
| Probation casual leaves | | | |
| Internet reimbursement cap | | | |
| Pet-care leaves | | | |

Write one sentence: *For which query was the without-retrieval answer most dangerously confident?*

**Common doubt:** *If without-retrieval sounds nicer, is RAG worse?* No. Style is not truth. A fluent wrong number is more expensive than a short grounded answer.

---

## Common Mistakes and Fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| `OpenAI API key is missing` | Key not exported | `export OPENAI_API_KEY=...` before ingest / app |
| Answer ignores edited `.md` file | Vectors not rebuilt | Re-run **ingest** after handbook changes |
| `StrOutputParser` type error | Missing `()` | Use `StrOutputParser()` in the chain |
| Only 3 chunks for 3 files | `chunk_size` larger than files | Lower `chunk_size` (e.g. 100–200) to practise splits |
| Wrong or vague matches | Chunks too large / no overlap | Tune `chunk_size` and `chunk_overlap` |
| Retrieval quality poor | Different embedding model at query time | Use the **same** `EMBEDDING_MODEL` everywhere |
| No-retrieval answer “wins” on style | Judging by fluency only | Score with the grounding criteria table |

---

## Key Takeaways

- **RAG** lets an LLM answer from **your** handbook via retrieve-then-generate, not by retraining on gigabytes of policy text.
- **LangChain** packages loaders, splitters, embeddings, Chroma, retrievers, and **LCEL** chains into a repeatable pipeline.
- **Persist Chroma** so retrieval is reproducible across runs; re-ingest when source documents change.
- **Chunk size and overlap** control retrieval quality; demo used **800 / 120** on a small corpus.
- **Grounding critique** means comparing the **same queries** with and without retrieval using fidelity, citation, refusal honesty, and hallucination risk.
- **Upcoming** work can attach retrieval as a **tool** on agents; today’s with/without habit prepares you for formal evaluation.

---

## Important Commands, Libraries, and Terminologies

| Term / Command | Type | Meaning |
|---|---|---|
| `handbook_create_corpus.py` | File | Writes handbook `.md` files from a dictionary |
| `handbook_ingest.py` | File | Load → split → embed → persist in Chroma |
| `handbook_rag_app.py` | File | LCEL RAG + with/without retrieval comparison |
| `DirectoryLoader` / `TextLoader` | Class | Load folder / read Markdown text files |
| `RecursiveCharacterTextSplitter` | Class | Split documents into overlapping chunks |
| `chunk_size` / `chunk_overlap` | Params | Max chunk length; repeated margin between chunks |
| `OpenAIEmbeddings` / `text-embedding-3-small` | Embeddings | OpenAI wrapper / 1,536-dim demo model |
| `Chroma` / `persist_directory` / `collection_name` | Vector DB | Persist vectors locally in a named collection |
| `as_retriever()` / `k: 3` | Retrieval | Similarity search returning top 3 chunks |
| **LCEL** / `RunnablePassthrough` | Chain | Pipe components; forward question unchanged |
| `ChatPromptTemplate` / `StrOutputParser()` | Prompt / parse | `{context}` + `{question}` slots; LLM → string |
| **RAG** / **Grounding** / **Citation** | Concepts | Retrieve-then-generate; answer from context; name the source file |
| `export OPENAI_API_KEY=...` | Shell | Authenticate OpenAI calls |
| `shutil.rmtree(chroma_db)` | Code | Optional full reset before re-ingest |
