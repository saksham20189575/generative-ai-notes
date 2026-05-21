# Short-Term vs Long-Term Memory in AI Agents

## Context of This Session

In the previous session, we built a solid foundation by understanding what memory means for an AI agent. We explored the concept of **state** — the ability of an agent to hold and use information from past interactions. We saw how **stateless agents** treat every message as brand new, while **stateful agents** carry forward a thread of context that makes them feel intelligent and personalised. We also took a first look at the two broad categories of memory — short-term and long-term — and compared how agents behave with and without memory.

Now that you understand *why* memory matters, this session goes one level deeper: *how* memory actually works, *what kinds* of memory exist in detail, and *what strategies* agents use to manage memory efficiently. Think of the previous session as understanding that a library exists — and this session as learning how the library is organised, how books are filed, and how the librarian decides what to keep on the main shelf versus what to store in the archive.

**In this session, you will:**

- Revisit and reinforce the role of memory in enabling intelligent agent behaviour
- Clearly understand the difference between short-term and long-term memory with practical comparisons
- Learn how conversation history works as the agent's working memory
- Discover the real limitations of context-window-based memory
- Explore three practical short-term memory strategies — Buffer, Window, and Summary
- Understand the three types of long-term memory — Episodic, Semantic, and Procedural
- See how basic memory strategies can be wired into an agent workflow
- Understand how agents decide what is worth remembering and get a foundation for external storage

---

## Revisiting Memory — Why It Is the Core of Agent Intelligence

Before we go deeper, let's quickly lock in the idea we built in the last session. An agent without memory is like a very smart but extremely forgetful assistant — it can think well, but only about what is in front of it right now.

- **Memory enables continuity** — the agent can refer back to something the user said 10 messages ago
- **Memory enables personalisation** — the agent learns user preferences, names, and habits over time
- **Memory enables better decisions** — the agent can factor in past outcomes when choosing the next action

Now, here is the key question this session answers: **not all memory is the same.** Just as your brain handles a phone number you need for 5 minutes very differently from how it handles your mother's face, agents have different memory types for different purposes. This difference is not just theoretical — it directly impacts how you design and build AI agents.

---

## Short-Term Memory vs Long-Term Memory — The Big Picture

The simplest way to understand both types is through a comparison you already know from everyday life.

- **Official Definition:** **Short-Term Memory (STM)** in an agent refers to the information the agent holds and uses *within a single, ongoing session or interaction*. It is temporary, active, and directly accessible during the current conversation.
- **In Simple Words:** Short-term memory is what the agent remembers *right now, in this conversation*. Once the session ends, this memory is gone — unless you explicitly save it.
- **Real-Life Example:** Think of the notepad a customer care agent uses during a phone call. They jot down your order number, your complaint, and the steps they have already tried. That notepad is session memory — useful right now, but it gets discarded once the call ends.

---

- **Official Definition:** **Long-Term Memory (LTM)** in an agent refers to information that is *stored persistently* — saved across sessions — so the agent can recall facts, preferences, and past experiences even in a completely new conversation.
- **In Simple Words:** Long-term memory is what the agent remembers *even after the conversation ends*. It is stored somewhere durable — a file, a database, a vector store — and retrieved when needed in a future session.
- **Real-Life Example:** Think of your doctor's patient file. Every visit, the doctor writes notes. Next time you visit — even a year later — the doctor opens your file and immediately knows your history. That file is long-term memory.

| Feature | Short-Term Memory | Long-Term Memory |
|---|---|---|
| **Duration** | Lives only during the session | Persists across sessions |
| **Storage Location** | In the model's active context window | External file, database, or vector store |
| **Speed of Access** | Instant (already in context) | Requires a retrieval step |
| **Capacity** | Limited by token/context window size | Virtually unlimited |
| **Risk of Loss** | Disappears when session ends | Durable and retrievable |
| **Use Case** | Maintaining conversation flow | Storing user profiles, past summaries, facts |

![Short-term memory holds what matters during this session; long-term memory is stored outside the chat so it survives after the session ends](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session13/session13-stm-vs-ltm.png)

---

