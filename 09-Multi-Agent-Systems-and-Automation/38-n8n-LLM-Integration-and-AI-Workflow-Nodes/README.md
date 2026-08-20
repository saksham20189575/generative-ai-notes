# n8n LLM Integration and AI Workflow Nodes

## Context of This Session

In the **previous** session you navigated the **n8n workspace**, ran n8n locally, and built a first **trigger-driven workflow** with **nodes**, **connections**, **expressions**, and **credentials**. You practised a **form trigger → Set (enrich) → inspect** path and learned that every node has inspectable **inputs** and **outputs**.

This session adds **intelligence** to that canvas. You will connect an **LLM provider**, configure **prompts** with structured workflow inputs, **chain** AI output into downstream actions, handle **failures** with retry or fallback branches, and **evaluate** AI output against simple quality checks before delivery.

**In this session, you will:**

- **Connect** an LLM provider (for example OpenAI) to n8n and configure system + user prompts
- **Chain** multiple nodes so AI text becomes input to Set, Sheets, Slack, or HTTP actions
- **Handle** common LLM failures with **IF / error** branches, retry, and fallback paths
- **Evaluate** AI step outputs against simple quality criteria before sending data downstream

---

## Why Add an LLM Inside n8n?

In the **previous** build, the form → Set path could map fields and set `priority` with expressions. That works for dropdown ratings. Real feedback is often **free text** — *"Delivery was late and the box was damaged"* — which expressions alone cannot classify well.

- **Official Definition:** An **LLM node** in n8n calls a large language model to generate or transform text as one step inside a workflow.
- **In Simple Words:** You insert a smart reading-and-writing station on the train route — not only copy-paste stations.
- **Real-Life Example:** A placement cell receives long internship reviews. An LLM can summarize each review and label sentiment as **positive / neutral / negative** before the trainer sees the sheet.

n8n already connects apps. An LLM turns messy human language into **structured, usable fields** for the next node.

![n8n AI workflow — form trigger feeds an LLM node that classifies feedback, then Set and Sheets receive structured sentiment and summary for downstream delivery](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session38/session38-01-llm-workflow-overview.png)

---

## Recap — What You Bring From the Previous Session

Keep the same mental model:

| Building block | Role on the canvas |
|---|---|
| **Trigger** | Starts the workflow (form, webhook, schedule, app event) |
| **Node** | One action or decision |
| **Connection** | Passes output → next input |
| **Expression** | Dynamic value like `{{ $json.rating }}` |
| **Credential** | Secure key for a third-party service |

Today you reuse that vocabulary and add **AI nodes**, **prompt configuration**, the **HTTP Request** node, **error branches**, and a **quality gate**.

**Common doubt:** *"Do I need a new Docker install?"* — No. Restart the same local n8n at **http://localhost:5678** with your existing volume if you still have it.

### Quick restart (if the container is stopped)

