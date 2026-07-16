# lecture28.py — LangChain Tools: custom @tool functions + a manual tool-calling loop (Session 28)
#
# In Session 27 you shipped a REAL project layout: settings came from .env, the prompt
# became a role-based ChatPromptTemplate, and a validation gate sat AFTER the chain:
#
#       ChatPromptTemplate  ->  ChatOllama  ->  StrOutputParser
#
# That chain can only GENERATE TEXT. It cannot add numbers reliably, look up a record, or
# apply exact business rules. Today the model stops being text-only: it learns to REQUEST
# ACTIONS through tools. This is the first step from "a chain" toward "an agent."
#
# Big idea this session: the model NEVER runs your Python. It only emits a structured
# REQUEST (tool_calls) saying "call THIS tool with THESE arguments." YOUR application reads
# that request, runs the function, and sends the result back as a ToolMessage. Then the
# model turns the raw result into one polite final answer. Restaurant analogy:
#
#       user = customer   |   LLM = waiter   |   tool_calls = order slip
#       your function = kitchen   |   ToolMessage = plated dish   |   final reply = the serve
#
# What this file demonstrates (one script, five escalating stages):
#   STAGE 1 — LOAD CONFIG from .env and build a tool-capable ChatOllama
#   STAGE 2 — @tool: turn plain Python functions into LangChain tools (name/desc/args)
#   STAGE 3 — bind_tools + inspect tool_calls: see the model's "order slip", it does NOT run
#   STAGE 4 — MANUAL TOOL LOOP with max_steps + ToolMessage + error containment (the core)
#   STAGE 5 — CONTROLLED QUERY SET: one trace loop to diagnose tool-selection faults
#
# PREREQUISITES (do these in the terminal BEFORE running this file):
#   python3 -m venv venv && source venv/bin/activate     # (Windows: venv\Scripts\activate)
#   pip install -U pip langchain-core langchain-ollama python-dotenv
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

# LangChain Core — the tool decorator and the message classes for the tool-feedback loop.
from langchain_core.tools import tool  # @tool converts a Python function into a LangChain tool
from langchain_core.messages import HumanMessage, ToolMessage  # User input + tool-result messages

# Provider package — the LangChain wrapper that makes Ollama look like a Runnable.
from langchain_ollama import ChatOllama  # ChatOllama is a Runnable bound to your Ollama server

# ---------------------------------------------------------------------------
# STAGE 1 — CONFIGURATION FROM .env (same secure pattern as Session 27)
# ---------------------------------------------------------------------------
# load_dotenv() MUST run BEFORE any os.environ.get(...) below, or the values are missing and
# the defaults silently take over. Settings live in .env, never in the .py file.
load_dotenv()  # Make OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_TEMPERATURE available via os.environ

# Each get() has a DEFAULT so the script still runs if a key is missing. The default model
# here is a TOOL-CAPABLE one — swap it in .env, never in code.
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")  # Tag from "ollama list", tool-capable
BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")  # Where Ollama listens
# Temperature arrives as a STRING from .env, so float() converts it. 0 = stable tool selection.
TEMPERATURE = float(os.environ.get("OLLAMA_TEMPERATURE", "0.3"))  # Deterministic during testing


# ===========================================================================
# STAGE 2 — WRITING CUSTOM TOOLS WITH @tool
# ===========================================================================
# @tool reads FIVE things from each function and shows them to the model: the NAME, the
# DOCSTRING (description), the ARGUMENT names, their TYPE HINTS, and the return value. The
# model uses name + description + arg types to DECIDE which tool to call and with what args.
# Rules that make tools reliable: clear names, a type hint on every argument, a docstring that
# says WHAT it does and WHEN to use it, and validation INSIDE the function (hints are a guide,
# not a guard). One clear job per tool.

@tool  # Register this function as a LangChain tool the model can request.
def calculate_final_fee(base_fee: int, discount_percent: int) -> int:  # Typed inputs -> int out
    """Calculate the final course fee after applying a discount percentage."""  # WHEN to use it
    discount_amount = base_fee * discount_percent // 100  # Integer math for the discount amount
    final_fee = base_fee - discount_amount  # Subtract the discount from the original fee
    return final_fee  # Return the payable amount to LangChain


@tool  # Register a second tool that applies simple business rules.
def check_course_eligibility(has_laptop: bool, weekly_hours: int) -> str:  # Two typed inputs
    """Check if a learner is eligible for a coding-heavy online course."""  # Business use case
    if not has_laptop:  # Validate the laptop requirement INSIDE the tool, not just via type hint
        return "Not eligible yet: a laptop is required for hands-on practice."  # Clear reason
    if weekly_hours < 10:  # Validate the time commitment
        return "Not eligible yet: at least 10 hours per week are needed."  # Clear reason
    return "Eligible: the learner has the basic setup and time commitment."  # Approval message


