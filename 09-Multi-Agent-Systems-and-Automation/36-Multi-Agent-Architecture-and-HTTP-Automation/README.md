# Multi-Agent Architecture, HTTP & Automation Foundations

## Context of This Session

In the **previous** session, you applied everything you had learned to a **real-world use case** — an HR onboarding agent with a corpus, retrieval, tools, guardrails, escalation, and an evaluation harness.

All of that was still **one agent** doing one job. Now you build bigger systems. This session focuses on how to structure **multi-agent workflows**, and how **HTTP APIs**, **triggers**, and **webhooks** connect those workflows to real automation pipelines.

**In this session, you will:**

- Decide when a goal needs a **single agent** vs a **multi-agent system**
- Break a goal into sub-tasks with clear **inputs, outputs, and handoff points**
- Build the **researcher → writer → editor** pipeline, the cleanest multi-agent pattern to start from
- Use **HTTP methods**, **triggers**, and **webhooks** to start and chain automation
- Make automations survive the real world with **status codes**, **idempotency**, and **retries**

![Single agent juggling every step vs multi-agent system with specialized researcher, writer, and editor roles coordinated by an orchestrator](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session36/session36-01-single-vs-multi-agent.png)

---

## Why Multi-Agent Architecture Feels Different

When an agent does one job well, it is powerful. When a goal needs multiple different skills, a **multi-agent system** usually works better.

- **Official Definition:** A **multi-agent system** is a setup where multiple AI agents coordinate to achieve a goal.
- **In Simple Words:** Instead of one brain doing everything, you give each brain a job.
- **Real-Life Example:** Think of a restaurant kitchen where the **chef** cooks, the **tandoor** specialist handles naan, and the **waiter** coordinates delivery to the table. Each role is narrow, but together they deliver the full experience.

---

## Single-Agent vs Multi-Agent: The Decision Rule

Once you know what a multi-agent system is, you need a simple rule to decide when to split work.

### Single-Agent Workflow (one agent, many steps)

- **Official Definition:** A **single-agent system** is a workflow where one agent plans and executes the whole task.
- **In Simple Words:** One agent tries to think through everything end-to-end.
- **Real-Life Example:** One person trying to both design a poster, print it, and deliver it to customers.

### Multi-Agent Workflow (multiple agents, coordinated roles)

- **Official Definition:** A **multi-agent workflow** is a coordinated set of agent roles that hand work from one stage to the next.
- **In Simple Words:** Different agents cover different parts, and an orchestrator ensures the sequence works.
- **Real-Life Example:** A content pipeline where one person researches, one person drafts, and one person edits before publishing.

### When Multi-Agent is Appropriate

- **Data + tool mismatch:** Different parts of the goal need different tools or different retrieval setups.
- **Risk isolation:** One role can be constrained (for safety) while another role focuses on generation.
- **Complex decomposition:** The goal is naturally split into stages with clear handoffs.
- **Quality control:** You want separate checks (research groundedness, writing clarity, editorial style).

### Common Doubt: "Will this be slower?"

- Multi-agent can add overhead, but it often reduces rework because each role is specialized.
- If the system keeps retrying "the whole task," it wastes time; splitting helps localize failures.

### Activity — Pick the Right Architecture

Open your notebook and choose one goal you care about (examples: "prepare project notes," "plan a trip," "summarize a course chapter").

- Write the goal in one line.
- Circle the parts that feel different in nature (research vs writing vs checking).
- Decide: single-agent or multi-agent.
- Write one sentence explaining why your choice reduces mistakes.

---

## Task Decomposition: Turning One Goal into Sub-Tasks

After you decide to use multiple agents, you still need the "how" of splitting work.

- **Official Definition:** **Task decomposition** is the process of breaking a complex goal into smaller sub-tasks.
- **In Simple Words:** You chop the big problem into bite-size steps.
- **Real-Life Example:** If you want to submit an assignment, you decompose into "read question," "plan structure," "write," and "proofread."

### What "Good Decomposition" Looks Like

- Each sub-task should have a clear **input** (what that role needs) and a clear **output** (what it produces).
- Each handoff should have a **handoff point** where one agent stops and the next agent starts.
- Each output should be in a format that the next role can reliably use.

