# Claude Code: MCP, Tools, and Permission Modes

## Context of This Session

In the **previous** session you packaged playbooks as **skills** and specialists as **sub-agents**. Those specialists still need **tools**: file edits, bash, and **MCP** servers (Jira, Slack, browsers, internal APIs).

This session treats tools as a **permission design**, not as “turn everything on.”

**In this session, you will:**

- Map built-in tools (`Read`, `Edit`, `Bash`, …) vs **MCP** tools
- Use `/mcp`, `/permissions`, and `--permission-mode`
- Write allow / ask / deny rules that a PM can explain
- Connect a first MCP server without pasting secrets into chat

---

## Notes status

Full lecture notes for this topic will be added next. Use the outline as the map.

## What this session covers

- **Official Definition:** **MCP (Model Context Protocol)** is a standard way to plug external tools and data into the agent as servers.
- **In Simple Words:** USB ports for Claude — Jira is a printer; the browser is a camera.
- Permission modes from Topic 50, expanded: `default`, `plan`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`.
- `settings.json` `permissions.allow` / `deny`, `/fewer-permission-prompts`.
- `--allowedTools` / `--disallowedTools` for scripts (`claude -p`).

⬅️ [Back to module](../)
