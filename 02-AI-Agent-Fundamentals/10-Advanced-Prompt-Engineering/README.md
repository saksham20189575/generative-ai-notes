# Advanced Prompt Engineering for Agents

## What We Covered So Far & What's Coming Next

In our last session, we explored the **foundations of Prompt Engineering** — we learned how **system prompts** set the behaviour and personality of an AI agent, how **role prompting** (giving the AI a role like "teacher" or "analyst") shapes its responses, and we got a high-level introduction to popular agent frameworks like **LangChain**, **CrewAI**, and **AutoGen**. We also looked at real-world use cases where these agents are deployed — from customer support bots to coding assistants.

Now that you know *what* a prompt is and *why* it matters, this session takes things one level deeper. We are going to learn **advanced techniques** that make prompts much smarter — techniques that help an AI agent actually *think* through a problem instead of just guessing an answer.

**In this session, you will learn:**
- What **Prompt Engineering** truly means at an advanced level and why it is the most powerful skill in the AI era
- How **Chain-of-Thought (CoT) prompting** forces an AI to reason step by step
- How to build **Structured Prompts** using a professional template (Role + Task + Instructions + Constraints + Output Format)
- How to write **Reasoning Prompts** for comparison, analysis, and decision-making tasks
- How to **evaluate and improve** a prompt when the output is weak
- Best practices for building prompts that work reliably inside real AI agents

---

## What Is Prompt Engineering (Advanced View)

**Official Definition:** Prompt Engineering is the discipline of designing and refining input instructions (called "prompts") given to a Large Language Model (LLM) to reliably produce accurate, useful, and well-structured outputs.

**In Simple Words:** Think of a Large Language Model like a very brilliant but very literal genie. If you say "make my life better," the genie is confused. But if you say "I want a salary of ₹1 lakh per month, a job in Bangalore as a data analyst, and I want to start in 3 months," — the genie knows exactly what to do. Prompt engineering is the skill of talking to this genie in the right way.

**Real-Life Example:** Imagine you are a manager giving a task to a new employee. A vague instruction like "write something about our product" will give you a random result. But a clear instruction — "Write a 200-word Instagram caption for our new protein bar, targeting gym-goers aged 18–25, using an energetic tone" — gives you exactly what you need. Prompting an AI is no different.

![Vague vs specific prompts — clear, detailed instructions get reliable outputs; fuzzy wishes do not](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session10/session10-vague-vs-specific-prompt.png)

- **Why this matters for agents:** In an AI agent system, the agent doesn't just answer one question — it is working on a task autonomously, sometimes for minutes at a time. If the prompt guiding it is vague, the entire agent goes off track. A well-crafted prompt is the *blueprint* for agent behaviour.
- **The two biggest mistakes beginners make:** (1) Writing prompts that are too short and vague, expecting the AI to "figure it out." (2) Writing prompts that are too long but unstructured, which confuses the model with contradicting instructions.
- **The skill gap:** Basic prompting gives you a 50% good result. Advanced prompting consistently gives you 90%+ results. That is the gap this session is filling.

> **[ Student Activity ]**
>
> **The Genie Test**
>
> Think of something you genuinely need help with right now — a career question, a study problem, a business idea.
> - First, write the most vague version of that prompt (1 sentence, no details).
> - Then rewrite it as a specific, detailed prompt — add context, your goal, and what kind of answer you need.
> - Share both versions with the person sitting next to you. Can they tell exactly what you wanted just from the vague version?
>
> *Instructor note: Pick 2–3 pairs to share their before/after. Point out what details made the biggest difference.*

---

## How Basic Prompting Fails (And Why We Need Advanced Techniques)

Before learning the advanced techniques, it is important to understand *what goes wrong* with a basic prompt so we appreciate why these techniques were invented.

**Basic Prompt Example:**

```
"What should I do to grow my small business?"
```

**What the AI gives you:** A generic 5-point list — "Make a business plan. Use social media. Hire good people." — that could apply to *any* business anywhere in the world. It is not useful.

**Why it fails:**
- The AI has no context about *your* business, your resources, or your goal
- The AI has no instruction to *think carefully* before answering — it just pattern-matches to the most common answer it has seen
- There is no format specified, so the output can be anything

This is where **Chain-of-Thought, Structured Prompts, and Reasoning Prompts** come in — each one solves a different part of this problem.

> **[ Student Activity ]**
>
> **Spot the Problem**
>
> Look at this prompt: *"Tell me about AI."*
> - Without looking ahead, write down exactly 3 things that are wrong or missing from this prompt.
> - What information would the AI need to give you a *useful* answer?
>
> *Instructor note: Take quick answers from 3–4 students before revealing the analysis in the next section. This builds anticipation.*

---

## Chain-of-Thought Prompting

**Official Definition:** Chain-of-Thought (CoT) Prompting is a technique where you instruct or demonstrate to an LLM to break down a problem into intermediate reasoning steps before arriving at the final answer, rather than jumping directly to a conclusion.