```bash
# Create volume only if missing; then start n8n (comments describe each flag)
# --name n8n | -p 5678:5678 | Asia/Kolkata timezone | volume n8n_data | official image
docker volume create n8n_data
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -e GENERIC_TIMEZONE="Asia/Kolkata" \
  -e TZ="Asia/Kolkata" \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

### How the code works
- **`docker volume create`** is safe to re-run only when needed; existing volumes keep workflows.
- **`-p 5678:5678`** opens the UI at **http://localhost:5678**.
- **Timezone flags** keep schedule triggers aligned to India time.
- **Volume mount** preserves credentials and workflows across restarts.

---

## LLM Nodes Available in n8n

Open a workflow → click **+** after a trigger → look under **AI**.

| Node / pattern | When to use it |
|---|---|
| **Basic LLM Chain** | Simple prompt → model → text (best starter) |
| **OpenAI / Anthropic / Gemini / Ollama** chat model | The model sub-node attached under a chain |
| **AI Agent** | Multi-step tool-using agent (later depth) |
| **Information Extractor / Sentiment** style helpers | Structured fields when available in your n8n version |

- **Official Definition:** A **Basic LLM Chain** is an n8n pattern that takes a prompt, calls a chat model, and returns text output.
- **In Simple Words:** You write instructions; the model writes the reply; the next node reads that reply.
- **Real-Life Example:** Asking a senior intern to "summarise this feedback in two lines and say if the student is happy or unhappy."

**Rule for today:** Prefer **Basic LLM Chain + OpenAI Chat Model** for clarity. Full agent templates can wait until you are comfortable with prompts and chaining.

---

## Connect an LLM Provider Securely

Connecting sentence: Just as Google Sheets needed OAuth in concept form earlier, an LLM needs an **API credential**.

### OpenAI credential in n8n

1. Add **Basic LLM Chain** after your form (or Set) node.
2. Attach **OpenAI Chat Model** as the model sub-node.
3. **Set up credential** → paste your **OpenAI API key**.
4. Save — n8n verifies the key.
5. Choose a model (for learning: a cost-friendly GPT model such as **gpt-4o-mini** or the current class recommendation).

**Never** paste the API key into the prompt text or a sticky note on the canvas.

```bash
# Optional on self-hosted machines — set the key in the environment before starting tools
export OPENAI_API_KEY="your-key-here"
```

### How the code works
- **`export`** places the secret in the process environment.
- n8n’s credential store is still preferred for keys used inside the UI.
- On **n8n cloud**, enter keys in the credentials UI — you cannot SSH into their servers.

**Common error:** `Error in subnode, OpenAI chat model` — usually means missing/invalid key, wrong model name, or the sub-node was not saved. Fix credentials first, then re-execute.

### Activity — Connect the provider once

1. Create or open a workflow named **Feedback AI classifier**.
2. Ensure a form trigger (or pin sample form JSON) exists from the **previous** pattern.
3. Add **Basic LLM Chain** + **OpenAI Chat Model**.
4. Save the OpenAI credential and execute the model node once with a tiny test prompt: `Reply with the word OK`.

---

## Prompt Configuration for Structured Workflow Inputs

Connecting sentence: A connected model without a clear prompt is like hiring a tutor without telling them the syllabus.

- **Official Definition:** **Prompt configuration** means writing the **system** and **user** messages (and mapped fields) that tell the LLM what to do with workflow data.
- **In Simple Words:** System = standing rules. User = this specific task + this specific data.
- **Real-Life Example:** System: "You are a polite placement-cell assistant." User: "Classify this review and return JSON."

### System prompt (role and boundaries)

```text
You are a helpful assistant for training feedback analysis.
Return ONLY valid JSON with keys: sentiment, summary, priority.
sentiment must be one of: positive, neutral, negative.
summary must be one short sentence.
priority must be high if negative, else normal.
Do not invent student details that are not in the input.
```

### User prompt (task + data from previous node)

Use **Define below** and drag fields from the form / Set node. Example shape:

```text
Student feedback to analyse:
Name: {{ $json.Name }}
Email: {{ $json.Email }}
Batch: {{ $json.Batch }}
Rating: {{ $json.Rating }}
Free-text comment: {{ $json.Comment }}

