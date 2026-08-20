# CrewAI: Roles, Tasks, and First Multi-Agent Crew

## Context of This Session

In the **previous** session you built an **end-to-end n8n pipeline**: ingest a document or message, **summarise** with an LLM, **route** by urgency, and **deliver** to Slack, email, or a sheet. That was a factory line of nodes.

This session staffs an **AI team**. You define **agents** with roles, assign **tasks** with expected outputs, form a **crew**, choose a **process**, then **kick off** one collaborative run and read the **output artifacts**.

**In this session, you will:**

- **Define** agents with **role**, **goal**, and **backstory** inside a bounded campus scenario
- **Assign** tasks with explicit **expected outputs** and **dependencies** between agents
- **Configure** a crew, choose a **process** model, and run a first end-to-end **kickoff**
- **Interpret** which **role** or **task** drove each segment of the result

---

## From a Pipeline of Steps to a Crew of Specialists

n8n is excellent when work looks like stations: intake → process → route → notify. Some work needs **specialists** who think in different ways, then hand a **deliverable** to the next person.

- **Official Definition:** **CrewAI** is a Python framework for building **multi-agent teams**: you define agents, tasks, and a crew, then start one collaborative run.
- **In Simple Words:** It is a way to hire AI teammates, give job titles and work items, and press **start** on the whole team.
- **Real-Life Example:** A **placement cell** brief is not one chat. Someone gathers facts, someone writes the notice, someone checks that no stipend figure was invented.

You already designed a **researcher–writer–editor** pipeline earlier in this module, on paper. Today that design becomes a runnable **crew**.

![Three campus specialists — researcher, writer, and reviewer — forming one CrewAI team ready for kickoff](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session40/session40-01-role-task-crew.png)

**Common doubt:** *“Is this just three n8n LLM nodes in a row?”* — Related idea, different unit. n8n moves **data through apps**. CrewAI moves **work through roles**, with each role keeping a goal and a backstory while it works.

---

## The Role–Task–Crew Model

Connecting sentence: Before any Python, lock the three nouns you will keep repeating: **who** does the work, **what** must be produced, and **which team** you start.

- **Official Definition:** The **role–task–crew model** is CrewAI’s design pattern: **roles** (who), **tasks** (what to deliver), and a **crew** (the team you run as one unit).
- **In Simple Words:** Job titles + work items + the team meeting you actually start.
- **Real-Life Example:** Film shoot: researcher of locations, writer of the script, editor of the cut, and a **crew** that hears “Action!”

| Building block | Job | Campus mapping |
|---|---|---|
| **Agent** | Teammate with role, goal, backstory | Placement researcher / brief writer / reviewer |
| **Task** | Work item with an expected output | Research notes → draft → final brief |
| **Crew** | Agents + tasks you run together | “Placement Brief Crew” |
| **Process** | How work moves between agents | Sequential: research, then write, then review |
| **Tool** | Extra ability given to *some* agents | Researcher may read a facts file; writer may not |
| **Kickoff** | Start the crew run | `crew.kickoff(...)` |
| **Output artifact** | Visible result of a task or of the crew | Markdown files + the final printed result |

**Why this model:** Vague prompts make three chats that copy each other. Clear roles, strict tasks, and one crew start give the next agent a usable packet instead of a messy paste.

### Activity — Fill the three nouns

On paper, write one line each: the **role** that finds facts, the **task** that must come out of writing, and the **crew** name you would print on a folder.

---

## Agents — Role, Goal, and Backstory

Connecting sentence: An agent is not “the AI.” It is one teammate whose identity you write in three fields.

- **Official Definition:** A CrewAI **Agent** is an autonomous teammate powered by an LLM, constrained by a **role**, a **goal**, and a **backstory**, and optionally given **tools**.
- **In Simple Words:** Job title + what success looks like + the experience that shapes tone and limits.
- **Real-Life Example:** “Campus Placement Researcher” is not allowed to invent company names, because the backstory says they work from files, not rumours.

![Agent identity card showing role as job title, goal as the target, and backstory as workplace experience](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session40/session40-02-agent-card.png)

### The three fields (write them as a contract)

