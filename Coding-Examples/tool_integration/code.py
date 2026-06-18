# lecture24.py — ShopKart Tool-Calling Agent lab (Session 24)
#
# Builds directly on the Session 20-23 arc. Sessions 20-22 gave the ShopKart bot
# RAG over STORED policy documents (returns / shipping / warranty / refunds).
# Session 23 added LIVE FACTS through APIs — a weather GET that we parsed in the
# terminal WITHOUT calling Groq. Today we close Module 2 by joining the two: the
# MODEL chooses which tool to use, OUR runtime executes it, and Groq writes one
# grounded customer reply from the structured JSON results.
#
# Big idea this session: FUNCTION CALLING. The model is the COORDINATOR; your
# Python functions are the WORKERS. The model NEVER touches Open-Meteo or Chroma
# directly — it only REQUESTS a tool by name with JSON arguments. Your runtime
# performs the real HTTP / retrieval and feeds the JSON result back.
#
# What this file demonstrates (the full agent loop):
#   STAGE 1 — register two tools with clear schemas (policy search + weather GET)
#   STAGE 2 — implement each tool so it ALWAYS returns JSON — success OR structured error
#   STAGE 3 — run the execution loop: propose -> execute -> return JSON -> final answer
#   STAGE 4 — drive demo queries that need policy only, weather only, and BOTH tools
#
# NOTE: search_shopkart_policy uses an INLINE policy map so the session stays
# focused on TOOL CALLING. Swap in your Chroma + BGE retriever from the previous
# build later — keep the SAME tool name and JSON shape and the loop is unchanged.

import json  # Parse the model's tool arguments (loads) and serialise tool results (dumps)
import sys  # Exit cleanly on unrecoverable setup errors (e.g. missing API key)
from typing import Any, Dict, List  # Type hints keep tool signatures self-documenting

import requests  # Third-party: the weather tool's HTTP GET (pip install requests)
from dotenv import load_dotenv  # Load GROQ_API_KEY from .env so keys stay out of code
from groq import Groq  # LLM client with NATIVE tool-calling support (pip install groq)

# ---------------------------------------------------------------------------
# Configuration — one place to change the model, endpoint, and timeouts
# ---------------------------------------------------------------------------
GENERATION_MODEL = "llama-3.3-70b-versatile"  # Same model family as prior ShopKart RAG labs
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"  # Free weather API from Session 23 — no key required
REQUEST_TIMEOUT_SECONDS = 15  # Stop waiting if the network hangs instead of blocking forever
HTTP_OK = 200  # Success status code — check this BEFORE trusting the response body

# Inline policy excerpts — the SAME four areas used across the ShopKart RAG labs.
# This stands in for Chroma retrieval so today's focus stays on tool calling.
POLICY_SNIPPETS = {
    "returns": (
        "Unopened items may be returned within 7 calendar days of delivery. "
        "Opened or used items are not eligible unless defective."
    ),
    "shipping": (
        "Standard delivery takes 3-5 business days after dispatch. "
        "Express delivery (paid) arrives in 1-2 business days in metro cities only."
    ),
    "warranty": (
        "Electronics carry a 12-month manufacturer warranty from delivery date. "
        "Warranty does not cover physical damage or liquid exposure."
    ),
    "refunds": (
        "Refunds are credited within 5-7 business days after warehouse verification. "
        "Cash-on-delivery orders are refunded to UPI or bank account only."
    ),
}


# ===========================================================================
# STAGE 1 — REGISTER TOOLS: machine-readable schemas the model reads to ROUTE
# ===========================================================================
# Groq (like other LLM APIs) accepts a `tools` list. Each entry describes ONE
# callable function: its name, WHEN to use it (description = routing instructions),
# and the JSON Schema for its arguments. The DESCRIPTION matters more than the
# name — write "Search ShopKart returns/shipping/warranty/refund policy", not "tool_a".
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_shopkart_policy",  # Short identifier the model emits in tool_calls
            "description": (  # Routing instructions: tells the model WHEN to pick this tool
                "Search ShopKart customer policy for returns, shipping, warranty, or refunds. "
                "Use when the question is about rules, timelines, or eligibility in policy documents."
            ),
            "parameters": {  # JSON Schema for the arguments the model must supply
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Customer policy question in plain English",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_city_weather",
            "description": (
                "Fetch current weather for a delivery city using latitude and longitude. "
                "Use when live weather may affect courier handoff or delivery timing."
            ),
            "parameters": {
                # Common mistake: registering weather with NO latitude/longitude — the model
                # then passes a city name only and the GET has nothing to look up. Include
                # city + coordinates here (or map city names to coordinates in your function).
                "type": "object",
                "properties": {
                    "city_name": {"type": "string", "description": "City label for logs and replies"},
                    "latitude": {"type": "number", "description": "City latitude"},
                    "longitude": {"type": "number", "description": "City longitude"},
                },
                "required": ["city_name", "latitude", "longitude"],
            },
        },
    },
]