**In Simple Words:** Imagine you ask a student "What is 17 × 8?" If the student just blurts out "136" without showing any working, that is *direct answering* — the answer may be right or wrong, and you have no way to know why. But if the student says "17 × 8 = 17 × 4 × 2 = 68 × 2 = 136," they are showing their work step by step. Chain-of-Thought asks the AI to show its work — and when it does, it makes far fewer mistakes because each step keeps the reasoning on track.

**Real-Life Example:** Think of a doctor diagnosing a patient. A bad doctor says "You have fever, take paracetamol" after 2 seconds. A good doctor says "Let me check your symptoms one by one — you have fever since 3 days, your throat is red, you have body ache — this looks like viral fever, not bacterial, so antibiotics won't help. I recommend rest, fluids, and paracetamol." The second doctor is doing Chain-of-Thought reasoning.

![Chain-of-Thought prompting — step-by-step reasoning keeps the model on track instead of jumping to a shallow answer](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session10/session10-chain-of-thought-flow.png)

### Why CoT Improves Accuracy

- **LLMs are next-token predictors.** They predict the next word based on patterns. When you ask for a direct answer, the model picks the most common pattern — which is often a shallow, popular answer, not the correct one.
- **Forcing step-by-step thinking** makes the model "commit" to intermediate correct steps, and each step acts as a constraint on the next. This reduces errors dramatically.
- **Research has proven this:** Studies on GPT-4 and similar models show that adding "Let's think step by step" to a prompt improves accuracy on logical and math problems by 40–50%.

### Types of Chain-of-Thought Prompting

**1. Zero-Shot CoT — Adding the magic phrase**

You simply add a phrase that triggers step-by-step reasoning:

- "Let's think step by step."
- "Walk me through your reasoning."
- "Think carefully before answering."
- "Break this problem down first."

**Example Prompt:**
```
A train leaves Mumbai at 6 AM at 80 km/h. Another train leaves Pune (150 km away) at 8 AM at 100 km/h 
towards Mumbai. At what time will they meet? Let's think step by step.
```

**Why "zero-shot":** You are not giving the AI any examples — you are just telling it to reason. The phrase alone is enough to trigger better thinking.

**2. Few-Shot CoT — Showing Examples First**

Here, you give the AI 1–2 solved examples *with reasoning shown*, and then ask your actual question. This is more powerful for complex tasks.

**Example Prompt:**
```
Example 1:
Q: A shopkeeper buys apples at ₹10 each and sells them at ₹15 each. If he sells 20 apples, what is the profit?
Reasoning: Cost price of 20 apples = 20 × 10 = ₹200. Selling price = 20 × 15 = ₹300. Profit = 300 - 200 = ₹100.
A: The profit is ₹100.

Now solve this:
Q: A vendor buys pens at ₹5 each and sells them at ₹8 each. He sells 50 pens in a day. What is his daily profit?
Reasoning: [think step by step]
```

**Why this works:** By seeing the *pattern of reasoning* in the example, the AI mimics the same structured approach for your question.

### Applying CoT in Agent Prompts

When you are building an AI agent, you often add CoT instructions directly into the **system prompt** so the agent always reasons carefully:

```python
# This is a system prompt for an AI agent that handles customer complaints

system_prompt = """
You are a customer support agent for an e-commerce company.

When a customer reports a problem, you MUST follow these steps before responding:
Step 1: Identify what the customer's core problem is.
Step 2: Check if this is a delivery issue, a product issue, or a payment issue.
Step 3: Based on the category, think about the best solution.
Step 4: Draft a response that is empathetic, clear, and offers a concrete next step.

Only respond after completing all 4 steps internally.
"""
```

**How the code works:**
- The `system_prompt` variable holds the agent's core instructions — this is sent to the LLM before every conversation
- The numbered steps force the agent to *categorise* the problem before answering — this prevents generic, unhelpful responses
- `"think about the best solution"` is a CoT trigger embedded in the workflow
- `"Only respond after completing all 4 steps internally"` ensures the model does not shortcut its reasoning

> **[ Student Activity ]**
>
> **Trigger the Thinking**
>
> You are given this basic prompt: *"Should I learn Python or SQL first for a data career?"*
> - **Part A (3 min):** Rewrite it as a **Zero-Shot CoT** prompt by adding one or two phrases that trigger step-by-step reasoning. Do not add any examples — just the trigger phrase.
> - **Part B (4 min):** Now write a **Few-Shot CoT** version. Create one solved example (with reasoning shown) before asking the main question.
> - Compare your Part A and Part B. Which one do you think would give the AI more useful guidance?
>
> *Instructor note: Ask 2 students to read their Zero-Shot versions. Show how different trigger phrases (e.g., "walk me through" vs "step by step") can produce slightly different reasoning styles.*

