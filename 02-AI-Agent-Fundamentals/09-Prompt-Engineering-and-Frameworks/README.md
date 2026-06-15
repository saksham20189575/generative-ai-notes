# Prompt Engineering, Business Use Cases & Framework Overview

Till now, we have understood **what AI agents are** and how **LLMs** (Large Language Models) like ChatGPT work behind the scenes. Today, we will learn the **most important skill** to actually *control* these models — **Prompt Engineering** — and we will also peek into the popular **frameworks** (LangChain, CrewAI, AutoGen) that help us build real AI agents without writing everything from scratch.

By the end of this class, you should be able to look at any business problem and say, "Okay, this is the prompt I will write, this is the role I will give the AI, and this is the framework I will pick."

## Introduction to Prompt Engineering

When we talk to an AI like ChatGPT, whatever we type is called a **prompt**. The quality of the answer depends **completely** on the quality of our question.

- **Official Definition:** **Prompt Engineering** is the practice of designing and refining the input instructions given to a Large Language Model to get accurate, useful, and reliable outputs.
- **In Simple Words:** It is the skill of **asking the AI in the right way** so that it gives you exactly what you want — not something random.
- **Real-Life Example:** Think of hiring an auto-rickshaw. If you just say *"Bhaiya, chalo"*, the driver will be confused. But if you say *"Bhaiya, HSR Sector 4, 5th Main, near the bakery, shortest route please"*, you will reach your destination quickly. Prompt Engineering is exactly this — giving **clear, complete directions** to the AI.

Now that we know *why* prompts matter, let us understand the **first and most powerful type** of prompt — the System Prompt.

## Understanding System Prompts

Every AI model has **two kinds of instructions** — one from the developer (hidden) and one from the user (what you type). The hidden one is called the **System Prompt**.

- **Official Definition:** A **System Prompt** is a set of initial instructions given to the LLM that defines its **behavior, tone, personality, boundaries, and rules** for the entire conversation.
- **In Simple Words:** It is like the **job description** you give the AI *before* the customer starts talking to it. Once set, the AI follows these rules for every reply.
- **Real-Life Example:** Imagine you are opening a new restaurant. Before customers arrive, you tell your waiter: *"Always greet with namaste, suggest the chef's special first, never recommend non-veg if customer says Jain, and keep tone polite."* That briefing is the **System Prompt** for your waiter.

### Key Things a System Prompt Controls

- **Identity** — Who the AI *is* (e.g., "You are a banking assistant for HDFC Bank").
- **Tone** — How it should *speak* (e.g., "Polite, professional, never casual").
- **Boundaries** — What it *must not* do (e.g., "Never share account numbers or OTPs").
- **Format** — How answers should *look* (e.g., "Always reply in 3 bullet points").
- **Knowledge Scope** — What topics it can or cannot discuss (e.g., "Only answer loan-related questions").

### Example of a Good System Prompt

```text
You are "SehatBot", a friendly health assistant for Indian users.
- Always reply in simple Hindi-English mix.
- Never give medicine dosages; always tell the user to consult a doctor.
- Keep answers under 4 sentences.
- If asked anything outside health, politely say "I can only help with health queries."
```

**How this system prompt works:**

- The **first line** fixes the **identity** of the bot — it is a health assistant, not a general chatbot.
- The next bullets set **tone**, **safety rules**, and **length control** so the bot stays predictable.
- The **last rule** creates a clear **boundary** so the bot does not start talking about cricket or movies.

A very common doubt students ask: **"Can the user override the system prompt?"** Generally no — the system prompt is given highest priority by the model, which is why companies use it to protect their product.

### In-Session Practice 1 — Build Your Own System Prompt (10 minutes)

Open **ChatGPT** (or **Gemini** / **Claude**). Use the *"Customize GPT"* or *"Custom Instructions"* area — or simply start a new chat and paste your system prompt as the **first message** saying *"Follow these rules for the rest of this conversation."*

- **Task:** Build a **"PaisaBachao Bot"** — a bot that helps Indian college students save money.
- **Your Prompt Must Include:**
    - **Identity** — Name and purpose of the bot.
    - **Tone** — Friendly, Hindi-English mix, like a senior in college.
    - **Boundaries** — Never suggest loans, gambling, or crypto.
    - **Format** — Reply in 3 short bullets only.
    - **Scope** — Only answer money-saving questions.
- **Then Test It With These User Questions:**
    - *"How do I save ₹2,000 a month from my ₹8,000 pocket money?"*
    - *"Should I take a personal loan to buy the new iPhone?"* (testing the boundary)
    - *"Who won the cricket match yesterday?"* (testing the scope)
