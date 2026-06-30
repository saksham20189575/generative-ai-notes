# lecture27.py — LangChain env setup + first real LCEL chain with validation (Session 27)
#
# In Session 26 you met LangChain: PromptTemplate -> ChatOllama -> StrOutputParser, all
# with HARD-CODED settings inside the Python file. That proves the pattern, but it is not
# how a team ships a project. The model name, host, and temperature were baked into code,
# the prompt was ONE plain string, and nothing checked whether the answer was usable.
#
# Today you move from a concept demo to a REAL PROJECT layout. Three things change:
#   1) CONFIGURATION moves out of code and into .env (model, host, temperature) — swap
#      local/cloud or a model tag by editing .env, never the Python.
#   2) The prompt becomes a CHAT prompt with ROLES: a system message (how to behave) and
#      a human message (the actual ask) — ChatPromptTemplate.from_messages, not from_template.
#   3) You VALIDATE the output (type, non-empty, length) and run the SAME chain over many
#      DISTINCT inputs — proving the pipeline is consistent, not a one-off lucky answer.
#
# Big idea this session: the LCEL spine you already know stays the same —
#
#       ChatPromptTemplate  ->  ChatOllama  ->  StrOutputParser
#
# — but the settings come from .env and a validation gate sits AFTER the chain. That is
# the difference between "it ran once on my laptop" and "it reproduces for the whole cohort."
#
# What this file demonstrates (one script, four escalating stages):
#   STAGE 1 — LOAD CONFIG from .env and build a ChatOllama bound to those values
#   STAGE 2 — CHATPROMPTTEMPLATE: system + human messages with {placeholders}
#   STAGE 3 — LCEL CHAIN: prompt | llm | parser — same pipe, now with a chat prompt
#   STAGE 4 — VALIDATE the output across several distinct inputs and report a pass count
#
# PREREQUISITES (do these in the terminal BEFORE running this file):
#   python3 -m venv venv && source venv/bin/activate     # (Windows: venv\Scripts\activate)
#   pip install -U pip langchain-core langchain-ollama python-dotenv
#   ollama pull qwen2.5:0.5b          # the same light local model from Sessions 25-26
# Create a .env next to this file (do NOT commit it) with:
#   OLLAMA_MODEL=qwen2.5:0.5b
#   OLLAMA_HOST=http://localhost:11434
#   OLLAMA_TEMPERATURE=0.3
# The Ollama app/service must be RUNNING (localhost:11434) or you get "connection refused".

# Standard library — read configuration from the environment after .env is loaded.
import os  # os.environ.get(...) pulls values that load_dotenv() placed there

# python-dotenv — bridges a .env file on disk into os.environ at runtime.
from dotenv import load_dotenv  # Reads key=value pairs from .env so secrets stay out of code

# LangChain Core — stable building blocks: the chat prompt template and the string parser.
from langchain_core.prompts import ChatPromptTemplate  # Role-based messages with {slots}
from langchain_core.output_parsers import StrOutputParser  # Returns plain text, not a message

# Provider package — the LangChain wrapper that makes Ollama look like a Runnable.
from langchain_ollama import ChatOllama  # ChatOllama is a Runnable bound to your Ollama server

# ---------------------------------------------------------------------------
# STAGE 1 — CONFIGURATION FROM .env (read once, reuse everywhere)
# ---------------------------------------------------------------------------
# load_dotenv() MUST run BEFORE any os.environ.get(...) below, or the values are missing
# and the defaults silently take over. This is the same secure pattern you used for the
# Ollama Cloud key in Session 25 — settings live in .env, never in the .py file.
load_dotenv()  # Make OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_TEMPERATURE available via os.environ

# Each get() has a DEFAULT second argument so the script still runs if a key is missing.
# The model tag MUST match a name from "ollama list" — tiny models (0.5B-2B) suit laptops.
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")  # Same tag as ollama list
BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")  # Where Ollama listens
# Temperature arrives as a STRING from .env, so float() converts it before ChatOllama uses it.
TEMPERATURE = float(os.environ.get("OLLAMA_TEMPERATURE", "0.3"))  # Lower = more stable demos


