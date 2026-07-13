# RAG Tool and Integrated LangChain Agent

## Context of This Session

In the **previous** session you built a **LangChain RAG pipeline** on an **employee handbook**: loaders, chunking, **Chroma**, a **retriever**, and an **LCEL** retrieve-then-generate chain. You also compared answers **with** versus **without** retrieval to judge **grounding**.

That pipeline always searched documents. A real HR helpdesk also needs **non-document tools** (for example, a weekday helper for leave forms) and **memory** for follow-ups like *“And what about after confirmation?”* after a probation leave question. Earlier you already practised **`AgentExecutor`**, **`MessagesPlaceholder`**, and **`chat_history`**.

Today those skills meet: wrap the handbook retriever as a **tool**, add a **second tool**, keep **multi-turn memory**, and score the whole agent with a **compact eval pack**.

**In this session, you will:**

- Design a **retriever-backed tool** with a clear contract next to a **non-retrieval** tool
- Run **multi-turn** handbook Q&A that combines **chat history** and retrieval
- Appraise behaviour with an **eval pack** (in-domain, out-of-domain, tool-first)
- Read **failure signatures** — wrong tool, weak retrieval, over-refusal — to prioritise fixes

---

## Why One Pipeline Is Not Enough

- **Official Definition:** An **integrated LangChain agent** unifies retrieval tools, auxiliary tools, conversational memory, and bounded execution in one workflow.
- **In Simple Words:** One helpdesk that can **search the handbook**, **use another calculator-style tool**, and **remember** earlier turns.
- **Real-Life Example:** An employee asks probation casual-leave limits, then *“Convert 12 June to a weekday for my form,”* then *“And what about after confirmation?”* — three different needs in one chat.

| Skill alone | What it can do | What breaks |
|---|---|---|
| RAG chain only | Grounded policy answers | Searches docs for weekday questions |
| Tools only (no RAG) | Calls calculators / APIs | Invents leave rules |
| Memory only | Smooth follow-ups | Still invents policy |
| All three + eval | Chooses, remembers, and can be judged | Needs clear tool contracts |

**Common doubt:** *Can I keep the LCEL RAG chain and add tools later?* You can for demos. Products usually expose retrieval as a **tool** so the agent can **choose** search versus something else.

![Integrated HR helpdesk — one agent unifies handbook search, weekday helper, and chat memory instead of separate disconnected skills](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session32/session32-integrated-agent-overview.png)

---

## From RAG Chain to Retriever Tool

In the previous RAG lesson, retrieval was **always on** inside the LCEL chain. Here retrieval becomes **optional** — the agent calls it only when the question needs handbook text.

- **Official Definition:** **`create_retriever_tool`** wraps a LangChain **retriever** as a named tool the agent can call like any other `@tool`.
- **In Simple Words:** You turn the Chroma search button into a labelled **“Search handbook”** action on the agent’s desk.
- **Real-Life Example:** Instead of always opening the policy binder, the receptionist opens it only when the visitor asks a policy question.

**Tool contract** means the **name + description** the model reads before choosing. Sharp contracts improve **arbitration** (which tool to pick). Vague contracts cause **wrong-tool** failures.

| Contract piece | Good practice | Weak practice |
|---|---|---|
| **Name** | `handbook_search_tool` | `tool1` |
| **When to use** | Leave, WFH, reimbursement, travel policy | “Use for anything useful” |
| **When not to use** | Dates, weekday names, math | (silent) |
| **What returns** | Relevant handbook passages | “Some text” |

You will reload the **same** persisted Chroma from the previous ingest (`chroma_db`, collection `employee_handbook_docs`). Re-run ingest first if that folder is missing.

![From always-on RAG chain to optional retriever tool — the agent opens the handbook only when a policy question needs it](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session32/session32-rag-chain-to-tool.png)

---

## The Second Tool — Force a Real Choice

A second, **non-retrieval** tool makes arbitration visible. If only one tool exists, every hard question looks like a search problem.

- **Official Definition:** An **auxiliary tool** is a callable capability that is **not** document retrieval — for example date helpers, calculators, or status APIs.
- **In Simple Words:** A second button on the desk that does a **different job**.
- **Real-Life Example:** HR keeps a **calendar widget** for leave forms beside the **policy binder**. Opening the binder for “What weekday is 12 June?” wastes time and may confuse the model.