@tool  # Register a third tool that looks up a record (simulated database).
def get_ticket_status(ticket_id: str) -> str:  # A string ID in, a status string out
    """Get the current status of a learner support ticket by ticket ID."""  # What it retrieves
    ticket_database = {  # A small in-memory dict stands in for a real database
        "T101": "Open: waiting for mentor review.",  # Sample ticket
        "T102": "Resolved: refund confirmation sent.",  # Sample ticket
        "T103": "In progress: technical team is checking the issue.",  # Sample ticket
    }
    return ticket_database.get(ticket_id, "Ticket not found.")  # Safe fallback, never a crash


# All tools in one list. This SAME list is bound to the model AND turned into a name->tool
# lookup for execution, so the two can never drift apart.
tools = [calculate_final_fee, check_course_eligibility, get_ticket_status]  # The tool menu
tool_map = {current_tool.name: current_tool for current_tool in tools}  # Lookup by tool name


def describe_tools() -> None:
    """Print what the model will actually SEE for each tool — its name, description, and schema.

    Before wiring anything up, inspect the tool metadata. If a description is vague or an
    argument type is wrong HERE, the model will mis-select or mis-fill it later.
    """
    print("=" * 72)
    print("REGISTERED TOOLS (this is what the model sees):")
    for current_tool in tools:  # Loop through every registered tool
        print("-" * 72)
        print("name        :", current_tool.name)  # The name the model reads to choose the tool
        print("description :", current_tool.description)  # The docstring drives tool selection
        print("args        :", current_tool.args)  # Input schema inferred from the type hints


# ===========================================================================
# STAGE 3 — bind_tools + INSPECTING tool_calls (the model does NOT run anything)
# ===========================================================================
def build_model_with_tools():
    """Create a ChatOllama from .env and ATTACH the tool menu with bind_tools.

    bind_tools does NOT execute anything — it only tells the model "these helpers exist for
    this request." The model can only choose from the tools you bind. Reused by every stage.
    """
    model = ChatOllama(
        model=MODEL_NAME,  # Tool-capable tag from OLLAMA_MODEL
        base_url=BASE_URL,  # Host from OLLAMA_HOST
        temperature=TEMPERATURE,  # 0 from OLLAMA_TEMPERATURE = deterministic selection
    )
    return model.bind_tools(tools)  # A model wrapper that knows about our tools


def show_tool_calls(model_with_tools) -> None:
    """Send one query and print the model's structured REQUEST without executing it.

    The reply is an AIMessage with two parts: .content (any text) and .tool_calls (the
    "order slip"). Each tool call is a dict with name, args, and id. The model has NOT run
    the function — it only asked. Your app decides what to do next.
    """
    print("=" * 72)
    query = "A course fee is 50000 rupees. Discount is 20%. What is the final fee?"  # Tool-worthy
    response = model_with_tools.invoke(query)  # Ask the model to DECIDE whether a tool is needed
    print("QUERY      :", query)
    print("CONTENT    :", response.content)  # Often empty when the model only wants a tool
    print("TOOL CALLS :", response.tool_calls)  # The structured request: name, args, id, type
    # Each entry looks like:
    #   {"name": "calculate_final_fee", "args": {"base_fee": 50000, "discount_percent": 20},
    #    "id": "call_abc123", "type": "tool_call"}
    # name -> which function to run, args -> its inputs, id -> links the result back later.


# ===========================================================================
# STAGE 4 — THE MANUAL TOOL LOOP: max_steps + ToolMessage + error containment
# ===========================================================================
# This is the heart of the session and the foundation of agentic systems. One question may
# need SEVERAL model turns (check eligibility, THEN calculate fee), so we loop — but a BOUNDED
# loop (max_steps) prevents running forever. Every tool call runs inside try/except so a tool
# failure becomes a recoverable ToolMessage instead of a crash. Handle ALL cases: zero tool
# calls, one, many, an unknown tool name, and an exception mid-execution.

