# lecture36.py — A TEAM OF HELPERS working together (Session 36)
#
# Big idea of this session, in one line:
#   Instead of ONE helper doing everything, we use a small TEAM where each helper has one job,
#   and they pass the work along like a relay race.
#
# Run it with plain Python — nothing to install, no internet, no accounts:
#
#   python3 lecture36.py
#
# The story you will see printed:
#   1. You press a "START" button (this is called a TRIGGER).
#   2. Three helpers do their jobs in order (a RESEARCHER, a WRITER, an EDITOR).
#   3. When they finish, the system sends YOU a "job done" message (this is called a WEBHOOK).
#
# That's it. Read the comments top to bottom — it reads like a short story.


# ===========================================================================
# THE THREE HELPERS  (each one has a single, simple job)
# ===========================================================================
# Think of a small content team:
#   - the RESEARCHER collects the main points
#   - the WRITER turns those points into sentences
#   - the EDITOR cleans it up so it reads nicely
# Each helper takes what the previous one made and improves it. That is the whole "team" idea.

def researcher(topic):
    """Helper 1 — collect a few key points about the topic."""
    points = [
        "Split a big job into small jobs so it is easier",
        "Let each helper do the one thing it is good at",
        "Send a 'done' message at the end so nobody has to keep checking",
    ]
    print("   Researcher: I found 3 key points.")
    return points


def writer(points):
    """Helper 2 — turn the points into simple sentences (a first draft)."""
    draft = ["We should " + point.lower() + "." for point in points]
    print("   Writer:     I turned those points into 3 sentences.")
    return draft


def editor(draft):
    """Helper 3 — tidy up the draft into clean final notes."""
    final_notes = [sentence.strip().capitalize() for sentence in draft]
    print("   Editor:     I cleaned it up. The notes are ready.")
    return final_notes


# ===========================================================================
# THE MANAGER  (runs the three helpers in the right order)
# ===========================================================================
# In real systems this "manager" is called an ORCHESTRATOR. Here it is just a simple function
# that calls the helpers one after another and passes the work along.

def run_the_team(topic):
    print(f"\n   The team starts working on: '{topic}'")
    points = researcher(topic)   # step 1
    draft = writer(points)       # step 2 (uses the researcher's points)
    notes = editor(draft)        # step 3 (uses the writer's draft)
    return notes


# ===========================================================================
# THE "JOB DONE" MESSAGE  (this is a WEBHOOK — a message sent back to you)
# ===========================================================================
# A webhook is just an automatic message that says "your job is finished, here is the result",
# so you don't have to keep asking "is it ready yet?". Like a food app texting you
# "your order is out for delivery" instead of you refreshing the screen every minute.

def send_done_message(topic, notes):
    print("\n   [Notification] Your job is DONE! Here are your final notes:")
    for i, line in enumerate(notes, start=1):
        print(f"       {i}. {line}")


# ===========================================================================
# THE "START" BUTTON  (this is a TRIGGER — it kicks everything off)
# ===========================================================================
# A trigger is simply the thing that STARTS the work: a button click, a form submit,
# a scheduled time, etc. Here, calling this function is like pressing "Start".

def press_start(topic):
    print("=" * 64)
    print("You pressed START (this is called a 'trigger').")
    print("=" * 64)
    notes = run_the_team(topic)      # the three helpers do their jobs
    send_done_message(topic, notes)  # you get a 'job done' message (a 'webhook')


# ===========================================================================
# RUN THE STORY
# ===========================================================================
def main():
    press_start("How to organise a class event")

    print("\n" + "-" * 64)
    print("What just happened, in plain words:")
    print("  • TRIGGER  = the START button that began the work.")
    print("  • TEAM     = researcher -> writer -> editor, each doing one job.")
    print("  • WEBHOOK  = the 'job done' message sent back to you at the end.")
    print("-" * 64)

    # Try it yourself (no coding needed to understand it):
    #   1) Change the topic in press_start(...) to anything you like and run again.
    #   2) Add a 4th helper (for example a "fact_checker") between writer and editor.
    #   3) Change the 3 points inside researcher(...) and watch the final notes change.


if __name__ == "__main__":
    main()
