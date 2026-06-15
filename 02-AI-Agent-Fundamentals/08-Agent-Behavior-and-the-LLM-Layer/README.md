# Agent Behavior & Understanding the LLM Layer

## Setting the Stage — What Happened in the Last Session?

In the previous session, we studied how an AI agent is structured — Planning, Reasoning, Memory, and Action — and how it loops through Observe → Think → Act to get things done. We talked about the agent as a "smart personal secretary" that works toward a goal autonomously. But here is the big question we left unanswered: **what is actually doing the thinking inside the agent?** Who — or what — is reading the goal, making the plan, and deciding on the next step?

The answer is a **Large Language Model** — or an **LLM**. In this session, we are going to open the "thinking box" of an AI agent and understand exactly what is inside. By the end of this session, you will understand what an LLM is, what it can and cannot do, who builds these models, how agents use them, and how the technology works at a high level. No formulas, no heavy math — just clear concepts with real examples.

---

## What Is a Large Language Model (LLM)?

Let us start from the very beginning. You have been using language your whole life — you read, write, speak, and understand. But teaching a *computer* to do the same thing is extraordinarily hard. For decades, computers could only handle language in very rigid, rule-based ways. Then came a breakthrough: the **Large Language Model**.

- **Official Definition:** A **Large Language Model (LLM)** is a type of artificial intelligence model that has been trained on massive amounts of text data and can understand, generate, and interact with human language in a flexible, context-aware manner.
- **In Simple Words:** An LLM is a very, very smart text-processing machine. You give it text as input, and it gives you text as output. That is the core idea. Text in → Text out.
- **Real-Life Example 1 — The Brilliant Scholar:** Imagine a scholar who has read *every book, every article, every website, every forum post, and every document ever written in every language* — billions and billions of pages. Now you can walk up to this scholar and ask them *anything*, and they can answer in fluent, natural language. They can write essays, summarize reports, translate languages, solve problems, and hold conversations. That scholar is essentially what an LLM is — except it exists as a computer program.
- **Real-Life Example 2 — The Autocomplete That Grew Up:** You have used autocomplete on your phone's keyboard. You type "I am going to" and it suggests "the market" or "college." That is a very tiny, basic version of language prediction. Now imagine that same autocomplete, but trained on billions of documents, with thousands of times more power — so instead of suggesting one word, it can write full paragraphs, answer complex questions, and even write code. That is an LLM.

**The Three Words in "Large Language Model" — What They Mean:**

| Word | What It Means | Simple Way to Think About It |
|---|---|---|
| **Large** | The model has billions of parameters (internal settings) and was trained on an enormous amount of text data | Like a student who has studied for 10,000 hours across thousands of subjects |
| **Language** | It works specifically with human language — reading and generating text | It speaks your language — literally |
| **Model** | It is a mathematical system that has learned patterns from data | Like a very complex formula that has been fine-tuned over millions of examples |

![LLM core behavior — text in, text out](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session08/session08-01-llm-text-in-text-out.png)

---

## The Core Behavior of an LLM: Text In → Text Out

The single most important thing to remember about an LLM is its core behavior. It is beautifully simple:

**You give it text → It gives you text back.**

That is it. Everything else — answering questions, writing stories, summarizing documents, translating languages, writing code — is a *variation* of this single pattern.

- **Input (what you give it):** Any text — a question, an instruction, a paragraph, a document, a conversation history.
- **Output (what it gives back):** Any text — an answer, a continuation, a summary, a translation, code, a list.

**Simple Examples of Text In → Text Out:**

| What You Give the LLM (Input) | What the LLM Returns (Output) |
|---|---|
| "What is the capital of India?" | "The capital of India is New Delhi." |
| "Translate 'Hello, how are you?' into Hindi." | "नमस्ते, आप कैसे हैं?" |
| "Summarize this paragraph in 2 sentences: [paragraph]" | A 2-sentence summary of that paragraph |
| "Write a Python function to add two numbers." | A complete Python function with the code |
| "You are a helpful chef. Suggest a dish using paneer and spinach." | "You could make Palak Paneer! Here is a simple recipe..." |
| "Continue this story: Rohan opened the old door and saw..." | "...a staircase leading down into the darkness. He hesitated, then took the first step." |

**The Critical Insight Here:**
- Notice that the LLM does not "know" in advance what kind of task you are giving it. It just reads whatever text you give, and responds with what seems like the most appropriate text continuation.
- It does not have a separate "question-answering mode" and a "story-writing mode." The *same* model handles all of these — because all of them are just variations of "text in → text out."

---

## The LLM as the "Brain" of an AI Agent

Now let us bring this back to what you already know. In the last session, we talked about the four components of an agent: Planning, Reasoning, Memory, and Action. We said the agent "thinks" and "plans." But *who* is doing the thinking and planning?