- **Discuss in Pairs (2 mins):** Did the bot stay in character? Where did it break? Fix the system prompt and try again.

Now that the AI has an identity, we can make it even more focused using **Role Prompting**.

## Applying Role Prompting

Role Prompting is a *simpler, lighter* version of system prompts that you can use even inside normal chat.

- **Official Definition:** **Role Prompting** is a technique where you explicitly assign a **persona or profession** to the LLM so that its answers match the expected expertise and style of that role.
- **In Simple Words:** You tell the AI, *"Pretend you are a ____"* and it will answer **as that person** would.
- **Real-Life Example:** If you ask a **random stranger** "How should I save money?", you get a general answer. But if you ask a **Chartered Accountant**, you get tax-saving tips, SIP advice, and section 80C tricks. Role prompting makes the AI behave like that CA.

### Common Roles You Can Use

- **"You are an experienced school teacher"** — for simple explanations.
- **"You are a senior software engineer"** — for code review and architecture.
- **"You are a financial analyst"** — for investment and market insights.
- **"You are a motivational speaker"** — for energetic, positive answers.
- **"You are a strict interview panelist"** — for tough practice Q&A.

### Why Role Prompting Works

- LLMs are trained on **billions of examples**, including how teachers, doctors, lawyers *actually write*.
- When you assign a role, the model **pulls out that specific style** from its memory.
- This gives answers more **depth, accuracy, and right vocabulary** without extra effort from you.

### Quick Comparison — Without vs With Role

- **Without Role:** *"Explain compound interest."* → Gives a textbook definition.
- **With Role:** *"You are a friendly bank relationship manager. Explain compound interest to a 40-year-old shopkeeper."* → Gives an example using his shop savings, in simple Hindi-English, with a real number.

### In-Session Practice 2 — Same Question, Five Roles (10 minutes)

Pick **ONE** question and ask it to ChatGPT **five times**, each time with a different role. This helps you *feel* how much the role changes the answer.

- **Question to Use:** *"Should I start learning Python in 2026?"*
- **Roles to Try (copy-paste one by one):**
    1. *"You are a 10-year-old kid. Answer in your own simple words."*
    2. *"You are a strict school principal. Give a serious, formal answer."*
    3. *"You are a Silicon Valley tech CEO. Answer with data and future trends."*
    4. *"You are a stand-up comedian. Give a funny, honest take."*
    5. *"You are a SEBI-registered career counsellor. Give a practical, India-focused answer."*
- **Your Job:**
    - Copy **each reply** into a Google Doc or Notes app.
    - In a **group of 3**, rank which answer was *most useful*, *most fun*, and *most unexpected*.
    - Share your favourite role with the class in one sentence.
- **Learning:** By the end of this, you will *never* again ask ChatGPT a question **without a role**.

With roles clear, let us now learn how to **write the actual prompt body** in a way that gets the best output.

## Writing Simple Effective Prompts

Most beginners write **one-line prompts** and then complain that ChatGPT gave a bad answer. The problem is not ChatGPT — it is the prompt.

- **Official Definition:** An **Effective Prompt** is one that provides the model with **clear context, specific instructions, expected format, and necessary constraints** to generate the desired output.
- **In Simple Words:** A good prompt is like a **good WhatsApp message to your maid** — you mention *what, when, how, and how much*, leaving no confusion.
- **Real-Life Example:** Bad message: *"Aaj subzi bana do."* Good message: *"Aaj lunch ke liye aloo-gobhi banao, thoda kam teekha, 2 logon ke liye, 12 baje tak."* The second one leaves zero room for mistakes.

### The 4-Part Formula for a Good Prompt

Every strong prompt has **four parts** — remember them as **C-I-F-C**:

- **C — Context:** Who you are or what the situation is.
- **I — Instruction:** What exact task the AI should do.
- **F — Format:** How the output should look.
- **C — Constraints:** Any limits like word count, tone, or things to avoid.

![The C-I-F-C formula for a strong prompt — Context, Instruction, Format, Constraints](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session09/cifc_formula.png)

### Example of a Weak vs Strong Prompt

- **Weak Prompt:** *"Write something about Diwali."*
- **Strong Prompt:** *"I am a school teacher (Context). Write a short speech on Diwali for Class 5 students (Instruction). Use 5 bullet points, each one line (Format). Keep language simple and avoid any religious controversy (Constraints)."*

The second prompt will almost always give you a ready-to-use output, while the first one gives something generic.

### Common Mistakes Beginners Make