---

## Structured Prompts

**Official Definition:** A Structured Prompt is a prompt built using a defined template with specific components — typically Role, Task, Instructions, Constraints, and Output Format — to produce consistent and predictable responses from an LLM.

**In Simple Words:** Imagine you are filling a job application form. The form has separate boxes for your name, education, experience, and skills. Because of this structure, every applicant fills in the same information in the same place — making it easy to compare. A Structured Prompt does the same thing for AI: it puts every piece of information in the right box so the AI knows exactly what is expected.

**Real-Life Example:** Think of a police FIR (First Information Report). It has a defined structure: Name of complainant, Date and time of incident, Location, Description of the event, Witnesses. Because of this structure, no important detail is missed. A structured prompt ensures no important instruction is missing from your AI request.

### The 5 Building Blocks of a Structured Prompt

| Component | What It Tells the AI | Example |
|-----------|---------------------|---------|
| **Role** | Who you are / what persona to adopt | "You are a senior financial advisor" |
| **Task** | What specific job needs to be done | "Analyse this mutual fund portfolio" |
| **Instructions** | How to do the task (step by step if needed) | "First check the risk level, then check returns, then suggest improvements" |
| **Constraints** | What NOT to do, or limits to follow | "Do not recommend direct stocks. Keep advice simple. Use no jargon." |
| **Output Format** | How the response should look | "Give me a 3-section report: Risk Summary, Performance Summary, Recommendations" |

![The five building blocks of a structured prompt — Role, Task, Instructions, Constraints, and Output Format](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session10/session10-structured-prompt-five-components.png)

### Building a Structured Prompt: Step-by-Step

Let's build a structured prompt together for a real scenario — an AI agent that helps a student choose the right career path.

**Step 1 — Write the Role:**
```
You are a career counsellor with 15 years of experience helping students from non-technical backgrounds 
transition into the tech industry.
```

**Step 2 — Write the Task:**
```
Your task is to analyse the student's background and interests, and recommend the top 3 career paths 
that match their profile.
```

**Step 3 — Write the Instructions:**
```
Follow these steps:
1. Understand the student's educational background
2. Identify their top 2 interests from what they share
3. Match these to realistic tech careers that don't require heavy coding
4. For each career, explain what the job involves in simple language
```

**Step 4 — Write the Constraints:**
```
Do NOT recommend careers that require a Computer Science degree.
Do NOT use technical jargon without explaining it.
Keep each recommendation under 100 words.
```

**Step 5 — Write the Output Format:**
```
Present your answer in this format:
Career 1: [Name]
- What you will do: [2 sentences]
- Why it suits you: [1 sentence]
- Starting salary in India: [approximate range]

Career 2: ...
Career 3: ...
```

**The Full Assembled Structured Prompt:**

```
You are a career counsellor with 15 years of experience helping students from non-technical 
backgrounds transition into the tech industry.

Your task is to analyse the student's background and interests, and recommend the top 3 career paths 
that match their profile.

Follow these steps:
1. Understand the student's educational background.
2. Identify their top 2 interests from what they share.
3. Match these to realistic tech careers that don't require heavy coding.
4. For each career, explain what the job involves in simple language.

Constraints:
- Do NOT recommend careers that require a Computer Science degree.
- Do NOT use technical jargon without explaining it.
- Keep each recommendation under 100 words.

Output Format:
Career 1: [Name]
- What you will do: [2 sentences]
- Why it suits you: [1 sentence]
- Starting salary in India: [approximate range]

Career 2: [Name]
...
Career 3: [Name]
...

Student Profile: I am a BCom graduate, I enjoy talking to people and organising things. I am not 
comfortable with heavy coding but I am good with Excel and PowerPoint.
```

**How the code works (analysing the prompt structure):**
- The **Role** immediately tells the AI what expertise and perspective to adopt — it won't give generic advice, it will think like an experienced counsellor
- The **Task** is one clean sentence that removes ambiguity about what the final deliverable is
- The **Instructions** create a chain-of-thought naturally — the AI now *must* follow the 4 steps in sequence
- The **Constraints** act as guardrails — they prevent the AI from going off-topic or giving impractical advice
- The **Output Format** is the most underrated part — specifying format means your output is always usable, not a wall of text

### Using Structured Prompts Inside Python for an Agent

