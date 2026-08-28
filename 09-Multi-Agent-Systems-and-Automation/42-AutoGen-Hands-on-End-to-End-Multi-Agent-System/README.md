# AutoGen: Hands-on — End-to-End Multi-Agent System

## Context of This Session

In the **previous** session you built a **CrewAI** production workflow: **custom tools**, **process** choice, optional **memory**, a validation checklist, and **iteration** on one weak prompt. Crews shine when research, write, and review are **tickets**.

This session is a **new product**, not a sequel to that story. You will build a **Hotel Guest Complaint Intake Desk** in **AutoGen**: a guest message arrives, specialists **intake**, **classify**, **look up** the stay, **create a ticket**, and **stop**. The conversable pair (clerk + desk runner) lives **inside** a chaired GroupChat.

**In this session, you will:**

- **Configure** intake, classifier, clerk, and desk-runner seats with non-overlapping system messages
- **Register** stay-lookup and ticket tools with caller ≠ executor
- **Run** a **GroupChat** with speaker selection and max rounds
- **Read** traces and apply one configuration fix

---

## Why AutoGen for a Front-Office Desk

Connecting sentence: A weekly crew is the wrong shape for “AC not cooling in 412 — raise a ticket now.”

- **Official Definition:** The **conversable-agent model** is AutoGen’s pattern: agents send and receive messages until a **termination** condition fires.
- **In Simple Words:** A designed work chat, not folders on a conveyor.
- **Real-Life Example:** Reception WhatsApp buries the trail. A chatbot invents booking ids. An **intake desk** listens, sorts, checks the stay, and stamps a case id.

![Hotel front desk: guest complaint incoming versus a labelled AutoGen intake desk that files a tracked ticket](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session42/session42-01-from-crew-to-autogen-desk.png)

**Need:** One mega-agent hides who invented the room number. Split seats keep the **trace** auditable.

**Common doubt:** *“Does AutoGen replace CrewAI?”* — No. Crews remain strong for fixed handoffs. AutoGen shines for **interactive intake** with tools and a chair.

| Guest message | Expected path |
|---|---|
| `"AC not cooling in room 412, booking BK-7781"` | Classify `room_comfort` → lookup stay → create ticket |
| `"Something is wrong with my stay"` | Intake asks for booking id / clearer details |
| `"Wrong spa charge of 2500, BK-9002"` | Classify `billing` → lookup → ticket |

The same pattern appears in e-commerce returns and HR helpdesks. This lab uses a hotel so roles stay easy to picture.

---

## Seats, Tools, and the Stop Stamp

Connecting sentence: The desk needs job titles, access cards, and a meeting alarm **before** code.

- **Official Definition:** An **AssistantAgent** is an LLM specialist that plans and may **suggest** tools. A **UserProxyAgent** starts the case and may **execute** registered functions.
- **In Simple Words:** Experts think. The desk runner presses approved buttons.
- **Real-Life Example:** The clerk may request `lookup_guest_stay`. Only the desk runner runs it.

| Seat | AutoGen class | Must do | Must not do |
|---|---|---|---|
| IntakeAgent | AssistantAgent | Ask for booking / room if missing | Guess BK-ids; create tickets |
| ClassifierAgent | AssistantAgent | Tag `room_comfort`, `housekeeping`, `billing`, `dining`, `unclear` | Lookup stays; invent categories |
| DeskClerkAgent | AssistantAgent | Suggest tools; write the confirmation | Execute tools; skip lookup |
| HotelDeskRunner | UserProxyAgent | Run registered functions; start the chat | Invent ticket ids |

**Tools (local fake PMS — property management system):**

| Tool | Returns | Safe failure |
|---|---|---|
| `lookup_guest_stay(booking_id)` | Guest, room, dates | `STAY_NOT_FOUND` |
| `create_complaint_ticket(category, summary, room)` | Ticket id e.g. `HT-ROOM-412` | Never invent an id without the tool |

**Stop stamp:** After a successful ticket, the clerk’s last line is `TICKET_CREATED:` plus `TERMINATE`. Vague complaints never get a fake ticket.

