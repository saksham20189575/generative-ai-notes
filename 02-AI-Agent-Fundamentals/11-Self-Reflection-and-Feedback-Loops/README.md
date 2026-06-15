# Self-Reflection and Feedback Loops

## Context of This Session

In the previous session, we explored **Advanced Prompt Engineering for Agents** — how to write structured, chain-of-thought, and reasoning prompts that guide an AI to think step by step and produce cleaner, more predictable outputs. We learned to break down a prompt into role, task, instructions, constraints, and output format. We practiced chain-of-thought, where the AI reasons through a problem step by step before answering, and we compared that against basic one-liner prompts to see how structure dramatically changes output quality.

Now that you know how to *design* a well-crafted prompt, the next challenge you will face in the real world is: **what happens when the AI still gets it wrong?** Even the best-structured prompt can sometimes produce an incomplete answer, a vague explanation, or an outright factual error. In this session, we take a big leap forward — we go beyond just writing prompts and start teaching the AI to **check its own work**, **spot its own mistakes**, and **keep improving its output** through loops of reflection and feedback.

**In this session, you will:**

- Understand why AI agents need self-reflection and what it looks like in practice
- Learn how to design prompts that make an AI critique and rewrite its own response
- Practice iterative prompting — improving output step by step across multiple rounds
- Understand how feedback loops work and how agents use them to self-regulate quality
- Build a complete agent prompt flow that combines instructions, reflection, and feedback
- Compare one-shot, iterative, and reflection-based strategies and know when to use each
- Evaluate AI responses by recognising errors, gaps, hallucinations, and weak output
- Optimise feedback loops so they are efficient and reusable for real-world agent workflows

---

## Introduction to Self-Reflection in AI Agents

### The Problem That Self-Reflection Solves

Picture this: you are building a customer support agent for an e-commerce company. The agent's job is to answer customer queries about orders, returns, and refunds. A customer asks:

> *"I ordered a jacket 10 days ago and it still hasn't arrived. What should I do?"*

The AI responds:

> *"Please contact customer support for assistance."*

That answer is technically not wrong — but it is absolutely useless. It gives the customer no actionable steps, no empathy, and no actual information about the return window, how to raise a complaint, or what typically causes delays. The AI picked the easiest possible answer and stopped.

This is the default behaviour of an AI without reflection — it gives you the **first thing that comes to mind**, not the **best possible answer**. Self-reflection is the mechanism we use to change that.

### What is Self-Reflection?

- **Official Definition:** Self-reflection in AI refers to the ability of an agent to **review, evaluate, and revise its own output** before or after presenting it to the user.
- **In Simple Words:** It is the AI's version of reading your own answer before submitting it. The AI asks itself: *"Is this correct? Is this complete? Have I actually answered what was asked? Can I do better?"* — and then acts on those questions.
- **Real-Life Example:** Think of a student writing an exam. A student who submits the paper the moment they finish the last question is taking a risk. A student who re-reads the paper, catches a calculation error, and fixes a misunderstood question — that student is practising self-reflection. Self-reflection gives AI agents that same second-check habit.

### Seeing the Difference — Without Reflection vs With Reflection

The clearest way to understand why self-reflection matters is to see the same task handled both ways.

![Without reflection the model stops at a vague first draft; with reflection it checks criteria and produces specific, actionable steps](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session11/session11-without-vs-with-reflection.png)

**Scenario:** You ask an AI to write a short description of a healthy morning routine for a beginner.

---

**Without Reflection — Bad Response:**

```
Prompt: Write a short description of a healthy morning routine for a beginner.

AI Response:
A healthy morning routine includes waking up early, exercising, and eating a good breakfast.
Staying hydrated is also important.
```

**What is wrong with this response?**
- It is vague — "exercising" gives no guidance on what type or for how long.
- It is incomplete — it skips important beginner-friendly details like sleep time, screen time, or mental wellness.
- It reads like a generic tip, not a structured routine a beginner can actually follow.
- A beginner reading this will walk away with no practical plan.

---

**With Reflection — Good Response:**

```
Prompt: Write a short description of a healthy morning routine for a beginner.

After writing your description, check:
- Does it have at least 4 specific, actionable steps?
- Is it simple enough for someone with no prior fitness habit?
- Does it include a time estimate for each step?

If any answer is No, rewrite it until all answers are Yes.

AI Response (after reflection):
Here is a simple morning routine any beginner can follow:

1. Wake up at the same time every day (6:30–7:00 AM) — consistency trains your body clock.
2. Drink one full glass of water (5 minutes) — rehydrates your body after 7–8 hours of sleep.
3. Do a 10-minute light stretch or a short walk — wakes up your muscles without overwhelming you.
4. Eat a simple breakfast: oats, fruit, or eggs (15 minutes) — fuels your brain for the morning.
5. Spend 5 minutes writing down 3 things you want to accomplish today — sets focus and intention.

Total time: approximately 35–40 minutes. Start with these five steps and build from there.
```

**What makes this response good?**
- Each step is **specific and actionable** — the beginner knows exactly what to do.
- **Time estimates** are included so the routine feels manageable.
- The tone is encouraging and realistic for a beginner.
- The final line gives motivation and a clear next step.

The difference between these two responses is not the AI's ability — it is whether or not the AI was asked to reflect. That one extra instruction to check and improve produced a dramatically better result.

### The "Thinking Twice" Principle

- Every first draft produced by an AI is a **rough attempt** — useful as a starting point, but rarely the best version.
- Self-reflection adds a deliberate second pass: the AI reads its own output with a critical eye and asks, *"If a real person read this, would it actually help them?"*
- Think of it as the difference between a **spell-checker and a proof-reader** — spell-check catches typos, but a proof-reader catches unclear sentences, missing logic, and weak arguments. Self-reflection is the AI acting as its own proof-reader.
- When you build agents, the agents that perform best in the real world are always the ones with a **built-in review step** — not because they are smarter, but because they are more disciplined.

---

## Self-Correction Prompts

### What is a Self-Correction Prompt?

- **Official Definition:** A self-correction prompt is a prompt that explicitly **instructs the AI to verify, critique, and fix its own response** within the same interaction, before delivering the final answer.
- **In Simple Words:** You are not just asking the AI to answer — you are asking it to be its own quality checker. You say: *"Answer this, then check your own answer, then fix whatever is wrong."*
- **Real-Life Example:** Think of a **bank loan officer**. Before approving a loan, they fill out a form. Then a second officer reviews the same form for errors before it goes for final approval. The second review is the self-correction step — the system catches mistakes before they become problems.