### Handoff Points You Can Design

- **Research handoff:** "Here are the evidence-backed points" (plus citations or references).
- **Draft handoff:** "Here is the first structured draft" (no final claims without review).
- **Edit handoff:** "Here are corrections and improvements" (style, clarity, and factual fixes).

### Common Doubt: "How do I know outputs are correct?"

- You define what "correct" means at each stage (groundedness for research, readability for writing, style + consistency for editing).
- You create quick checks that run before handing off (example: "did the researcher include evidence for each bullet?").

### Activity — Decompose a Goal with Role Inputs/Outputs

Pick any one goal and create a 3-stage plan on paper.

- Stage 1 (Research): write what the researcher must take as input and what it must output.
- Stage 2 (Write): write what the writer takes and what it outputs.
- Stage 3 (Edit): write what the editor takes and what it outputs.
- Add one "quality check" sentence for each stage.

---

## Role-Based Agents: Who Does What

Task decomposition is the plan, but roles are the execution style.

- **Official Definition:** A **role-based agent** is an agent constrained to a specific responsibility inside a workflow.
- **In Simple Words:** It has a job title and boundaries.
- **Real-Life Example:** In a train station, one person manages tickets, another manages platform directions, and another handles announcements.

### Why Roles Matter

- Roles reduce ambiguity: each agent knows what it should optimize for.
- Roles enable guardrails: you can restrict what a role is allowed to do.
- Roles simplify debugging: failures happen in a specific stage, not everywhere at once.

### Orchestrator vs Agents

- **Official Definition:** An **orchestrator** is a controller that coordinates when each agent runs.
- **In Simple Words:** It is the stage manager who schedules roles.
- **Real-Life Example:** A rehearsal director who says "research first, then draft, then review."

### Common Doubt: "Do we always need an orchestrator?"

- In simple demos, your "orchestrator" can just be a function that calls roles in order.
- In production, orchestration may be a separate service that handles retries, state, and observability.

---

## Sequential vs Collaborative Workflows

Now you can split work into roles, and the next decision is how those roles cooperate.

### Sequential Pipeline (one stage after another)

- **Official Definition:** A **sequential workflow** is where stage B starts only after stage A finishes.
- **In Simple Words:** Work flows in a strict order.
- **Real-Life Example:** Editing happens only after writing is done.

### Collaborative Multi-Agent Workflow (agents interact)

- **Official Definition:** A **collaborative workflow** is where multiple agents contribute together, often with feedback loops.
- **In Simple Words:** Roles can refine each other instead of only passing one-way outputs.
- **Real-Life Example:** During exam preparation, one person creates questions, another checks difficulty, and a third ensures coverage.

### Trade-offs

- Sequential is easier to reason about and easier to debug.
- Collaborative can improve quality but requires better coordination and more checks.

### Activity — Spot the Workflow Style

Read these two mini-scenarios and label each as sequential or collaborative.

- "Research finishes, then writing starts, then editing starts."
- "Writer drafts, researcher critiques sources, editor edits, then a final check updates claims."

---

## Researcher–Writer–Editor Pipeline (A Practical Multi-Agent Pattern)

This pipeline is a clean example because the roles naturally match different kinds of work.

![Sequential researcher-writer-editor pipeline with clear handoffs — evidence bullets flow into a draft, then into polished final notes](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session36/session36-02-researcher-writer-editor-pipeline.png)

- **Official Definition:** The **researcher–writer–editor pipeline** is a multi-stage workflow where research evidence feeds writing, and editing improves correctness and clarity.
- **In Simple Words:** Evidence first, words second, polishing last.
- **Real-Life Example:** A teacher who first collects references, then creates a lesson draft, then proofreads and improves explanations.

### Stage 1: Researcher

- **Goal:** Find evidence and structure key points.
- **Output shape:** Bullet points with claims linked to evidence.
- **Common doubt:** "What if the evidence is weak?"
  - If evidence is missing, the stage should mark "uncertain" instead of inventing.

### Stage 2: Writer

- **Goal:** Turn evidence into a clear narrative or structured content.
- **Output shape:** A draft with sections and plain-language explanations.
- **Common doubt:** "What if writer guesses?"
  - The writer should keep claims aligned with the researcher outputs.

