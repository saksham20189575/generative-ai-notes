# main.py — DEBUGGING & ITERATING AN AGENT: label the failure, then patch ONE layer (Session 34)
#
# In Session 33 your evaluation harness told you WHAT broke. This session is about FIXING it — not by
# guessing, not by rewriting everything, and not by shouting "the model is bad." You label the
# failure, pick the matching patch, change ONE knob, and re-run the SAME cases to prove it helped.
#
# The three controlled fixes (remediation levers):
#   PROMPT PATCH    -> edit the instructions (e.g. stricter refusal)
#   TOOL PATCH      -> fix a tool's name / description / arguments
#   RETRIEVAL TUNE  -> change how docs are split & searched (chunk_size, overlap, k)
#
# This file demonstrates the headline RETRIEVAL TUNE from the lecture with NO API key required. A tiny
# keyword search STANDS IN for a real vector store (same trick as Session 33), so you can run it and
# watch the SAME query fail then pass when only the chunking changes:
#
#   Query: "What is the return window for electronics items?"
#     chunk_size=40  -> "electronics" and "seven days" land in DIFFERENT chunks -> "I don't know"
#     chunk_size=160 -> one chunk holds BOTH -> the correct, grounded answer
#   Same document, same query, same code. Only the INGEST setting changed. That is WEAK RETRIEVAL
#   caused by bad chunking — a retrieval-tune bug, not a bad LLM.
#
# Run it (no key, no install beyond Python):  python3 main.py

import re  # split text into words for the keyword search


# ===========================================================================
# THE MINI RAG — ingest (chunk) -> retrieve (keyword) -> answer only if grounded
# ===========================================================================
# A real RAG embeds chunks into a vector store and asks an LLM to answer from the retrieved context.
# Here we keep the SHAPE but drop the machinery: chunk the text, retrieve by word overlap, and
# "answer" only if the needed fact is actually in the retrieved context. If it is not, we refuse
# honestly ("I don't know based on the provided documents") instead of hallucinating.

# One source document (stands in for return_policy.md). Notice each rule pairs a CATEGORY word with
# a NUMBER — chunking decides whether they stay together.
RETURN_POLICY = (
    "Return Policy. "
    "Electronics items can be returned to the store within seven days of the delivery date. "
    "Clothing items can be returned within thirty days of the delivery date. "
    "Grocery and food items cannot be returned once delivered."
)


def chunk_text(text, chunk_size, overlap):
    """Split text into overlapping chunks of chunk_size characters (a tiny text splitter)."""
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])  # take chunk_size characters
        start += chunk_size - overlap                  # step forward, leaving an overlap margin
    return chunks