```python
# This function creates a structured prompt dynamically based on student input

def build_career_prompt(student_background, interests):
    # Define each component of the structured prompt separately for clarity
    
    role = """You are a career counsellor with 15 years of experience helping students 
    from non-technical backgrounds transition into the tech industry."""
    
    task = "Recommend the top 3 career paths that match the student's profile."
    
    instructions = """Follow these steps:
    1. Analyse the student's educational background carefully.
    2. Identify their key interests and strengths from what they share.
    3. Match these to realistic tech careers that don't require heavy coding.
    4. Explain each career in simple, jargon-free language."""
    
    constraints = """Constraints:
    - Do NOT recommend careers requiring a CS degree.
    - Keep each recommendation under 100 words.
    - Do not use technical jargon without explaining it."""
    
    output_format = """Output Format:
    Career 1: [Name]
    - What you will do: [2 sentences]
    - Why it suits you: [1 sentence]
    - Starting salary range in India: [range]
    
    Repeat for Career 2 and Career 3."""
    
    # Combine all components into a single structured prompt string
    full_prompt = f"""
    {role}
    
    Task: {task}
    
    {instructions}
    
    {constraints}
    
    {output_format}
    
    Student Background: {student_background}
    Student Interests: {interests}
    """
    
    return full_prompt  # Return the assembled prompt to be sent to the LLM

# Example usage — calling the function with a real student's data
prompt = build_career_prompt(
    student_background="BCom graduate, 2 years experience in sales",
    interests="Talking to people, organising data in Excel"
)

print(prompt)  # Prints the final assembled prompt — ready to be sent to any LLM API
```

**How the code works:**
- Each component (role, task, instructions, constraints, output_format) is stored as its own variable — this makes it easy to update individual parts without rewriting the whole prompt
- The `f-string` (`f"""..."""`) at the end **assembles** all components into one clean prompt string with the student's real data injected
- `student_background` and `interests` are passed as arguments — this makes the function **reusable** for any student, not just one specific person
- `return full_prompt` gives back the complete prompt ready to be fed into an LLM API like OpenAI or Gemini

> **[ Student Activity ]**
>
> **Build Your Own Structured Prompt**
>
> Think of a real task you would want an AI agent to help you with — it could be from your own studies, your job, your college project, or your personal life.
> - Write all **5 components** for your prompt: Role, Task, Instructions, Constraints, Output Format.
> - Keep each component to 2–4 lines.
> - Once done, swap your prompt with the person next to you. Can they tell — just by reading your prompt — exactly what the AI should produce?
>
> *Instructor note: Pick 2–3 students to read their Role + Output Format aloud. Point out: a strong Role + clear Output Format is often what separates a good prompt from a bad one.*

---

## Reasoning Prompts

**Official Definition:** Reasoning Prompts are prompts specifically designed to trigger higher-order cognitive tasks in LLMs — such as comparison, trade-off analysis, causal reasoning, and decision-making — by structuring the question to require logical evaluation rather than information recall.

**In Simple Words:** There is a difference between asking someone "What is a mango?" (recall — they just remember the answer) and asking "Should I grow mangoes or apples in my farm in Rajasthan, given the climate and water availability?" (reasoning — they have to *think*, compare, weigh factors, and decide). Reasoning prompts push the AI into this second, harder mode of thinking.

**Real-Life Example:** A judge in a court does not just recall the law — they *reason*: "The accused committed act X, law Y applies, but there is a mitigating factor Z, so the sentence should be reduced." Reasoning prompts ask the AI to act like this judge — considering multiple factors before making a call.

![Three kinds of reasoning prompts — comparison (A vs B), causal chains (why X happened), and decision-making under constraints](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session10/session10-reasoning-prompt-types.png)

### Types of Reasoning Prompts

**1. Comparison Reasoning — "A vs B"**

Forces the AI to evaluate two or more options across defined criteria.

```
Compare Python and JavaScript for building AI agents.
Evaluate them on these 4 criteria:
1. Ease of learning for beginners
2. Availability of AI libraries
3. Deployment options
4. Community support for AI development

Present your comparison in a table, then give a final recommendation with your reasoning.
```

- **What makes this a reasoning prompt:** The criteria-based structure forces the AI to *evaluate*, not just *describe*. The final recommendation demand forces a decision with justification.

**2. Causal Reasoning — "Why did X happen?"**

Asks the AI to trace cause-and-effect chains.

```
A company deployed a chatbot for customer service. After 2 weeks, customer satisfaction scores 
dropped by 30%. Think through the possible causes step by step. 

Consider: chatbot response quality, types of customer queries, escalation handling, and emotional 
tone of responses. Then suggest the 2 most likely root causes with your reasoning.
```

- **What makes this a reasoning prompt:** It does not ask for a generic list of chatbot problems — it asks the AI to trace the chain of events that *specifically* led to the satisfaction drop.

**3. Decision-Making Reasoning — "What should I do?"**

Gives the AI a scenario with constraints and asks for a reasoned recommendation.

```
I am a startup founder with ₹5 lakhs to spend on AI tools in the next 6 months. 
My team size is 3 people. We need to build a customer support AI agent.

Given these constraints (budget, team size, timeline), should I:
Option A: Use an off-the-shelf chatbot platform (like Intercom)
Option B: Build a custom agent using LangChain and OpenAI API
Option C: Hire a freelancer to build a custom solution

Reason through each option considering cost, technical complexity, and time-to-deploy. 
Then give me a clear final recommendation.
```

