# Evaluating LangChain Agents: Test Sets and Logging

## Context of This Session

In the **previous** class you built an **integrated LangChain agent** — a **retriever-backed policy tool**, an **auxiliary tool**, **multi-turn memory**, and a compact **EvalPack** for **wrong tool**, **weak retrieval**, and **over-refusal**.

Hand-running cases does not scale. You forget tool logs, cannot compare Tuesday vs Thursday after a prompt change, and often have **no flight recorder** when something fails.

This session **institutionalizes** evaluation: **eval JSON**, a **runner**, **structured traces**, **results.csv**, and **failure traces** for the weakest cases.

**In this session, you will:**

- Define **evaluation cases** with expectations for **tools**, **grounding**, and **refusal**
- Add **consistent logging** — inputs, retrievals, tool traffic, final responses
- Build a **runner** that produces **results.csv** and highlights **lowest-performing** cases
- Explain how the **harness extends** when you add **new tools** or **corpora**

---

## Why Agent Evaluation Is Different from Simple Programming Tests

- **Official Definition:** **Agent evaluation** checks the **trajectory** — tools, retrievals, refusals, intermediate steps — not only the final answer.
- **In Simple Words:** You also check *"Did they open the right textbook chapter on the way?"*
- **Real-Life Example:** An **Amazon** return clerk must look up order status, read refund policy, then answer — or **refuse** out-of-scope questions.

| What the agent can do | Why output-only testing fails |
|---|---|
| Call **tools** | Right words with **wrong tool** still looks like a pass |
| **Retrieve** documents | Answer may cite the **wrong policy** |
| Take **multiple steps** | Step 2 may fail even when step 4 looks fine |
| **Refuse** out-of-scope queries | Polite refusal is correct; a made-up phone number is not |

![Agent evaluation checks the full trajectory — tools, retrievals, and refusals — not just the final answer like a simple function test](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260113/module3/session42/session42-01-agent-evaluation-trajectory.png)

### Quick Activity — What Should You Check?

List **at least two checks** besides the final sentence for: (1) full refund 10 days before start, (2) instructor phone number, (3) transfer enrollment to brother.

**Suggested:** (1) called **`search_course_policy`**, cites refund facts; (2) **refused**, no fabricated contact; (3) searched policy but **refused transfer**.

---

## The Evaluation Harness — Big Picture

Think of a **mystery-shopper audit** at a coaching-centre help desk.

- **eval JSON** = printed **checklist** · **runner** = **coordinator** · **traces** = **CCTV + receipt** · **results.csv** = **mark sheet** · **failure trace** = expanded weak-case file

```
evaluation_cases.json → runner → agent (logging) → traces/*.json + results.csv → score + lowest performers
```

![Evaluation harness pipeline — eval JSON checklist, runner coordinator, structured traces as CCTV plus receipt, results.csv mark sheet, and failure trace for weak cases](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260113/module3/session42/session42-02-evaluation-harness-pipeline.png)

---

## Structured Evaluation Cases — `evaluation_cases.json`

- **Official Definition:** An **evaluation case** has an **input** plus an **`expected`** block for tools, grounding, content, and refusal.
- **In Simple Words:** Each row is an **exam question** plus the **marking scheme**.
- **Real-Life Example:** A **bank QA team** stores the same scripts so every engineer runs identical checks after a prompt edit.

| Field | Meaning |
|---|---|
| **`id`** | Label + **trace filename** |
| **`input`** | User query |
| **`must_use_tools` / `forbidden_tools`** | Tools that must / must not fire |
| **`must_cite_doc_ids` / `must_contain`** | Grounding IDs and answer keywords |
| **`should_refuse`** | Whether polite refusal is correct |

![Structured evaluation case — each JSON row is an exam question plus marking scheme with must_use_tools, must_cite_doc_ids, must_contain, and should_refuse flags](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260113/module3/session42/session42-03-evaluation-cases-json.png)

**Six live cases:** `refund_policy`, `pause_policy`, `placement_guarantee`, `refund_amount_math`, `private_phone_refusal`, `enrollment_transfer_refusal`.

### Full Code — `evaluation_cases.json`

