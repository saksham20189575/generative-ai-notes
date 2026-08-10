# Introduction to n8n Workflow Automation

## Context of This Session

In the **previous** session, you learned **multi-agent architecture**, **HTTP APIs**, **triggers**, and **webhooks**. You saw how specialised roles hand work forward, and how an external system can start a job or push a completion event over HTTP.

This session introduces **n8n** — a **visual workflow automation platform** where those same ideas become a canvas of connected steps. You will navigate the workspace, use **triggers**, **nodes**, **connections**, **expressions**, and **credentials**, and validate a first trigger-driven workflow with inspectable inputs and outputs.

**In this session, you will:**

- **Explain** n8n as a visual platform for connecting services and orchestrating tasks
- **Configure** triggers and node connections that move data through a simple multi-step flow
- **Apply** credentials and environment settings securely for third-party integrations
- **Validate** a baseline workflow run by inspecting each node's input and output

---

## Why Visual Workflow Automation Matters

Until now, connecting Sheets, Slack, an LLM, and a database often meant writing Python and debugging one long script. That works for engineers — but many teams need automation without a full coding sprint for every small process.

- **Official Definition:** **Workflow automation** is software that runs a sequence of steps when a condition is met, moving data between tools with minimal manual work.
- **In Simple Words:** Like **auto-debit** for your electricity bill — the same steps happen every month without visiting the office.
- **Real-Life Example:** A college **placement cell** receives hundreds of form submissions. Copying each row into a sheet and mailing confirmations by hand becomes error-prone at scale.

**n8n** gives you a **visual canvas** for that journey: what starts the flow, what each step does, and what data moves forward.

![n8n visual workflow automation — canvas connecting form trigger, AI, Sheets, and email instead of coding every connection](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session37/session37-01-n8n-workflow-overview.png)

---

## What Is n8n?

n8n (pronounced "n-eight-n") is a popular tool for building **business workflows**, **integrations**, and **AI workflows** through a visual interface.

- **Official Definition:** **n8n** is a **workflow automation platform** — a drag-and-drop engine for connecting apps, databases, APIs, and AI models into multi-step automations.
- **In Simple Words:** A **visual backend** where you pick blocks from a menu instead of typing every integration in code.
- **Real-Life Example:** A **CA firm** wants monthly reports from Tally, email, and Google Sheets. With n8n, a finance person can wire those steps on a canvas without becoming a full-stack developer first.

### Core Properties

| Property | What it means |
|---|---|
| **Visual / no-code first** | Drag-and-drop nodes; thousands of pre-built integrations |
| **1,500+ integrations** | Google Sheets, Slack, Gmail, Postgres, WhatsApp, GitHub, and more |
| **Optional code** | Python or JavaScript inside **code nodes** when you need custom logic |
| **Any LLM** | OpenAI, Anthropic, Gemini, Ollama — connect the model you choose |
| **Observability** | See each node's **input** and **output** on the canvas |
| **Templates** | Pre-built workflow examples on the n8n website to learn from |

**Common doubt:** *"If it is no-code, can I never write code?"* — You **can**. Use the UI for standard integrations; use a **code node** when you need full control.

### n8n vs "Just Using an LLM"

An **LLM** is one piece of an agentic application. Real systems also need **triggers**, **databases**, **email**, and **conditional logic**. n8n bundles those **tools** around the LLM — that is why it is broader than chatting with a model alone.

This connects to the **previous** lesson: HTTP triggers and webhooks are how outside systems start work; n8n turns those same ideas into reusable visual building blocks.

---

## Hosting Models — Cloud vs Self-Hosted

n8n is **not entirely free** for production use on their cloud. Understanding hosting helps you choose how to practise.

- **Official Definition:** **Hosted n8n** runs workflows on n8n's servers; **self-hosted n8n** runs on your laptop or company servers.
- **In Simple Words:** **Hosted** = renting a furnished flat. **Self-hosted** = running the app on your own computer for learning.
- **Real-Life Example:** A student testing automations uses **Docker on a laptop** (free for learning). A company serving hundreds of employees may pay for **n8n cloud** or host on **AWS**.

| Option | Do you need Docker? | Best for |
|---|---|---|
| **n8n cloud** | **No** — build in the browser | Teams that want public URLs and zero server setup |
| **Self-hosted with Docker** | **Yes** — class method | Free local practice |
| **Self-hosted without Docker** | **No** — npm/server install | Experienced developers |