> ### 🟦 Student Activity 1 — "Short-Term or Long-Term?"
>
> **Format:** Individual reflection → Instructor-led sharing (Zoom)
>
> **Instructions:**
> Two situations are described below. For each one, decide — is this short-term memory, long-term memory, or both? Prepare one sentence of reasoning before sharing.
>
> - Situation A: You are chatting with a shopping assistant. You say "I prefer blue" and two messages later it suggests blue shoes.
> - Situation B: You open a fitness app after three months. The coach says "Welcome back — last time you were working on your lower body strength."
>
> **Goal:** Anchor the STM vs LTM distinction to real, familiar experiences before moving into how conversation history physically works.

---

## How Conversation History Works as Short-Term Memory

Now that we understand *what* short-term memory is, let's understand *how* it actually works inside an agent.

When you are talking to an AI agent, the agent does not magically "remember" your earlier messages by magic. What really happens is much simpler — and also much more constrained.

- **Official Definition:** The **Context Window** is the total amount of text (measured in **tokens**) that an AI model can read and process in a single call. Everything the model "sees" — your questions, its own past answers, system instructions — must fit within this window.
- **In Simple Words:** The context window is like the desk space on which the agent works. It can only act on what is currently on the desk. Whatever is placed on the desk is its "memory" for this session.
- **Real-Life Example:** Imagine you are studying for an exam and you can only have 10 books open at a time. You keep the most relevant ones open in front of you. If you need a new book, you have to close one first. The context window works the same way — there is a fixed "desk space," and everything relevant must fit on it.

![The context window is limited working space — only the messages that fit “on the desk” are visible to the model on each call](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session13/session13-context-window-desk.png)

Here is the critical insight: **conversation history is short-term memory** because it is literally stored inside the context window. The agent is given the entire past conversation as part of every new request, which is why it appears to "remember" what you said earlier.

### How It Looks in Practice

Every time the user sends a message, the agent actually receives something like this:

```
System: You are a helpful assistant.

User: Hi, my name is Priya.
Agent: Hello Priya! How can I help you?

User: What did I just tell you my name was?
Agent: [Now processes this and sees "Priya" above in the history]
```

The entire message history is passed in full as part of the **prompt** to the model. The agent does not have a separate "memory module" — the conversation history *is* the memory, packed into the context window.

**How this works step by step:**

- **Step 1:** User sends Message 1 → Agent gets [System Prompt + Message 1] and responds
- **Step 2:** User sends Message 2 → Agent gets [System Prompt + Message 1 + Response 1 + Message 2] and responds
- **Step 3:** User sends Message 3 → Agent gets [System Prompt + all prior messages + Message 3] and responds
- With every turn, the context window grows larger, because more messages are added to the history

---

## The Real Limitations of Context-Window-Based Memory

Now that you understand how conversation history works as memory, let's talk about why this approach has serious limitations in real-world use.

Understanding these limitations is not discouraging — it is exactly what motivates the smarter memory strategies we will explore next.

### Limitation 1 — Token Limits

Every model has a maximum context window size. For example, a model might support 8,000 tokens, 32,000 tokens, or even 128,000 tokens. Once the conversation history exceeds this limit, **older messages must be removed** to make space for new ones.

- This means the agent literally "forgets" older parts of the conversation
- If critical information was said early in a long conversation, it may get cut off
- **Real-Life Example:** It is like a whiteboard that can only hold 100 words. As you keep writing, you have to erase the oldest lines to make room. The erased content is gone.

### Limitation 2 — Increasing Cost

In most AI APIs, you pay per token. Since every new message is sent along with the entire conversation history, the cost of each API call grows as the conversation gets longer.

- A 100-message conversation costs significantly more per message than a 5-message one
- For production systems that handle thousands of users, this cost compounds fast
- **Real-Life Example:** Imagine paying for every page of a document you re-read every time you open it — even the pages you have already read a hundred times.

### Limitation 3 — Performance Degradation

Research and real-world observation show that as the context window fills up, models can start to underperform. They might:

- Pay more attention to recent messages and "forget" important early messages
- Make mistakes because the relevant information is buried deep in a long context
- Take longer to process larger contexts, slowing down response times

This is why simply "keeping all history" is not a scalable solution. We need smarter approaches — which brings us to the **Short-Term Memory Strategies**.

![Why raw history breaks down at scale — token ceilings erase old turns, cost rises with every resend, and very long contexts become harder to use reliably](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session13/session13-context-limitations.png)

