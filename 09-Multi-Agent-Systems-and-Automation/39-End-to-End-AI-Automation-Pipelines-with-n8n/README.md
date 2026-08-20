# Building End-to-End AI Automation Pipelines with n8n

## Context of This Session

In the **previous** session you connected an **LLM provider** to n8n, wrote **system and user prompts**, **chained** AI output into Set / Sheets / Slack, used the **HTTP Request** node, and added **error branches** plus a **quality gate**.

This session joins those pieces into one **end-to-end pipeline**: ingest a document or message, **summarise** with an LLM, **route** by category or urgency, **deliver** to email, Slack, or a sheet, then **test** and **export** the workflow for handoff.

**In this session, you will:**

- **Design** an ingest → summarise → route → deliver automation on the n8n canvas
- **Integrate** Slack, email, and database-style sheet updates as workflow outcomes
- **Test** with a happy path, one **failure**, and one **edge-case** input
- **Document** credentials, dependencies, and operational assumptions for the next owner

---

## What Is an End-to-End AI Automation Pipeline?

Until now you practised **stations**. Today you run the **full train**: content arrives, AI processes it, the right people get notified, and a record is stored — without copy-paste.

- **Official Definition:** An **end-to-end AI automation pipeline** is a complete workflow that **ingests** content, applies **AI processing**, **routes** the result, and **delivers** a notification or storage update.
- **In Simple Words:** Inbox → smart reading → “who should see this?” → send / save. No human middle-copy.
- **Real-Life Example:** A **placement cell** receives internship reports and student messages. Staff should not read every page. The pipeline summarises, flags urgent cases to Slack, emails routine notes to a trainer, and logs every item in a sheet.

A pipeline is not “one clever LLM node.” It is a **contract**: what goes in, what must come out, and what happens when something fails.

![End-to-end n8n pipeline — ingest document or message, LLM summarisation, routing, then Slack email and sheet delivery](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session39/session39-01-e2e-pipeline-overview.png)

---

## Pipeline Blueprint — Campus Ops Inbox

Connecting sentence: Reuse the **training / placement feedback** story, but now treat every item as **content to process**, not only a short form comment.

### Target workflow

```text
Trigger (form / webhook / email text)
  → Normalise fields (Set)
  → IF raw_text present?
       ├─ no  → Sheets (needs_review); Slack only if you choose an empty-inbox alert
       └─ yes → LLM summarisation (structured JSON)
                  → Quality gate (IF)
                       ├─ pass → Router (IF / Switch by urgency)
                       │            ├─ high    → Slack + Sheets
                       │            ├─ medium  → Email + Sheets
                       │            └─ low     → Sheets only
                       └─ fail → Fallback Set → Slack alert + Sheets (needs_review)
```

| Stage | Job | n8n idea |
|---|---|---|
| **Ingestion** | Accept a document or message | Form, Webhook, or pinned sample |
| **Summarisation** | Short, structured AI output | Basic LLM Chain (from **previous**) |
| **Routing** | Choose the next path | IF or Switch |
| **Notifications / storage** | Tell people and keep a record | Slack, Email, Google Sheets |
| **Testing** | Prove happy, fail, and edge paths | Manual run + pin data |
| **Export** | Handoff the workflow | Download JSON + a short runbook |

**Common doubt:** *“Is this the same as the feedback classifier?”* — Same skills, **longer journey**. Ingestion can be a full report. Routing has **several outcomes**, not only one sheet row.

---

## Document and Message Ingestion

Connecting sentence: A pipeline is only as good as what it **accepts**. You must decide the **intake door**.

- **Official Definition:** **Document ingestion** is collecting raw content (file text, email body, chat message, form paste) into the workflow as structured fields the later nodes can read.
- **In Simple Words:** Putting the letter on the desk in a labelled tray before anyone summarises it.
- **Real-Life Example:** Students send a long internship write-up on WhatsApp, paste it into a form, or email a PDF. Ingestion turns that into `source`, `student_name`, `raw_text`.

### Intake options for this lab

| Trigger | Best when | Beginner note |
|---|---|---|
| **Form Trigger** | Classroom demo, file-or-paste | Easiest to test live |
| **Webhook** | Another app POSTs JSON | Same HTTP idea you already know |
| **Email / IMAP** (concept) | Real mailbox later | Needs mailbox credentials — skip if not set up |
| **Manual + Pin data** | Designing later nodes | Freeze a sample so you do not retype |