The answer is the **LLM**. The LLM is the **brain** of the agent.

- **Official Definition:** In an agentic system, the LLM acts as the **central reasoning engine** — it receives the current context (goal, memory, tool results), processes it, and generates either a decision, a plan, or an action instruction.
- **In Simple Words:** Every time the agent needs to "think" — whether it is making a plan, deciding which action to take, or evaluating a result — it is *asking the LLM a question and reading its answer*.
- **Real-Life Analogy — The CEO and the Staff:** Think of an AI agent like a company. The LLM is the **CEO** — the decision-maker, the thinker, the one who says "Here is what we will do next." The tools (search engine, database, API) are the **staff** — they execute the CEO's instructions. The CEO (LLM) thinks; the staff (tools) act.

![The LLM as the agent’s brain — orchestrates memory, tools, and decisions](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session08/session08-02-llm-brain-agent.png)

**How the LLM Plugs Into the Agent Loop:**

You remember the Observe → Think → Act loop from the last session. The LLM powers the **Think** stage:

![Observe → Think → Act — the LLM runs inside the Think stage](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session08/session08-03-llm-in-think-stage.png)

```
[ Agent receives input or tool result ]
              ↓
         OBSERVE
  (gather context, memory, tool output)
              ↓
          THINK  ←── LLM IS HERE
  (send context to LLM → LLM decides
   what to plan or do next)
              ↓
           ACT
  (execute the LLM's decision using tools)
              ↓
     [ loop back to Observe ]
```

- In every single "Think" cycle, the agent sends a carefully constructed text to the LLM.
- The LLM reads it and replies with text — and that text *is* the thinking. It might say: "I should search for more information." or "The answer is X." or "Next, I need to call the payment API."
- The agent reads the LLM's response and turns it into the next action.

**A Concrete Mini-Example:**
- User says to the agent: "What is the weather in Mumbai today?"
- The agent (in the Think stage) sends this to the LLM: *"The user wants to know today's weather in Mumbai. You have access to a weather tool. Decide what to do."*
- The LLM replies: *"I should call the weather API with the city = Mumbai."*
- The agent reads this and executes the action: calls the weather API.
- The API returns: "Mumbai: 34°C, Humid, Partly Cloudy."
- The agent sends this result back to the LLM: *"The weather tool returned: Mumbai 34°C, Humid, Partly Cloudy. Now respond to the user."*
- The LLM replies: *"Today's weather in Mumbai is 34°C with high humidity and partly cloudy skies. Quite hot — stay hydrated!"*
- The agent shows this response to the user.

In this whole process, the LLM was the "thinker" at every stage. The agent's code just orchestrated the loop.

---

## What Can an LLM Actually Do? — Exploring Its Capabilities

The LLM is powerful because it is not trained on just one type of task. It has seen so much text — in so many forms — that it has developed broad, general capabilities. Let us go through the main ones.

**Capability 1: Answering Questions**
- The most basic capability. You ask something, it answers.
- **Example:** "Who invented the telephone?" → "Alexander Graham Bell invented the telephone in 1876."
- The LLM does not look this up like Google. It already "knows" it from training data.
- **Important nuance:** It answers based on what it learned during training — not real-time data. So if you ask "Who won the cricket match yesterday?" — it may not know, because that happened after its training cutoff.

**Capability 2: Text Summarization**
- You give it a long document, article, or conversation — it produces a short, clear summary.
- **Example:** Give it a 5-page government policy document → it returns a 3-bullet-point summary.
- This is incredibly useful in the real world — imagine summarizing 100 customer complaints into 5 key themes in seconds.

**Capability 3: Text Generation and Creative Writing**
- You give it a topic or a starting point — it generates coherent, fluent text.
- **Example:** "Write a professional email to a client apologizing for a delayed delivery." → The LLM writes a complete, polished email.
- **Another Example:** "Write a short story about a robot who learns to cook." → Full story, characters, plot, ending.

**Capability 4: Language Translation**
- It can translate between dozens of languages — often better than simple rule-based translators.
- **Example:** "Translate this paragraph from English to Tamil." → Accurate Tamil translation.

**Capability 5: Code Writing and Explanation**
- It can write code in Python, JavaScript, SQL, and many other languages.
- **Example:** "Write a Python function that takes a list of numbers and returns the average." → The LLM writes the complete function.
- It can also *explain* existing code in plain English — very useful when you are learning to code.

**Capability 6: Classification and Extraction**
- Given a piece of text, it can identify categories, extract specific information, or label sentiment.
- **Example:** "Is this customer review positive or negative? Review: 'The product arrived late and was broken.'" → "Negative."
- **Another Example:** "Extract the name, date, and amount from this invoice text." → The LLM extracts the three fields.

