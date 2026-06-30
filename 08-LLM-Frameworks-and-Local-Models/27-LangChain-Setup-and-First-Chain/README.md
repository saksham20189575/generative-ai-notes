# LangChain Environment Setup and First LCEL Chain

## Context of This Session

In the **previous** session, you learned what **LangChain** is, why teams use a **framework** instead of scattered API glue, and how **Runnables** snap together into **chains**. You saw **PromptTemplate**, the **LCEL pipe operator** (`|`), **StrOutputParser**, and a guided demo ending in **`prompt | llm | parser`**.

Before that, you installed **Ollama**, pulled a **light local model**, called it from **Python**, and stored settings safely in **`.env`**. That gave you a working model on your laptop.

Today you move from **concepts** to a **real project worktree**: isolated **venv**, installed packages, secure **folder layout**, configuration through **environment variables**, and a first end-to-end chain on **ChatOllama** using **ChatPromptTemplate**.

**In this session, you will:**

- Create an isolated **Python environment** with LangChain and Ollama integration packages
- Apply a **collaborative project layout** with **`.env`** conventions
- Bind **ChatOllama** to your Ollama host and model name from configuration
- Compose **`ChatPromptTemplate | ChatOllama | StrOutputParser`** as one LCEL pipeline
- Run **`hello_chain.py`** and **validate** output across distinct inputs

---

## Why a Proper Environment Matters

Concepts are useless if packages fight on your laptop. LangChain projects need **version-matched** libraries — `langchain-core`, `langchain-ollama`, and helpers like **`python-dotenv`**.

- **Official Definition:** A **virtual environment (`venv`)** is an isolated Python interpreter and `site-packages` folder dedicated to one project.
- **In Simple Words:** Separate notebooks for separate subjects — maths notes do not mix with chemistry notes.
- **Real-Life Example:** One college project needs an old library version; another needs a new one. A **venv** stops them from fighting on the same machine.

Installing into **system Python** often causes:

- **`ModuleNotFoundError`** when a teammate clones your repo
- **Version conflicts** between this module and other work on your laptop
- **Accidental commits** of API keys inside `.py` files

![Virtual environment isolation for LangChain projects — global Python can have package conflicts, while each project venv keeps its own dependency versions separate](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260113/module3/session36/session36-01-environment-isolation.png)

### Create and activate a virtual environment