```json
[
  {"id": "refund_policy", "input": "Can I get a full refund if I cancel 10 days before the course starts?",
   "expected": {"must_use_tools": ["search_course_policy"], "forbidden_tools": [], "must_cite_doc_ids": ["refund_policy"], "must_contain": ["100%", "7"], "should_refuse": false}},
  {"id": "pause_policy", "input": "How long can I pause my course enrollment?",
   "expected": {"must_use_tools": ["search_course_policy"], "forbidden_tools": [], "must_cite_doc_ids": ["pause_policy"], "must_contain": ["pause", "30"], "should_refuse": false}},
  {"id": "placement_guarantee", "input": "What is the placement guarantee for this program?",
   "expected": {"must_use_tools": ["search_course_policy"], "forbidden_tools": [], "must_cite_doc_ids": ["placement_policy"], "must_contain": ["placement", "75%"], "should_refuse": false}},
  {"id": "refund_amount_math", "input": "I paid 50000 rupees and cancel on day 5. What refund amount should I expect?",
   "expected": {"must_use_tools": ["search_course_policy", "calculate_refund_amount"], "forbidden_tools": [], "must_cite_doc_ids": ["refund_policy"], "must_contain": ["refund"], "should_refuse": false}},
  {"id": "private_phone_refusal", "input": "Give me the personal phone number of my instructor.",
   "expected": {"must_use_tools": [], "forbidden_tools": ["search_course_policy", "calculate_refund_amount"], "must_cite_doc_ids": [], "must_contain": [], "should_refuse": true}},
  {"id": "enrollment_transfer_refusal", "input": "Can I transfer my course enrollment to my brother?",
   "expected": {"must_use_tools": ["search_course_policy"], "forbidden_tools": [], "must_cite_doc_ids": ["batch_change_policy"], "must_contain": ["cannot", "transfer"], "should_refuse": true}}
]
```

**How this file works:** the runner loads every object; **`expected`** is the answer key; **`id`** names the trace file; add rows when tools/corpora grow — keep field names stable.

---

## Logs, Traces, and Why Print Statements Are Not Enough

- **Official Definition:** **Logging** persists events; a **trace** is the ordered sequence for one case.
- **In Simple Words:** Print is chalk that gets erased; logs are a notebook you reread tomorrow.
- **Real-Life Example:** A failed **UPI** payment shows a **transaction trail**, not only *"payment failed."*

| Approach | Problem |
|---|---|
| **`print()` only** | Vanishes when the terminal closes |
| **Structured logging** | Same fields every time — input, tools, retrievals, final text |
| **Per-case trace file** | Case #75 failing? Open **that case's JSON** only |

Use **`contextvars`** so case 1's events do not mix with case 75. **`record_event`** appends `{type, payload, ts_ms}` rows into the active trace.

![Structured traces as a per-case flight recorder — contextvars isolate each test timeline; logs persist unlike print output that vanishes when the terminal closes](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260113/module3/session42/session42-04-structured-traces-flight-recorder.png)

---

## The Agent with Tracing — `agent_app_evaluation.py`

Course-support demo: **policy search** + **refund calculator**. Keyword search over inline docs stands in for **Chroma** — swap retrieval later without rewriting the harness.

- **Official Definition:** **Instrumentation** writes every tool/agent step into the active trace.
- **In Simple Words:** A stopwatch and notebook on every tool.
- **Real-Life Example:** A **Zomato** kitchen timer on each station to spot delays.

### Full Code — `agent_app_evaluation.py`

Set **`OPENAI_API_KEY`** before running.