**Capability 7: Reasoning and Problem-Solving**
- It can work through logical problems, math word problems, and multi-step questions.
- **Example:** "If a train leaves Delhi at 8 AM at 90 km/h and another leaves Mumbai at 10 AM at 120 km/h, when do they meet?" → The LLM reasons through the problem and gives an answer.

**Why This Versatility Matters for Agents:**
- An AI agent needs a "brain" that can do many different things — plan, reason, write, summarize, extract, and decide.
- A traditional hardcoded system would need a separate program for each capability. An LLM handles all of them in one place, with one interface.
- This is why LLMs are the ideal brain for AI agents — they are *generalist thinkers*.

---

## Understanding Prompts — The Instructions That Control the LLM

Here is one of the most important concepts in working with LLMs: the **prompt**. The output of an LLM is entirely shaped by what you *give* it as input. Change the input → the output changes completely. The text you give to an LLM is called a **prompt**.

- **Official Definition:** A **prompt** is the input text you provide to an LLM to instruct it on what task to perform and how to respond. It controls the model's behavior, tone, format, and the nature of the output.
- **In Simple Words:** The prompt is your instruction to the LLM. It is like telling a very capable assistant exactly what you want them to do.
- **Real-Life Analogy:** Imagine you walk into a stationery shop and say: "Give me a pen." You will get some random pen. Now you say: "Give me a blue ballpoint pen, medium nib, that writes smoothly on thick paper." You get exactly what you want. The *more specific and clear* your request, the *better the output*. Prompts work the same way.

**How Different Prompts Produce Different Outputs from the Same LLM:**

| Prompt (Input) | Output (What LLM Returns) |
|---|---|
| "Explain photosynthesis." | A general, school-level explanation |
| "Explain photosynthesis in 3 bullet points for a 10-year-old." | Simple, 3-bullet explanation |
| "Explain photosynthesis like you are a stand-up comedian." | A funny, lighthearted explanation with jokes |
| "Explain photosynthesis in Hindi." | A Hindi-language explanation |
| "You are a biology professor. Explain photosynthesis formally." | A detailed, technical, formal explanation |

- Notice: the *same LLM*, the *same topic*, but five completely different outputs — because the prompt changed.
- **The key insight:** In an AI agent, when the agent "thinks," it is constructing a carefully designed prompt and sending it to the LLM. The quality of the agent's thinking depends heavily on the quality of the prompts it constructs.

![Same model, different prompts — different outputs](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session08/session08-04-prompt-controls-output.png)

**What a Prompt Typically Contains in an Agent:**
- **Role:** "You are a helpful customer support agent."
- **Context:** "The user's order ID is #56789. It was placed 3 days ago and has not shipped yet."
- **Task:** "Decide the best way to respond to the user's frustration."
- **Format instruction:** "Respond in 2-3 short sentences. Be empathetic."

All of this is just *text* — assembled by the agent's code and sent to the LLM. We will dive much deeper into prompt design in a dedicated later session. For now, just understand: **the prompt is how you talk to the LLM, and it controls everything about the output**.

---

## Where LLMs Are Strong — The Genuine Superpowers

LLMs are genuinely extraordinary at certain things. Let us be specific about where they shine.

**Strength 1: Natural Language Understanding**
- LLMs understand human language the way humans do — they grasp context, nuance, tone, and implied meaning.
- **Example:** If a user says "Can you not make it simpler?" — a traditional system would be confused (is that a "yes" or a "no"?). An LLM understands: the user wants a simpler version.
- They understand slang, idioms, sarcasm, and informal writing — not just formal, structured sentences.

**Strength 2: Generalization Across Topics**
- They are not specialists in one subject. They have broad knowledge across science, history, languages, business, law, medicine, coding, and much more.
- **Example:** You can ask the same LLM to write a legal contract clause in the morning and explain a chemistry reaction in the afternoon.

**Strength 3: Flexible Output Format**
- They can produce output in any format you specify — a bullet list, a table, a Python class, a JSON object, a poem, a formal report, a casual message.
- This flexibility is essential for agents that need to pass structured data between tools.

**Strength 4: In-Context Learning**
- You can give the LLM a few examples *inside the prompt* and it immediately picks up the pattern — without any special programming.
- **Example:** Give it 3 examples of customer complaints labeled "refund" or "exchange," then give it a new complaint — it correctly labels it, having learned the pattern from just those 3 examples.

**Strength 5: Multi-Step Reasoning for Language-Based Problems**
- For problems where the solution involves interpreting text, drawing logical conclusions, or writing structured responses — LLMs reason impressively well.
- They can solve riddles, logic puzzles, and multi-step word problems with accuracy.

---

## Where LLMs Are Weak — The Limitations You Must Know

Now here is the honest part. LLMs are powerful, but they have real, important limitations. Understanding these is *not* optional — it is essential if you ever design or use agentic systems professionally.

**Limitation 1: Hallucination — Confidently Wrong**