**Free path for learning:** Run n8n **locally with Docker**. You can also activate a **free license key** (emailed during setup) to unlock features on self-hosted instances.

---

## Website Walkthrough — Example Workflows

Before installing, study how **triggers**, **nodes**, and **branches** fit together on n8n.io.

### HR — New Employee Onboarding

**Trigger:** Form submission — HR fills a "create user" form (name, email, department, manager).

**Typical flow:** AI agent → Postgres (store data) → Jira ticket → **If manager?** branch (manager channel vs regular profile update).

- **Real-Life Example:** When you join a large company, HR does not manually create every account and ticket — automation chains handle repeatable onboarding.

### Sales — Insights from Reviews

Load reviews → cluster or classify with an LLM → write ranked leads into **Google Sheets** so sales knows whom to call first.

### SecOps — Incident Enrichment

**Trigger:** New security ticket → extract IP/domain → virus/URL scan → merge reports for the analyst.

- **Real-Life Example:** A bank **SOC** team cannot manually scan every suspicious URL at 2 a.m. — automation enriches the ticket before a human opens it.

These examples show the pattern you will build in smaller form today: **trigger → process → store or notify**.

### Platform Habits Worth Copying

- **Build visually** — place nodes left to right so the story of the workflow is readable.
- **Inspect every decision** — open outputs after each test run before adding the next node.
- **Human in the loop** — for refunds, transfers, or ticket booking, pause for approval instead of blind auto-action.
- **Start from templates** — import an HR or sales template from n8n.io, then delete nodes until you understand each one.

---

## n8n and Docker — Two Different Things

Many beginners assume **n8n = Docker**. That is **not** correct.

| Tool | What it actually is |
|---|---|
| **n8n** | The **workflow automation application** — canvas, nodes, triggers, integrations |
| **Docker** | A **helper program** that runs packaged apps in isolated boxes on your laptop |

- **Official Definition:** **Docker** is a **container runtime** — software that launches pre-packaged apps without manual dependency setup.
- **In Simple Words:** **n8n** is the **car**. **Docker** is a **ready parking slot** so you can drive without building the engine.
- **Real-Life Example:** **WhatsApp** is not the same as the **Play Store**. n8n is the app; Docker is one convenient install method.

**You are not learning Docker as a career skill here.** You only need enough to **start n8n**, open **localhost:5678**, and **stop** the container when done.

![n8n vs Docker — three ways to run n8n: cloud, Docker self-host, advanced self-host](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session37/session37-02-n8n-vs-docker-three-ways.png)

### Three Docker Words

| Term | Plain meaning | n8n example |
|---|---|---|
| **Image** | Frozen installer package | Official n8n download |
| **Container** | Running copy of that image | n8n working right now |
| **Volume** | Saved folder that survives restarts | Your workflows and login |

**Common doubt:** *"If I close Docker, do I lose my workflows?"* — **No**, if you used a **volume** (`n8n_data`).

---

## Install and Run n8n with Docker

**Prerequisites:** Install **Docker Desktop**, wait until it shows "running", allow disk space for the image (~few GB).

### Step 1 — Create a Volume

```bash
# Create a named volume — stores all n8n data on your machine
docker volume create n8n_data
```

### How the code works
- **`docker volume create`** reserves persistent storage.
- **`n8n_data`** is the volume name used in the next command.

### Step 2 — Run the Container (Mac / Linux)

```bash
# Start a new container and remove it when the process stops
# --name n8n gives the running container a clear name
# -p 5678:5678 maps host port 5678 to container port 5678
# -e GENERIC_TIMEZONE sets n8n schedule timezone to India
# -e TZ sets the container system timezone to India
# -v n8n_data:/home/node/.n8n attaches the volume so workflows persist
# docker.n8n.io/n8nio/n8n is the official n8n image to download and run
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -e GENERIC_TIMEZONE="Asia/Kolkata" \
  -e TZ="Asia/Kolkata" \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

### How the code works
- **`docker run`** starts a container from an image.
- **`-p 5678:5678`** exposes n8n at **http://localhost:5678**.
- **`-e GENERIC_TIMEZONE` / `-e TZ`** set India time for schedules.
- **`-v n8n_data:/home/node/.n8n`** attaches the volume so workflows persist.
- **`docker.n8n.io/n8nio/n8n`** is the official image URL.

**Windows tip:** Use a single line, or the backtick `` ` `` instead of `\` for line breaks.

### Step 3 — Open the Workspace

1. Go to **http://localhost:5678**
2. Create an **owner account**
3. Optional: request a **free license key** by email and activate it

**Localhost vs public links:** A form URL like `http://localhost:5678/form/...` works **only on your machine**. Classmates cannot open it. Public URLs need **n8n cloud** or a server with a public address — the same idea as exposing a webhook endpoint in the **previous** session.

