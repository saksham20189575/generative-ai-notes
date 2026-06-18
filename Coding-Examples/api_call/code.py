# lecture23.py — ShopKart APIs & JSON lab (Session 23)
#
# Builds on the Session 20-22 RAG series. So far the ShopKart bot answered from
# STORED policy documents (returns / shipping / warranty / refunds) indexed in
# Chroma and written up by a Groq LLM. Today we extend its world with LIVE FACTS
# that change minute-to-minute — order status, weather, exchange rates — which
# arrive through APIs, usually packaged as JSON.
#
# Big idea this session: every call — a weather GET or a Groq POST — follows the
# SAME rhythm:  prepare request -> send -> read STATUS first -> only then trust
# the BODY (JSON).
#
# What this file demonstrates (fetch-and-parse only):
#   STAGE 1 — json.loads / json.dumps round-trip (string <-> Python dict)
#   STAGE 2 — GET live weather with requests, check status BEFORE parsing
#   STAGE 3 — extract ONLY the fields a future agent tool would trust
#   STAGE 4 — run several delivery cities through the full fetch -> parse -> print loop
#
# NOTE: There is intentionally NO Groq/LLM call today. The lecture notes defer
# "the model chooses RAG vs API tool, then merges both" to the NEXT session
# (function calling). Stacking two API services in one script also invites 429
# rate limits, so today stays focused on reliable fetch + parse + extract.

import json  # Built-in: parse JSON strings (loads) and pretty-print dicts (dumps) — no pip install
import sys  # Exit cleanly when the weather API returns a non-success status
from typing import Any, Dict, List  # Type hints make function signatures self-documenting

import requests  # Third-party: send HTTP GET calls and read .status_code / .text / .json()  (pip install requests)

# ---------------------------------------------------------------------------
# Configuration — one place to change the endpoint, cities, and timeouts
# ---------------------------------------------------------------------------
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"  # Free public weather API — no API key required
REQUEST_TIMEOUT_SECONDS = 15  # Stop waiting if the network hangs instead of blocking forever
HTTP_OK = 200  # Success status code — check this BEFORE trusting the response body

# Demo delivery cities — label MUST match the coordinates (a common, silent mistake)
DELIVERY_CITIES = [
    {"city": "Delhi", "latitude": 28.6139, "longitude": 77.2090},  # North — demo pickup city
    {"city": "Mumbai", "latitude": 19.0760, "longitude": 72.8777},  # West — express handoff hub
    {"city": "Bengaluru", "latitude": 12.9716, "longitude": 77.5946},  # South — courier coverage check
]


# ===========================================================================
# STAGE 1 — JSON ROUND-TRIP: string <-> Python dict (json.loads / json.dumps)
# ===========================================================================
def demo_json_round_trip() -> None:
    # APIs speak JSON — structured TEXT with key-value pairs, lists, and nested objects.
    # Sometimes JSON arrives as ONE big string (from a log, file, or older example):
    # then you must json.loads() it before indexing with dictionary brackets.
    json_response_string = """
    {
        "order_id": "ORD-88421",
        "status": "out_for_delivery",
        "customer_city": "Delhi",
        "eta_hours": 4
    }
    """  # Raw JSON exactly as it would arrive over the wire — note: this is a str

    # json.loads = Load String -> turn JSON text INTO a Python dict
    order = json.loads(json_response_string)  # Now `order` is a normal dict we can index

    print("STAGE 1 — json.loads(): parsed a JSON string into a Python dict")
    print("  Order ID :", order["order_id"])  # Same bracket access as any dict
    print("  Status   :", order["status"])  # 'out_for_delivery'
    print("  City     :", order["customer_city"])  # 'Delhi'
    print("  Parsed type:", type(order))  # <class 'dict'> — proof it is no longer a string

    # json.dumps = Dump to String -> turn a Python dict INTO JSON text (for logs / request bodies)
    tracking_update = {
        "order_id": "ORD-88421",  # Which order this event belongs to
        "event": "courier_picked_up",  # What happened
        "city": "Delhi",  # Where it happened
    }
    json_to_send = json.dumps(tracking_update, indent=2)  # indent=2 pretty-prints for readable logs

    print("\n  json.dumps(): Python dict -> JSON text ready to send/log")
    print(json_to_send)  # Human-friendly multi-line JSON
    print("  Serialized type:", type(json_to_send))  # <class 'str'> — JSON on the wire is always text