| Field | Official meaning | Weak version | Strong version (today) |
|---|---|---|---|
| **Role** | Function inside the crew | “Helper” | Campus Placement Researcher |
| **Goal** | What the agent optimises for | “Be useful” | Extract only file-backed facts for the topic |
| **Backstory** | Style, experience, and **boundaries** | “You are smart” | Placement-cell staff; never invent amounts |

**Logic:** The LLM still *can* hallucinate. Role + goal + backstory do not magically stop that. They **steer** the agent, and your **task expected output** plus a **reviewer** catch leftovers.

**Common error:** Two agents with overlapping roles (“both write nicely and also check facts”). They repeat work or contradict each other. Keep research, writing, and review **narrow**.

**Delegation note:** For this first crew set `allow_delegation=False`. Each agent finishes its own task. Manager-style passing around can wait until you are comfortable reading a simple sequential log.

### Activity — Tighten one backstory

Rewrite this weak backstory in two sentences: *“You are a great writer.”* Add a campus setting and one **thing the writer must not do**.

---

## Tools Per Agent

Connecting sentence: Identity is not enough. Some jobs need a **tool**; others get worse if they have one.

- **Official Definition:** A **tool** is a function an agent may call (search, file read, calculator). **Tools per agent** means you attach tools only to the agents that should use them.
- **In Simple Words:** Give the librarian the catalogue. Do not give the novelist the same catalogue if you want them to write from notes, not wander.
- **Real-Life Example:** Only the placement researcher may open `campus_facts.txt`. The writer must use research notes. The reviewer compares draft vs notes — no extra file hunting.

**Need:** If every agent can “look things up,” the writer may skip the researcher and invent a parallel story. That breaks the handoff you designed.

Today the researcher gets **one** custom tool: **Campus Facts Lookup**. It reads a **local** text file. No live web search, no extra API key. The scenario stays **bounded**, so you can judge quality.

**Common doubt:** *“Should I add Google search on day one?”* — Not for this lab. Live search makes the first kickoff noisy and expensive. A facts file is the training-wheels version of a knowledge tool.

---

## Tasks — Expected Outputs and Dependencies

Connecting sentence: Agents are people on the org chart. **Tasks** are the tickets they must close.

- **Official Definition:** A CrewAI **Task** is a work item with a **description**, an **expected output**, an assigned **agent**, optional **context** (dependencies), and optional **output_file**.
- **In Simple Words:** “Do this job, deliver it in this shape, wait for these earlier tickets, and save a copy.”
- **Real-Life Example:** “Write a one-page stipend brief in markdown with four headings, using only the research bullets.”

![Sequential handoff of folders: research notes, then draft brief, then final brief](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session40/session40-03-task-handoffs.png)

### Expected output (the contract the next agent reads)

A description without an expected output is a wish. A good expected output names **format**, **length**, and **forbidden extras**.

| Task | Expected output (today) | Why it is strict |
|---|---|---|
| Research | 6–10 markdown bullets + an `UNCERTAIN` list | Writer must not receive a novel |
| Write | Four sections, no new facts | Reviewer can diff against notes |
| Review | Final brief + a quality table | **You** can see who drove each segment |

### Dependencies (`context`)

- **Official Definition:** A task **dependency** in CrewAI is the `context=[...]` list of earlier `Task` objects whose outputs are fed into this task.
- **In Simple Words:** “Do not start writing until research notes exist.”
- **Real-Life Example:** The editor of a college magazine does not layout a page before the article file arrives.

In a **sequential** process, task **order** in the `tasks=[...]` list is the run order. `context` is still worth writing: it tells the later agent **which** earlier outputs to use, not only “whatever happened last.”

**Common error:** Writer task with no `context`. The writer may ignore research and produce a generic essay. Always wire `context=[research_task]` (and for review, both prior tasks).

### Activity — Write one expected output

For a task named “draft brief,” write two lines: the **shape** (headings), and one sentence the writer is **forbidden** to add.

---

## Crew, Process, and Kickoff

Connecting sentence: Agents and tasks are ingredients. The **crew** is the dish you actually cook.