### The Three-Stage Structure

A good self-correction prompt always has three distinct stages:

![Self-correction in three stages — generate a draft, critique gaps, then rewrite using that critique](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session11/session11-self-correction-three-stages.png)

- **Stage 1 — Generate:** Ask the AI to produce an initial response to the task.
- **Stage 2 — Critique:** Ask the AI to review what it just wrote and identify what is missing, incorrect, or weak.
- **Stage 3 — Rewrite:** Ask the AI to produce a new, improved version based on its own critique.

Keeping these three stages **separate and explicit** is the key. If you merge them into one vague instruction like *"Write a perfect answer,"* the AI does not reliably apply all three stages. Spelling them out forces the AI to actually do each step.

### Full Example — Self-Correction in Action

**Task:** Explain why sleep is important for students.

---

**Without Self-Correction — Bad Response:**

```
Prompt: Explain why sleep is important for students.

AI Response:
Sleep is very important for students. It helps them feel rested and
perform better in school. Students should get enough sleep every night.
```

**Why this is a bad response:**
- It is circular — it says sleep is important because it helps students perform better, but gives no reason *why*.
- It has no scientific backing or specific detail — "feel rested" is too vague.
- It gives no practical guidance — students do not know what "enough sleep" means.
- Reading this teaches a student nothing they did not already know.

---

**With Self-Correction Prompt — Good Response:**

```
Prompt:

Stage 1 — Answer: Explain why sleep is important for students.

Stage 2 — Critique: Review your answer above. What important facts,
reasons, or details are missing? What could be explained better?

Stage 3 — Rewrite: Now write an improved explanation that fixes all
the gaps and weaknesses you identified.

---

AI — Stage 1 (Initial Answer):
Sleep is very important for students. It helps them feel rested and
perform better in school.

AI — Stage 2 (Critique):
My initial answer is too vague. I did not explain:
- What actually happens in the brain during sleep
- The specific consequences of sleep deprivation on learning
- How many hours of sleep students need and why
- Any practical advice

AI — Stage 3 (Improved Answer):
Sleep is one of the most powerful tools a student has — not for
resting, but for learning.

During deep sleep, the brain processes and stores everything learned
during the day. Think of it as your brain's nightly "save" button —
without it, the information from class never gets properly saved to
long-term memory.

Research shows that students who get 7–9 hours of sleep:
- Retain information 40% better than those who sleep less than 6 hours
- Score higher on tests that require problem-solving and creativity
- Have better focus and attention spans during lectures

Sleep deprivation has the opposite effect. A student running on 5
hours of sleep has the same cognitive impairment as someone slightly
intoxicated — their reaction time is slower, their memory is weaker,
and their decision-making is poor.

The practical rule: aim for 7–9 hours on school nights. Sleep at the
same time every night — your brain learns your sleep schedule and
becomes more efficient at it.
```

**Why the corrected response is genuinely better:**
- It explains the **mechanism** — what the brain actually does during sleep.
- It uses a **concrete analogy** (the "save button") that is instantly understandable.
- It includes **specific, verifiable details** (40% retention improvement, 7–9 hours).
- It names the **consequences** of bad sleep with a vivid comparison.
- It ends with **actionable advice** the student can apply tonight.

The Stage 2 critique was the turning point — once the AI identified exactly what was missing, Stage 3 became easy to write well.

### Designing Effective Self-Correction Prompts

- **Separate the stages with clear labels** — "Stage 1", "Stage 2", "Stage 3" or "Step 1", "Step 2", "Step 3". This is not optional. Without clear labels, the AI tends to skip the critique stage and go directly to the rewrite, which defeats the purpose.
- **Tell the AI what to look for in the critique** — Instead of "find any issues," say "check for missing facts," "check if the explanation is clear for a beginner," or "check if every claim is supported." Specific critique instructions produce specific improvements.
- **Use the critique to guide you as well** — When you read Stage 2, you learn what the AI considers its own weaknesses. This tells you where your original prompt was unclear or under-specified.
- **Common Mistake:** Writing a single-line instruction like *"Give me a detailed, perfect answer"* — this sounds like it should trigger self-correction, but it does not. The AI interprets it as one instruction and gives you one (better) answer without the structured review. The three-stage structure is what forces genuine self-correction.

---

## Iterative Prompting

### The Core Idea

Imagine you are directing a film. You do not film one scene, call it done, and submit the movie. You shoot a take, watch it back, give notes — *"That line needs more energy," "Move the camera left,"* — and shoot again. Each take is better than the last because you are building on what worked and fixing what did not.

**Iterative prompting** applies exactly this logic to working with AI. Instead of expecting one perfect prompt to produce one perfect answer, you treat the conversation as a **creative process** — multiple rounds, each one refining and improving the output.

### What is Iterative Prompting?

- **Official Definition:** Iterative prompting is the practice of **sending a sequence of targeted follow-up prompts**, where each prompt builds on the previous response to progressively improve the quality, depth, or accuracy of the output.
- **In Simple Words:** You start with a first version, look at what is missing or weak, and then give the AI specific instructions to fix that one thing. Then you look again, fix the next thing. You keep going until the output is exactly what you need.
- **Real-Life Example:** Think of how a sculptor works. They start with a rough block of stone — the general shape is there, but it is not finished. They chisel away one section at a time, refining details with each pass. Iterative prompting works the same way — each round of prompting chisels the response closer to the final form you want.

### Why One-Shot Prompting is Not Always Enough

One-shot prompting has its place. If you ask *"What is the boiling point of water?"* — you get a perfect answer in one shot and you are done. There is no need to iterate.

But here is what happens when you use one-shot prompting on a task that is genuinely complex:

---

**One-Shot Attempt — Bad Response:**

```
Prompt: Write a business proposal for a new healthy food delivery startup
targeting college students in India.

AI Response (one-shot):
Our company delivers healthy food to college students.
We offer nutritious meals at affordable prices.
Our target market is students aged 18–24.
We plan to expand to multiple cities.
```

**Why this is a bad response for this task:**
- It reads like a title slide, not a business proposal.
- There is no market analysis, no financial projection, no unique selling point.
- The "affordable prices" claim has no numbers behind it.
- A real investor or professor reading this would reject it immediately.

The issue is not that the AI cannot write a business proposal. The issue is that one shot is not enough for a task this complex — there are too many dimensions (market, product, financials, competition, execution plan) for a single prompt to cover well.