def words(text):
    """Lowercase word set, used to score keyword overlap."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve(query, chunks, k):
    """Return the top-k chunks that share the most words with the query (weak stand-in for a vector search)."""
    query_words = words(query)
    scored = [(len(query_words & words(chunk)), chunk) for chunk in chunks]
    scored.sort(key=lambda pair: pair[0], reverse=True)  # best overlap first
    return [chunk for score, chunk in scored[:k] if score > 0]


def answer(query, context, answer_phrase):
    """Simulate a GROUNDED LLM: answer only if the fact is in the retrieved context, else refuse honestly."""
    if answer_phrase in context.lower():
        return f"Yes — {answer_phrase} (grounded in retrieved context)."
    return "I don't know based on the provided documents."  # honest refusal beats a confident guess


# ===========================================================================
# ONE RAG RUN — ingest with given settings, retrieve, and answer the same query
# ===========================================================================
# Everything below the ingest settings is IDENTICAL across runs. That is the whole point: when the
# answer changes, you know the RETRIEVAL (chunking) changed it — not the query and not the "LLM".

def run_rag(query, answer_phrase, chunk_size, overlap, k=2):
    """Do one full retrieve-then-answer pass and print what happened (the trajectory)."""
    chunks = chunk_text(RETURN_POLICY, chunk_size, overlap)
    hits = retrieve(query, chunks, k)
    context = " ".join(hits)
    reply = answer(query, context, answer_phrase)

    print(f"\n--- ingest: chunk_size={chunk_size}, overlap={overlap}, k={k} ---")
    print(f"Chunks produced : {len(chunks)}")
    print(f"Retrieved chunks: {hits}")
    print(f"Context tokens  : ~{len(context.split())} words")  # bigger context = more tokens = more cost
    print(f"Q: {query}")
    print(f"A: {reply}")
    return reply.startswith("Yes")  # True == the case passed (grounded answer given)


# ===========================================================================
# DEMO 1 — RETRIEVAL TUNE: the same query fails, then passes
# ===========================================================================
def demo_chunk_tuning():
    """Show weak retrieval from bad chunking, then fix it by tuning ONE knob (chunk_size)."""
    print("=" * 70)
    print("DEMO 1 — RETRIEVAL TUNE (same query, only chunk_size changes)")
    print("=" * 70)
    query = "What is the return window for electronics items?"

    # BEFORE: tiny chunks split "electronics" away from "seven days" -> weak retrieval -> I don't know.
    run_rag(query, "seven days", chunk_size=40, overlap=10)

    # AFTER: bigger chunks keep the category and the rule together -> correct grounded answer.
    run_rag(query, "seven days", chunk_size=160, overlap=30)

    print("\nSame files, same app code — only INGEST parameters changed. That is a retrieval-tune fix,")
    print("not a bad LLM. Failure class: WEAK RETRIEVAL caused by bad chunking.")


# ===========================================================================
# DEMO 2 — MEASURE THE FIX: re-run the SAME eval set before vs after
# ===========================================================================
# A fix is only real if the numbers move. Run the identical cases under the "before" and "after"
# settings and compare pass counts — the same before/after discipline as the Session 33 harness.
EVAL_CASES = [
    {"query": "What is the return window for electronics items?", "answer_phrase": "seven days"},
    {"query": "What is the return window for clothing items?",    "answer_phrase": "thirty days"},
]


def score_settings(label, chunk_size, overlap):
    """Run every eval case under one ingest setting and return how many passed."""
    print(f"\n### {label}: chunk_size={chunk_size}, overlap={overlap}")
    passed = 0
    for case in EVAL_CASES:
        ok = run_rag(case["query"], case["answer_phrase"], chunk_size, overlap)
        passed += 1 if ok else 0
    print(f">>> {label} score: {passed}/{len(EVAL_CASES)} passed")
    return passed


def demo_before_after():
    """Prove the retrieval tune helped by comparing pass counts on the same cases."""
    print("\n" + "=" * 70)
    print("DEMO 2 — MEASURE THE FIX (same cases, before vs after)")
    print("=" * 70)
    before = score_settings("BEFORE (tiny chunks)", chunk_size=40, overlap=10)
    after = score_settings("AFTER (bigger chunks)", chunk_size=160, overlap=30)
    print(f"\nResult: {before}/{len(EVAL_CASES)} -> {after}/{len(EVAL_CASES)} after tuning ONE knob.")
    print("Rule of thumb: change ONE thing, re-run the WHOLE set, then decide (guard against regressions).")


# ===========================================================================
# DRIVER
# ===========================================================================
def main():
    demo_chunk_tuning()   # retrieval tune: same query fails then passes
    demo_before_after()   # measure it: pass count moves on the same eval set

    # Try it:
    #   1) Push chunk_size up to 400 — the answer stays correct, but "Context tokens" grows. That is the
    #      COST-LATENCY TRADE-OFF: more context can mean more tokens (a bigger bill) for no extra quality.
    #   2) Raise k from 2 to 4 in run_rag and watch the context (tokens) grow — tune ONE knob at a time.
    #   3) Add a case with an answer_phrase that is NOT in the document — a good agent should refuse
    #      honestly ("I don't know"), never invent a policy (that would be a HALLUCINATION failure).
    print("\nDebug loop: LABEL the failure -> patch ONE layer (prompt / tool / retrieval) -> re-run -> compare.")


if __name__ == "__main__":
    main()
