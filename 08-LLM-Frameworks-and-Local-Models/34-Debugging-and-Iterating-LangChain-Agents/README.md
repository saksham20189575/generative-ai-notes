# Debugging and Iterating LangChain Agents

## Context of This Session

In the **previous** class you built a full **evaluation harness** for a LangChain agent — **eval JSON**, a **runner**, **results.csv**, **failure traces**, and timing logs.

That harness answers: *what broke, and what path did the agent take?* This session closes the loop on **fixing** agents systematically — not by guessing, not by rewriting everything at once, and not by blaming *"the model is bad."*

**In this session, you will:**

- Group mistakes into **failure classes** and pick the right **remediation** for each
- Apply **prompt patching**, **tool patching**, and **retrieval tuning** as controlled fixes
- Track **quality metrics**, **token usage**, and **latency**, including the **cost–latency trade-off**
- See how **chunk size** and **overlap** change the answer on the same RAG query

![From evaluation harness to iteration loop — eval JSON and traces identify failure classes; prompt, tool, and retrieval patches improve quality metrics before ship](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session34/session34-01-eval-to-iteration-loop.png)

---

## What Is Debugging?

- **Official Definition:** **Debugging** is finding the **root cause** of incorrect behaviour and applying a fix so the system works as expected.
- **In Simple Words:** Something is broken — you hunt **where** and **why**, then repair it.
- **Real-Life Example:** A **UPI payment** fails. Debugging checks **network**, **wrong PIN**, or **server downtime** — not shouting at the app.

A **bug** is any error or unexpected behaviour in code. Debugging always has two parts:

1. **Find** the exact place or step where things go wrong.
2. **Fix** the root cause — not just the symptom.

For a simple maths function, debugging is easy: input `2 + 2`, expected output `4`. If you get `5`, the function is wrong. Agentic applications are not that simple — and that is where today's mindset begins.

---

## Why Agent Debugging Is Harder Than Traditional Apps

```
User question → LLM reasons → tool call → tool output → maybe another tool → final answer
```

In a **traditional** app, you often compare **one input** to **one output**. In an **agentic** workflow, the journey has many steps — and the agent can fail for dozens of reasons at any of them:

- **Wrong data** in the knowledge base
- **Over-refusal** on a valid question
- **Under-refusal** on an out-of-domain question
- **Bad prompt** so the LLM misunderstands
- **Wrong arguments** passed to a tool
- **Missing API key** so a tool times out
- **Slow vector database** so retrieval lags

You cannot debug this with input–output alone. You must inspect **which step** failed.

- **Common mistake:** Saying *"the LLM is bad"* and swapping models first. Check **prompt**, **tools**, and **retrieval** before blaming the model.
- **Common mistake:** Reading only the **final answer** when the bug is in the **trajectory** — wrong tool, thin context, or a bad argument.

Each box in the workflow diagram is a place where debugging can start.

![Simple input-output apps vs multi-step agent workflows — many failure points across prompt, tool choice, arguments, retrieval, and final text](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session34/session34-02-simple-io-vs-agent-workflow.png)

### Activity — Spot the Failure Layer

User asks: *"What is my order refund status for order #8821?"* Agent replies: *"I cannot help with weather queries."*

1. Is the **final sentence** the main problem, or the **path**?
2. Name one likely **failure class**.

**Suggested:** The **path** is wrong — likely **over-refusal** or **wrong tool selection**.

---

## Failure Class — Grouping Defects Before You Fix

- **Official Definition:** A **failure class** is a **category of defect** responsible for an incorrect agent response.
- **In Simple Words:** A **label** for *what kind of mistake* happened — like sorting hospital cases into fracture vs fever before treatment.
- **Real-Life Example:** At a **railway complaint desk**, delays are filed under signal fault, crew shortage, or weather — each needs a different fix team.

**Name the defect type first**, then pick the matching remedy.

---

## Eight Common LangChain Agent Failure Classes

