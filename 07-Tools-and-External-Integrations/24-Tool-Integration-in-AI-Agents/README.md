# Tool Integration in AI Agents

## Context of This Session

In the **previous session**, you built the **API and JSON foundation** — **RAG vs live data**, **request–response** mapping, **REST** and **status codes**, and a **weather GET lab** that **parsed JSON in the terminal** without calling **Groq**.

Today you **complete the agent loop**. The model **chooses tools** — **policy search** and **weather fetch** — your Python runtime **executes** them, and **Groq** writes one **grounded ShopKart reply** from **structured JSON results**. This is the **last build session of Module 2** before **LangChain** single-agent work in the **upcoming module**.

**In this session, you will:**

- Explain **function calling** — model selects tools; runtime executes them
- **Register** a **policy search tool** and a **weather API tool** with clear schemas
- Run the **tool execution loop** — propose → execute → return JSON → final answer
- **Handle tool errors** safely — no invented weather or policy when tools fail
- **Combine RAG-style policy excerpts and live weather** in one customer response

The lab **is** the session — you build and run **`shopkart_tool_agent.py`**.

---

## From Fixed Scripts to Tool-Calling Agents

In the **previous session**, **you** decided every step: call weather API, parse fields, print JSON. That works for **one demo path**. Real support questions mix sources unpredictably.

| Question type | Tool needed | Fixed script problem |
|---|---|---|
| *"Seven-day return for unopened items?"* | **Policy search only** | Weather call wastes time |
| *"Current temperature in Mumbai?"* | **Weather only** | Policy search adds noise |
| *"Express to Delhi tomorrow — policy + rain impact?"* | **Both tools** | Hard-coded `if/else` breaks on wording variants |

- **Function calling**
  - **Official Definition:** A pattern where an LLM emits a **structured tool choice and arguments**; the application **validates and runs** the call, then feeds **JSON results** back for the final answer.
  - **In Simple Words:** The model is the **coordinator**; your Python functions are the **workers**.
  - **Real-Life Example:** A hospital receptionist who routes you to **lab** or **billing** — they do not run the tests themselves.

**Critical rule:** The model **never** calls Open-Meteo or searches Chroma directly. It only **requests** a tool. **Your runtime** performs HTTP and retrieval.

![Function calling — the LLM chooses the tool and arguments; your Python runtime performs the real API or database work](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session24/session24-01-function-calling.png)

### Simple Activity — Route the Question

For each customer line, write which tool(s) should run — **policy**, **weather**, or **both**:

1. *"Can I return unopened earphones within seven days?"*
2. *"What is the temperature in Mumbai right now?"*
3. *"Express delivery to Delhi metro tomorrow — what does policy say, and is weather rough today?"*

**Expected direction:** (1) policy; (2) weather; (3) both.

---

## The Tool Execution Loop

Every tool-enabled agent follows the same cycle:

![Tool execution loop — user question through tool choice, Python execution, JSON result, and grounded final answer](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session24/session24-02-tool-execution-loop.png)

| Step | Who | What happens |
|---|---|---|
| 1 | **User** | Asks a ShopKart question |
| 2 | **Model** | Reads tool list and user message |
| 3 | **Model** | Returns **tool_calls** (zero, one, or many) OR a direct answer |
| 4 | **Runtime** | Parses tool name + JSON arguments |
| 5 | **Runtime** | Runs Python function — policy search or weather GET |
| 6 | **Tool** | Returns **JSON dict** — success data or structured error |
| 7 | **Runtime** | Appends **tool result messages** to conversation |
| 8 | **Model** | Reads tool JSON; may call more tools or finish |
| 9 | **User** | Sees one **grounded** natural-language reply |

**Contrast with the previous lab:** There, step 5 was **always** weather GET. Today step 3 **decides** the path.

**Integrated learning point:** Tool **descriptions** matter more than cryptic function names. Write *"Search ShopKart returns, shipping, warranty, and refund policy excerpts"* — not *"tool_a"*.

---

## Registering Tools — Schemas the Model Can Read

**Groq** (like other LLM APIs) accepts a **`tools`** list — each entry describes one callable function.

