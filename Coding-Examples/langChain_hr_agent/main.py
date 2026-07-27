# main.py — REAL-WORLD USE CASE: a tiny HR ONBOARDING AGENT you can run today (Session 35)
#
# The lecture notes build the "real" HR agent with LangChain + Chroma + OpenAI. That needs API keys,
# installs, and a running vector store. This file keeps the SAME SHAPE — corpus, retrieval, tools,
# guardrails, escalation, memory, and an evaluation harness — but strips out the machinery so it runs
# with nothing but plain Python:
#
#   python3 main.py        (no pip install, no API key, no internet)
#
# What you will see, exactly like the notes describe:
#   1. A GROUNDED answer   -> "How many casual leaves?"      -> searches HR docs, answers "12"
#   2. A TOOL action       -> "VPN still not working"        -> creates an IT ticket
#   3. A REFUSAL / ESCALATE-> "What is my salary?"           -> refuses + escalates to HR
#   4. MULTI-TURN memory   -> "...can I carry them forward?" -> "them" = casual leaves from turn 1
#   5. An EVALUATION run    -> the same structured test cases from the notes, PASS/FAIL + a summary
#
# The one big simplification: real retrieval embeds text and does a vector search. Here a tiny
# KEYWORD search stands in for it (same trick as Session 34). Everything else — search-first,
# cite-the-source, refuse sensitive topics, escalate unknowns — is the real design.


import re  # split text into words for the keyword "retriever"


# ===========================================================================
# 1) THE CORPUS  (stands in for hr_documents/*.md ingested into a vector store)
# ===========================================================================
# In the notes these are separate .md files loaded and chunked into Chroma. Here each "document" is
# one entry: a source filename + its text. Keyword search over these plays the role of the retriever.

HR_DOCUMENTS = [
    {
        "source": "leave_policy.md",
        "text": (
            "Casual leave: every full-time employee gets 12 casual leaves per calendar year. "
            "Casual leaves cannot be carried forward to the next year. "
            "Sick leave: 10 sick leaves per year. "
            "Earned leave: 15 earned leaves per year, and earned leaves can be carried forward up to 30 days."
        ),
    },
    {
        "source": "it_setup_guide.md",
        "text": (
            "VPN access: download the company VPN client from the internal portal and log in with your "
            "employee id and temporary password. Email setup: your official email is "
            "firstname.lastname@company.com, accessed via Outlook or the webmail portal."
        ),
    },
    {
        "source": "benefits_faq.md",
        "text": (
            "Health insurance covers the employee, spouse, and up to two children. "
            "Provident fund (PF) is deducted monthly and matched by the company."
        ),
    },
    {
        "source": "org_chart.md",
        "text": (
            "The head of the engineering department is Anita Rao. "
            "The head of the human resources department is Vikram Singh."
        ),
    },
]