### 1. Wrong Tool Selection

The agent calls a tool that does not fit the question.

- **Example:** User asks about **return policy**, but the agent calls **get ticket status**.
- **Likely causes:** Vague **tool name**, weak **tool description**, unclear **system prompt**.
- **Why it hurts:** Even a fluent final answer is untrustworthy if the wrong backend was used.

### 2. Missing Tool Call

The agent answers **without** calling a tool when it should have.

- **Example:** User asks for **live order status**, but the model guesses from memory instead of calling **get_order_status**.
- **Likely causes:** Prompt does not list tools clearly; no instruction that certain queries **require** a tool.
- **Fix hint:** Sometimes adding the word **must** — *"You must call this tool for order queries"* — changes behaviour.

### 3. Bad Tool Arguments

Right tool, wrong **inputs**.

- **Official Definition:** **Arguments** are the **parameters** passed into a tool — order ID, date range, etc.
- **In Simple Words:** Correct door, wrong flat number.
- **Example:** `get_refund_status(order_id="")`.

### 4. Weak Retrieval

- **Official Definition:** **Weak retrieval** means vector search returns **irrelevant or insufficient chunks**.
- **In Simple Words:** Right library, wrong shelf — or only half a page.
- **Real-Life Example:** A coaching bot fetches **chemistry** notes for a **maths** doubt.

| Cause | What to check |
|---|---|
| Corpus missing facts | Tuning cannot invent missing policy text |
| **K** too low / too high | Start near **3–5**; too high adds noise |
| Wrong **search type** | Compare **similarity** vs **MMR** |
| Bad **chunking** | Keyword and answer land in different chunks |

- **Remember:** Similarity search is **probabilistic** — it finds *nearby* text, not guaranteed exact phrase matches.

### 5. Hallucinated Final Response

Confident answer without support — often after **weak retrieval**. Detect via groundedness checks and thin-context traces.

### 6. Over-Refusal and Under-Refusal

- **Over-refusal:** refuses **valid in-domain** questions.
- **Under-refusal:** answers **out-of-domain** questions it should block.
- Watch **refusal rate** over time — a jump from ~5% to ~30% is an incident.

### 7. Excessive Tool Calling (Loops)

Agent retries tools endlessly (API down). Cap with **`max_iterations`**. Like a lift that keeps reopening doors — you need a maximum retry.

### 8. Slow Response (High Latency)

Answer is correct but too slow. Measure start/end time per tool and per request; at scale you need **observability**, not manual timing.

### Activity — Match Symptom to Failure Class

| Symptom | Failure class |
|---|---|
| Cites policy text never in retrieved chunks | Hallucinated / weak grounding |
| GST math routed to document search | Wrong tool selection |
| Valid refund gets *"I cannot help"* | Over-refusal |
| Refund API called with empty `order_id` | Bad tool arguments |
| Same search tool fires six times until timeout | Excessive tool calling |

---

## Final Answer vs Trajectory Debugging

- **Official Definition:** **Trajectory debugging** inspects the **step-by-step path** — tools, retrievals, intermediate messages — not only the last string.
- **In Simple Words:** Checking **how the student solved the sum**, not only the final number.
- **Real-Life Example:** A failed delivery — track warehouse → hub → rider, not only *"not delivered"* on the app.

| Debug style | What you compare | Enough for agents? |
|---|---|---|
| **Final answer** | Expected vs actual text | Never alone |
| **Trajectory** | Tools, retrievals, refusals vs expected steps | Yes — professional practice |

Your **evaluation harness** from the **previous** class is built for trajectory thinking.

![Final answer debugging vs trajectory debugging — compare only the last sentence or inspect tools, retrievals, and refusals step by step](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session34/session34-03-trajectory-vs-final-answer.png)

---

## Remediation Strategies by Defect Category

Once you label a **failure class**, apply a **targeted fix** — not a random full rewrite.