# ===========================================================================
# STAGE 2 — FETCH: GET live weather, check STATUS before trusting the BODY
# ===========================================================================
def fetch_current_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    # GET = the HTTP method for READING data without changing anything on the server (REST convention).
    params = {  # Query parameters appended to the URL after "?"  (?latitude=...&longitude=...&current=...)
        "latitude": latitude,  # North-south position of the delivery city
        "longitude": longitude,  # East-west position of the delivery city
        "current": "temperature_2m,weather_code",  # Ask for ONLY the fields we need — keeps the response small
    }

    # requests.get builds the URL, sends it, and returns a response object with .status_code / .text / .json()
    response = requests.get(OPEN_METEO_URL, params=params, timeout=REQUEST_TIMEOUT_SECONDS)  # Read-only, no body sent

    # Professional habit: ALWAYS inspect the status code first — the server's "first answer".
    print(f"  Weather API status code: {response.status_code}")  # 200 OK, 400 bad input, 404 wrong path, 429 rate limit...

    if response.status_code != HTTP_OK:  # Non-2xx — do NOT trust the body as weather data
        print("  Weather API call failed. Body preview (first 500 chars):")
        print(response.text[:500])  # Show the start of the error so you can diagnose 4xx vs 5xx
        sys.exit(1)  # Stop before accidentally parsing an HTML error page as weather JSON

    # requests can skip manual json.loads() — response.json() parses the JSON body into a Python dict for us
    return response.json()  # Equivalent to json.loads(response.text) when the status is success


# ===========================================================================
# STAGE 3 — EXTRACT: pull ONLY the fields a future agent tool / prompt trusts
# ===========================================================================
def extract_weather_fields(city_name: str, weather_data: Dict[str, Any]) -> Dict[str, Any]:
    # Huge JSON payloads waste tokens and invite invented fields when you prompt an LLM later.
    # Same discipline as sending top-k policy chunks (not the whole PDF) in the RAG labs:
    # navigate the nested JSON and keep only what matters.
    current = weather_data["current"]  # Nested object holding the live readings
    return {
        "city": city_name,  # Label for logs — MUST match the coordinates that were fetched
        "temperature_c": current["temperature_2m"],  # data["current"]["temperature_2m"] -> live Celsius reading
        "weather_code": current["weather_code"],  # Numeric code (mapped to words in a later session)
        "latitude": weather_data["latitude"],  # Echo coordinate back for traceability
        "longitude": weather_data["longitude"],  # Echo coordinate back for traceability
    }


# ===========================================================================
# STAGE 4 — WIRE THE LOOP: fetch -> status check -> parse -> extract -> print
# ===========================================================================
def report_city_weather(city_record: Dict[str, Any]) -> Dict[str, Any]:
    # Run ONE delivery city through the full pipeline and print a clean, structured result.
    city = city_record["city"]  # Human label for this city
    print("\n" + "=" * 72)
    print(f"Delivery city: {city}")
    print("=" * 72)

    # Step A — GET the live weather JSON (status is checked inside this call)
    weather_data = fetch_current_weather(city_record["latitude"], city_record["longitude"])

    # Step B — Extract only the small set of fields we will trust downstream
    fields = extract_weather_fields(city, weather_data)

    # Step C — Print the extracted dict as pretty JSON — this is the shape a tool would return next session
    print("  Extracted fields (this dict feeds agent tools in the next session):")
    print(json.dumps(fields, indent=2))

    # Step D — Confirm we are holding parsed Python types, not a raw string
    print("  temperature_c type:", type(fields["temperature_c"]))  # e.g. <class 'float'> — proof JSON was parsed

    return fields  # Return so callers could compare cities or feed a later RAG+API merge


def main() -> None:
    # First, the JSON round-trip demo so the loads/dumps mechanics are clear before any network call
    demo_json_round_trip()

    # Then run each demo delivery city through the live fetch -> parse -> extract -> print loop
    print("\n\n" + "#" * 72)
    print("LIVE WEATHER GET FOR EACH DELIVERY CITY")
    print("#" * 72)

    all_fields: List[Dict[str, Any]] = []  # Collect every city's extracted fields
    for city_record in DELIVERY_CITIES:  # One GET per city
        all_fields.append(report_city_weather(city_record))  # Fetch, parse, extract, print

    # Summary — confirm each city returned DIFFERENT live readings (label and coordinates matched)
    print("\n\n" + "#" * 72)
    print("SUMMARY — live temperature per delivery city")
    print("#" * 72)
    for fields in all_fields:
        print(f"  {fields['city']:<12} {fields['temperature_c']}°C  (weather_code={fields['weather_code']})")

    print("\nLab complete — structured weather data ready for agent tools (next session).")


if __name__ == "__main__":
    main()  # Run JSON demo, then fetch -> parse -> extract -> print for each city when executed directly