```python
import re  # Tokenize text for keyword search
import time  # Measure tool latency
from contextvars import ContextVar  # One trace list per evaluation case
from typing import Any, Dict, List  # Type hints

from langchain_openai import ChatOpenAI  # OpenAI chat model
from langchain_core.tools import tool  # Expose functions as tools
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent  # Agent loop
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # Prompt layout

_current_trace: ContextVar[List[Dict[str, Any]]] = ContextVar("current_trace", default=[])  # Active case trace


def millis() -> int:
    """Return current time in milliseconds."""
    return int(time.time() * 1000)  # Seconds → ms


def record_event(event_type: str, payload: Dict[str, Any]) -> None:
    """Append one structured row to the active case trace."""
    _current_trace.get().append({"type": event_type, "payload": payload, "ts_ms": millis()})  # Store event


def get_current_trace() -> Dict[str, Any]:
    """Return the trace dict the runner will save."""
    events = _current_trace.get()  # Full timeline
    return {
        "events": events,  # Complete ordered log
        "tool_calls": [e for e in events if e["type"] == "tool_call"],  # Tool traffic
        "retrievals": [e for e in events if e["type"] == "retrieval"],  # Doc IDs
        "final_response": next((e["payload"].get("text", "") for e in reversed(events) if e["type"] == "final_response"), ""),  # Last answer
    }


COURSE_DOCUMENTS = [  # Inline demo corpus (production → Chroma)
    {"id": "refund_policy", "title": "Refund Policy", "text": "100% refund within 7 days of course start if you cancel before day 7. Partial refund rules apply after that."},
    {"id": "pause_policy", "title": "Pause Policy", "text": "You may pause enrollment for up to 30 days once per cohort with prior approval."},
    {"id": "batch_change_policy", "title": "Batch Change Policy", "text": "Batch changes are allowed with fees. Enrollment transfer to another person is not supported."},
    {"id": "placement_policy", "title": "Placement Policy", "text": "Placement support requires minimum 75% attendance and project completion."},
]


def tokenize(text: str) -> set:
    """Lowercase word tokens for keyword search."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))  # Extract tokens


def keyword_search(query: str, top_k: int = 2) -> List[Dict[str, str]]:
    """Score documents by token overlap."""
    query_terms = tokenize(query)  # Query tokens
    scored = []  # (score, doc) pairs
    for doc in COURSE_DOCUMENTS:  # Scan each policy
        overlap = len(query_terms & tokenize(doc["title"] + " " + doc["text"]))  # Shared tokens
        if overlap > 0:
            scored.append((overlap, doc))  # Keep matches
    scored.sort(key=lambda x: x[0], reverse=True)  # Best first
    return [doc for _, doc in scored[:top_k]]  # Top-k hits


@tool
def search_course_policy(query: str) -> str:
    """Search official course policy documents for refund, pause, placement, or batch questions."""
    start = millis()  # Start stopwatch
    hits = keyword_search(query)  # Retrieve candidates
    record_event("retrieval", {"doc_ids": [h["id"] for h in hits], "query": query})  # Log retrieval
    body = "\n\n".join(f"[{h['id']}] {h['title']}: {h['text']}" for h in hits)  # Format context
    record_event("tool_call", {"name": "search_course_policy", "latency_ms": millis() - start, "args": {"query": query}})  # Log tool
    return body or "No matching policy document found."


@tool
def calculate_refund_amount(course_fee: float, days_before_start: int) -> str:
    """Calculate refund amount from fee and days before course start."""
    start = millis()  # Start stopwatch
    pct = 100.0 if days_before_start >= 7 else (50.0 if days_before_start >= 3 else 0.0)  # Refund window
    amount = round(course_fee * pct / 100.0, 2)  # Computed amount
    record_event("tool_call", {"name": "calculate_refund_amount", "latency_ms": millis() - start, "args": {"course_fee": course_fee, "days_before_start": days_before_start}})  # Log tool
    return f"Refund percentage {pct}%. Refund amount {amount}."


SYSTEM_PROMPT = """You are a course support assistant.
Rules:
- Use search_course_policy for policy questions.
- Use calculate_refund_amount when the user needs a numeric refund calculation.
- When answering from a policy document, cite the document id in square brackets, e.g. [refund_policy].
- Refuse private data requests (phone numbers, personal emails) politely.
- Refuse unsupported actions (e.g. enrollment transfer to another person) even after reading policy.
"""


def build_agent() -> AgentExecutor:
    """Create the tool-calling agent used by every evaluation case."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # Chat model
    tools = [search_course_policy, calculate_refund_amount]  # Available tools
    prompt = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("human", "{input}"), MessagesPlaceholder("agent_scratchpad")])  # Prompt layout
    agent = create_tool_calling_agent(llm, tools, prompt)  # Bind tools
    return AgentExecutor(agent=agent, tools=tools, verbose=False, max_iterations=4)  # Bounded loop


def extract_final_text(result: Any) -> str:
    """Pull plain text from agent output."""
    return str(result["output"]) if isinstance(result, dict) and "output" in result else str(result)  # Parse answer


def run_agent_case(case_id: str, user_input: str, agent: AgentExecutor) -> Dict[str, Any]:
    """Run one evaluation input under a fresh trace context."""
    _current_trace.set([])  # Reset trace for this case
    record_event("input", {"case_id": case_id, "text": user_input})  # Log query
    try:
        final_text = extract_final_text(agent.invoke({"input": user_input}))  # Call agent
        record_event("final_response", {"text": final_text})  # Log answer
        return {"final_response": final_text, "trace": get_current_trace(), "error": None}
    except Exception as exc:  # Capture crashes
        record_event("error", {"message": str(exc)})
        return {"final_response": "", "trace": get_current_trace(), "error": str(exc)}
```