From your module worktree folder (for example `langchain_worktree/`):

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python3 -m venv venv
venv\Scripts\activate
```

After activation, your prompt usually shows **`(venv)`**. Run **`which python`** (macOS/Linux) — the path should point **inside** `venv/`, not `/usr/bin/python3`.

- **Common mistake:** Installing packages **before** activation — they land in global Python and the chain script still fails inside the venv.
- **Deactivate** when you leave the project: `deactivate`.

> **[ Student Activity ]**
>
> **Venv Check**
>
> Activate your venv and run `which python` and `pip list`. Confirm Python lives inside `venv/` and that `langchain-core` is **not** listed yet. This baseline proves the environment is isolated before you install anything.

---

## Required Packages

With the venv active, install the minimal stack for today's chain.

- **Official Definition:** A **package** is reusable code published for installation via **pip**.
- **In Simple Words:** Ready-made tools — like a Maggi packet instead of making noodles and masala from scratch.
- **Real-Life Example:** You do not build a car engine to go to college; you use a bus that already runs on a fixed route.

```bash
pip install -U pip langchain-core langchain-ollama python-dotenv
```

| Package | Role |
| --- | --- |
| **`langchain-core`** | **ChatPromptTemplate**, **StrOutputParser**, **LCEL**, Runnable base |
| **`langchain-ollama`** | **ChatOllama** — LangChain wrapper for your Ollama server |
| **`python-dotenv`** | Loads **`.env`** key-value pairs into `os.environ` at runtime |

If pip prints **requirement already satisfied**, that is fine — it means the package is already in this venv.

- **Common mistake:** Typing `pip install langchain` only — today's demo needs **`langchain-core`** and **`langchain-ollama`** explicitly.
- **Prerequisite:** **Ollama** must be running and your model tag must appear in **`ollama list`** (for example `qwen2.5:0.5b` from your earlier local setup).

---

## Safe Project Layout and Environment Variables

Professional LangChain repos separate **code**, **secrets**, and **local tooling** so teammates can collaborate without leaking keys.

- **Official Definition:** An **environment variable** is a name-value pair stored outside source code and read at runtime.
- **In Simple Words:** A private sticky note your program reads when it starts — not written on the Python file itself.
- **Real-Life Example:** Your ATM PIN is required to use the card, but you do not engrave the PIN on the plastic.

Recommended layout for this module worktree:

```text
langchain_worktree/
├── venv/                 # Local virtual environment (do not commit)
├── .env                  # Machine-local secrets and settings (do not commit)
├── .env.example          # Committed template with empty placeholders
├── .gitignore            # Lists .env and venv/
├── hello_chain.py        # Builds, runs, and validates the LCEL chain
└── requirements.txt      # Optional: pinned package list for teammates
```

### `.env` — what belongs inside

For **local Ollama**, you usually need **no API key**. You still centralise **model name** and **host** so one change updates every script.

**`.env`** (create locally — do not commit):

```text
OLLAMA_MODEL=qwen2.5:0.5b
OLLAMA_HOST=http://localhost:11434
OLLAMA_TEMPERATURE=0.3
USE_CLOUD=0
OLLAMA_API_KEY=
```

**`.env.example`** — same keys as `.env`, committed with empty or placeholder values only.

**`.gitignore`** (minimum entries):

```text
venv/
.env
__pycache__/
*.pyc
```

### Safety rules for collaborative work

- Never hardcode **API keys** or production URLs inside Python files.
- Add **`.env`** to **`.gitignore`** — share **`.env.example`** instead.
- Read **model** and **host** from **`os.environ`** after **`load_dotenv()`** — the same pattern you used for Ollama Cloud earlier.
- **Common mistake:** Committing `.env` to GitHub — treat it like your ATM PIN written on a public notice board.

> **[ Student Activity ]**
>
> **Layout Drill**
>
> Create the folder tree above. Copy `.env.example` to `.env` and set `OLLAMA_MODEL` to the exact tag from `ollama list`. Add `.env` and `venv/` to `.gitignore`. This mirrors how real teams onboard new developers without sharing private keys in chat.

---

## ChatOllama — Binding LangChain to Ollama

In the **previous** session the model step used **ChatOllama** with hard-coded settings. Today those values come from **`.env`** so swapping model or host does not mean editing chain logic.

- **Official Definition:** **ChatOllama** is a LangChain **chat model Runnable** that sends chat messages to an Ollama server and returns a model response object.
- **In Simple Words:** The adapter between LangChain's language and Ollama's language.
- **Real-Life Example:** LangChain speaks Hindi; Ollama speaks Tamil — **ChatOllama** is the translator at the counter.

| Setting | Typical local value | Where it lives |
| --- | --- | --- |
| **`model`** | `qwen2.5:0.5b` | `OLLAMA_MODEL` in `.env` |
| **`base_url`** | `http://localhost:11434` | `OLLAMA_HOST` in `.env` |
| **`temperature`** | `0.3` for stable demos | `OLLAMA_TEMPERATURE` in `.env` |
| **`num_predict`** | Approximate output token cap (e.g. `100`) | Optional in code — limits runaway length on small models |

### Temperature

- **Official Definition:** **Temperature** controls randomness in model output — lower values are more deterministic.
- **In Simple Words:** Low temperature = strict exam answer. High temperature = creative story competition.
- **Real-Life Example:** Mess menu announcement (low) vs fresher's event poster copy (high).

