# Hands-On Real-World Use Cases

## Context of This Session

In the **previous** session, you learned how to **debug and iterate** LangChain agents systematically — classifying failures, applying **prompt patches**, **tool patches**, and **retrieval tuning**, then measuring improvement with **quality metrics** and **cost–latency trade-offs**.

All of that was about **fixing** a single agent. Now you take a step forward — you apply those skills to **real-world domains**. This session moves from theory and isolated fixes to building and evaluating an agent that solves an actual business problem.

**In this session, you will:**

- Compare how **finance**, **HR onboarding**, and **content creation** agents differ in data, tools, memory, and guardrails
- Design an **HR onboarding assistant** architecture from scratch
- Implement the HR agent by extending the **LangChain stack** you already know
- Evaluate it with **structured test cases** covering grounded answers, tool use, refusal, and multi-turn continuity
- Demonstrate it live with **in-domain** and **out-of-corpus** queries and discuss residual risks

---

## Why Real-World Use Cases Matter

- **Official Definition:** A **use case** is a specific scenario in which a system is used to achieve a defined goal.
- **In Simple Words:** It is the *actual job* you are hiring the agent to do — not a toy example, but something a real company would pay for.
- **Real-Life Example:** Think of a **Zomato** delivery bot vs a **Zerodha** portfolio bot. Both are chatbots, but the data they need, the tools they call, and the mistakes they must avoid are completely different.

Building agents in a vacuum teaches you mechanics. Building agents for **real domains** teaches you **judgment** — what to include, what to guard against, and where the risks hide.

---

## Contrasting Three Single-Agent Workflows

Before building the HR agent, it helps to see how **three different domains** shape agent design differently. Each domain has its own data sources, tools, memory needs, and guardrails — even though the underlying LangChain architecture is the same.

### Finance Due-Diligence Agent

| Dimension | Finance agent |
|---|---|
| **Data sources** | Regulatory filings (annual reports, SEBI disclosures), financial ratios, market data APIs |
| **Tools** | Calculator for ratios, document search over filings, live market-price lookup |
| **Memory / retrieval** | Long-context retrieval — a single filing can be 200+ pages; chunk size must be large enough to keep tables intact |
| **Guardrails** | Must **never** give buy/sell advice (regulatory risk); must cite source document and page; must refuse personal financial questions |

- **Key risk:** Hallucinated numbers in a financial context can cause **legal liability**. Groundedness checks are non-negotiable.
- **Operational note:** Latency tolerance is higher — an analyst waiting 10 seconds for a well-sourced answer is acceptable. A wrong answer is not.

### HR Onboarding Agent

| Dimension | HR onboarding agent |
|---|---|
| **Data sources** | Company handbook, leave policy, IT setup guide, benefits FAQ, org chart |
| **Tools** | Document search over HR corpus, ticket-creation tool for IT requests, escalation tool for unknown queries |
| **Memory / retrieval** | Medium-length documents; policies are usually 1–5 pages each; chunk sizes of 150–300 work well |
| **Guardrails** | Must not answer **salary negotiation** or **disciplinary** questions; must escalate unknowns to HR team; must handle **multi-turn** context (employee asks follow-up) |

- **Key risk:** Giving wrong leave-balance or benefits information creates **employee trust** damage.
- **Operational note:** New joiners ask many questions in the first week — the agent must handle **volume** and **varied** query types.

### Content Creation Agent

| Dimension | Content creation agent |
|---|---|
| **Data sources** | Brand style guide, past blog posts, product descriptions, SEO keyword lists |
| **Tools** | Text generation (LLM itself), plagiarism check API, word-count validator |
| **Memory / retrieval** | Style guide retrieval to maintain brand voice; past posts for tone consistency |
| **Guardrails** | Must follow brand tone; must not produce plagiarised content; must stay within word limits; must refuse off-brand topics |

- **Key risk:** Off-brand or plagiarised content published publicly damages **reputation**.
- **Operational note:** Output quality is subjective — evaluation needs **human review** alongside automated checks.

### Activity — Compare the Three Domains

Fill in the blanks for yourself:

| Question | Finance | HR | Content |
|---|---|---|---|
| Most dangerous failure? | Hallucinated number | Wrong policy info | Plagiarised text |
| Latency tolerance? | High (10s OK) | Medium (3–5s) | Medium (5–10s) |
| Main guardrail? | No advice | No salary/discipline | Brand voice |

Think about which domain has the **strictest** grounding requirement and why.

