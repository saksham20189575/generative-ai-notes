# multi_agent_http_webhook_demo_server.py — the FastAPI version from the Session 36 notes.
#
# Run it with:
#   pip install fastapi uvicorn requests
#   uvicorn multi_agent_http_webhook_demo_server:app --reload --port 8000
#
# Then, in a second terminal:
#   python3 call_pipeline_client.py
#
# If you do not want to install anything, run `python3 main.py` instead — same flow, no server.

from fastapi import FastAPI, Request, BackgroundTasks  # Import FastAPI core types for endpoints and background tasks.
from pydantic import BaseModel  # Import BaseModel to define request body schemas.
import hashlib  # Import hashlib to compute SHA-256 hashes for signatures.
import hmac  # Import hmac to create secure message authentication codes (MAC).
import json  # Import json to encode/decode JSON payloads.
import time  # Import time to add timestamps to events.
import requests  # Import requests to send outbound HTTP webhook callbacks.
from typing import Dict, Any  # Import typing types for clearer payload structures.

app = FastAPI()  # Create the FastAPI app instance.

WEBHOOK_SECRET = b"dev-secret-change-me"  # Store a secret used to sign and verify webhook payloads.


class StartPayload(BaseModel):  # Define the expected body for starting the pipeline.
    user_goal: str  # Store the goal that the pipeline should process.
    callback_url: str  # Store the URL where the webhook callback will be sent.


def sign_bytes(payload_bytes: bytes) -> str:  # Create an HMAC signature for the given payload bytes.
    mac = hmac.new(WEBHOOK_SECRET, payload_bytes, hashlib.sha256)  # Compute HMAC using the secret and SHA-256.
    return mac.hexdigest()  # Convert the MAC result into a hex string for transport.


def researcher(goal: str) -> Dict[str, Any]:  # Simulate a research step that returns evidence-like bullets.
    bullets = [  # Create bullet points that look like evidence-backed claims.
        {"claim": "Decompose goals into roles to reduce rework", "evidence": "Pipeline design principle in agent workflows"},  # Example evidence text.
        {"claim": "Use HTTP endpoints to trigger and chain automation", "evidence": "HTTP request/response patterns for workflow orchestration"},  # Example evidence text.
        {"claim": "Use webhooks to notify completion without polling", "evidence": "Webhook callback mechanism avoids repeated checks"},  # Example evidence text.
    ]  # End bullets list.
    return {"stage": "researcher", "goal": goal, "bullets": bullets}  # Return structured research output.


def writer(research_output: Dict[str, Any]) -> Dict[str, Any]:  # Simulate a writing step that turns bullets into a draft.
    title = f"Draft for: {research_output['goal']}"  # Build a title using the goal.
    paragraphs = [  # Create short paragraphs to keep structure simple.
        "Explain the goal first, then split work into roles.",  # Describe decomposition in plain words.
        "Show that HTTP APIs trigger actions and return structured status.",  # Describe HTTP as workflow backbone.
        "Show that webhooks push events back to your system when done.",  # Describe webhook callback chaining.
    ]  # End paragraphs list.
    return {"stage": "writer", "title": title, "draft": paragraphs}  # Return structured writer output.


def editor(writer_output: Dict[str, Any]) -> Dict[str, Any]:  # Simulate an editing step that improves clarity and consistency.
    cleaned = [line.strip().rstrip(".") + "." for line in writer_output["draft"]]  # Normalize formatting for each paragraph line.
    return {"stage": "editor", "title": writer_output["title"], "final_notes": cleaned}  # Return structured final edited notes.


def run_pipeline_and_callback(goal: str, callback_url: str) -> None:  # Run the full pipeline and send a webhook callback.
    r = researcher(goal)  # Execute the researcher stage.
    w = writer(r)  # Execute the writer stage using research output.
    e = editor(w)  # Execute the editor stage using writer output.

    callback_payload = {  # Build the webhook payload that will be sent to the receiver.
        "goal": goal,  # Include the original goal for context.
        "stages": {"researcher": r, "writer": w, "editor": e},  # Include all stage outputs for debugging and audit.
        "completed_at": int(time.time()),  # Include a completion timestamp (epoch seconds).
    }  # End callback_payload.

    body_bytes = json.dumps(callback_payload).encode("utf-8")  # Convert payload dict into JSON bytes for signing.
    signature = sign_bytes(body_bytes)  # Create a signature for the JSON bytes.
    headers = {"Content-Type": "application/json", "X-Signature": signature}  # Add signature header so receiver can verify authenticity.

    # Send the webhook callback to the configured callback URL.
    requests.post(callback_url, data=body_bytes, headers=headers, timeout=10)  # Post the event payload with a timeout.


@app.get("/health")  # Define a health endpoint for quick checking.
def health() -> Dict[str, str]:  # Return a simple response object.
    return {"status": "ok"}  # Indicate the service is running.


@app.post("/webhooks/pipeline-complete")  # Define the webhook receiver endpoint.
async def pipeline_complete_webhook(request: Request) -> Dict[str, Any]:  # Receive webhook payload and validate it.
    body = await request.body()  # Read raw request body bytes for signature verification.
    received_signature = request.headers.get("X-Signature", "")  # Extract signature from headers (may be missing).
    expected_signature = sign_bytes(body)  # Compute expected signature from the shared secret and body.

    if not hmac.compare_digest(received_signature, expected_signature):  # Compare signatures securely to avoid timing leaks.
        return {"accepted": False, "reason": "invalid signature"}  # Reject if signature is wrong.

    decoded = json.loads(body.decode("utf-8"))  # Parse JSON payload into a Python dictionary.
    return {"accepted": True, "received_goal": decoded.get("goal")}  # Confirm acceptance and show one field for visibility.


@app.post("/v1/pipeline/start")  # Define a trigger endpoint that starts the pipeline.
async def start_pipeline(payload: StartPayload, background: BackgroundTasks) -> Dict[str, Any]:  # Accept input and schedule background execution.
    background.add_task(run_pipeline_and_callback, payload.user_goal, payload.callback_url)  # Run pipeline and then send webhook in background.
    return {"started": True, "callback_url": payload.callback_url}  # Respond immediately so the caller knows the job started.
