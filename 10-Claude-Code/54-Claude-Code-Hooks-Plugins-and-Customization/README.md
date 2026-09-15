# Claude Code: Hooks, Plugins, and Customization

## Context of This Session

In the **previous** session, permissions decide *whether* a tool may run. **Hooks** decide *what must happen* around that tool — formatters, secret scanners, “never `rm -rf`.” **Plugins** ship skills, agents, MCP, and hooks as a pack.

**In this session, you will:**

- Place `PreToolUse` / `PostToolUse` (and related) hooks in `.claude/`
- Install and reload plugins (`/plugin`, `/reload-plugins`)
- Know what `--safe-mode` strips when customizations misbehave
- Choose settings scope: user vs project vs managed

---

## Notes status

Full lecture notes for this topic will be added next. Use the outline as the map.

## What this session covers

- **Official Definition:** A **hook** is automation that runs on Claude Code lifecycle events (tool use, session start, compact, …).
- **In Simple Words:** A security guard at the door — markdown in `CLAUDE.md` is a sign; a hook can actually stop the bag.
- Plugin marketplaces vs a repo-local plugin directory (`--plugin-dir`).
- Status line, output styles, `/config`.

⬅️ [Back to module](../)