---

### The Iterative Prompting Cycle

The cycle has four stages. The key is to move through them deliberately:

1. **Draft** — Send an initial prompt to get the first version. Do not expect perfection here. The draft is just a starting shape.
2. **Review** — Read the output carefully. Ask yourself: *What is missing? What is too vague? What is incorrect? What needs more depth?* Pick the **single most important thing** to fix first.
3. **Refine** — Send a follow-up prompt that targets that one thing specifically.
4. **Repeat** — After each refinement, do another review. Keep going until the output meets your standard.

![The iterative prompting cycle — draft, review, refine one thing at a time, repeat until the output meets your bar](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session11/session11-iterative-prompting-cycle.png)

### Full Example — Three Rounds of Iterative Prompting

**Task:** Write an explanation of how ATMs work, for a village school student who has never seen one.

---

**Round 1 — Draft:**

```
Prompt: Explain how an ATM works for a village school student who has
never seen one before.

AI Response (Round 1):
An ATM is a machine that gives you cash. You insert your debit card,
enter your PIN, select the amount, and the machine gives you money.
It is connected to your bank account.
```

**Review after Round 1:**
- The explanation is technically accurate but too compressed. A student who has never seen an ATM has no mental model for "debit card," "PIN," or "bank account." We need to build those concepts first.
- Missing: what a debit card is, what a PIN is, what happens "behind the scenes."

---

**Round 2 — Refine:**

```
Prompt: Good start. But this student has never seen a debit card or
heard the word PIN. Rewrite the explanation and first introduce
what a debit card and a PIN are using simple village-life comparisons.
Then explain the ATM steps using those same comparisons.

AI Response (Round 2):
Think of a debit card like a special pass that your bank gives you.
Just like a school ID proves you are a student of that school, the
debit card proves you have a bank account and money in it.

A PIN is a secret code — like the lock on your trunk at home that
only you know the combination to. It makes sure no one else can use
your card.

Now, here is how an ATM works step by step:
1. You put your card into the ATM slot — like showing your ID at a gate.
2. You type in your secret PIN — like entering the combination to your trunk.
3. You tell the ATM how much money you want.
4. The ATM checks with your bank: "Does this person have that much money?"
5. If yes, the ATM counts out the cash and hands it to you.
```

**Review after Round 2:**
- Much better! The comparisons are excellent and relatable. But it still does not explain *where* the cash in the ATM comes from, or what happens if the ATM is wrong. A curious student will ask.

---

**Round 3 — Refine Again:**

```
Prompt: Excellent. Now add two more things: (1) explain where the
cash inside the ATM comes from, and (2) what happens to your bank
account after you take out money. Keep the same simple tone.

AI Response (Round 3):
[Previous explanation stays as is, and adds:]

Where does the cash inside the ATM come from?
The bank fills the ATM regularly — just like a shopkeeper refills
their cash drawer. Bank staff bring bundles of notes and load them
into the machine, often at night when the ATM is not busy.

What happens to your bank account?
The moment you take out ₹500, your bank account is reduced by ₹500.
It is like taking money from a piggy bank — what you remove is no
longer there. This is why it is important to check your account
balance before withdrawing, so you do not take out more than you have.
```

**Why Round 3 is the version you would actually use:**
- The explanation now covers the full picture — what the card is, what the PIN is, how the transaction works, where the cash comes from, and what the consequence of withdrawal is.
- Every concept is anchored to a real-world object the student already knows.
- No single round produced this quality — it took three deliberate passes.

### Best Practices for Iterative Prompting

- **Fix one thing at a time** — Do not send a follow-up prompt that asks the AI to fix five different things simultaneously. Pick the most important gap and target it. This gives you cleaner, more controlled improvements.
- **Acknowledge what is working** — Start your follow-up with what you want to keep: *"The structure is great. Now make the examples more specific."* This signals to the AI that it should not throw away the good parts.
- **Carry context forward** — Always refer to the previous response. Say *"In your last answer, the third paragraph was too technical — simplify it."* This is far more effective than starting a new prompt from scratch.
- **Know when to stop** — 3 to 5 rounds is the healthy range. If you are on Round 7 and the output is still not right, the problem is your initial prompt — go back and redesign it from scratch with clearer constraints.
- **Common Mistake:** Saying *"This is bad, try again"* without specifying what is bad. The AI will just produce another version of the same answer. Be specific: *"The second paragraph assumes the reader knows what SQL is. Explain it as if they have never heard of SQL."*

---

## Designing Feedback Loops for AI Agents

### The Gap Between One Conversation and a Working Agent

There is a big difference between using an AI in a chat and building a **working agent**. In a chat, you are present at every turn — you read the output, spot the problem, and send a correction. That works fine for personal use.

But when you build an agent — say, a customer support bot, a content review tool, or an automated writing assistant — **you are not there for every conversation**. The agent handles hundreds of interactions without you watching. If it produces a bad answer in interaction number 47, there is nobody there to catch it.

This is the problem that **feedback loops** solve. A feedback loop makes the agent its own quality controller — it generates output, checks that output against a standard, and fixes it automatically, without needing you to be present.

### What is a Feedback Loop?

- **Official Definition:** A feedback loop is a **mechanism where the output of a system is evaluated against a set of criteria and the result of that evaluation is used as input to improve the next output**.
- **In Simple Words:** It is a cycle. The agent does something, checks if it did it correctly using a predefined checklist, and if it did not, it does it again — better. It keeps cycling until the standard is met.
- **Real-Life Example:** Think of a **thermostat**. You set the temperature to 24°C. The thermostat measures the room temperature constantly. If it drops below 24°C, the heater turns on. If it rises above 24°C, the heater turns off. The thermostat is running a feedback loop — it checks the output (room temperature) against a criterion (24°C) and acts accordingly, without you doing anything. AI feedback loops work on the exact same principle.

### Two Types of Feedback Loops

Feedback loops in AI agents come from two different sources:

![User feedback loops vs internal feedback loops — human steering versus checklist-driven self-evaluation in the prompt](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session11/session11-feedback-loop-user-vs-internal.png)

**1. User Feedback Loop**

The user reads the output and provides direct correction or guidance. The agent uses that input to adjust its next response.

