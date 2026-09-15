# Claude Code: Setup, Memory, and Project File Structure

## Context of This Session

In the **previous** session you learned the commands people actually type: `claude`, `/plan`, `/compact`, `/diff`. Those commands still fail if every teammate has a different “how we work here” story in their head.

Today you wire the **project so Claude starts with the same facts every session**: install + login, `CLAUDE.md` vs auto memory, and a `.claude/` layout you can commit without leaking secrets.

**In this session, you will:**

- Install and authenticate Claude Code, then confirm health with `claude doctor`
- Choose **where** instructions live: managed policy, user, project, local
- Write a **short** `CLAUDE.md` and optional `.claude/rules/` files
- Understand **auto memory** (`MEMORY.md`) vs files **you** author
- Commit a **safe folder tree** (gitignore `CLAUDE.local.md` and local settings)

---

## What Claude Code Is (Setup Mental Model)

- **Official Definition:** **Claude Code** is Anthropic’s agentic coding CLI (and IDE integrations) that works in a project directory with tools for files, shell, and optional MCP servers.
- **In Simple Words:** A very fast intern who can open the whole cupboard — but only remembers what you wrote on the fridge magnet and what they jotted in their own notebook.
- **Real-Life Example:** Greenfield’s placement FAQ lives in git. Ananya’s personal sandbox URL does **not**. `CLAUDE.md` is the shared fridge magnet. `CLAUDE.local.md` is Ananya’s sticky note on her laptop.

Each session starts with a **fresh context window**. Persistence comes from files and auto memory, not from “Claude magically remembers last Tuesday.”

---

## Install and First Run

Connecting sentence: Treat setup like Python’s venv — do it once, verify, then stop tinkering.

1. Install the CLI using Anthropic’s current instructions for your OS (native binary is the usual path; some teams pin a version with `claude install stable`).
2. Sign in:

```bash
claude auth login
claude auth status
```

3. Health:

```bash
claude --version
claude doctor
```

4. From the repo:

```bash
cd generative-ai-notes
claude --permission-mode plan
```

Then `/status` inside the session. Confirm model, account, and that you are in the folder you think you are.

**Common mistake:** Running `claude` from `$HOME`. It will try to treat your entire home directory as the project. Always `cd` into the repo first.

**IDE:** VS Code / JetBrains extensions can start Claude Code with their own permission defaults. The **files** (`CLAUDE.md`, `.claude/`) are the same.

> **[ Student Activity ]**
>
> **Cwd check**
>
> Start Claude in this notes repo. Ask: “What is my current working directory and which `CLAUDE.md` files did you load? Use `/context` if needed.” Write the paths. If the answer is your home folder, you launched from the wrong place.

---

## Two Memory Systems

Connecting sentence: Teams fight because they put procedures in the wrong drawer.

Claude Code loads **both** at the start of a conversation. They are **context**, not a hard lock. To *block* an action no matter what Claude decides, you need a **hook** or **permission deny** (later topics) — not a polite sentence in markdown.

| | **CLAUDE.md** (and rules) | **Auto memory** |
| --- | --- | --- |
| Who writes it | You / the team / IT | Claude, from corrections and patterns |
| What it holds | Instructions, commands, architecture facts | Learnings, debug notes, preferences it noticed |
| Where it lives | Repo, `~/.claude/`, or org policy path | Usually `~/.claude/projects/<project>/memory/` |
| Use for | “Always run tests with X” | “This package’s tests hang unless we set Y” |

- **Official Definition:** **`CLAUDE.md` files** are markdown instructions Claude reads at session start. **Auto memory** is notes Claude writes for itself across sessions.
- **In Simple Words:** The employee handbook vs the intern’s private notebook.
- **Real-Life Example:** “Never commit `.env`” belongs in `CLAUDE.md`. “The refund eval fixture is named `trace_refund_policy.json`” may start in auto memory after you correct Claude twice.

Toggle auto memory with `/memory` (writes `autoMemoryEnabled` in settings). Disable for one project:

```json
{
  "autoMemoryEnabled": false
}
```

