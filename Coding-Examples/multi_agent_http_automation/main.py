# main.py — MULTI-AGENT PIPELINE + TRIGGER + WEBHOOK you can run today (Session 36)
#
# The lecture notes build the "real" version with FastAPI + uvicorn + requests (see
# multi_agent_http_webhook_demo_server.py and call_pipeline_client.py in this folder). That needs
# installs and a running web server on a port. This file keeps the SAME SHAPE — a researcher -> writer
# -> editor pipeline, a POST "trigger" that starts it, an HMAC-signed webhook callback, signature
# verification, idempotency, and reliability rules — but strips out the machinery so it runs with
# nothing but plain Python:
#
#   python3 main.py        (no pip install, no server, no port, no internet)
#
# What you will see, exactly like the notes describe:
#   1. TRIGGER            -> a POST to /v1/pipeline/start kicks off a background job
#   2. MULTI-AGENT RUN    -> researcher -> writer -> editor, each with a clear input/output handoff
#   3. SIGNED WEBHOOK     -> the server POSTs the result to your callback_url with an X-Signature seal
#   4. VERIFICATION       -> the receiver rejects tampered payloads and accepts genuine ones
#   5. IDEMPOTENCY        -> a duplicate webhook (network retry) is detected and ignored safely
#
# The one big simplification: real delivery sends bytes over HTTP to another process. Here a tiny
# in-memory transport calls the receiver directly and hands back a status code — same request/response
# mental model, no network. Everything else — decompose into roles, sign the payload, verify the seal,
# dedupe by event id — is the real design.


import hashlib   # SHA-256 hashing, the core of the signature
import hmac      # keyed-hash message authentication code (the tamper-proof seal)
import json      # encode/decode the JSON payload we sign and send
import time      # timestamps + a fake, stable "event id"


# ===========================================================================
# 0) THE SHARED SECRET  (both sender and receiver know it; nobody else does)
# ===========================================================================
# In the notes this is WEBHOOK_SECRET on the server. The receiver uses the SAME secret to recompute
# the signature. If the bytes were changed in transit, the recomputed signature will not match.

WEBHOOK_SECRET = b"dev-secret-change-me"


def sign_bytes(payload_bytes):
    """Create an HMAC-SHA256 signature (a hex 'seal') for exactly these bytes."""
    return hmac.new(WEBHOOK_SECRET, payload_bytes, hashlib.sha256).hexdigest()


# ===========================================================================
# 1) THE THREE ROLE-BASED AGENTS  (task decomposition: evidence -> words -> polish)
# ===========================================================================
# Each role has a narrow job, a clear INPUT, and a clear OUTPUT the next role can rely on. This is the
# whole point of a multi-agent workflow: one brain per job, with defined handoff points.

def researcher(goal):
    """Stage 1 — find evidence. INPUT: a goal. OUTPUT: claims linked to evidence."""
    bullets = [
        {"claim": "Decompose goals into roles to reduce rework",
         "evidence": "Pipeline design principle in agent workflows"},
        {"claim": "Use HTTP endpoints to trigger and chain automation",
         "evidence": "Request/response patterns for workflow orchestration"},
        {"claim": "Use webhooks to notify completion without polling",
         "evidence": "Callback mechanism avoids repeated status checks"},
    ]
    return {"stage": "researcher", "goal": goal, "bullets": bullets}


def writer(research_output):
    """Stage 2 — turn evidence into a draft. INPUT: research output. OUTPUT: a structured draft."""
    paragraphs = [
        "Explain the goal first, then split the work into specialized roles.",
        "HTTP APIs trigger actions and return a structured status you can act on.",
        "Webhooks push events back to your system the moment work is done.",
    ]
    return {"stage": "writer",
            "title": f"Draft for: {research_output['goal']}",
            "draft": paragraphs}


def editor(writer_output):
    """Stage 3 — polish for clarity/consistency. INPUT: draft. OUTPUT: final notes."""
    cleaned = [line.strip().rstrip(".") + "." for line in writer_output["draft"]]
    return {"stage": "editor", "title": writer_output["title"], "final_notes": cleaned}