### Form fields for Campus Ops Inbox

Use a form named **Campus Ops Inbox**. Type field names **exactly** as below so `{{ $json.student_name }}` matches.

| Field | Type | Why it exists |
|---|---|---|
| `student_name` | text | Who sent it |
| `source` | dropdown: `form` / `email` / `chat` | Helps routing and the handoff doc |
| `raw_text` | textarea | The document or message body |
| `doc_title` | text (optional) | Filename or subject line |

**Why not only a PDF upload today?** Binary extract nodes differ by n8n version. Pasting **text** (or a short extracted excerpt) keeps the pipeline visible. If your build has **Extract from File**, you can still map extracted text into `raw_text`.

**Common errors:** Empty `raw_text`, 50-page paste that blows token limits, or mixing Hindi + English without telling the model. Ingestion should **reject empty body** early with an IF: `raw_text` is not empty.

### Activity — Choose the door

Write two lines: which trigger you will use in class, and one field you refuse to leave blank.

---

## Summarisation Step — LLM as a Processor

Connecting sentence: Ingestion gives you **raw_text**. Summarisation turns it into **fields the router can trust**.

You already know **Basic LLM Chain**, **system vs user**, and **JSON output**. Today the model is a **processor in the middle of a factory**, not the whole product.

- **Official Definition:** **Summarisation** here means an LLM step that compresses ingested content into a short summary plus labels (category, urgency, action) in a **fixed JSON shape**.
- **In Simple Words:** “Read this report. Give me 4 lines I can route.”
- **Real-Life Example:** A 900-word internship diary becomes: summary, category `complaint`, urgency `high`, action `call student`.

### System prompt (standing rules)

```text
You are a campus operations assistant.
Return ONLY valid JSON with keys:
summary, category, urgency, action, confidence.
category must be one of: complaint, query, praise, report, other.
urgency must be one of: high, medium, low.
summary: 2 to 4 short sentences. Do not invent names or scores.
action: one next step a staff member can do.
confidence: high, medium, or low.
If the text is empty or nonsense, still return JSON with
category "other", urgency "low", confidence "low".
```

### User prompt (live data)

```text
Student name: {{ $json.student_name }}
Source: {{ $json.source }}
Title: {{ $json.doc_title }}
Document or message:
{{ $json.raw_text }}
```

### Expected JSON shape

```json
{
  "summary": "Student reports delayed stipend for June internship. Asks placement cell to follow up with the company.",
  "category": "complaint",
  "urgency": "high",
  "action": "Email company HR and update the student on Slack.",
  "confidence": "high"
}
```

Keep **temperature low**. After the LLM, a **Set** (or small **Code**) node should expose those five keys cleanly — same chaining habit as **previous**.

**Quality reuse:** Fail the gate if `summary` is empty, `category` is not in the allowed list, or `confidence` is `low` **and** `urgency` is `high` (do not auto-page Slack on a guess).

![Ingestion to summarisation — form or webhook text enters Set then LLM JSON with summary category urgency](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session39/session39-02-ingest-summarise.png)

---

## Routing — Send Work to the Right Desk

Connecting sentence: A summary sitting in one node helps nobody. **Routing** decides the **next desk**.

- **Official Definition:** **Routing** is branching the workflow so different labels (urgency, category, source) take different delivery paths.
- **In Simple Words:** Urgent complaint → loud bell. Routine praise → quiet notebook.
- **Real-Life Example:** College exam cell: malpractice goes to the controller immediately; a seating query goes to a clerk’s email.

### Routing table for this pipeline

| Condition | Path | Why |
|---|---|---|
| `urgency` = `high` | **Slack** + **Sheets** | Someone must act now |
| `urgency` = `medium` | **Email** + **Sheets** | Trainer can handle in the inbox |
| `urgency` = `low` | **Sheets only** | Record without noise |
| Quality gate fail | **Slack alert** + Sheets `needs_review` | Human-in-the-loop |

Implement with **IF** nodes (two IFs is fine) or a **Switch** on `urgency`. Do not put Slack, Email, and Sheets in **one unbranched line** if you want different outcomes.

**Common mistake:** Routing on the **original essay** instead of the **LLM labels**. The router should read `urgency` / `category` after Set.

### Activity — Fill the router

For category `praise` and urgency `low`, which nodes run? For `complaint` + `high`?

---

## Delivery — Email, Slack, and Database-Style Updates