The auxiliary tool here is **`weekday_for_date`** — it returns the weekday name for a date string like `2026-06-12`. That is a **tool-first** question: the handbook never stores “12 June is a Friday.”

![Tool arbitration — handbook_search_tool for policy questions, weekday_for_date for calendar questions, polite refusal for trivia](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session32/session32-tool-arbitration.png)

---

## Architecture of the Integrated Agent

```
User question
    → AgentExecutor (max_iterations, verbose)
        → may call handbook_search_tool  (Chroma retriever)
        → may call weekday_for_date      (Python helper)
        → may refuse (out of domain)
    → Final answer
    → Append to chat_history for the next turn
```

| Piece | Role |
|---|---|
| **Chroma + retriever** | Same handbook vectors as the previous RAG session |
| **`create_retriever_tool`** | Expose retrieval as `handbook_search_tool` |
| **`@tool weekday_for_date`** | Auxiliary non-retrieval capability |
| **`MessagesPlaceholder("chat_history")`** | Multi-turn continuity |
| **`AgentExecutor`** | Bounded tool loop with traces |
| **Eval pack** | Compact scored cases before you trust the demo |

**Run order:** ensure `chroma_db` exists (from previous ingest) → set `OPENAI_API_KEY` → run `handbook_integrated_agent.py`.

---

## Step 1 — Retriever Tool and Auxiliary Tool

### Install / environment (same stack as previous RAG work)

```bash
pip install langchain langchain-openai langchain-community langchain-chroma langchain-text-splitters chromadb
export OPENAI_API_KEY="your-key-here"
```

### Full code — tools section (part of `handbook_integrated_agent.py`)

```python
from datetime import datetime  # Parse date strings and compute weekday names
from pathlib import Path  # Build paths to the persisted Chroma folder

from langchain.agents import AgentExecutor, create_tool_calling_agent  # Managed tool-calling agent runtime
from langchain.tools.retriever import create_retriever_tool  # Wrap a retriever as an agent tool
from langchain_chroma import Chroma  # Reload persisted handbook vectors
from langchain_core.messages import AIMessage, HumanMessage  # Typed messages for chat_history append
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # Prompt layout + history slots
from langchain_core.tools import tool  # Decorator for the auxiliary weekday tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # Chat model + same embedding model as ingest

CHROMA_DIR = Path("chroma_db")  # Same persist folder as the previous RAG ingest
COLLECTION_NAME = "employee_handbook_docs"  # Same collection name as the previous ingest
EMBEDDING_MODEL = "text-embedding-3-small"  # Must match the model used at ingest time

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)  # Needed to query Chroma with matching vectors

vector_store = Chroma(  # Reload handbook vectors without re-embedding every run
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR),
)

retriever = vector_store.as_retriever(  # Similarity search over handbook chunks
    search_type="similarity",
    search_kwargs={"k": 3},  # Top 3 passages for each handbook search call
)

handbook_search_tool = create_retriever_tool(  # Turn retriever into a named agent tool
    retriever,
    name="handbook_search_tool",
    description=(
        "Search the company employee handbook for leave, WFH, laptop, reimbursement, "
        "and travel policies. Use only for policy and handbook questions. "
        "Do NOT use for weekday names, date math, or general trivia."
    ),
)


@tool  # Register a non-retrieval helper the agent can choose instead of search
def weekday_for_date(date_text: str) -> str:
    """Return the weekday name for a date. Prefer YYYY-MM-DD. Use for leave-form date questions, not policy search."""
    cleaned = date_text.strip()  # Remove accidental spaces around the date
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):  # Accept a few common Indian date formats
        try:
            parsed = datetime.strptime(cleaned, fmt)  # Try parsing with this format
            return f"{cleaned} falls on a {parsed.strftime('%A')}."  # e.g. Friday
        except ValueError:
            continue  # Try the next format
    return "Could not parse the date. Please use YYYY-MM-DD (example: 2026-06-12)."  # Clear failure message


TOOLS = [handbook_search_tool, weekday_for_date]  # Both tools available for arbitration
```