- **Official Definition:** A **Crew** groups agents and tasks and runs them under a **process**. **Kickoff** (`crew.kickoff`) starts that run and returns a **CrewOutput**.
- **In Simple Words:** Assemble the team, choose how they work, press start, collect the packet of results.
- **Real-Life Example:** “Action!” on a film set — cameras, script, and editor now work under one shoot plan.

### Process models (choose one for the first run)

| Process | Official meaning | When to use |
|---|---|---|
| **Sequential** (`Process.sequential`) | Tasks run in list order; later tasks see earlier outputs | First crew, clear pipeline, easy logs |
| **Hierarchical** (`Process.hierarchical`) | A **manager** LLM assigns and checks work | Later, when you need a lead to delegate |

**Today’s choice:** **sequential**. It matches researcher → writer → reviewer. Hierarchical needs a manager model and is harder to read on the first day.

```text
kickoff({topic})
  → Researcher + Campus Facts Lookup  → 01_research_notes.md
  → Writer (context = research)       → 02_draft_brief.md
  → Reviewer (context = both)         → 03_final_brief.md
  → CrewOutput (raw ≈ last task)
```

**Kickoff inputs:** Placeholders like `{topic}` in task text are filled by `crew.kickoff(inputs={"topic": "..."})`. Same idea as filling a form before an n8n run.

**Output artifacts:** After kickoff you inspect (1) files from `output_file`, (2) `result.raw` (usually the **last** task), (3) `result.tasks_output` (each task’s text). Verbose logs show which agent is speaking.

**Common error:** Printing only `result` and declaring success. The weak paragraph may live in **research**, not in the final page. Open all three artifacts.

### Activity — Name the process

Write one sentence: why **sequential** fits this stipend brief, and one situation where you would wait for a **hierarchical** manager instead.

---

## Lab Setup

Connecting sentence: The crew will call an LLM, so the key lives in `.env`, not in the Python file.

Create a folder `placement_brief_crew`. Inside it, create `.env` (do **not** commit this file):

```text
OPENAI_API_KEY=your_openai_key_here
```

Install:

```bash
pip install crewai python-dotenv
```

Use the same OpenAI key idea you used as an n8n credential. CrewAI reads `OPENAI_API_KEY` from the environment after `load_dotenv()`.

If your classroom uses another provider, you can later swap the `LLM(...)` line. Keep **one** working key for this first kickoff.

---

## Bounded Scenario — Campus Placement Brief

Connecting sentence: A first crew needs a **fence**. The fence is a short facts file. Nothing outside that file is “known.”

Save this as `campus_facts.txt` next to your Python script:

```text
Campus: Greenfield Institute of Technology, Pune
Placement cell lead: Prof. Meera Kulkarni
Issue: June internship stipends delayed for 14 students (2026 summer cohort)
Companies named in file: Nimbus Analytics; Riverbank Retail
Evidence date: email dated 28 July
Stipend range on file: Rs 8,000 to Rs 15,000 per month
Channel: Campus Ops Inbox form
Already done: one reminder email to company HR on 4 August
Not done: no trainer Slack alert yet
Policy: delays above 21 days are high urgency
Do not invent: other company names, per-student unpaid totals, legal threats
```

**Goal of the run:** Produce a faculty-facing **placement brief** on **internship stipend delays**, using only this file.

This continues the **Campus Ops Inbox** story: n8n could route a student complaint. The crew now **researches, writes, and reviews** a staff brief from known facts.

---

## Full Crew Script

Connecting sentence: The facts file is the fence. The script below is the full team: three agents, three tasks, one sequential kickoff.

Save as `placement_brief_crew.py` in the same folder as `campus_facts.txt` and `.env`.