### Combining CoT + Structured Prompt + Reasoning — The Power Combination

The real power comes when you combine all three techniques. Here is a full example of an agent prompt that uses all three:

```python
# A complete advanced prompt for an AI business analyst agent

advanced_agent_prompt = """
You are a Business Intelligence Analyst specialising in early-stage Indian startups.

Your task is to evaluate whether a startup idea is viable and recommend a go/no-go decision.

Follow this reasoning process step by step:
Step 1: Identify the core problem the startup is solving.
Step 2: Evaluate the market size — is this problem faced by enough people?
Step 3: Assess the competition — are there existing solutions? What is different here?
Step 4: Analyse the revenue model — how does this startup make money?
Step 5: Check the team capability — does the team have the right skills?
Step 6: Based on your analysis above, give a GO or NO-GO recommendation with clear reasoning.

Constraints:
- Do not give a vague answer. Your recommendation must be clearly GO or NO-GO.
- Use data or logical reasoning at each step — do not rely on gut feeling.
- Keep each step's analysis to 3-4 bullet points maximum.
- Write for a non-technical investor audience — no jargon.

Output Format:
**Step 1 — Problem:** [your analysis]
**Step 2 — Market:** [your analysis]
**Step 3 — Competition:** [your analysis]
**Step 4 — Revenue Model:** [your analysis]
**Step 5 — Team:** [your analysis]
**Final Recommendation:** GO / NO-GO
**Reason in one paragraph:** [your reasoning]

Startup to Evaluate: {startup_description}
"""
```

**How the code works:**
- The `role` is set as a Business Intelligence Analyst — specialised, not generic
- The `step-by-step reasoning process` is CoT baked directly into the agent's core instructions
- The `constraints` act as guardrails preventing vague, uncommitted, or jargon-heavy outputs
- The `output format` with bold headers ensures every evaluation follows the same structure — making it easy to compare multiple startup evaluations
- `{startup_description}` is a **placeholder** — in actual code this would be replaced with the real startup pitch using Python's `.format()` method or an f-string

> **[ Student Activity ]**
>
> **Make the AI Reason**
>
> Choose ONE type of reasoning prompt from what you just learned — Comparison, Causal, or Decision-Making — and write a prompt for a real situation from your own life.
>
> *Ideas to pick from:*
> - **Comparison:** "WhatsApp vs Telegram for a student study group" / "Online MBA vs Full-time MBA"
> - **Causal:** "Why do students stop attending online classes after week 3?" / "Why did a food delivery startup lose customers?"
> - **Decision:** "Should I take a job offer now or complete my certification first?"
>
> Make sure your prompt includes: the scenario, the evaluation criteria, and a request for a final reasoned recommendation.
>
> *Instructor note: Ask students to identify which reasoning type they chose and why. Highlight that real agent tasks almost always involve one of these three types.*

---

## Comparing Prompt Techniques: When to Use Which

Understanding *when* to apply each technique is as important as knowing the technique itself.

| Technique | Best Used When | Example Situation |
|-----------|---------------|-------------------|
| **Basic Prompt** | Simple, factual queries | "What is the capital of France?" |
| **Chain-of-Thought** | Math, logic, multi-step problems | Solving a word problem, debugging a reasoning error |
| **Structured Prompt** | Complex tasks needing consistent output | Building an agent prompt, writing reports, generating formatted content |
| **Reasoning Prompt** | Comparisons, decisions, analysis | "Which framework should I use?" or "Why did this agent fail?" |
| **CoT + Structured + Reasoning (Combined)** | High-stakes agent workflows | Autonomous agents doing research, analysis, or business decisions |

- **A common mistake:** Students try to add all three techniques to every prompt. This is overkill. A simple question does not need a 10-line structured prompt. Match the complexity of the technique to the complexity of the task.
- **The golden rule:** Use the *minimum* structure needed to get a *reliable* output. Simpler is better when simple works.

> **[ Student Activity ]**
>
> **Technique Match**
>
> The instructor will read out 5 real-world scenarios. For each one, shout out (or write down) which technique you would use: **Basic**, **CoT**, **Structured**, **Reasoning**, or **Combined**.
>
> *Scenarios:*
> 1. "What is machine learning?" — *(Basic)*
> 2. "A hospital's AI triage system is flagging low-priority patients as critical. Find the most likely cause." — *(CoT / Reasoning)*
> 3. "Write a weekly social media content plan for a bakery targeting working women aged 25–40 in Mumbai." — *(Structured)*
> 4. "Should our startup build a mobile app first or a web app first, given we have ₹3 lakhs and 2 developers?" — *(Reasoning — Decision)*
> 5. "Design an AI agent that onboards new employees at a company, explains company policies, answers HR questions, and escalates unresolved issues." — *(Combined)*
>
> *Instructor note: Don't give the answers immediately — let students debate briefly before confirming. The goal is to build intuition for technique selection.*