- **Being too short** — *"Tell me about marketing"* is too open; AI will give a Wikipedia-like reply.
- **Being too long and confusing** — Asking 5 things in one prompt makes the AI mix them up.
- **Not giving examples** — If you want a specific style, **show one sample** of what you want.
- **Forgetting the audience** — Always mention *"for a 10-year-old"* or *"for a CEO"* to control depth.

### In-Session Practice 3 — Fix the Weak Prompt (15 minutes)

Below are **four weak prompts**. Your job is to **rewrite each one** using the **C-I-F-C formula** and then test both versions in ChatGPT to compare.

- **Weak Prompt A:** *"Write an email."*
- **Weak Prompt B:** *"Give me a business idea."*
- **Weak Prompt C:** *"Summarise this article."* (paste any news article)
- **Weak Prompt D:** *"Plan my trip."*

**Instructions:**

- Take **5 minutes** on your own — rewrite all 4 prompts in your notebook using C-I-F-C.
- Take **5 minutes** to run both the *weak* and your *strong* version in ChatGPT side by side.
- Take **5 minutes** in groups of 4 — share the **best rewrite** of each prompt and vote on the group winner.

**Example of What a Good Rewrite Looks Like:**

```text
Weak:   "Write an email."

Strong: "I am a B.Tech fresher applying for a data analyst role at Infosys (Context).
        Write a short cold email to the HR introducing myself and requesting an interview (Instruction).
        Format: 120 words max, with a clear subject line and 3 short paragraphs (Format).
        Keep tone humble, no fancy words, no salary talk (Constraints)."
```

**How this rewrite works:**

- The **Context** tells the AI *who* is sending the email, which changes the whole tone.
- The **Instruction** is very specific — "cold email" + "request interview" leaves no confusion.
- The **Format** (120 words, subject line, 3 paras) makes the output ready to *send*, not to edit.
- The **Constraints** (humble tone, no salary) remove common AI mistakes *before* they happen.

Once you can write a clear prompt, the next skill is to **control the output format**, which is what businesses actually need.

## Controlling Output Format

AI answers are only useful if they are in the **format you can use directly** — inside Excel, inside a report, inside an email. This is called Output Formatting.

- **Official Definition:** **Output Format Control** is the technique of explicitly instructing the LLM to structure its response in a specific layout like bullets, tables, JSON, steps, or a fixed template.
- **In Simple Words:** You tell the AI, *"Don't just write a paragraph — give me the answer in a **table / list / steps / JSON** format."*
- **Real-Life Example:** If you ask a Zomato delivery partner for directions, a **Google Maps-style step-by-step list** is much more useful than a long paragraph explanation. Format makes data **usable**.

### Popular Output Formats You Can Ask For

- **Bullet Points** — For quick scanning and presentations.
- **Numbered Steps** — For tutorials and "how-to" guides.
- **Tables** — For comparisons (e.g., two phones, three plans).
- **JSON / Key-Value** — For feeding output into other software.
- **Short Answer (1 line)** — For dashboards and chatbots.
- **Markdown Format** — For documentation and blog writing.

### Example Prompts for Different Formats

```text
Prompt 1 (Table): Compare iPhone 15 vs Samsung S24 in a markdown table with columns: Feature, iPhone 15, Samsung S24.

Prompt 2 (Steps): Give me step-by-step instructions to reset a Wi-Fi router, numbered from 1 to 6.

Prompt 3 (JSON): Extract the name, age, and city from this sentence and return ONLY a JSON object: "Rahul, 27, lives in Pune."

Prompt 4 (Bullets): List 5 benefits of yoga in one-line bullets, no explanations.
```

**How these prompts work:**

- Each prompt **names the format** directly, so there is no confusion.
- The **word "ONLY"** in Prompt 3 tells the model *not* to add extra explanation — very important when output goes into software.
- Specifying **column names** or **number of bullets** removes all randomness from the answer.

A small tip: when you want data inside your app or Excel, **always ask for JSON or CSV**. Paragraphs are for humans, structured formats are for machines.

### In-Session Practice 4 — Same Data, Four Formats (10 minutes)

Let us take **one small piece of information** and force ChatGPT to give it in **four different formats**. This trains your eye to *choose* the right format for real business work.

- **Topic:** *"The top 5 most populous cities in India."*
- **Four Prompts to Run One By One:**
    1. **Paragraph:** *"Write a short paragraph about the top 5 most populous cities in India."*
    2. **Bullet Points:** *"List the top 5 most populous cities in India as one-line bullets — only city name and population."*
    3. **Markdown Table:** *"Give a markdown table with columns: Rank, City, State, Population (approx). Top 5 cities in India."*
    4. **JSON:** *"Return ONLY a JSON array of the top 5 most populous Indian cities. Each object must have keys: rank, city, state, population. No explanation."*
