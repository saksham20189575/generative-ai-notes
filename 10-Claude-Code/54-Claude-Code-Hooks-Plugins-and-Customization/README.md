# Claude Code: Hooks, Plugins, and Customization

## Context of This Session

In the **previous** session, permissions decide *whether* a tool may run. **Hooks** decide *what must happen* around that tool — formatters, secret scanners, “never `rm -rf`.” **Plugins** ship skills, agents, MCP, and hooks as a pack.

**In this session, you will:**

- Place `PreToolUse` / `PostToolUse` (and related) hooks in `.claude/`
- Install and reload plugins (`/plugin`, `/reload-plugins`)
- Know what `--safe-mode` strips when customizations misbehave
- Choose settings scope: user vs project vs managed

Official reference: [Hooks](https://code.claude.com/docs/en/hooks), [Plugins](https://code.claude.com/docs/en/discover-plugins), [CLI `--safe-mode`](https://code.claude.com/docs/en/cli-reference).

---

## Why Markdown Is Not Enough

Connecting sentence: Topic 51 said `CLAUDE.md` is a fridge magnet. Hooks are the lock on the door.

- **Official Definition:** A **hook** is automation that runs on Claude Code **lifecycle events** (session start, a tool about to run, a tool that just succeeded, compact, …). A **plugin** is a distributable folder that can include skills, sub-agents, MCP servers, hooks, and settings.
- **In Simple Words:** A hook is a **security guard** (or a janitor who tidies after every edit). A plugin is a **care package** the whole team installs once.
- **Real-Life Example:** “Format Python after every Write” is a `PostToolUse` hook. “Greenfield lecture-note skill + navigator agent + that hook” is a **plugin**.

Permissions **hide or block** tools. Hooks can **inspect stdin JSON**, block with an error message, or run `ruff` after a successful edit. Use both.

---

## Hook Events You Will Actually Use

Connecting sentence: Dozens of events exist. Five cover ninety percent of classroom work.

| Event | When | Typical job |
| --- | --- | --- |
| `PreToolUse` | Before a tool runs | Block `Bash(rm *)`, scan a Write path |
| `PostToolUse` | After a tool **succeeds** | Format the file that was just edited |
| `PostToolUseFailure` | After a tool **fails** | Log, notify |
| `SessionStart` | Session begins or resumes | Inject extra context (sparingly) |
| `Stop` | Claude finished a turn | Notify that it is your turn |
| `PreCompact` | Before `/compact` | Snapshot something you must not lose |

Also useful later: `UserPromptSubmit` (inspect/block a prompt), `WorktreeCreate` / `WorktreeRemove` (custom VCS), `Notification` (desktop ping).

Cadence:

- Once per session: `SessionStart`, `SessionEnd`
- Once per turn: `UserPromptSubmit`, `Stop`
- Every tool in the loop: `PreToolUse`, `PostToolUse` (`EndConversation` skips both)

### Where hooks live

| Location | Who gets it |
| --- | --- |
| `~/.claude/settings.json` | You, all projects |
| `.claude/settings.json` | Team, via git |
| `.claude/settings.local.json` | You, this clone (gitignore) |
| Managed policy | Whole org — users cannot override |
| Plugin `hooks/hooks.json` | When the plugin is on |
| Skill / agent frontmatter | While that component is active |

`/hooks` is a **read-only** browser: event, matcher, source file. To change a hook, edit JSON or ask Claude to edit it — the menu does not write.

### Settings format (project / user)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/format.sh"
          }
        ]
      }
    ]
  }
}
```

- **matcher** — tool name (or `Write|Edit`). MCP tools use `mcp__server__tool`.
- **if** — extra permission-style filter (`Bash(rm *)`).
- **command** — stdin is JSON about the tool call; stdout/exit code can **allow**, **deny**, or (for some events) **rewrite input**.

`${CLAUDE_PROJECT_DIR}` is the **stable project root** (where the session started), even if Claude later `cd`s or enters a worktree. Read the worktree path from the hook JSON `cwd` field if you need it.

**Types:** `command` (shell), `http` (POST), `prompt` (a small LLM check). Start with `command`.

Plugin `hooks/hooks.json` wraps the same events under a top-level `hooks` key plus an optional `description`.

> **[ Student Activity ]**
>
> **Magnet vs lock**
>
> For each wish, pick `CLAUDE.md`, permission deny, or hook: (1) “Prefer pytest.” (2) “Never read `.env`.” (3) “If Claude writes a `.py` file, run the formatter.” One sentence of why.

---

## Plugins — A Pack, Not a Blog Post

Connecting sentence: If three repos copy the same skill folder, you wanted a plugin.

### Install

The official marketplace (`claude-plugins-official`) is added on first interactive start.

```text
/plugin
/plugin install github@claude-plugins-official
/reload-plugins
```

Shell equivalents: `claude plugin install …`, `claude plugin marketplace add owner/repo`.

| Piece | Typical path inside the plugin |
| --- | --- |
| Manifest | `.claude-plugin/plugin.json` |
| Skills | `skills/` |
| Sub-agents | `agents/` |
| Hooks | `hooks/hooks.json` |
| MCP | `.mcp.json` or inline in `plugin.json` |

`--plugin-dir ./my-plugin` loads a folder or `.zip` **for this session only** (repeat the flag for several). Good for class demos before you publish a marketplace.

`/reload-plugins` if the install summary says the plugin is on disk but not active yet.

**Common mistake:** Committing a plugin that embeds API keys in MCP `headers`. Same rule as Topic 53.

> **[ Student Activity ]**
>
> **Pack the drawer**
>
> List three things from Topics 51–53 you would put in a *Greenfield notes* plugin, and one thing you would **not** (hint: Ananya’s sandbox URL).

---

## Other Customization (Keep It Small)

Connecting sentence: Status lines and output styles are paint. Hooks are plumbing.

| Control | What it is |
| --- | --- |
| `/config` | Session settings UI |
| `/statusline` | Ask Claude to generate a status-line script |
| Output styles | How answers are phrased (including bundled “explanatory” styles) |
| `/theme` | Colours — does not change tool policy |

A status line is a `statusLine.command` in settings. It runs a script; treat it like any other executable you did not audit.

---

## Settings Scope and `--safe-mode`

Connecting sentence: When the intern starts formatting *poetry*, you need a kill switch.

| Scope | Path | Override? |
| --- | --- | --- |
| Managed | Console / MDM / `managed-settings.json` | Nothing below it |
| User | `~/.claude/settings.json` | Project can add, not smash policy |
| Project | `.claude/settings.json` | Team defaults |
| Local | `.claude/settings.local.json` | Your machine |

```bash
claude --safe-mode
```

From CLI v2.1.169, **`--safe-mode`** starts with customizations **off**: project `CLAUDE.md`, skills, plugins, hooks, MCP, custom agents/commands, output styles, status line, auto-memory, … Auth, model, built-in tools, and **permissions** still work. **Managed policy** still applies (including policy hooks). Use it to answer: “Is a plugin / CLAUDE.md making Claude weird?”

`--bare` is the even thinner profile for scripts. `--plugin-dir` is the opposite: *add* a plugin once.

IT can set `disableAllHooks` or `allowManagedHooksOnly` so only org hooks run.

---

## End-to-End Mini Lab (This Notes Repo)

1. Add a `PostToolUse` hook matcher `Write|Edit` that echoes the file path to a gitignored log (no secrets).
2. `/hooks` — confirm the event count went up.
3. Trigger a tiny edit in plan-then-accept, or skip if you are read-only: still validate JSON with `python3 -m json.tool`.
4. Run `claude --safe-mode` and confirm `/hooks` no longer shows the project hook.
5. Optional: `claude --plugin-dir` on a toy folder with one skill.

Do not commit hook scripts that call production APIs with keys.

---

## Key Takeaways

- **Permissions** gate tools. **Hooks** run *around* tools and can hard-block.
- Commit **project** hooks that the whole team needs; keep experiments in **local** settings.
- A **plugin** is skills + agents + MCP + hooks with a `plugin.json`.
- **`--safe-mode`** is the broken-config fire extinguisher; managed policy still burns.

**Upcoming:** Topic 55 — how work **leaves** the laptop: `/diff`, reviews, GitHub, `/rewind` vs git.

---

## Quick Reference — Important Commands, Files, and Terminologies

| Term / item | Meaning |
| --- | --- |
| Hook | Lifecycle automation (command / http / prompt) |
| `PreToolUse` | Before a tool; can block |
| `PostToolUse` | After success |
| `/hooks` | Read-only hook browser |
| `.claude/settings.json` → `hooks` | Project hook config |
| Plugin `hooks/hooks.json` | Bundled hooks |
| `/plugin` | Marketplace + install UI |
| `/reload-plugins` | Activate a just-installed plugin |
| `--plugin-dir` | Session-only plugin path |
| `--safe-mode` | Disable most customizations |
| `${CLAUDE_PROJECT_DIR}` | Stable project root for hook scripts |
| `/statusline` | Generate a status-line command |

⬅️ [Back to module](../)