For classroom demos, **`0.3`** keeps answers focused. Raise it only when you deliberately want more variety.

### Before you invoke

1. Ollama daemon running (desktop app or background service).
2. Model pulled: `ollama pull qwen2.5:0.5b` (or your chosen tag).
3. **`ChatOllama(model=...)`** uses the **same string** as `ollama list`.
4. **Common mistake:** `connection refused` on port **11434** — Ollama is not running.

---

## ChatPromptTemplate — Reusable Chat Messages

The **previous** demo used **`PromptTemplate`** — one formatted **string**. Chat models work better with **role-based messages**: **system** (how to behave) and **human** (the user's ask).

- **Official Definition:** **ChatPromptTemplate** builds a **list of chat messages** with `{placeholder}` slots filled at runtime.
- **In Simple Words:** A wedding invitation template — structure stays fixed; names, venue, and date change per family.
- **Real-Life Example:** A college helpdesk script: system says *"You are polite and brief"*; human says *"Explain {topic} to {audience}"*.

### System and human messages

- **System message:** Sets behaviour — tone, role, format rules.
- **Human message:** Carries the actual request with variables like `{topic}` and `{audience}`.

### `from_template` vs `from_messages`

- **`from_template()`** — one simple string prompt (what you used with **PromptTemplate**).
- **`from_messages()`** — a **list** of role tuples like `("system", "...")` and `("human", "...")`.

**Common mistake:** Calling **`from_template()`** with a list of messages — use **`from_messages()`** when you have system + human roles.

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a beginner-friendly instructor. Be concise."),
    ("human", "Explain {topic} to {audience} using one analogy from {analogy_domain}."),
])
```

Keys in **`invoke({...})`** must match placeholder names **exactly** — `{topic}` needs `"topic"` in the dict, not `"subject"`.

---

## LCEL — LangChain Expression Language

LCEL is how you declare a pipeline without writing manual step-by-step glue.

- **Official Definition:** **LCEL** (LangChain Expression Language) composes **Runnables** into a chain using the **pipe operator** `|`.
- **In Simple Words:** Connect prompt → model → parser the way metro stations connect — board at one stop, interchange, exit at the next.
- **Real-Life Example:** Dosa counter at Saravana Bhavan — batter to tawa, dosa to plate, plate to customer. Order is fixed.

```text
ChatPromptTemplate  →  ChatOllama  →  StrOutputParser
```

```python
chain = prompt | llm | output_parser
```

### How data moves

1. **`invoke({"topic": "REST APIs", ...})`** fills template placeholders.
2. **ChatPromptTemplate** outputs a message list for the chat model.
3. **ChatOllama** calls Ollama and returns a response object.
4. **StrOutputParser** extracts plain text — a Python **string**.

![LCEL chain flow with LangChain and Ollama — input dictionary goes into ChatPromptTemplate, then ChatOllama at localhost, then StrOutputParser returns a plain string response](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260113/module3/session36/session36-02-lcel-chain-flow.png)

The mental model matches what you built **previously** — only the **prompt type** (**ChatPromptTemplate**) and **configuration source** (**.env**) are new.

---

## StrOutputParser — Clean String Output

Without a parser, **`chain.invoke()`** may return an **`AIMessage`** object — fine for debugging, awkward for a UI.

- **Official Definition:** **StrOutputParser** extracts text content from a model response and returns a plain Python **string**.
- **In Simple Words:** Swiggy delivers bag, bill, and tissue — you eat only the food. The parser gives only the answer text.
- **Real-Life Example:** A marksheet PDF vs the single percentage number your app displays on screen.

| Chain ending | What `print(result)` shows |
| --- | --- |
| `prompt \| llm` | Message object with `.content` and metadata |
| `prompt \| llm \| StrOutputParser()` | **Plain string** ready for UI or logs |

---

## Full Code — `hello_chain.py`

This file is the **module proof script**: load config, build the chain, run it, and validate across multiple inputs.

**File: `hello_chain.py`**

```python
# Standard library — read configuration from the environment
import os  # Access environment variables after dotenv loads them