### Stage 3: Editor

- **Goal:** Improve clarity, structure, and consistency.
- **Output shape:** Final notes or a corrected draft.
- **Common doubt:** "Should the editor change facts?"
  - If edits require changing facts, the editor should ask for corrected evidence.

---

## HTTP APIs as the Backbone for Agent Automation

Even with great agent roles, real systems must talk to external tools. That is where HTTP APIs come in.

- **Official Definition:** An **HTTP API** is a service that exposes operations through HTTP endpoints (URLs).
- **In Simple Words:** It is a standardized way for programs to "ask" and "tell" each other something.
- **Real-Life Example:** Like a government website where you submit a form and the system responds with status.

### Key HTTP Building Blocks

- **Official Definition:** An **endpoint** is a specific URL path where an API accepts requests.
- **In Simple Words:** It is a door in a building for one specific task.
- **Real-Life Example:** The "Passport" counter is an endpoint; the "Ticket refund" counter is another.

- **Official Definition:** A **request** is what a client sends to an API (method + path + headers + body).
- **In Simple Words:** It is your message.
- **Real-Life Example:** "I want to book a cab" is the request intent.

- **Official Definition:** A **response** is what the API sends back (status + headers + data).
- **In Simple Words:** It is the reply.
- **Real-Life Example:** "Cab booked" is the response.

### HTTP Methods You Will Use in Automations

An agent pipeline often needs different operations, so it uses different HTTP methods.

![HTTP API methods as service counters — GET reads, POST triggers, PUT replaces, PATCH updates partially, DELETE removes](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session36/session36-03-http-api-methods.png)

- **Official Definition:** **GET** retrieves data without changing server state.
- **In Simple Words:** "Show me."
- **Real-Life Example:** Checking the balance at an ATM.

- **Official Definition:** **POST** creates a resource or triggers an action.
- **In Simple Words:** "Do this."
- **Real-Life Example:** Submitting an application form.

- **Official Definition:** **PUT** updates a resource completely (full replacement).
- **In Simple Words:** "Overwrite with this full new version."
- **Real-Life Example:** Replacing a full file with a new file.

- **Official Definition:** **PATCH** updates a resource partially.
- **In Simple Words:** "Change only this part."
- **Real-Life Example:** Editing one line in a document.

- **Official Definition:** **DELETE** removes a resource.
- **In Simple Words:** "Remove it."
- **Real-Life Example:** Canceling a ticket.

### Common Doubt: "Which method should I choose?"

- Use `GET` for reading, `POST` for "create/trigger," `PUT/PATCH` for updates, and `DELETE` for removals.
- If it is a workflow start ("run pipeline now"), `POST` is usually the right mental model.

### Activity — Match the Method to the Task

Choose the best method for each scenario.

- You want to start a background pipeline job.
- You want to fetch the latest job status.
- You want to update only the job retry policy.
- You want to remove a job record.

---

## Triggers: Starting Automation from Events

Once HTTP is your communication channel, you still need "when to start." That is the trigger idea.

- **Official Definition:** A **trigger** is an event or signal that starts an automation or workflow.
- **In Simple Words:** It is the "start button."
- **Real-Life Example:** When you press "Submit" on a form, it triggers backend processing.

### Common Trigger Examples

- User submits a form (start pipeline).
- New file appears in a storage bucket (start ingestion).
- A job reaches a specific state (start next stage).

### How Triggers Connect to Agent Pipelines

- A trigger endpoint (often `POST`) receives input.
- The automation creates a job or background task.
- Stages run in order, and results are sent onward.

---

## Webhooks: Pushing Events back to Your System

Triggers start work, but webhooks are how completed work "reports back" reliably.

![Triggers start automation with POST while webhooks push completion events back — avoiding repeated polling checks](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session36/session36-04-triggers-and-webhooks.png)

- **Official Definition:** A **webhook** is an HTTP callback where a system sends an event to your endpoint.
- **In Simple Words:** It is the remote system calling your server when something happens.
- **Real-Life Example:** Delivery apps calling your phone with "your order is out for delivery."

### Why Webhooks are Useful

- They avoid constant "polling" (checking again and again).
- They let external tools notify your pipeline at the right time.
- They enable chaining: one service finishes, then notifies another.