```
User: "Summarise this article for me."

Agent: "The article discusses global warming and its effects on
polar ice caps, leading to rising sea levels worldwide."

User: "That's too vague. Give me 3 specific facts from the article,
not a general summary."

Agent: "Here are 3 specific facts from the article:
1. Arctic sea ice has decreased by 13% per decade since 1979.
2. Sea levels have risen by 8–9 inches since 1880.
3. The last decade (2011–2020) was the hottest on record globally."
```

The user's correction is the feedback. The agent takes it and produces a targeted, improved response. This loop can continue until the user is satisfied.

**2. Internal Feedback Loop**

No user input is needed. The agent evaluates its own output against criteria embedded in the prompt and decides whether to accept or revise it.

```
Prompt: "Write a 2-sentence product disclaimer for a health supplement.

After writing it, evaluate:
- Is it under 30 words? (Yes/No)
- Does it include a warning that results may vary? (Yes/No)
- Does it recommend consulting a doctor? (Yes/No)

If any answer is No, rewrite and re-evaluate until all three are Yes."

Agent — Attempt 1:
"This supplement supports general wellness. Take one capsule daily."

Agent — Self-Evaluation:
- Under 30 words? Yes
- Includes results may vary? No
- Recommends doctor? No

Agent — Attempt 2:
"This supplement supports general wellness. Results may vary.
Always consult your doctor before starting any supplement routine.
Take one capsule daily as directed."

Agent — Self-Evaluation:
- Under 30 words? Yes (28 words)
- Includes results may vary? Yes
- Recommends doctor? Yes
All criteria met. Final answer accepted.
```

No human was involved in that correction cycle. The agent checked its own work and looped until all criteria were satisfied.

### Building a Feedback Loop Prompt — Step by Step

A well-designed feedback loop prompt has four parts:

1. **Generate** — A clear, specific task for the agent to complete.
2. **Evaluate** — A checklist of measurable criteria the agent uses to judge its own output.
3. **Improve** — An instruction to revise and re-evaluate if any criterion fails.
4. **Deliver** — An instruction on how to present the final accepted output.

**Full Example — Feedback Loop for a Job Application Email:**

```
Task:
Write a professional email to apply for a Data Analyst internship at a
tech startup. The applicant is a 2nd-year BCA student with basic Python
and Excel skills.

Evaluate your email against these criteria:
- Does it open with a confident, specific first sentence (not "I am writing
  to apply")? (Yes/No)
- Does it mention Python and Excel skills with a brief example? (Yes/No)
- Is the email under 150 words? (Yes/No)
- Does it close with a clear call to action (asking for an interview or
  a follow-up)? (Yes/No)

If any answer is No, rewrite the email and re-evaluate.
Repeat until all four criteria are satisfied.
Present the final accepted version only.

---

Agent — Attempt 1:
Subject: Application for Data Analyst Internship

Dear Hiring Manager,

I am writing to apply for the Data Analyst Internship position at your
company. I am a 2nd-year BCA student with knowledge of Python and Excel.
I am hardworking and eager to learn. I hope to hear from you soon.

Regards,
[Name]

Agent — Self-Evaluation (Attempt 1):
- Confident opening (not "I am writing to apply")? No — opens with exactly that.
- Mentions Python/Excel with an example? No — mentions them but gives no example.
- Under 150 words? Yes
- Clear call to action? No — "I hope to hear from you soon" is passive, not a call to action.
Criteria not met. Rewriting.

---

Agent — Attempt 2:
Subject: Data Analyst Internship Application — BCA Student with Python & Excel Skills

Dear Hiring Manager,

Your internship programme is an exciting opportunity, and I believe
my skills make me a strong fit.

As a 2nd-year BCA student, I have used Python to automate data
cleaning tasks in a college project, reducing manual effort by 60%.
I am also proficient in Excel, including pivot tables and VLOOKUP for
data analysis.

I would love to bring this hands-on experience to your team. Could
we schedule a 15-minute call this week to discuss how I can contribute?

Warm regards,
[Name]

Agent — Self-Evaluation (Attempt 2):
- Confident opening? Yes — starts with what makes this interesting, not "I am writing."
- Python/Excel with example? Yes — Python automation project with a specific result.
- Under 150 words? Yes (95 words)
- Clear call to action? Yes — asks for a specific 15-minute call.
All criteria met. Final version accepted.
```

**Why the second email is dramatically better:**
- The opening immediately shows the applicant knows why this company is interesting — it is confident and personalised.
- The Python example is **specific** (automation, 60% reduction) — not just "I know Python."
- The call to action is **assertive** (asks for a specific call) — not passive.
- The feedback loop found all four failures in Attempt 1 and fixed them in Attempt 2 with no human involved.

### When to Use User Feedback vs Internal Feedback

- Use **user feedback loops** when the task is creative, subjective, or depends on personal preference. Example: writing a speech, designing a plan, crafting a story. The user's reaction is the most important signal.
- Use **internal feedback loops** when the task has objective, measurable criteria. Example: word count, inclusion of specific elements, format compliance. These criteria do not need a human to evaluate — the agent can check them itself.
- In advanced agents, both loops work together: the internal loop maintains quality automatically, and the user loop allows the user to steer direction when they want something different.

---

## Building Complete Agent Prompt Flows

### From Single Prompts to a Designed System

Everything we have covered so far — self-reflection, self-correction, iterative prompting, and feedback loops — are individual techniques. Each one is powerful on its own. But when you **combine them into a single structured flow**, you create something much more valuable: an agent that can handle complex, multi-step tasks reliably, consistently, and without constant supervision.

An **agent prompt flow** is that combination. It is a designed system — not just a prompt, but a sequence of prompts with defined roles, checkpoints, and criteria that work together like a pipeline.

### What is an Agent Prompt Flow?

- **Official Definition:** An agent prompt flow is a **structured, reusable sequence of prompts** that guides an AI agent through a task from start to finish — combining role definition, task execution, self-reflection, feedback evaluation, and output formatting into a single orchestrated workflow.
- **In Simple Words:** Instead of asking the AI one question at a time and hoping for the best, you design a **recipe** for the agent. Each step in the recipe has a purpose, and the agent follows the steps in order until it produces a result that meets your standard.
- **Real-Life Example:** Think of a **hospital discharge process**. When a patient is ready to leave, they do not just walk out. There is a checklist: the doctor reviews the final diagnosis, the nurse confirms medications, the billing team processes insurance, and the patient signs a discharge form. Each person has a defined role and a quality checkpoint. An agent prompt flow gives AI the same kind of structured, accountable process.

### The Four Components of an Agent Prompt Flow