**How the code works:**

- **`Chroma` + `as_retriever`** — reuses the previous session’s handbook index.
- **`create_retriever_tool`** — gives the agent a searchable tool with a **when / when-not** description.
- **`weekday_for_date`** — pure Python; no handbook involved.
- **`TOOLS`** — both tools sit side by side so the model must **choose**.

**Common doubt:** *Why put “Do NOT use for weekday names” in the description?* Because tool choice is driven by text the model reads. Clear negatives reduce **wrong-tool** calls.

### Simple Activity — Predict the Tool

For each question, write **handbook**, **weekday**, or **neither**:

| Question | Your prediction |
|---|---|
| How many casual leaves in probation? | |
| What weekday is 2026-06-12? | |
| Who won the IPL auction this year? | |

---

## Step 2 — Agent, Memory, and Multi-Turn Handbook Q&A

Memory without retrieval forgets the handbook. Retrieval without memory forgets *“that leave limit”* from the last turn. Together they support real chat.

- **Official Definition:** **Multi-turn document Q&A** combines **conversational history** with **retrieval-backed** answers across several user messages.
- **In Simple Words:** The bot remembers what you already asked **and** can search the handbook again when needed.
- **Real-Life Example:** Turn 1: probation casual leaves (handbook says **6** in six months). Turn 2: *“And what about after confirmation?”* — history supplies *casual leaves*; retrieval supplies the confirmed rule (**12** casual / **15** earned).

### Full code — agent + `ask()` (continue in the same file)

```python
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # Low temperature for factual HR answers

prompt = ChatPromptTemplate.from_messages([  # Prompt with history and scratchpad slots
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
    MessagesPlaceholder(variable_name="chat_history", optional=True),  # Past user/assistant turns
    ("human", "{input}"),  # Current user message
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # Current-run tool steps (filled by executor)
])

agent = create_tool_calling_agent(llm=llm, tools=TOOLS, prompt=prompt)  # Build tool-aware agent

agent_executor = AgentExecutor(  # Bounded runtime for the tool loop
    agent=agent,
    tools=TOOLS,
    verbose=True,  # Print tool names and observations so you can diagnose choices
    max_iterations=4,  # Hard stop so the loop cannot run forever
    handle_parsing_errors=True,  # Recover from malformed tool calls when possible
)

chat_history: list = []  # Rolling short-term memory for this process


def ask(user_text: str) -> str:
    """Run one user turn, then append both sides to chat_history."""
    result = agent_executor.invoke(  # Pass current input plus prior turns
        {"input": user_text, "chat_history": chat_history}
    )
    answer = result["output"]  # Final natural-language reply
    chat_history.append(HumanMessage(content=user_text))  # Store user turn
    chat_history.append(AIMessage(content=answer))  # Store assistant turn
    return answer


def demo_multi_turn() -> None:
    """Show retrieval + memory + auxiliary tool in one conversation."""
    chat_history.clear()  # Start a fresh conversation for the demo
    print("\n--- Turn 1: in-domain handbook (expect handbook_search_tool) ---")
    print(ask("According to our handbook, how many casual leaves can a probation employee take in the first six months?"))
    print("\n--- Turn 2: follow-up (needs memory + retrieval again) ---")
    print(ask("And what about after confirmation?"))
    print("\n--- Turn 3: tool-first weekday question ---")
    print(ask("For my leave form, what weekday is 2026-06-12?"))
```

**How the code works:**

- **System prompt** — tells the model **which tool for which job** and when to **refuse**.
- **`chat_history`** — you append after each `ask()`; without append, turn 2 forgets turn 1.
- **`agent_scratchpad`** — short-term tool trace for **this** invoke only; not long chat memory.
- **`verbose=True`** — watch whether the agent picked `handbook_search_tool` or `weekday_for_date`.
- **`max_iterations=4`** — keeps the agent **bounded**.

**Common defect:** Placeholder exists but history is never appended → follow-ups fail even though “memory” looks wired.

![Multi-turn handbook Q&A — chat_history carries context across turns while retrieval and the weekday tool answer each new question](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session32/session32-multi-turn-memory.png)

