# Claude Code: Security, Cost, and Enterprise Managed Settings

## Context of This Session

By now the agent can edit code, call MCP, and spawn sub-agents. This session is the **governance layer**: what IT can enforce, what you must never put in git, and how to read `/usage` before the bill becomes a story.

**In this session, you will:**

- Separate **CLAUDE.md advice** from **enforced** `permissions.deny` / sandbox
- Read org **managed settings** vs user vs project precedence
- Budget with `/usage`, `--max-budget-usd` (print mode), model/`/effort` choices
- Apply a secret-handling checklist (`.env`, MCP OAuth, heap dumps)

Official reference: [Settings](https://code.claude.com/docs/en/settings), [Managed settings](https://code.claude.com/docs/en/server-managed-settings), [Costs](https://code.claude.com/docs/en/costs.md), [Permissions](https://code.claude.com/docs/en/permissions). Links back to Module 9 governance notes.

---

## Advice vs Enforcement

Connecting sentence: Topic 51’s fridge magnet still cannot lock the door.

| Layer | Example | Strength |
| --- | --- | --- |
| Prompt / `CLAUDE.md` | “Never commit `.env`” | Claude *tries* to obey |
| `permissions.deny` | `Read(./.env)`, `Bash(curl *)` | CLI **blocks** |
| Hooks | `PreToolUse` on `Bash(rm *)` | Extra hard stop + message |
| Managed settings | Org deny + `disableBypassPermissionsMode` | Users **cannot** override |
| OS / network | No prod credentials on the laptop | Outside Claude entirely |

- **Official Definition:** **Managed settings** are organization (or machine) policy delivered from the claude.ai admin console, MDM/OS policy, or a system `managed-settings.json`. They sit at the **top** of the settings stack.
- **In Simple Words:** Your `.claude/settings.json` is house rules. Managed settings are **building code**.
- **Real-Life Example:** Greenfield can write “don’t push to main” in `CLAUDE.md`. A bank sets `permissions.deny` for `git push` to `main` and `allowManagedPermissionRulesOnly` so an intern’s local allow list cannot punch a hole.

`/status` → **Setting sources** tells you whether managed policy is actually loaded.

```json
{
  "permissions": {
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ],
    "disableBypassPermissionsMode": "disable"
  },
  "allowManagedPermissionRulesOnly": true
}
```

`--restricted` (where your CLI documents it) and **`--safe-mode`** shrink what *project* customizations can do. Safe-mode still honours **managed** policy. Use them for incident response (“which plugin did this?”) and for evals that must not load random MCP.

---

## Settings Precedence (Who Wins)

Connecting sentence: Broader policy wins. That is the point.

Highest → lowest (simplified):

1. **Managed** (server / MDM / system file) — including `allowManagedPermissionRulesOnly`, MCP allowlists
2. Command-line flags **except** they cannot beat managed keys
3. **Local** `.claude/settings.local.json`
4. **Project** `.claude/settings.json`
5. **User** `~/.claude/settings.json`

MCP servers have a parallel story: `allowedMcpServers`, `allowManagedMcpServersOnly`, `disabledMcpjsonServers`. A cloned `.mcp.json` still needs **workspace trust** (Topic 53).

**What a developer can still do:** other editors, raw `curl`, copying files. Claude Code policy is not a full DLP product. Combine with laptop management.

---

## Secrets Checklist

Connecting sentence: The leak is almost never “the model invented a key.” It is “someone put the key in a file Claude can Read.”

| Do | Do not |
| --- | --- |
| `.env` gitignored; deny `Read` on `.env*` | Commit `.env`, `settings.local.json` with tokens |
| MCP OAuth via `/mcp` | Paste bearer tokens into chat or `.mcp.json` |
| Placeholders in committed MCP JSON | Production URLs + live keys in git |
| Rotate if a key appeared in a transcript | Share `/heapdump` output |

`/heapdump` writes a JavaScript snapshot (often to Desktop). It contains **conversation text and credentials**. Diagnose memory; **never** attach it to a public issue.

`/privacy-settings` (Pro/Max) for product telemetry choices. Org ZDR / retention is an admin topic — Code Review cloud features may be off under ZDR (Topic 55).

**Sandbox:** Claude Code can restrict filesystem/network depending on platform settings. Treat “it ran in a sandbox” as extra, not as permission to skip deny rules.

> **[ Student Activity ]**
>
> **Leak hunt**
>
> List five paths in *this* notes repo you would put on `permissions.deny` for Read. Include at least one glob. Then name one leak deny **cannot** stop (hint: you photographing the terminal).

---

## Cost and Budgets

Connecting sentence: Parallel agents (Topic 56) are a cost multiplier with a friendly UI.

```text
/usage
```

Aliases: `/cost`, `/stats`.

| Audience | What `/usage` means |
| --- | --- |
| API / Console | Session token estimate (local math; Console is billing source of truth) |
| Pro / Max / Team / Enterprise | **Plan bars**, plus a breakdown (skills, sub-agents, MCP) from **this machine’s** recent history |

Other devices and claude.ai chat are **not** in that local breakdown. Press `d` / `w` for 24h vs 7d where offered.

```bash
claude -p "summarise README.md" --max-budget-usd 2
```

`--max-budget-usd` caps **print-mode** API spend **including sub-agents**. It is not a managed-settings key and it is not your Team plan limit. Admins use Console workspaces, gateway spend caps, and rate limits.

Levers you control in-session:

- `/model` — Haiku vs Sonnet vs Opus
- `/effort` — how hard this session thinks
- `/compact` vs letting the window rot into a second novel
- Don’t `/batch` a notes typo

`/usage-credits` (Pro/Max) can set a **personal** monthly credit cap if you have billing access.

---

## Incident Mini Playbook

Connecting sentence: When Claude “goes rogue,” isolate first, lecture second.

1. `claude --safe-mode` — did a plugin / CLAUDE.md cause it?
2. `/permissions` — unexpected allows in `settings.local.json`?
3. `/mcp` — disable unknown servers.
4. Rotate anything that appeared in chat.
5. Tell IT if managed settings **failed to load** (`/status`) — fail-open vs fail-closed is an org choice (`forceRemoteSettingsRefresh` exists for a reason).

---

## End-to-End Mini Lab (This Notes Repo)

1. `/status` — write down setting sources (managed or not).
2. Draft (do not need to ship) a project `permissions.deny` for env files.
3. `/usage` — screenshot-level notes for yourself; do not commit account identifiers.
4. Confirm `.gitignore` has `CLAUDE.local.md` and `.claude/settings.local.json`.
5. Write one sentence: advice vs deny vs managed, using “never `curl` production.”

---

## Key Takeaways

- **`CLAUDE.md` advises. Deny/hooks/managed enforce.**
- Managed settings are the top of the stack; trust and MCP allowlists are part of the same story.
- **Secrets:** gitignore + deny Read + never heapdump-share.
- **`/usage` is a dashboard, not an invoice.** `--max-budget-usd` is for `-p` runs.

**Upcoming:** Topic 59 — capstone: one bounded job that uses the whole stack, then a publish/don’t-publish gate.

---

## Quick Reference — Important Commands, Files, and Terminologies

| Term / item | Meaning |
| --- | --- |
| Managed settings | Org/machine policy; highest precedence |
| `allowManagedPermissionRulesOnly` | Ignore non-managed permission rules |
| `disableBypassPermissionsMode` | Ban bypass mode |
| `/status` | See setting sources |
| `/usage` | Session / plan usage |
| `--max-budget-usd` | Print-mode spend cap |
| `/heapdump` | Memory snapshot — **secret** |
| `/privacy-settings` | Subscriber privacy UI |
| `--safe-mode` | Strip project customizations |
| Workspace trust | Project allows/MCP wait until accepted |
| Fail-open | Session continues if remote policy fetch fails |

⬅️ [Back to module](../)