```text
Guest complaint
   → IntakeAgent (clarify if needed)
   → ClassifierAgent (tag category)
   → DeskClerkAgent suggests tools → HotelDeskRunner executes
   → Clerk confirmation → TERMINATE
```

![Tech stack for the hotel desk: AutoGen classes, register_function, GroupChatManager, and Groq or OpenAI behind llm_config](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session42/session42-02-pair-tech-stack.png)

### Activity — Predict the Hand-off

For `"Towels not replaced in room 208, booking BK-3301"`, write expected category, next speaker after classify, and first tool.

**Suggested answers:** `housekeeping` → DeskClerkAgent → `lookup_guest_stay`

### Activity — Spot the Role Leak

Which system message is wrong and why? “ClassifierAgent may also create tickets if the guest sounds angry.”

**Suggested answer:** Category and ticket creation must stay separate so audits remain clear.

Connecting sentence: Those seats only work if tools, the chair, and the stop phrase are named as clearly as the job titles.

- **Official Definition:** `register_function` wires a Python helper so a **caller** may suggest it and an **executor** may run it.
- **In Simple Words:** An access card for one button. The clerk points; the desk runner presses.
- **Real-Life Example:** Reception may *request* a PMS lookup. Only the authorised clerk terminal *runs* it.

- **Official Definition:** A **termination condition** ends the chat when a phrase appears or a turn cap is hit.
- **In Simple Words:** The meeting stops when the stamp is real, or when the alarm rings.
- **Real-Life Example:** `TICKET_CREATED:` plus `TERMINATE` is the planned close. `max_round=12` is the fire alarm.

- **Official Definition:** **GroupChat** is the shared message list every specialist writes into.
- **In Simple Words:** One notepad for the whole desk.
- **Real-Life Example:** Intake, classifier, and clerk do not keep private chats. The auditor reads one thread.

- **Official Definition:** **GroupChatManager** is the coordinator that applies speaker rules to that list.
- **In Simple Words:** The chairperson of the room.
- **Real-Life Example:** The manager does not clean rooms. It only decides who speaks next.

- **Official Definition:** **Speaker selection** chooses which agent talks on the next turn.
- **In Simple Words:** The chair calls the right person.
- **Real-Life Example:** After a tool-call payload, the next speaker must be **HotelDeskRunner**, not ClassifierAgent.

- **Official Definition:** **Max rounds** is a hard cap on turns in the GroupChat.
- **In Simple Words:** The meeting alarm.
- **Real-Life Example:** `max_round=12` stops polite loops. It is a fuse, not the planned close.

- **Official Definition:** `human_input_mode="NEVER"` runs the proxy without typing between turns.
- **In Simple Words:** The lab is automatic so you can read the trace, not pause for a human.
- **Real-Life Example:** A Zoom demo should not wait for you to press Enter after every tool.

**Need:** If the chair never returns the desk, tools stay as text and the ticket id is invented.

**Common doubt:** *“Can one AssistantAgent be caller and executor?”* — Not in this lab. The split is the audit.

---

## Setup and `llm_config` (Groq or OpenAI)

Connecting sentence: The same desk should run on the key you already have.

```bash
pip install "ag2[openai]"
export GROQ_API_KEY="your_key"
# or: export OPENAI_API_KEY="your_key"
# optional: export LLM_MODEL="llama-3.3-70b-versatile"
```

`ag2` is the maintained AutoGen family. It still exposes `AssistantAgent`, `UserProxyAgent`, `GroupChat`, and `GroupChatManager`.

The script below reads `LLM_API_KEY`, then `GROQ_API_KEY`, then `OPENAI_API_KEY`. Set `LLM_API_TYPE=groq` (and usually `LLM_MODEL`) when the key is Groq. Never paste keys into notebooks you share.

If the key is missing, agents cannot call the model. That is a setup failure, not an AutoGen bug.

---

## Build the Full Desk

Connecting sentence: One file is the product: seats, tools, chair, three demos.