- **Your Job:**
    - Run all 4 prompts and **screenshot each output**.
    - Decide: Which format would you send to — **a friend on WhatsApp?** **your boss in an email?** **a developer who will put this in an app?** **a reporter writing a story?**
    - Discuss with the person next to you — **format is not decoration, format is delivery**.

With formatting done, the next important skill is learning **how small changes in prompts give very different outputs**.

## Experimenting with Prompt Variations

The same question, asked in **5 different ways**, can give 5 very different answers. A prompt engineer's real job is to **test variations** and pick the best one.

- **Official Definition:** **Prompt Variation** is the systematic process of modifying parts of a prompt — role, tone, format, or wording — to compare outputs and identify the version that gives the most accurate or useful result.
- **In Simple Words:** It means **trying the prompt 3–4 times in different styles** and keeping the best one.
- **Real-Life Example:** Like a photographer clicks the **same pose from 5 angles** before picking one for Instagram — a good prompt engineer tries 5 versions before finalising one for production.

### What You Can Vary

- **The Role** — "as a teacher" vs "as a CEO".
- **The Tone** — formal vs casual vs funny.
- **The Length** — "in 50 words" vs "in 500 words".
- **The Format** — bullets vs table vs paragraph.
- **The Example Given** — giving 0 examples vs 1 example vs 3 examples (called **zero-shot, one-shot, few-shot** prompting).

### Mini Comparison Exercise

Let us see how one topic — *"Explain EMI"* — changes with variations:

- **V1 (Plain):** *"Explain EMI."* → Generic definition.
- **V2 (Role):** *"As a bank manager, explain EMI to a first-time loan taker."* → Friendly, practical.
- **V3 (Format):** *"Explain EMI in 3 bullets, each under 15 words."* → Crisp and tweet-ready.
- **V4 (Example-based):** *"Explain EMI using the example of a ₹5 lakh car loan for 5 years."* → Concrete and relatable.

Try each version once — you will feel the difference in **5 minutes** and understand why big companies hire Prompt Engineers.

### In-Session Practice 5 — Prompt A/B Testing Challenge (15 minutes)

Now we do what real Prompt Engineers at companies like **Flipkart, Swiggy, and Meesho** do every day — **A/B test prompts** and pick the winner.

- **Challenge:** Write a **product description** for a simple kurta on a Meesho-like shopping app.
- **Step 1 — Write 3 Variations of the Prompt:**
    - **V1 (Zero-shot):** *"Write a product description for a cotton kurta."*
    - **V2 (Role + Format):** *"You are a fashion copywriter. Write a 40-word product description for a cotton kurta in 3 short bullets. Include fabric, fit, and an occasion to wear it."*
    - **V3 (Few-shot):** Same as V2 but add **one example first**: *"Here is a sample good description: 'Soft pure cotton, relaxed fit, perfect for office or Sunday brunch.' Now write one for a blue printed cotton kurta."*
- **Step 2 — Run All 3 in ChatGPT.** Paste each output into a Google Doc.
- **Step 3 — Score Each Output (1 to 5) on:**
    - Clarity — Does it make the product sound clear?
    - Appeal — Would *you* click "Add to Cart"?
    - Length — Is it the right size for a mobile app?
- **Step 4 — Share Winners (3 mins):** Two volunteers share which version won for them and *why* — this is your first real Prompt Engineering report.

**A Small Doubt Students Often Have:** *"Which version is always the best?"* There is **no single winner** — that is exactly why A/B testing exists. For short product listings, few-shot usually wins. For long essays, role-based wins. **Always test.**

Now that we have mastered prompting, let us shift to **where all this is actually used** — real business problems.

## Exploring Real-World Use Cases

AI agents are not just toys — they are **already saving crores of rupees** for companies by replacing repetitive work. Let us look at the most common use cases.

- **Official Definition:** A **Use Case** is a specific real-world business problem or workflow where an AI agent can be applied to automate, assist, or enhance human effort.
- **In Simple Words:** It is a **real job** in a real company where an AI is doing the work instead of (or along with) humans.
- **Real-Life Example:** A Zomato customer support chatbot that refunds your cancelled order instantly — *that* is an AI agent doing a real use case.

### Top Business Use Cases Today