Every reliable agent prompt flow is built from four components:

![The four parts of an agent prompt flow — role, task, reflection or feedback criteria, and output format](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session11/session11-agent-prompt-flow-four-components.png)

1. **Role (System Instruction)** — Defines *who* the agent is and *what its core job is*. This sets the agent's default behaviour, tone, and constraints for the entire interaction. Think of this as the job description.

2. **Task** — Defines *what the agent must do* in this specific instance. This is the concrete, specific assignment given within the role's scope.

3. **Reflection + Feedback Criteria** — Defines *how the agent checks its own work*. These are the measurable quality criteria the agent uses to evaluate each output before accepting it.

4. **Output Format** — Defines *what the final answer should look like*. This controls structure, length, and presentation so the output is always clean and predictable.

### Full Example — A Complete Agent Prompt Flow

**Scenario:** Build an agent that explains a complex concept in simple terms, verifies the explanation is genuinely simple, and rewrites it if not.

---

**Without a Structured Flow — Bad Response:**

```
Prompt: Explain machine learning simply.

AI Response:
Machine learning is a subset of artificial intelligence that enables
systems to learn from data, identify patterns, and make decisions
with minimal human intervention using algorithms and statistical models.
```

**Why this response fails:**
- This is a textbook definition that a beginner cannot decode.
- Words like "subset," "statistical models," and "algorithms" are barriers, not bridges.
- There is no analogy, no example, no connection to everyday life.
- A person who needed a simple explanation is now more confused.

---

**With a Complete Agent Prompt Flow — Good Response:**

```
[ROLE]
You are a teacher who specialises in explaining technical topics to
people with zero technical background. You never use jargon. Every
concept you explain gets a relatable real-life analogy.

[TASK]
Explain the concept of machine learning to a 40-year-old shopkeeper
who has completed schooling but never studied computers.

[REFLECTION + FEEDBACK CRITERIA]
After writing your explanation, evaluate it:
- Does it avoid all technical jargon? (Yes/No)
- Does it use at least one real-life analogy a shopkeeper can relate to? (Yes/No)
- Would someone with no computer education understand it in one read? (Yes/No)

If any answer is No, rewrite and re-evaluate until all are Yes.

[OUTPUT FORMAT]
Present the final explanation as 3–4 short paragraphs. Each paragraph
should be 2–3 sentences. End with one sentence summarising the big idea.

---

AI Response (after reflection):
Have you ever noticed how, after buying rice from the same supplier for
years, you just know when the quality is off — even before checking
the weight? You have learned from experience. Machine learning teaches
computers to do the same thing — learn from experience instead of
following fixed rules.

Imagine you are training a new helper in your shop. The first day,
they make mistakes. But every day, you correct them, and they get
better. Machine learning is that exact process, but for computers —
they are shown thousands of examples, they make mistakes, they are
corrected, and they gradually get better at the task.

This is how your phone knows your face to unlock, how Google knows
what you are about to type, and how Netflix knows what show you will
like next. None of those features were programmed with specific rules.
They were all learned from patterns in data.

In short: machine learning is how we teach computers to learn from
experience, just like how you learned your trade.
```

**Why this response works:**
- The shopkeeper analogy ("rice quality," "training a new helper") makes the concept **personally relatable**.
- Real examples from daily life (phone face unlock, Google autocomplete, Netflix) prove that machine learning is already part of the shopkeeper's world.
- The language is completely jargon-free — not a single technical word.
- The final summary sentence gives the reader a clean, memorable takeaway.
- The reflection criteria caught what a vague prompt would have missed.

### Why the Four-Component Structure Matters

- **Without the Role**, the AI picks a default tone — often academic or formal, which is wrong for a beginner audience.
- **Without the Task** being specific, the AI picks the broadest possible interpretation and produces a generic answer.
- **Without Reflection Criteria**, even a good initial answer may have subtle problems that go unnoticed.
- **Without the Output Format**, the AI chooses its own structure — which may be inconsistent across different runs of the same agent.

Each component is a guardrail. Together, they turn a single prompt into a **predictable, reliable system**.

---

## Comparing Prompting Strategies

### The Three Strategies Side by Side

By now you have seen three distinct approaches. Each one is a tool — and like any tool, it works well in the right situation and poorly in the wrong one.

| Strategy | Core Behaviour | Best Suited For | Where It Falls Short |
|---|---|---|---|
| **One-Shot Prompting** | Single prompt → single response. No follow-up, no review. | Simple factual queries, quick lookups, tasks with one obvious correct answer. | Falls apart on complex, multi-part, or nuanced tasks. |
| **Iterative Prompting** | Multiple rounds of human-guided refinement. You review each output and direct the next step. | Creative work, long documents, personalised content where your preferences matter. | Requires you to be actively involved in every round. |
| **Reflection-Based Prompting** | The AI evaluates and revises its own output automatically using built-in criteria. | Autonomous agents, quality-sensitive tasks, high-stakes outputs where errors are costly. | Slightly longer processing; requires well-defined criteria upfront. |

![One-shot, iterative, and reflection-based prompting — when each strategy fits and how autonomous the process is](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session11/session11-three-prompting-strategies.png)

### Seeing the Same Task Handled Three Ways

**Task:** Write a short health tip for a senior citizen about managing high blood pressure.

---

**One-Shot Prompting:**

```
Prompt: Write a short health tip for a senior citizen about managing
high blood pressure.

Response: Reduce salt intake and exercise regularly to manage
high blood pressure. Consult your doctor for medication if needed.
```

Result: Passable for a simple tip, but generic. Fine if you just need a quick filler line, but not good enough if this is medical guidance a real senior will read.

---

**Iterative Prompting (3 rounds):**

```
Round 1 Prompt: Write a health tip for a senior about high blood pressure.
Round 1 Response: Reduce salt intake, exercise daily, and take prescribed medicines on time.

Round 2 Prompt: Add specific foods they should avoid and one they should eat more of.
Round 2 Response: Avoid pickles, papads, processed foods, and canned soups — these are
high in hidden sodium. Increase bananas and leafy greens, which are rich in potassium
and help lower blood pressure naturally.

Round 3 Prompt: Now add a practical morning habit they can start tomorrow.
Round 3 Response: Start your morning with a 20-minute walk — not fast, just steady.
Walking reduces systolic blood pressure by 4–9 mmHg over time, which is comparable
to some medications. Pick a fixed time so it becomes a habit, not a decision.
```