# Load .env file into os.environ before reading any settings
from dotenv import load_dotenv  # Reads key=value pairs from .env on disk

# LangChain Core — prompt template and output parser
from langchain_core.prompts import ChatPromptTemplate  # Chat messages with {placeholders}
from langchain_core.output_parsers import StrOutputParser  # Returns plain string from model reply

# Ollama integration — chat model wrapper
from langchain_ollama import ChatOllama  # Runnable that talks to your Ollama server

# Load .env from the same folder as this script
load_dotenv()  # Makes OLLAMA_MODEL, OLLAMA_HOST, etc. available via os.environ

# Read model settings from .env — defaults match local teaching setup
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")  # Must match ollama list
BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")  # Local Ollama address
TEMPERATURE = float(os.environ.get("OLLAMA_TEMPERATURE", "0.3"))  # Lower = more stable demos


def build_chain():  # Factory function — returns a reusable LCEL chain
    # Chat-style prompt with separate system and human roles
    prompt = ChatPromptTemplate.from_messages([  # Use from_messages for role tuples
        ("system", (  # System instruction — how the model should behave
            "You are a beginner-friendly programming instructor. "
            "Explain concepts in simple language with short bullet points. "
            "Avoid long introductions."
        )),
        ("human", (  # User request with placeholders filled at invoke time
            "Explain {topic} to {audience} using one analogy from {analogy_domain}."
        )),
    ])

    # ChatOllama Runnable — credentials and endpoint from .env block above
    llm = ChatOllama(
        model=MODEL_NAME,  # Tag from OLLAMA_MODEL — same as ollama list
        base_url=BASE_URL,  # Host from OLLAMA_HOST — usually localhost:11434
        temperature=TEMPERATURE,  # Creativity knob from OLLAMA_TEMPERATURE
    )

    output_parser = StrOutputParser()  # Last step — chain output becomes a str

    # LCEL composition: template → model → parser
    chain = prompt | llm | output_parser  # Pipe declares left-to-right order

    return chain  # Caller can invoke without rebuilding the pipeline


def is_response_valid(response: str, max_words: int = 120) -> tuple[bool, list[str]]:
    # Simple success criteria — string, non-empty, not too long
    errors = []  # Collect every failed check here

    if not isinstance(response, str):  # Parser should always return str — guard anyway
        errors.append("Response is not a string.")
        return False, errors  # Stop — further string checks are unsafe

    if not response.strip():  # Whitespace-only counts as empty
        errors.append("Response is empty.")

    word_count = len(response.split())  # Rough word count for length check

    if word_count > max_words:  # Model may ignore brevity — catch it here
        errors.append(f"Response is too long: {word_count} words (max {max_words}).")

    return len(errors) == 0, errors  # True only when errors list is empty


def main():  # Run chain and validation when executed directly
    chain = build_chain()  # Build once — reuse for every test input

    # Distinct inputs — proves placeholders drive behaviour, not hard-coded prompts
    test_cases = [
        {
            "topic": "LangChain Expression Language",
            "audience": "first-year students",
            "analogy_domain": "college canteen queue",
        },
        {
            "topic": "Prompt Templates",
            "audience": "non-tech interns",
            "analogy_domain": "wedding invitation cards",
        },
        {
            "topic": "virtual environments",
            "audience": "beginners",
            "analogy_domain": "separate hostel cupboards",
        },
    ]

    passed = 0  # Count how many inputs meet success criteria

    for test_input in test_cases:  # Loop — one invoke per distinct input dict
        result = chain.invoke(test_input)  # Run full LCEL pipeline
        valid, errors = is_response_valid(result)  # Check instructor success criteria

        print("Input:", test_input)  # Show which placeholders were used
        print("Response:", result)  # Plain string thanks to StrOutputParser
        print("Valid:", valid)  # True or False
        print("Errors:", errors)  # Empty list when valid
        print("-" * 40)  # Visual separator between test cases

        if valid:
            passed += 1  # Track pass rate across inputs

    print(f"Passed {passed} of {len(test_cases)} validation checks.")


