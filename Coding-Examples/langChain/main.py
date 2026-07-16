# lecture26.py — Intro to LangChain: from a raw Ollama call to a first LCEL chain (Session 26)
#
# In Session 25 you solved WHERE the brain lives: you ran a model locally with Ollama,
# called it from Python, and compared local vs Ollama Cloud on the same prompt. That
# gives you a reliable model call. But a single chat() call is not an application.
#
# Today you learn HOW to wire that brain into a real product without the project falling
# apart. Raw Ollama calls work for one script; they break the moment you add reusable
# prompts, parsing, memory, RAG, and tools. LangChain is the MIDDLE FLOOR between the
# model provider (Ollama) and your application — a common language for prompts, chains,
# parsers, memory, and retrievers.
#
# Big idea this session: an LLM app is built from RUNNABLES — small reusable bricks that
# snap together. A "chain" is runnables linked so the OUTPUT of one step becomes the INPUT
# of the next. Today's spine is the simplest useful chain there is:
#
#       PromptTemplate  ->  ChatOllama  ->  StrOutputParser
#
# What this file demonstrates (one script, three escalating stages):
#   STAGE 1 — RAW Ollama call: the baseline you already know (no LangChain)
#   STAGE 2 — PromptTemplate + ChatOllama: a reusable prompt, but you still read .content
#   STAGE 3 — First LCEL chain: prompt | llm | parser — order declared with the pipe |
#   STAGE 4 — Drive all three on the SAME task so you see what the structure buys you
#
# PREREQUISITES (do these in the terminal BEFORE running this file):
#   python3 -m venv venv && source venv/bin/activate     # (Windows: venv\Scripts\activate)
#   pip install ollama langchain-core langchain-ollama
#   ollama pull qwen2.5:0.5b          # the same light local model from Session 25
# The Ollama app/service must be RUNNING (localhost:11434) or you get "connection refused".

# Raw Ollama helper — the same baseline transport you used in Session 25 (no LangChain).
from ollama import chat  # Sends JSON to localhost:11434 and returns a response dict

# LangChain Core — stable building blocks: templates, parsers, the Runnable/LCEL base.
from langchain_core.prompts import PromptTemplate  # Reusable prompt with {placeholders}
from langchain_core.output_parsers import StrOutputParser  # Returns plain text, not an object

# Provider package — the LangChain wrapper that makes Ollama look like a Runnable.
from langchain_ollama import ChatOllama  # ChatOllama is a Runnable bound to your Ollama server

# ---------------------------------------------------------------------------
# Configuration — one place to change the model and the teaching prompt
# ---------------------------------------------------------------------------
# Local tag MUST match a model shown by "ollama list". Tiny models (0.5B-2B) are the
# right choice for student laptops — avoid 70b+ tags that freeze most machines.
LOCAL_MODEL = "qwen2.5:0.5b"  # Same light model as Session 25 — fast on a laptop
OLLAMA_HOST = "http://localhost:11434"  # Default local Ollama address

# Build the ChatOllama runnable ONCE and reuse it across the templated and chain stages.
# temperature low = more focused, repeatable answers — better for a classroom demo.
llm = ChatOllama(
    model=LOCAL_MODEL,  # Same tag as the raw call below, just LangChain-shaped
    base_url=OLLAMA_HOST,  # Where Ollama listens; matches the raw chat() transport
    temperature=0.3,  # Slightly deterministic so reruns look similar in class
)

# A reusable PROMPT BLUEPRINT. Instead of scattering f-strings across files, define the
# {slots} once. Same skeleton serves many topics — only the runtime variables change.
prompt = PromptTemplate.from_template(
    """Explain {topic} to {audience} with these requirements:
- Use {tone} tone
- Give one real-life analogy
- Keep the answer within {limit} words"""
)

# The variables we will feed the template this run. In production these come from a web
# form or your API; the template body never changes when you swap these values.
TEMPLATE_VARS = {
    "topic": "REST APIs",  # Subject of the explanation
    "audience": "beginners",  # Who the answer is written for
    "tone": "simple",  # Writing style
    "limit": "150",  # Word cap — a STRING, because it is substituted as text
}


