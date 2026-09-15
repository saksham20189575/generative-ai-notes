# Claude Code: Security, Cost, and Enterprise Managed Settings

## Context of This Session

By now the agent can edit code, call MCP, and spawn sub-agents. This session is the **governance layer**: what IT can enforce, what you must never put in git, and how to read `/usage` before the bill becomes a story.

**In this session, you will:**

- Separate **CLAUDE.md advice** from **enforced** `permissions.deny` / sandbox
- Read org **managed settings** vs user vs project precedence
- Budget with `/usage`, `--max-budget-usd` (print mode), model/`/effort` choices
- Apply a secret-handling checklist (`.env`, MCP OAuth, heap dumps)

---

## Notes status

Full lecture notes for this topic will be added next. Use the outline as the map.

## What this session covers

- Managed `CLAUDE.md` vs `permissions.deny` (reminder from Topic 51).
- `--restricted` / `--safe-mode` for evals and incident response.
- `/privacy-settings`, `/heapdump` (do not share — contains conversation + credentials).
- Links back to Module 9 governance notes.

⬅️ [Back to module](../)