Classify sentiment and summarise. Reply with JSON only.
```

**Why JSON?** Downstream nodes need predictable keys (`sentiment`, `summary`, `priority`) — the same idea as matching sheet column names in the **previous** session.

**Common mistakes:**

- Hard-coding one student's comment instead of using expressions
- Asking for "a nice paragraph" when the next node expects **JSON**
- Forgetting to expand the prompt editor when instructions get long

### Activity — Write a structured prompt

On paper or in the n8n prompt box:

1. Write a **system** prompt with role + JSON keys.
2. Write a **user** prompt that references at least two fields with `{{ }}`.
3. Execute once and open the LLM node **JSON** output panel.

---

## Chain AI Output Into Downstream Actions

Connecting sentence: The LLM is useful only when its answer becomes the next station’s luggage.

### Target chain for this session

```
Form trigger → (optional Set) → Basic LLM Chain → Set / Edit Fields → Google Sheets or Slack
```

| Step | Job |
|---|---|
| **Form trigger** | Collect Name, Email, Batch, Rating, Comment |
| **LLM Chain** | Produce `sentiment`, `summary`, `priority` |
| **Set** | Map LLM fields into clean names for Sheets |
| **Sheets / Slack** | Store or notify (needs credentials) |

### Parsing LLM text into fields

LLM output often arrives as a **text** string. If the model returned JSON text, use a **Set** node or a small **Code** node to expose:

- `sentiment`
- `summary`
- `priority`

Then map those into Google Sheets columns or a Slack message body with expressions — never retype the values.

**Optional Code node idea:** if the model wraps JSON in markdown code fences, strip the fence lines first, then parse the remaining text to JSON, and return clean fields (`sentiment`, `summary`, `priority`). Keep a simple English comment on every line if you add this in class — same documentation habit as earlier Python labs.

**Temperature tip:** For classification and JSON extraction, use a **low temperature** (near 0) so labels stay stable.

- **Official Definition:** **Chaining AI steps** means wiring LLM output as the input of later automation actions so the pipeline continues without human copy-paste.
- **In Simple Words:** Whatever the model wrote becomes the next node's starting material.
- **Real-Life Example:** After the chef tastes the dish (LLM), the waiter labels the plate (Set) and delivers it to the table (Sheets/Slack).

### Parallel AI idea (preview)

Independent tasks can run as **two LLM nodes** from the same trigger (summarise + extract actions). A **Merge** waits for both. Fuller parallel pipelines deepen in the **upcoming** end-to-end session — today, master **one clear chain** first.

![AI chaining — LLM JSON output mapped through Set into Sheets columns and a Slack notify path](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session38/session38-02-ai-chaining-downstream.png)

### Activity — Chain one AI output

1. Execute the LLM node with a sample negative comment.
2. Confirm `sentiment` is `negative` and `priority` is `high`.
3. Add a **Set** node that maps `summary` → `feedback_summary`.
4. Inspect Set output — field names must match what Sheets will expect.

---

## HTTP Request Node — Call APIs Directly

Connecting sentence: Not every AI call must use a branded LLM node. Sometimes you call the provider (or your own FastAPI service) with **HTTP Request** — the same HTTP idea from multi-agent automation foundations.

- **Official Definition:** The **HTTP Request** node sends an HTTP call (GET, POST, etc.) to any URL and returns the response to the workflow.
- **In Simple Words:** A phone call from n8n to another server — "please do this and reply."
- **Real-Life Example:** POST feedback JSON to your own `/v1/analyse` API, or call OpenAI’s chat completions URL with a bearer token.

### When to use HTTP Request vs LLM node

| Use **LLM / Basic Chain** when | Use **HTTP Request** when |
|---|---|
| You want quick UI prompts and model picker | You call a **custom backend** you built |
| Standard OpenAI/Anthropic chat is enough | The API is not in n8n’s AI menu |
| Beginners need fewer headers/JSON details | You need exact headers, query params, or raw body control |

### Example POST body shape (conceptual)

```text
POST https://api.openai.com/v1/chat/completions
Authorization: Bearer <from credential / header auth>
Content-Type: application/json

{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "system", "content": "Return JSON with sentiment and summary."},
    {"role": "user", "content": "{{ $json.Comment }}"}
  ]
}
```

### How this works in the workflow
- Method **POST** starts a write/analyse operation (same idea as earlier **POST** triggers).
- Headers carry **auth** — store tokens in credentials / header auth, not on the canvas.
- Response JSON is inspected like any other node output, then mapped downstream.

**Common doubt:** *"Is HTTP Request replacing LLM nodes?"* — No. LLM nodes are convenience wrappers. HTTP Request is the **general tool** for any API — including APIs that are not LLMs (tickets, CRM, your FastAPI webhook receiver).

### Activity — Design an HTTP step on paper

Write four lines:

1. URL you would call
2. Method (`GET` or `POST`)
3. One header that must stay secret
4. Which response field the next node would read

---

## Error Branches — Retry and Fallback Paths

Connecting sentence: LLM steps fail — rate limits, bad keys, empty model output, network timeouts. Production workflows need a **Plan B**, not only a happy path.

- **Official Definition:** An **error branch** (or failure path) is a workflow route that runs when a node errors or when output fails a check — often for **retry**, **fallback**, or **human alert**.
- **In Simple Words:** If the smart station is closed, send luggage to the backup desk instead of dropping it on the floor.
- **Real-Life Example:** If UPI fails at checkout, the app offers card payment or "try again" — it does not silently vanish.

### Common LLM failure modes

| Failure | Typical cause | Beginner response |
|---|---|---|
| Auth / 401 | Bad or missing API key | Fix credential; do not loop forever |
| Rate limit / 429 | Too many calls | Wait / retry with backoff; alert on repeat |
| Empty or garbage text | Weak prompt or model glitch | Fallback template message |
| Invalid JSON | Model ignored format rules | Re-ask with stricter prompt or use fallback |

### Pattern A — IF after LLM (quality / format check)

```
LLM Chain → IF (output looks valid?) 
              ├─ true  → Set → Sheets
              └─ false → Fallback Set (safe defaults) → Slack alert