| Failure class | Remediation strategy |
|---|---|
| **Wrong tool selection** | **Tool patch** — clearer name/description; prompt examples |
| **Missing tool call** | **Prompt patch** — *"You **must** call [tool] for [query type]"* |
| **Bad tool arguments** | **Tool patch** — tighten schema; validate inputs |
| **Weak retrieval** | **Retrieval tune** — K, search type, filters, corpus |
| **Hallucinated response** | **Prompt patch** — answer only from context; refuse if thin |
| **Over-refusal** | **Prompt patch** — relax overly strict in-domain guardrails |
| **Under-refusal** | **Prompt patch** — tighten out-of-scope rules |
| **Excessive tool calling** | Set **`max_iterations`**; fix retry logic |
| **High latency** | Cut unnecessary calls; add **caching** |

- **One change at a time** — otherwise nobody knows what helped.
- **Regression risk:** fix one case, break three others — re-run the **full** evaluation set.

![Failure class to remediation map — wrong tool, missing call, weak retrieval, hallucination, loops, and latency each have a targeted patch strategy](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session34/session34-04-failure-class-remediation.png)

### Activity — Pick the First Fix

**Case A:** Five arithmetic failures all called **`search_course_policy`** instead of **`calculate_gst`**.  
**Case B:** Agent invents baby-product returns; corpus has no baby policy; retrieved chunks empty/irrelevant.

**Suggested:** A → wrong tool → **tool patch** (+ small *must call* prompt). B → weak retrieval / hallucination → **retrieval tune** first, then grounding prompt patch.

---

## Observability and Monitoring

- **Official Definition:** **Observability** is understanding system health from **metrics, logs, and traces**.
- **In Simple Words:** **CCTV plus alarms** for your agent.
- **Real-Life Example:** A **Swiggy**-scale chatbot cannot time each chat by hand — dashboards plot latency automatically.

| Signal | Why it matters |
|---|---|
| **Latency** | Users leave slow chats |
| **Failure count** | Spikes show broken tools or bad deploys |
| **Token usage** | Direct **cost** on LLM bills |

**Healthy range mental model:** most responses sit in a **1–2 second** band. Drift to **3 seconds** → raise a level-1 alert. Climbing further → escalate. You set a **cutoff threshold** — e.g. alert if p95 latency **> 3 seconds**. Same pattern for error rate and token spikes. This extends the timing logic from the **previous** evaluation lab into production dashboards.

---

## Prompt Patching, Tool Patching, and Retrieval Tuning

### Prompt Patch

- **Official Definition:** A **focused edit** to system or agent instructions.
- **In Simple Words:** Fix one paragraph in the instruction manual, not the whole book.
- **Example:** Add stricter out-of-domain refusal language.

### Tool Patch

- **Official Definition:** Update a tool's **name, description, schema, or output shape**.
- **In Simple Words:** Rewrite a teammate's job description so work is assigned correctly.
- **Example:** Rename `tool1` → `search_return_policy` with refund/cancellation language.

### Retrieval Tune

- **Official Definition:** Adjust how documents are **split, embedded, and searched** — chunk size, overlap, K, algorithm.
- **In Simple Words:** Reorganise library shelves so the right chapter lands on the desk.
- **Knobs:** `chunk_size`, `chunk_overlap`, `k`, `search_type`, metadata filters.

**Demo workflow:** `langchain_rag_ingest.py` (load → split → embed → Chroma) then `langchain_rag_app.py` (retriever + prompt + LLM). Only **ingest settings** change between a failed and passing run on the **same query**.

---

## Quality Metrics — Measuring Agent Health

- **Official Definition:** **Quality metrics** are measurable indicators of accuracy, safety, speed, and cost.
- **In Simple Words:** The **report card** you track week after week.
- **Real-Life Example:** A call centre tracks handle time, first-call resolution, and complaint rate.