- **Customer Support Bots** — Answer FAQs, track orders, issue refunds (e.g., Flipkart, Swiggy).
- **Coding Assistants** — Generate, debug, and review code (e.g., GitHub Copilot, Cursor).
- **Research Assistants** — Summarise long PDFs, compare companies, prepare reports.
- **Sales Email Writers** — Draft personalised emails to thousands of leads.
- **Resume Screeners** — Shortlist 1,000 CVs in minutes based on job requirements.
- **Content Creators** — Generate blogs, social media posts, and ad copies.
- **Data Analysts** — Read Excel files and give insights in plain English.
- **Legal Assistants** — Read contracts and highlight risky clauses.
- **Medical Triage Bots** — Ask symptoms and guide the patient to the right specialist.
- **Learning Tutors** — Personalised doubt-solving for students (like Byju's / Unacademy AI).

### How to Spot a Good Use Case

- The task is **repetitive** — done many times every day.
- The task involves **reading, writing, or decision-making** with text or data.
- The task **does not need physical hands** (AI is not a robot yet, mostly).
- The task has **clear rules** or **clear examples** we can show the AI.
- Mistakes are **correctable** — we are not using AI for life-and-death decisions without human checks.

Once we pick a use case, the next step is to **map it to a specific agent behavior**.

## Mapping Use Case to Agent Behavior

Every use case needs a **different kind of agent**. A chatbot for customer support is **not** the same as a research agent.

- **Official Definition:** **Agent Behavior Mapping** is the process of identifying the *type of actions, tools, memory, and personality* an AI agent needs in order to solve a particular business problem effectively.
- **In Simple Words:** It means **matching the right kind of agent to the right kind of job** — just like you would not hire a chef to fix your laptop.
- **Real-Life Example:** In a hospital, the **receptionist** greets and directs patients, the **doctor** diagnoses, and the **pharmacist** gives medicines. Each has a different role, tools, and style. AI agents work the same way.

### Quick Mapping Table (Use Case → Agent Behavior)

| Use Case | Agent Needs To… | Key Skill / Tool Needed |
|---|---|---|
| Customer Support Bot | Answer FAQs, stay polite, escalate tough ones | Knowledge Base, polite tone |
| Coding Help Agent | Write code, debug, explain errors | Code tools, terminal access |
| Research Assistant | Read many docs and summarise | PDF reader, web search |
| Sales Email Writer | Personalise 100s of emails | CRM data, tone control |
| Data Analyst Bot | Read Excel / SQL and explain numbers | Database tools, chart maker |
| Interview Practice Bot | Ask tough questions, evaluate answers | Memory of previous answers |

Notice how each row needs **different tools and different personality** — that is why **frameworks** exist, which we will see next.

Speaking of frameworks, let us now understand **why they exist in the first place**.

## Understanding Why Frameworks Exist

Building an AI agent from scratch is like **building your own car from nuts and bolts** — possible, but exhausting. Frameworks give you a ready chassis.

- **Official Definition:** An **AI Agent Framework** is a pre-built software toolkit that provides ready-made components — like memory, tools, planning, and multi-agent communication — so developers can build agents faster and more reliably.
- **In Simple Words:** It is a **kit with all common parts already made**, so you just have to assemble your agent, not invent every wheel.
- **Real-Life Example:** Think of cooking. You *can* grind your own masala, make your own paneer, roll your own rotis. Or you can use **MTR masala, Amul paneer, and store-bought rotis** and cook 10× faster. Frameworks are the MTR masala of AI.

### What Frameworks Usually Provide

- **LLM Connectors** — Ready-made connection to ChatGPT, Claude, Gemini, etc.
- **Memory** — Agents can remember past chats and user details.
- **Tools / Plugins** — Agent can call Google Search, send emails, read PDFs, etc.
- **Planning** — Agent can break a big task into small steps by itself.
- **Multi-Agent Coordination** — Many agents can work as a team.
- **Logging & Debugging** — Helps us see *why* the agent did what it did.

### Why Not Just Use ChatGPT Directly?

- ChatGPT has **no memory of your business data** by default.
- It **cannot click buttons, send emails, or update databases** on its own.
- It **cannot call other agents** or split tasks.
- Frameworks add all these missing powers around the LLM.

The three biggest frameworks right now are **LangChain, CrewAI, and AutoGen**. Let us explore each at a high level.

## Exploring LangChain

LangChain is the **oldest and most popular** framework for building AI agents and applications.

- **Official Definition:** **LangChain** is an open-source framework that provides modular components and standardised interfaces for connecting LLMs with external tools, data sources, memory, and workflows.
- **In Simple Words:** It is like **LEGO blocks for AI** — you pick a model block, a memory block, a tool block, and snap them together into an app.
- **Real-Life Example:** Imagine a **dabba delivery service** like Mumbai's dabbawalas. LangChain is the *system* that picks the tiffin from home (data source), takes it to the station (LLM), delivers it to the office (tool), and brings back the empty box (memory). It is the full **workflow connector**.

### What LangChain Is Good For

- **Connecting LLMs to your own documents** — PDFs, Word files, databases.
- **Chains** — Linking multiple LLM calls in a sequence (e.g., summarise → translate → email).
- **Retrieval-Augmented Generation (RAG)** — Making the AI answer from *your* data, not just public data.
- **Single, powerful agents** — One smart agent that can use many tools.
- **Integration with 500+ services** — Gmail, Slack, Notion, Google Drive, etc.

### A Simple LangChain Flow (Conceptual)

```text
User Question → LangChain → LLM (ChatGPT) → Tool (Google Search) → LLM again → Final Answer
```

**How this flow works:**

- The **user's question** enters LangChain, which acts like a **traffic controller**.
- LangChain sends it to the **LLM** to *decide* if a tool is needed.
- If yes, LangChain calls the **tool** (like Google Search) and gets fresh info.
- The LLM is called **again** with this info to write a final clean answer.
- LangChain returns the **final answer** to the user — all this happens in seconds.

When you need **one strong agent with many tools**, LangChain is your first choice. But when you need **many agents working together**, we use CrewAI.

## Exploring CrewAI

CrewAI was created for a different problem — when **one agent is not enough** and you need a whole **team of AI agents**.

- **Official Definition:** **CrewAI** is an open-source framework designed to orchestrate multiple autonomous AI agents with defined roles, goals, and tasks, so they can collaborate like a real-world team.
- **In Simple Words:** It lets you build a **team of AI workers** — each with its own job, reporting manager, and deadline — just like a real office.
- **Real-Life Example:** Think of a **newspaper office**. One person is the **reporter**, one is the **editor**, one is the **photographer**, one is the **publisher**. No single person can run the paper alone — they **work as a crew**. CrewAI does this with AI agents.

### Key Ideas in CrewAI

- **Agent** — One AI worker with a specific role (e.g., "Researcher", "Writer", "Reviewer").
- **Task** — A specific job given to that agent (e.g., "Find top 5 EV cars in India").
- **Crew** — A *team* of agents + tasks that work together towards one big goal.
- **Process** — The order in which tasks happen (sequential or parallel).

### Example — A Blog Writing Crew

- **Researcher Agent** — Goal: "Find latest trends on electric cars in India."
- **Writer Agent** — Goal: "Write a 500-word blog using the research."
- **Editor Agent** — Goal: "Check grammar, tone, and SEO of the blog."
- **Publisher Agent** — Goal: "Post the final blog to WordPress."

![CrewAI blog-writing crew — Researcher → Writer → Editor → Publisher agents passing work forward](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session09/crewai_blog_crew.png)

Each agent **does its job, passes the work forward**, and you get a finished blog — without you writing a single word.

### When to Choose CrewAI

- You have a **complex workflow** with clear, separate roles.
- You want agents to **collaborate and share information**.
- You need **parallel work** — e.g., research + design happening at the same time.
- You want a **manager agent** to oversee other agents.

If CrewAI is about **team roles**, then AutoGen is about **free-flowing conversations between agents**.

## Exploring AutoGen

AutoGen, built by Microsoft, takes a slightly different angle — it focuses on **agents talking to each other like humans do in a chatroom**.

- **Official Definition:** **AutoGen** is an open-source framework developed by Microsoft that enables multiple AI agents (and humans) to interact through conversational messaging to solve complex tasks collaboratively.
- **In Simple Words:** It is like creating a **WhatsApp group of AI agents** where they keep chatting, asking each other questions, and eventually agreeing on a solution.
- **Real-Life Example:** Imagine you are stuck on a tough problem and you create a WhatsApp group with a **CA, a lawyer, and a doctor**. They discuss, argue, and together give you the best advice. AutoGen builds this chatroom, but for AI.

### Key Ideas in AutoGen

- **Conversable Agents** — Every agent can send and receive messages.
- **User Proxy Agent** — Represents *you*, the human, inside the chat.
- **Assistant Agents** — AI agents that do the actual work.
- **Group Chat** — Multiple agents in one conversation, taking turns.
- **Code Execution** — Agents can even **write and run code** to verify ideas.

### Example — A Debugging Conversation

- **You (User Proxy):** "My Python code is giving an error."
- **Coder Agent:** "Let me check. I think line 5 has a typo."
- **Reviewer Agent:** "Also, you are missing an import statement."
- **Coder Agent:** "Good point, let me rewrite and run it."
- **Final Answer** → A fixed, tested piece of code, built through a *natural back-and-forth*.

### When to Choose AutoGen

- You want agents to **discuss and debate** before finalising an answer.
- Your use case needs **code execution and verification** (e.g., data analysis).
- You want a **human in the loop** — jumping in whenever needed.
- You like a **chat-style architecture** over a task-list architecture.

Now that we have seen all three frameworks, let us **compare them side by side**.

## Comparing Frameworks — A Simple Guide

You don't need to master all three frameworks. You just need to know **which one fits which situation**.

![LangChain vs CrewAI vs AutoGen — a quick visual comparison of what each framework is best for](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session09/frameworks_comparison.png)

### Side-by-Side Comparison Table

| Feature | LangChain | CrewAI | AutoGen |
|---|---|---|---|
| **Main Idea** | Chains + Tools | Team of Role-Based Agents | Conversation Between Agents |
| **Best For** | One smart agent + many tools | Multi-step business workflows | Collaborative problem-solving |
| **Learning Curve** | Medium | Easy | Medium |
| **Multi-Agent Support** | Limited | Very Strong | Very Strong |
| **Human-in-the-Loop** | Possible | Possible | Native, built-in |
| **Community / Maturity** | Largest | Growing fast | Microsoft-backed |
| **Typical Use Case** | RAG chatbots, doc Q&A | Blog factory, research crew | Code debugging, data analysis |

### A Simple Decision Rule

- Do you need **one agent with access to your data**? → **LangChain**.
- Do you need a **team of agents with different job roles**? → **CrewAI**.
- Do you need agents to **chat back and forth and even run code**? → **AutoGen**.

A common doubt students have: **"Can I use them together?"** Yes — many real projects use **LangChain for tools** and **CrewAI or AutoGen for orchestration** on top. Frameworks are not competitors; they are **building blocks**.

With the theory clear, let us put everything together by **designing a simple agent flow**.

## Designing a Simple Agent Flow

An agent, at its heart, is just a loop of **Prompt → LLM → Action → Result**. Let us design one on paper.

- **Official Definition:** An **Agent Flow** is the sequence of steps — input, reasoning, tool usage, and output — that an AI agent follows to complete a task autonomously.
- **In Simple Words:** It is a **flowchart** of how the agent thinks, acts, and finishes the job.
- **Real-Life Example:** The flow of a **food delivery agent**: Take order → Go to restaurant → Pick food → Deliver to customer → Take payment. Every AI agent has a similar simple loop.

### The 4 Building Blocks of Any Agent

- **Input (Prompt)** — The user's question or goal.
- **Brain (LLM)** — The model that thinks and plans.
- **Hands (Tools)** — APIs, search, email, database — how the agent *acts*.
- **Output (Result)** — The final answer or completed action.

![Agent flow loop — Prompt → LLM → Tools → Output, with the LLM looping back to tools when the task is not yet done](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/session09/agent_flow_loop.png)

### Example Flow — A "Career Advisor Agent"

```text
Step 1: User says → "Suggest 3 careers based on my skills: Python, Excel, communication."

Step 2: System Prompt sets role → "You are a friendly Indian career counsellor."

Step 3: LLM thinks → "Skills match: Data Analyst, Business Analyst, Python Developer."

Step 4: Tool call → Agent searches job portals for current demand.

Step 5: LLM writes final answer → A table with 3 careers, avg salary, and top companies.

Step 6: Output returned to user → Student reads and picks one.
```

**How this flow works:**

- **Step 1** is the **user's raw goal** — unclear but direction-giving.
- **Step 2** is the **system prompt** that fixes the agent's personality *before* it responds.
- **Step 3** is the **LLM reasoning** — pure thinking, no tools yet.
- **Step 4** shows **tool usage** — this is what separates an agent from a plain chatbot.
- **Step 5** and **Step 6** are about **formatting** the answer nicely for the user.

This same pattern can be used for **any** business problem — just change the role, the tools, and the prompt. That is the entire magic of agents.

Now let us actually *try* a small version of this together.

## Guided Mini Activity — Build Your First Role-Based Agent (Pen & Paper)

This activity needs **zero coding**. We will use ChatGPT (or any LLM you have) and build a **working agent** just using smart prompts.

### Task

Build a **"Personal Finance Coach Agent"** that helps an Indian middle-class user plan monthly savings.

### Step-by-Step Instructions

- **Step 1 — Design the System Prompt.** Write a 4-line system prompt fixing the role, tone, language, and boundaries. Example starter: *"You are SaveSmart, a warm and practical Indian finance coach. Use simple Hindi-English. Never suggest risky products like crypto. Keep answers under 5 bullet points."*
- **Step 2 — Choose the Role.** Add a role line at the top of every conversation — e.g., *"Act as an experienced SEBI-registered financial planner."*
- **Step 3 — Write the User Prompt.** Use the **C-I-F-C formula** — Context, Instruction, Format, Constraints. Example: *"I am a 26-year-old with ₹40,000 monthly salary in Bangalore (Context). Suggest a monthly savings plan (Instruction). Give answer in a table with categories and amounts (Format). Keep total expenses under salary, no crypto, no risky stocks (Constraints)."*
- **Step 4 — Control the Output.** Ask for a **table** with columns: Category, Amount (₹), Why.
- **Step 5 — Try 3 Variations.** Run the same prompt with these changes:
    - Variation A: Change role to *"strict father giving advice"*.
    - Variation B: Change format to *"5 crisp bullets, no table"*.
    - Variation C: Add constraint *"user has a 2-year-old kid"*.
- **Step 6 — Compare & Discuss.** In groups of 3, compare which variation gave the most **useful and realistic** advice. Discuss *why*.

### What You Will Learn From This Activity

- How a **system prompt** changes the entire *personality* of the agent.
- How **role prompting** adjusts the depth and style of advice.
- How **small prompt changes** create very different outputs.
- How **output format control** makes the answer ready-to-use.
- How a real **agent flow** feels — even without writing any code.

This activity is the foundation of every AI agent you will ever build. Once you are comfortable here, moving to LangChain, CrewAI, or AutoGen is just a matter of **which framework** you pick — the *thinking* remains the same.

## Summary — What We Learned Today

We did not just read about prompts today — we **wrote, tested, and compared** them live in **5 hands-on practices** plus the final capstone activity. That is how real Prompt Engineers learn.

- **Prompt Engineering** is the art of asking AI in the right way to get reliable outputs.
- **System Prompts** set the agent's identity, tone, and boundaries for the whole conversation.
- **Role Prompting** instantly upgrades answer quality by assigning a profession or persona.
- **Effective Prompts** follow the **C-I-F-C** formula — Context, Instruction, Format, Constraints.
- **Output Format Control** (tables, JSON, bullets) makes AI outputs usable in real business tools.
- **Prompt Variations** help us A/B test prompts and pick the best-performing version.
- **Real-World Use Cases** include support bots, coders, researchers, analysts, and more.
- Different use cases need **different agent behaviors** — match the agent to the task.
- **Frameworks** (LangChain, CrewAI, AutoGen) give us ready-made building blocks to build agents faster.
- **LangChain** is best for *one* smart agent with many tools.
- **CrewAI** is best for a *team* of role-based agents working together.
- **AutoGen** is best for agents (and humans) *chatting* to solve a problem.
- Every agent, at its core, is a simple loop: **Prompt → LLM → Tool → Output**.

## Important Concepts, Commands & Frameworks — Quick Reference

| Term | Meaning | When to Use |
|---|---|---|
| **Prompt** | The input you give to an LLM | Every time you talk to AI |
| **System Prompt** | Hidden instruction that sets agent's identity | Starting any new AI product |
| **Role Prompting** | Assigning a persona like "teacher", "CA", "doctor" | To get expert-style answers |
| **Zero-shot Prompt** | Giving a task with no examples | Simple, direct tasks |
| **Few-shot Prompt** | Giving 2–3 examples inside the prompt | When you want a specific style |
| **C-I-F-C Formula** | Context + Instruction + Format + Constraints | Writing any strong prompt |
| **Output Formats** | Bullets, Table, JSON, Steps, Markdown | To make output usable |
| **Use Case** | A real business problem solved by AI | Picking where to apply agents |
| **Agent Flow** | Prompt → LLM → Tool → Output loop | Designing any AI agent |
| **LangChain** | Framework for single agents + tools + data | RAG, chatbots, doc Q&A |
| **CrewAI** | Framework for team-of-agents with roles | Multi-step workflows |
| **AutoGen** | Framework for conversational multi-agents | Collaborative & code-heavy tasks |
| **User Proxy Agent** | Represents the human inside AutoGen | Human-in-the-loop systems |
| **RAG** | Retrieval-Augmented Generation | When AI must answer from your own documents |

Keep this table handy — these are the 14 terms that will keep coming back in **every** AI agent class from here on.
