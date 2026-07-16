# lecture30.py — LangChain MEMORY on agents: chat_history, manual append, and RunnableWithMessageHistory (Session 30)
#
# In Session 29 you built a tool-calling AGENT with AgentExecutor: create_tool_calling_agent
# made the decision layer, the executor ran a BOUNDED loop (max_iterations), and you used a
# MessagesPlaceholder for agent_scratchpad. But that scratchpad only holds TOOL STEPS FOR THE
# CURRENT RUN — it forgets everything the moment invoke() returns. So each call was still
# STATELESS: ask "My order ID is ORD102" then "What is the status of it?" and the second call
# has no idea what "it" means.
#
# Today the same agent gains CONVERSATIONAL MEMORY. You add a SECOND placeholder — chat_history
# — that carries prior user<->assistant turns INTO each new invoke. Now follow-ups work:
#
#       Turn 1: "My order ID is ORD102."       -> agent notes the ID
#       Turn 2: "What is the status of it?"     -> agent resolves "it" = ORD102, calls the tool
#
# Clinic-file analogy: a stateless call is a new clerk who asks your order number every time;
# conversational memory is a clinic reception file — each visit adds a line and the doctor reads
# the WHOLE file, not just your latest sentence. You are not building a plain chatbot: you are
# building an agent with TOOLS *and* MEMORY.
#
# Two placeholders, two different jobs (the distinction everyone misses):
#   agent_scratchpad -> tool steps for the CURRENT run       (filled by AgentExecutor)
#   chat_history     -> past user/AI turns ACROSS invocations (filled by YOU, or an auto wrapper)
#
# What this file demonstrates (one script, five escalating stages):
#   STAGE 1 — LOAD CONFIG from .env and build a tool-capable ChatOllama
#   STAGE 2 — PROMPT with TWO placeholders (chat_history + agent_scratchpad) + one status tool
#   STAGE 3 — MANUAL chat_history: multi-turn demo, append human THEN ai after every invoke
#   STAGE 4 — STATELESS baseline: same agent, always pass [], never append -> follow-ups fail
#   STAGE 5 — AUTOMATIC history: RunnableWithMessageHistory + session-scoped in-memory stores
#
# PREREQUISITES (do these in the terminal BEFORE running this file):
#   python3 -m venv venv && source venv/bin/activate     # (Windows: venv\Scripts\activate)
#   pip install -U pip langchain langchain-core langchain-ollama python-dotenv
#   ollama pull llama3.1          # IMPORTANT: use a model that supports TOOL CALLING well
# Tiny models (qwen2.5:0.5b from Sessions 25-27) chat fine but are UNRELIABLE at tool calls.
# Create a .env next to this file (do NOT commit it) with:
#   OLLAMA_MODEL=llama3.1
#   OLLAMA_HOST=http://localhost:11434
#   OLLAMA_TEMPERATURE=0          # temperature 0 = deterministic tool selection while testing
# The Ollama app/service must be RUNNING (localhost:11434) or you get "connection refused".

# Standard library — read configuration from the environment after .env is loaded.
import os  # os.environ.get(...) pulls values that load_dotenv() placed there

# python-dotenv — bridges a .env file on disk into os.environ at runtime.
from dotenv import load_dotenv  # Reads key=value pairs from .env so settings stay out of code

# LangChain Core — the tool decorator, prompt helpers, message classes, and history store.
from langchain_core.tools import tool  # @tool converts a Python function into a LangChain tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # prompt + placeholders
from langchain_core.messages import HumanMessage, AIMessage  # typed messages for manual append

# typing.Optional lets the tool accept a MISSING order id without crashing on validation.
from typing import Optional  # order_id may be None when the model calls the tool with no id yet
from langchain_core.chat_history import InMemoryChatMessageHistory  # per-session RAM history store
from langchain_core.runnables.history import RunnableWithMessageHistory  # auto history wrapper

# LangChain agents — the decision-layer builder and the runtime that executes the loop.
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent  # agent + its manager