### Webhook Payload and Signature (Security)

When a webhook arrives, you should treat it like untrusted input.

- **Official Definition:** A **webhook signature** is a cryptographic tag you use to confirm the payload came from the trusted sender.
- **In Simple Words:** It is a tamper-check seal.
- **Real-Life Example:** Checking a sealed packet before accepting it.

### Common Doubt: "Do webhooks always arrive once?"

- No. Network retries can cause duplicates.
- Your receiver should be prepared to accept repeated events safely (often using an event id).

---

## Making Automations Reliable: Status Codes, Idempotency, and Retries

The pipeline demo shows the flow, but production needs to survive networks, retries, and duplicates.

### HTTP Status Codes: Understanding the Reply

- **Official Definition:** An **HTTP status code** is a numeric indicator returned by a server to describe the result of a request.
- **In Simple Words:** It tells you "what happened" in one quick number.
- **Real-Life Example:** A shopkeeper's receipt tells you whether the payment succeeded or failed.

### Common Status Code Families in Automations

- **2xx:** The request succeeded and the server processed it normally.
- **4xx:** The client request is wrong (missing fields, wrong auth, invalid endpoint).
- **5xx:** The server failed (internal errors, dependency failure, timeout).

### Common Doubt: "Should the agent treat non-200 as failure?"

- For triggers, treat `2xx` as accepted and `4xx/5xx` as "needs handling."
- For webhooks, returning `2xx` usually tells the sender "do not retry," while `5xx` may trigger retries.

### Idempotency: Making Retries Safe

- **Official Definition:** **Idempotency** is a property where repeating the same operation multiple times produces the same final result.
- **In Simple Words:** "If the same message comes twice, nothing bad should happen."
- **Real-Life Example:** If you book the same cab twice due to network confusion, you should still end up with only one real booking.

### Idempotency Key and Event ID

- Use an **idempotency key** (or **event id**) so your receiver can detect duplicates.
- Store that id and ignore repeats after the first successful processing.

### Common Doubt: "Where should idempotency live?"

- Put idempotency logic in the place that receives the repeated input (often the webhook receiver).
- Keep the trigger endpoint safe too, because the caller may retry the `POST` request.

### Retries: When the Network is Unkind

- **Official Definition:** A **retry** is an attempt to perform an operation again after a failure.
- **In Simple Words:** "Try again in a controlled way."
- **Real-Life Example:** When the OTP does not arrive, you resend after a delay.

### Practical Retry Rules

- Retry only on failures that are likely temporary (timeouts, transient 5xx, connection errors).
- Use backoff (wait longer after each retry) to avoid overload.
- Set a max retry limit so the pipeline does not loop forever.

### Activity — Reliability Checklist for Your Workflow

On paper, write answers for these questions.

- What field will you use as an **idempotency key** (job id, webhook event id, or trigger request id)?
- What should happen if the webhook arrives twice?
- What status code will you return if the signature is invalid?
- What should your trigger endpoint do if it receives the same job twice?

---

## Observability: Logs, Correlation IDs, and Audit Trails

When something fails, you need evidence to debug quickly and to prove what happened.

- **Official Definition:** **Observability** is the ability to understand system behavior from logs, metrics, and traces.
- **In Simple Words:** It is your "system eyesight."
- **Real-Life Example:** A CCTV camera helps you see what happened when customers complain.

### Correlation ID: Tie Everything Together

- **Official Definition:** A **correlation id** is an identifier that links events and requests that belong to the same workflow run.
- **In Simple Words:** It is like a case number for a complaint.
- **Real-Life Example:** A hospital uses a patient file number across departments.

### What to Log in Multi-Agent HTTP Automation

- `job_id` for the pipeline instance.
- `stage_name` (researcher, writer, editor) for where failures occur.
- `request_id` for incoming HTTP calls.
- `callback_url` for outbound webhook delivery.

### Activity — Write Your Debug Story

Imagine the webhook receiver returns `accepted: False` because the signature is invalid.

- Write the 3 log fields you would check first.
- Write one possible cause (wrong secret, payload changed, header missing).
- Write one fix (share correct secret, sign exactly the received bytes, validate header presence).

---

## End-to-End API Automation Flow (What to Build)