| Schema field | Purpose |
|---|---|
| **`name`** | Short identifier the model emits in **`tool_calls`** |
| **`description`** | When to use this tool — routing instructions for the model |
| **`parameters`** | JSON Schema for arguments — city name, coordinates, policy query |

- **Tool schema**
  - **Official Definition:** A machine-readable contract describing a tool's name, purpose, and expected inputs.
  - **In Simple Words:** The **label and form fields** on the concierge's routing sheet.
  - **Real-Life Example:** A Swiggy internal API doc saying *"Send `restaurant_id` — receive menu JSON"*.

![ShopKart agent with two registered tools — search_shopkart_policy and get_city_weather extend the assistant beyond chat alone](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session24/session24-03-shopkart-two-tools.png)

### Tool 1 — `search_shopkart_policy`

Returns grounded excerpts from the **same four policy areas** used across ShopKart RAG labs. This lab uses an **inline policy map** so the session focuses on **tool calling** — swap in your **Chroma retriever** from the **previous build** when extending the project.

| Policy area | Source text (abbreviated) |
|---|---|
| **Returns** | Unopened items: **7 calendar days**; opened/used not eligible unless defective |
| **Shipping** | Standard **3–5 business days**; express **1–2 days** in **metro cities only** |
| **Warranty** | Electronics: **12-month** manufacturer warranty; no liquid/physical damage |
| **Refunds** | **5–7 business days** after warehouse check; COD to UPI/bank only |

### Tool 2 — `get_city_weather`

Wraps the **Open-Meteo GET helper** from the **previous session** — status check, parse, extract **`temperature_c`** and **`weather_code`**.

**Common mistake:** Registering weather with no **latitude/longitude** in the schema — the model may pass a city name only. Include **city + coordinates** in parameters, or map cities in your Python function.

---

## Safe Tool Results — Errors Without Hallucination

Tools must return **honest JSON** when things fail:

| Situation | Tool JSON | Final answer should |
|---|---|---|
| Weather API **200** | `{ "city": "Delhi", "temperature_c": 34.2, ... }` | Cite live temperature |
| Weather API **non-200** | `{ "error": "Weather API failed", "status_code": 503 }` | Say weather **unavailable** — no invented rain |
| Policy query with **no match** | `{ "error": "No policy excerpt found", "query": "..." }` | Refuse or ask to rephrase |
| **Empty retrieval** | `{ "excerpts": [] }` | Do **not** invent refund rules |

**Link to evaluation work:** A confident answer with **`error` in tool JSON** is a **generation failure** — same discipline as RAG hallucination diagnosis.

---

## Project Setup

Create **`shopkart_tool_agent`**:

```
shopkart_tool_agent/
├── shopkart_tool_agent.py
└── .env                  # GROQ_API_KEY=your-key-here
```

Install:

```bash
pip install groq requests python-dotenv
```

Reuse **`GROQ_API_KEY`** from ShopKart RAG labs. Never commit **`.env`**.

---

## Full Lab Code — ShopKart Tool Agent

Save as **`shopkart_tool_agent.py`**:

```python
# shopkart_tool_agent.py — Groq function calling with policy + weather tools

import json  # Parse tool arguments and serialise tool results
import sys  # Exit on unrecoverable setup errors

import requests  # Weather tool HTTP GET
from dotenv import load_dotenv  # Load GROQ_API_KEY from .env
from groq import Groq  # LLM client with native tool calling support

# ── Configuration ───────────────────────────────────────────────────────────
GENERATION_MODEL = "llama-3.3-70b-versatile"  # Same model family as prior ShopKart labs
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"  # Free weather API from previous lab
REQUEST_TIMEOUT_SECONDS = 15  # Network timeout for weather GET

# Inline policy excerpts — same knowledge as ShopKart RAG; swap for Chroma retriever later
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

# Groq tool definitions — descriptions guide model routing
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_shopkart_policy",
            "description": (
                "Search ShopKart customer policy for returns, shipping, warranty, or refunds. "
                "Use when the question is about rules, timelines, or eligibility in policy documents."
            ),
            "parameters": {
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


def search_shopkart_policy(query: str) -> dict:
    """Return relevant policy excerpts as JSON — lightweight stand-in for RAG retrieval."""
    query_lower = query.lower()  # Case-insensitive keyword routing
    matched = []  # List of {category, text} dicts to return

    keyword_map = {
        "returns": ["return", "unopened", "opened", "eligible", "send back"],
        "shipping": ["shipping", "express", "delivery", "metro", "dispatch"],
        "warranty": ["warranty", "repair", "defect", "liquid", "water"],
        "refunds": ["refund", "cod", "upi", "money back", "credit"],
    }

    for category, keywords in keyword_map.items():  # Scan each policy area
        if any(word in query_lower for word in keywords):  # Any keyword hit counts
            matched.append({"category": category, "text": POLICY_SNIPPETS[category]})

    if not matched:  # No keyword hit — honest empty result
        return {"error": "No policy excerpt found", "query": query, "excerpts": []}

    return {"query": query, "excerpts": matched}  # Structured success payload


def get_city_weather(city_name: str, latitude: float, longitude: float) -> dict:
    """GET live weather — same pattern as previous session; return JSON either way."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code",
    }
    response = requests.get(OPEN_METEO_URL, params=params, timeout=REQUEST_TIMEOUT_SECONDS)

    if response.status_code != 200:  # Safe error JSON — never fake weather
        return {
            "error": "Weather API failed",
            "status_code": response.status_code,
            "city": city_name,
        }

    data = response.json()  # Parse success body
    current = data["current"]
    return {
        "city": city_name,
        "temperature_c": current["temperature_2m"],
        "weather_code": current["weather_code"],
        "latitude": latitude,
        "longitude": longitude,
    }


# Map tool names from model output to Python callables
TOOL_FUNCTIONS = {
    "search_shopkart_policy": search_shopkart_policy,
    "get_city_weather": get_city_weather,
}


def run_tool_agent(client: Groq, user_message: str) -> str:
    """Run model → tool loop until the model returns a final text answer."""
    messages = [
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

    response = client.chat.completions.create(
        model=GENERATION_MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",  # Let model decide whether to call tools
    )
    assistant_message = response.choices[0].message

    # Loop while the model requests tool executions
    while assistant_message.tool_calls:
        messages.append(assistant_message)  # Keep assistant tool_call message in history

        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name  # Which tool the model chose
            raw_arguments = tool_call.function.arguments  # JSON string of args
            arguments = json.loads(raw_arguments)  # Parse to Python dict

            if function_name not in TOOL_FUNCTIONS:  # Unknown tool guard
                result = {"error": f"Unknown tool: {function_name}"}
            else:
                result = TOOL_FUNCTIONS[function_name](**arguments)  # Execute Python tool

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,  # Must match the pending tool call
                    "content": json.dumps(result),  # Tool result back to model as JSON text
                }
            )

        response = client.chat.completions.create(
            model=GENERATION_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        assistant_message = response.choices[0].message

    return assistant_message.content.strip()  # Final customer-facing answer


def main():
    load_dotenv()  # Read GROQ_API_KEY
    client = Groq()

    demo_queries = [
        "Can I return unopened earphones within seven days?",
        "I chose express delivery to Delhi metro tomorrow. What does policy say about express timing, and is current weather likely to affect courier handoff today?",
    ]

    for user_message in demo_queries:
        print("\n" + "=" * 72)
        print("Customer:", user_message)
        print("=" * 72)
        answer = run_tool_agent(client, user_message)
        print("\nFinal answer:")
        print(answer)


if __name__ == "__main__":
    main()
```

Run:

```bash
cd shopkart_tool_agent
python shopkart_tool_agent.py
```

**How the code works:**

- **`TOOLS`** — JSON schemas the model reads to **route** policy vs weather questions.
- **`search_shopkart_policy`** — returns **`excerpts`** or structured **`error`** — never silent failure.
- **`get_city_weather`** — reuses **status-before-parse** from the **previous** lab; errors return JSON, not crashes.
- **`run_tool_agent`** — **`while assistant_message.tool_calls`** implements the **execution loop**.
- **`role: tool`** messages carry **`json.dumps(result)`** back to the model for the **final synthesis**.

