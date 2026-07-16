# lecture29.py — Building your first LangChain AGENT: create_tool_calling_agent + AgentExecutor (Session 29)
#
# In Session 28 you wrote the tool-calling loop BY HAND: you used @tool to register functions,
# bind_tools to expose them, read the model's tool_calls "order slip", ran each tool inside a
# try/except, and fed results back as ToolMessages — all inside a BOUNDED loop capped by
# max_steps. That manual loop taught you every step of the flow:
#
#       model requests -> your Python runs the tool -> result goes back -> model replies
#
# Today you keep the SAME flow but stop hand-writing the loop. LangChain's AGENT RUNTIME
# manages it for you: create_tool_calling_agent builds the DECISION layer (when + which tool),
# and AgentExecutor is the runtime MANAGER that runs the loop, executes tools, applies safety
# limits, and records step-level traces. You stay in control through CONFIGURATION.
#
# Restaurant-to-office analogy carried forward: the model is still the waiter that plans, your
# tools are still the kitchen. New in this session: AgentExecutor is the SHIFT MANAGER who
# runs the whole service — tracks which desk was called, what reply came back, and when to
# stop retrying — so you do not babysit every step yourself.
#
# What changes vs Session 28 (the mental map):
#   bind_tools + read tool_calls yourself   ->   create_tool_calling_agent (decision layer)
#   your for-loop over tool_calls           ->   AgentExecutor (managed loop)
#   max_steps you coded                     ->   max_iterations (config)
#   your try/except recovery                ->   handle_parsing_errors=True
#   your print statements for diagnosis     ->   return_intermediate_steps=True (real traces)
#
# What this file demonstrates (one script, five escalating stages):
#   STAGE 1 — LOAD CONFIG from .env and build a tool-capable ChatOllama
#   STAGE 2 — @tool: three focused tools over a fake order DB (one clear job each)
#   STAGE 3 — PROMPT with an agent_scratchpad placeholder (working memory for one run)
#   STAGE 4 — create_tool_calling_agent + AgentExecutor with bounded, observable defaults
#   STAGE 5 — COHORT TEST PACK: validate the tool PATH (single / multi / no tool) not just text
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

# LangChain Core — the tool decorator plus the prompt helpers the agent needs.
from langchain_core.tools import tool  # @tool converts a Python function into a LangChain tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # prompt + scratchpad

# LangChain agents — the decision layer builder and the runtime that executes the loop.
# NOTE: In LangChain 1.x the classic AgentExecutor + create_tool_calling_agent moved to the
# `langchain-classic` package (install: pip install langchain-classic). On LangChain 0.x these
# were importable from `langchain.agents` instead.

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent  # agent + its manager

# Provider package — the LangChain wrapper that makes Ollama look like a chat model.
from langchain_ollama import ChatOllama  # ChatOllama is a Runnable bound to your Ollama server

# ---------------------------------------------------------------------------
# STAGE 1 — CONFIGURATION FROM .env (same secure pattern as Sessions 27-28)
# ---------------------------------------------------------------------------
# load_dotenv() MUST run BEFORE any os.environ.get(...) below, or the values are missing and
# the defaults silently take over. Settings live in .env, never in the .py file.
load_dotenv()  # Make OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_TEMPERATURE available via os.environ

# Each get() has a DEFAULT so the script still runs if a key is missing. The default model
# here is a TOOL-CAPABLE one — swap it in .env, never in code.
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")  # Tag from "ollama list", tool-capable
BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")  # Where Ollama listens
# Temperature arrives as a STRING from .env, so float() converts it. 0 = stable tool selection.
TEMPERATURE = float(os.environ.get("OLLAMA_TEMPERATURE", "0"))  # Deterministic during testing


# ===========================================================================
# STAGE 2 — THREE FOCUSED TOOLS OVER A FAKE ORDER DATABASE
# ===========================================================================
# Same rules as Session 28: clear name, a type hint on every argument, a docstring that says
# WHAT the tool does and WHEN to use it, and validation INSIDE the function. One clear job per
# tool. The e-commerce support scenario makes tool ROUTING easy to test: status, refund, ETA.
# Tool output should EXPLAIN the policy (not just say yes/no) so the model writes a better reply.

# A small in-memory dict stands in for a real orders database.
orders_db = {  # order_id -> record with the fields the tools read
    "ORD101": {"status": "shipped", "city": "Delhi", "amount": 2500, "delivery_days": 2},
    "ORD102": {"status": "cancelled", "city": "Bangalore", "amount": 1800, "delivery_days": 0},
    "ORD103": {"status": "delivered", "city": "Mumbai", "amount": 3200, "delivery_days": 0},
}