if __name__ == "__main__":  # Standard Python entry point
    main()  # Only runs when you execute: python hello_chain.py
```

### How the code works

- **`load_dotenv()`** runs **before** reading `OLLAMA_MODEL` — same secure pattern as your Ollama Cloud scripts.
- **`build_chain()`** keeps prompt, model, and parser in one place — other files can import it later.
- **`ChatPromptTemplate.from_messages()`** separates **system** behaviour from the **human** question.
- **`ChatOllama`** reads **model** and **base_url** from `.env` — swap cloud/local by editing `.env`, not Python logic.
- **`prompt | llm | output_parser`** is the LCEL spine you practised **previously**, now with **ChatPromptTemplate**.
- **`is_response_valid()`** implements **instructor success criteria**: type, non-empty, word limit.
- The **loop** proves **consistent structure** across **distinct inputs** — content changes, pipeline stays the same.

**Run:**

```bash
python hello_chain.py
```

**Expected:** Three blocks of output — each with input dict, readable text (not `<AIMessage ...>`), validation result, and a final pass count.

---

## Understanding Output Quality

Small local models sometimes produce weak or unclear analogies even when the **chain is wired correctly**. That is normal in classroom demos.

- The **code worked** — venv, packages, `.env`, LCEL pipe, and parser all ran.
- The **chain was composed correctly** — placeholders filled, model responded, parser returned a string.
- **Answer quality** depends on which Ollama model you use — like comparing a basic calculator with a scientific one.

If validation passes but wording feels weak, try a larger local model or cloud mode later. The LangChain structure stays almost the same.

---

## Validating Output Before Showing Users

LLM answers should not always go straight to the user interface.

- **Official Definition:** **Output validation** checks whether generated text follows expected rules before use.
- **In Simple Words:** A teacher reviews answer sheets before declaring final marks.
- **Real-Life Example:** A hostel warden checks the mess complaint summary before posting it on the notice board.

Models can return **empty** text, ignore word limits, or produce unclear analogies — especially **small local models**. Validation catches **structural** failures even when wording is weak.

![LLM output validation gate — model response is checked for string type, non-empty content, and word limit before showing it to a user or retrying](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260113/module3/session36/session36-03-output-validation-gate.png)

### Instructor success criteria for this chain

| Check | Rule | Why it matters |
| --- | --- | --- |
| Type | Must be **`str`** | UI and logs expect text, not objects |
| Non-empty | **`strip()`** must leave content | Empty replies break the user experience |
| Length | Under **120 words** (adjustable) | Catches runaway outputs in demos |
| Consistency | Same pipeline, different inputs | Proves placeholders work — not one hard-coded answer |

- **Common doubt:** *"Validation passed but the analogy is weak"* — small models do that. The **chain** can be correct while **quality** needs a bigger model or cloud mode later.
- **One input passing** does not prove the chain always works — always test **at least two** distinct `invoke` dicts.

Tracking how many responses pass validation is the first step toward **observability** — knowing what your chain does in the background before users see it.

![Observability and bounded regeneration loop — prompt, LLM, validation, retry with feedback up to max retries, plus dashboard metrics for pass rate and failures](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260113/module3/session36/session36-04-observability-retry-loop.png)

> **[ Student Activity ]**
>
> **Chain Experiment**
>
> Run `hello_chain.py` with the default test cases. Then add a fourth input: topic `"REST APIs"`, audience `"school students"`, analogy_domain `"cricket scoreboard"`. Note whether validation passes and whether the analogy quality changes. Change only **`OLLAMA_TEMPERATURE`** in `.env` from `0.3` to `0.9`, run again, and compare strictness vs creativity.

---

## Troubleshooting — Debug Order

When `python hello_chain.py` fails, check in this order:

1. **venv active?** — Prompt shows `(venv)`; `which python` points inside `venv/`.
2. **Packages installed?** — `pip show langchain-ollama` inside the venv.
3. **Ollama running?** — `ollama list` works; no `connection refused` on **11434**.
4. **Model tag matches?** — `OLLAMA_MODEL` in `.env` equals a name from `ollama list`.
5. **`.env` loaded?** — `load_dotenv()` before `os.environ.get(...)`.
6. **Placeholder keys match?** — `invoke` dict keys must equal `{topic}`, `{audience}`, `{analogy_domain}`.
7. **Parser present?** — Without **StrOutputParser**, validation may see the wrong type.

| Error | Likely fix |
| --- | --- |
| `ModuleNotFoundError: langchain_ollama` | Activate venv; `pip install langchain-ollama` |
| `Connection refused` | Start Ollama app or service |
| `model not found` | `ollama pull <tag>`; fix `OLLAMA_MODEL` |
| Missing variable in prompt | Fix key names in `invoke({...})` dict |

### Common doubts

- **"Do I need an API key for local Ollama?"** — Usually no on `localhost`; cloud mode uses **`OLLAMA_API_KEY`** in `.env` as you practised earlier.
- **"Why is my answer weak?"** — Small models produce unclear analogies; the chain can still be correct.
- **"Why `from_messages()`?"** — Use it for system + human role lists; use **`from_template()`** for one plain string.

---

## Key Takeaways

- A **venv** plus a clear **folder layout** (**.env`**, **`.gitignore`**, **`hello_chain.py`**) keeps LangChain work reproducible for the whole cohort.
- **ChatOllama** binds LangChain to Ollama using **model** and **base_url** from your **Ollama setup block** in `.env` — not scattered hard-coded strings.
- **`ChatPromptTemplate | ChatOllama | StrOutputParser`** is the first production-style LCEL spine for this module worktree.
- **`StrOutputParser`** ensures **`invoke`** returns a **plain string** — essential before wiring a UI or API response.
- **Validation across distinct inputs** proves the chain behaves consistently; weak wording from a small model is a separate issue from a broken pipeline.