### Terminal Verification Checklist

| Demo query | Tools expected | Answer must |
|---|---|---|
| Unopened earphones return | **Policy only** | Mention **7 days** from excerpts — no invented weather |
| Express Delhi + weather | **Policy + weather** | Cite **metro express 1–2 days** **and** live **temperature** |
| Tool error drill | Break weather URL once | Say weather **unavailable** — not fake rain |

### Simple Activity — Trace One Combined Query

For the **express + Delhi weather** demo query, sketch on paper:

1. Which **`tool_calls`** names appear?
2. What JSON keys come back from each tool?
3. Which numbers in the **final answer** must match tool JSON exactly?

---

## Connecting APIs as Tools

External tools — weather APIs today, order systems tomorrow — all follow the **previous session's pattern** inside a Python wrapper:

**GET → status check → parse JSON → return small dict**

The agent sees only the **wrapper result**, not raw HTTP. That is how **connecting APIs and tools** scales: one function per external capability, one JSON shape per tool.

![Session 23 weather GET wrapped as get_city_weather tool — status check, parse JSON, return fields to the model](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session24/session24-04-api-as-tool-wrapper.png)

**Extension path:** Replace **`search_shopkart_policy`** with your **Chroma + BGE retriever** from the **previous build** — keep the **same tool name and JSON shape** so the agent loop unchanged.

---

## Module 2 Close — Full Agentic Trace

Trace one **combined** question end to end:

| Stage | Component | Output |
|---|---|---|
| **Input** | Customer question | Express + weather wording |
| **Decision** | Groq **function calling** | Two **`tool_calls`** |
| **Action 1** | **`search_shopkart_policy`** | Shipping excerpt JSON |
| **Action 2** | **`get_city_weather`** | Live temperature JSON |
| **Synthesis** | Groq final message | Policy + weather in plain English |
| **Quality check** | You read terminal | Numbers match tool JSON |

This closes **Module 2**: **memory concepts**, **databases**, **vector search**, **RAG build and evaluation**, **APIs/JSON**, and **tool integration**.

**Upcoming module preview:** **LangChain** **`AgentExecutor`** automates the same loop you wrote manually today — with **retriever tools**, **memory**, and richer workflows.

---

## Key Takeaways

- **Function calling** lets the **model choose tools**; your **runtime executes** them — the model does not call HTTP directly.
- **Clear tool descriptions** and **JSON schemas** route policy vs weather questions better than hard-coded branches.
- The **tool loop** — **propose → execute → return JSON → reply** — is the core pattern of actionable agents.
- **Structured errors** in tool JSON prevent **invented weather or policy** when APIs or retrieval fail.
- **Combined ShopKart answers** merge **policy excerpts and live weather** only from **tool results** — the same grounding discipline as RAG evaluation.
- **Upcoming:** **LangChain** wraps this loop; you already understand what happens **under the hood**.

---

## Important Commands, Libraries, and Terminologies used

| Term / Command | Meaning in one line |
|---|---|
| **Function calling** | Model emits tool name + args; Python runs the function |
| **Tool schema** | Name, description, and parameter JSON Schema for routing |
| **`tools=`** | Groq parameter listing registered callable tools |
| **`tool_choice="auto"`** | Model decides whether and which tools to call |
| **`tool_calls`** | Structured tool requests on the assistant message |
| **`role: tool`** | Message carrying JSON tool result back to the model |
| **`tool_call_id`** | Links each tool result to its pending request |
| **`TOOL_FUNCTIONS`** | Python dict mapping tool names to callables |
| **`search_shopkart_policy`** | Returns policy excerpt JSON — RAG stand-in in this lab |
| **`get_city_weather`** | Wraps Open-Meteo GET from previous session |
| **`run_tool_agent`** | Manual tool execution loop until final text answer |
| **`json.loads` / `json.dumps`** | Parse model tool args; serialise tool results |
| **`requests.get`** | HTTP GET inside weather tool wrapper |
| **Agent runtime** | Your script registering and executing tools |
| **Groq / `.env`** | Same LLM stack as ShopKart RAG labs |