# Provider package — the LangChain wrapper that makes Ollama look like a chat model.
from langchain_ollama import ChatOllama  # ChatOllama is a Runnable bound to your Ollama server

# ---------------------------------------------------------------------------
# STAGE 1 — CONFIGURATION FROM .env (same secure pattern as Sessions 27-29)
# ---------------------------------------------------------------------------
# load_dotenv() MUST run BEFORE any os.environ.get(...) below, or the values are missing and
# the defaults silently take over. Settings live in .env, never in the .py file.
load_dotenv()  # Make OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_TEMPERATURE available via os.environ

MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3.1")  # Tag from "ollama list", tool-capable
BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")  # Where Ollama listens
# Temperature arrives as a STRING from .env, so float() converts it. 0 = stable tool selection.
TEMPERATURE = float(os.environ.get("OLLAMA_TEMPERATURE", "0"))  # Deterministic during testing


# ===========================================================================
# STAGE 2 — ONE STATUS TOOL + A PROMPT WITH TWO PLACEHOLDERS
# ===========================================================================
# We continue the e-commerce support idea from Session 29, but trim to a single focused tool so
# the spotlight stays on MEMORY, not tool routing. The prompt now has TWO MessagesPlaceholders:
# chat_history (past turns) and agent_scratchpad (current-run tool steps).

# A small in-memory dict stands in for a real orders database (RAM-only, like the tool demos).
ORDERS = {  # order_id -> record
    "ORD101": {"status": "shipped"},  # sample shipped order from earlier demos
    "ORD102": {"status": "delivered"},  # sample cancelled order from earlier demos
}


@tool  # Register this function as a LangChain tool the agent can request.
def get_order_status(order_id: Optional[str] = None) -> str:  # ID (or None) in, a status string out
    """Use when the user asks for order status or tracking of a specific order ID."""  # WHEN to use
    # A tool-calling model may invoke this with NO id (e.g. "What is my order ID?"). Pydantic would
    # reject None for a required str BEFORE our logic runs, so we accept Optional[str] and guard here.
    if not order_id:  # None or empty -> the model called us without an id to look up
        return "No order ID provided. Please share your order ID (e.g. ORD101) so I can check it."
    order = ORDERS.get(order_id)  # Safe lookup — returns None for an unknown id
    if not order:  # Handle the not-found case INSIDE the tool, never crash
        return f"Order with ID {order_id} not found."  # Clear, model-readable message
    return f"Order status for {order_id} is {order['status']}."  # Status for a valid order


# One tool list, reused by the agent AND the executor so they can never drift apart.
tools = [get_order_status]  # The (single) tool menu for this memory-focused demo


# The prompt has FOUR layers. The ORDER matters: system rules, then rolling history, then the
# current human input, then the scratchpad for this run's tool steps.
prompt = ChatPromptTemplate.from_messages([
    ("system", (  # behaviour boundaries for the support assistant
        "You are a helpful customer support agent. "
        "If the user gives an order ID, remember it for this conversation. "
        "For follow-ups like 'track it' or 'what is the status of it', use the order ID "
        "from chat history. Use tools when order status is required. "
        "If no order ID is available, ask politely for it."
    )),
    # chat_history is a reserved SLOT for past user<->AI turns. optional=True lets turn 1 run
    # with an EMPTY history without raising an error. The placeholder does NOT store anything
    # itself — it only marks WHERE the history list will be injected at invoke() time.
    MessagesPlaceholder(variable_name="chat_history", optional=True),  # rolling conversation memory
    ("human", "{input}"),  # the current user message is injected here each turn
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # AgentExecutor fills this per run
])