# ===========================================================================
# STAGE 2 — IMPLEMENT TOOLS: each ALWAYS returns JSON — success OR honest error
# ===========================================================================
def search_shopkart_policy(query: str) -> Dict[str, Any]:
    """Return relevant policy excerpts as JSON — a lightweight stand-in for RAG retrieval."""
    query_lower = query.lower()  # Case-insensitive keyword routing
    matched: List[Dict[str, str]] = []  # Collect {category, text} dicts to return

    # Tiny keyword map mimics what a retriever would surface from the policy docs.
    keyword_map = {
        "returns": ["return", "unopened", "opened", "eligible", "send back"],
        "shipping": ["shipping", "express", "delivery", "metro", "dispatch"],
        "warranty": ["warranty", "repair", "defect", "liquid", "water"],
        "refunds": ["refund", "cod", "upi", "money back", "credit"],
    }

    for category, keywords in keyword_map.items():  # Scan each policy area
        if any(word in query_lower for word in keywords):  # Any keyword hit counts
            matched.append({"category": category, "text": POLICY_SNIPPETS[category]})

    if not matched:  # No keyword hit — return an HONEST empty result, never invent rules
        return {"error": "No policy excerpt found", "query": query, "excerpts": []}

    return {"query": query, "excerpts": matched}  # Structured success payload


def get_city_weather(city_name: str, latitude: float, longitude: float) -> Dict[str, Any]:
    """GET live weather — same status-before-parse pattern as Session 23; return JSON either way."""
    params = {  # Query parameters appended to the URL after "?" — read-only GET, no body
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code",  # Ask for ONLY the fields we need
    }
    response = requests.get(OPEN_METEO_URL, params=params, timeout=REQUEST_TIMEOUT_SECONDS)

    if response.status_code != HTTP_OK:  # Non-200 — return SAFE error JSON, never fake weather
        return {
            "error": "Weather API failed",
            "status_code": response.status_code,
            "city": city_name,
        }

    data = response.json()  # Parse the success body into a Python dict
    current = data["current"]  # Nested object holding the live readings
    return {
        "city": city_name,  # Label MUST match the coordinates that were fetched
        "temperature_c": current["temperature_2m"],  # Live Celsius reading
        "weather_code": current["weather_code"],  # Numeric condition code
        "latitude": latitude,  # Echo coordinates back for traceability
        "longitude": longitude,
    }


# Map tool NAMES (as the model emits them) to the Python callables that run them.
TOOL_FUNCTIONS = {
    "search_shopkart_policy": search_shopkart_policy,
    "get_city_weather": get_city_weather,
}


# ===========================================================================
# STAGE 3 — THE EXECUTION LOOP: propose -> execute -> return JSON -> final answer
# ===========================================================================
def run_tool_agent(client: Groq, user_message: str) -> str:
    """Run the model -> tool loop until the model returns a final natural-language answer."""
    messages: List[Dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "You are a precise ShopKart support assistant. "
                "Use tools when policy rules or live weather are needed. "
                "Ground answers in tool JSON only — do not invent policy numbers or weather. "
                "If a tool returns error, say you cannot confirm that part."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    # First turn — the model reads the tool list + user message and DECIDES the path:
    # return tool_calls (zero, one, or many) OR answer directly.
    response = client.chat.completions.create(
        model=GENERATION_MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",  # Let the model decide whether and which tools to call
    )
    assistant_message = response.choices[0].message

    # Loop WHILE the model keeps requesting tool executions. Each pass: run every
    # requested tool, append its JSON result, then ask the model to continue.
    while assistant_message.tool_calls:
        messages.append(assistant_message)  # Keep the assistant's tool_call message in history

        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name  # Which tool the model chose
            raw_arguments = tool_call.function.arguments  # Arguments arrive as a JSON STRING
            arguments = json.loads(raw_arguments)  # Parse the JSON string into a Python dict

            if function_name not in TOOL_FUNCTIONS:  # Guard against an unknown tool name
                result = {"error": f"Unknown tool: {function_name}"}
            else:
                result = TOOL_FUNCTIONS[function_name](**arguments)  # Execute the real Python tool

            # Send the tool result back as a `role: tool` message — JSON text, linked by id.
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,  # MUST match the pending tool call
                    "content": json.dumps(result),  # Tool result back to the model as JSON text
                }
            )

        # Ask the model again — now armed with the tool JSON. It may call MORE tools or finish.
        response = client.chat.completions.create(
            model=GENERATION_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        assistant_message = response.choices[0].message

    return assistant_message.content.strip()  # No more tool_calls -> final customer-facing answer


# ===========================================================================
# STAGE 4 — DRIVE DEMO QUERIES: policy only, weather only, and BOTH tools
# ===========================================================================
def main() -> None:
    load_dotenv()  # Read GROQ_API_KEY from .env (reuse the key from the ShopKart RAG labs)
    client = Groq()  # Client picks up GROQ_API_KEY from the environment

    if client is None:  # Defensive — should never trip, but fail loudly if the client is unset
        print("Groq client could not be created. Check GROQ_API_KEY in .env")
        sys.exit(1)

    demo_queries = [
        # 1) Policy only — should call search_shopkart_policy, cite 7 days, invent no weather.
        "Can I return unopened earphones within seven days?",
        # 2) BOTH tools — policy (express timing) AND live weather for Delhi in one reply.
        (
            "I chose express delivery to Delhi metro tomorrow. What does policy say about "
            "express timing, and is current weather likely to affect courier handoff today?"
        ),
    ]

    for user_message in demo_queries:
        print("\n" + "=" * 72)
        print("Customer:", user_message)
        print("=" * 72)
        answer = run_tool_agent(client, user_message)  # Run the full propose -> execute -> reply loop
        print("\nFinal answer:")
        print(answer)

    print("\nLab complete — the model chose tools, your runtime executed them, Groq grounded the reply.")


if __name__ == "__main__":
    main()  # Register tools, then run the tool-calling loop for each demo query when executed directly