This is the most famous and most dangerous limitation of LLMs.

- **Official Definition:** **Hallucination** is when an LLM generates information that sounds completely plausible and confident — but is factually incorrect, made-up, or nonsensical.
- **In Simple Words:** The LLM "makes things up" but presents them with full confidence, as if they were true.
- **Real-Life Analogy:** Imagine a student in an exam who does not know the answer to a question. Instead of leaving it blank, they *write something that sounds convincing* — hoping the examiner will not notice. Except the LLM is not even trying to deceive — it genuinely does not "know" what it does not know. It just keeps generating plausible-sounding text.
- **Example 1:** Ask an LLM: "What books has Professor XYZ of IIT Delhi written?" If Professor XYZ is not famous enough to be in the training data, the LLM might invent two or three book titles that sound realistic. The titles do not exist. But the LLM stated them as facts.
- **Example 2:** Ask an LLM for a legal citation. It might give you a court case name, a year, and a judgment summary — all of which look completely real — but the case never happened.
- **Why This Happens:** The LLM does not have a database of facts it looks up. It generates text based on *patterns it learned*. Sometimes those patterns lead it to produce plausible-but-wrong completions.
- **Why This Matters for Agents:** If an AI agent uses an LLM to gather facts and never verifies them, it might take *real-world actions* based on hallucinated information — like sending a report full of made-up statistics, or referencing a policy that does not exist.

![Hallucination — plausible text is not the same as verified fact](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session08/session08-05-hallucination-limitation.png)

**Limitation 2: No Real-Time Knowledge**
- LLMs are trained on data up to a specific date — called the **training cutoff**. They have no knowledge of events that happened after that date.
- **Example:** If an LLM's training cutoff is early 2024 and you ask it "Who won the 2025 IPL?", it will either say it doesn't know — or worse, make up an answer.
- **In agents:** This is why agents often need to use a *search tool* to fetch real-time information. The LLM alone cannot be trusted for current facts.

**Limitation 3: Poor at Precise Mathematics**
- LLMs are trained on text, not mathematics. They can often get simple arithmetic right, but they struggle with complex, multi-step calculations.
- **Example:** Ask an LLM to multiply two 10-digit numbers. There is a good chance it gets it wrong.
- **The Fix in Agents:** Agents route math problems to a code execution tool — the LLM generates Python code, runs it, and returns the computed result. This way, the calculation is done by the computer (which is accurate), not the LLM (which is not).

**Limitation 4: Inconsistency**
- The same prompt can produce slightly different responses on different runs, because LLMs have a degree of randomness in their generation process.
- **Example:** Ask the same question twice in two separate conversations — the wording of the answer may differ slightly, and in rare cases, even the facts.
- **Why This Matters:** In systems where consistency is critical (legal, medical, financial), raw LLM output must always be reviewed and validated.

**Limitation 5: Limited "Working Memory" During a Session**
- The LLM can only process a certain amount of text at one time — this is called the **context window**. If a conversation gets very long or a document is very large, older parts get "forgotten."
- **Example:** In a very long conversation (100 messages), the LLM might forget what was said in message #5 by the time it is responding to message #95.
- We will talk more about this when we discuss tokens later in this session.

---

## Who Builds These LLMs? — The Major Model Providers

You do not build an LLM from scratch to use it. Just like you do not build a car engine to drive a car — you buy the car and drive it. Similarly, large technology companies spend enormous resources (thousands of GPUs, billions of dollars, years of training) to build LLMs, and then they offer access to these models as a **service**.

These companies are called **Model Providers**.

**Provider 1: OpenAI**
- **Based in:** San Francisco, USA
- **Their Models:** GPT-3.5, GPT-4, GPT-4o (the "o" stands for Omni — it can handle text, voice, and images).
- **Famous Product:** ChatGPT — the chatbot that introduced billions of people to LLMs.
- **Who Uses It:** Businesses, developers, researchers — through OpenAI's API.
- **Simple Analogy:** Think of OpenAI as the company that manufactures one of the best "thinking engines" in the world. ChatGPT is like their showroom where you can try it. The API is the service door where developers pick up the engine and put it into their own products.

**Provider 2: Google DeepMind**
- **Based in:** London, UK (with major operations in the USA)
- **Their Models:** Gemini (previously known as Bard, and before that, LaMDA). Google's models are deeply integrated with Google Search and Google Workspace.
- **Famous Product:** Google Gemini — available at gemini.google.com.
- **Interesting Fact:** Google was one of the *inventors* of the Transformer architecture (the technology that powers all modern LLMs). We will talk about Transformers shortly.
- **Simple Analogy:** If OpenAI is like one premium car brand, Google DeepMind is another premium brand — with its own engine design, its own strengths, and its own showroom.