def build_agent_executor() -> AgentExecutor:
    """Create the model, the tool-calling agent, and a bounded, recoverable AgentExecutor.

    Same safety ideas as Session 29: max_iterations caps the loop, handle_parsing_errors keeps
    a bad parse from crashing. Memory is added via the PROMPT (chat_history), not the executor.
    """
    llm = ChatOllama(
        model=MODEL_NAME,  # Tool-capable tag from OLLAMA_MODEL
        base_url=BASE_URL,  # Host from OLLAMA_HOST
        temperature=TEMPERATURE,  # 0 from OLLAMA_TEMPERATURE = deterministic selection
    )
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)  # decision layer
    agent_executor = AgentExecutor(
        agent=agent,  # the decision layer we just built
        tools=tools,  # the SAME tool list
        verbose=False,  # stream internal execution logs for tracing
        max_iterations=1,  # keep the bounded-loop idea from Session 29
        handle_parsing_errors=True,  # a parsing hiccup becomes recoverable, not a crash
    )
    return agent_executor


# ===========================================================================
# STAGE 3 — MANUAL chat_history: pass the list in, then append after each turn
# ===========================================================================
# chat_history is just a Python list YOU own. The placeholder only says WHERE it goes; filling
# and updating it is your job. The rule that makes follow-ups work:
#   1) pass chat_history on EVERY invoke (or the slot is empty)
#   2) after invoke, append HUMAN first, then AI (user speaks, then the assistant replies)
# Miss step 2 and you hit the classic bug: the app runs, but turn 2 still asks for the order ID.

def demo_manual_memory() -> None:
    """Run a two-turn conversation where turn 2 depends on the order ID given in turn 1."""
    agent_executor = build_agent_executor()  # a fresh agent for this demo
    chat_history = []  # start with EMPTY conversation memory (a plain Python list)

    def ask_agent(user_input: str) -> str:  # run one turn AND update the shared history
        response = agent_executor.invoke({  # execute the agent for this turn
            "input": user_input,  # the current user message
            "chat_history": chat_history,  # ALL prior human/AI turns go into the placeholder
        })
        ai_text = response["output"]  # the final assistant text for this turn
        chat_history.append(HumanMessage(content=user_input))  # append the USER message FIRST
        chat_history.append(AIMessage(content=ai_text))  # then append the ASSISTANT reply
        return ai_text

    print("=" * 72)
    print("STAGE 3 — MANUAL chat_history (memory ON)")
    print("Turn 1")
    print("User :", "Hi, my order ID is ORD102.")
    print("AI   :", ask_agent("Hi, my order ID is ORD102."))  # the agent notes ORD102
    print("Turn 2 (depends on turn 1)")
    print("User :", "What is the status of it?")
    # Turn 2 has no explicit ID, but chat_history carries ORD102, so the tool can be called.
    print("AI   :", ask_agent("What is the status of it?"))


# ===========================================================================
# STAGE 4 — STATELESS BASELINE: same agent, empty history, never append
# ===========================================================================
# To PROVE memory changes behaviour, run the identical agent but always pass chat_history=[]
# and never append. Turn 2 typically fails to recall ORD102 and asks for the ID again — the
# same wording that SUCCEEDS once memory is wired in Stage 3.

def demo_stateless_baseline() -> None:
    """Run the same two turns with NO memory update to contrast against Stage 3."""
    agent_executor = build_agent_executor()  # same construction, different usage

    def ask_agent_stateless(user_input: str) -> str:  # a helper that NEVER updates history
        response = agent_executor.invoke({
            "input": user_input,  # only the current message
            "chat_history": [],  # ALWAYS empty -> the model sees no prior turns
        })
        return response["output"]

    print("=" * 72)
    print("STAGE 4 — STATELESS baseline (memory OFF)")
    print("Turn 1")
    print("AI   :", ask_agent_stateless("Hi, my order ID is ORD102."))  # noted, but not kept
    print("Turn 2 (no prior context)")
    # With no history, "it" is unresolved — expect the agent to ask for the order ID again.
    print("AI   :", ask_agent_stateless("What is the status of it?"))


# ===========================================================================
# STAGE 5 — AUTOMATIC history with RunnableWithMessageHistory + session stores
# ===========================================================================
# Manual append is great for learning but error-prone in production (forget a turn, wrong order,
# wrong session). RunnableWithMessageHistory loads a session's history, injects it into the
# prompt, runs the executor, and appends the new turns automatically. Histories are kept PER
# SESSION so User A's order ID can never leak into User B's chat — like separate chat tabs.