```

Example IF idea: `sentiment` is one of `positive|neutral|negative` **AND** `summary` is not empty.

### Pattern B — On Error path

Many n8n nodes support continuing on fail / error output:

```
LLM Chain
  ├─ success → normal chain
  └─ error   → Wait (optional) → Retry LLM once → still fail? → notify human
```

**Retry rule for beginners:** Retry **once or twice**, then **fallback**. Infinite retries burn money and still fail.

### Fallback content example

If the LLM fails, Set node can write:

| Field | Fallback value |
|---|---|
| `sentiment` | `unknown` |
| `summary` | `AI summary unavailable — please review manually` |
| `priority` | `high` (so humans still look) |

![Error and fallback branches — LLM success path to Sheets versus failure path with retry once then Slack alert and safe defaults](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session38/session38-03-error-fallback-branches.png)

### Activity — Draw your failure path

For the feedback classifier, write:

1. One condition that means "LLM output is bad"
2. What the **true** path does
3. What the **false / error** path does (include one human alert)

---

## Evaluate AI Output Before Downstream Delivery

Connecting sentence: Chaining is dangerous if you trust every model sentence blindly. Add a **quality gate** before Sheets, Slack, or email.

- **Official Definition:** **Output evaluation** (beginner level) means checking AI results against simple, explicit criteria before they affect customers or databases.
- **In Simple Words:** A teacher checks the answer key before posting marks — not after parents complain.
- **Real-Life Example:** Do not auto-tweet an LLM summary until it has a minimum length, no banned words, and valid sentiment labels.

### Simple quality criteria checklist

Use this before marking a workflow "done":

- **Format:** Output is JSON (or the exact shape next nodes need)
- **Allowed labels:** `sentiment` ∈ {positive, neutral, negative}
- **Non-empty:** `summary` has at least ~10 characters
- **Grounding:** Summary does not invent a batch or email that was not in the input
- **Safety:** No API keys or passwords appear in the generated text
- **Priority logic:** If sentiment is `negative`, `priority` should be `high`

### Implement the gate in n8n

1. After LLM, add **IF** (or Code) that tests the checklist.
2. **Pass** → continue to Sheets / notify.
3. **Fail** → route to fallback + optional human-in-the-loop sticky note / Slack.

**Pin data** while tuning prompts and IF rules (same habit as before). **Unpin** for a realistic end-to-end form submit.

### Baseline validation for an AI step

| Check | Pass looks like |
|---|---|
| LLM node executed green | Output panel shows text/JSON |
| Expression fields resolved | Name/comment not literally `{{ $json.Comment }}` |
| Quality IF true path runs on good sample | Negative comment → high priority stored |
| Error path tested once | Invalid key or empty summary hits fallback |

---

## Build Walkthrough — Feedback Form + LLM Classifier

Use this as the main hands-on spine. It stays in sync with the **previous** form workflow and adds AI.

### Step 1 — Form trigger fields

| Field | Type | Required |
|---|---|---|
| Name | Text | Yes |
| Email | Email | Yes |
| Batch | Text | Yes |
| Rating | Dropdown 1–5 | Yes |
| Comment | Textarea | Yes |

### Step 2 — LLM Chain

- System + user prompts from earlier (JSON keys required)
- OpenAI credential connected
- Execute with sample: rating `2`, comment *"Mentor never joined the doubt session"*

### Step 3 — Quality IF

- True if sentiment in allowed set and summary non-empty
- False → fallback Set + alert

### Step 4 — Downstream Set + optional Sheets

Map `sentiment`, `summary`, `priority`, plus original email/name.

### Step 5 — Inspect every node

Open **Table / JSON / Schema** on Form, LLM, IF, and Set — the observability habit from the **previous** session still applies.

![Quality gate before delivery — IF checks sentiment labels and non-empty summary then allows Sheets update or sends fallback for human review](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session38/session38-04-quality-gate.png)

---

## Student Activities

### Activity 1 — Prompt vs expression

A rating dropdown can set priority with an expression. A free-text comment cannot. Write one sentence explaining **when** you need an LLM node instead of only `{{ }}` expressions.

### Activity 2 — System vs user

Label each line as **system** or **user**:

1. "You only return JSON."
2. "Comment: {{ $json.Comment }}"
3. "Never invent student emails."
4. "Batch: {{ $json.Batch }}"

### Activity 3 — Chain map

Draw boxes: Form → LLM → ? → Sheets. Fill the missing box and name two fields that must be mapped.

### Activity 4 — HTTP vs LLM node

Pick one: call OpenAI chat completions from a branded LLM node, or from HTTP Request. Write one reason for your choice for a beginner classroom demo.

### Activity 5 — Failure drill

API returns 429 rate limit. Should your workflow (a) retry forever, (b) retry once then fallback + alert, or (c) ignore and write empty rows? Justify in one sentence.

### Activity 6 — Quality gate

Which outputs should **fail** the gate?

```json
{"sentiment": "awesome", "summary": "", "priority": "low"}
```

```json
{"sentiment": "negative", "summary": "Mentor missed the doubt session.", "priority": "high"}
```

### Activity 7 — Inspect before blame

LLM looks fine but Sheets stays empty. List the **first two** panels you open (which nodes?) before changing the prompt again.

---

## Key Takeaways

- **LLM nodes** add language understanding to n8n — classify, summarise, and structure messy text for later steps.
- **Prompt configuration** (system + user + expressions) must request a **predictable shape** (often JSON) so chaining works.
- **HTTP Request** is the general API tool when you need custom backends or raw control; LLM nodes are the convenient path for standard providers.
- **Error branches** with limited retry and clear **fallback** keep automations safe when models or networks fail.
- **Quality criteria** before Sheets/Slack/email prevent bad AI text from becoming bad business data.

**Upcoming** work extends this into fuller **end-to-end AI pipelines** — document or message ingestion, summarisation, routing, notifications, testing, and workflow export for handoff.

---

## Important Commands, Libraries, and Terminologies Used

| Term / Command | Type | Meaning |
|---|---|---|
| **LLM node** | Concept | n8n step that calls a language model |
| **Basic LLM Chain** | Node | Prompt + model → text output pattern |
| **OpenAI Chat Model** | Sub-node | Model provider attachment under a chain |
| **System prompt** | Config | Standing role and rules for the model |
| **User prompt** | Config | Task + live workflow data for this run |
| **Prompt configuration** | Skill | Designing system/user messages and mapped fields |
| **Chaining AI steps** | Pattern | AI output becomes input to later nodes |
| **HTTP Request node** | Node | Generic GET/POST (and more) calls to any URL |
| **Error branch** | Pattern | Path taken on failure or failed checks |
| **Retry** | Pattern | Re-attempt a failed LLM/API call a limited number of times |
| **Fallback** | Pattern | Safe default path when AI cannot complete |
| **Quality gate / evaluation** | Habit | Check AI output against simple criteria before delivery |
| **IF node** | Node | True/false branch for format or business rules |
| **Set / Edit Fields** | Node | Map and clean fields after the LLM |
| **Merge** | Node | Wait for / combine parallel branches (preview) |
| **Credential** | Security | Stored API key for OpenAI or other providers |
| **Pin data** | Habit | Freeze sample output while designing later nodes |
| **Observability** | Habit | Inspect per-node Table / JSON / Schema |
| `export OPENAI_API_KEY=...` | Command | Set API key in environment (self-hosted helper) |
| **localhost:5678** | URL | Local n8n UI |
| **JSON output** | Format | Structured LLM reply for reliable downstream mapping |
| **Rate limit (429)** | Error | Too many API calls — retry carefully, then fallback |
| **Human-in-the-loop** | Habit | Send unclear/failed AI cases to a person |
| **Downstream action** | Concept | Sheets, Slack, email, or HTTP after the AI step |
