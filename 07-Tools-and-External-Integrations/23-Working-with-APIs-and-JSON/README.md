# Working with APIs and JSON

## Context of This Session

In the **previous session**, you **evaluated and improved** the **ShopKart RAG assistant** — classifying failures as **retrieval**, **generation**, or **hallucination**, tuning **top-k**, **metadata filters**, and **grounding prompts**, and practising **test → diagnose → improve → re-test**. You also saw how **Groq rate limits** can stop generation when too many API calls run in one script.

That work sharpened answers from **stored policy documents**. Today you extend the assistant's world: **live facts from external systems** — order status, weather, exchange rates — arrive through **APIs**, usually packaged as **JSON**.

**In this session, you will:**

- Distinguish **RAG** (document-grounded answers) from **API-fetched live data**
- Map the **request–response pattern** onto **Groq calls** you already use
- Understand **REST methods** and **HTTP status codes** — including **429 rate limits**
- **Parse JSON** in Python with **`json.loads()`** and **`response.json()`**
- Run a **GET request** with **`requests`**, handle errors safely, and **print extracted JSON fields** in the terminal

The lab **is** part of the session — you build and run **`shopkart_api_json_lab.py`** (fetch and parse only). **Groq prompt routing**, **function calling**, and **RAG-plus-API agent workflows** come in the **next** session.

---

## RAG Answers Documents — APIs Fetch Live Facts

Your ShopKart bot already handles policy questions well when the answer lives in **returns**, **shipping**, **warranty**, or **refunds** files indexed in **Chroma**.

| Customer question | Best source | Why |
|---|---|---|
| *"Can I return an opened laptop charger?"* | **RAG** — search policy chunks | Rule lives in stored documents |
| *"Where is order ORD-88421 right now?"* | **API** — live order system | Status changes every minute — not in PDFs |
| *"What is today's temperature in Delhi for courier pickup?"* | **API** — weather service | External live reading |
| *"Summarise the 7-day return window politely"* | **RAG + LLM** | Evidence from policy; natural language from model |

- **RAG (Retrieval-Augmented Generation)**
  - **Official Definition:** A pattern where a model answers using **retrieved excerpts** from a prepared knowledge base.
  - **In Simple Words:** Search your **rule book first**, then write the reply from what you found.
  - **Real-Life Example:** A hostel warden answering from the **printed notice board**, not from memory alone.

- **API (Application Programming Interface)**
  - **Official Definition:** A **contract** between two software components — what request may be sent and what response will be returned.
  - **In Simple Words:** A **fixed menu** for asking another system for work and getting a structured answer back.
  - **Real-Life Example:** Swiggy's app asking the restaurant system *"Show pending orders for outlet 42"* and getting a list back — not copying data by hand.

**Integrated learning point:** Mixing them up creates **confident wrong answers**. Policy text cannot tell you **today's courier location**. Live API data should not invent **return windows** that live only in PDFs. Professional assistants **pick the right source first**.

### Simple Activity — RAG or API?

For each ShopKart customer line, write **RAG**, **API**, or **Both** and one reason:

1. *"Is express delivery available in metro cities?"*
2. *"Has my refund for order ORD-4421 been processed yet?"*
3. *"What is the warranty period for electronics?"*
4. *"Will heavy rain in Mumbai delay today's express handoff?"*

**Expected direction:** (1) RAG — policy wording; (2) API — live order/refund status; (3) RAG — warranty file; (4) API for live weather + RAG or policy for express rules if combining in a **next** workflow.

![RAG vs API for ShopKart — stored policy chunks answer rule questions; live order status weather and rates need external API calls](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session23/session23-01-rag-vs-api.png)

---

## The Request–Response Pattern You Already Use

Every **Groq** call in your RAG labs follows the same rhythm as **Flipkart**, **UPI**, or a **weather app**:

1. **Prepare a request** — where to send it, what action you want, and any details (prompt, model name, API key).
2. **Send the request** over the internet.
3. **Receive a response** — first a **status** (success or failure), then **data** (often JSON).

Think of an API like a **restaurant waiter**. You do not enter the kitchen. You order from the **menu** (the contract). The waiter carries your **request** and brings back **food** or says *"that item is unavailable today"*.

| Request part | Plain meaning | Groq call example |
|---|---|---|
| **URL / endpoint** | Address of the service | Groq chat completions endpoint (handled by the library) |
| **Method** | Action type — read vs create | **POST** — you are **creating** a new model completion |
| **Headers** | Metadata — auth, content type | **Authorization** with your **API key** from **`.env`** |
| **Body** | Data you send | **Messages** list with system + user prompt |