Result: Much richer and more useful. Each round added a specific layer — foods to avoid, foods to eat, and a daily habit. But this required three active rounds of human guidance.

---

**Reflection-Based Prompting (agent evaluates itself):**

```
Prompt: Write a health tip for a senior citizen about managing high blood pressure.

After writing, check:
- Does it include at least one specific food to avoid? (Yes/No)
- Does it include a specific daily habit they can start? (Yes/No)
- Is it written simply enough for a 70-year-old with no medical background? (Yes/No)
- Is it under 100 words? (Yes/No)

Rewrite until all four criteria are satisfied.

Final Response:
To manage blood pressure, avoid high-salt foods like pickles, papads, and processed
snacks — they quietly raise your numbers. Eat a banana or some spinach daily, as
potassium helps balance sodium.

Every morning, take a 20-minute slow walk. It is one of the most effective habits
for controlling blood pressure, and it costs nothing.

Take your medication at the same time daily — consistency matters. And check your
blood pressure at home once a week so you spot changes early. [98 words]
```

Result: Comparable to the iterative result, but produced in a single prompt — no back-and-forth needed. The agent caught its own gaps and fixed them.

### The Golden Rule

- **Use one-shot** when the task is simple and the answer has one obvious correct form.
- **Use iterative** when you want creative control and your own preferences need to shape the output across multiple rounds.
- **Use reflection-based** when you are building an agent that will run without you present, and the quality of output matters every single time.

As you build more complex AI systems, you will find yourself **combining all three** — one-shot for simple sub-tasks within a larger flow, iterative when a human is in the loop, and reflection-based for autonomous quality control.

---

## Practicing Prompt Refinement

### The Weak-to-Strong Prompt Method

The fastest way to improve your instinct for prompt design is to take a weak prompt and deliberately strengthen it — step by step. This exercise makes visible exactly what information the AI needs and what happens when it lacks it.

Think of it like teaching a new team member. A bad briefing leads to bad work — not because the person is incapable, but because they did not have the information they needed. A strong brief produces strong work. Prompt refinement is the skill of giving the AI a strong brief every time.

### Full Exercise — Refining a Weak Prompt

**Starting Point — Weak Prompt:**

```
Prompt: Tell me about online safety.

AI Response (to the weak prompt):
Online safety is important in today's digital world. People should
protect their passwords and be careful about what they share online.
Cybercrime is increasing every year.
```

**What is wrong:**
- Audience is undefined — "people" could be children, adults, or the elderly.
- No specific guidance — what should they actually *do*?
- No structure — this is three loose sentences, not useful information.

---

**Refinement Round 1 — Add Role and Audience:**

```
Prompt: You are a school teacher. Explain 3 important online safety
rules to Class 8 students (age 13–14) in simple language.

AI Response:
1. Never share your passwords: Not even with your best friend.
   Your password is like your house key — giving it to someone else
   means they can enter without your permission.

2. Think before you post: Anything you put online — a photo, a comment,
   a video — can be seen by thousands of people and cannot be fully deleted.
   Ask yourself: "Would I be okay if my parents or teacher saw this?"

3. Don't talk to strangers online: Someone who says they are 14 might
   be a 45-year-old adult. Never agree to meet anyone you only know online.
```

**Improvement:** Much better — specific rules, good analogies, right tone. But there are only 3 points and no practical scenario the students can apply.

---

**Refinement Round 2 — Add a Scenario-Based Check:**

```
Prompt: Good. Now add a 4th rule about recognising phishing messages.
Give a realistic example of a phishing message a Class 8 student might
actually receive, and explain what the red flags are.

AI Response (adds):
4. Spot fake messages (phishing): Scammers send fake messages that look
   real to trick you into giving away personal information.

   Example of a real phishing message a student might get on WhatsApp:
   "Congratulations! You have won a ₹5,000 Flipkart voucher. Click this
   link and enter your name, school, and phone number to claim it."

   Red flags in this message:
   - You did not enter any contest — so how did you "win"?
   - It asks for personal information (name, school, phone).
   - The link is not a real Flipkart address.
   - Real companies do not give prizes via WhatsApp messages.
   
   Rule: If a message gives you a feeling of "this is too good to be
   true" — it almost always is.
```

**Improvement:** Now the student has a real-world example they can immediately apply. The red flags list makes the teaching concrete and practical.

---

**Refinement Round 3 — Add a Reflection Step and Format Constraint:**

```
Prompt: Review everything above. Check:
- Is every rule explained in under 3 sentences? (Yes/No)
- Does each rule have either an analogy or a real example? (Yes/No)
- Is any language too technical for a 13-year-old? (Yes/No)

Fix any issue and present the final four rules in a clean numbered list.
```

This third step turns your human-reviewed output into a **self-correcting document** — the AI checks its own clarity before you get the final version.

**The key lesson:** Each refinement round targeted one specific gap. Round 1 added role and audience. Round 2 added a concrete scenario. Round 3 added quality control and clean formatting. At no point did you try to fix everything in one prompt — and that is exactly the discipline that makes iterative prompting powerful.

---

## Evaluating Response Quality

### The Skill That Makes Everything Else Work

Reflection, self-correction, iterative prompting, and feedback loops — all of these depend on one underlying skill: **the ability to judge whether an AI response is actually good**. If you cannot spot a weak response, you cannot guide the AI to improve it.

This section trains that judgment. By the end, you will be able to look at any AI response and immediately identify what is wrong and what to do about it.

### The Five Types of Bad AI Responses

---

**Type 1: Hallucination — The Confident Lie**

The AI states something that is completely false, but with full confidence and detail, as if it were fact.

```
Bad Response Example:

User: Who invented the Python programming language?

AI: Python was invented by James Gosling in 1991 as a general-purpose
programming language designed for ease of use.

(Note: James Gosling invented Java, not Python. Python was created by
Guido van Rossum. This is a hallucination — wrong person, but stated
confidently.)
```

Hallucinations are dangerous because they **sound convincing**. The answer has a name, a year, and a purpose — all the markers of a real fact. The only problem is the name is wrong.

**How to catch it:** If the AI mentions specific names, dates, statistics, or citations — verify them independently. Never use AI-generated facts directly in anything important without a second-source check.

---

**Type 2: Vagueness — The Non-Answer**

The AI gives a response that is technically true but so general it gives you nothing actionable.

```
Bad Response Example:

User: How do I improve my writing skills?

AI: To improve your writing, practice regularly, read good books,
and get feedback from others.
```