---

## Designing the HR Onboarding Assistant Architecture

Now that you see how domains differ, you will focus on the **HR onboarding agent** — designing it before writing a single line of code.

### What the Agent Must Do

An HR onboarding assistant helps **new employees** get answers to common questions during their first weeks:

- *"How many casual leaves do I get?"*
- *"How do I set up my laptop VPN?"*
- *"Who is the head of the engineering department?"*
- *"Can I negotiate my salary?"* (should be **refused** or **escalated**)

### Architecture Components

```
New Employee Question
        │
        ▼
  ┌─────────────┐
  │  LLM Agent  │──── System Prompt (guardrails, persona, escalation rules)
  └──────┬──────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
 Retriever   Tools
 (HR docs)   (ticket, escalate)
```

**1. Corpus (Knowledge Base)**

The agent needs access to HR documents. In a real company, these would be:

- `leave_policy.md` — casual, sick, earned leave rules
- `it_setup_guide.md` — VPN, email, software installation steps
- `benefits_faq.md` — health insurance, PF, gratuity
- `org_chart.md` — department heads, reporting structure

These files are **ingested** into a vector store (Chroma) using the same **ingest pipeline** from the previous session.

**2. Tools**

| Tool | Purpose |
|---|---|
| `search_hr_docs` | Retriever-based search over the HR corpus |
| `create_it_ticket` | Logs an IT setup request with employee name and issue description |
| `escalate_to_hr` | Flags a query for human HR review when the agent cannot answer |

**3. Memory and Multi-Turn**

The agent must remember context within a conversation. If an employee asks *"How many casual leaves do I get?"* and then follows up with *"Can I carry them forward?"*, the agent must know "them" refers to casual leaves.

LangChain's **ConversationBufferMemory** or message history handles this.

**4. Escalation Behaviour**

- If the retrieved context is **empty or irrelevant**, the agent should say: *"I do not have this information. Let me escalate this to the HR team."*
- If the query is about **salary, appraisal, or disciplinary matters**, the agent should **refuse** politely and suggest contacting HR directly.
- This is an **escalation guardrail** — it prevents the agent from hallucinating on sensitive topics.

### Activity — Architecture Sketch

On a piece of paper or notepad, draw the four components (corpus, retriever, tools, LLM with prompt) and connect them. Label which component handles:

1. Answering a leave-policy question
2. Creating an IT ticket
3. Refusing a salary question

---

## Implementing the HR Onboarding Agent

You will extend the **integrated LangChain stack** from earlier sessions. The implementation has two files: an **ingest script** to load HR documents into Chroma, and an **agent app** that wires retrieval, tools, and the LLM together.

### Step 1 — Prepare HR Documents

Create a folder called `hr_documents/` with sample policy files. Here is a minimal `leave_policy.md`:

```markdown
# Leave Policy

## Casual Leave
- Every full-time employee gets 12 casual leaves per calendar year.
- Casual leaves cannot be carried forward to the next year.
- Maximum 3 consecutive casual leaves at a time.

## Sick Leave
- 10 sick leaves per year.
- Medical certificate required for more than 2 consecutive days.

## Earned Leave
- 15 earned leaves per year, accrued monthly.
- Earned leaves can be carried forward up to a maximum of 30 days.
```

And a minimal `it_setup_guide.md`:

```markdown
# IT Setup Guide for New Joiners

## Laptop Setup
- Collect your laptop from the IT desk on Floor 2.
- Default OS: Windows 11 or macOS (based on your role).

## VPN Access
- Download the company VPN client from the internal portal.
- Use your employee ID and temporary password to log in.
- Raise a ticket if VPN does not connect within 24 hours.

## Email Setup
- Your official email is: firstname.lastname@company.com
- Access via Outlook or the webmail portal.
```

### Step 2 — Ingest HR Documents

