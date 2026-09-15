# Claude Code: Plan Mode, Worktrees, and Parallel Agents

## Context of This Session

In the **previous** session one agent shipped one PR. Real work is often **several** streams: plan first, then implement in an isolated **worktree**, then fan out with `/batch` or `claude agents`.

**In this session, you will:**

- Start and stay in **plan mode** until a written plan exists
- Use `claude -w` / `isolation: worktree` so experiments do not trash `main`
- Monitor background sessions with `claude agents`, `/tasks`, `/background`, `/fork`
- Know when `/batch` is worth the extra PRs — and when it is chaos

---

## Notes status

Full lecture notes for this topic will be added next. Use the outline as the map.

## What this session covers

- `Shift+Tab` vs `/plan [description]`.
- Agent view vs sub-agents vs agent teams.
- `/subtask` (result returns here) vs `/fork` (independent background copy).
- Cost: parallel agents multiply `/usage`.

⬅️ [Back to module](../)