### Simple Activity — Trace One Multi-Turn Chat

Run `demo_multi_turn()`. Fill this table from the **verbose** log:

| Turn | Expected tool | Tool actually called | Did follow-up use earlier context? |
|---|---|---|---|
| 1 | handbook_search_tool | | (n/a) |
| 2 | handbook_search_tool | | |
| 3 | weekday_for_date | | |

---

## Step 3 — Compact Eval Pack and Failure Signatures

Building is exciting. **Judging** is what makes the workflow professional.

- **Official Definition:** A **compact evaluation set (eval pack)** is a small fixed list of cases with expected behaviour across **in-domain**, **out-of-domain**, and **tool-first** scenarios.
- **In Simple Words:** A short exam paper for your agent — not a full enterprise lab, but enough to catch common mistakes.
- **Real-Life Example:** Before opening an HR bot to all employees, you try three tickets: one real policy question, one nonsense question, one calendar question.

| Scenario type | What it checks | Example |
|---|---|---|
| **In-domain** | Handbook should support the answer | Probation casual-leave limit |
| **Out-of-domain** | Refusal or honest limit when corpus is silent | Pet-care leave / IPL trivia |
| **Tool-first** | Auxiliary tool preferred over retrieval | Weekday for `2026-06-12` |

For **out-of-domain** handbook questions, calling `handbook_search_tool` and then saying *I don’t know based on the documents* is often **correct**. The failure is inventing a confident fake policy — not merely searching once.

### Failure signatures to prioritise fixes

| Signature | What you see | Likely fix first |
|---|---|---|
| **Wrong tool** | Searches handbook for a weekday question (or vice versa) | Sharpen tool descriptions + system prompt |
| **Weak retrieval** | Right tool, wrong or thin passages, fuzzy answer | Chunking / `k` / re-ingest / query wording |
| **Over-refusal** | Handbook has the answer, but agent refuses | Soften refusal rules; check prompt guardrails |

**Common doubt:** *Which failure do I fix first for a live demo?* Usually **wrong tool** — audiences notice a calendar question answered with random policy text immediately. Then **weak retrieval**, then **over-refusal**.

![Compact eval pack and failure signatures — in-domain, tool-first, and out-of-domain cases expose wrong tool, weak retrieval, and over-refusal patterns](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module3/session32/session32-eval-failure-signatures.png)

### Full code — eval pack (same file)

```python
EVAL_PACK = [  # Compact cases spanning the three scenario types
    {
        "id": "in_domain_leave",
        "input": "How many casual leaves can a probation employee take in the first six months?",
        "expect_tool": "handbook_search_tool",  # Should search the handbook
        "scenario": "in-domain",
    },
    {
        "id": "tool_first_weekday",
        "input": "What weekday is 2026-06-12?",
        "expect_tool": "weekday_for_date",  # Should NOT search policies
        "scenario": "tool-first",
    },
    {
        "id": "out_of_domain_pets",
        "input": "How many pet-care leaves does a confirmed employee get?",
        "expect_tool": None,  # Search-then-admit-unknown is OK; inventing pet-care leave fails
        "scenario": "out-of-domain",
    },
    {
        "id": "out_of_domain_trivia",
        "input": "Who won the IPL auction this year?",
        "expect_tool": None,  # Polite refusal — not a handbook question
        "scenario": "out-of-domain",
    },
]


def run_eval_pack() -> None:
    """Run each case on a fresh history so memory bleed cannot fake a pass."""
    print("\n===== EVAL PACK =====")
    for case in EVAL_PACK:
        chat_history.clear()  # Isolate cases — history from case A must not help case B
        print(f"\nCase: {case['id']} ({case['scenario']})")
        print("Q:", case["input"])
        print("Expected tool:", case["expect_tool"])
        answer = ask(case["input"])  # verbose=True shows actual tool calls in the log
        print("A:", answer)
        print(
            "Score mentally: tool choice | grounding | refusal honesty | failure signature"
        )


if __name__ == "__main__":
    demo_multi_turn()  # First: multi-turn demo with memory
    run_eval_pack()  # Then: compact evaluation set
```

**How the code works:**