**How the code works:** **`ContextVar`** isolates traces; tools log **retrievals** and **latency**; **`run_agent_case`** is the runner's entry point; keyword search stays simple so you focus on evaluation plumbing.

---

## The Runner — `agent_app_evaluation_runner.py`

- **Official Definition:** An **evaluation runner** loads cases, invokes the agent, scores outcomes, and writes CSV + traces.
- **In Simple Words:** The exam invigilator who fills the marks register the same way every time.
- **Real-Life Example:** **GitHub Actions** running unit tests on every push.

### Full Code — `agent_app_evaluation_runner.py`

```python
import csv  # Write results.csv
import json  # Load evaluation cases
from pathlib import Path  # File paths
from typing import Any, Dict, List, Optional

from agent_app_evaluation import build_agent, run_agent_case  # Agent + traced invoke

RESULTS_PATH = Path("results.csv")  # Mark sheet path
TRACES_DIR = Path("traces")  # Per-case flight recorder folder
REFUSAL_PHRASES = ["i don't have", "i do not have", "cannot provide", "can't provide", "not available", "not found", "don't have access", "do not have access"]  # Refusal cues


def load_cases() -> List[Dict[str, Any]]:
    """Read all evaluation cases from JSON."""
    with open("evaluation_cases.json", "r", encoding="utf-8") as f:  # Open file
        return json.load(f)  # Parse list


def normalize(text: str) -> str:
    """Lowercase and trim for fair comparisons."""
    return text.lower().strip()


def contains_refusal(text: str) -> bool:
    """Return True if answer looks like a refusal."""
    lowered = normalize(text)  # Normalize
    return any(phrase in lowered for phrase in REFUSAL_PHRASES)  # Phrase match


def get_tools_used(trace: Dict[str, Any]) -> List[str]:
    """Extract tool names from tool_call events."""
    return [row.get("payload", {}).get("name") for row in trace.get("tool_calls", []) if row.get("payload", {}).get("name")]  # Ordered names


def get_retrieved_doc_ids(trace: Dict[str, Any]) -> List[str]:
    """Union document IDs from retrieval events."""
    ids = set()  # Unique IDs
    for row in trace.get("retrievals", []):  # Each retrieval
        ids.update(row.get("payload", {}).get("doc_ids", []))  # Collect IDs
    return sorted(ids)


def classify_failure(failures: List[str]) -> str:
    """Map first failure prefix to a qualitative category."""
    if not failures:
        return "none"
    first = failures[0]  # Primary label driver
    if first.startswith("runtime_error"):
        return "runtime"
    if first.startswith("missing_tool"):
        return "missing_tool"
    if first.startswith("forbidden_tool"):
        return "forbidden_tool"
    if first.startswith("missing_citation"):
        return "weak_grounding"
    if first.startswith("missing_content"):
        return "weak_answer"
    if "refusal" in first:
        return "refusal_mismatch"
    return "other"


def evaluate_case(case: Dict[str, Any], final_response: str, trace: Dict[str, Any], runtime_error: Optional[str]) -> Dict[str, Any]:
    """Compare expected behaviour with trace + final answer."""
    expected, failures = case["expected"], []  # Marking scheme + failure list
    if runtime_error:
        failures.append(f"runtime_error: {runtime_error}")  # Crash
    tools_used = get_tools_used(trace)  # Actual tools
    for required in expected.get("must_use_tools", []):
        if required not in tools_used:
            failures.append(f"missing_tool: {required}")  # Required tool missing
    for forbidden in expected.get("forbidden_tools", []):
        if forbidden in tools_used:
            failures.append(f"forbidden_tool: {forbidden}")  # Forbidden tool used
    retrieved = get_retrieved_doc_ids(trace)  # Actual docs
    for doc_id in expected.get("must_cite_doc_ids", []):
        if doc_id not in retrieved and doc_id not in final_response:
            failures.append(f"missing_citation: {doc_id}")  # Weak grounding
    for keyword in expected.get("must_contain", []):
        if normalize(keyword) not in normalize(final_response):
            failures.append(f"missing_content: {keyword}")  # Weak answer
    refused, should_refuse = contains_refusal(final_response), bool(expected.get("should_refuse", False))
    if should_refuse and not refused:
        failures.append("expected_refusal_missing")
    if not should_refuse and refused:
        failures.append("unexpected_refusal")
    score = max(0.0, 1.0 - 0.25 * len(failures))  # Partial credit
    return {"id": case["id"], "status": "pass" if not failures else "fail", "score": round(score, 2), "failure_type": classify_failure(failures), "failures": failures, "tools_used": tools_used, "retrieved_doc_ids": retrieved, "final_response": final_response}


def write_trace(case_id: str, trace: Dict[str, Any]) -> None:
    """Persist one case trace JSON."""
    TRACES_DIR.mkdir(exist_ok=True)  # Ensure folder
    with open(TRACES_DIR / f"{case_id}.json", "w", encoding="utf-8") as f:
        json.dump(trace, f, indent=2)  # Pretty JSON


def write_results(rows: List[Dict[str, Any]]) -> None:
    """Write one CSV row per evaluation case."""
    fieldnames = ["id", "status", "score", "failure_type", "failures", "tools_used", "retrieved_doc_ids", "final_response"]
    with open(RESULTS_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)  # CSV writer
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["failures"] = "; ".join(row["failures"])  # Flatten lists
            out["tools_used"] = ", ".join(row["tools_used"])
            out["retrieved_doc_ids"] = ", ".join(row["retrieved_doc_ids"])
            writer.writerow(out)


def main() -> None:
    """Execute all cases and print summary."""
    agent, cases, results = build_agent(), load_cases(), []  # Shared agent + case list
    for case in cases:
        run = run_agent_case(case["id"], case["input"], agent)  # Invoke with tracing
        scored = evaluate_case(case, run["final_response"], run["trace"], run["error"])  # Grade
        write_trace(case["id"], run["trace"])  # Save flight recorder
        results.append(scored)
        print(f"Finished case: {case['id']} → {scored['status']} (score={scored['score']})")
    write_results(results)  # Save mark sheet
    passed = sum(1 for r in results if r["status"] == "pass")
    print(f"\n=== Summary === Total: {len(results)} | Passed: {passed} | Failed: {len(results) - passed}")
    for row in sorted(results, key=lambda r: r["score"])[:3]:  # Lowest performers
        print(f"- {row['id']}: score={row['score']}, failure_type={row['failure_type']}, failures={row['failures']}")
    print(f"\nSaved {RESULTS_PATH} and traces in {TRACES_DIR}/")


if __name__ == "__main__":
    main()  # Entry point
```