Now you will see a complete mini example that uses `POST` to trigger a pipeline and then uses a webhook callback at completion.

![End-to-end flow — client POST starts the pipeline, server runs multi-agent stages in background, signed webhook POST notifies the receiver on completion](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session36/session36-05-end-to-end-automation-flow.png)

This demo follows this flow:

- You call `POST /v1/pipeline/start` with your goal and a `callback_url`.
- The server runs a researcher → writer → editor pipeline in a background task.
- When the pipeline finishes, it sends `POST` to the `callback_url` as a webhook.
- Your webhook receiver validates the signature and reads the payload.

---

## Code Demo: Multi-Agent Pipeline + Trigger + Webhook Callback

> **Runnable lab:** all three files below live in
> [`Coding-Examples/multi_agent_http_automation/`](../../Coding-Examples/multi_agent_http_automation/).
> If you want to see the whole flow **without installing anything or starting a server**, run
> `python3 main.py` in that folder — it reproduces the same trigger → pipeline → signed webhook flow
> (plus idempotency and tampered-payload demos) using only the Python standard library.

### What you need installed

- `fastapi`
- `uvicorn`
- `requests`

Run these commands in your terminal:

```bash
pip install fastapi uvicorn requests
```

### File 1: `multi_agent_http_webhook_demo_server.py`

```python
from fastapi import FastAPI, Request, BackgroundTasks  # Import FastAPI core types for endpoints and background tasks.
from pydantic import BaseModel  # Import BaseModel to define request body schemas.
import hashlib  # Import hashlib to compute SHA-256 hashes for signatures.
import hmac  # Import hmac to create secure message authentication codes (MAC).
import json  # Import json to encode/decode JSON payloads.
import time  # Import time to add timestamps to events.
import requests  # Import requests to send outbound HTTP webhook callbacks.
from typing import Dict, Any  # Import typing types for clearer payload structures.

app = FastAPI()  # Create the FastAPI app instance.

WEBHOOK_SECRET = b"dev-secret-change-me"  # Store a secret used to sign and verify webhook payloads.

class StartPayload(BaseModel):  # Define the expected body for starting the pipeline.
    user_goal: str  # Store the goal that the pipeline should process.
    callback_url: str  # Store the URL where the webhook callback will be sent.

def sign_bytes(payload_bytes: bytes) -> str:  # Create an HMAC signature for the given payload bytes.
    mac = hmac.new(WEBHOOK_SECRET, payload_bytes, hashlib.sha256)  # Compute HMAC using the secret and SHA-256.
    return mac.hexdigest()  # Convert the MAC result into a hex string for transport.

def researcher(goal: str) -> Dict[str, Any]:  # Simulate a research step that returns evidence-like bullets.
    bullets = [  # Create bullet points that look like evidence-backed claims.
        {"claim": "Decompose goals into roles to reduce rework", "evidence": "Pipeline design principle in agent workflows"},  # Example evidence text.
        {"claim": "Use HTTP endpoints to trigger and chain automation", "evidence": "HTTP request/response patterns for workflow orchestration"},  # Example evidence text.
        {"claim": "Use webhooks to notify completion without polling", "evidence": "Webhook callback mechanism avoids repeated checks"},  # Example evidence text.
    ]  # End bullets list.
    return {"stage": "researcher", "goal": goal, "bullets": bullets}  # Return structured research output.

def writer(research_output: Dict[str, Any]) -> Dict[str, Any]:  # Simulate a writing step that turns bullets into a draft.
    title = f"Draft for: {research_output['goal']}"  # Build a title using the goal.
    paragraphs = [  # Create short paragraphs to keep structure simple.
        "Explain the goal first, then split work into roles.",  # Describe decomposition in plain words.
        "Show that HTTP APIs trigger actions and return structured status.",  # Describe HTTP as workflow backbone.
        "Show that webhooks push events back to your system when done.",  # Describe webhook callback chaining.
    ]  # End paragraphs list.
    return {"stage": "writer", "title": title, "draft": paragraphs}  # Return structured writer output.

def editor(writer_output: Dict[str, Any]) -> Dict[str, Any]:  # Simulate an editing step that improves clarity and consistency.
    cleaned = [line.strip().rstrip(".") + "." for line in writer_output["draft"]]  # Normalize formatting for each paragraph line.
    return {"stage": "editor", "title": writer_output["title"], "final_notes": cleaned}  # Return structured final edited notes.

def run_pipeline_and_callback(goal: str, callback_url: str) -> None:  # Run the full pipeline and send a webhook callback.
    r = researcher(goal)  # Execute the researcher stage.
    w = writer(r)  # Execute the writer stage using research output.
    e = editor(w)  # Execute the editor stage using writer output.

    callback_payload = {  # Build the webhook payload that will be sent to the receiver.
        "goal": goal,  # Include the original goal for context.
        "stages": {"researcher": r, "writer": w, "editor": e},  # Include all stage outputs for debugging and audit.
        "completed_at": int(time.time()),  # Include a completion timestamp (epoch seconds).
    }  # End callback_payload.

    body_bytes = json.dumps(callback_payload).encode("utf-8")  # Convert payload dict into JSON bytes for signing.
    signature = sign_bytes(body_bytes)  # Create a signature for the JSON bytes.
    headers = {"Content-Type": "application/json", "X-Signature": signature}  # Add signature header so receiver can verify authenticity.

    # Send the webhook callback to the configured callback URL.
    requests.post(callback_url, data=body_bytes, headers=headers, timeout=10)  # Post the event payload with a timeout.

@app.get("/health")  # Define a health endpoint for quick checking.
def health() -> Dict[str, str]:  # Return a simple response object.
    return {"status": "ok"}  # Indicate the service is running.

@app.post("/webhooks/pipeline-complete")  # Define the webhook receiver endpoint.
async def pipeline_complete_webhook(request: Request) -> Dict[str, Any]:  # Receive webhook payload and validate it.
    body = await request.body()  # Read raw request body bytes for signature verification.
    received_signature = request.headers.get("X-Signature", "")  # Extract signature from headers (may be missing).
    expected_signature = sign_bytes(body)  # Compute expected signature from the shared secret and body.

    if not hmac.compare_digest(received_signature, expected_signature):  # Compare signatures securely to avoid timing leaks.
        return {"accepted": False, "reason": "invalid signature"}  # Reject if signature is wrong.

    decoded = json.loads(body.decode("utf-8"))  # Parse JSON payload into a Python dictionary.
    return {"accepted": True, "received_goal": decoded.get("goal")}  # Confirm acceptance and show one field for visibility.

@app.post("/v1/pipeline/start")  # Define a trigger endpoint that starts the pipeline.
async def start_pipeline(payload: StartPayload, background: BackgroundTasks) -> Dict[str, Any]:  # Accept input and schedule background execution.
    background.add_task(run_pipeline_and_callback, payload.user_goal, payload.callback_url)  # Run pipeline and then send webhook in background.
    return {"started": True, "callback_url": payload.callback_url}  # Respond immediately so the caller knows the job started.
```