- **Four cases** — cover in-domain, tool-first, and two out-of-domain shapes.
- **`chat_history.clear()`** between cases — prevents false passes from leftover memory.
- **`expect_tool`** — your checklist while reading the verbose log (this pack does not auto-assert tool names).
- **Mental scoring line** — keeps evaluation **bounded** and easy to repeat.

### Simple Activity — Classify Failures

After `run_eval_pack()`, mark each case:

| Case id | Pass / Fail | If fail: wrong tool / weak retrieval / over-refusal / other |
|---|---|---|
| in_domain_leave | | |
| tool_first_weekday | | |
| out_of_domain_pets | | |
| out_of_domain_trivia | | |

Write one sentence: *Which failure would you fix first before showing this to a manager — and why?*

---

## Putting the Full Script Together

Assemble **one** file named **`handbook_integrated_agent.py`** by stacking the code blocks in order: **imports + tools** (Step 1) → **agent + `ask` + `demo_multi_turn`** (Step 2) → **`EVAL_PACK` + `run_eval_pack` + `__main__`** (Step 3). Keep the file next to `chroma_db` from the previous ingest.

**Checklist before you run:**

1. `handbook_docs/` and `chroma_db/` exist from the previous RAG session (re-run create + ingest if needed).
2. `OPENAI_API_KEY` is exported.
3. Embedding model name matches ingest (`text-embedding-3-small`).
4. You watch **verbose** output for tool names, not only the final sentence.

**Common mistakes and fixes:**

| Symptom | Likely cause | Fix |
|---|---|---|
| Chroma / collection errors | Ingest not run or wrong path | Re-run previous ingest; confirm `chroma_db` |
| Always calls handbook search | Weak auxiliary description | Strengthen “Do NOT use for…” lines |
| Always calls weekday tool | Vague handbook description | List policy topics explicitly |
| Follow-up ignores turn 1 | Missing history append | Append `HumanMessage` + `AIMessage` after each ask |
| Eval cases “pass” wrongly | History reused across cases | `chat_history.clear()` per case |
| Fluent wrong leave number | Weak retrieval or skipped tool | Check verbose log; re-ingest; tune `k` |

---

## Key Takeaways

- **`create_retriever_tool`** turns your handbook retriever into an agent-callable search tool with a clear contract.
- A **second non-retrieval tool** forces real **arbitration** — the agent must choose search versus helper versus refusal.
- **Multi-turn document Q&A** needs both **`chat_history`** and retrieval; either alone is incomplete for helpdesk chat.
- A **compact eval pack** (in-domain, out-of-domain, tool-first) makes quality visible before you celebrate.
- **Failure signatures** — wrong tool, weak retrieval, over-refusal — tell you what to fix first.
- **Upcoming** work can deepen evaluation logging and remediation; today’s habit is to **unify and judge** the whole agent, not only one chain.

---

## Important Commands, Libraries, and Terminologies

| Term / Command | Type | Meaning |
|---|---|---|
| `create_retriever_tool` | Function | Wrap a retriever as a named agent tool |
| `handbook_search_tool` | Tool | Retriever-backed handbook search |
| `weekday_for_date` | Tool | Auxiliary date → weekday helper |
| **Tool contract** | Concept | Name + description that guides tool choice |
| **Tool arbitration** | Concept | Choosing the right tool (or none) for a query |
| `AgentExecutor` / `create_tool_calling_agent` | Runtime | Bounded tool-calling agent loop |
| `MessagesPlaceholder` / `chat_history` | Memory | Rolling conversational history across turns |
| `agent_scratchpad` | Memory | Current-run tool steps only |
| `max_iterations` / `verbose` | Config | Loop limit / print intermediate tool steps |
| **Eval pack** | Concept | Compact in-domain / out-of-domain / tool-first cases |
| **Wrong tool** | Failure | Called search for a helper question (or reverse) |
| **Weak retrieval** | Failure | Right tool, poor passages or ungrounded answer |
| **Over-refusal** | Failure | Refused though documents support the answer |
| `chroma_db` / `employee_handbook_docs` | Store | Persisted handbook vectors from previous ingest |
| `export OPENAI_API_KEY=...` | Shell | Authenticate OpenAI chat + embeddings |