```python
import shutil  # Clean old Chroma data on re-ingest
from pathlib import Path  # File path handling

from langchain_chroma import Chroma  # Vector store
from langchain_community.document_loaders import DirectoryLoader, TextLoader  # Load .md files
from langchain_openai import OpenAIEmbeddings  # Embedding model
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Chunking

DATA_DIR = Path("hr_documents")  # Folder with HR policy files
CHROMA_DIR = Path("hr_chroma_db")  # Persisted vector store
COLLECTION_NAME = "hr_onboarding_docs"  # Collection inside Chroma
EMBEDDING_MODEL = "text-embedding-3-small"  # Embedding model name

CHUNK_SIZE = 200  # Enough to keep a full policy rule in one chunk
CHUNK_OVERLAP = 30  # Overlap so boundary sentences are not lost

if CHROMA_DIR.exists():  # Remove old vectors when re-ingesting
    shutil.rmtree(CHROMA_DIR)

loader = DirectoryLoader(  # Load all Markdown files from the HR folder
    str(DATA_DIR), glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"},
)
documents = loader.load()  # Returns list of Document objects
print(f"Loaded {len(documents)} HR documents")

text_splitter = RecursiveCharacterTextSplitter(  # Split into chunks
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    add_start_index=True,  # Track position of each chunk in original doc
)
chunks = text_splitter.split_documents(documents)  # Apply splitting
print(f"Created {len(chunks)} chunks")

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)  # Initialize embedding model
vector_store = Chroma(  # Create and persist Chroma store
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR),
)
vector_store.add_documents(chunks)  # Embed and store all chunks
print(f"Stored {len(chunks)} chunks in '{COLLECTION_NAME}'")
```

**How the code works:**

- Loads every `.md` file from `hr_documents/` folder
- Splits them into chunks of 200 characters with 30-character overlap — large enough to keep a complete leave rule together
- Embeds each chunk using OpenAI's embedding model and stores in Chroma
- On re-run, old vectors are deleted first to avoid stale data

### Step 3 — Define Tools

```python
from langchain_core.tools import tool  # Decorator to create LangChain tools


@tool
def create_it_ticket(employee_name: str, issue: str) -> str:
    """Create an IT support ticket for a new joiner. Use this when the employee
    needs hardware, software, VPN, or email setup help that cannot be resolved
    from documentation alone."""
    ticket_id = f"IT-{hash(employee_name + issue) % 10000:04d}"  # Simple unique ID
    return f"Ticket {ticket_id} created for {employee_name}: {issue}. IT team will respond within 4 hours."


@tool
def escalate_to_hr(employee_name: str, query: str) -> str:
    """Escalate a query to the human HR team. Use this when the question is about
    salary, appraisal, disciplinary action, or when no relevant information is
    found in the HR documents."""
    return f"Query from {employee_name} has been escalated to the HR team: '{query}'. A team member will respond within 1 business day."
```

**How the code works:**

- **`create_it_ticket`** generates a simple ticket ID and returns a confirmation message — in production, this would call an actual ticketing API like Jira or ServiceNow
- **`escalate_to_hr`** simulates forwarding the query to a human — the tool description tells the LLM **when** to use it (salary, appraisal, unknown queries)
- The `@tool` decorator converts a Python function into a LangChain-compatible tool with automatic schema generation

### Step 4 — Build the Agent