```python
# Operating-system helpers for API keys
import os  # Read environment variables

# AutoGen building blocks for the hotel desk
from autogen import (  # Core symbols used below
    AssistantAgent,  # Specialist LLM agent
    UserProxyAgent,  # Starter + tool executor
    GroupChat,  # Shared conversation room
    GroupChatManager,  # Chairperson for the room
    register_function,  # Safe tool wiring helper
)


def build_llm_config():  # Shared Groq / OpenAI config for all specialists
    """Build llm_config from Groq or OpenAI env vars."""
    # Prefer a generic key name, then Groq, then OpenAI
    api_key = (  # First non-empty key wins
        os.getenv("LLM_API_KEY")  # Optional generic name
        or os.getenv("GROQ_API_KEY")  # Groq
        or os.getenv("OPENAI_API_KEY")  # OpenAI
    )
    if not api_key:  # Fail fast with a clear message
        raise RuntimeError(  # Setup error, not an AutoGen bug
            "Set LLM_API_KEY, GROQ_API_KEY, or OPENAI_API_KEY."
        )
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")  # Override with LLM_MODEL
    config = {  # One config list item
        "model": model,  # Chat-completions model id
        "api_key": api_key,  # Secret from the environment
    }
    api_type = os.getenv("LLM_API_TYPE", "").strip().lower()  # Optional provider
    if api_type:  # e.g. groq
        config["api_type"] = api_type  # Provider hint for the client
    return {"config_list": [config], "temperature": 0}  # Stable lab replies


llm_config = build_llm_config()  # Shared by all AssistantAgents

# Fake hotel stay register keyed by booking id
HOTEL_STAYS = {  # Local stand-in for a PMS
    "BK-7781": {  # AC / room comfort demo
        "guest": "Rohit Sharma",  # Guest name
        "room": "412",  # Room number
        "check_in": "2026-04-10",  # Stay start
        "check_out": "2026-04-13",  # Stay end
    },
    "BK-9002": {  # Billing / spa demo
        "guest": "Anita Desai",  # Guest name
        "room": "918",  # Room number
        "check_in": "2026-04-11",  # Stay start
        "check_out": "2026-04-14",  # Stay end
    },
    "BK-3301": {  # Housekeeping demo
        "guest": "Vikram Rao",  # Guest name
        "room": "208",  # Room number
        "check_in": "2026-04-09",  # Stay start
        "check_out": "2026-04-12",  # Stay end
    },
}


def lookup_guest_stay(booking_id: str) -> str:  # Tool: stay lookup
    """Return stay facts or STAY_NOT_FOUND. Never invent a stay."""
    bid = (booking_id or "").strip().upper()  # Normalise the id
    row = HOTEL_STAYS.get(bid)  # None if unknown
    if not row:  # Honest miss
        return f"STAY_NOT_FOUND: {bid}"  # Safe failure
    return (  # Compact stay line
        f"STAY {bid}: guest={row['guest']}; room={row['room']}; "
        f"dates={row['check_in']} to {row['check_out']}"
    )


def create_complaint_ticket(category: str, summary: str, room: str) -> str:  # Tool: ticket stamp
    """Issue a ticket id from category + room. Do not call without a lookup."""
    prefix = (category or "general").strip().upper().replace(" ", "-")[:12]  # Ticket prefix from category
    room_part = (room or "000").strip()  # Room from the stay row
    return f"TICKET_CREATED: HT-{prefix}-{room_part}"  # Visible stamp


# Intake: clarify only — no tools, no tickets
intake = AssistantAgent(
    name="IntakeAgent",  # Unique speaker name
    llm_config=llm_config,  # Shared model config
    system_message=(  # Clarify missing booking or room
        "You are hotel intake. If booking id or room is missing, ask one "
        "short question. Do not classify. Do not invent BK-ids. Do not "
        "create tickets. If details are enough, say INTAKE_READY."
    ),
)

# Classifier: category only
classifier = AssistantAgent(
    name="ClassifierAgent",  # Unique speaker name
    llm_config=llm_config,  # Shared model config
    system_message=(  # Closed category list
        "You classify guest complaints. Reply with one tag: room_comfort, "
        "housekeeping, billing, dining, or unclear. No tools. No tickets."
    ),
)

# Clerk: suggest tools and write the confirmation
clerk = AssistantAgent(
    name="DeskClerkAgent",  # Unique speaker name
    llm_config=llm_config,  # Shared model config
    system_message=(  # Suggest tools; never execute them
        "You are the hotel desk clerk. Suggest lookup_guest_stay, then "
        "create_complaint_ticket. Never invent a ticket id. After a real "
        "TICKET_CREATED line, write one guest-facing confirmation and end "
        "with TERMINATE. If intake is still asking, wait."
    ),
)

# Desk runner: start the chat and execute tools
desk = UserProxyAgent(
    name="HotelDeskRunner",  # Executor name used in speaker rules
    human_input_mode="NEVER",  # Unattended lab
    code_execution_config=False,  # Tools only, no shell
    max_consecutive_auto_reply=8,  # Cap executor chatter
    is_termination_msg=lambda m: "TERMINATE" in (m.get("content") or ""),  # Desk stops on stamp
    llm_config=False,  # No LLM on the executor
    system_message="Execute registered hotel tools. Do not invent ids.",
)

# Caller = clerk; executor = desk. Never reverse.
register_function(
    lookup_guest_stay,  # Stay lookup
    caller=clerk,  # May suggest
    executor=desk,  # May run
    name="lookup_guest_stay",  # Tool name in the chat
    description="Look up a hotel stay by booking id. Returns STAY or STAY_NOT_FOUND.",
)
register_function(
    create_complaint_ticket,  # Ticket stamp
    caller=clerk,  # May suggest
    executor=desk,  # May run
    name="create_complaint_ticket",  # Tool name in the chat
    description="Create a complaint ticket. Use only after a successful stay lookup.",
)


def hotel_speaker_select(last_speaker, groupchat):  # Chair: who speaks next
    """Open at intake; route tool calls to the desk; send tool results to the clerk."""
    last = groupchat.messages[-1] if groupchat.messages else {}  # Last turn
    content = (last.get("content") or "") if isinstance(last, dict) else ""  # Text of last turn
    # Tool-call payloads must run on the executor, not another specialist
    if "function_call" in str(last) or "tool_call" in str(last).lower():  # Suggested tool must execute
        return desk  # HotelDeskRunner executes
    if last_speaker is desk:  # Opening complaint vs tool result
        if any(s in content for s in ("STAY ", "STAY_NOT_FOUND", "TICKET_CREATED")):  # Tool result text
            return clerk  # Interpret tool output
        return intake  # Guest text goes to intake first
    if last_speaker is intake:  # After intake, classifier tags
        if "INTAKE_READY" in content:  # Details enough to classify
            return classifier
        return intake  # Still clarifying
    if last_speaker is classifier:  # After a tag, clerk owns tools
        return clerk
    return clerk  # Default: clerk drives the case


groupchat = GroupChat(
    agents=[desk, intake, classifier, clerk],  # One shared notepad
    messages=[],  # Fresh thread per demo
    max_round=12,  # Meeting alarm
    speaker_selection_method=hotel_speaker_select,  # Custom chair
)

manager = GroupChatManager(
    groupchat=groupchat,  # Same room
    llm_config=llm_config,  # Manager may use the model
    is_termination_msg=lambda m: "TERMINATE" in (m.get("content") or ""),  # Manager stops on stamp
)


def run_hotel_desk(complaint: str) -> None:  # One isolated demo
    """Reset the shared notepad, then start one guest complaint."""
    groupchat.messages = []  # Do not leak demo 1 into demo 2
    print("\n" + "=" * 64)  # Banner
    print("GUEST:", complaint)  # The incoming message
    print("=" * 64)  # Banner
    desk.initiate_chat(manager, message=complaint, max_turns=12)  # Start the chaired room


if __name__ == "__main__":  # Run three isolated demos
    run_hotel_desk("AC not cooling in room 412, booking BK-7781")  # Happy path
    run_hotel_desk("Something is wrong with my stay")  # Clarify path
    run_hotel_desk("Wrong spa charge of 2500 on my bill, booking BK-9002")  # Billing path
```