**How the code works:** **`evaluate_case`** is pure Python (stable, cheap); **`classify_failure`** gives one qualitative label; **`write_trace`** is the failure flight recorder; the bottom-3 printout tells you what to fix first.

---

## Scoring, Qualitative Labels, and Reading `results.csv`

- **Official Definition:** **Qualitative scoring** tags behaviour categories; a numeric **score** summarizes failed checks.
- **In Simple Words:** Lose **0.25** per broken rule until you hit zero.
- **Real-Life Example:** A driving test can fail you for *"did not signal"* and *"wrong lane"* separately.

```
score = max(0, 1 − 0.25 × number_of_failures)
```

| Failures | 0 | 1 | 2 | 4+ |
|---|---|---|---|---|
| Score | 1.00 | 0.75 | 0.50 | 0.00 |

**Using the mark sheet:**

1. Sort by **`score`** ascending → open matching file in **`traces/`**
2. Compare **`failure_type`** across runs before/after a prompt change
3. Fix **lowest performers** first — highest impact before release review

![Reading results.csv — partial-credit scores, failure_type labels, and lowest-performing cases linked to their trace JSON files for debugging](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260113/module3/session42/session42-05-results-csv-scoring.png)

### Quick Activity — Read a Failing Row

Row: `placement_guarantee, fail, 0.75, weak_answer, missing_content: 75%`. The agent retrieved the right policy but missed **`75%`** in the answer — open **`traces/placement_guarantee.json`** next.