```python
from pathlib import Path  # Path handling

from langchain_chroma import Chroma  # Load persisted vector store
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # LLM and embeddings
from langchain.agents import AgentExecutor, create_openai_tools_agent  # Agent framework
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # Prompt template
from langchain_core.tools import tool  # Tool decorator

CHROMA_DIR = Path("hr_chroma_db")  # Must match ingest script
COLLECTION_NAME = "hr_onboarding_docs"  # Must match ingest script
EMBEDDING_MODEL = "text-embedding-3-small"  # Must match ingest script

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)  # Same model used during ingest
vector_store = Chroma(  # Connect to persisted Chroma
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR),
)
retriever = vector_store.as_retriever(  # Configure retrieval
    search_type="similarity",  # Can try "mmr" for diversity
    search_kwargs={"k": 3},  # Top 3 chunks
)


@tool
def search_hr_docs(query: str) -> str:
    """Search the company HR knowledge base for policy information about leaves,
    IT setup, benefits, org structure, and other onboarding topics. Always use
    this tool first for any HR-related question."""
    docs = retriever.invoke(query)  # Retrieve relevant chunks
    if not docs:  # No relevant documents found
        return "No relevant HR documents found for this query."
    return "\n\n".join(  # Combine chunks with source info
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )


@tool
def create_it_ticket(employee_name: str, issue: str) -> str:
    """Create an IT support ticket for a new joiner. Use when the employee needs
    hardware, software, VPN, or email help beyond what documentation covers."""
    ticket_id = f"IT-{hash(employee_name + issue) % 10000:04d}"
    return f"Ticket {ticket_id} created for {employee_name}: {issue}. IT team will respond within 4 hours."


@tool
def escalate_to_hr(employee_name: str, query: str) -> str:
    """Escalate a query to the human HR team. Use when the question is about salary,
    appraisal, disciplinary action, or when no relevant information exists in HR docs."""
    return f"Query from {employee_name} escalated to HR team: '{query}'. Response within 1 business day."


tools = [search_hr_docs, create_it_ticket, escalate_to_hr]  # All tools available to agent

system_prompt = """You are an HR Onboarding Assistant for new employees.

Your responsibilities:
- Answer questions about company policies, leave rules, IT setup, benefits, and org structure.
- Always search the HR knowledge base FIRST before answering any policy question.
- If the knowledge base has the answer, respond clearly and cite the source document.
- If the knowledge base does NOT have the answer, escalate to the HR team. Do NOT guess or make up information.

Strict rules:
- NEVER answer questions about salary, compensation, appraisal, promotion, or disciplinary matters. Escalate these immediately.
- NEVER provide information that is not present in the retrieved documents.
- If the employee needs IT help that documents cannot resolve, create an IT ticket.
- Be warm, professional, and helpful — remember, the employee is new and might feel nervous.

Always address the employee by name if provided."""

prompt = ChatPromptTemplate.from_messages([  # Agent prompt with memory placeholder
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history", optional=True),  # Multi-turn memory
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # Agent reasoning steps
])

llm = ChatOpenAI(model="gpt-4o", temperature=0)  # Deterministic for policy answers
agent = create_openai_tools_agent(llm, tools, prompt)  # Wire LLM + tools + prompt
agent_executor = AgentExecutor(  # Runnable agent with loop control
    agent=agent,
    tools=tools,
    verbose=True,  # Print agent reasoning steps
    max_iterations=5,  # Prevent runaway tool loops
    handle_parsing_errors=True,  # Graceful error handling
)

print("=" * 60)
print("HR Onboarding Assistant is ready.")
print("=" * 60)

test_queries = [
    "Hi, I am Priya. How many casual leaves do I get per year?",
    "Can casual leaves be carried forward?",
    "How do I set up VPN on my laptop?",
    "What is my salary package?",
    "I cannot connect to VPN even after following the guide. Can you help?",
]

for query in test_queries:  # Run each test query
    print(f"\n{'─' * 40}")
    print(f"Employee: {query}")
    result = agent_executor.invoke({"input": query})  # Execute agent
    print(f"Agent: {result['output']}")
```

**How the code works:**

- Connects to the same Chroma store created by the ingest script
- Defines three tools: **search_hr_docs** (retrieval), **create_it_ticket** (action), **escalate_to_hr** (safety valve)
- The **system prompt** sets guardrails — search first, cite sources, refuse salary questions, escalate unknowns
- **`MessagesPlaceholder`** for `chat_history` enables multi-turn conversations
- **`max_iterations=5`** prevents the agent from looping endlessly if a tool keeps failing
- Test queries cover the main paths: grounded answer, follow-up, refusal, and escalation

---

## Evaluating the HR Agent

Building the agent is only half the job. You need to prove it works — and prove it fails safely where it should.

### Designing Structured Test Cases

A good evaluation set covers **four categories**:

| Category | What it tests | Example query |
|---|---|---|
| **Grounded answer** | Agent retrieves correct info and cites source | *"How many sick leaves do I get?"* |
| **Tool use** | Agent calls the right tool with valid arguments | *"Create a ticket — my VPN is not working"* |
| **Refusal path** | Agent refuses or escalates out-of-scope queries | *"What is my CTC breakup?"* |
| **Multi-turn continuity** | Agent remembers context across turns | *"How many earned leaves?"* → *"Can I carry them forward?"* |

### Evaluation JSON

```json
[
  {
    "id": "HR-001",
    "query": "How many casual leaves do I get per year?",
    "category": "grounded_answer",
    "expected_tool": "search_hr_docs",
    "expected_keywords": ["12", "casual"],
    "expected_refusal": false
  },
  {
    "id": "HR-002",
    "query": "What is my salary?",
    "category": "refusal",
    "expected_tool": "escalate_to_hr",
    "expected_keywords": ["salary", "escalat"],
    "expected_refusal": true
  },
  {
    "id": "HR-003",
    "query": "My VPN is not connecting after following the guide. Please raise a ticket.",
    "category": "tool_use",
    "expected_tool": "create_it_ticket",
    "expected_keywords": ["ticket", "created"],
    "expected_refusal": false
  },
  {
    "id": "HR-004",
    "query": "How many earned leaves can I carry forward?",
    "category": "grounded_answer",
    "expected_tool": "search_hr_docs",
    "expected_keywords": ["30", "carry forward"],
    "expected_refusal": false
  },
  {
    "id": "HR-005",
    "query": "Tell me about the latest cricket match score",
    "category": "refusal",
    "expected_tool": "escalate_to_hr",
    "expected_keywords": ["cannot", "not"],
    "expected_refusal": true
  }
]
```

