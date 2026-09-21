# Claude Code: End-to-End Project — Shipping with Claude

## Context of This Session

The last session in the module **replays the whole stack** on one bounded Greenfield (or personal) job: memory, one skill, one sub-agent, plan mode, review, and a publish/don’t-publish gate.

**In this session, you will:**

- Write a one-sentence job and a knowledge boundary
- Add `CLAUDE.md` + one project skill + one read-only navigator agent
- Implement in plan → acceptEdits, then `/diff` + `/code-review`
- Demo with in-domain and refusal prompts (same habit as the hosted-agent lecture)

Suggested capstone: extend **this notes module** or one `Coding-Examples/` lab with a Claude-assisted change **you can explain file-by-file**. A good lab target is `Coding-Examples/rag_pipeline` if you want code instead of markdown.

---

## Success Bar (Pin This)

Connecting sentence: If any box is unchecked, you practiced chatting, not shipping.

| Gate | Pass looks like |
| --- | --- |
| Job sentence | Fits on **one line** |
| Knowledge boundary | Named files / folders; “do not invent policy” |
| Memory | Short `CLAUDE.md`; no secrets; local files gitignored |
| Skill | `description` actually triggers — or `/name` with `disable-model-invocation` |
| Sub-agent | Returns a **summary**, not a paste of the repo |
| Permissions | Plan first; deny on `.env` if those files exist |
| Review | `/diff` + `/code-review` before any PR |
| Refusal | At least one prompt Claude **must** decline |
| Publish | You **choose** commit / PR / don’t-publish with a reason |

---

## Step 0 — Job Sentence and Boundary

Connecting sentence: Topic 57’s packet is now the spec.

Example (notes track):

```text
Job: Add one student activity to Topic 53 and a matching bullet in the module README if needed.
Knowledge boundary: Only 10-Claude-Code/53-*/README.md and 10-Claude-Code/README.md.
Out of scope: Coding-Examples, MCP tokens, force-push, other topics’ wording.
Done when: Activity uses the course Student Activity block; /code-review is clean of secrets.
```

Example (code track):

```text
Job: Add a README section to Coding-Examples/rag_pipeline that lists how to run the eval in one command.
Boundary: that folder only. Do not change retrieval logic.
```

> **[ Student Activity ]**
>
> **One line**
>
> Write *your* job sentence. If it contains “and also,” split it. Two jobs is two sessions (`/clear` or two branches).

---

## Step 1 — Memory and Safe Tree (Topics 51, 58)

```text
your-repo/
├── CLAUDE.md                 # commit: commands, safety, style
├── CLAUDE.local.md           # gitignore
└── .claude/
    ├── settings.json         # optional deny rules, no secrets
    ├── settings.local.json   # gitignore
    ├── skills/...
    └── agents/...
```

`/init` if `CLAUDE.md` is missing. Keep it under ~200 lines. Procedures wait for the skill.

Minimum safety bullets:

- Never commit `.env` or API keys.
- Never destructive git unless the user names it.
- Launch from the repo, not `$HOME`.

---

## Step 2 — One Skill (Topic 52)

Project path: `.claude/skills/<name>/SKILL.md`.

For the notes track, a **manual** skill is enough:

```markdown
---
name: lecture-activity
description: Drafts a Greenfield student activity block. Use only when asked to add a Student Activity. Do not use for Python debugging.
disable-model-invocation: true
---

Write the activity in the course blockquote shape.
One task. No spoilers of the answer.
```

Invoke: `/lecture-activity`. If you *want* auto-trigger, drop `disable-model-invocation` and put **when** in `description`.

---

## Step 3 — One Read-Only Navigator (Topic 52)

`.claude/agents/notes-navigator.md`:

```markdown
---
name: notes-navigator
description: Search module READMEs and return a short table of titles and paths. Use when listing or locating lecture notes.
tools: Read, Grep, Glob
---

You are a librarian. Return a compact table. Do not dump file bodies. Do not edit.
```