Start the server with:

```bash
uvicorn multi_agent_http_webhook_demo_server:app --reload --port 8000
```

### File 2: `call_pipeline_client.py`

```python
import requests  # Import requests to call HTTP endpoints.

BASE_URL = "http://localhost:8000"  # Set the base URL for the local demo server.

def main() -> None:  # Define the main entry point.
    callback_url = f"{BASE_URL}/webhooks/pipeline-complete"  # Set the webhook receiver endpoint on the same server.
    payload = {  # Prepare the JSON body to start the pipeline.
        "user_goal": "Write lecture notes using multi-agent roles and automation",  # The goal that will be processed.
        "callback_url": callback_url,  # Where the webhook callback should be sent.
    }  # End payload.

    resp = requests.post(f"{BASE_URL}/v1/pipeline/start", json=payload, timeout=10)  # Call the trigger endpoint.
    resp.raise_for_status()  # Throw an error if the status code indicates failure.
    print("Start response:", resp.json())  # Print the JSON response returned by the start endpoint.

if __name__ == "__main__":  # Ensure main runs only when this file is executed directly.
    main()  # Call the main function.
```

Run the client in a second terminal:

```bash
python3 call_pipeline_client.py
```

### How the code works

- `POST /v1/pipeline/start` is the **trigger** that starts work.
- The server schedules `run_pipeline_and_callback` as a **background task** so the API responds quickly.
- `run_pipeline_and_callback` runs a simple **researcher → writer → editor** sequence and creates a structured payload.
- The server sends that payload using `requests.post(...)` to your `callback_url`.
- `POST /webhooks/pipeline-complete` is the **webhook receiver** that validates an `X-Signature` header.
- If the signature matches, the receiver returns `accepted: True`.