# ===========================================================================
# STAGE 1 — RAW OLLAMA: the baseline, exactly like Session 25 (no LangChain)
# ===========================================================================
def ask_raw(question: str) -> str:
    """Call Ollama directly: hand-built prompt string, manual dict digging for the text.

    This is the "just call the LLM" approach. It is fine for ONE static prompt, but the
    prompt is hard-coded and you must reach into response["message"]["content"] yourself.
    Add a second prompt, a second format, or a parser and this style starts to sprawl.
    """
    response = chat(
        model=LOCAL_MODEL,  # Must match a tag from "ollama list"
        messages=[{"role": "user", "content": question}],  # One human turn — Ollama's shape
    )
    # The reply is a dict; the assistant text lives at message -> content (manual extraction).
    return response["message"]["content"]


# ===========================================================================
# STAGE 2 — TEMPLATE + MODEL: reusable prompt, but still reading .content by hand
# ===========================================================================
def ask_with_template(variables: dict) -> str:
    """Fill the PromptTemplate, then invoke ChatOllama — still no pipe, no parser yet.

    PromptTemplate.format() turns the blueprint + variables into ONE final string. The
    model is now a LangChain Runnable (ChatOllama), so we call .invoke(). But invoke()
    returns a MESSAGE OBJECT, so we still manually read .content — that is the gap Stage 3
    closes with a parser.
    """
    final_prompt = prompt.format(**variables)  # Blueprint + values -> finished prompt string
    response = llm.invoke(final_prompt)  # Runnable call; returns a message object, not str
    return response.content  # .content holds the assistant text — extracted manually


# ===========================================================================
# STAGE 3 — FIRST LCEL CHAIN: prompt | llm | parser — the capstone pattern
# ===========================================================================
def ask_with_chain(variables: dict) -> str:
    """Compose three Runnables with the pipe operator so output flows A -> B -> C.

    LCEL (LangChain Expression Language): the `|` declares ORDER. The template formats the
    input dict, ChatOllama generates, and StrOutputParser strips metadata so the result is
    already a plain Python string. You do NOT write "step 1 then step 2" — the pipe does it.
    Adding a fourth step later (logging, a retriever, a tool) means extending the pipe,
    not rewriting three scripts.
    """
    output_parser = StrOutputParser()  # Last step: return clean text, not a message object

    # The whole app on one line. Each piece is a Runnable; `|` wires output into input.
    chain = prompt | llm | output_parser  # PromptTemplate -> ChatOllama -> plain string

    # invoke() passes a DICT — keys MUST match the template placeholders exactly, or it errors.
    return chain.invoke(variables)  # Already a string because StrOutputParser is last


# ===========================================================================
# STAGE 4 — DRIVE ALL THREE on the same task and compare the developer experience
# ===========================================================================
def main() -> None:
    # Build the single hard-coded question Stage 1 uses, so all three answer the same task.
    raw_question = (
        "Explain REST APIs to beginners with these requirements: "
        "use a simple tone, give one real-life analogy, keep it within 150 words."
    )

    print("=" * 72)
    print("STAGE 1 — RAW OLLAMA (no LangChain): hard-coded prompt, manual .content")
    print("=" * 72)
    print(ask_raw(raw_question))

    print("\n" + "=" * 72)
    print("STAGE 2 — PROMPTTEMPLATE + CHATOLLAMA: reusable prompt, still manual .content")
    print("=" * 72)
    print(ask_with_template(TEMPLATE_VARS))

    print("\n" + "=" * 72)
    print("STAGE 3 — FIRST LCEL CHAIN: prompt | llm | StrOutputParser -> plain string")
    print("=" * 72)
    print(ask_with_chain(TEMPLATE_VARS))

    # All three printed similar answers today — that is expected for ONE static prompt.
    # The chain earns its keep when you add a fourth step or a new topic:
    #   - Stage 1: you would copy-paste and re-edit the whole prompt string.
    #   - Stage 3: change only TEMPLATE_VARS, or extend the pipe with one more Runnable.
    print("\n" + "-" * 72)
    print("Try it: change topic to 'vector databases' and limit to '400' in TEMPLATE_VARS,")
    print("then re-run. The template body never changes — that is composability.")


if __name__ == "__main__":
    main()  # Run the raw call, the templated call, and the LCEL chain on the same task