Save as `hotel_desk.py`. Run: `python hotel_desk.py`.

**How the code works**

- `build_llm_config` picks **Groq** or **OpenAI** from the environment so the desk is not locked to one vendor.
- Four seats share one `GroupChat`. Intake clarifies. Classifier tags. Clerk suggests tools. **HotelDeskRunner** executes them.
- `register_function` sets **caller = clerk** and **executor = desk**. Reversing that split lets a specialist invent a stamp.
- `hotel_speaker_select` sends the opening complaint to intake, tool-call turns to the desk, and tool results to the clerk.
- `run_hotel_desk` clears `groupchat.messages` so demo 2 cannot inherit room 412 from demo 1.
- The planned close is `TICKET_CREATED:` plus `TERMINATE`. `max_round=12` is only a fuse.

![Conversable loop: clerk suggests a tool, desk runner executes, result returns until TERMINATE](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session42/session42-03-pair-data-flow.png)

---

## What This End-to-End System Implements

Connecting sentence: If a demo cannot show this table, the lab is incomplete.

| Piece | What the guest / auditor sees |
|---|---|
| Intake | One clarify question when booking or room is missing — not a fake ticket |
| Classify | One tag from the closed list |
| Tools | `lookup_guest_stay` then `create_complaint_ticket`; `STAY_NOT_FOUND` if the id is wrong |
| Orchestration | Named speakers; tool calls routed to **HotelDeskRunner** |
| Close | `TICKET_CREATED:` plus `TERMINATE` on a complete case |
| Isolation | `groupchat.messages = []` so demo 2 does not inherit demo 1 |