---

## How to Evaluate a Prompt's Quality

Before you use a prompt in a real agent, you should evaluate it. Here is a simple mental checklist:

**The CICO Framework for Prompt Evaluation:**

- **C — Clarity:** Is every instruction crystal clear? Would a stranger understand exactly what to do?
- **I — Intent:** Does the prompt clearly communicate the *goal* of the task, not just the task itself?
- **C — Constraints:** Are guardrails in place to prevent the AI from going off-track?
- **O — Output Specification:** Is the expected output format, length, and structure clearly defined?

### Hands-On Exercise: Fix This Broken Prompt

**Broken Prompt:**
```
Tell me about AI agents and their benefits for businesses.
```

**Problem analysis:**
- No Role — AI doesn't know from whose perspective to answer
- No Task clarity — "tell me about" is too vague
- No Constraints — response could be 50 words or 5000 words
- No Output Format — could be paragraphs, bullets, or a poem

**Fixed Prompt (using Structured Prompt technique):**
```
You are a technology consultant presenting to a board of directors of a mid-sized Indian retail 
company with no technical background.

Task: Explain what AI agents are and list 3 specific benefits they can bring to a retail business.

Instructions:
1. First, define AI agents in one simple sentence using a relatable analogy.
2. Then explain each benefit with a specific retail example (e.g., inventory management, customer service).

Constraints:
- Do not use technical jargon. Assume zero tech knowledge.
- Keep the total response under 300 words.
- Do not mention competitor products or brand names.

Output: 
- One-paragraph definition
- 3 bullet points, one per benefit, each with a concrete retail example
```

> **[ Student Activity ]**
>
> **Run the CICO Check**
>
> Apply the **CICO Framework** to this prompt and score each letter Pass or Fail:
>
> *Prompt to evaluate:* `"You are a helpful assistant. Help the user plan their week."`
>
> | Letter | Question to Ask | Pass or Fail? | What is Missing? |
> |--------|----------------|---------------|-----------------|
> | C — Clarity | Is every instruction crystal clear? | ? | ? |
> | I — Intent | Is the goal of the task communicated? | ? | ? |
> | C — Constraints | Are there guardrails to keep the AI on track? | ? | ? |
> | O — Output | Is the format/length of the response specified? | ? | ? |
>
> After scoring, rewrite the prompt so it passes all 4 letters.
>
> *Instructor note: This is a quick individual exercise. After 3–4 minutes, ask one student to share their rewritten prompt and check it against CICO live.*

---

## Iterative Prompt Refinement: Improving Prompts Like a Pro

A great prompt is rarely written in one shot. The process of improving a prompt is called **Iterative Prompt Refinement**.

**Official Definition:** Iterative Prompt Refinement is the process of systematically testing a prompt, identifying where the output falls short, and modifying specific components of the prompt to improve the output — repeating this cycle until the desired quality is consistently achieved.

**In Simple Words:** Think of how a chef perfects a recipe. First attempt — too salty. So they reduce the salt. Second attempt — not spicy enough. They add chilli. Third attempt — perfect. Prompt refinement works the same way: test, identify the flaw, fix that one thing, test again.

![Iterative prompt refinement — write, test, diagnose, fix one thing at a time, then repeat](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session10/session10-iterative-refinement-loop.png)

### The 4-Step Refinement Loop

```
Step 1: WRITE — Write your initial prompt
    ↓
Step 2: TEST — Run the prompt and read the output carefully
    ↓
Step 3: DIAGNOSE — Identify exactly what went wrong:
         - Too generic? → Add more Role/Context
         - Wrong format? → Add Output Format specification
         - Missing reasoning? → Add CoT trigger
         - Going off-topic? → Add Constraints
    ↓
Step 4: FIX — Change only the diagnosed component. Do not rewrite the whole prompt.
    ↓
Back to Step 2 — Test again
```

- **Critical tip:** Change only ONE thing at a time between tests. If you change Role AND Constraints AND Format all at once, you won't know which change actually fixed the problem.
- **Track your iterations:** Keep a simple log of what you changed and what improved. This builds your intuition for prompt design over time.

> **[ Student Activity ]**
>
> **One Fix at a Time**
>
> Here is a prompt and the AI output it produced. Your job is to diagnose what is wrong and fix *only one thing*.
>
> **Original Prompt:** `"Give me tips to be more productive."`
>
> **AI Output received:** *"Here are some productivity tips: 1. Wake up early. 2. Make a to-do list. 3. Avoid distractions. 4. Take breaks. 5. Stay hydrated."*
>
> - Using the **4-Step Refinement Loop**, diagnose: which of these is the problem — no Role, no Output Format, no Constraints, or missing CoT?
> - Make exactly **one change** to the prompt to fix the most critical problem.
> - Write your improved prompt and predict how the AI's response will change.
>
> *Instructor note: The most common answer students give is "add more detail" — redirect them to diagnose the specific component. The main issue here is no Role + no Constraints. Accept any single fix that genuinely improves specificity.*