# ===========================================================================
# STAGE 2 + STAGE 3 — BUILD THE CHAIN: chat prompt -> model -> parser
# ===========================================================================
def build_chain():
    """Assemble the LCEL chain once and return it so callers invoke without rebuilding.

    This is the heart of the session. Two pieces are new versus Session 26:
      - ChatPromptTemplate.from_messages: a LIST of (role, text) tuples, not one string.
        Chat models behave better when "how to act" (system) is separated from "what to
        answer" (human). from_template() would be wrong here — that is for a single string.
      - Every setting on ChatOllama comes from the .env block above, so changing the model
        or host is a .env edit, not a code change.
    """
    # STAGE 2 — the chat prompt. {placeholders} are filled at invoke() time, not now.
    prompt = ChatPromptTemplate.from_messages([  # from_messages because we have role tuples
        ("system", (  # System message sets BEHAVIOUR — tone, role, format rules
            "You are a beginner-friendly programming instructor. "
            "Explain concepts in simple language with short bullet points. "
            "Avoid long introductions."
        )),
        ("human", (  # Human message carries the actual request, with runtime variables
            "Explain {topic} to {audience} using one analogy from {analogy_domain}."
        )),
    ])

    # The model step — a Runnable configured entirely from .env (see STAGE 1).
    llm = ChatOllama(
        model=MODEL_NAME,  # Tag from OLLAMA_MODEL — must match "ollama list"
        base_url=BASE_URL,  # Host from OLLAMA_HOST — usually localhost:11434
        temperature=TEMPERATURE,  # Creativity knob from OLLAMA_TEMPERATURE
    )

    output_parser = StrOutputParser()  # Last step: strip metadata so the result is a str

    # STAGE 3 — LCEL composition. The pipe `|` declares ORDER: each piece's output feeds
    # the next. Same spine as Session 26, now starting from a role-based chat prompt.
    chain = prompt | llm | output_parser  # ChatPromptTemplate -> ChatOllama -> plain string

    return chain  # Reusable — main() invokes it many times without rebuilding


# ===========================================================================
# STAGE 4a — THE VALIDATION GATE: is this answer actually usable?
# ===========================================================================
def is_response_valid(response: str, max_words: int = 120) -> tuple:
    """Check the model output against simple success criteria; return (ok, list_of_errors).

    A correctly wired chain can still return text you would NOT show a user — empty replies
    or runaway length, especially from a tiny local model. This gate catches STRUCTURAL
    failures before the answer reaches a UI or log. It does not judge wording quality;
    weak analogies from a small model are a separate concern from a broken pipeline.
    """
    errors = []  # Collect every failed check so the caller sees all problems at once

    if not isinstance(response, str):  # StrOutputParser should guarantee str — verify anyway
        errors.append("Response is not a string.")
        return False, errors  # Stop early: the string checks below would be unsafe

    if not response.strip():  # Whitespace-only is effectively empty
        errors.append("Response is empty.")

    word_count = len(response.split())  # Rough word count for the length check
    if word_count > max_words:  # Small models often ignore brevity — flag it here
        errors.append(f"Response is too long: {word_count} words (max {max_words}).")

    return len(errors) == 0, errors  # ok is True only when no checks failed


# ===========================================================================
# STAGE 4b — DRIVE THE CHAIN over distinct inputs and report a pass count
# ===========================================================================
def main() -> None:
    chain = build_chain()  # Build the pipeline ONCE, reuse for every test input

    # Distinct inputs prove the placeholders DRIVE the answer — it is not one hard-coded
    # reply. Each dict's keys MUST match the {placeholders} in the prompt exactly.
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

    passed = 0  # Count how many inputs meet the success criteria — first taste of observability

    for test_input in test_cases:  # One invoke per distinct input dict
        result = chain.invoke(test_input)  # Run the full LCEL pipeline; result is a str
        valid, errors = is_response_valid(result)  # Apply the validation gate

        print("=" * 72)
        print("Input    :", test_input)  # Which placeholder values were used
        print("Response :", result)  # Plain string thanks to StrOutputParser
        print("Valid    :", valid)  # True only when every check passed
        print("Errors   :", errors)  # Empty list when valid

        if valid:
            passed += 1  # Track the pass rate across all inputs

    print("=" * 72)
    print(f"Passed {passed} of {len(test_cases)} validation checks.")

    # Try it: add a fourth input (topic "REST APIs", audience "school students",
    # analogy_domain "cricket scoreboard") and re-run. Then change ONLY OLLAMA_TEMPERATURE
    # in .env from 0.3 to 0.9 and compare strictness vs creativity — the Python never changes.
    print("\nEdit .env (model, host, temperature) and re-run — the chain code stays the same.")


if __name__ == "__main__":
    main()  # Load .env, build the chain, run every input through it, and validate each answer