**Happy path (demo 1):** BK-7781 → `room_comfort` → stay facts → `HT-ROOM-412` (or similar) → guest-facing line → stop.

**Clarify path (demo 2):** No booking id → intake asks → **no** invented ticket.

**Billing path (demo 3):** BK-9002 → `billing` → stay for room 918 → ticket → stop.

**Need:** `max_round=12` is a fuse, not the plan. The plan is `TERMINATE` after a real stamp.

![GroupChat: Intake, Classifier, and Clerk under a manager; tool calls route to the desk runner](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session42/session42-04-groupchat-orchestration.png)

---

## AutoGen vs n8n / make.com

Connecting sentence: Students often ask why not draw the same desk in a no-code builder.

| | AutoGen (this lab) | n8n / make.com |
|---|---|---|
| Shape | Named agents, tools, chair, traces | Boxes, routers, retries |
| Strength | Ambiguous guest text; speaker policy | SaaS glue; logs; non-engineers |
| Weakness | Needs a key, traces, prompt care | Weak at multi-turn “who speaks” |
| Fit | Interactive intake + tools | Nightly syncs, webhooks, CRMs |

**Need:** AutoGen does not replace a workflow SaaS. Use AutoGen when the hard part is **dialogue and seats**. Use n8n/make.com when the hard part is **integrations**. Many products use both.

**Common doubt:** *“Is AutoGen production?”* — Treat this desk as a **correct lab product**. Production still needs auth, a real PMS, and human override.

---

## Read the Trace; Fix One Failure

Connecting sentence: A green exit code is not a passing desk.

**Read in order:** (1) Did IntakeAgent speak when details were thin? (2) Did ClassifierAgent emit one allowed tag? (3) Did **HotelDeskRunner** run tools — not the clerk? (4) Is there `TICKET_CREATED:` and `TERMINATE` on complete cases? (5) Did demo 2 invent a booking?

