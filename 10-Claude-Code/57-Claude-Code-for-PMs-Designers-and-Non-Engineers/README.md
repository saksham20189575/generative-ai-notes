# Claude Code for PMs, Designers, and Non-Engineers

## Context of This Session

Topic 50 was a **command cheat sheet**. This session is the **job design**: how Meera (PM), a designer, and Campus Ops use the same CLI without becoming unofficial SREs.

**In this session, you will:**

- Run a **plan-only** working agreement (no surprise edits)
- Ask for cited file paths, user-visible diffs, and refusal cases
- Use `/review`, `/export`, `/team-onboarding`, `/insights`
- Hand engineers a packet: job sentence, files in scope, out-of-scope list

Official reference: [Commands](https://code.claude.com/docs/en/commands), [CLI](https://code.claude.com/docs/en/cli-reference).

---

## The Working Agreement

Connecting sentence: Power without a contract is how FAQs get rewritten at 11pm.

- **Official Definition:** **Plan mode** is a permission mode in which Claude explores the repo and proposes work but does not edit source until you leave that mode. Non-engineers use it as a **default contract**, not as a one-off.
- **In Simple Words:** You hired a fast intern. Plan mode is “read the filing cabinet; do not use the shredder until I say.”
- **Real-Life Example:** Meera starts every Greenfield session with `claude --permission-mode plan` and the sentence “Do not edit files. Cite paths.” Ananya is allowed `acceptEdits` on a throwaway branch after the plan is accepted.

```bash
cd generative-ai-notes
claude --permission-mode plan
```

Put the contract in **project** `CLAUDE.md` if the whole squad agrees; put Meera’s extra caution in **`CLAUDE.local.md`** so it does not lecture engineers.

**When to stop and ping an engineer**

| You hit this | Why it is not a PM job |
| --- | --- |
| Permission / sandbox errors you cannot parse | Policy, not product |
| MCP needs a production token | Secret handling (Topic 58) |
| Claude wants to change CI, IAM, or `main` | Blast radius |
| `/security-review` flags auth or PII | Needs an owner |

---

## Prompt Patterns That Keep You Honest

Connecting sentence: Vague prompts produce confident fiction. Tight prompts produce footnotes.

| Pattern | Example |
| --- | --- |
| Only these files | “Only use `greenfield_leave_policy.txt` and Topic 50 README. Do not open other modules.” |
| Do not edit | “Answer in chat. Do not Write or Edit.” |
| Cite | “Every claim: `path` + heading. If you cannot find it, say so.” |
| User-visible | “Describe what a student sees on screen, not the class names.” |
| Leadership | “Five bullets for Campus Ops. No stack traces.” |
| Refusal | “If I ask for production student emails, refuse and tell me who to ask.” |
| Knowledge boundary | “You may use this repo and the ticket text I paste. No guessing HR policy.” |

Kickoff template:

```text
Job: Explain how leave requests are described in this notes repo.
Files in scope: 10-Claude-Code/50-*/README.md and any file you cite.
Out of scope: Editing files, Coding-Examples, inventing policy.
Done when: I have a numbered file map and three open questions for Ananya.
```

**Common doubt:** *Do I need to read Python?* You need to **recognise** file names and reject a plan that edits twenty packages. You do not need to write the parser.

> **[ Student Activity ]**
>
> **Packet**
>
> Write a four-line packet (job, in scope, out of scope, done when) for: “Draft a student-facing FAQ from Topic 51 about CLAUDE.md vs auto memory.” Swap with a neighbour; strike any line that would let Claude edit `.claude/settings.json`.

---

## Commands for People Who Do Not Ship Compilers

Connecting sentence: Topic 50 listed these. Here is **when**.

| Command | PM / designer / ops use |
| --- | --- |
| `/help` | See what **your** plan and install actually expose |
| `/plan …` | Force a written approach before anyone implements |
| `/review [PR]` | User-visible risk, empty states, copy — not import order |
| `/diff` | Confirm Claude did not write files despite the contract |
| `/btw …` | Side question; keeps the spec thread clean |
| `/export notes.md` | Conversation → text for Confluence / Google Doc |
| `/team-onboarding` | Guide from ~30 days of *your* Claude usage for the next PM |
| `/insights` | Where sessions actually go (friction, project areas) |
| `/usage` | Plan bars — ping a lead before the team burns the cap |
| `/compact` | Same meeting, cleaner board |
| `/clear` | New ticket, new meeting |

`/team-onboarding` can also produce a **share link** on Pro/Max/Team/Enterprise (claude.ai). Paste the markdown if you are on a Console-only classroom.

**Review sentence** (repeat from Topic 55, it earns it):

```text
Ignore style nits. List user-visible behaviour, PII/secret risk,
and what Campus Ops would see if this merged today. Cite paths.
```

---

## Designers

Connecting sentence: Screenshots are data. Component names are better data.

```text
/design-sync
/design-login
```

`/design-sync` uploads a **React design system** from the repo to Claude Design so generated screens use **your** components. First sync can take a long time. It needs Anthropic API reach to claude.ai — **unavailable** on some enterprise clouds (Bedrock / Vertex / Foundry).

If the command is missing:

1. Attach screenshots.
2. Name the components (`Button`, `EmptyState`).
3. “Do not invent a new colour token. Propose copy only.”

Never paste Figma access tokens into chat; use the product’s login command.

---

## Campus Ops / Content

Connecting sentence: FAQs live in git. Your tone lives in a local file.

- Point at the **policy file**, not “whatever you know about leave.”
- `/export` after a good thread so the next hire does not start from zero.
- Refuse: live student records, unmarked production dumps, “just this CSV.”

---

## Handoff to Engineering

Connecting sentence: The deliverable is a packet, not a vibe.

1. Job sentence (one line).
2. Files / folders in scope.
3. Out of scope (especially MCP, secrets, `main`).
4. Acceptance: screenshots, FAQ bullets, or a PR number.
5. Open questions — numbered.

Engineers then leave plan mode. You can still `/review` the PR.

---

## End-to-End Mini Lab (This Notes Repo)

1. `claude --permission-mode plan`.
2. Ask for a map of `10-Claude-Code/` with citations. No edits.
3. `/diff` — must be empty. If not, `/rewind` code or git restore and tighten the prompt.
4. `/export pm-session.md` (gitignored or do not commit).
5. Draft the four-line packet for Ananya: “Add one student activity to Topic 53.”

---

## Key Takeaways

- **Plan mode is the job.** Edits are an explicit promotion.
- **Cite paths or it did not happen.**
- **`/review` + user-visible prompt** is the PM superpower.
- **Stop** at secrets, production data, and CI. That is Topic 58 plus an engineer.

**Upcoming:** Topic 58 — **enforced** policy, cost, and what never belongs in git.

---

## Quick Reference — Important Commands, Files, and Terminologies

| Term / item | Meaning |
| --- | --- |
| Plan-only agreement | Default `--permission-mode plan` + “do not edit” |
| Packet | Job, scope, out of scope, done-when |
| `/review` | Fast PR read for product risk |
| `/export` | Save the thread as text |
| `/team-onboarding` | Pasteable setup guide from usage history |
| `/insights` | Session pattern report |
| `/btw` | Side question |
| `/design-sync` | Push repo components to Claude Design |
| `/usage` | Remaining plan / session cost |
| Knowledge boundary | What sources Claude may use |

⬅️ [Back to module](../)