Or set `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. Auto memory is **machine-local** — it is not a substitute for git.

`MEMORY.md` is an **index**. Claude Code loads roughly the first **200 lines or 25KB**. Detail should move into topic files (`debugging.md`, …). If the index grows past the limit, later lines are dropped on the next load.

---

## Where CLAUDE.md Can Live (Load Order)

Connecting sentence: Broader files load first; closer files are read later — so the folder you launched in usually “speaks last.”

| Scope | Typical path | Who sees it | Example |
| --- | --- | --- | --- |
| Managed policy | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md` (Linux/Windows have org paths) | Whole machine / org | “Never push to `main`” |
| User | `~/.claude/CLAUDE.md` | Only you, all projects | Personal tone, editor habits |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team via git | Build, test, layout |
| Local | `./CLAUDE.local.md` | Only you, this clone | Sandbox URLs — **gitignore this** |

Claude also walks **parent directories** for `CLAUDE.md` / `CLAUDE.local.md`. Nested `CLAUDE.md` under subfolders often load **when Claude reads files in that folder**, not always at launch.

Confirm load with `/context` → Memory files.

### `/init`

`/init` explores the repo and **writes or suggests** a starter `CLAUDE.md`. If one exists, it proposes improvements rather than blindly overwriting.

```bash
# Optional richer wizard (skills, hooks, personal files)
CLAUDE_CODE_NEW_INIT=1
```

Then run `/init` inside the session.

### AGENTS.md

Claude Code reads **`CLAUDE.md`**, not `AGENTS.md`. If the repo already has `AGENTS.md` for other tools:

```markdown
@AGENTS.md

## Claude Code
Use plan mode for changes under `src/billing/`.
```

Or symlink: `ln -s AGENTS.md CLAUDE.md` (on Windows, prefer the `@` import).

Imports use `@path` in `CLAUDE.md`. Relative paths resolve from **the file that contains the import**. Imports can nest (limited depth). Wrap `@README` in backticks if you only want to *mention* a path, not import it.

---

## Write CLAUDE.md That Claude Will Follow

Connecting sentence: Long novels get skimmed. Fridge magnets get followed.

**Size:** Aim **under ~200 lines** per file. Procedures belong in **skills** (next topic). Path-specific noise belongs in **`.claude/rules/`**.

**Specificity:**

| Weak | Strong |
| --- | --- |
| Format code properly | Use 2-space indentation in JS |
| Test your changes | Run `python3 -m pytest Coding-Examples/rag_pipeline` before committing |
| Keep files organized | API handlers live in `src/api/handlers/` |

**Structure:** markdown headings and bullets. Contradictory rules → Claude may pick at random. Review nested files.

**HTML comments** in `CLAUDE.md` are stripped from Claude’s context (human-only notes). Comments inside fenced code stay.

Example project file (short on purpose):

```markdown
# Greenfield notes repo

## Commands
- Run Python examples from the topic `code/` folder or `Coding-Examples/`.
- Do not commit `.env` or API keys.

## Style
- Lecture notes use Official Definition / In Simple Words / Real-Life Example.
- Do not invent new module numbers; follow README.md.

## Safety
- Never run destructive git commands unless the user names them explicitly.
```

> **[ Student Activity ]**
>
> **Magnet drill**
>
> Write six bullets you would put in *this* repo’s `CLAUDE.md`. Strike any bullet that is a multi-step procedure (that belongs in a skill) or a personal URL (that belongs in `CLAUDE.local.md`).

---

## `.claude/rules/` — Modular, Sometimes Path-Scoped

Connecting sentence: When `CLAUDE.md` becomes a junk drawer, split it.

```text
your-project/
├── CLAUDE.md                 # or .claude/CLAUDE.md
├── CLAUDE.local.md           # gitignored
└── .claude/
    ├── settings.json         # team defaults (optional)
    ├── settings.local.json   # gitignored machine overrides
    └── rules/
        ├── testing.md
        ├── security.md
        └── api-design.md
```

Rules without `paths` frontmatter load like extra project instructions. Path-scoped rules load when Claude works with matching files:

```markdown
---
paths:
  - "Coding-Examples/**/*.py"
---

# Python labs
- Prefer stdlib first; pin extra deps in that lab’s folder.
```