Every word of this is true. And yet a student reading this has learned nothing. *How* do you practice? *What* kind of books? *Who* gives feedback and *how* do you apply it?

```
Good Response (same question, after iterative refinement):

To improve your writing:

1. Write every day for 15 minutes — set a timer, pick a topic (your day,
   a news story, a random idea), and write without stopping to edit.
   The habit of writing is more important than the quality at first.

2. Read one well-written article or story per week and analyse a paragraph
   you liked — why does it work? What words did the writer choose?
   Copy their structure with different content to learn the technique.

3. Share one piece of writing per week with one person whose opinion you
   trust. Ask one specific question: "Was there any part that confused you?"
   That specific question gets you useful feedback instead of vague praise.
```

The second version is **actionable** — the student can start tomorrow with "write for 15 minutes."

---

**Type 3: Incomplete Coverage — The Half-Answer**

The AI answers part of the question but quietly skips the parts it finds harder or less interesting.

```
Bad Response Example:

User: What are the pros and cons of using social media for a small business?

AI: Social media helps small businesses reach more customers, build
brand awareness, and engage with their audience. It is a cost-effective
marketing tool.
```

This response covers only the pros. A student asked for *pros and cons* — the cons are completely missing. This is not technically wrong, but it is seriously incomplete. A business owner making a decision based on this response would have an incomplete picture.

**How to catch it:** Re-read the original question and check if the AI addressed every part. If the question has multiple dimensions (pros/cons, advantages/disadvantages, before/after), make sure all are covered.

---

**Type 4: Wrong Format — Disobeying the Instructions**

The AI ignores the format you asked for and presents the answer in its own preferred structure.

```
Bad Response Example:

User: Give me 5 one-sentence tips for staying focused while studying.
Format them as a numbered list.

AI: Staying focused while studying is important for academic success.
You should eliminate distractions, take regular breaks, set clear goals,
stay hydrated, and maintain a consistent study schedule. Creating a
dedicated study space also helps. Overall, focus comes from habit and
environment.
```

The user asked for 5 numbered one-sentence tips. The AI gave a paragraph. The content might be fine, but the format is wrong — which means the output is unusable if you needed a formatted list for a document or slide.

```
Good Response (same question):

1. Turn off phone notifications before you sit down to study.
2. Use the 25-minute Pomodoro method — study for 25 minutes, rest for 5.
3. Write your study goal at the top of the page before you start.
4. Keep a glass of water on your desk — dehydration reduces focus by 20%.
5. Study in the same place every day so your brain associates that space with focus.
```

**How to catch it:** If you specified a format — numbered list, bullet points, table, paragraph — check that the output matches. If it does not, send a correction targeting the format specifically.

---

**Type 5: Logical Contradiction — The Internal Inconsistency**

The AI says two things in the same response that cannot both be true.

```
Bad Response Example:

User: Is coffee good or bad for health?

AI: Coffee is excellent for health. Studies show it reduces the risk of
diabetes and improves cognitive function. However, coffee is bad for health
because it causes anxiety, disrupts sleep, and increases heart rate.
Therefore, coffee is a healthy beverage you should drink regularly.
```

The AI opens by calling coffee "excellent," then lists serious health risks, then concludes you should "drink regularly." The final conclusion contradicts the risks listed in the middle. A reader trying to make a real decision based on this is left more confused than before.

**How to catch it:** Read the conclusion and check if it follows logically from the body of the response. If the AI argued both for and against something, the conclusion should reflect that nuance — not pretend the counterarguments do not exist.

### The EVAL Framework — A Quick Check for Any AI Response

Use these four questions on any AI output before accepting it:

- **E — Exactness:** Did the AI answer *exactly* what was asked — not a related topic, not a simplified version, but the actual question?
- **V — Validity:** Can the specific facts, names, dates, and claims in the response be verified? Or are there things that sound right but feel unverifiable?
- **A — Adequacy:** Is the depth of the response sufficient for the purpose? A one-sentence answer to a complex question is not adequate, even if it is technically correct.
- **L — Layout:** Does the format match what you asked for? Is it readable and well-structured?

If any of these four fail, send a targeted correction prompt. Do not ask the AI to "redo the whole thing" — point to exactly which criterion failed and ask it to fix that specifically.

### How to Send a Good Correction Prompt

The correction prompt you send after identifying a bad response is just as important as the original prompt. Here is the difference between a weak correction and a strong one:

```
Weak Correction:
"This is wrong. Try again."

(Result: The AI produces a different version of roughly the same quality.
 It does not know what was wrong.)

---

Strong Correction:
"Your second paragraph states that Python was invented by James Gosling.
 This is incorrect. Python was created by Guido van Rossum. Please correct
 that specific paragraph and verify any other names or dates in your answer."

(Result: The AI corrects the specific error and re-checks the rest.)
```

Specific corrections produce specific improvements. Vague corrections produce vague improvements.

---

## Optimizing Feedback Loops for Real-World AI Agents

### From Useful to Production-Ready

Everything we have covered in this session works in a single conversation. But the real goal of learning agentic systems is to build agents that work **reliably at scale** — agents that handle hundreds of tasks, maintain consistent quality, and can be reused across different contexts.

For that, your feedback loops need to be designed with care. A poorly designed feedback loop either produces low-quality output (criteria too weak) or runs forever never reaching a conclusion (criteria too strict or poorly defined). A well-designed feedback loop hits the target in 2–3 cycles, every time.

### Four Principles for Efficient Feedback Loops

**Principle 1 — Make Criteria Measurable, Not Subjective**

```
Weak Criteria (subjective, hard to self-evaluate):
"Is the response good quality?"
"Is it clear?"
"Does it sound professional?"

Strong Criteria (measurable, objective):
"Is it under 100 words?" (count is verifiable)
"Does it mention all 3 required points: price, availability, and delivery time?" (checkable)
"Does it use formal language (no contractions, no slang)?" (specific rule)
```

Measurable criteria allow the AI to self-evaluate accurately. Subjective criteria like "is it good?" give the AI nothing concrete to check against.

**Principle 2 — Keep the Loop Small — 2 to 3 Cycles Maximum**

A feedback loop that runs for 7, 8, 9 cycles is a symptom of a poorly designed initial prompt. If the AI cannot meet your criteria in 2–3 cycles, one of two things is true: your criteria are contradictory (impossible to satisfy all at once) or your task instruction is too vague (the AI does not know what to produce). The fix is to go back and redesign the prompt, not to let the loop run indefinitely.