@tool  # Register this function as a LangChain tool the agent can request.
def get_order_status(order_id: str) -> str:  # A string ID in, a status string out
    """Get the current status, city, and amount for a specific order ID."""  # WHEN to use it
    order = orders_db.get(order_id)  # Safe lookup — returns None if the id is unknown
    if not order:  # Handle the not-found case INSIDE the tool, never crash
        return f"No order found for order ID {order_id}."  # Clear, model-readable message
    return (  # Return a readable summary the model can turn into a reply
        f"Order {order_id} is currently {order['status']} "
        f"for {order['city']} and the amount is {order['amount']}."
    )


@tool  # Register the refund tool — note it EXPLAINS policy, not just a number.
def calculate_refund_amount(order_id: str) -> str:  # Order id in, policy-aware message out
    """Explain the refund eligibility and amount for a specific order ID."""  # Business use case
    order = orders_db.get(order_id)  # Look the order up first
    if not order:  # Unknown id -> recoverable message
        return f"No order found for order ID {order_id}."
    if order["status"] == "cancelled":  # Cancelled orders get a full refund in this demo
        return f"Order {order_id} is cancelled, so the full refund amount is {order['amount']}."
    if order["status"] == "delivered":  # Delivered orders depend on policy
        return f"Order {order_id} is delivered. Refund eligibility depends on product policy."
    return f"Order {order_id} is shipped. Refund cannot be finalized until return/cancellation."


@tool  # Register the ETA tool — condition-based responses keep it focused.
def estimate_delivery_timeline(order_id: str) -> str:  # Order id in, ETA message out
    """Estimate the delivery timeline for a specific order ID."""  # What it retrieves
    order = orders_db.get(order_id)  # Fetch the record
    if not order:  # Invalid id -> clear not-found message
        return f"No order found for order ID {order_id}."
    if order["status"] == "shipped":  # In transit -> report remaining days
        return f"Order {order_id} is shipped and expected in {order['delivery_days']} day(s)."
    if order["status"] == "delivered":  # Already arrived
        return f"Order {order_id} has already been delivered."
    if order["status"] == "cancelled":  # Cancelled -> no timeline exists
        return f"Order {order_id} is cancelled, so no delivery timeline exists."
    return f"Delivery status for order {order_id} is currently unavailable."  # Unknown status


# One list, reused everywhere: given to the agent AND to the executor, so they can never drift.
tools = [get_order_status, calculate_refund_amount, estimate_delivery_timeline]  # The tool menu


# ===========================================================================
# STAGE 3 — THE PROMPT WITH AN agent_scratchpad PLACEHOLDER
# ===========================================================================
# The agent prompt needs THREE pieces:
#   - a SYSTEM message that sets behaviour boundaries ("use tools only when needed")
#   - a HUMAN placeholder {input} that carries the user's query
#   - a MESSAGES placeholder named "agent_scratchpad" — the agent's NOTEPAD for this one run
# The scratchpad holds intermediate reasoning + tool observations so multi-step chaining keeps
# its context. WITHOUT it, the executor cannot pass tool results into the next model turn.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful e-commerce support assistant. Use tools only when required."),
    ("human", "{input}"),  # the user's query is injected here at invoke() time
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # working memory for the current run
])


# ===========================================================================
# STAGE 4 — BUILD THE AGENT AND WRAP IT IN A BOUNDED, OBSERVABLE EXECUTOR
# ===========================================================================
# create_tool_calling_agent builds the DECISION layer (when + which tool) — it replaces the
# part where you called bind_tools and inspected tool_calls yourself in Session 28.
# AgentExecutor is the RUNTIME MANAGER: it runs the loop, executes tools, and applies safety
# controls. The four executor settings below move this closer to production behaviour.

def build_agent_executor() -> AgentExecutor:
    """Create the model, the tool-calling agent, and a safely-configured AgentExecutor.

    Executor settings and WHY each matters:
      verbose=True                   -> print internal logs so you can watch the loop run
      max_iterations=3               -> BOUNDED retries (the managed version of max_steps)
      handle_parsing_errors=True     -> recover gracefully instead of crashing on bad output
      return_intermediate_steps=True -> include step-level (action, observation) traces
    """
    llm = ChatOllama(
        model=MODEL_NAME,  # Tool-capable tag from OLLAMA_MODEL
        base_url=BASE_URL,  # Host from OLLAMA_HOST
        temperature=TEMPERATURE,  # 0 from OLLAMA_TEMPERATURE = deterministic selection
    )

    # The decision layer: reasons about WHEN and WHICH tool to call, using the prompt above.
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

    # The runtime layer: actually runs the agent, tracks steps, handles errors, and stops
    # runaway loops. You OWN the tools; the executor OWNS the repetitive orchestration.
    agent_executor = AgentExecutor(
        agent=agent,  # the decision layer we just built
        tools=tools,  # the SAME tool list the agent was given
        verbose=False,  # stream internal execution logs for tracing
        max_iterations=3,  # cap the action loops so it never retries forever
        handle_parsing_errors=False,  # a parsing hiccup becomes recoverable, not a crash
        return_intermediate_steps=True,  # expose per-step traces for observability
    )
    return agent_executor