def run_agent_loop(user_query: str, max_steps: int = 5) -> str:
    """Drive the model->tools->model feedback loop until a text-only answer or the step cap.

    Loop logic (per the lecture):
      1) invoke the model on the running message history
      2) append its AIMessage
      3) if it emitted NO tool_calls -> that content IS the final answer, return it
      4) otherwise run each requested tool SAFELY and append a ToolMessage per call, then repeat
      5) if still not done after max_steps, return a polite give-up message
    """
    model_with_tools = build_model_with_tools()  # Bind tools once for this whole conversation

    # The conversation history grows as we append AIMessages and ToolMessages. The model reads
    # the WHOLE list each turn, which is how it "sees" tool results from earlier steps.
    messages = [HumanMessage(content=user_query)]  # Start with the user's question

    for step in range(max_steps):  # Bounded: never loop forever
        ai_message = model_with_tools.invoke(messages)  # Ask the model what to do next
        messages.append(ai_message)  # ALWAYS record the model's turn in history

        if not ai_message.tool_calls:  # No tool requested -> the model is giving its final reply
            return ai_message.content  # Done: hand back the text answer

        # The model requested one or more tools. Run EACH one safely.
        for tool_call in ai_message.tool_calls:  # Handles one, many, or repeated tool calls
            tool_name = tool_call["name"]  # Which tool the model asked for
            tool_args = tool_call["args"]  # The arguments it supplied
            tool_call_id = tool_call["id"]  # The ID that links this result back to the request

            if tool_name not in tool_map:  # The model may hallucinate a tool that does not exist
                error_text = f"Tool error: unknown tool '{tool_name}'."  # Controlled message
                messages.append(ToolMessage(content=error_text, tool_call_id=tool_call_id))
                continue  # Feed the error back and move on — do NOT crash

            selected_tool = tool_map[tool_name]  # Find the matching Python tool object

            try:  # Protected execution: a tool can raise, and that must not kill the program
                tool_result = selected_tool.invoke(tool_args)  # Run the real Python function
                tool_content = str(tool_result)  # ToolMessage content must be text
            except Exception as error:  # Bad args, bad types, or a raised ValueError land here
                tool_content = f"Tool error: {error}"  # Convert the failure into recoverable text

            # Append the result (success OR error) tagged with the id so the model can match it
            # to its original request — the "same order number" on the plated dish.
            messages.append(ToolMessage(content=tool_content, tool_call_id=tool_call_id))

        # Loop back: the model now sees the ToolMessages and can either finish or call more tools.

    # Fell through the step cap without a text-only answer — fail politely, not silently.
    return "Sorry, I could not complete this request within the allowed number of steps."


# ===========================================================================
# STAGE 5 — CONTROLLED QUERY SET: a repeatable trace to DIAGNOSE tool faults
# ===========================================================================
# A controlled query set is a fixed "mini test paper" for your tool-calling setup. Running the
# same queries every time makes tool-selection faults visible: no tool when one was expected,
# the wrong tool, a wrong/missing argument name, or a bad argument type. Always inspect the
# model's tool_calls BEFORE assuming the tool CODE is wrong.

def trace_controlled_queries() -> None:
    """Send a fixed set of queries and print the raw tool_calls the model emits for each."""
    model_with_tools = build_model_with_tools()  # Same bound model, no execution here

    test_queries = [  # Mixed on purpose: some need tools, one should NOT
        "Calculate final fee for 50000 rupees with 20 percent discount.",  # -> calculate_final_fee
        "I have a laptop and can study 8 hours weekly. Am I eligible?",  # -> not eligible (time)
        "I have no laptop but can study 20 hours weekly. Am I eligible?",  # -> not eligible (laptop)
        "What is the status of ticket T102?",  # -> get_ticket_status
        "Tell me a motivational line for studying daily.",  # -> NO tool: pure text generation
    ]

    for query in test_queries:  # One trace per query
        response = model_with_tools.invoke(query)  # Just DECIDE — we do not run the tools here
        print("=" * 72)
        print("QUERY      :", query)  # The exact input, for readable traces
        print("CONTENT    :", response.content)  # Any direct text the model produced
        print("TOOL CALLS :", response.tool_calls)  # What the model wants to run (name + args)
        # If the model picks the wrong tool or wrong arg names here, fix the tool NAME,
        # DESCRIPTION, or type hints — not the loop code.


# ===========================================================================
# DRIVER — walk through all five stages in order
# ===========================================================================
def main() -> None:
    # STAGE 2 — inspect what the model will see for each tool.
    describe_tools()

    # STAGE 3 — bind the tools and look at the "order slip" without executing it.
    model_with_tools = build_model_with_tools()
    show_tool_calls(model_with_tools)

    # STAGE 4 — the real thing: run full tool-feedback loops end to end.
    loop_queries = [
        # Needs TWO checks in one question -> the model may emit multiple tool calls.
        "I have a laptop and can study 12 hours weekly. Also calculate the fee after a "
        "15% discount on 60000 rupees.",
        # A lookup query -> get_ticket_status with a valid id.
        "What is the current status of my support ticket T103?",
        # An id that does NOT exist -> the tool returns a safe 'not found', not a crash.
        "Check the status of ticket T999 for me.",
    ]
    for query in loop_queries:
        print("=" * 72)
        print("USER  :", query)
        answer = run_agent_loop(query)  # Full model -> tool -> model round trip
        print("AGENT :", answer)  # One clean, user-facing reply built from the tool results

    # STAGE 5 — diagnostic trace over the controlled query set.
    trace_controlled_queries()

    # Try it:
    #   1) Add a query that needs the ticket tool AND the fee tool in one sentence, and watch
    #      run_agent_loop handle multiple tool calls.
    #   2) Weaken get_ticket_status's docstring to "Gets data." and re-run STAGE 5 — see the
    #      model stop selecting it. Then restore the clear description.
    #   3) Change ONLY OLLAMA_TEMPERATURE in .env from 0 to 0.9 and compare how stable the
    #      tool selection stays — the Python never changes.
    print("=" * 72)
    print("Edit .env (model, host, temperature) and re-run — the tool + loop code stays the same.")


if __name__ == "__main__":
    main()  # Load .env, register tools, inspect calls, run the loop, and trace the query set