User-level rules live in `~/.claude/rules/` and apply to every project on your machine.

---

## Recommended Project Tree for a Team

Connecting sentence: This is the “venv + `.env.example`” lesson, but for Claude.

```text
your-repo/
├── CLAUDE.md
├── CLAUDE.local.md          # gitignore
├── .gitignore
├── .claude/
│   ├── settings.json        # committed team defaults
│   ├── settings.local.json  # gitignore
│   ├── rules/               # optional, committed
│   ├── skills/              # next topic
│   ├── agents/              # next topic
│   └── commands/            # legacy custom slash files; still work
├── README.md
└── src/  or  notes folders…
```

**`.gitignore` extras:**

```text
CLAUDE.local.md
.claude/settings.local.json
.claude/agent-memory-local/
```

**settings.json** (idea only — teams differ): default permission mode, extra directories, denied bash patterns. **Managed org settings** override user and project when IT deploys them.

**Trust dialog:** the first time Claude Code opens a folder, you accept workspace trust. Hooks and some local settings only apply after that — same idea as “this repo is allowed to run project automation.”

### What not to put in git

| Commit | Do not commit |
| --- | --- |
| `CLAUDE.md`, `.claude/rules/`, project skills | API keys, `.env`, `CLAUDE.local.md` |
| `.claude/settings.json` without secrets | `settings.local.json` with machine paths |
| Example MCP config with placeholders | OAuth tokens, production URLs |

---

## Auto Memory Directory (So You Are Not Surprised)

Default shape:

```text
~/.claude/projects/<encoded-project>/memory/
├── MEMORY.md           # index loaded every session (capped)
├── debugging.md
└── api-conventions.md
```

Same git repo → same auto-memory folder across worktrees. Not synced to teammates’ laptops.

`/memory` is the UI to edit CLAUDE.md files, toggle auto memory, and inspect entries.

**Subagents** do **not** automatically get the main conversation’s auto memory. They can have their own `memory:` field (next topic).

---

## Troubleshooting Setup

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Ignores your rules | File not loaded, too long, or contradictory | `/context`; shorten; one rule per idea |
| Personal URL leaked in a PR | Wrote it in `CLAUDE.md` | Move to `CLAUDE.local.md` |
| Two CLAUDE.md files fighting | User + project + nested | Make project the source of truth; trim user file |
| “Unknown command” | Old CLI | `claude update` then `claude --version` |
| Skills/hooks not loading | Launched with `--bare` or `--safe-mode` | Restart without those flags |

`claude --safe-mode` **disables** project customizations on purpose — use it to test whether a plugin/`CLAUDE.md` is the bug.

---

## Key Takeaways

- Setup is **cwd + auth + doctor**. Launch from the repo, not from `$HOME`.
- **`CLAUDE.md` is the team handbook.** Keep it short, specific, and in git.
- **Auto memory is Claude’s notebook** on *your* machine. It does not replace documentation.
- **`CLAUDE.local.md` and `settings.local.json` stay off git.**
- **`.claude/rules/`** splits a growing handbook; **skills** (next session) hold procedures.

**Upcoming:** Topic 52 — `SKILL.md`, custom `/commands`, org-managed agents, Claude **Managed Agents** on the API, and **sub-agents**.

---

## Quick Reference — Important Commands, Files, and Terminologies

| Term / path | Meaning |
| --- | --- |
| `claude auth login` | Sign in |
| `claude doctor` | Shell diagnostics |
| `/init` | Generate / improve `CLAUDE.md` |
| `/memory` | Edit memory; toggle auto memory |
| `/context` | Confirm which memory files loaded |
| `CLAUDE.md` | Project or user instructions |
| `CLAUDE.local.md` | Personal, gitignored |
| `~/.claude/CLAUDE.md` | Your global handbook |
| `.claude/rules/` | Modular / path-scoped rules |
| Auto memory | Claude-written `MEMORY.md` index |
| `@AGENTS.md` | Import shared agent instructions |
| `--safe-mode` | Load almost no customizations |
| `--bare` | Minimal discovery for scripts |
| Workspace trust | Gate for project hooks/settings |