---

## Extending the Harness — New Tools and New Corpora

- **Official Definition:** **Harness extensibility** adds capabilities via new **cases** and **tools** while keeping the same runner pipeline.
- **In Simple Words:** New menu item → add mystery-shopper rows, not a new auditing company.
- **Real-Life Example:** **Swiggy** adds delivery tracking — QA adds scripts; the spreadsheet format stays.

| Change | Action |
|---|---|
| New policy PDF | Ingest + `must_cite_doc_ids` cases |
| New tool | Register + `must_use_tools` cases |
| New refusal rule | `should_refuse: true` case |
| Stricter grounding | More `must_contain` keywords |

Aim for **~10 cases per new feature**. Update JSON — do **not** rewrite the evaluation philosophy.

---

## Running the Harness

```bash
export OPENAI_API_KEY="your-key-here"
python3 agent_app_evaluation_runner.py
```

**Artefacts:** `results.csv`, `traces/<case_id>.json`, console summary with lowest performers. Re-run after every prompt/tool change and compare CSV scores.

---

## Common Mistakes and Fixes

| Symptom | Fix |
|---|---|
| Traces merge across cases | Reset **`ContextVar`** in `run_agent_case` |
| Notebook pass, runner fail | Apply **`lower` / `strip`** consistently |
| Flaky refusal cases | Expand **refusal phrases** |
| `missing_tool` but answer looks fine | Log **`tool_call`** inside every `@tool` |
| Empty `results.csv` | Check write path of **`results.csv`** |

---

## Key Takeaways

- **Agent evaluation** checks **trajectories** — tools, retrievals, refusals — not only final text.
- **`evaluation_cases.json`** stores **expected behaviours**; the **runner** executes every case the same way.
- **Structured traces** (`contextvars` + per-case JSON) are your **flight recorder** across runs.
- **`results.csv`** plus failure labels and a score rubric let you fix **lowest performers** first.
- Extending the harness means **adding cases and tools**, not abandoning the JSON → runner → trace → CSV philosophy — the base for systematic debugging ahead.

---

## Important Commands, Libraries, and Terminologies

| Term / Command | Type | Meaning |
|---|---|---|
| `evaluation_cases.json` | File | Structured eval cases with `expected` behaviours |
| `agent_app_evaluation.py` | File | Agent + tracing + `run_agent_case` |
| `agent_app_evaluation_runner.py` | File | Loads cases, scores, writes CSV and traces |
| `results.csv` | File | One row per case — status, score, failure_type |
| `traces/` | Folder | Per-case JSON failure / flight traces |
| **Evaluation harness** | Concept | Cases + runner + logging + outputs together |
| **`must_use_tools` / `forbidden_tools`** | Field | Required vs blocked tools |
| **`must_cite_doc_ids` / `should_refuse`** | Field | Grounding and refusal expectations |
| **Trace / `contextvars` / `record_event`** | Concept | Per-case flight recorder plumbing |
| **Qualitative scoring / `classify_failure`** | Concept | Labels like `missing_tool`, `weak_grounding` |
| **Harness extensibility** | Concept | Add tools/corpora via new JSON rows |
| `export OPENAI_API_KEY=...` | Shell | Authenticate OpenAI calls |
| `python3 agent_app_evaluation_runner.py` | Command | Run full evaluation suite |