### File 3: `main.py` — the same flow with zero dependencies

The FastAPI version needs installs and a running port. `main.py` in the lab folder keeps the **same shape** — trigger, roles, signed callback, verification — but replaces the network with a tiny in-memory transport, so it runs anywhere:

```bash
python3 main.py
```

It adds the two production behaviours the FastAPI demo leaves out, so you can watch them work:

- **Idempotency** — the same `event_id` delivered twice is processed only once.
- **Signature rejection** — a payload edited after signing is rejected with `401`.

---

## Student Activities: Connect Concepts to Real HTTP/Webhooks

### Activity — Design the Trigger Endpoint

Write a new trigger endpoint design for your own workflow.

- Choose an operation that starts a background job.
- Decide the method (usually `POST`) and endpoint path (example: `/v1/pipeline/start`).
- Write the JSON fields you would accept (example: `job_type`, `input_data`, `callback_url`).

### Activity — Design a Webhook Payload

Create a webhook payload schema for an event like "task completed."

- Include the event type (example: `event_name`).
- Include the identifier you need for idempotency (example: `event_id`).
- Include output summary fields (example: `status`, `result_link`, or stage outputs).
- Write one sentence on how your receiver validates authenticity.

---

## Key Takeaways

- A **multi-agent system** splits complex goals into specialized roles that coordinate through handoffs.
- **Task decomposition** works best when each stage has clear inputs, outputs, and quality checks.
- **HTTP APIs** provide the standardized communication channel for triggering automation and exchanging state.
- **Triggers** start workflows, and **webhooks** push completion events back without repeated polling.
- **Idempotency keys** and **signature checks** are what make webhook delivery safe in the real world.
- A practical researcher–writer–editor pipeline is an easy pattern to scale into larger multi-agent architectures.

The next step is to add reliability: retries, idempotency, and stronger evaluation so multi-agent workflows stay correct as they get bigger.

---

## Important Commands, Libraries, and Terminologies Used

| Term / Command | Type | Meaning |
|---|---|---|
| **multi-agent system** | Concept | Multiple coordinated agents with role-based responsibilities |
| **task decomposition** | Concept | Breaking a goal into smaller sub-tasks with handoffs |
| **orchestrator** | Concept | Controller that coordinates when each role runs |
| **sequential workflow** | Concept | Next stage starts only after the previous stage finishes |
| **collaborative workflow** | Concept | Roles interact with feedback loops to improve quality |
| **HTTP API** | Concept | Service exposing operations through HTTP endpoints |
| **endpoint** | Concept | Specific URL path for one API operation |
| **trigger** | Concept | Event/signal that starts a workflow or job |
| **webhook** | Concept | HTTP callback where a system sends an event to your endpoint |
| **idempotency key** | Concept | Id (often `event_id`) used to process a repeated delivery only once |
| **webhook signature** | Concept | HMAC seal proving the payload came from the trusted sender, unmodified |
| `POST /v1/pipeline/start` | Endpoint | Trigger endpoint to start an automation job |
| `POST /webhooks/pipeline-complete` | Endpoint | Webhook receiver endpoint for pipeline completion events |
| `fastapi` | Library | Build HTTP APIs and webhook endpoints in Python |
| `uvicorn` | Server | Run the FastAPI app locally |
| `requests` | Library | Make outbound HTTP calls from the client/automation |
| `hmac` / `hashlib` | Library | Standard-library modules used to sign and verify webhook payloads |
| `pip install fastapi uvicorn requests` | Command | Install dependencies for the demo |
| `uvicorn multi_agent_http_webhook_demo_server:app --reload --port 8000` | Command | Start the demo server for the trigger + webhook receiver |
| `python3 call_pipeline_client.py` | Command | Call the trigger endpoint to start the demo pipeline |
| `python3 main.py` | Command | Run the dependency-free version of the whole flow |