```python
# placement_brief_crew.py — first sequential CrewAI crew
from pathlib import Path  # safe path to campus_facts.txt
from dotenv import load_dotenv  # load .env into environment
from crewai import Agent, Task, Crew, Process, LLM  # CrewAI building blocks
from crewai.tools import tool  # turn a Python function into an agent tool

load_dotenv()  # read OPENAI_API_KEY from .env

FACTS_PATH = Path(__file__).parent / "campus_facts.txt"  # facts file beside this script

llm = LLM(model="openai/gpt-4o-mini", temperature=0.2)  # shared model; low temperature for facts


@tool("Campus Facts Lookup")  # register this function as a named agent tool
def campus_facts_lookup(query: str) -> str:  # query is what the researcher asks
    """Read the local campus facts file. Use this instead of inventing names or numbers."""  # agent-facing tool description
    text = FACTS_PATH.read_text(encoding="utf-8")  # load bounded knowledge
    return f"Query: {query}\n\nKnown campus facts:\n{text}"  # give the agent the file text


researcher = Agent(  # specialist who only gathers file-backed facts
    role="Campus Placement Researcher",  # job title
    goal="Extract only evidence-backed facts from the campus facts file for the topic.",  # success
    backstory="You work in a Pune placement cell. You never invent companies, amounts, or dates.",  # boundary
    llm=llm,  # model for this agent
    tools=[campus_facts_lookup],  # only the researcher may read the file
    verbose=True,  # print thinking in the terminal
    allow_delegation=False,  # do not pass this task to someone else
)  # end researcher

writer = Agent(  # specialist who drafts from notes, not from the facts file
    role="Placement Brief Writer",  # job title
    goal="Turn research notes into a clear one-page brief without adding new facts.",  # success
    backstory="You write notices faculty can scan in two minutes. Simple Indian English only.",  # style
    llm=llm,  # same model, different role
    tools=[],  # no facts-file access; must use research notes
    verbose=True,  # observable run
    allow_delegation=False,  # stay in the writer seat
)  # end writer

editor = Agent(  # specialist who labels quality; does not invent facts
    role="Quality Reviewer",  # job title
    goal="Check the draft against research notes and label who drove each segment.",  # success
    backstory="You flag claims that are not in the notes. You do not invent replacement facts.",  # boundary
    llm=llm,  # same model, review stance
    tools=[],  # compare texts only
    verbose=True,  # observable run
    allow_delegation=False,  # stay in the reviewer seat
)  # end editor

research_task = Task(  # ticket 1: notes the writer can trust
    description=(  # what to do; {topic} filled at kickoff
        "Use Campus Facts Lookup. Collect facts about {topic}. "
        "List only what the file supports. Mark gaps as UNCERTAIN."
    ),  # end research description
    expected_output=(  # contract for the writer
        "Markdown list of 6 to 10 bullets. Each bullet is one fact plus a short source hint. "
        "End with a short UNCERTAIN list."
    ),  # end research expected output
    agent=researcher,  # who owns this ticket
    output_file="output/01_research_notes.md",  # artifact on disk
)  # end research_task

write_task = Task(  # ticket 2: four-section brief, no new facts
    description=(  # writing ticket
        "Using only the research notes, write a one-page placement brief on {topic}. "
        "Sections: Title, What happened, Who is affected, Recommended next step. "
        "Do not add companies, amounts, or dates that are not in the notes."
    ),  # end write description
    expected_output="A markdown brief with those four sections and no new facts.",  # contract for the reviewer
    agent=writer,  # who owns this ticket
    context=[research_task],  # dependency: wait for research
    output_file="output/02_draft_brief.md",  # artifact on disk
)  # end write_task

review_task = Task(  # ticket 3: final brief plus who-drove-what table
    description=(  # review ticket
        "Compare the draft with the research notes. Keep good sentences. "
        "Label each paragraph FROM_RESEARCH, FROM_WRITER_STYLE, or FLAGGED. "
        "Return the final brief plus a short quality table."
    ),  # end review description
    expected_output=(  # contract for you, the human reader
        "Final markdown brief, then a table with columns: Segment | Driven by | Notes."
    ),  # end review expected output
    agent=editor,  # who owns this ticket
    context=[research_task, write_task],  # needs both earlier artifacts
    output_file="output/03_final_brief.md",  # artifact on disk
)  # end review_task

crew = Crew(  # one team: three agents, three tasks, sequential process
    agents=[researcher, writer, editor],  # the team
    tasks=[research_task, write_task, review_task],  # run order for sequential process
    process=Process.sequential,  # research, then write, then review
    verbose=True,  # print crew-level logs
)  # end crew


if __name__ == "__main__":  # run only when this file is executed directly
    result = crew.kickoff(inputs={"topic": "internship stipend delays"})  # start the run
    print("=== FINAL CREW OUTPUT (usually last task) ===")  # banner
    print(result)  # CrewOutput; often the reviewer’s final brief
    print("=== PER-TASK ARTIFACTS ===")  # banner
    for item in result.tasks_output:  # one object per task
        print("---")  # separator
        print("Agent:", item.agent)  # which role produced this segment
        print((item.raw or "")[:500])  # first 500 characters of that task
```