---

## The n8n Workspace

After login, choose **Build workflow**. The editor feels like **draw.io** — a blank canvas where you add steps.

### Every Workflow Starts with a Trigger

A **trigger** answers: *"When should this automation start?"*

| Trigger type | When it fires | Example |
|---|---|---|
| **Trigger manually** | You click **Execute** | Safe testing |
| **On app event** | Something happens in a connected app | New Google Sheets row |
| **On a schedule** | Cron-style timing | Every day at 9 a.m. |
| **On webhook call** | External system sends HTTP | Razorpay payment success |
| **On form submission** | Someone submits a form | Student feedback form |
| **When executed by another workflow** | Another workflow calls this one | Reusable sub-flows |

**Connecting sentence:** A **webhook trigger** in n8n is the visual version of the HTTP callback pattern you studied earlier — an outside system POSTs an event, and your workflow starts.

### Schedule Trigger — Plain English

- Run **every day**, **hour**, **week**, or **month** at a fixed time.
- Example: At **10 a.m. daily**, pull yesterday's data, analyse it, and email a report to managers.
- Timezone matters — that is why the Docker command sets **Asia/Kolkata**.

### Webhook Trigger — Payment Flow Recap

1. Customer pays via a Razorpay link on your site.
2. Razorpay sends an HTTP callback — success, failure, or expired.
3. Your n8n workflow **starts** — ship product, send receipt, or alert finance.

This is the same **event → start job** idea as a FastAPI trigger endpoint, except n8n draws the steps on a canvas.

![n8n trigger types — manual, schedule, webhook, form, and app event](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session37/session37-03-triggers-and-nodes.png)

Once a trigger exists, the **+** menu offers AI nodes, actions (Sheets, Gmail, Slack), logic, and code. Order matters: you cannot put a form page before a **form trigger**.

---

## Nodes — Every Step on the Canvas

- **Official Definition:** A **node** is one **action or decision** in a workflow — a single step on the canvas.
- **In Simple Words:** One **station** on a train route — form station, transform station, spreadsheet station.
- **Real-Life Example:** In a **dosa shop**, taking order, cooking, and billing are separate steps — each could be one node.

| Category | Role | Example |
|---|---|---|
| **Trigger node** | Starts the workflow | Form trigger, webhook |
| **Action node** | Talks to an external service | Google Sheets — create row |
| **AI / LLM node** | Calls a language model | Sentiment on feedback text |
| **Logic node** | Branching rules | If rating ≥ 4 → priority path |
| **Code / Set node** | Transform data | Map fields, add computed values |

---

## Connections and Data Flow

Connecting sentence: Nodes alone do nothing useful until you link them so data can travel.

- **Official Definition:** A **connection** is the link between two nodes that defines how **output** from one becomes **input** to the next.
- **In Simple Words:** The **track** between train stations — wrong track, wrong destination.
- **Real-Life Example:** Form output `{ "email": "...", "rating": 5 }` must connect to the next node that expects those field names.

**Data flow** is the journey: trigger → transform → store or notify. Open any executed node to see exactly what arrived and what left — that is **observability**.

---

## Expressions — Dynamic Values

- **Official Definition:** An **expression** is a formula that computes a value at **runtime** from input data instead of using a fixed constant.
- **In Simple Words:** Like an **Excel formula** — the cell updates when marks change.
- **Real-Life Example:** A report card grade depends on marks, not a letter typed once in January.

**Static (bad for automation):**

```text
grade = "A"
```

**Dynamic (expression logic):**

```text
if marks > 90 → grade A
if marks > 80 → grade B
otherwise → grade C
```

In n8n you often use `{{ }}` syntax to reference earlier fields, for example `{{ $json.rating }}` or `{{ $json.name }}`. Agents and automations must react to **changing** form data — expressions glue steps without rewriting the workflow for every student.

---

## Credentials and Environment Settings

Connecting Google Sheets, Slack, or OpenAI requires **permission**. n8n stores that permission as a **credential**.