| Response part | Plain meaning | Groq call example |
|---|---|---|
| **Status code** | Success or error signal | **200** when completion succeeds; **429** when rate limited |
| **Body** | Payload — usually JSON | Object with **`choices[0].message.content`** — the reply text |

- **Status code**
  - **Official Definition:** A three-digit HTTP signal summarising whether a request succeeded or failed, and why.
  - **In Simple Words:** The server's **first answer** before you trust the data — *"OK"*, *"not found"*, or *"slow down"*.
  - **Real-Life Example:** A courier saying *"parcel delivered"* vs *"wrong pin code"* — you react differently before opening the box.

**Common doubt:** *"The Groq library hides HTTP — do I still need this?"* **Yes.** Libraries wrap the same pattern. When something breaks — **401** bad key, **429** too many calls — you diagnose faster if you know **status before body**.

![The four parts of an API request — URL, HTTP method, headers (auth and content type), and optional JSON body](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session23/session23-02-api-request-four-parts.png)

### Simple Activity — Match Groq to the Pattern

Fill this table from memory of your RAG script (no coding required):

| Part | Your Groq usage |
|---|---|
| Authentication | |
| Data you send | |
| Data you read back | |
| Failure you saw in the previous lab | |

**Expected direction:** **`.env` / GROQ_API_KEY**; **`messages`** with policy excerpts and customer question; **`response.choices[0].message.content`**; **429** or empty answers when limits hit.

---

## REST Conventions and HTTP Methods

Most web APIs follow **REST** — a convention where URLs name **resources** (things) and **HTTP methods** express the **action**.

- **REST**
  - **Official Definition:** **Representational State Transfer** — design guidelines structuring APIs around **nouns** (resources), not action verbs in the URL.
  - **In Simple Words:** Name the **thing** (`/orders`), then say **what to do** with GET/POST/PATCH/DELETE.
  - **Real-Life Example:** A library shelf labelled **"Orders"** — you **read**, **add**, **edit**, or **remove** books on that shelf using different procedures.

| CRUD action | HTTP method | Plain use | Body usually? |
|---|---|---|---|
| **Create** | **POST** | Add a new record | Yes |
| **Read** | **GET** | Fetch data | No |
| **Update (partial)** | **PATCH** | Change some fields | Yes |
| **Update (full)** | **PUT** | Replace entire record | Yes |
| **Delete** | **DELETE** | Remove a record | Rarely |

| What you want | Non-REST style | REST style |
|---|---|---|
| List orders | `/get-orders` | **GET** `/orders` |
| One order | `/get-order-by-id` | **GET** `/orders/88421` |
| Place order | `/create-order` | **POST** `/orders` |

**Integrated learning point:** REST is a **convention**, not a strict law. Real products bend rules. Learning REST helps you **read documentation** and **design agent tools** in the **next** session.

![REST style — resource-based URLs paired with HTTP methods for read, create, partial update, full replace, and delete](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session23/session23-03-rest-http-methods.png)

Today's lab uses **GET** only — you **read** live weather for a delivery city without changing anything on the server.

---

## HTTP Status Codes — Check Before You Trust the Body

Status codes group by first digit:

| Range | Meaning | Who to fix? |
|---|---|---|
| **2xx** | Success | Nobody — proceed |
| **4xx** | Client error | Your request, key, or URL |
| **5xx** | Server error | External service |

| Code | Plain meaning | ShopKart / lab connection |
|---|---|---|
| **200** | OK — data returned | Weather GET succeeded |
| **201** | Created | New order placed via POST (future tools) |
| **400** | Bad request — invalid input | Wrong latitude format in URL |
| **401** | Unauthorized — bad or missing key | Invalid **GROQ_API_KEY** |
| **404** | Not found | Wrong API path or order ID |
| **429** | Too many requests — rate limit | **Groq free tier** during heavy RAG testing |
| **500** | Server error | External API temporarily down |

**Why 429 matters here:** In the **previous** evaluation lab, running many queries quickly consumed **Groq** quota. That is **429** behaviour — not a Python syntax bug. **Pause, retry later, or use a fresh key** before blaming retrieval.

![HTTP status families — 2xx success, 4xx client mistakes, 5xx server problems — with common codes you will see in practice](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session23/session23-04-http-status-codes.png)