---

## Best Practices for Agent Prompt Design

These are the practices used by professional AI engineers when building real-world agents:

**1. Be Explicit, Not Implicit**
- Bad: "Answer professionally."
- Good: "Use formal English. No slang. No contractions (e.g., write 'do not' not 'don't'). Keep sentences under 20 words."

**2. Use Positive Instructions Over Negative Ones**
- Bad: "Don't be vague. Don't give long answers."
- Good: "Give specific, actionable answers. Keep each point to 1–2 sentences."
- *Why:* LLMs sometimes over-focus on the negated concept. "Don't think about a pink elephant" — what did you just think about?

**3. Anchor the Persona Firmly**
- Add 2–3 specific details to the Role to make it more vivid: Not just "You are a teacher" but "You are a patient, encouraging high school teacher who specialises in explaining abstract concepts using everyday examples."

**4. Put the Most Important Instruction Last**
- Research shows that LLMs pay more attention to instructions at the *beginning* and the *end* of a prompt. If there is one instruction that absolutely must be followed, place it at the very end.

**5. Always Specify What Happens in Edge Cases**
- Add a fallback instruction: "If the user's question is outside your area of expertise, say 'I am not equipped to answer this. Please consult [relevant expert].' Do not guess."

**6. Test Across Different Inputs**
- A prompt that works perfectly for one type of input may fail on another. Always test your agent prompt with 3–5 different types of inputs before calling it final.