| Metric | What it checks |
|---|---|
| **Response / tool / argument accuracy** | Correct answer, expected tool, valid inputs |
| **Retrieval accuracy / groundedness** | Useful chunks; answer supported by evidence |
| **Refusal accuracy** | Correct refuse vs answer decision |
| **Latency / token utilization** | Speed and cost |

**Watching trends:** If daily tokens rise **30–50%** with no traffic spike, investigate prompt bloat, higher **K**, or runaway tool loops. A **10%** drift might be seasonal noise — **2×** growth is not.

**Quantify improvement:** re-run the **same runner** on the **same eval cases** after each patch; compare pass counts and failure-class totals in **results.csv**. That before/after discipline proves a fix worked.

**When to stop:** agree a **quality bar** — e.g. *90% pass on in-domain, zero fabrication on out-of-domain, latency under 2s in testing*. Try **10–20** retrieval combinations in real projects, then stop when metrics meet the bar or **marginal gains** no longer justify cost and latency.

---

## Cost vs Latency Trade-Off

- **Official Definition:** A **trade-off** means gaining one benefit by accepting a cost elsewhere.
- **In Simple Words:** Something for something — better performance often costs more money or time.
- **Real-Life Example:** A high-end laptop is fast, but you choose how much performance your budget allows.

| Change | Quality effect | Cost / latency effect |
|---|---|---|
| Higher **K** (3 → 5) | Often better answers | More **input tokens** → higher bill |
| Larger / better LLM | Stronger reasoning | Higher per-token price |
| **Caching** repeated queries | Same quality for repeats | Lower average latency and cost |

- **Common mistake:** Doubling **K** and **chunk size** together, then wondering why the bill doubled — tune **one** knob, measure, decide.

### Activity — Trade-Off Decision

Agent passes **17 of 20** cases. Raising **K** from 3 to 8 fixes two more but **doubles** average tokens. Will accuracy rise? What happens to token utilization? Would you ship if cost-per-query is capped? Articulate **quality gained** vs **money spent**.

---

## Hands-On Retrieval Tuning — Chunk Size and Overlap Demo

Same query every run: *"What is the return window for electronics items?"*

With **`chunk_size=50`**, **`chunk_overlap=10`**: many tiny chunks; search matches **"electronics"** in one chunk while *"return within seven days"* lives in another → *"I don't know based on the provided documents."* That is **weak retrieval from bad chunking**, not a bad LLM.

With **`chunk_size=150`**, **`chunk_overlap=20`**: richer chunks contain **both** category and policy → correct answer. **Same files, same app code**, only ingest parameters changed.

![Chunk tuning demo — chunk_size 50 retrieved electronics but missed the 7-day rule; chunk_size 150 returned the correct answer on the same query](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session34/session34-05-chunk-tuning-electronics-demo.png)

Retriever knobs in the app (no re-ingest needed for `k` / `search_type`):

```python
retriever = vector_store.as_retriever(  # Turn Chroma store into a retriever
    search_type="similarity",  # Try "mmr" in your own experiments
    search_kwargs={"k": 3},  # Compare k=3 vs k=5
)
```

**Chunk size** changes require **re-running ingest**.

### Full Code — `langchain_rag_ingest.py`

Set **`OPENAI_API_KEY`**. Policy `.md` files should exist in `documents/`.