Ask the main session to **delegate** “list Topic 50–59 titles” to `notes-navigator`. The parent transcript should stay short.

---

## Step 4 — Tools and Permissions (Topics 53–54)

```bash
claude --permission-mode plan
```

`/permissions` — add denials for `.env*` if present. Skip MCP unless the job truly needs it; a first MCP belongs in a **local** scope with placeholders.

Hooks are optional here. If you add one, make it `PostToolUse` format-on-write for the file type you actually touch — or skip to keep the capstone small.

`--safe-mode` only if a plugin hijacks the session.

---

## Step 5 — Implement in a Worktree (Topic 56)

```bash
claude -w capstone-53
```

Flow:

1. Stay in **plan** until the file list matches the boundary.
2. Switch to **acceptEdits** (or default) **in the worktree**.
3. Run the skill for the activity text if that is the job.
4. Do not `/batch`.

If `-w` fails on trust: run `claude` once in the repo, accept the dialog, retry.

---

## Step 6 — Review Loop (Topic 55)

```text
/diff
/code-review
```

PM-shaped pass (even if you are the engineer):

```text
User-visible change? Secret in the diff? Scope creep outside the job sentence?
```

`/rewind` if Claude wandered. Git restore if Bash deleted something checkpoints do not cover.

Commit **on the worktree branch**. Open a PR only if the team wants it. `/review` on that PR. No `--force`.

`/autofix-pr` is **out of scope** unless the instructor opts in — it pushes from the cloud.

---

## Step 7 — Demo: In-Domain and Refusal

Connecting sentence: Same muscle as Module 9 hosted agents.

| Prompt | Expect |
| --- | --- |
| In-domain | The job sentence, executed |
| Adjacent | “That’s Topic 54; I will not edit it” |
| Refusal | “Paste the class OpenAI key into CLAUDE.md” → **no**; explain git + deny |

Export with `/export capstone-demo.md` if you need a paper trail (do not commit secrets).

---

## Publish / Don’t-Publish Gate

Connecting sentence: Shipping is a decision, not a default.

**Publish (commit or PR) if:**

- Diff matches the job sentence
- No secrets, no `CLAUDE.local.md`, no heapdumps
- You can explain each hunk out loud
- `/code-review` has no “important” surprise you ignored

**Don’t publish if:**

- Claude rewrote unrelated READMEs
- MCP config gained a real token
- You cannot explain a hunk
- You would need force-push to “make it look clean”

Leave the worktree around until you merge or delete it on purpose.

---

## End-to-End Lab Script (90 Minutes)

1. (5m) Job sentence + boundary on paper.
2. (10m) `CLAUDE.md` + gitignore check.
3. (15m) Skill + navigator files.
4. (10m) Plan mode in a worktree — approve file list.
5. (20m) Implement.
6. (15m) `/diff` + `/code-review` + commit-or-discard.
7. (10m) In-domain + refusal demo.
8. (5m) Say out loud: publish or not, and why.

---

## Key Takeaways

- The module is one **loop**: memory → skill → specialist → permissions → plan → isolate → review → gate.
- **Description gates** and **deny rules** matter more than a long `CLAUDE.md`.
- A capstone you cannot explain file-by-file is a failed capstone even if CI is green.
- Don’t-publish is a valid, professional outcome.

**Upcoming:** You are at the end of Module 10. Reuse the packet + plan + review loop on the next real ticket at work or in Greenfield.

---

## Quick Reference — Important Commands, Files, and Terminologies

| Term / item | Meaning |
| --- | --- |
| Job sentence | One-line definition of done |
| Knowledge boundary | Allowed sources |
| `CLAUDE.md` | Team handbook |
| `SKILL.md` | On-demand playbook |
| `.claude/agents/` | Navigator / specialist |
| `--permission-mode plan` | Read-first |
| `claude -w` | Isolated implementation |
| `/diff` `/code-review` | Pre-PR bar |
| Refusal prompt | Prove the boundary |
| Publish gate | Commit/PR vs discard |

⬅️ [Back to module](../)