> **[ Student Activity ]**
>
> **Spot the Violations**
>
> Read this agent prompt carefully and identify which **2 best practices** it violates:
>
> *Prompt:* `"You are an AI. Don't be rude. Don't give long answers. Don't use jargon. Help the user with whatever they ask."`
>
> - Write down the 2 violations with a one-line explanation for each.
> - Then rewrite the prompt to fix both violations — without changing the core purpose of the agent.
>
> *Violations to find:*
> 1. It uses **negative instructions** instead of positive ones (Best Practice #2)
> 2. The **persona is not anchored** — "You are an AI" is not a Role (Best Practice #3)
>
> *Instructor note: See if students can spot both violations independently. The rewrite exercise is a bonus for fast finishers — ask one student to share their rewrite.*

---

## Practical Prompt Design Session: Building an Agent Prompt From Scratch

Let's apply everything in one full example. We will build a **complete system prompt for an AI Study Assistant agent** that a student would use to prepare for exams.

```python
# Complete system prompt for a Student Study Assistant Agent
# This prompt uses Role, CoT, Structured Format, Constraints, and Reasoning techniques

study_agent_system_prompt = """
You are Arya, a patient and encouraging academic tutor specialising in helping undergraduate 
students understand difficult concepts. You have taught students from non-engineering backgrounds 
for over 10 years and you excel at making complex topics feel simple and approachable.

Your core capabilities:
1. Explain any academic concept in simple language with relatable Indian examples
2. Create short practice questions to test understanding
3. Identify gaps in a student's reasoning and gently correct them
4. Break down complex problems step by step

When a student asks you to explain a topic, ALWAYS follow this process:
Step 1: Check if they have any prior knowledge — ask one quick question if needed
Step 2: Give a simple analogy or real-life example FIRST, before the technical definition
Step 3: Then provide the technical definition
Step 4: Give 1-2 examples with increasing complexity
Step 5: Ask the student to summarise what they learned in their own words

Constraints:
- Never give a direct answer to a practice question — guide the student to the answer
- Do not use academic jargon without immediately explaining it in brackets
- Never make the student feel bad for not knowing something — always use encouraging language
- If a student seems confused, ask ONE clarifying question, not multiple questions at once
- Keep all explanations under 200 words unless the student asks for more detail

Your tone: Warm, encouraging, patient. Like a helpful older sibling who is good at studies.

If the student says something like "I don't understand" or "This is too hard", respond with:
"Totally okay! Let's try a different approach..." and then use a different analogy.
"""

# This prompt would be sent to an LLM API as the 'system' message
# Every student message after this would be the 'user' message
# The agent would maintain this persona and follow these instructions throughout the conversation
print("Study Agent system prompt is ready.")
print(f"Prompt length: {len(study_agent_system_prompt)} characters")
```

**How the code works:**
- `study_agent_system_prompt` is a multi-line string (using triple quotes `"""`) that holds the entire system prompt
- The **Role** is given a *name* (Arya) and specific personality traits — this makes the agent far more consistent in its behaviour than a nameless, trait-less role
- The **CoT process** (Steps 1–5) is embedded as the agent's "when a student asks" workflow — so every explanation follows a logical teaching sequence
- The **Constraints** prevent common agent failures: giving away answers, using jargon, discouraging students
- The **edge case handling** at the end (`"I don't understand"`) ensures the agent never gets stuck or gives a cold response when a student struggles
- `len(study_agent_system_prompt)` at the end measures the character count — in real LLM APIs, you are charged by tokens (roughly 4 characters = 1 token), so prompt length management matters for cost

> **[ Student Activity ]**
>
> **Build Your Mini Agent**
>
> This is your session capstone. Design a **complete system prompt** for an AI agent that helps *you* with something in your real life — your studies, your work, your side project, or your daily routine.
>
> Your system prompt **must include all 4 of these**:
> - **Role** — Give the agent a name and a specific persona with 2–3 personality traits
> - **CoT Process** — Write at least 3 numbered steps the agent must follow before responding
> - **Constraints** — Write at least 2 guardrails (what the agent must NOT do)
> - **Output Format** — Specify how the agent's response should be structured
>
> *Examples of agents you can build:*
> - A "daily planner" agent that helps you prioritise your tasks each morning
> - A "mock interviewer" agent that asks you questions and gives feedback
> - A "side hustle advisor" agent that helps evaluate business ideas
> - A "fitness coach" agent that creates workout plans based on your constraints
>
> Once done, read your Role and Constraints to the batch. The class votes: does this agent sound reliable and useful?
>
> *Instructor note: This is the most important activity of the session — give students the full 10 minutes. Walk around and help students who are stuck on the Role or CoT steps. In the last 2 minutes, pick 2–3 students to share. Point out what makes each agent prompt strong.*

---

## Key Takeaways

- **Prompt Engineering is a skill, not a trick.** Advanced techniques like Chain-of-Thought, Structured Prompts, and Reasoning Prompts give you consistent, high-quality AI outputs — the kind that are actually usable in real products.
- **Chain-of-Thought (CoT)** works by forcing the LLM to reason step by step before answering, which significantly reduces errors in logic, math, and multi-factor problems.
- **Structured Prompts** with five components — Role, Task, Instructions, Constraints, Output Format — are the professional standard for building agent prompts because they eliminate ambiguity and produce predictable, formatted outputs.
- **Reasoning Prompts** elevate the AI from information recall to genuine analysis — they are essential when your agent needs to compare options, trace causes, or make decisions.
- **Iterative Refinement** is the real-world workflow: test, diagnose, fix one thing, test again. The best agent prompts are refined over many iterations, not written perfectly in one shot.
- In the coming sessions, we will take these advanced prompts and integrate them directly into agent frameworks like **LangChain and CrewAI**, where prompt design is the primary lever for controlling how a multi-agent system thinks and acts.

---

## Important Commands, Libraries, Terminologies Used

| Term / Command | Category | Meaning |
|----------------|----------|---------|
| **Prompt Engineering** | Concept | The discipline of designing inputs to LLMs to produce reliable, accurate outputs |
| **Chain-of-Thought (CoT)** | Technique | Asking the LLM to show reasoning steps before giving a final answer |
| **Zero-Shot CoT** | Technique | Triggering step-by-step reasoning with a phrase only (no examples) — e.g., "Let's think step by step" |
| **Few-Shot CoT** | Technique | Showing 1–2 solved examples with reasoning before asking your question |
| **Structured Prompt** | Technique | A prompt template with defined components: Role, Task, Instructions, Constraints, Output Format |
| **Role** | Prompt Component | Defines who the AI is (e.g., "You are a senior financial advisor") |
| **Task** | Prompt Component | States what the AI must deliver (e.g., "Analyse this portfolio") |
| **Instructions** | Prompt Component | Step-by-step guidance on how to complete the task |
| **Constraints** | Prompt Component | Guardrails — what the AI must NOT do or must limit |
| **Output Format** | Prompt Component | Specifies the structure, length, and style of the expected response |
| **Reasoning Prompt** | Technique | A prompt that requires comparison, causal analysis, or decision-making from the LLM |
| **Iterative Prompt Refinement** | Process | Testing, diagnosing, and fixing one component of a prompt at a time to improve quality |
| **CICO Framework** | Evaluation | Clarity, Intent, Constraints, Output — a 4-point checklist for evaluating prompt quality |
| **System Prompt** | LLM Concept | The initial instruction sent to an LLM agent that defines its persona and rules for the entire conversation |
| **f-string** | Python | Python syntax (`f"..."`) for embedding variables inside strings — used to inject data into prompts |
| **LLM (Large Language Model)** | Concept | AI models like GPT-4, Gemini, Claude that generate text based on input — the engine behind AI agents |
| **Token** | LLM Concept | The basic unit of text that LLMs process (~4 characters = 1 token); LLM API costs are measured in tokens |
| **`"""..."""`** | Python | Triple-quoted multi-line string — used to write long prompts cleanly in Python code |
| **`.format()`** | Python | Python string method to replace placeholders like `{name}` with actual values |