```python
import shutil  # Delete old Chroma folder when re-ingesting with new chunk settings
from pathlib import Path  # Paths to documents/ and chroma_db/

from langchain_chroma import Chroma  # Vector database wrapper
from langchain_community.document_loaders import DirectoryLoader, TextLoader  # Load .md policies
from langchain_openai import OpenAIEmbeddings  # Embedding API wrapper
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Split text into chunks

DATA_DIR = Path("documents")  # Folder with return_policy.md etc.
CHROMA_DIR = Path("chroma_db")  # Persisted vectors on disk
COLLECTION_NAME = "e_commerce_policy_docs"  # Collection name inside Chroma
EMBEDDING_MODEL = "text-embedding-3-small"  # Must match the app file at query time

CHUNK_SIZE = 150  # Class demo: 50 failed electronics query; 150 fixed it
CHUNK_OVERLAP = 20  # Shared tail characters between neighbouring chunks

if CHROMA_DIR.exists():  # Clean slate when chunk settings change
    shutil.rmtree(CHROMA_DIR)  # Old vectors were built with different splits

loader = DirectoryLoader(  # Load every Markdown policy file
    str(DATA_DIR), glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"},
)
documents = loader.load()  # List of Document objects
print(f"Original documents loaded: {len(documents)}")

text_splitter = RecursiveCharacterTextSplitter(  # Standard recursive splitter
    chunk_size=CHUNK_SIZE,  # Max characters per chunk
    chunk_overlap=CHUNK_OVERLAP,  # Margin so sentences are not cut in half
    add_start_index=True,  # Track where each chunk started
)
chunks = text_splitter.split_documents(documents)  # Apply splitting
print(f"Chunks generated: {len(chunks)}")  # Compare runs: many tiny vs fewer rich

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)  # Same model for ingest and query
vector_store = Chroma(collection_name=COLLECTION_NAME, embedding_function=embeddings, persist_directory=str(CHROMA_DIR))
vector_store.add_documents(chunks)  # Embed and store every chunk
print(f"Stored {len(chunks)} chunks in '{COLLECTION_NAME}' at '{CHROMA_DIR}'")
```

**How the code works:** **`CHUNK_SIZE` / `CHUNK_OVERLAP`** are the main ingest-time tune levers; **`shutil.rmtree`** avoids stale vectors; print **chunk count** after each experiment; re-run the app with the **same question** to compare.

### Full Code — `langchain_rag_app.py`

```python
from pathlib import Path  # Path constants

from langchain_chroma import Chroma  # Load persisted Chroma
from langchain_core.output_parsers import StrOutputParser  # LLM output → plain string
from langchain_core.prompts import ChatPromptTemplate  # Template with {context} and {question}
from langchain_core.runnables import RunnablePassthrough  # Pass question through unchanged
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # Chat + embeddings

CHROMA_DIR = Path("chroma_db")  # Must match ingest script
COLLECTION_NAME = "e_commerce_policy_docs"  # Must match ingest script
EMBEDDING_MODEL = "text-embedding-3-small"  # Must match ingest script

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)  # Required to query existing vectors
vector_store = Chroma(collection_name=COLLECTION_NAME, embedding_function=embeddings, persist_directory=str(CHROMA_DIR))
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})  # Retrieval tune knobs


def format_docs(docs):  # Join retrieved chunks into one context block
    return "\n\n".join(doc.page_content for doc in docs)


prompt = ChatPromptTemplate.from_template(  # Prompt patch target: edit guardrails here
    """You are a helpful customer support assistant for an e-commerce company.
Use only the retrieved context to answer the user's question.
If the answer is present in the context, answer clearly.
If the answer is not present in the context, say: I don't know based on the provided documents.
Do not use outside knowledge.
Do not answer any out-of-domain query strictly.
Mention the source file name wherever possible.

Context:
{context}

Question:
{question}
"""
)

llm = ChatOpenAI(model="gpt-4o", temperature=0)  # Low temperature for factual answers
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}  # Retrieve then format
    | prompt
    | llm
    | StrOutputParser()  # Note the parentheses — common syntax mistake
)

question = "What is the return window for electronics items?"  # Same query every tuning run
answer = rag_chain.invoke(question)
print("\nQ:", question)
print("A:", answer)  # Expect grounded 7-day rule after chunk_size=150 ingest
```

**How the code works:** ingest controls **what** is stored; retriever `k` / `search_type` control **what** is fetched; the prompt is your **prompt-patch** surface for grounding and refusal.

### Simple Activity — Two-Ingest Comparison