| Failure | Likely cause | One config fix |
|---|---|---|
| Tools never run | Speaker never returns the desk | Route `function_call` / `tool_call` to HotelDeskRunner |
| Ticket with no stay line | Clerk skipped lookup | System message: lookup before create |
| Demo 2 gets a fake ticket | Clerk spoke first; intake skipped | After the desk opening, return IntakeAgent |
| Chat hits round 12 | Weak `TERMINATE` | Require stamp + TERMINATE; keep max_round as fuse |
| Demo 2 mentions 412 | Shared `messages` | Reset `groupchat.messages` before each run |

### Activity — Trace Audit

Paste a 12-turn log. Mark the first turn tools should have run but a specialist spoke instead. Name the speaker-function change.

**Suggested answer:** After a tool-call payload, return **HotelDeskRunner**, not IntakeAgent.

### Activity — Isolation Check

If demo 3 cites room 412 from demo 1, what line did you skip?

**Suggested answer:** `groupchat.messages = []` at the start of `run_hotel_desk`.

---

## Recap

Connecting sentence: One hotel desk is the whole session — not a pair lab plus a later group lab.

You configured **non-overlapping seats**, registered **lookup** and **ticket** with **caller ≠ executor**, ran a **GroupChat** with a **speaker function** and **max rounds**, and treated **traces** as the test. **Groq** or **OpenAI** is only `llm_config`. **CrewAI** remains the ticket-shaped crew from the previous session; this session is a **different product** for live guest intake.

**Need:** If the trace has no `TICKET_CREATED:` on a complete complaint, do not call the desk done.

---

## Knowledge Check

**Question 1**

Why may IntakeAgent not call `create_complaint_ticket`?

A. AutoGen forbids assistants from seeing tools  
B. Tickets must stay on the clerk + desk-runner path so the audit stays clear  
C. GroupChat cannot mix AssistantAgent and UserProxyAgent  
D. Groq keys cannot register functions  

**Correct answer:** B

**Explanation:** Split seats keep category, stay facts, and stamps on different speakers.

**Question 2**

A tool-call payload appears and ClassifierAgent speaks next. What is the first fix?

A. Delete GroupChatManager  
B. Return HotelDeskRunner from the speaker function on tool-call turns  
C. Set temperature to 1  
D. Remove `lookup_guest_stay`  

**Correct answer:** B

**Explanation:** Suggested tools must reach the executor.

**Question 3**

Demo 2 (`"Something is wrong with my stay"`) prints `TICKET_CREATED` with no booking id. What failed?

A. `max_round` was too high  
B. Intake did not block a stamp without a stay  
C. OpenAI is required  
D. `register_function` was used twice  

**Correct answer:** B

**Explanation:** Vague complaints must clarify, not invent tickets.

---

## Key Takeaways

- AutoGen is a **conversable team** with tools and a chair — the right shape for live guest intake
- **Caller ≠ executor** keeps stay facts and ticket stamps honest
- **Speaker selection** plus **max rounds** stop polite loops; `TERMINATE` is the planned close
- The **trace** is the test: names, tools, stamp, and isolation across demos
- **CrewAI** stays the ticket-shaped crew from the **previous** session; this hotel desk is a **new** product, not a sequel

**Upcoming** work draws similar workflows as **graphs** (nodes and edges) instead of a chat chair. Seats, tools, stop rules, and traces here remain the foundation.

---

## Important Commands, Libraries, Terminologies

| Name | What it is in this lab |
|---|---|
| `ag2` / `autogen` | Package family that exposes AutoGen agent and GroupChat classes |
| `AssistantAgent` | LLM specialist: intake, classifier, or clerk |
| `UserProxyAgent` | **HotelDeskRunner** — starts the case and executes tools |
| `register_function` | Wires a tool with caller ≠ executor |
| `GroupChat` / `GroupChatManager` | Shared notepad and chairperson |
| Speaker selection / `max_round` | Who speaks next / meeting alarm |
| `lookup_guest_stay` | Fake PMS lookup; may return `STAY_NOT_FOUND` |
| `create_complaint_ticket` | Issues a visible `TICKET_CREATED:` stamp |
| `llm_config` | Groq or OpenAI from environment keys |
| Conversation trace | Ordered speakers, tool results, and stop phrase |