- **Official Definition:** A **credential** in n8n is a securely stored authentication record (API key, OAuth token) that authorizes access to a third-party service.
- **In Simple Words:** The **key card** for Google Sheets — kept in a safe, not taped to the monitor.
- **Real-Life Example:** If a company **Slack** login leaked, strangers could join internal channels — credential security is non-negotiable.

### Secure Habits

- Credentials are **not** stored as plain text on the canvas.
- Prefer the **Credentials** UI over pasting secrets into node fields.
- On self-hosted setups, put secrets in **environment variables** that n8n reads at runtime.

**Never do this:**

```bash
# BAD — hard-coding a secret in a script or chat
token="sk-abc123plaintext"
```

**Prefer this pattern on your machine:**

```bash
# Set an API key in the environment before starting tools that need it
export OPENAI_API_KEY="your-key-here"
```

### How the code works
- **`export`** places the value in the process environment for child programs.
- The key stays out of the workflow JSON you share or screenshot.
- On **n8n cloud**, enter secrets in the **settings UI** instead of terminal `export`.

### OAuth2 in Simple Words

- **Official Definition:** **OAuth2** lets a third-party app (n8n) get **limited** access to your Google (or other) account **without** sharing your password with n8n.
- **In Simple Words:** Like **Login with Google** on a website — you approve scopes; Google issues a token.
- **Real-Life Example:** A photo app may reasonably ask for Google Photos access; a school portal usually needs only email — grant **minimum** permissions.

High-level Google Sheets setup: open the node → **Set up credentials** → **OAuth2** → Client ID / Secret from Google Cloud → consent screen → paste spreadsheet URL.

![Credentials vault and OAuth2 — secure data flow from form to Sheets](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session37/session37-04-credentials-oauth-data-flow.png)

---

## First Workflow — Form Trigger, Transform, Inspect

You will now build a **baseline multi-step workflow**: form submission → enrich fields with an expression → inspect outputs at each node.

### Build Order (Important)

**Common mistake:** Adding a form page before a **form trigger** causes: *"Form Trigger node must be set before this node."*

**Correct order:**

1. First step → **On new n8n form event** (form trigger)
2. Configure form fields
3. Add a **Set** (or **Edit Fields**) node connected from the trigger
4. Execute and inspect Table / JSON / Schema at **each** node

### Form Fields

| Field | Type | Notes |
|---|---|---|
| **Name** | Text | Required |
| **Email** | Email | Validates format |
| **Batch** | Text | Required |
| **Rating** | Dropdown | Options 1–5 |

**Form title:** Feedback form

### Step after the Trigger — Enrich with Expressions

In the **Set** node, create mapped fields such as:

