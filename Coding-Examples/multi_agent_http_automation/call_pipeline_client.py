# call_pipeline_client.py — calls the Session 36 trigger endpoint to start the pipeline.
#
# Start the server first:
#   uvicorn multi_agent_http_webhook_demo_server:app --reload --port 8000
# Then run this file:
#   python3 call_pipeline_client.py

import requests  # Import requests to call HTTP endpoints.

BASE_URL = "http://localhost:8000"  # Set the base URL for the local demo server.


def main() -> None:  # Define the main entry point.
    callback_url = f"{BASE_URL}/webhooks/pipeline-complete"  # Set the webhook receiver endpoint on the same server.
    payload = {  # Prepare the JSON body to start the pipeline.
        "user_goal": "Write lecture notes using multi-agent roles and automation",  # The goal that will be processed.
        "callback_url": callback_url,  # Where the webhook callback should be sent.
    }  # End payload.

    resp = requests.post(f"{BASE_URL}/v1/pipeline/start", json=payload, timeout=10)  # Call the trigger endpoint.
    resp.raise_for_status()  # Throw an error if the status code indicates failure.
    print("Start response:", resp.json())  # Print the JSON response returned by the start endpoint.


if __name__ == "__main__":  # Ensure main runs only when this file is executed directly.
    main()  # Call the main function.