### Simple Activity — Status Code Scenarios

Match each situation to the most likely code:

1. Weather API URL typo — `/forcast` instead of `/forecast`
2. Script sends 40 Groq completions in one minute on a free account
3. Weather API returns current temperature JSON successfully
4. ShopKart order API receives malformed order ID `ORD???`

**Expected direction:** **404** or **400**; **429**; **200**; **400**.

**Professional habit:** In code, always check **`response.status_code == 200`** (or **`response.ok`**) **before** parsing JSON. Never feed an error HTML page into **Groq** as if it were weather data.

---

## JSON — The Data Format APIs Speak

**JSON** (**JavaScript Object Notation**) is **structured text** — **key–value pairs**, **lists**, and **nested objects** — sent over the internet.

- **Official Definition:** A lightweight, text-based format for storing and transmitting structured data between systems.
- **In Simple Words:** A **filled form** computers can exchange — labels and values in a standard shape.
- **Real-Life Example:** A courier label: **`"city": "Mumbai"`**, **`"pin": "400001"`**, **`"weight_kg": 2.5`**.

JSON maps cleanly to Python:

| JSON | Python |
|---|---|
| `{ "name": "Ravi" }` | `{ "name": "Ravi" }` dict |
| `[1, 2, 3]` | list |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

**Common doubt:** *"API returned JSON — why can't I use `data["temperature"]` immediately?"* Sometimes the library already parsed it (**`response.json()`** in **`requests`**). Sometimes you receive one big **string** — then you need **`json.loads()`** first.

![JSON as structured key–value text — and how json.loads / json.dumps swap between strings and Python dictionaries](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session23/session23-05-json-python-roundtrip.png)

### Sample API Response (Weather)

```json
{
  "latitude": 28.6139,
  "longitude": 77.209,
  "current": {
    "temperature_2m": 34.2,
    "weather_code": 3
  }
}
```

**Navigation practice:** **`current.temperature_2m`** → **34.2**; **`current.weather_code`** → **3**. In Python after parsing: **`data["current"]["temperature_2m"]`**.

### Simple Activity — Find the Fields

From the JSON above, write the path (keys in order) to:

1. City latitude
2. Current temperature
3. Weather code

---

## Working with JSON in Python

Python's built-in **`json`** module needs **no pip install**.

- **`json.loads()`** — **L**oad **S**tring → JSON text **into** a Python **dict**
- **`json.dumps()`** — **D**ump to **S**tring → Python **dict into** JSON text for sending

### Full Code Example — Parse and Stringify JSON

```python
# Import the built-in JSON module — no installation needed
import json

# ─────────────────────────────────────────────────────────────────
# PART 1: json.loads() — parse a JSON string into a Python dict
# ─────────────────────────────────────────────────────────────────

# Raw JSON arrives as ONE text string from an API (or a saved file)
json_response_string = '''
{
    "order_id": "ORD-88421",
    "status": "out_for_delivery",
    "customer_city": "Delhi",
    "eta_hours": 4
}
'''

# Convert JSON string into a Python dictionary
order = json.loads(json_response_string)

# Access fields with dictionary syntax
print("Order ID:", order["order_id"])
print("Status:", order["status"])
print("City:", order["customer_city"])

# ─────────────────────────────────────────────────────────────────
# PART 2: json.dumps() — convert a Python dict to a JSON string
# ─────────────────────────────────────────────────────────────────

# Build data in Python first — easier to work with
tracking_update = {
    "order_id": "ORD-88421",
    "event": "courier_picked_up",
    "city": "Delhi"
}

# Convert to JSON text ready for an API POST body
json_to_send = json.dumps(tracking_update, indent=2)

print("\nJSON ready to send:")
print(json_to_send)
print("Type:", type(json_to_send))
```

**How the code works:**

- **`import json`** — standard library for parse/stringify only.
- **`json.loads(...)`** — turns wire-format **text** into a **`dict`** you can index.
- **`order["status"]`** — same bracket access as any Python dictionary.
- **`json.dumps(..., indent=2)`** — pretty-prints JSON for logging or request bodies.
- **`type(json_to_send)`** shows **`str`** — JSON on the wire is always text.

**Integrated learning point:** **`requests`** can skip manual **`loads`** when you call **`response.json()`** — it parses for you. **`loads`** still matters when JSON arrives as a **string** from logs, files, or older examples.

---

## What Comes Next — From Parsed JSON to Agent Tools