**How the code works:**

- `load_dotenv()` + `LLM(...)` give every agent the same model, with a low temperature so facts stay stable.
- `@tool` wraps a file read. Only `researcher` receives `tools=[campus_facts_lookup]`. Writer and editor get `tools=[]`.
- Three `Agent` objects encode **role / goal / backstory**. `allow_delegation=False` keeps each ticket with its owner.
- Three `Task` objects encode **description**, **expected_output**, **agent**, **context**, and **output_file**.
- `context` is the dependency wire: write waits on research; review waits on both.
- `Crew` uses `Process.sequential`, so the `tasks` list order is the run order.
- `kickoff(inputs={"topic": ...})` fills `{topic}` in the descriptions. `result.tasks_output` is how you map **who produced what**.

Run:

```bash
python placement_brief_crew.py
```

Wait for all three tasks. Then open the `output/` folder.

![Kickoff starts the crew; research notes, draft brief, and final brief appear as inspectable artifacts](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module4/session40/session40-04-kickoff-artifacts.png)

**What you should see:** verbose logs naming **Campus Placement Researcher**, then **Placement Brief Writer**, then **Quality Reviewer**. After that, three markdown files appear under `output/`.

### If kickoff fails

| Symptom | Likely cause | Fix |
|---|---|---|
| Auth / API key error | `.env` missing or not loaded | Confirm `OPENAI_API_KEY` and that `load_dotenv()` runs first |
| File not found | `campus_facts.txt` not beside the script | Same folder as `placement_brief_crew.py` |
| Model error | Account cannot use `gpt-4o-mini` | Ask for the class model name; change only the `LLM(...)` line |
| Empty research | Tool not called | Check `tools=[campus_facts_lookup]` is only on the researcher |
| Writer invents a company | Weak `context` or expected output | Confirm `context=[research_task]` and re-run once |

Do not add a fourth agent to “fix” a missing key. Fix setup, then kick off again.

---

## Interpret Output Quality — Who Drove What

Connecting sentence: A pretty final page can still hide a bad research step. Read the crew like a team lead, not like a magic box.

- **Official Definition:** **Output artifacts** are the saved or returned results of tasks and of the crew (`output_file` contents, `result.raw`, `result.tasks_output`).
- **In Simple Words:** The homework copies each teammate submitted, plus the stapled final version.
- **Real-Life Example:** If the final brief mentions “Infosys,” but `campus_facts.txt` does not, the **writer** (or a sloppy **reviewer**) drove that segment — not the facts file.

### Reading order after the first kickoff

1. Open `output/01_research_notes.md`. Count bullets. Is every company from the file? Is there an `UNCERTAIN` list?
2. Open `output/02_draft_brief.md`. Do the four headings exist? Any new number?
3. Open `output/03_final_brief.md`. Did the reviewer **flag** invented claims or quietly keep them?
4. Skim the terminal: which agent name appears before each block?

A **healthy** research bullet looks like: `Nimbus Analytics is named in the facts file (email dated 28 July).` A **weak** bullet looks like: `Several IT firms in Pune are involved.` The second one is not in the file. The writer should not turn that fog into a confident paragraph.

### Quality table (fill this in your notebook)

| Segment you noticed | Likely driver | Evidence |
|---|---|---|
| List of two companies | Researcher task | Matches the facts file |
| Four-section layout | Writer task | Headings requested in expected output |
| Friendly one-line opener | Writer style | Not in the facts file, but not a new “fact” |
| A third company name | Writer or weak review | **Not** in `campus_facts.txt` |
| “High urgency” | Researcher applying policy | File states the 21-day rule; June → August is longer than 21 days |
| Slack not sent | Researcher | File says “not done” |