def run_pipeline(goal):
    """The orchestrator: run the roles IN ORDER and collect every stage output for the audit trail."""
    r = researcher(goal)   # evidence first
    w = writer(r)          # words second (using the research)
    e = editor(w)          # polish last (using the draft)
    return {"researcher": r, "writer": w, "editor": e}


# ===========================================================================
# 2) THE WEBHOOK RECEIVER  (your endpoint — treats every payload as untrusted input)
# ===========================================================================
# In the notes this is @app.post("/webhooks/pipeline-complete"). It must do three things, in order:
#   (a) verify the signature      -> is this really from us? (4xx if not)
#   (b) check the event id         -> have we already processed this one? (idempotency)
#   (c) accept and act once        -> return 2xx so the sender stops retrying
# `seen_event_ids` is the receiver's memory of what it has already handled.

seen_event_ids = set()


def webhook_receiver(body_bytes, headers):
    """Return (status_code, response_dict) — exactly like an HTTP endpoint would."""
    received_signature = headers.get("X-Signature", "")
    expected_signature = sign_bytes(body_bytes)   # recompute from the SAME bytes we received

    # (a) VERIFY — compare_digest avoids timing leaks; mismatch means tampered or wrong secret.
    if not hmac.compare_digest(received_signature, expected_signature):
        return 401, {"accepted": False, "reason": "invalid signature"}

    payload = json.loads(body_bytes.decode("utf-8"))
    event_id = payload.get("event_id")

    # (b) IDEMPOTENCY — a retry can deliver the same event twice; process it at most once.
    if event_id in seen_event_ids:
        return 200, {"accepted": True, "duplicate": True, "event_id": event_id}

    # (c) ACCEPT — remember the id, then act on the payload exactly once.
    seen_event_ids.add(event_id)
    return 200, {"accepted": True, "duplicate": False,
                 "received_goal": payload.get("goal"),
                 "final_notes": payload["stages"]["editor"]["final_notes"]}


# ===========================================================================
# 3) THE (FAKE) HTTP TRANSPORT  (stands in for requests.post over the network)
# ===========================================================================
# Real code does requests.post(callback_url, data=body, headers=headers). Here "posting" just calls the
# receiver directly and returns its status code — the same request -> response shape, minus the network.

def http_post(target, body_bytes, headers):
    print(f"    --> POST (signed webhook, {len(body_bytes)} bytes) to {target}")
    return webhook_receiver(body_bytes, headers)


def deliver_webhook(goal, stages, callback_url, event_id):
    """Build the completion payload, SIGN it, and POST it to the callback URL."""
    payload = {
        "event_id": event_id,          # the idempotency key the receiver dedupes on
        "event_name": "pipeline.completed",
        "goal": goal,
        "stages": stages,              # every stage output, for debugging + audit
        "completed_at": int(time.time()),
    }
    body_bytes = json.dumps(payload).encode("utf-8")     # exact bytes we sign
    headers = {"Content-Type": "application/json", "X-Signature": sign_bytes(body_bytes)}
    return body_bytes, headers, http_post(callback_url, body_bytes, headers)


# ===========================================================================
# 4) THE TRIGGER ENDPOINT  (POST /v1/pipeline/start — the "start button")
# ===========================================================================
# In the notes the server responds immediately and runs the pipeline in a BackgroundTask. Here we run
# it inline for clarity, but the shape is identical: trigger -> run roles -> deliver webhook.

def start_pipeline(goal, callback_url, event_id):
    print(f"[trigger] POST /v1/pipeline/start  goal={goal!r}")
    print("[trigger] responded {'started': True} immediately; running pipeline in background...")
    stages = run_pipeline(goal)
    for name in ("researcher", "writer", "editor"):
        print(f"    - {name} stage done")
    return deliver_webhook(goal, stages, callback_url, event_id)