### Running the Evaluation

```python
import json  # Parse eval JSON
import csv  # Write results to CSV
import time  # Measure latency

from pathlib import Path  # File handling

eval_file = Path("hr_eval_cases.json")  # Path to evaluation JSON
results_file = Path("hr_eval_results.csv")  # Output results

with open(eval_file, "r") as f:  # Load test cases
    eval_cases = json.load(f)

results = []  # Collect results for CSV

for case in eval_cases:  # Run each test case
    query = case["query"]
    expected_tool = case["expected_tool"]
    expected_keywords = case["expected_keywords"]
    expected_refusal = case["expected_refusal"]

    start_time = time.time()  # Start timer
    response = agent_executor.invoke({"input": query})  # Run agent
    elapsed = round(time.time() - start_time, 2)  # Measure latency

    output = response["output"].lower()  # Normalize for keyword matching

    keyword_hit = all(  # Check if all expected keywords appear in response
        kw.lower() in output for kw in expected_keywords
    )

    passed = keyword_hit  # Basic pass criterion: expected keywords present
    results.append({  # Record result
        "id": case["id"],
        "category": case["category"],
        "query": query,
        "passed": passed,
        "latency_s": elapsed,
        "response_snippet": response["output"][:150],
    })
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {case['id']} — {query[:50]}... ({elapsed}s)")

with open(results_file, "w", newline="") as f:  # Write CSV
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

pass_count = sum(1 for r in results if r["passed"])  # Count passes
total = len(results)
print(f"\nResults: {pass_count}/{total} passed. Details in {results_file}")
```

**How the code works:**

- Loads evaluation cases from a JSON file
- Runs each query through the agent and measures **latency**
- Checks if **expected keywords** appear in the response as a basic accuracy signal
- Writes results to a CSV file for comparison across iterations
- Prints pass/fail status for each case with timing

This is the same **evaluation harness pattern** from the previous session — now applied to a domain-specific agent.

---

## Live Demonstration — In-Domain vs Out-of-Corpus Queries

A live demo is where the agent proves itself. You run **two types** of queries side by side:

### In-Domain Queries (Should Answer Well)

| Query | Expected behaviour |
|---|---|
| *"How many casual leaves per year?"* | Retrieves leave policy, answers **12** |
| *"How do I access my company email?"* | Retrieves IT setup guide, gives Outlook/webmail steps |
| *"Can I carry forward earned leaves?"* | Retrieves policy, says **yes, up to 30 days** |

### Out-of-Corpus Queries (Should Refuse or Escalate)

| Query | Expected behaviour |
|---|---|
| *"What is my CTC breakup?"* | Escalates to HR — salary topic |
| *"Who won the IPL last year?"* | Refuses — out of domain entirely |
| *"Can I get a transfer to another city?"* | Escalates — not in HR corpus |

### What to Watch During the Demo

- Does the agent **search first** or jump to answering?
- Does it **cite the source document** in its response?
- Does it **refuse gracefully** on salary and out-of-domain queries?
- Does it **escalate** when retrieval returns nothing relevant?

### Residual Risks and Improvement Priorities

No agent is perfect after a first build. Common residual risks for an HR onboarding agent:

- **Stale documents:** If the leave policy changes mid-year and the corpus is not re-ingested, the agent gives outdated answers
- **Edge-case queries:** Questions that are *technically* in-domain but phrased unusually may get weak retrieval
- **Multi-turn memory limits:** Very long conversations may exceed context window, losing early context
- **Tool misrouting:** Borderline queries (e.g., *"my laptop is slow"*) may trigger document search instead of ticket creation

**Improvement priorities** for a production version:

1. Add **automated re-ingestion** when documents are updated
2. Expand the evaluation set to **50+ cases** covering edge cases
3. Add **groundedness scoring** — LLM-as-judge checking if the answer is supported by retrieved chunks
4. Implement **conversation summarisation** for long multi-turn sessions
5. Add **observability dashboards** tracking latency, failure rate, and token usage

---

## Extending the Agent to Other Domains