**Logic:** Style can come from the **writer**. Facts must trace to **research**, and flags must come from the **reviewer**. If you cannot point to a role, tighten the expected outputs.

**Common errors:**

- Calling the whole run “the AI was wrong” — name the **task file**.
- Only reading `result.raw` — that is usually the **last** task.
- Rewriting all three backstories at once — change **one** field, kick off again, compare artifacts.

### Activity — Map three segments

After your run, copy three short phrases from the final brief. For each, write **researcher**, **writer**, or **reviewer** (or **flagged**). One phrase should be a fact from the file.

### Activity — One failure mode

Delete the two company names from `campus_facts.txt`, save, and kick off again. Predict: the research `UNCERTAIN` list should grow; the writer should **not** invent replacements. If it still names Nimbus, the **writer** ignored context — tighten the write-task expected output, not the reviewer first.

---

## What “Good” Looks Like on This First Crew

Connecting sentence: You are not grading literature. You are grading **contracts**.

A successful first run has all of the following:

- Terminal shows three agents in order (researcher, then writer, then reviewer)
- Three files exist under `output/`
- Research bullets stay inside the facts file
- Draft uses the four required sections
- Final page includes a **Driven by** table you can actually use
- No extra company names

If the prose is a bit stiff, that is acceptable. If a **fact** appears from nowhere, that is a crew-design bug.

**Upcoming** work can add richer tools, a **hierarchical** process with a manager, and a small evaluation checklist you iterate against. This session’s job is a **readable first crew**, not a production department.

---

## Key Takeaways

- **CrewAI** turns a multi-agent idea into a runnable **role–task–crew** unit: agents (who), tasks (what), crew (the team you start).
- Write **role**, **goal**, and **backstory** as a contract, then give **tools only** to the agents that should have them.
- Tasks need **expected outputs** and **dependencies** (`context`); sequential **process** plus **kickoff** produces inspectable **output artifacts**.
- Judge quality by mapping each segment to a **role or task**, not by a single thumbs-up on the final page.

These habits — specialist roles, explicit deliverables, and reading artifacts — are what you will reuse when crews grow tools, a manager process, and stricter evaluation in **upcoming** sessions.

---

## Important Commands, Libraries, and Terminologies Used

| Term / Command | Type | Meaning |
|---|---|---|
| **CrewAI** | Framework | Python library for multi-agent crews |
| **Role–task–crew model** | Pattern | Who does work, what is delivered, which team you run |
| **Agent** | Class | Teammate with role, goal, backstory, optional tools |
| **Role** | Field | Job title inside the crew |
| **Goal** | Field | What that agent optimises for |
| **Backstory** | Field | Experience and boundaries that shape behaviour |
| **Task** | Class | Work item with description and expected output |
| **Expected output** | Field | Required shape of the task result |
| **context** | Field | Earlier tasks this task depends on |
| **Crew** | Class | Agents + tasks run as one unit |
| **Process** | Enum | How work moves (`sequential` or `hierarchical`) |
| **Process.sequential** | Process | Tasks run in list order |
| **Process.hierarchical** | Process | Manager coordinates assignment and checks |
| **Tools per agent** | Habit | Attach tools only where they belong |
| **@tool** | Decorator | Turns a function into an agent tool |
| **Kickoff** | Method | `crew.kickoff(inputs=...)` starts the run |
| **CrewOutput** | Result | Return value of kickoff (`raw`, `tasks_output`) |
| **Output artifact** | Result | `output_file` plus per-task text you inspect |
| **output_file** | Field | Path where a task writes its result |
| **tasks_output** | Attribute | List of per-task results after kickoff |
| **verbose** | Flag | Print agent/crew logs during the run |
| **allow_delegation** | Flag | Whether an agent may pass work to another |
| **LLM** | Class | Model wrapper (`openai/gpt-4o-mini` here) |
| `pip install crewai python-dotenv` | Command | Install CrewAI and `.env` loader |
| `load_dotenv()` | Call | Load `OPENAI_API_KEY` from `.env` |
| `python placement_brief_crew.py` | Command | Run the first crew |
| **Bounded scenario** | Habit | Limit knowledge (here: `campus_facts.txt`) |