# store maps session_id -> its own InMemoryChatMessageHistory (NOT one global list). RAM-only:
# restart the app and it is gone unless you persist to a database in production.
store = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Return the history object for a session, creating an empty one on first use."""
    if session_id not in store:  # first time we see this session id
        store[session_id] = InMemoryChatMessageHistory()  # start it with an empty history
    return store[session_id]  # existing or newly created history


def demo_automatic_memory() -> None:
    """Wrap the executor so history load/inject/append happens automatically, per session."""
    agent_executor = build_agent_executor()  # the same executor as before

    # The wrapper wires three keys to match our prompt + executor: input (current message),
    # chat_history (the placeholder name), and output (the assistant text to append back).
    agent_with_memory = RunnableWithMessageHistory(
        agent_executor,  # the runnable to execute
        get_session_history,  # factory returning the history for a given session id
        input_messages_key="input",  # key for the current user input
        history_messages_key="chat_history",  # MUST match the prompt placeholder name
        output_messages_key="output",  # key for the assistant output to append
    )

    def ask_agent_auto(session_id: str, user_input: str) -> str:  # one turn within a session
        result = agent_with_memory.invoke(
            {"input": user_input},  # pass ONLY the new message — the wrapper adds history
            config={"configurable": {"session_id": session_id}},  # select the conversation bucket
        )
        return result["output"]

    print("=" * 72)
    print("STAGE 5 — AUTOMATIC history (RunnableWithMessageHistory)")

    session_a = "user-001"  # first customer's conversation
    print("Session A, HUMAN INPUT Turn 1: Hi, my order ID is ORD101.")
    print("Session A, Turn 1:", ask_agent_auto(session_a, "Hi, my order ID is ORD101."))
    # "it" resolves from session A's own history -> the tool runs with ORD101.
    print("Session A, HUMAN INPUT Turn 2: What is the status of it?") 
    print("Session A, Turn 2:", ask_agent_auto(session_a, "What is the status of it?"))

    session_b = "user-002"  # a DIFFERENT customer — must not see session A's ID
    # Correct wiring means session B has no knowledge of ORD101; the agent should ask for an id.
    print("Session B, HUMAN INPUT Turn 1: What is my order ID?")
    print("Session B, Turn 1:", ask_agent_auto(session_b, "What is my order ID?"))

    # Peek at the stored histories to SEE that sessions are isolated in RAM.
    print("-" * 72)
    print("Stored sessions:", list(store.keys()))
    print("Session A messages:", len(store[session_a].messages))
    print("Session B messages:", len(store[session_b].messages))


# ===========================================================================
# DRIVER — run the three memory patterns back to back
# ===========================================================================
def main() -> None:
    # STAGE 3 — memory ON via manual append: the follow-up succeeds.
    demo_manual_memory()

    # STAGE 4 — memory OFF baseline: the same follow-up fails, proving memory matters.
    demo_stateless_baseline()

    # STAGE 5 — memory ON via the auto wrapper, with session isolation.
    demo_automatic_memory()

    # Try it:
    #   1) In demo_manual_memory, DELETE the two append lines and re-run — watch turn 2 ask for
    #      the order ID again (the classic "placeholder without append" bug).
    #   2) Change the placeholder name to "history" in ONE place only and see the wiring break —
    #      the template name must match the invoke/wrapper key exactly.
    #   3) Add n_messages=4 to the chat_history placeholder, run 6+ turns in one session, then
    #      print store[session_id].messages and confirm the earliest turns dropped.
    #   4) Change ONLY OLLAMA_TEMPERATURE in .env from 0 to 0.9 and compare stability — the
    #      Python never changes.
    print("=" * 72)
    print("Edit .env (model, host, temperature) and re-run — the memory wiring stays the same.")xss


if __name__ == "__main__":
    main()  # Load .env, then walk manual memory, the stateless baseline, and automatic memory
