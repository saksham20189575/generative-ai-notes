# lecture25.py — Ollama: Local LLMs + Ollama Cloud, one script two modes (Session 25)
#
# This session opens Module 3 and adds a LOCAL path to everything you have built.
# Through Module 2 every LLM call went to a CLOUD API (Groq) you do not host: in
# Session 24 the model chose tools, your runtime executed them, and Groq wrote the
# grounded reply — but inference always happened on someone else's servers.
#
# Today you run a model ON YOUR LAPTOP with Ollama, call it from Python, and then
# compare it against Ollama Cloud on the SAME prompt — switching backends by editing
# a single value in .env, never the Python.
#
# Big idea this session: an LLM is just SOFTWARE + WEIGHTS. Ollama downloads the
# weights ("ollama pull"), runs them, and serves a LOCAL HTTP API at
# http://localhost:11434 so Python talks to it exactly like a cloud API. A tiny
# local model is fast and private but weaker at reasoning; a bigger cloud model is
# stronger but sends your text off-device. Good engineering is choosing deliberately.
#
# What this file demonstrates (the dual-mode capstone):
#   STAGE 1 — chat with a LOCAL model on localhost:11434 (no API key, no network)
#   STAGE 2 — chat with OLLAMA CLOUD using a Bearer-token Client and a bigger model
#   STAGE 3 — select local vs cloud from USE_CLOUD in .env — the prompt stays identical
#   STAGE 4 — drive one reasoning prompt so you can compare speed, reasoning, privacy
#
# PREREQUISITES (do these in the terminal BEFORE running this file):
#   pip install ollama python-dotenv
#   ollama pull qwen2.5:0.5b          # download the light local model
#   ollama run  qwen2.5:0.5b          # confirm CLI chat works, then /bye to exit
# The Ollama app/service must be RUNNING for the local branch to connect.

import os  # Read USE_CLOUD and OLLAMA_API_KEY from the environment after loading .env
import sys  # Exit cleanly on unrecoverable setup errors (e.g. cloud mode with no key)

from dotenv import load_dotenv  # Load key=value pairs from .env into os.environ
from ollama import Client, chat  # chat() talks to localhost; Client() targets a custom host

# ---------------------------------------------------------------------------
# Configuration — one place to change models, host, and the comparison prompt
# ---------------------------------------------------------------------------
# Local tag MUST match a model shown by "ollama list" on this machine. Tiny models
# (0.5B-2B) are the right choice for student laptops — avoid 70b+ tags that need
# tens of GB of RAM and will freeze most machines.
LOCAL_MODEL = "qwen2.5:0.5b"  # ~0.5B params — fastest laptop-friendly smoke test
# Cloud model name — verify the exact tag on ollama.com/library before relying on it.
CLOUD_MODEL = "gpt-oss:120b"  # Much larger; runs on Ollama's servers, not your laptop
CLOUD_HOST = "https://ollama.com"  # Ollama Cloud host (local default is localhost:11434)

# Same prompt for BOTH modes — only the BACKEND changes, so the comparison is fair.
# A multi-step word problem is deliberately chosen: it exposes where a tiny local
# model skips steps or invents numbers versus a larger cloud model.
COMPARISON_PROMPT = (
    "A train leaves Delhi at 9:00 AM at 60 km/h. Another leaves Mumbai at 10:00 AM "
    "at 80 km/h toward Delhi. The cities are 1400 km apart. When do they meet? "
    "Show reasoning step by step, then give the final time."
)


# ===========================================================================
# STAGE 1 — LOCAL CHAT: talk to the model running on THIS computer
# ===========================================================================
def ask_local(question: str) -> str:
    """Chat with Ollama on localhost:11434 — no API key, no third party sees the text.

    The default chat() helper wraps the local HTTP API, so there is no raw requests
    code. The messages list uses the SAME role + content shape as Groq — only the
    transport differs. Requires the model to be pulled and the Ollama service running.
    """
    response = chat(
        model=LOCAL_MODEL,  # Small model loaded from disk into RAM on first call
        messages=[  # List of chat turns — identical shape to the Groq labs
            {"role": "user", "content": question},  # A single human turn
        ],
    )
    # The reply is a dict; the assistant text lives at message -> content.
    return response["message"]["content"]


# ===========================================================================
# STAGE 2 — CLOUD CHAT: borrow a bigger model when the laptop is too small
# ===========================================================================
def ask_cloud(question: str) -> str:
    """Chat with Ollama Cloud using an API key — same messages shape, different host + auth.

    Cloud runs a larger model than a student laptop can hold. We authenticate with a
    Bearer token in the request header. The key is read from .env so it never lives
    in code or Git. Same "messages" format as the local branch — that is the point.
    """
    api_key = os.environ.get("OLLAMA_API_KEY")  # Secret loaded from .env by load_dotenv()
    if not api_key:  # Fail loudly instead of sending a broken, unauthenticated request
        raise ValueError("Cloud mode needs OLLAMA_API_KEY in your .env file.")

    cloud_client = Client(  # Unlike chat(), Client lets us point at a custom host + headers
        host=CLOUD_HOST,  # Remote Ollama host instead of localhost
        headers={"Authorization": "Bearer " + api_key},  # Prove identity to Ollama Cloud
    )
    response = cloud_client.chat(
        model=CLOUD_MODEL,  # Larger cloud model name (verify on ollama.com)
        messages=[{"role": "user", "content": question}],  # Same message shape as local
    )
    return response["message"]["content"]  # Assistant reply text


# ===========================================================================
# STAGE 3 — SELECT THE BACKEND from .env — flip modes WITHOUT editing Python
# ===========================================================================
def answer_question(question: str, use_cloud: str) -> tuple:
    """Route to local or cloud based on USE_CLOUD and return (mode_label, model, answer).

    USE_CLOUD is read as a STRING from .env: "1" means cloud, anything else (default
    "0") means local. Keeping the switch in .env means the same script reproduces on
    every student's machine — they change one line, not the code.
    """
    if use_cloud == "1":  # Cloud branch — bigger model, sent to Ollama's servers
        return "CLOUD", CLOUD_MODEL, ask_cloud(question)
    # Local branch (default) — runs on this laptop, private and free
    return "LOCAL", LOCAL_MODEL, ask_local(question)


# ===========================================================================
# STAGE 4 — DRIVE THE COMPARISON: same prompt, one backend per run
# ===========================================================================
def main() -> None:
    load_dotenv()  # Read .env BEFORE any API call so USE_CLOUD and the key are available

    # "0" = local laptop (default), "1" = Ollama Cloud — set this in .env, not in code.
    use_cloud = os.environ.get("USE_CLOUD", "0")

    try:
        mode_label, model_label, answer = answer_question(COMPARISON_PROMPT, use_cloud)
    except ValueError as error:  # Missing cloud key — explain instead of crashing cryptically
        print("Setup error:", error)
        sys.exit(1)

    print("=" * 72)
    print("Mode :", mode_label)  # LOCAL or CLOUD — which path actually ran
    print("Model:", model_label)  # The exact model tag used
    print("=" * 72)
    print("Question:", COMPARISON_PROMPT)
    print("\nAnswer:")
    print(answer)  # The generated reasoning + final time

    # Run this file once with USE_CLOUD=0, then again with USE_CLOUD=1, and compare:
    #   - Did it show its steps?      - Is the final time plausible?
    #   - Any invented facts?         - Which would you trust for homework vs a demo?
    print("\nFlip USE_CLOUD in .env (0=local, 1=cloud) and re-run to compare the same prompt.")


if __name__ == "__main__":
    main()  # Load .env, pick the backend, send the shared prompt, and print the answer