---

> ### 🟩 Milestone — Context Window Limitations Covered
>
> You now understand *why* storing raw conversation history is not enough at scale: tokens run out, costs climb, and very long contexts make the model less reliable. This is the motivation for everything that follows. In the next section, you will see three concrete strategies that agents use to work around these limitations intelligently.

---

## Short-Term Memory Strategies — Managing Conversation History Smartly

Given the limitations above, there are three main strategies agents use to manage conversation history intelligently. Each one is a trade-off between **memory completeness** and **efficiency**.

Think of these three strategies as three different ways a student can prepare notes before an exam — each suits a different situation.

---

### Strategy 1 — Buffer Memory (Keep Everything)

- **Official Definition:** **Buffer Memory** means the agent stores and passes the *complete and unmodified* conversation history to the model with every new request.
- **In Simple Words:** The agent keeps every single message — nothing is deleted, summarised, or filtered. It passes the full conversation as-is every time.
- **Real-Life Example:** Imagine photocopying and carrying the entire transcript of every conversation you have ever had with a customer, and handing all of it to a new customer care rep before each call. Complete information, but increasingly heavy and expensive.

**When Buffer Memory works well:**

- Short conversations with just a few turns (2–10 messages)
- Tasks where every word of past context matters, such as legal drafts or detailed technical debugging
- Situations where precision is more important than cost

**When Buffer Memory becomes a problem:**

- Long, multi-turn conversations where the history grows huge
- High-volume production systems where token cost matters
- When the context window limit is approaching

**Key Behaviour:**

- No information is ever lost
- Cost and context size grow linearly with every new message
- Simple to implement — just keep appending messages to a list

---

### Strategy 2 — Window Memory (Keep the Last N Messages)

- **Official Definition:** **Window Memory** means the agent keeps only the last *N* messages in the conversation history and discards everything older. The value of *N* (for example, 10 or 20 messages) is defined by the designer.
- **In Simple Words:** The agent has a sliding window of recent messages. As new messages come in, old ones fall off the other end — like a conveyor belt that always moves forward.
- **Real-Life Example:** Imagine a cricket commentator who only commentates based on the last 5 overs. They do not revisit what happened in over 1 when discussing over 45. They focus on the recent and relevant.

**When Window Memory works well:**

- Conversations where only recent context is relevant for the next response
- Customer support bots where old messages in a session are rarely needed
- Systems where you need a predictable, bounded memory cost

**When Window Memory can cause problems:**