**Principle 3 — Save Working Prompt Flows as Templates**

When you design a prompt flow that consistently produces excellent results, **save it**. Document the role, task, criteria, and output format. The next time you need a similar agent, you only change the TASK — everything else stays the same.

```
Template Example — "Simple Explainer Agent":

[ROLE]: You are an expert teacher who explains technical concepts to
beginners with no prior knowledge.

[TASK]: [INSERT TOPIC HERE]

[REFLECTION CRITERIA]:
- Does it use at least one real-life analogy? (Yes/No)
- Is every sentence understandable to a 10th-grade student? (Yes/No)
- Is it between 100–150 words? (Yes/No)

[LOOP]: Rewrite if any criterion is not met. Re-evaluate after each rewrite.

[OUTPUT]: Final explanation only. No preamble.
```

With this template, you can explain any concept — from machine learning to financial derivatives to photosynthesis — just by changing the TASK line. The rest of the system ensures quality automatically.

**Principle 4 — Layer Complexity Gradually**

Start with the simplest possible loop (one criterion, one revision cycle) and get it working well. Then add a second criterion. Then a third. Building complexity in layers is far more reliable than designing a 10-criterion loop from the start, which is very difficult to debug when something goes wrong.

```
Stage 1 Loop (start here):
"After writing, check: Is it under 100 words? If No, shorten it."

Stage 2 Loop (add after Stage 1 works):
"Also check: Does it include a real-life example? If No, add one."

Stage 3 Loop (add after Stage 2 works):
"Also check: Is it in plain English (no jargon)? If No, simplify."
```

By Stage 3, you have a reliable three-criteria loop — built incrementally, tested at each stage.

### The Complete Reusable Reflection Workflow

Here is the master template that brings every concept in this session together:

```
[ROLE]:
You are a [describe the agent's expertise and persona].

[TASK]:
[Describe the specific task the agent must complete. Be specific about
 the subject, the audience, and the desired outcome.]

[REFLECTION]:
After completing the task, evaluate your response against each criterion:

  Criterion 1: [Specific, measurable check — Yes/No]
  Criterion 2: [Specific, measurable check — Yes/No]
  Criterion 3: [Specific, measurable check — Yes/No]

[LOOP]:
If any criterion is answered No, identify what needs to change,
revise your response, and evaluate again.
Repeat until all criteria are satisfied.
Maximum cycles: 3. If still not passing after 3 cycles, state which
criterion remains unsatisfied and why.

[OUTPUT]:
Present only your final, approved response in [specific format].
Include the self-evaluation result in brackets at the end.
```

**Why each line of this template matters:**

- The **ROLE** line means every response from this agent is grounded in a specific expertise — not a generic chatbot response.
- The **TASK** specificity means the agent knows exactly what is expected — no guessing, no defaulting to the broadest interpretation.
- The **Criterion format** (Yes/No) makes self-evaluation binary and checkable — the AI cannot give a vague "somewhat" answer.
- The **LOOP instruction** gives the agent autonomy to revise without human input — this is the core of autonomous agent behaviour.
- The **Maximum cycles** line prevents infinite loops — a safety measure for production agents.
- The **OUTPUT instruction** ensures the final result is clean, formatted, and includes accountability (the self-evaluation result).

This template is your starting point for every agent you build from this session forward. As you progress in the course, you will extend it with memory, tool use, and multi-agent coordination — but the structure at its core will always be this same framework.

---

## Key Takeaways

- **Self-reflection transforms first drafts into reliable answers** — without a review step, AI agents default to whatever comes first, which is almost never the best version of the response.
- **Self-correction prompts work because they separate thinking from reviewing** — by forcing the AI to generate, critique, and rewrite in three distinct stages, you get a quality of output that a single-instruction prompt cannot match.
- **Iterative prompting gives you creative control** — by refining one specific thing at a time across multiple rounds, you can shape an output exactly to your needs without needing a perfect prompt from the start.
- **Feedback loops are what make agents autonomous** — when criteria are embedded in the prompt, the agent can evaluate and revise its own output without any human present, which is the foundation of every real-world AI agent.
- **In the sessions ahead, we will use this framework as the backbone of multi-step, multi-agent systems** — where one agent's output becomes another agent's input, and each agent in the chain runs its own reflection loop to maintain quality across the entire pipeline.

---

## Important Commands, Libraries, Terminologies Used

| Term / Concept | Meaning |
|---|---|
| **Self-Reflection** | The AI's ability to review, evaluate, and revise its own output before delivering the final answer |
| **Self-Correction Prompt** | A three-stage prompt that instructs the AI to generate, critique, and rewrite its own response |
| **Stage 1 / Generate** | The first stage of a self-correction prompt — produce an initial response |
| **Stage 2 / Critique** | The second stage — the AI reviews its own response and identifies weaknesses |
| **Stage 3 / Rewrite** | The third stage — the AI rewrites using the insights from its own critique |
| **Iterative Prompting** | A technique where multiple targeted follow-up prompts progressively improve an AI's output |
| **One-Shot Prompting** | Sending a single prompt and accepting the first response — suitable only for simple tasks |
| **Feedback Loop** | A cycle where the AI's output is evaluated against criteria and revised until the criteria are met |
| **User Feedback Loop** | A feedback loop driven by direct human input and correction |
| **Internal Feedback Loop** | A feedback loop where the agent self-evaluates using criteria embedded in the prompt |
| **Agent Prompt Flow** | A structured, four-component workflow (Role + Task + Reflection + Output Format) for reliable agent behaviour |
| **Hallucination** | When an AI confidently produces false information — names, dates, statistics — that sounds real |
| **Vagueness** | A response that is technically true but too general to be actionable or useful |
| **Logical Contradiction** | When an AI states two claims in the same response that cannot both be true |
| **EVAL Framework** | Four-point quality check: Exactness, Validity, Adequacy, Layout |
| **Reflection-Based Prompting** | A strategy where the AI is instructed to self-verify and iterate before delivering a final answer |
| **Reusable Workflow / Template** | A saved prompt flow structure where only the task changes and the quality system stays the same |
| **Measurable Criteria** | Specific, objective checks (word count, inclusion of elements) that allow accurate self-evaluation |
| **Chain-of-Thought (recap)** | Reasoning technique from the previous session — the AI thinks step by step before answering |
| **Structured Prompt (recap)** | A prompt organised into role, task, instructions, constraints, and output format |