Connecting sentence: Routing without **delivery** is a labelled parcel that never leaves the sorting office.

- **Official Definition:** A **delivery mechanism** is a workflow outcome that notifies people (**email**, **Slack**) or updates stored records (**Sheets**, database).
- **In Simple Words:** Ring the right phone, and write it in the register.
- **Real-Life Example:** Hostel complaint: warden gets a WhatsApp-style Slack ping; the office clerk still writes the row in the complaint register (the sheet).

### Slack (urgent path)

Use the **Slack** node (or HTTP to a webhook URL if that is what your lab credential allows).

Message body idea:

```text
URGENT campus inbox
Student: {{ $json.student_name }}
Category: {{ $json.category }}
Action: {{ $json.action }}
Summary: {{ $json.summary }}
```

Store the Slack credential in n8n. Never paste the bot token on the canvas.

### Email (routine path)

Use **Gmail**, **SMTP**, or **Send Email** depending on your n8n setup. Subject should be boring and searchable:

```text
[Campus Ops] {{ $json.category }} — {{ $json.student_name }}
```

Body: summary + action + source. **BCC** a shared ops mailbox if the team wants an archive.

### Sheets as the database of record

Every path (including fallback) should **append one row**. Columns:

| Column | Source |
|---|---|
| timestamp | n8n `{{ $now }}` or a Set field |
| student_name | ingestion |
| source | ingestion |
| category | LLM |
| urgency | LLM |
| summary | LLM |
| action | LLM |
| delivery | `slack` / `email` / `sheet_only` / `review` |
| status | `ok` or `needs_review` |

**Why a sheet even when Slack already fired?** Notifications disappear in chat. The sheet is the **audit trail** for handoff and testing.

**Common doubt:** *“Can I use Postgres instead of Sheets?”* — Yes, later. For class, Sheets is the **database update** you can see immediately.

![Routing and delivery — high urgency to Slack, medium to email, all paths append a Google Sheets audit row](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session39/session39-03-route-notify.png)

---

## Build Walkthrough — One Complete Workflow

Restart local n8n if needed (same volume as **previous**):

```bash
docker volume create n8n_data   # named volume so workflows survive restarts
docker run -it --rm \           # interactive run; remove container on stop
  --name n8n \                  # easy name for docker stop later
  -p 5678:5678 \                # open the n8n UI on this machine
  -e GENERIC_TIMEZONE="Asia/Kolkata" \  # n8n schedule/clock in IST
  -e TZ="Asia/Kolkata" \        # container OS clock in IST
  -v n8n_data:/home/node/.n8n \ # mount the volume into n8n's data folder
  docker.n8n.io/n8nio/n8n       # official n8n image
```

### How the code works

- **Volume** keeps workflows and credentials across restarts.
- **Port 5678** is the UI at **http://localhost:5678**.
- **Timezone** keeps timestamps in India time for the sheet.

### Canvas steps

1. **Form Trigger** — fields listed above. Save as **Campus Ops Inbox Pipeline**.
2. **IF — body present** — if `raw_text` is empty, Set `status=needs_review`, skip LLM, and still **Append** a Sheets row.
3. **Basic LLM Chain + OpenAI Chat Model** — prompts from the summarisation section.
4. **Set / Edit Fields** — map `summary`, `category`, `urgency`, `action`, `confidence`.
5. **IF — quality gate** — allowed labels + non-empty summary.
6. **IF — urgency high?** — true → Slack; false → next IF.
7. **IF — urgency medium?** — true → Email; false → sheet-only.
8. **Google Sheets — Append** — on **every** surviving path (use extra connections or duplicate the Sheets node).
9. **Execute** once with a short sample, then inspect **each** node JSON.

Optional **Code** node if the model wraps JSON in markdown fences:

```javascript
// Read the LLM text from the previous node
const raw = $input.first().json.text || $input.first().json.output || "";
// Remove markdown code fences if the model added them
const cleaned = String(raw).replace(/```json/g, "").replace(/```/g, "").trim();
// Parse the remaining text as JSON
const data = JSON.parse(cleaned);
// Return one item with the five routing fields
return [{ json: data }];
```

### How the code works

- **`$input.first()`** is the current item from the previous node.
- **Fence strip** avoids `JSON.parse` failing when the model wraps JSON in markdown fences.
- **`return [{ json: data }]`** is n8n’s item format so Set / IF can read keys.

If parse throws, that is a **failure path** — do not hide it.

---

## Pipeline Testing — Happy, Failure, Edge

Connecting sentence: A pipeline that “worked once with my own essay” is not tested. You need **representative inputs**.

- **Official Definition:** **Pipeline testing** means running the workflow with planned samples: a normal case, a **failure** case, and an **edge case**, then checking **every branch** and the sheet row.
- **In Simple Words:** Try a normal letter, a blank letter, and a weird letter — then look at Slack, email, and the register.
- **Real-Life Example:** UPI apps test success, “insufficient balance,” and a ₹1 payment — not only a perfect ₹500 transfer.

### Test pack (pin each as data)

**Happy path — intern stipend complaint (should Slack + Sheets):**

```json
{
  "student_name": "Asha Verma",
  "source": "form",
  "doc_title": "June internship note",
  "raw_text": "My host company has not paid the June stipend. I mailed HR twice. Please help the placement cell follow up this week. I am in Batch 2026."
}
```

**Failure path — empty body (should skip LLM or fallback + review):**

```json
{
  "student_name": "Ravi Kumar",
  "source": "chat",
  "doc_title": "",
  "raw_text": ""
}
```

**Edge case — short, mixed, low-signal (should not false-alarm urgent Slack):**

```json
{
  "student_name": "Meera Iyer",
  "source": "email",
  "doc_title": "fw: fw: notes",
  "raw_text": "ok thanks. also see attachment. also Diwali. also maybe internship. lol. sent from my phone."
}
```

### What you must tick after each run

| Check | Happy | Failure | Edge |
|---|---|---|---|
| LLM node executed? | Yes | No / fallback | Yes, often `low` confidence |
| Slack fired? | Yes (urgent ops) | Optional empty-inbox alert only | No urgent ops ping; review alert only if gate fails |
| Email fired? | No | No | Maybe if labelled medium |
| Sheet row written? | Yes, `ok` | Yes, `needs_review` | Yes |
| Quality IF path? | pass | fail / empty IF | maybe fail if labels messy |

A **second edge** to try on paper: a 50-page paste. Expect token errors or a weak summary — that is why ingestion should cap length in the handoff assumptions.

**Pin data** on the Form output so you can re-run LLM and router without filling the form 20 times.

**Common error:** Testing only the happy path, then exporting. The next owner will hit empty text on day one.

### Activity — Record three runs

In a notebook, write: input name, which delivery fired, sheet `status`. Three rows only.

---

## Workflow Export and Handoff Documentation

Connecting sentence: A working canvas on **your** laptop is not a product. The next intern must **import**, **credential**, and **operate** it.

- **Official Definition:** **Workflow export** is saving the n8n workflow (usually **JSON**) plus a short document of **credentials**, **dependencies**, and **operational assumptions**.
- **In Simple Words:** Pack the recipe, the spice list, and the “don’t run this without gas” warning.
- **Real-Life Example:** Handing over a college fest registration desk: form link, Gmail login owner, “we close at 6 pm,” and “Slack channel is #fest-alerts.”

### Export from n8n

1. Open the workflow → **⋯** menu → **Download** / **Export** (JSON).
2. Keep a copy in your project folder, for example `campus-ops-inbox-pipeline.json`.
3. Confirm the file is **text JSON**, not a screenshot of the canvas.

Exported JSON includes **node graph and parameters**. It should **not** include secret key values if credentials are referenced by id — still **never** commit real API keys to Git.

### Handoff sheet (write this beside the JSON)

| Item | What to write |
|---|---|
| **Purpose** | Campus Ops Inbox: ingest → summarise → route → notify/store |
| **Trigger** | Form URL / webhook URL / when to use Manual |
| **Credentials needed** | OpenAI (or class LLM), Slack, Gmail/SMTP, Google Sheets |
| **Who owns each credential** | Names, not passwords |
| **Dependencies** | n8n version, Docker volume, internet, model name |
| **Sheet** | Spreadsheet name, tab, column list |
| **Slack channel** | e.g. `#campus-ops-urgent` |
| **Email inbox** | Trainer address used in the node |
| **Assumptions** | English-or-Hinglish text; empty body = review; high + low confidence ≠ auto Slack |
| **Test pack** | The three JSON samples above |
| **Failure behaviour** | Retry once (from **previous** lesson), then fallback + `needs_review` |
| **Do not** | Infinite retry; paste keys in prompts; skip the sheet row |

### Operational assumptions (say them out loud)

- The LLM **may be wrong**. Routing is only as good as labels + the quality gate.
- **Token / cost** limits: do not paste entire books into `raw_text`.
- **Timezone** is Asia/Kolkata for timestamps.
- **Active vs inactive** workflow: form/webhook only works if the workflow is **active** (or you execute manually in class).

![Testing and handoff — three sample inputs plus exported workflow JSON and a credentials runbook](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session39/session39-04-test-export-handoff.png)

### Activity — Mini runbook

Fill the handoff table with **your** channel names and sheet title. Leave secret values blank.

---

## Student Activities

### Activity 1 — Pipeline sketch

Draw boxes: Ingest → Summarise → Route → Deliver. Label each box with the n8n node type you used.

### Activity 2 — Ingestion contract

Write the four form fields. Circle the one that must never be empty, and write the IF condition in words.

### Activity 3 — Summary JSON

Without looking back, list the five JSON keys the LLM must return. Mark which two keys the **router** actually reads.

### Activity 4 — Routing decisions

Asha’s stipend text: which delivery nodes run? Meera’s “ok thanks lol” text: what should **not** happen?

### Activity 5 — Delivery map

Match: Slack / Email / Sheets-only to high / medium / low. Add one sentence on why Sheets still runs on **all** paths.

### Activity 6 — Test pack

Execute (or pin-and-execute) happy, empty, and edge samples. Tick the testing table. Note one surprise.

### Activity 7 — Handoff

List three credentials the next intern needs, and one assumption that will break if they import the JSON on a machine with no OpenAI key.

---

## Key Takeaways

- An **end-to-end AI pipeline** ingests documents or messages, **summarises** with an LLM, **routes** by labels, and **delivers** Slack, email, or storage updates.
- **Ingestion** must produce clean fields (`raw_text`, source, name) and reject empty bodies before you spend tokens.
- **Routing + delivery** turn AI JSON into real ops: urgent Slack, routine email, and a **sheet row on every path** as the audit trail.
- **Testing** needs a happy path, a **failure**, and an **edge case** — not only the sample that already worked.
- **Export JSON + a runbook** (credentials, dependencies, assumptions) is how the workflow survives beyond your laptop.

**Upcoming** work can deepen **production** habits: more channels, stricter monitoring, and richer agent loops on top of this same ingest → process → deliver spine.

---

## Important Commands, Libraries, and Terminologies Used

| Term / Command | Type | Meaning |
|---|---|---|
| **End-to-end pipeline** | Concept | Ingest → AI process → route → deliver |
| **Document ingestion** | Stage | Bring file text, form paste, or message into the workflow |
| **Message ingestion** | Stage | Chat/email-style text as the content source |
| **Summarisation** | AI step | Compress content into short text + labels |
| **Routing** | Pattern | IF/Switch paths from urgency or category |
| **Notification** | Outcome | Slack or email to a human |
| **Database / sheet update** | Outcome | Append an audit row (Sheets as beginner DB) |
| **Quality gate** | Habit | Check LLM JSON before routing |
| **Fallback** | Pattern | Safe path when AI or input fails |
| **Pin data** | Habit | Freeze sample output for repeat tests |
| **Pipeline testing** | Habit | Happy + failure + edge-case runs |
| **Edge case** | Test | Weird, mixed, or low-signal input |
| **Workflow export** | Skill | Download n8n JSON for backup/handoff |
| **Handoff / runbook** | Doc | Credentials, dependencies, assumptions |
| **Credential** | Security | Stored API key (LLM, Slack, Gmail, Sheets) |
| **Form Trigger** | Node | Classroom intake door |
| **Webhook** | Node | HTTP POST intake from another app |
| **Basic LLM Chain** | Node | Prompt + model → text/JSON |
| **IF / Switch** | Node | Routing and empty-body checks |
| **Slack node** | Node | Urgent human ping |
| **Email / Gmail / SMTP** | Node | Routine delivery |
| **Google Sheets Append** | Node | Register / audit trail |
| **Set / Edit Fields** | Node | Clean names after LLM |
| **Code node** | Node | Parse JSON, strip markdown fences |
| `localhost:5678` | URL | Local n8n UI |
| `docker volume create n8n_data` | Command | Persist n8n data |
| **Operational assumption** | Doc | Limits you rely on (language, size, timezone) |