**Provider 3: Anthropic**
- **Based in:** San Francisco, USA
- **Their Models:** Claude (Claude 2, Claude 3 — in versions Haiku, Sonnet, Opus).
- **Known For:** A strong focus on AI safety — building models that are less likely to produce harmful, manipulative, or dangerous outputs.
- **Simple Analogy:** If OpenAI and Google are like sports cars — fast and powerful — Anthropic's Claude is like a car designed with extra safety features — still fast, but with an emphasis on responsible, safe behavior.

**Provider 4: Meta AI**
- **Based in:** Menlo Park, USA (Facebook's parent company)
- **Their Models:** LLaMA (Large Language Model Meta AI) — LLaMA 2, LLaMA 3.
- **What Makes It Different:** Meta's LLaMA models are **open-source** — meaning Meta has released the model weights (the "recipe") for free. Anyone can download the model and run it on their own computers.
- **Why This Matters:** Most other providers keep their models proprietary (secret). Meta's open-source approach has enabled thousands of researchers and developers to build their own custom LLMs without depending on a paid API.

**A Quick Comparison of Major Providers:**

| Provider | Key Model | Known For | Access Type |
|---|---|---|---|
| **OpenAI** | GPT-4o | Power, versatility, most widely used | Paid API + ChatGPT |
| **Google DeepMind** | Gemini | Integration with Google services, multimodal | Paid API + Gemini App |
| **Anthropic** | Claude 3 | Safety-focused, strong long-context ability | Paid API + Claude App |
| **Meta AI** | LLaMA 3 | Open source, free to use and customize | Free download |

**An Important Note — These Are All "LLMs" Underneath:**
- Despite coming from different companies, having different names, and having different strengths, all of these models share the same fundamental technology: the **Transformer architecture**.
- Think of it like different smartphone brands — Samsung, Apple, OnePlus. They look different, have different software, but all run on a similar underlying technology (a processor, a screen, a battery, an OS). LLMs are similar — different brands, same fundamental architecture.

---

## How LLMs Are Actually Used — APIs and Access

You now know who builds LLMs. But how do you actually *use* one in your code or your application? The answer is: through an **API**.

- **Official Definition:** An **API (Application Programming Interface)** is a way for one software system to talk to another. In the context of LLMs, the API lets your code send a prompt (text) to the model provider's servers and receive the model's output (text) back.
- **In Simple Words:** An API is like a waiter at a restaurant. You (the developer) are the customer. The LLM is the kitchen. You give your order to the waiter (the API). The waiter goes to the kitchen, gets the food (the model's response), and brings it back to you.
- **Real-Life Analogy:** Think of electricity. You do not generate your own electricity at home. You plug into the grid and use it. The electricity company (like OpenAI) generates the power (runs the huge model on massive servers). Your device (your Python code) plugs into the grid (the API) and uses it.

![Calling an LLM through an API — prompt out, response back](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session08/session08-06-api-flow.png)

**How It Works — Step by Step (Conceptual, No Deep Code):**
- Step 1: You write a Python program (or any code).
- Step 2: Your code sends a text prompt to the LLM provider's server using an API call. This is like sending a text message.
- Step 3: The provider's server passes the prompt to the actual LLM (which is running on very powerful hardware — think hundreds of GPUs).
- Step 4: The LLM processes the prompt and generates a response.
- Step 5: The response travels back through the API to your Python code.
- Step 6: Your code reads the response and uses it — displays it to the user, makes a decision, calls another tool, etc.

**A Conceptual Look at the API Interaction:**
```python
# This is a simplified conceptual example — actual API code comes in a later session
import openai

# You give the LLM a prompt (your instruction)
prompt = "Summarize the following text in 2 sentences: [long article text here]"

# The API call sends your prompt to OpenAI's servers
response = openai.chat.completions.create(
    model="gpt-4o",        # which LLM model to use
    messages=[{"role": "user", "content": prompt}]
)

# The LLM's reply comes back as text
print(response.choices[0].message.content)
# Output: "The article discusses... [2-sentence summary]"
```

- You can see the pattern: **Text goes in** (the prompt), **Text comes back** (the response). This is the text in → text out pattern we discussed, now in code form.
- **You do not need to understand every line right now.** The important takeaway is: LLMs are accessed remotely, over the internet, using a simple text-based interface (the API).

**Why API Access Matters for Agents:**
- An AI agent uses the LLM API every time it needs to "think."
- In a complex agentic task with 15 steps, the agent might call the LLM API 15 times — once for each "Think" cycle in the loop.
- Each API call costs money (a small amount, based on how much text was processed). This is why understanding **tokens** — which we cover next — is important.

---

## Understanding Tokens — How LLMs "See" Text

Here is something that surprises most people: an LLM does not read text the way you and I do. It does not see letters, words, or sentences directly. It sees **tokens**.

- **Official Definition:** A **token** is a small chunk of text — it could be a whole word, part of a word, a punctuation mark, or even a space — that an LLM uses as its basic unit of processing. Text is broken into tokens before it is fed to the model.
- **In Simple Words:** Think of tokens as the "bite-size pieces" the model chews text into before digesting it. Words are not the atoms of an LLM — tokens are.
- **Real-Life Analogy:** Think of how you eat a roti. You do not swallow the whole roti at once. You tear it into pieces and eat piece by piece. Tokenization is the LLM "tearing the text into pieces" — each piece is a token — before it processes the text.

**How Tokenization Works — Examples:**
- "Hello" → 1 token
- "Hello, how are you?" → 5 tokens (Hello / , / how / are / you)
- "Unbelievable" → might be 3-4 tokens (Un / be / liev / able) — long or uncommon words get split
- "I love biryani" → 4 tokens (I / love / biry / ani) — even "biryani" might be split because it is less common in English training data
- A rough rule of thumb: **1 token ≈ 0.75 words** in English, or about **4 characters** on average.

![Tokens — text split into chunks the model processes](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session08/session08-07-tokens-chunking.png)

**Why Tokens Matter — Three Practical Reasons:**

**Reason 1: The Context Window Limit**
- Every LLM has a **context window** — a maximum number of tokens it can process at one time (in one API call).
- GPT-4 can handle around 128,000 tokens. Claude 3 Opus can handle 200,000 tokens.
- If your input (prompt + conversation history) exceeds this limit, the model cannot process it — or it forgets the earlier parts.
- **Example:** If you have a very long document (say, 500 pages), you cannot just paste it all into one prompt. You would need to break it into chunks and process them separately.

**Reason 2: Cost**
- API providers charge you based on the number of tokens processed — both the input tokens (what you send) and the output tokens (what the model generates).
- A longer prompt = more tokens = more cost.
- A short, efficient prompt = fewer tokens = lower cost.
- **Example:** If you are building an agent that processes 10,000 customer queries per day, the total token count (and cost) can add up very quickly. Efficient prompt design directly saves money.

**Reason 3: Speed**
- Processing more tokens takes more time. Shorter prompts lead to faster responses.
- In real-time applications (like a chatbot), speed matters a lot for user experience.

**You Do Not Need to Count Tokens Manually:**
- LLM providers give you tools to count tokens. In Python, libraries like `tiktoken` (for OpenAI models) can count tokens before you send a prompt.
- For now, just understand the *concept*: text is broken into bite-size tokens, and the number of tokens affects limits, cost, and speed.

---

## The Transformer Architecture — The Technology Behind LLMs (Intuition Only)

You now know *what* LLMs do and *how* they are used. Let us briefly look at *why* they are so good — the underlying technology. We are going to explain this using intuition and analogies only. No math, no formulas.

**The Key Question: What Was the Big Invention?**

Before 2017, language AI models were much simpler and weaker. They could handle short sequences of text reasonably well, but struggled with long, complex sentences and documents. Then, in 2017, a team at Google published a research paper titled **"Attention Is All You Need."** This paper introduced the **Transformer architecture** — and it changed everything.

- **Official Definition:** A **Transformer** is a type of neural network architecture designed to process sequential data (like text) by using a mechanism called **attention** to understand relationships between all parts of the input simultaneously.
- **In Simple Words:** The Transformer is the specific engine design that makes LLMs so powerful. It is the "blueprint" that all major LLMs — GPT, Gemini, Claude, LLaMA — are built on.
- **Historical Analogy:** Before the Transformer, language AI models were like bicycles — they could move, but slowly and with effort. The Transformer was the invention of the car engine. Same general purpose (moving), but a completely different level of capability.

**Why Was This So Revolutionary? — Before vs. After:**

- **Before Transformers (older models like RNN/LSTM):** These models read text *one word at a time, in sequence*, like reading a sentence word by word in strict order. By the time they reached the end of a long sentence, they had "forgotten" the beginning.
- **With Transformers:** The model processes the *entire input at once*, and can look at any word in relation to any other word — no matter how far apart they are in the text. This is what **attention** does.

---

## Understanding Attention — How the Model Focuses on What Matters

The most powerful idea inside the Transformer is called **Attention**. Let us build an intuition for this.

**What Is Attention?**

- **Official Definition:** **Attention** is the mechanism within a Transformer model that allows it to weigh the importance of different words in the input when processing each word — so that it can capture relationships and context across the entire sentence.
- **In Simple Words:** Attention is the model's ability to ask: "For each word I am currently processing, which *other* words in the sentence are most important and relevant?" Then it pays more "attention" to those words.

**The Classic Example — The Word "It":**

Consider the sentence: *"The trophy did not fit in the suitcase because it was too large."*

What does "it" refer to here? Is "it" the trophy or the suitcase?
- The answer is: "it" = the trophy (because the trophy was too large to fit).
- A human brain instantly figures this out by connecting "it" to "trophy" based on context.
- **Attention allows the LLM to do the same thing.** When processing the word "it," the attention mechanism identifies that "trophy" and "large" are the most contextually relevant words — so the model "pays attention" to them. This tells the model that "it" refers to the trophy.

**Another Example — "Bank":**

Consider: *"I sat by the river bank and read a book."* vs. *"I deposited money at the bank."*

The word "bank" means completely different things in these two sentences. Attention allows the model to look at all the surrounding words ("river," "sat," "read" vs. "deposited," "money") and figure out which meaning is correct — automatically.

**Analogy — The Spotlight in a Concert:**
- Imagine a large concert stage with 50 musicians. When the lead singer starts performing, a spotlight follows them.
- But when the guitar solo happens, the spotlight moves to the guitarist.
- The spotlight doesn't illuminate everything equally — it focuses on what is *most important for the current moment*.
- Attention in a Transformer works like that spotlight — for every word being processed, it shines the brightest light on the words that matter most for understanding that word.

![Attention links words across the sentence — e.g. resolving “it” from context](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session08/session08-08-attention-mechanism.png)

**Why Attention Made LLMs So Powerful:**
- Because every word can "look at" and "consider" every other word in the input, the model understands context far better than older models.
- Long-range dependencies — where a word at the start of a paragraph determines the meaning of a word at the end — are handled naturally.
- This is why LLMs can hold coherent, context-rich conversations across many paragraphs, something older models could not do.

**Important Note for This Stage:**
- You do not need to understand the mathematics of attention right now. The key intuition is: **Transformers allow every word to consider every other word** — and that rich understanding of context is what makes LLMs able to produce fluent, context-aware language.

---

## Connecting the LLM Back to the Full Agent Flow

Now let us put all the pieces of this session together and see how the LLM connects to the complete agentic system we learned about in the last session.

**The Complete Picture:**

![User → agent (memory, tools, LLM) → tools execute → loop until done](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session08/session08-09-full-agent-llm-flow.png)

```
USER INPUT
    ↓
AGENT (the orchestrator — built in Python)
    │
    ├── Memory (short-term: current context; long-term: user profile)
    │
    ├── Tools (search engine, API, database, calculator)
    │
    └── LLM (the brain — GPT-4, Gemini, Claude, etc.)
              ↑
       (Prompt is sent to LLM)
       (LLM returns decision/text)
              ↓
AGENT executes the LLM's decision using Tools
    ↓
RESULT goes back to AGENT
    ↓
AGENT loops (Observe → Think → Act) until done
    ↓
FINAL OUTPUT to User
```

**The LLM's Specific Role at Each Stage of the Loop:**

| Agent Loop Stage | What the LLM Does |
|---|---|
| **Observe** | The agent gathers context. The LLM is not active here yet. |
| **Think — Plan** | The agent sends the goal to the LLM with a prompt like "Break this goal into steps." The LLM returns a numbered plan. |
| **Think — Reason** | The agent sends a prompt like "Given these search results, which is most relevant?" The LLM analyzes and decides. |
| **Think — Decide Next Action** | The agent sends a prompt like "What tool should I use next?" The LLM chooses: "Use the weather API." |
| **Act** | The agent executes the tool call. The LLM is not active during the execution itself. |
| **Observe (next round)** | The tool result is sent to the LLM: "Here is what the tool returned. What should we do with this?" |

**The Key Insight:**
- The LLM is not running *constantly*. It is called at specific decision points — when the agent needs to think.
- Between LLM calls, the agent code (Python) is handling the execution — calling APIs, managing memory, looping the flow.
- The LLM is the *thinker*. Python is the *executor*.

---

## When Agents Go Wrong Because of LLM Failures

Let us look at some concrete examples of how LLM limitations cause real problems in agentic systems. This is important because you will one day be building or evaluating these systems.

**Failure Example 1: The Hallucinating Research Agent**
- Scenario: An agent is asked to "Write a report on the top 5 hospitals in Hyderabad for cardiac care."
- What goes wrong: The LLM confidently lists 5 hospitals, includes their addresses, bed counts, and doctor names. Some of these details are hallucinated — the addresses are wrong, one hospital does not even exist.
- Why it happened: The LLM generated plausible-sounding information based on patterns, not verified facts.
- The fix: A well-designed agent would use a *search tool* to look up real information, and the LLM would *summarize that real information* — not generate facts from memory.

**Failure Example 2: The Out-of-Date Agent**
- Scenario: A user asks an AI financial assistant: "What is the current interest rate on FD accounts at SBI?"
- What goes wrong: The LLM's training cutoff was 18 months ago. It confidently states a rate that is now outdated.
- Why it happened: The LLM does not know it is outdated. It states what it learned during training as if it is current fact.
- The fix: The agent should use a real-time search tool or a bank API to fetch the current rate, then have the LLM format and present the answer.

**Failure Example 3: The Inconsistent Agent**
- Scenario: A company builds an agent to grade 1,000 student essays on a scale of 1-10. They run the same essay through the agent twice.
- What goes wrong: The first run gives a score of 7. The second run gives a score of 6. The criteria for grading feel slightly different each time.
- Why it happened: LLMs have a temperature parameter — a degree of randomness in output. This makes outputs slightly different each time.
- The fix: For tasks requiring precise consistency (grading, legal review, medical assessment), the temperature should be set very low, and a structured scoring rubric should be included in the prompt.

**Failure Example 4: The Math-Challenged Agent**
- Scenario: An accounting agent is asked to "Calculate the total revenue across these 50 invoices and give me the percentage growth vs last year."
- What goes wrong: The LLM attempts the arithmetic itself and makes errors in the 13th and 24th invoice totals — producing a wrong final number.
- Why it happened: LLMs are not calculators. They approximate arithmetic.
- The fix: The agent should use a code execution tool — ask the LLM to write Python code for the calculation, run the code, and return the actual computed result.

---

## Putting It All Together: The Big Picture of This Session

Let us do a quick recap of everything we covered today, in one connected flow:

- An **LLM** is a large, powerful text-processing AI model. Text in → Text out.
- It is the **brain** of an AI agent — it handles all the reasoning, planning, and decision-making inside the agent.
- LLMs are accessed through **APIs** — your Python code sends a prompt (text), and the model returns a response (text).
- The text you give the LLM is called a **prompt** — it controls everything about the output.
- LLMs are built by major providers: **OpenAI (GPT), Google DeepMind (Gemini), Anthropic (Claude), Meta (LLaMA)**.
- Text is processed by LLMs as **tokens** — bite-size chunks. Token count affects limits, cost, and speed.
- LLMs are built on the **Transformer architecture**, which uses **attention** to understand context across entire documents.
- LLMs have real limitations: **hallucinations, no real-time knowledge, poor math, inconsistency** — all of which must be handled carefully in agent design.
- In the agent loop, the LLM powers the **Think** stage. Python code powers the **Act** stage. Together, they make a complete, functional agent.

---

## Quick Reference: Important Terms & Concepts

| Term | Simple Meaning | Example |
|---|---|---|
| **LLM (Large Language Model)** | A powerful AI model trained on massive text data that can understand and generate language | GPT-4, Gemini, Claude, LLaMA |
| **Text In → Text Out** | The core behavior of an LLM — give it text, get text back | Asking a question → getting an answer |
| **Prompt** | The input text you give to the LLM; it controls the model's behavior | "Summarize this in 3 bullet points" |
| **Hallucination** | When an LLM generates confident but factually wrong information | LLM invents a book title that doesn't exist |
| **Training Cutoff** | The date after which the LLM has no knowledge of events | A model trained until early 2024 won't know 2025 events |
| **Token** | The basic unit of text an LLM processes (roughly 0.75 words per token) | "biryani" might become 2-3 tokens |
| **Context Window** | The maximum number of tokens an LLM can process in one call | GPT-4o: ~128,000 tokens |
| **Model Provider** | A company that builds and offers LLMs as a service | OpenAI, Google DeepMind, Anthropic, Meta |
| **API (Application Programming Interface)** | The interface your code uses to send prompts to an LLM and receive responses | Sending a POST request to OpenAI's API |
| **Transformer** | The neural network architecture that powers all modern LLMs | Introduced in Google's 2017 "Attention Is All You Need" paper |
| **Attention Mechanism** | The part of a Transformer that lets every word "look at" every other word for context | Understanding what "it" refers to in a complex sentence |
| **OpenAI / GPT** | One of the most widely used LLM providers; makes GPT-3.5, GPT-4, GPT-4o | ChatGPT is built on GPT |
| **Google DeepMind / Gemini** | Google's LLM; integrates with Google Search and Workspace | Gemini App at gemini.google.com |
| **Anthropic / Claude** | Safety-focused LLM provider; known for long-context handling | Claude 3 Opus, Sonnet, Haiku |
| **Meta / LLaMA** | Open-source LLM provider; anyone can download and use the model | LLaMA 3 available free on Meta's website |
| **Temperature** | A setting that controls how random/creative the LLM's output is (0 = very consistent, 1+ = more creative) | Set low for grading; set higher for creative writing |
| **In-Context Learning** | Teaching the LLM a new pattern by putting examples directly in the prompt | Give 3 labeled examples → model learns to label new ones |
| **LLM as Agent Brain** | The LLM is used to power the "Think" stage of the agent's Observe → Think → Act loop | Agent sends context to GPT-4 → GPT-4 decides next step |