| Output field | Expression idea |
|---|---|
| `student_name` | `{{ $json.Name }}` (or your field's exact name) |
| `contact_email` | `{{ $json.Email }}` |
| `priority` | If rating ≥ 4 → `high`, else `normal` |

This is a **connection + expression** practice: data leaves the trigger, arrives at the Set node, and leaves again in a cleaner shape for Sheets, Slack, or an LLM later.

### Conceptual Next Step (Optional Preview)

```
Form trigger → Set (enrich) → Google Sheets (create row)
```

Sheets needs credentials (OAuth2). Even if you stop at Set today, you have already configured **trigger**, **connection**, **expression**, and **per-node inspection**.

### Execute and Validate

1. Click **Execute workflow** / **Execute step** on the form trigger
2. Submit test data — e.g. name **Deepak**, valid email, rating **5**
3. Open the trigger node → check **Table**, **JSON**, **Schema**
4. Open the Set node → confirm `priority` is `high` when rating is 5
5. If a later node fails, inspect the **previous** node's JSON first — mismatched field names are the most common issue

| View | What you see |
|---|---|
| **Table** | Columns for each field |
| **JSON** | Structured object for the next node |
| **Schema** | Field names and types |

**Test mode** is fine for learning. Production forms on cloud get public URLs; localhost links stay private.

### Baseline Validation Checklist

Use this checklist every time you claim a workflow "works":

- Trigger fired for the expected reason (form submit, not a random manual click unless you intended that).
- Trigger **JSON** contains all required fields with correct types (email looks like an email; rating is a number or chosen dropdown value).
- Connection exists from trigger → Set (no orphaned nodes).
- Set node **output** shows enriched fields (`priority`, mapped names) without nulls for required data.
- Field names used in expressions match the **exact** names from the previous node's schema (case-sensitive mismatches are common).
- If a third-party node is added later, credentials show as **connected** before you blame the expression.

### Observability and Human-in-the-Loop

- Trace **what went in** and **what came out** of every node.
- When step 3 fails, open step 2's JSON before rewriting step 3.
- For critical actions (refunds, money transfers), pause for **human approval** instead of full auto-run.

### Docs Habit

Every node has a **Docs** link in the editor. Use it for parameters, credential steps, and examples — you do not need to memorise every field name.

---

## Student Activities

### Activity 1 — Trigger Pick

**Scenario:** Every night at 11 p.m., compile the day's Razorpay payments and email a summary to finance.

Which trigger fits best — **manual**, **schedule**, **webhook**, or **form**? Write one sentence explaining why.

### Activity 2 — Map Onboarding Boxes

Draw four boxes: **Form submit** → **?** → **Jira ticket** → **If manager?**. Fill the missing middle step in one sentence.

### Activity 3 — Form Field Design

Design three fields for a workshop registration form: text, email, dropdown (Beginner / Intermediate / Advanced). Mark which are required and why email should use type **email**.

### Activity 4 — Static vs Expression

A workflow receives `marks = 85`. Write plain-English rules: A if > 90, B if > 80, C otherwise. What grade should output for 85?

### Activity 5 — OAuth Permission Check

An app asks for email, Drive, Photos, and Gmail read — but only shows your name on screen. List two permissions you would deny and why.

### Activity 6 — n8n vs Docker

Answer in one sentence each: Is n8n the same as Docker? Name one way to use n8n without Docker. What URL/port do you open after local setup, and why can a classmate not open your localhost form link?

### Activity 7 — Inspect JSON Shape

Given form output:

```json
{
  "name": "Priya",
  "email": "priya@example.com",
  "rating": 4
}
```

Write one sentence: which fields would a Sheets "create row" node map from this JSON?

---

## Key Takeaways

- **n8n** is a visual automation platform with many integrations — UI for standard steps, code when you need flexibility.
- **n8n and Docker are different** — Docker is only one way to run n8n locally; cloud needs no Docker.
- **Triggers** start workflows; **nodes** do work; **connections** pass data; **expressions** compute dynamic values.
- **Credentials**, environment variables, and **OAuth2** keep third-party access secure without plain-text secrets.
- Validate every run by inspecting **input/output** at each node — that baseline habit scales into larger agentic workflows later.

Upcoming practice will deepen multi-step integrations (Sheets, webhooks, LLM nodes) on top of this workspace foundation.

---

## Important Commands, Libraries, and Terminologies Used

| Term / Command | Type | Meaning |
|---|---|---|
| **n8n** | Platform | Visual workflow automation (independent of Docker) |
| **Docker** | Tool | Runs packaged apps in containers; one way to self-host n8n |
| **n8n cloud** | Hosting | Browser-hosted n8n — no Docker required |
| **Workflow** | Concept | Connected steps from trigger to outcome |
| **Trigger** | Concept | Event that starts a workflow |
| **Node** | Concept | One step/action on the canvas |
| **Connection** | Concept | Link passing output to the next node's input |
| **Data flow** | Concept | How information moves through the workflow |
| **Expression** | Concept | Runtime formula for dynamic values (`{{ }}`) |
| **Credential** | Concept | Stored API key / OAuth token for a service |
| **OAuth2** | Protocol | Scoped access without sharing your password |
| **Environment variable** | Config | Secret set outside the workflow (`export ...`) |
| **Docker image** | Term | Frozen installer package |
| **Docker container** | Term | Running copy of an image |
| **Docker volume** | Term | Persistent storage for workflows |
| **Form trigger** | Node | Starts on form submission |
| **Webhook trigger** | Node | Starts on external HTTP callback |
| **Schedule trigger** | Node | Starts on a timer |
| **Set / Edit Fields** | Node | Maps and enriches fields between steps |
| **Observability** | Habit | Inspect per-node inputs, outputs, errors |
| **Human-in-the-loop** | Habit | Require approval for critical actions |
| **localhost:5678** | URL | Local n8n UI after Docker start |
| `docker volume create n8n_data` | Command | Create persistent volume |
| `docker run ... docker.n8n.io/n8nio/n8n` | Command | Start local n8n container |
| `export OPENAI_API_KEY=...` | Command | Set API key in environment (self-hosted) |