1. Ingest with **`CHUNK_SIZE=50`**, **`CHUNK_OVERLAP=10`**; run the app question; note the answer.
2. Ingest with **`CHUNK_SIZE=150`**, **`CHUNK_OVERLAP=20`**; run the same question.
3. One sentence: *Why did search find "electronics" but still fail the first time?*

### Simple Activity — Prompt Patch vs Retrieval Tune

Circle **prompt patch**, **tool patch**, or **retrieval tune** as the **first** fix:

1. Invents baby-item returns — no baby policy; retrieval returns junk.
2. Uses `search_policy` for a GST calculation question.
3. Answers general-knowledge questions on a course-only bot.

---

## Optimizing Cost Without Breaking Quality

When the agent works but the **bill** is too high, common levers from class:

| Lever | Idea |
|---|---|
| **Dynamic LLM selection** | Cheap model for simple queries; premium only for hard ones |
| **Limit tool calls** | Stop redundant retrieval on every turn |
| **Ideal top K** | Do not retrieve more chunks than you need |
| **Shrink prompts** | Pass only relevant context — not huge files every time |
| **Smaller right-sized chunks** | Fewer tokens per prompt when chunks fit the answer |
| **Caching** | Store answers or retrieval results for repeated questions |

**Cost is measured in tokens** — input tokens plus output tokens. Bigger prompts and more chunks mean bigger invoices.

---

## Closing the Quality Loop

- **Evaluation** tells you **what** failed.
- **Failure classes** tell you **which category** of bug it is.
- **Prompt / tool / retrieval fixes** are **controlled patches**.
- **Metrics** (accuracy, latency, tokens) tell you if life got better.
- **Trade-offs** remind you that **perfect** is expensive — pick a bar and ship.

Upcoming work builds on these habits: measure, patch **one layer at a time**, and re-run the same harness before you celebrate a fix.

---

## Key Takeaways

- **Debugging** agents means tracing **workflows** — not only comparing final text.
- **Failure classes** point to **specific remedies** (prompt, tool, or retrieval).
- Prefer small **patches** over rewriting the whole system.
- **Observability** (latency, failures, tokens) with thresholds matters at production scale.
- **Chunk size and overlap** can make the **same RAG query** succeed or fail without changing the LLM.
- **Quality metrics** and **cost–latency trade-offs** decide when an agent is **good enough** to ship.

---

## Important Commands, Libraries, and Terminologies

| Term / Command | Type | Meaning |
|---|---|---|
| **Failure class** | Concept | Category of defect behind a bad agent response |
| **Trajectory debugging** | Concept | Inspect tools, retrievals, messages — not only final text |
| **Prompt / tool patch / retrieval tune** | Practice | Small controlled fixes to instructions, tools, or search |
| **Observability** | Concept | Metrics, logs, traces for production health |
| **Groundedness / token utilization / latency** | Metric | Evidence support, cost signal, response time |
| **Cost–latency trade-off** | Concept | Quality/speed gains vs money and time |
| **`max_iterations`** | Config | Cap agent loops to prevent runaway tools |
| **`chunk_size` / `chunk_overlap`** | Param | Ingest-time chunking knobs |
| **`search_type` / `k`** | Param | Retriever algorithm and top-k count |
| **`langchain_rag_ingest.py`** | File | Load, split, embed, persist Chroma |
| **`langchain_rag_app.py`** | File | LCEL RAG chain with guardrail prompt |
| **`RecursiveCharacterTextSplitter`** | Class | LangChain text splitter |
| **`python3 langchain_rag_ingest.py`** | Command | Rebuild vectors after chunk changes |
| **`python3 langchain_rag_app.py`** | Command | Run grounded Q&A against Chroma |
| **Caching** | Technique | Reuse prior answers or retrievals to cut latency/cost |
| **Wrong tool / missing call / bad args** | Failure class | Tool-path defects to remediate first |
| **Over-refusal / under-refusal** | Failure class | Guardrail too strict or too loose |
| **Weak retrieval / hallucination** | Failure class | Search or grounding defects |