The full pattern — **fetch → parse → select fields → prompt → generate** — is how agents combine **live tools** with **language models**. You build the first half today; the **next** session completes it with **function calling**.

![Large language models are consumed like any other API — client, authenticated POST, JSON response with the model's answer](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session23/session23-06-llm-as-api-preview.png)

**Preview (next session):** A customer asks whether **express courier handoff in Delhi** might be affected by **current weather**. Policy files explain **express rules** (RAG tool). **Live temperature** comes from the **weather API** you practise today. The agent **chooses both tools**, then **Groq** merges results into one reply.

**Why extract fields today?** Huge JSON payloads waste **tokens** and invite **invented fields** when you prompt later. Pull **`temperature_c`** and **`weather_code`** only — same discipline as sending **top-k policy chunks**, not the whole PDF.

**Note on `json.dumps()`:** You saw it in the parse demo for **logging**. In the **next** session it also helps when **tool arguments** are sent as JSON-shaped request bodies.

---

## Project Setup

Create a folder **`shopkart_api_json_lab`** with:

```
shopkart_api_json_lab/
└── shopkart_api_json_lab.py
```

Install packages:

```bash
pip install requests
```

- **`requests`** — send **GET** HTTP calls from Python and read **status codes** plus JSON bodies.

No **Groq** call in today's lab — that keeps focus on **fetch-and-parse** and avoids **429 rate limits** from stacking two API services in one script.

---

## Full Lab Code — Weather GET → Parse → Print Fields

Save as **`shopkart_api_json_lab.py`**:

```python
# shopkart_api_json_lab.py — GET live weather JSON, parse, extract fields, print to terminal

import json  # Pretty-print extracted fields in the terminal
import sys  # Exit cleanly when the weather API returns an error status

import requests  # Send HTTP GET requests to public APIs

# ── Configuration ─────────────────────────────────────────────────────────────
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"  # Free public weather API — no key required
DELHI_LAT = 28.6139  # Latitude for Delhi — demo delivery city
DELHI_LON = 77.2090  # Longitude for Delhi
CITY_NAME = "Delhi"  # Human label — must match coordinates you pass
REQUEST_TIMEOUT_SECONDS = 15  # Stop waiting if the network hangs


def fetch_current_weather(latitude: float, longitude: float) -> dict:
    """GET live weather JSON for a city coordinate pair."""
    params = {  # Query parameters appended to the URL after ?
        "latitude": latitude,  # North-south position
        "longitude": longitude,  # East-west position
        "current": "temperature_2m,weather_code",  # Only fields we need — keeps response small
    }
    response = requests.get(OPEN_METEO_URL, params=params, timeout=REQUEST_TIMEOUT_SECONDS)  # GET — read only

    print(f"Weather API status code: {response.status_code}")  # Always inspect status first

    if response.status_code != 200:  # Non-success — do not trust body as weather data
        print("Weather API call failed. Body preview:")
        print(response.text[:500])  # Print start of error message for debugging
        sys.exit(1)  # Stop before parsing error HTML as weather JSON

    return response.json()  # Parse JSON body into Python dict — like json.loads(response.text)


def extract_weather_fields(city_name: str, weather_data: dict) -> dict:
    """Pull only the fields a future agent tool or prompt would trust."""
    current = weather_data["current"]  # Nested object with live readings
    return {
        "city": city_name,  # Label for logs — must match the coordinates fetched
        "temperature_c": current["temperature_2m"],  # Degrees Celsius — live fact
        "weather_code": current["weather_code"],  # Numeric code — mapped to words in the next session
        "latitude": weather_data["latitude"],  # Echo coordinate for traceability
        "longitude": weather_data["longitude"],  # Echo coordinate for traceability
    }


def main():
    print(f"Step 1 — GET live weather for {CITY_NAME}...")
    weather_data = fetch_current_weather(DELHI_LAT, DELHI_LON)

    print("\nStep 2 — Extract selected JSON fields...")
    fields = extract_weather_fields(CITY_NAME, weather_data)
    print(json.dumps(fields, indent=2))  # Verification output — this dict feeds tools in the next session

    print("\nStep 3 — Confirm types (parsed dict, not raw string)...")
    print("temperature_c type:", type(fields["temperature_c"]))
    print("Lab complete — structured weather data ready for agent tools.")


if __name__ == "__main__":
    main()  # Run fetch → parse → extract → print when script executed directly
```

Run:

```bash
cd shopkart_api_json_lab
python shopkart_api_json_lab.py
```

Use **`python3`** if that is how Python is installed on your machine.

**How the code works:**

- **`requests.get(..., params=...)`** builds a **GET** URL with **`latitude`**, **`longitude`**, and **`current`** fields — **read-only**, no request body.
- **`response.status_code`** checked **before** **`response.json()`** — avoids parsing error pages as weather.
- **`extract_weather_fields`** selects a **small dict** — the same shape you will register as a **tool result** in the **next** session.
- **No Groq call today** — one external API, one learning goal: **trust only parsed fields after status 200**.

### Terminal Verification Checklist

| Step | What to look for |
|---|---|
| **Status** | `Weather API status code: 200` |
| **Extracted JSON** | **`city`**, **`temperature_c`**, **`weather_code`** printed |
| **Types** | `temperature_c type: <class 'float'>` (or similar numeric type) |
| **Failure drill** | Temporarily break the URL — confirm script **stops** on non-200 instead of printing fake weather |

### Simple Activity — Change City Coordinates

Update **`CITY_NAME`**, **`DELHI_LAT`**, and **`DELHI_LON`** to Mumbai (**19.0760**, **72.8777**). Re-run and confirm:

1. Status **200** from the weather API
2. **`city`** prints **Mumbai**
3. **`temperature_c`** **changes** from the Delhi run

**Common mistake:** Updating **`city`** in the label but leaving **Delhi coordinates** — extracted data would say Mumbai while showing **Delhi weather**. **Label and coordinates must match.**

---

## Combining RAG and APIs — Next Session Preview

Full **ShopKart** production flows often need **both**:

| Step | Source | When |
|---|---|---|
| 1 | **RAG** | Retrieve **express delivery policy** from Chroma |
| 2 | **API tool** | **GET** live weather for the customer's city |
| 3 | **Groq** | Merge **policy excerpts + live weather fields** in one grounded prompt |

Today you master **step 2 data only** — reliable **fetch, status check, parse, extract**. The **next** session adds **function calling** so the **model chooses** step 1 vs step 2, then writes step 3 — instead of you hard-coding every branch.

**Integrated learning point:** The evaluation habit from the **previous** session still applies in the **next** lab. If the final answer cites **35°C** but your tool JSON showed **28°C**, that is a **generation** failure — not an API failure.

---

## Key Takeaways

- **RAG** answers from **stored documents**; **APIs** fetch **live external facts** — picking the wrong source produces confident errors.
- Every call — **weather GET** or **Groq POST** — follows **request → status → body**; check **status codes** before trusting JSON.
- **REST** maps **GET/POST/PATCH/PUT/DELETE** to **read/create/update/delete**; today's lab uses **GET** only.
- **`json.loads()`** and **`response.json()`** turn API text into Python dicts; **`json.dumps()`** helps log or send structured data — extract **only needed fields** before any LLM step.
- **Next:** **function calling** and **tool integration** — register today's weather helper and RAG retrieval as tools, route JSON into **Groq**, and close Module 2 with one combined ShopKart reply.

---

## Important Commands, Libraries, and Terminologies used

| Term / Command | Meaning in one line |
|---|---|
| **API** | Contract defining allowed requests and expected responses between systems |
| **REST** | Resource-based API style — nouns in URLs, actions in HTTP methods |
| **GET** | HTTP method to **read** data without changing server state |
| **POST** | HTTP method to **create** or submit data — used by Groq under the hood |
| **Status code** | Numeric success/error signal — **200** OK, **429** rate limit, **404** not found |
| **JSON** | Structured text format — keys, values, lists, nested objects |
| **`json.loads()`** | Parse JSON **string** → Python **dict** |
| **`json.dumps()`** | Python **dict** → JSON **string** for logs or request bodies |
| **`requests.get()`** | Send HTTP GET; returns object with **`.status_code`**, **`.text`**, **`.json()`** |
| **`response.json()`** | Parse response body into Python dict when status is success |
| **`params=`** | Query parameters appended to URL (`?latitude=...&longitude=...`) |
| **Endpoint / URL** | Address of the API service |
| **Headers** | Request metadata — authentication, content type |
| **Rate limit (429)** | Too many requests in a short window — pause or reduce calls |
| **`requests`** | Third-party library for HTTP calls — `pip install requests` |
| **Field extraction** | Select only required JSON keys — feeds agent tools and prompts in the next session |