In upcoming work you will extend this same chain with **memory**, **retrieval**, **tools**, and **agent** behaviour — the **`|`** pipe grows; you do not start from scratch.

---

## Quick Reference — Important Commands, Libraries, and Terminologies

| Term / command | Meaning |
| --- | --- |
| **`venv`** | Isolated Python environment for one project |
| `python3 -m venv venv` | Create virtual environment |
| `source venv/bin/activate` | Activate venv (macOS/Linux) |
| `pip install langchain-core langchain-ollama python-dotenv` | Minimal package stack |
| **`.env`** | Local secrets and settings — not committed |
| **`.env.example`** | Committed template with placeholders |
| **`load_dotenv()`** | Load `.env` into `os.environ` |
| **`OLLAMA_MODEL`** | Model tag matching `ollama list` |
| **`OLLAMA_HOST`** | Ollama server URL (usually `http://localhost:11434`) |
| **ChatOllama** | LangChain Runnable for Ollama chat models |
| **ChatPromptTemplate** | Reusable system/human message template |
| **`from_messages()`** | Build prompt from role tuples |
| **LCEL** | Chain syntax using `\|` between Runnables |
| **StrOutputParser** | Returns plain string from model response |
| **`chain.invoke({...})`** | Run chain once with placeholder values |
| **`hello_chain.py`** | End-to-end proof script for the module worktree |
| `ollama list` | Confirm model tag before running chain |
| `python hello_chain.py` | Run and validate the first LCEL chain |
| **`num_predict`** | Approximate Ollama output token limit |
| **Observability** | Tracking pass/fail patterns over many chain runs |