The architecture you built is a **pattern**, not a one-time project. Here is how the same structure adapts:

| Component | HR Agent | Finance Agent (pattern) | Content Agent (pattern) |
|---|---|---|---|
| **Corpus** | Leave policy, IT guide | SEBI filings, annual reports | Brand style guide, past posts |
| **Retriever** | Chroma, k=3, similarity | Chroma, k=5, larger chunks | Chroma, k=3, MMR for diversity |
| **Tools** | Search, ticket, escalate | Search, calculator, escalate | Generate, plagiarism-check, word-count |
| **Guardrails** | No salary talk | No buy/sell advice | No off-brand content |
| **Evaluation** | Grounded, refusal, tool use | Grounded, no-advice, citation | Tone match, plagiarism, length |

The **debugging and iteration loop** from the previous session applies to every domain: label failures, patch one layer, re-run evaluation, check metrics.

### Activity — Design Your Own Domain Agent

Pick any domain you find interesting (e-commerce, education, healthcare helpdesk, travel booking). On a sheet of paper, fill in:

1. **Corpus** — What documents would the agent need?
2. **Tools** — What 2–3 tools would you give it?
3. **Guardrails** — What must the agent **never** do?
4. **One test case** — Write one eval query with expected tool and expected keywords.

---

## Module Checklist

This is the final session of the module. Here is a checklist of everything you should now be able to do:

- [ ] Explain what an **agent** is and how it differs from a simple chatbot
- [ ] Build a **LangChain agent** with tools, retrieval, and memory
- [ ] Design a **RAG pipeline** with ingest, chunking, embedding, and retrieval
- [ ] Write an **evaluation harness** with test cases, a runner, and results CSV
- [ ] Classify agent failures into **failure classes** and apply targeted **patches**
- [ ] Measure **quality metrics** — accuracy, groundedness, latency, token usage
- [ ] Understand **cost–latency trade-offs** and when to stop iterating
- [ ] Apply the agent pattern to a **real-world domain** with appropriate guardrails

If any of these feel weak, revisit the relevant session notes and run the code again. Practice is the only way to build confidence.

---

## Key Takeaways

- **Different domains** need different data, tools, and guardrails — but the **LangChain architecture pattern** stays the same.
- An HR onboarding agent needs a **knowledge base**, **retrieval**, **action tools** (tickets), and **escalation** for sensitive or unknown queries.
- **Evaluation** must cover grounded answers, correct tool use, refusal paths, and multi-turn continuity — not just "does the answer look right."
- **Residual risks** (stale docs, edge cases, memory limits) should be documented and prioritised, not ignored.
- The **build → evaluate → debug → iterate** loop you learned across this module is how production agents are maintained in real companies.

---

## Important Commands, Libraries, and Terminologies

| Term / Command | Type | Meaning |
|---|---|---|
| **Use case** | Concept | A specific scenario where the agent solves a real business problem |
| **Corpus** | Concept | The collection of documents the agent can search and retrieve from |
| **Escalation** | Pattern | Forwarding a query to a human when the agent cannot or should not answer |
| **Guardrail** | Concept | Rules that prevent the agent from producing harmful or incorrect output |
| **Groundedness** | Metric | Whether the agent's answer is supported by retrieved evidence |
| **Multi-turn continuity** | Concept | Agent remembering context across follow-up questions in a conversation |
| **`@tool`** | Decorator | LangChain decorator that converts a Python function into an agent tool |
| **`create_openai_tools_agent`** | Function | Creates a LangChain agent that uses OpenAI's tool-calling format |
| **`AgentExecutor`** | Class | Runs the agent loop — LLM reasons, calls tools, gets results, responds |
| **`max_iterations`** | Parameter | Caps the number of agent reasoning loops to prevent runaways |
| **`MessagesPlaceholder`** | Class | Placeholder in prompt template for chat history or agent scratchpad |
| **`RecursiveCharacterTextSplitter`** | Class | Splits documents into chunks with configurable size and overlap |
| **`Chroma`** | Library | Open-source vector database for storing and searching embeddings |
| **`DirectoryLoader`** | Class | Loads all files matching a pattern from a folder |
| **`python3 hr_ingest.py`** | Command | Run the HR document ingest pipeline |
| **`python3 hr_agent.py`** | Command | Start the HR onboarding agent with test queries |
| **Residual risk** | Concept | Known limitations that remain after building and testing the agent |
| **Evaluation harness** | Pattern | JSON test cases + runner + results CSV for systematic agent testing |