def run_query_with_trace(agent_executor: AgentExecutor, user_query: str) -> None:
    """Invoke the executor on one query, print the final answer, then the step-level trace.

    result["output"]             -> the single, polished, user-facing reply
    result["intermediate_steps"] -> a list of (action, observation) pairs — the REAL path:
        action.tool        -> which tool ran this step
        action.tool_input  -> the arguments the model supplied
        observation        -> what the tool returned
    These traces replace the print statements you scattered through the manual loop.
    """
    print("=" * 72)
    print("USER  :", user_query)
    result = agent_executor.invoke({"input": user_query})  # the executor runs the whole loop
    print("AGENT :", result["output"])  # one clean reply built from all the tool results

    # Step-level observability: verify the EXPECTED tool ran, inspect wrong args quickly, and
    # separate model-reasoning issues from tool-implementation bugs.
    for step_number, (action, observation) in enumerate(result["intermediate_steps"], start=1):
        print(f"  step {step_number}: tool={action.tool} "
              f"input={action.tool_input} -> {observation}")


# ===========================================================================
# STAGE 5 — COHORT TEST PACK: validate the tool PATH, not just the final text
# ===========================================================================
# A cohort test pack is a small, FIXED set of representative queries run repeatedly to validate
# behaviour. It checks the DECISION PATH (which tools were chosen), not only the final sentence.
# It is the managed-agent version of the controlled query set you used for diagnosis earlier.
# Query classes: single-tool, multi-tool, no-tool (out of scope), and missing id.

def run_cohort_test_pack(agent_executor: AgentExecutor) -> None:
    """Run each representative query and PASS/FAIL it on the SET of tools actually called."""
    test_pack = [  # each case pairs a query with the tools we EXPECT it to trigger
        {  # single-tool: only a status lookup is needed
            "query": "What is the status of order ORD101?",
            "expected_tools": ["get_order_status"],
        },
        {  # multi-tool: status + ETA + refund for one order
            "query": "For order ORD102, check status, delivery estimate, and refund amount.",
            "expected_tools": [
                "get_order_status",
                "estimate_delivery_timeline",
                "calculate_refund_amount",
            ],
        },
        {  # no-tool: out of scope — the agent should NOT invent a booking tool
            "query": "Can you book a flight from Delhi to Mumbai?",
            "expected_tools": [],
        },
        {  # missing id: refund asked without an order id — no tool path is correct
            "query": "What is my refund amount?",
            "expected_tools": [],
        },
    ]

    for case in test_pack:  # run each validation case
        result = agent_executor.invoke({"input": case["query"]})  # execute the agent
        # Collect the tools ACTUALLY used from the intermediate steps.
        actual_tools = {action.tool for action, _observation in result["intermediate_steps"]}
        expected_tools = set(case["expected_tools"])  # order-independent comparison via sets
        verdict = "PASS" if actual_tools == expected_tools else "FAIL"  # decision-path check
        print("=" * 72)
        print("QUERY    :", case["query"])
        print("EXPECTED :", sorted(expected_tools))  # the tools we intended
        print("ACTUAL   :", sorted(actual_tools))  # the tools the model chose
        print("RESULT   :", verdict)  # a regression after a prompt/tool change flips this


# ===========================================================================
# DRIVER — build once, then walk through the demo and the test pack
# ===========================================================================
def main() -> None:
    # STAGE 4 — build the agent + executor a single time and reuse it everywhere.
    agent_executor = build_agent_executor()

    # A few end-to-end runs with full traces: single-tool, multi-tool, and an invalid id.
    demo_queries = [
        "What is the status of order ORD101?",  # single tool -> get_order_status
        "For order ORD102, check status, delivery estimate, and refund amount.",  # multi-tool
        "What is the delivery timeline for order ORD999?",  # invalid id -> safe not-found
    ]
    for query in demo_queries:
        run_query_with_trace(agent_executor, query)  # one polished reply + the real tool path

    # STAGE 5 — validate the decision path across the standard query classes.
    run_cohort_test_pack(agent_executor)

    # Try it:
    #   1) Change max_iterations from 3 to 1 and re-run the MULTI-tool query — watch it stop
    #      early before completing every step.
    #   2) Toggle return_intermediate_steps between True and False and compare the output shape.
    #   3) Add a new order to orders_db and test all three tools for that id.
    #   4) Weaken a tool's docstring (e.g. "gets data") and re-run the cohort pack — see the
    #      model mis-route. Then restore the clear description.
    #   5) Change ONLY OLLAMA_TEMPERATURE in .env from 0 to 0.9 and observe how tool selection
    #      stability changes — the Python never changes.
    print("=" * 72)
    print("Edit .env (model, host, temperature) and re-run — the agent + executor code stays the same.")


if __name__ == "__main__":
    main()  # Load .env, build the agent + executor, run the demo queries, then the cohort pack