- If a user refers to something they said much earlier and it is now outside the window, the agent will not know about it
- Important early context (like the user's name or goal) can get dropped
- A common fix is to keep a few "pinned" messages at the top (like the system prompt or user profile) outside the window

**Key Behaviour:**

- Memory size stays constant after N messages
- Older messages are simply dropped
- Risk: important early context may be lost

---

### Strategy 3 — Summary Memory (Compress and Keep the Essence)

- **Official Definition:** **Summary Memory** means the agent periodically generates a **compressed summary** of older conversation history and replaces the raw messages with that summary. Only the summary and the most recent messages are passed to the model.
- **In Simple Words:** Instead of carrying all old messages, the agent writes a short summary — "The user mentioned they are building a Python chatbot for e-commerce, prefers short answers, and has already set up the environment." This summary replaces the old messages.
- **Real-Life Example:** Think of a journalist writing a story on an ongoing event. Instead of re-reading 200 pages of source material every day, they write a brief summary: "As of Day 10, the key developments are...". They keep the summary and move forward.

**When Summary Memory works well:**

- Long conversations where only the key facts from earlier turns are needed, not verbatim messages
- Personal assistant agents that track user goals and preferences over a session
- When you need to balance cost with context retention

**When Summary Memory can cause problems:**

- Summarisation itself costs tokens (you are making an extra LLM call)
- If the summariser misses a detail, that detail is gone permanently
- Works best for high-level context, not for verbatim recall of exact words

**Key Behaviour:**

- Keeps context compact and within token limits
- Loses verbatim detail but retains meaning and key facts
- Adds a small overhead — the summarisation step — but pays off in long conversations

---

### Comparing the Three Strategies

| Strategy | What Is Kept | Best For | Main Risk |
|---|---|---|---|
| **Buffer** | All messages, unmodified | Short, precise conversations | High token cost in long chats |
| **Window** | Last N messages only | Cost-efficient, recent-context tasks | Early important context gets lost |
| **Summary** | A compressed summary + recent messages | Long conversations needing key facts | Summariser may miss exact details |

![Three ways to trim short-term context — keep every message (buffer), keep only the last N turns (window), or compress the past into a running summary plus recent raw turns](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session13/session13-buffer-window-summary.png)

---

> ### 🟦 Student Activity 2 — "Pick the Right Memory Strategy"
>
> **Format:** Individual think → Instructor-led row-by-row reveal (Zoom)
>
> **Instructions:**
> Three agent use cases are listed below. For each one, decide which short-term memory strategy — **Buffer**, **Window**, or **Summary** — is the best fit, and prepare one sentence of reasoning. There are no trick answers, but be ready to defend your choice.
>
> | Use Case | Strategy | Why? |
> |---|---|---|
> | A legal document review assistant — the lawyer and agent discuss a contract clause by clause, and every word of the prior discussion matters | ? | |
> | A customer support bot for a food delivery app — most questions are resolved in 3–4 turns and are unrelated to anything said earlier | ? | |
> | A personal career coach agent — sessions run over an hour, tracking a user's job search journey across 60+ messages | ? | |
>
> **Goal:** Build intuition for choosing between the three strategies based on real design constraints, not just definitions.

---

Now that we have explored how agents manage memory *within a session*, a natural question arises: what about information that needs to survive beyond the session? What about the things the agent must *never* forget, no matter how many conversations have passed? This is where **Long-Term Memory** comes in.

---

## Long-Term Memory — Storing What Must Not Be Forgotten

Long-term memory is the answer to the key limitation of context-window-based memory: **it disappears when the session ends.** Long-term memory solves this by storing important information in an **external storage system** — a file, a database, or a vector store — from which the agent can retrieve it in future sessions.

There are three distinct types of long-term memory in agents, each serving a different purpose.

---

### Type 1 — Episodic Memory (Memory of Events and Experiences)

- **Official Definition:** **Episodic Memory** refers to the agent's ability to store and recall *specific past interactions or events* — essentially a log of "what happened, when, and with whom."
- **In Simple Words:** Episodic memory is the agent's personal diary. It stores the story of specific past conversations and experiences that can be recalled later.
- **Real-Life Example:** "Last Tuesday, Ravi asked me for restaurant suggestions near his office in Pune. He prefers vegetarian food and a quiet atmosphere." This is an episodic memory — a specific event with context, time, and preference.

**What Episodic Memory Enables:**

- The agent can say "Last time you asked me this, you preferred..." without the user repeating it
- Supports personalisation over time — the agent feels like it truly knows the user
- Enables continuity across sessions — pick up where you left off

**How It Is Stored:**

- Often stored as structured logs or documents in a database
- Can be retrieved using keywords, timestamps, or user IDs
- In advanced systems, stored in **vector databases** that allow semantic search ("find conversations similar to this one")

---

### Type 2 — Semantic Memory (Memory of Facts and Knowledge)

- **Official Definition:** **Semantic Memory** refers to the agent's stored knowledge about the world — facts, concepts, definitions, and domain knowledge that are not tied to any specific event or conversation.
- **In Simple Words:** Semantic memory is the agent's textbook or encyclopedia. It stores general knowledge — not "what happened" but "what is true."
- **Real-Life Example:** Knowing that "Mumbai is the financial capital of India," or that "Python is a programming language," or "a diabetic patient should avoid sugar" — these are facts that are true regardless of when or to whom they were told.

**What Semantic Memory Enables:**

- The agent can answer factual questions without needing them in the current conversation
- Domain-specific agents (medical, legal, financial) can be loaded with expert knowledge
- Allows the agent to "know" things about the product, company, or subject it is designed for

**How It Is Stored:**

- Typically stored in **knowledge bases** or **vector stores**
- Retrieved using **semantic search** — searching by meaning, not just keywords
- Can also be embedded directly as part of the system prompt for smaller knowledge sets

---

### Type 3 — Procedural Memory (Memory of How To Do Things)

- **Official Definition:** **Procedural Memory** refers to the agent's stored knowledge of *processes, workflows, and action sequences* — it knows how to perform specific tasks or follow specific procedures.
- **In Simple Words:** Procedural memory is the agent's instruction manual or SOP (Standard Operating Procedure). It stores not facts but *how-tos* — step-by-step routines the agent should follow.
- **Real-Life Example:** A customer support agent that knows "if the user says they have not received their order after 7 days, follow this escalation process: Step 1 — confirm order ID, Step 2 — check logistics system, Step 3 — raise a refund ticket." This process is procedural memory.

**What Procedural Memory Enables:**

- Consistent behaviour across all users for specific types of requests
- Agents can follow multi-step workflows reliably without being re-instructed every time
- Makes agents predictable, compliant, and auditable in regulated industries

**How It Is Stored:**

- Often embedded in the **system prompt** as instructions
- Can also be stored as structured workflows, prompt templates, or tool-calling rules retrieved dynamically

---

### Comparing the Three Types of Long-Term Memory

| Memory Type | Stores | Example | Used For |
|---|---|---|---|
| **Episodic** | Past events and interactions | "Last session, the user asked about X" | Personalisation, continuity across sessions |
| **Semantic** | Facts and knowledge about the world | "Python uses indentation for code blocks" | Domain expertise, factual Q&A |
| **Procedural** | How-tos and workflows | "If the user complains, follow these 3 steps" | Consistent behaviour, SOPs, compliance |

![Long-term memory flavours — episodic (what happened), semantic (what is true), and procedural (what steps to follow)](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session13/session13-ltm-three-types.png)

---

> ### 🟩 Milestone — Full Memory Taxonomy Covered
>
> You have now completed the full picture of memory in AI agents — both short-term (Buffer, Window, Summary) and long-term (Episodic, Semantic, Procedural). From here, the focus shifts to two practical questions: *how does an agent decide what to save*, and *where is that memory actually stored*? These are the engineering decisions that turn memory theory into working systems.

---

> ### 🟦 Student Activity 3 — "What Kind of Memory Is This?"
>
> **Format:** Individual think → Instructor-led row-by-row reveal (Zoom)
>
> **Instructions:**
> A medical AI assistant stores the following items between sessions. For each item, classify it as **Episodic**, **Semantic**, or **Procedural** memory, and prepare one sentence explaining your reasoning.
>
> | Stored Item | Memory Type | Why? |
> |---|---|---|
> | "The patient's name is Meera. She is 34 years old, has type 2 diabetes, and prefers concise explanations." | ? | |
> | "Metformin is a first-line medication for type 2 diabetes. It reduces hepatic glucose production." | ? | |
> | "When a patient reports chest pain, always ask about duration, severity, and radiation before any recommendation." | ? | |
>
> **Goal:** Sharpen classification of the three long-term memory types using a single concrete scenario, and establish that real agents use all three together.

---

## How Agents Decide What to Remember

Here is a question that might have occurred to you: if long-term memory must be stored deliberately, *how does the agent decide what is important enough to save?*

This is one of the most interesting design challenges in agent systems, and it is not fully solved — there are different strategies, and each one has its trade-offs.

### Relevance vs Recency — The Two Competing Priorities

- **Recency Bias:** The most recent events are usually the most immediately relevant. A window memory strategy uses pure recency — it keeps the most recent N messages and drops everything else.
- **Relevance Bias:** Sometimes an event from 50 messages ago is more important than the last 5. For example, if the user mentioned a health condition early in the conversation, that is highly relevant even if it was said a long time ago.

Real-world agents often try to combine both: prioritise recent context by default, but also flag certain high-importance facts for retention.

### Common Approaches to Memory Selection

- **Rule-Based Flagging:** The agent is instructed (via system prompt) to explicitly extract and save certain types of information — for example, "always remember the user's name, location, and stated goal."
- **LLM-Driven Extraction:** At the end of a session or after a set number of turns, a secondary LLM call analyses the conversation and extracts key facts worth saving to long-term memory.
- **User-Controlled Memory:** The user explicitly tells the agent what to remember — "Please remember that I prefer formal responses." This is the simplest and most transparent approach.
- **Implicit Behavioural Learning:** More advanced agents observe what kinds of information were most useful in past responses and learn to prioritise storing similar information in future sessions.

---

## Implementing Basic Memory Strategies — How It Looks in an Agent Workflow

Even though this session is primarily theoretical, it is important to see a concrete picture of how these strategies map to actual agent code logic. Let us walk through simple pseudo-implementations of each strategy.

### Buffer Memory — Full History

```python
# Buffer Memory: Keep all messages in a list and pass them all every time

# This list stores the full conversation history
conversation_history = []

def chat_with_agent(user_message):
    # Add the new user message to the history list
    conversation_history.append({"role": "user", "content": user_message})

    # Call the LLM with the full history — no trimming, no summarising
    response = call_llm(messages=conversation_history)

    # Add the agent's response to the history as well
    conversation_history.append({"role": "assistant", "content": response})

    # Return the response to the user
    return response
```

**How the code works:**

- `conversation_history` is a Python list that holds every message from both the user and the agent
- Every time the user sends a message, it is appended to the list
- The entire list is passed to the LLM — so the model sees the complete history every time
- The agent's response is also stored in the list for the next turn
- Simple, accurate, but gets expensive and large as the conversation grows

---

### Window Memory — Keep Only the Last N Messages

```python
# Window Memory: Keep only the most recent N messages to control context size

# Define the window size — how many recent messages to keep
WINDOW_SIZE = 10

# The full history is stored here but only the last N are sent to the model
full_history = []

def chat_with_agent_windowed(user_message):
    # Add the new user message to the full history
    full_history.append({"role": "user", "content": user_message})

    # Slice the list — take only the last WINDOW_SIZE messages
    recent_history = full_history[-WINDOW_SIZE:]

    # Call the LLM with only the recent messages, not the full history
    response = call_llm(messages=recent_history)

    # Save the agent's response to the full history
    full_history.append({"role": "assistant", "content": response})

    # Return the response to the user
    return response
```

**How the code works:**

- `WINDOW_SIZE = 10` means we will pass at most 10 recent messages to the LLM
- `full_history[-WINDOW_SIZE:]` uses Python list slicing to grab only the last 10 items
- The full history is maintained in `full_history` for record keeping, but only the window is sent to the model
- This keeps token usage bounded and predictable — the cost does not grow with conversation length
- The trade-off: messages older than position 10 in the history are invisible to the model

---

### Summary Memory — Compress Old History into a Brief

```python
# Summary Memory: Periodically summarise old messages and replace them with a compact summary

# This will store the compressed summary of the conversation so far
running_summary = ""

# This stores only the most recent messages (the live window)
recent_messages = []

# How many new messages trigger a re-summarisation
SUMMARISE_AFTER = 8

def chat_with_agent_summary(user_message):
    global running_summary

    # Add the new user message to the recent messages list
    recent_messages.append({"role": "user", "content": user_message})

    # If recent messages exceed the threshold, compress them into a summary
    if len(recent_messages) >= SUMMARISE_AFTER:
        # Ask the LLM to summarise the recent conversation
        summary_prompt = f"Summarise this conversation briefly:\n{recent_messages}"
        new_summary = call_llm(messages=[{"role": "user", "content": summary_prompt}])

        # Update the running summary by combining old summary with new one
        running_summary = running_summary + " " + new_summary

        # Clear the recent messages — they are now captured in the summary
        recent_messages.clear()

    # Build the context: start with the summary, then add recent messages
    context = [{"role": "system", "content": f"Conversation so far: {running_summary}"}]
    context.extend(recent_messages)

    # Call the LLM with the summarised context
    response = call_llm(messages=context)

    # Add the agent's response to the recent messages
    recent_messages.append({"role": "assistant", "content": response})

    # Return the response to the user
    return response
```

**How the code works:**

- `running_summary` holds the ever-growing compressed version of past conversation
- `recent_messages` holds the live, uncompressed messages from the current window
- Every 8 messages, a separate LLM call is triggered to compress the recent messages into a short summary
- The old summary and new summary are merged into an updated `running_summary`
- The context passed to the model is always: [summary as system message] + [recent messages]
- This approach keeps context compact while preserving key facts from the entire conversation

---

## Introducing Storage Awareness — Where Does Long-Term Memory Live?

Now that you understand the types of long-term memory and when they are needed, the final piece is understanding *where* that memory is physically stored. This is what **storage awareness** means — as an agent designer, you need to choose the right storage backend based on the type of memory and how it will be retrieved.

This is a foundation concept — we will explore each storage type in much more depth in the upcoming sessions. For now, understand that there are three main options:

### Option 1 — In-Memory / Variable Storage (Temporary)

- Memory lives in a Python variable, list, or dictionary during the program's runtime
- Fast and simple, but completely lost when the program stops
- Only suitable for session-scoped short-term memory (like Buffer and Window memory)
- **Example:** `conversation_history = []` in our code examples above

### Option 2 — File-Based Storage (Simple Persistence)

- Memory is written to a file (text file, JSON file, CSV) on the disk
- Survives after the session ends — you can read it back the next time the program runs
- Good for small-scale long-term memory (user profiles, summaries, fact sheets)
- **Example:** Saving a user's profile and preferences to `user_memory.json`

### Option 3 — Database / Vector Store (Scalable Retrieval)

- Memory is stored in a proper database — either a traditional database (like PostgreSQL) or a **vector database** (like Pinecone, ChromaDB, or Weaviate)
- Vector databases are special — they store information as **numerical embeddings** and allow retrieval by *semantic similarity* ("find memories related to this topic")
- Essential for episodic and semantic memory in production-grade agents
- **Real-Life Example:** A legal AI agent stores thousands of case summaries in a vector database and can retrieve the 5 most relevant ones when answering a new legal query

| Storage Type | Persistence | Scale | Best For |
|---|---|---|---|
| **In-Memory Variable** | Session only | Very small | Short-term / buffer memory |
| **File (JSON/Text)** | Durable | Small to medium | Simple long-term storage |
| **Database / Vector Store** | Durable + searchable | Large scale | Episodic, semantic memory in production |

![Choosing where memory lives — fast in-session variables, simple file persistence, or scalable searchable databases including vector stores](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session13/session13-storage-tiers.png)

---

## Key Takeaways

- **Short-term memory lives in the context window** — it is the conversation history passed to the model every time, and it disappears when the session ends.
- **Buffer, Window, and Summary are three practical strategies** for managing short-term memory, each suited to different conversation lengths and cost requirements.
- **Long-term memory has three types** — Episodic (past events), Semantic (facts and knowledge), and Procedural (workflows and processes) — and each is stored and retrieved differently.
- **Agents must decide what to remember** by balancing recency and relevance, using rule-based flagging, LLM-driven extraction, or explicit user instructions.
- In the upcoming sessions, we will explore **external storage systems** like vector databases that make long-term memory retrievable at scale — laying the groundwork for truly intelligent, personalised agents.

---

## Important Commands, Libraries, and Terminologies

| Term / Concept | Meaning |
|---|---|
| **Short-Term Memory (STM)** | Memory that exists only during the current session, stored in the context window |
| **Long-Term Memory (LTM)** | Memory that persists across sessions, stored in external files, databases, or vector stores |
| **Context Window** | The maximum text (in tokens) an LLM can process in a single call |
| **Token** | The basic unit of text measurement for LLMs; roughly 1 token ≈ 0.75 words |
| **Buffer Memory** | Strategy that keeps the full, unmodified conversation history |
| **Window Memory** | Strategy that keeps only the last N messages; older messages are dropped |
| **Summary Memory** | Strategy that compresses older messages into a running summary, keeping context compact |
| **Episodic Memory** | Long-term memory of specific past events and interactions |
| **Semantic Memory** | Long-term memory of facts, knowledge, and domain expertise |
| **Procedural Memory** | Long-term memory of how-to processes and action workflows |
| **Vector Database** | A database that stores information as numerical embeddings and retrieves by semantic similarity |
| **Embedding** | A numerical representation of text that captures its meaning |
| **Semantic Search** | Searching for information by meaning rather than exact keyword match |
| **Relevance vs Recency** | Two competing priorities when deciding what memory to retain |
| **`conversation_history`** | A Python list used to store all messages in the session |
| **`full_history[-N:]`** | Python list slicing to retrieve the last N elements of a list |
| **`call_llm(messages=...)`** | Pseudo-function representing an API call to a language model with a message list |
| **SOP (Standard Operating Procedure)** | A documented step-by-step process — the real-world analogue of procedural memory |
