# lecture40.py — CrewAI: Roles, Tasks, and First Multi-Agent Crew (Session 40)
#
# Same "Campus Placement Brief" crew as the lecture notes: a Researcher, a Writer, and a
# Reviewer run sequentially — research notes -> draft brief -> final brief with a quality table.
#
# ONE CHANGE from the notes: the shared LLM is Gemini instead of OpenAI (Groq is not supported
# in this environment). Gemini hosts Google's models behind a free-tier-friendly API — handy for
# a live classroom demo where you do not want to wait on rate limits or pay for OpenAI credits.
#
# Setup:
#   1. pip install crewai python-dotenv
#   2. Create a .env file next to this script:
#        GEMINI_API_KEY=your_gemini_key_here
#      (get a free key at https://aistudio.google.com/apikey)
#   3. Make sure campus_facts.txt sits in the same folder as this script.
#   4. python3 lecture40.py
#
# Everything else — role/goal/backstory, the Campus Facts Lookup tool, expected outputs,
# context dependencies, Process.sequential, and kickoff — is exactly the design taught in class.

from pathlib import Path  # safe path to campus_facts.txt
from dotenv import load_dotenv  # load .env into environment
from crewai import Agent, Task, Crew, Process, LLM  # CrewAI building blocks
from crewai.tools import tool  # turn a Python function into an agent tool

load_dotenv()  # read GEMINI_API_KEY from .env

FACTS_PATH = Path(__file__).parent / "campus_facts.txt"  # facts file beside this script

# Gemini model id format for CrewAI/LiteLLM is "gemini/<model-name>".
# gemini-2.0-flash was retired by Google; gemini-3.6-flash is the current fast/free-tier-friendly default.
llm = LLM(model="gemini/gemini-3.6-flash", temperature=0.2)  # shared model; low temperature for facts


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
    print(result)  # CrewOutput; often the reviewer's final brief
    print("=== PER-TASK ARTIFACTS ===")  # banner
    for item in result.tasks_output:  # one object per task
        print("---")  # separator
        print("Agent:", item.agent)  # which role produced this segment
        print((item.raw or "")[:500])  # first 500 characters of that task
