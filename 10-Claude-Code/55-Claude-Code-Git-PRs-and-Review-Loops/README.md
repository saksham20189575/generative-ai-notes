# Claude Code: Git, Pull Requests, and Review Loops

## Context of This Session

In the **previous** session you customized the **runtime**. This session is how work **leaves** the laptop: diffs, commits, GitHub reviews, and “fix CI” loops — without turning Claude into an unsupervised `git push --force`.

**In this session, you will:**

- Use `/diff`, `/code-review`, `/review`, `/security-review`, `/simplify`
- Install the GitHub app / `gh` flows (`/install-github-app`, `/web-setup`)
- Run `/autofix-pr` only when the team wants a cloud watcher on CI
- Write a review prompt that names **user-visible** risk for PMs

Official reference: [Commands](https://code.claude.com/docs/en/commands), [Code review](https://code.claude.com/docs/en/code-review), [Checkpointing](https://code.claude.com/docs/en/checkpointing).

---

## The Shipping Loop

Connecting sentence: Same as a human PR. Extra buttons. Same blame.

```text
plan → edit → /diff → /code-review → tests → commit → PR → /review → CI
```

- **Official Definition:** Claude Code can **review a diff in the terminal**, **comment on a GitHub PR**, and (on some plans) run a **cloud multi-agent review**. **Checkpoints** snapshot file edits Claude made in-session so `/rewind` can restore them.
- **In Simple Words:** `/diff` is “show me the pile.” `/code-review` is “find bugs in the pile.” `/rewind` is “Ctrl+Z for this chat’s file edits.” **Git** is still the history your teammates see.
- **Real-Life Example:** Ananya implements the leave-desk FAQ renderer. She does not push until `/diff` matches the plan and `/code-review` is quiet on correctness.

**Course rule:** no destructive git (`push --force`, `reset --hard` on shared branches, rewrite of `main`) unless the user **names** that command.

---

## Look Before You Commit

Connecting sentence: If you cannot narrate the diff, you are not ready to commit.

| Command | Job |
| --- | --- |
| `/diff` | Interactive uncommitted and per-turn diffs |
| `/code-review [effort] [--fix] [--comment] [target]` | Correctness **and** cleanup on a diff |
| `/simplify [target]` | Cleanup-only (reuse, simplify, efficiency) — **not** bug-hunting on current CLI |
| `/review [PR]` | Fast **read-only** GitHub PR review (pick from a list if no number) |
| `/security-review` | Diff vs default branch for common security issues |
| `/verify` | Run / observe the app, not only unit tests |

`/code-review` with no target: commits ahead of upstream **plus** uncommitted files. Pass a path, PR number, branch, or `main...feature`.

Effort: `low` … `max`, plus **`ultra`** (cloud, heavier). `/ultrareview` may appear as an alias depending on version.

```text
/code-review
/code-review --fix
/code-review 184
/code-review ultra
/review 184  Focus on user-visible copy and broken empty states.
```

`--fix` applies findings to the **working tree**. `--comment` posts inline GitHub comments. Cloud **GitHub App** review (org Code Review product) is separate: `@claude review` on the PR, Team/Enterprise, not ZDR orgs.

**PM review prompt** (paste after `/review <n>`):

```text
Ignore style nits. List: (1) user-visible behaviour changes,
(2) anything that could leak PII or secrets,
(3) what a Campus Ops person would see if this shipped today.
Cite file paths.
```

> **[ Student Activity ]**
>
> **Review card**
>
> You are Meera. `/review` returns 40 nits about import order. Write the **one sentence** you send next so the next pass is about users, not flake8.

---

## GitHub Wiring

Connecting sentence: Terminal review needs no app. PR comments and auto-fix do.

```text
/install-github-app
```

Walks repo selection, GitHub App install, optional Actions secrets. `gh` must be logged in for `/review`, `/autofix-pr`, and “open a PR” flows.

`/web-setup` (when offered) connects **Claude Code on the web** so a cloud session can watch the same repo.

Do not paste GitHub PATs into chat. Use `gh auth login` and the App flow.

---

## `/autofix-pr` — A Watcher, Not a Roommate

Connecting sentence: CI red is a loop. Decide whether a **cloud** agent is allowed to push.

```text
/autofix-pr
/autofix-pr only fix lint and type errors
```

- Detects the PR for the **current branch** (`gh pr view`)
- Spawns Claude Code **on the web**
- Watches CI failures and review comments; **pushes** when the fix is clear

Needs: `gh`, web access, GitHub App. To watch another PR, **check out that branch** first. Stop from the web CI bar or by telling Claude to stop watching.

**Team agreement:** autofix on **student forks** vs only on `dependabot` lint — write it down. Default “fix every comment” is noisy on design debates.

---

## Checkpoints vs Git vs Worktrees

Connecting sentence: Three undo buttons. People mash the wrong one.

| Mechanism | Undoes | Does **not** undo |
| --- | --- | --- |
| `/rewind` (`Esc Esc` on empty prompt) | Claude **Edit/Write** snapshots for this session (last ~100 turns) | Files changed **only** via Bash (`rm`, `mv`); most **sub-agent** edits; other people’s commits |
| `git checkout` / `git restore` | Anything **committed or staged** you name | Conversation text |
| Worktree (next topic) | Isolation so parallel agents do not share a dirty tree | Need to **merge** when done |

`/rewind` actions: restore **code + conversation**, conversation only, code only, or **summarize** from/to a message (like targeted `/compact`). Checkpoints are **not** a substitute for commits.

**Common mistake:** `rm` via Bash, then `/rewind`, then panic. Use **git**.

Aliases: `/checkpoint`, `/undo`.

---

## What Claude Should Not Do to Git

Connecting sentence: Same list as this course’s git safety protocol.

| Ask Claude to | Do not ask unless you name it |
| --- | --- |
| `git status`, `diff`, `log` | `git push --force` / `--force-with-lease` on shared branches |
| Draft a commit message **you** run | `git reset --hard` that throws away others’ work |
| `gh pr create` after you reviewed `/diff` | Rewrite `main` history |
| Amend **only** when hooks already rewrote the commit you just made and it is unpushed | Skip hooks (`--no-verify`) “to save time” |

Put the deny in **permissions** if the team wants it mechanical: `Bash(git push --force *)`, `Bash(git reset --hard *)`.

---

## End-to-End Mini Lab (This Notes Repo)

1. Make a tiny, reversible note edit on a **branch**.
2. `/diff` — write three bullets of what changed.
3. `/code-review` without `--fix`. Keep or reject each finding in one word.
4. Commit yourself (or ask Claude to **propose** the message). Do not force-push.
5. If `gh` works: open a draft PR and `/review` with the PM prompt above.
6. `/rewind` **conversation only** after a rambling debug — confirm files stayed.

Optional: `REVIEW.md` in the repo with “flag hardcoded secrets; ignore lecture-note line wrap.”

---

## Key Takeaways

- **`/diff` then `/code-review` then git.** Cloud `ultra` and GitHub App review are extras.
- **`/review` is for PMs** if you ask for user-visible risk. Default nits waste the room.
- **`/autofix-pr` pushes.** Treat it as production automation.
- **`/rewind` ≠ git.** Bash and sub-agents often need git to undo.

**Upcoming:** Topic 56 — **plan mode**, **worktrees**, and running **several** agents without colliding.

---

## Quick Reference — Important Commands, Files, and Terminologies

| Term / item | Meaning |
| --- | --- |
| `/diff` | See local changes |
| `/code-review` | Diff review; `--fix` / `--comment` / `ultra` |
| `/simplify` | Cleanup-only review (current CLI) |
| `/review [PR]` | Fast read-only GitHub review |
| `/security-review` | Security-oriented diff pass |
| `/verify` | Observe running behaviour |
| `/install-github-app` | GitHub App + optional Actions |
| `/autofix-pr` | Cloud watcher that can push |
| `/rewind` | Session checkpoint restore |
| Checkpoint | Snapshot of Claude file edits this session |
| `REVIEW.md` | Extra review guidance for App reviews |
| `@claude review` | Trigger org Code Review on a PR |

⬅️ [Back to module](../)