def words(text):
    """Lowercase set of words — the unit we match on (a very small stand-in for embeddings)."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


# ===========================================================================
# 2) THE TOOLS  (plain functions — no @tool decorator, no LLM needed)
# ===========================================================================
# The notes wrap these with LangChain's @tool decorator so the LLM can call them. The BEHAVIOUR is
# identical; here we just call them directly from simple routing rules below.

# Very common words carry no meaning, so we ignore them when scoring — otherwise a shared "the"
# would make an off-topic question (e.g. a cricket score) look like a match. Real retrievers handle
# this with embeddings; here we just drop a tiny stop-list.
STOP_WORDS = {"the", "a", "an", "do", "i", "my", "me", "is", "of", "to", "how", "can", "get", "about"}


def search_hr_docs(query):
    """Retriever tool: return the single best-matching HR document, or None if nothing is relevant."""
    query_words = words(query) - STOP_WORDS  # keep only the meaningful words
    best_doc = None
    best_score = 0
    for doc in HR_DOCUMENTS:
        score = len(query_words & words(doc["text"]))  # how many meaningful query words are in this doc
        if score > best_score:
            best_score = score
            best_doc = doc
    if best_score < 2:             # need at least 2 real word matches to trust the result
        return None                # too weak -> treat as "nothing relevant found"
    return best_doc


def create_it_ticket(employee_name, issue):
    """Action tool: log an IT request and return a confirmation (production would call Jira/ServiceNow)."""
    ticket_id = f"IT-{abs(hash(employee_name + issue)) % 10000:04d}"  # simple stable-looking id
    return f"Ticket {ticket_id} created for {employee_name}: {issue}. IT will respond within 4 hours."


def escalate_to_hr(employee_name, query):
    """Safety valve: forward anything the agent should not answer to a human HR teammate."""
    return f"Query from {employee_name} escalated to HR: '{query}'. A team member will reply within 1 business day."


# ===========================================================================
# 3) THE GUARDRAILS  (the rules that keep the agent safe — the heart of a real use case)
# ===========================================================================
# A real system prompt tells the LLM these rules; here we express the SAME rules as plain checks.

SENSITIVE_WORDS = {"salary", "compensation", "ctc", "appraisal", "promotion", "disciplinary"}
TICKET_WORDS = {"ticket", "not", "cannot", "broken", "help", "connect", "working", "issue", "problem"}


def is_sensitive(query):
    """True if the question is about salary / appraisal / disciplinary — must be refused + escalated."""
    return bool(words(query) & SENSITIVE_WORDS)


def wants_it_ticket(query):
    """True if the employee is reporting an IT problem that documentation could not solve."""
    qw = words(query)
    return ("vpn" in qw or "laptop" in qw or "email" in qw) and bool(qw & TICKET_WORDS)


# ===========================================================================
# 4) THE AGENT  (routing: guardrail first -> tool -> search-and-ground -> escalate)
# ===========================================================================
# This tiny router mimics what create_openai_tools_agent + the system prompt do in the notes:
#   - refuse sensitive topics and escalate them
#   - create a ticket for unresolved IT problems
#   - otherwise SEARCH FIRST, answer only if grounded, and cite the source document
#   - if retrieval finds nothing, escalate honestly instead of guessing (no hallucination)
# `memory` is a dict carrying context across turns so follow-up questions ("them") still make sense.

def hr_agent(employee_name, query, memory):
    # GUARDRAIL 1 — sensitive topics are refused and handed to a human.
    if is_sensitive(query):
        note = escalate_to_hr(employee_name, query)
        return (f"I'm not able to help with salary or appraisal matters. "
                f"Please contact HR directly. {note}")

    # GUARDRAIL 2 — an unresolved IT problem becomes a ticket (an ACTION, not an answer).
    if wants_it_ticket(query):
        return create_it_ticket(employee_name, query)

    # MULTI-TURN — resolve pronouns like "them"/"they"/"it" using what we searched last turn.
    lookup_query = query
    if words(query) & {"them", "they", "it", "these", "forward"} and memory.get("last_topic"):
        lookup_query = query + " " + memory["last_topic"]  # glue last turn's topic back in

    # SEARCH FIRST — the core RAG behaviour.
    doc = search_hr_docs(lookup_query)

    # ESCALATE — retrieval returned nothing relevant, so refuse honestly (do NOT invent an answer).
    if doc is None:
        note = escalate_to_hr(employee_name, query)
        return f"I don't have that information in our HR documents. {note}"

    # GROUNDED ANSWER — remember the topic for follow-ups, then answer WITH the source cited.
    memory["last_topic"] = lookup_query
    return f"(searched HR docs) Based on [{doc['source']}]: {doc['text']}"


# ===========================================================================
# DEMO 1 — A LIVE CONVERSATION  (in-domain, tool, refusal, and a multi-turn follow-up)
# ===========================================================================
def demo_conversation():
    print("=" * 70)
    print("DEMO 1 — HR ONBOARDING AGENT: a short conversation with new joiner 'Priya'")
    print("=" * 70)

    memory = {}  # one memory per conversation — carries context between turns
    name = "Priya"
    turns = [
        "How many casual leaves do I get per year?",   # grounded answer from leave_policy.md
        "Can I carry them forward?",                    # multi-turn: "them" = casual leaves
        "How do I set up my company email?",            # grounded answer from it_setup_guide.md
        "What is my salary package?",                   # sensitive -> refuse + escalate
        "My VPN is not connecting even after the guide, please help",  # tool -> create IT ticket
    ]

    for query in turns:
        print(f"\nEmployee ({name}): {query}")
        print(f"Agent          : {hr_agent(name, query, memory)}")


# ===========================================================================
# DEMO 2 — EVALUATION HARNESS  (the SAME structured test-case idea from the notes)
# ===========================================================================
# Each case says which query to send and what we expect: a keyword the answer must contain, and
# whether the agent should REFUSE. We run every case on a fresh memory and print PASS/FAIL + a total.
EVAL_CASES = [
    {"id": "HR-001", "query": "How many casual leaves do I get per year?",
     "expect_keyword": "12", "expect_refusal": False},
    {"id": "HR-002", "query": "What is my salary?",
     "expect_keyword": "escalated", "expect_refusal": True},
    {"id": "HR-003", "query": "My VPN is not working, please raise a ticket",
     "expect_keyword": "ticket", "expect_refusal": False},
    {"id": "HR-004", "query": "How many earned leaves can I carry forward?",
     "expect_keyword": "30", "expect_refusal": False},
    {"id": "HR-005", "query": "Tell me about the latest cricket match score",
     "expect_keyword": "escalated", "expect_refusal": True},
]


def demo_evaluation():
    print("\n" + "=" * 70)
    print("DEMO 2 — EVALUATION: run the structured test cases, count PASS/FAIL")
    print("=" * 70)

    passed = 0
    for case in EVAL_CASES:
        reply = hr_agent("Tester", case["query"], memory={}).lower()  # fresh memory per case
        keyword_ok = case["expect_keyword"].lower() in reply          # did the expected word appear?
        refused = ("escalated" in reply) or ("not able to help" in reply)
        refusal_ok = (refused == case["expect_refusal"])              # did it refuse only when it should?
        ok = keyword_ok and refusal_ok
        passed += 1 if ok else 0
        print(f"[{'PASS' if ok else 'FAIL'}] {case['id']} — {case['query'][:45]}")

    print(f"\nResults: {passed}/{len(EVAL_CASES)} passed.")
    print("Good evals cover four categories: grounded answer, tool use, refusal, and multi-turn continuity.")


# ===========================================================================
# DRIVER
# ===========================================================================
def main():
    demo_conversation()   # watch grounding, tool use, refusal, and memory in one chat
    demo_evaluation()     # prove it with structured PASS/FAIL cases

    # Try it yourself:
    #   1) Add an org-chart question: "Who is the head of engineering?" -> grounded answer (Anita Rao).
    #   2) Add a NEW HR document to HR_DOCUMENTS and ask about it — no re-training, just more corpus.
    #   3) Add a sensitive word to SENSITIVE_WORDS and confirm that topic now refuses + escalates.
    #   4) Break memory: ask "Can I carry them forward?" as the FIRST turn — with no context, it should
    #      escalate instead of guessing. That is the honest-refusal behaviour, not a hallucination.
    print("\nSame pattern, any domain: corpus + retrieval + tools + guardrails + escalation + evaluation.")


if __name__ == "__main__":
    main()