# ===========================================================================
# DEMO 1 — HAPPY PATH  (trigger -> pipeline -> signed webhook -> receiver accepts)
# ===========================================================================
def demo_happy_path():
    print("=" * 74)
    print("DEMO 1 — TRIGGER -> MULTI-AGENT PIPELINE -> SIGNED WEBHOOK CALLBACK")
    print("=" * 74)
    goal = "Write lecture notes using multi-agent roles and automation"
    _, _, (status, resp) = start_pipeline(goal, "/webhooks/pipeline-complete", event_id="evt-1001")
    print(f"[receiver] status={status}  accepted={resp['accepted']}  duplicate={resp.get('duplicate')}")
    print(f"[receiver] final notes: {resp['final_notes'][0]}")


# ===========================================================================
# DEMO 2 — IDEMPOTENCY  (a network retry re-delivers the SAME event; ignore it safely)
# ===========================================================================
def demo_idempotent_retry():
    print("\n" + "=" * 74)
    print("DEMO 2 — DUPLICATE WEBHOOK (network retry): same event_id must NOT double-process")
    print("=" * 74)
    goal = "Summarize a chapter with a researcher-writer-editor crew"
    body, headers, (s1, r1) = start_pipeline(goal, "/webhooks/pipeline-complete", event_id="evt-2002")
    print(f"[receiver] 1st delivery -> status={s1}  duplicate={r1.get('duplicate')}  (processed)")
    s2, r2 = webhook_receiver(body, headers)   # the exact same bytes arrive a second time
    print(f"    --> POST (retry, identical bytes) to /webhooks/pipeline-complete")
    print(f"[receiver] 2nd delivery -> status={s2}  duplicate={r2.get('duplicate')}  (ignored, no double work)")


# ===========================================================================
# DEMO 3 — TAMPERED PAYLOAD  (the seal no longer matches -> reject with 4xx)
# ===========================================================================
def demo_bad_signature():
    print("\n" + "=" * 74)
    print("DEMO 3 — TAMPERED / UNSIGNED WEBHOOK: signature check must reject it")
    print("=" * 74)
    body, headers, _ = deliver_webhook(
        "Plan a trip", run_pipeline("Plan a trip"), "/webhooks/pipeline-complete", event_id="evt-3003")
    # An attacker changes the bytes after signing (or the secret is wrong): signature no longer matches.
    tampered = body.replace(b"Plan a trip", b"Transfer all money")
    status, resp = webhook_receiver(tampered, headers)
    print(f"    --> POST (payload edited AFTER signing) to /webhooks/pipeline-complete")
    print(f"[receiver] status={status}  accepted={resp['accepted']}  reason={resp.get('reason')}")


# ===========================================================================
# DEMO 4 — MATCH THE METHOD  (the notes' activity: pick the right HTTP method for each task)
# ===========================================================================
METHOD_FOR_TASK = [
    ("Start a background pipeline job", "POST",   "creates/triggers an action"),
    ("Fetch the latest job status",     "GET",    "reads without changing state"),
    ("Update only the retry policy",    "PATCH",  "partial update of one field"),
    ("Replace the whole job config",    "PUT",    "full replacement"),
    ("Remove a job record",             "DELETE", "removes the resource"),
]


def demo_method_matching():
    print("\n" + "=" * 74)
    print("DEMO 4 — MATCH THE HTTP METHOD TO THE TASK")
    print("=" * 74)
    for task, method, why in METHOD_FOR_TASK:
        print(f"  {method:<7} {task:<34} ({why})")


# ===========================================================================
# DRIVER
# ===========================================================================
def main():
    demo_happy_path()        # the full trigger -> pipeline -> signed webhook flow
    demo_idempotent_retry()  # duplicates are safe (idempotency key = event_id)
    demo_bad_signature()     # tampered payloads are rejected (HMAC signature)
    demo_method_matching()   # GET / POST / PUT / PATCH / DELETE — right tool for the job

    # Try it yourself:
    #   1) Change WEBHOOK_SECRET on only one side and re-run Demo 1 -> the receiver returns 401.
    #   2) Add a 4th role (e.g. "fact_checker") between writer and editor; wire its handoff.
    #   3) Give two different events the SAME event_id and confirm the 2nd is treated as a duplicate.
    #   4) Add a "retry with backoff" loop that re-POSTs on a 5xx but gives up after 3 attempts.
    print("\nSame pattern in production: decompose into roles + trigger with POST + verify + dedupe webhooks.")


if __name__ == "__main__":
    main()
