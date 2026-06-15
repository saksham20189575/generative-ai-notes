# Version Control & GitHub — Lecture Notes

Session reference: why version control matters, Git locally, GitHub remotely, daily commands, branching, and collaboration.

**Outline:** Part I — Why VCS · Part II — Git, GitHub & setup · Part III — Local workflow (three areas) · Part IV — Undoing mistakes · Part V — Branching · Part VI — Remotes & collaboration (concepts) · Part VII — Remote workflows & access control · **Part VIII — End-to-end workflow (start here when you’re lost).**

---

## Part I — Why version control and core concepts

### 1. The Real-World Need for Version Control

Software development involves constant changes. Without a system to manage these changes, critical issues arise:

### a) Reverting to an Older Working Version
*   Adding new features can introduce bugs or be unnecessary later.
*   Without historical records, restoring a previous working state is impossible, making debugging difficult and affecting timelines.
*   **Problem:** How to reliably get back old code? Manual file copying is not professional.

### b) Collaborative Development Challenges
*   Teams modify the same files.
*   **Problems:** Overwriting work, no tracking of changes/authors, no conflict management, local-only storage risks.
*   **Problem:** How can multiple developers safely synchronize contributions?

<div align="center">

![Version control and collaboration](https://coding-platform.s3.amazonaws.com/dev/lms/tickets/8791fbc9-33ca-421b-ad68-a07d204fca84/qDCpbqCh13XUa0wH.png)

</div>

**Version Control Systems (VCS)** address these needs, ensuring code safety, proper history, and reliable teamwork.

---

### 2. What is Version Control?

A VCS is a software tool that manages changes to project files over time. It provides:
*   Tracking and storing every modification.
*   Reviewing change history (author, reasoning).
*   Restoring previous working versions.
*   Support for multiple contributors without overwriting.
*   Secure backups.

VCS enables systematic project evolution and prevents errors from becoming permanent.

---

### 3. How Version Control Works

VCS records project history as versions or snapshots. Each saved change creates a new version.
```
Version 1 → Version 2 → Version 3 → Version 4 → ...
(Stable)     (Bug)       (Fix)     (Feature)
```

<div align="center">

![How version control works](https://coding-platform.s3.amazonaws.com/dev/lms/tickets/ea91bbca-3caf-4d8e-b228-6f4b8380d69b/y2WUAoqPHCZheOkq.png)

</div>

Capabilities:
*   Move to any past stable version.
*   Compare versions to identify issues.
*   Selectively restore changes.
VCS acts as a project timeline, offering complete control over code evolution.

---

### 4. Version Control Analogy & Problems Solved

**Analogy:** Imagine writing a report and keeping multiple drafts (e.g., `draft1`, `draft2`). VCS automates this for code in a structured way: all versions stored permanently, changes reviewable/reversible, full traceability.

**Problems Solved by VCS:**
| Problem                                   | Impact                                 | VCS Solution                               |
| ----------------------------------------- | -------------------------------------- | ------------------------------------------ |
| Multiple disorganized file copies         | Confusion, wasted time                 | Automated, structured history              |
| Overwriting another teammate’s changes    | Lost work, conflicts                   | Safe merging process                       |
| No record of reasons behind modifications | Difficult maintenance, debugging       | Detailed commit history                    |
| System failure or accidental deletion     | Permanent loss of code                 | Easy recovery from repository              |
| Work stored only on a single machine      | Hard to continue if developer leaves   | Shared remote repository, distributed copies |
| Trying out a new feature                  | Risk of breaking stable code           | Use branches to isolate changes            |
| Debugging old issues                      | No clue where it went wrong            | Commit history reveals cause               |

Manual tracking methods are not suitable for professional development.

---

### 5. Types of Version Control Systems

VCS evolved in three forms:
### a) Local Version Control Systems
*   History on a single computer.
*   Only for individual projects; high data loss risk.
*   Example: RCS

### b) Centralized Version Control Systems (CVCS)
*   One central server stores project history.
*   Developers pull/push code from this server; network-dependent.
*   Examples: SVN, Perforce

### c) Distributed Version Control Systems (DVCS)
*   Every developer has a full copy of code and history.
*   Works offline; powerful collaboration (branching/merging).
*   Examples: Git, Mercurial (evolution towards distributed systems).

---

### 6. The Industry Standard: Git & GitHub

**Git** is the current global standard. Reasons for its popularity:
*   Faster and more flexible.
*   Full offline capability.
*   Efficient code collaboration, strong branching/merging.
*   Excellent security and data protection.

**GitHub** is a popular cloud-based platform for hosting Git repositories and enabling team collaboration.

<div align="center">

<img src="https://coding-platform.s3.amazonaws.com/dev/lms/tickets/6000a753-18b7-4a8b-bb7c-efd1aa3535dc/OkTPYUmUaszfEXKe.png" alt="Git versus GitHub" width="400" />

*Clarification: Git is the tool; GitHub is the service.*

</div>

---

### 7. Key Takeaways & Reflection

*   Version Control is essential for professional software development.
*   It safeguards code integrity and ensures productivity.
*   It supports teamwork, history tracking, and problem recovery.
*   Git is the global standard for managing source code versions.

**Mini Reflection:** How do you currently track different file versions, restore old code, or collaborate safely on shared code? Version Control provides a clear, reliable, and industry-approved solution.

---

## Part II — Git, GitHub, and environment setup

### 1. Source Code Management Tools
Teams use SCM tools to manage changing code. Many exist, categorized as centralized or distributed.

| Tool Name          | Nature            | Description                                  |
| ------------------ | --------------- | -------------------------------------------- |
| SVN, Perforce      | Centralized     | Single central repository                    |
| Git, Mercurial     | Distributed     | Full history on every developer’s machine    |
| Azure DevOps / TFS | Centralized/Cloud | Microsoft ecosystem for repo + project mgmt  |

Git is the most widely adopted due to its advantages.

### 2. Why Git is Standard
*   Works **offline** (full history locally)
*   **Fast** operations (commits, comparisons)
*   **Strong branching** and merging
*   **Secure** (built-in integrity checks)
*   Large **community** and open-source ecosystem
*   Integrates with cloud platforms (GitHub, GitLab)

Git facilitates safe experimentation and efficient teamwork.

### 3. What is Git?

<div align="center">

![Local version control on your machine — commits stay in your repo until you push](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/session06/session06-local-vs-remote.png)



</div>

Git is a **local command-line tool** for version control on your machine.
It's used for:
*   Tracking project changes
*   Recording versions via commits
*   Creating branches for new ideas
*   Merging contributions

### 4. What is GitHub?

<div align="center">

<img src="https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/session06/session06-local-vs-remote.png" alt="Local workspace vs shared remote: same idea as left and right of the diagram above" width="480" />



</div>

GitHub is a **cloud platform** for hosting Git repositories and enabling teamwork.

Its purpose includes:
*   Project backup and online storage
*   Collaboration (pull requests, code review)
*   Issue tracking, CI/CD
*   Showcasing developer contributions

| Aspect           | Git                        | GitHub                  |
| ---------------- | -------------------------- | ----------------------- |
| Runs where?      | Local system               | Cloud website           |
| Internet needed? | No                         | Yes                     |
| Purpose          | Version history management | Collaboration + Hosting |

### 5. Create GitHub Account (Mandatory Pre-Setup)

Create your GitHub profile using your **full professional name** and the **exact email** you'll use for Git configuration. This ensures proper commit attribution.

*   **Steps:**
    1.  Go to [github.com/signup](https://github.com/signup).
    2.  Sign up and verify your email.
    3.  Choose a clear username.

### 6. Install Git

Install Git based on your OS.

### Windows
*   Download installer from [git-scm.com](https://git-scm.com/download).
*   Use **default options**. Git Bash is included.

### macOS
*   Via Homebrew: `brew install git`
*   Or Xcode Command Line Tools: `xcode-select --install`

### Linux (Debian/Ubuntu)
*   `sudo apt update`
*   `sudo apt install git`

Verify: `git --version`

<div align="center">

![git --version output](https://coding-platform.s3.amazonaws.com/dev/lms/tickets/ee796583-5e7f-48c7-86d6-585278c363f2/CGnV2pb3SKxRvGEh.png)

</div>

### 7. Basic Git Setup

Configure Git with your identity, matching your GitHub account:

```bash
git config --global user.name "Exact GitHub Name"
git config --global user.email "YourGitHubEmail@example.com"
```

Verify settings: `git config --list`

**Why matching identity is crucial:**
*   Ensures your contributions are correctly counted on your GitHub profile.
*   Maintains clear ownership and accountability in team projects.
*   Mandatory even for local-only work.

---

To understand how Git tracks project changes, you must learn how files move through Git's **three core areas** and how commands like `add`, `status`, `commit`, `log`, and `diff` help you manage versions efficiently.

---

## Part III — Local workflow: working tree, staging, and commits

### 1. Git file lifecycle — the three-area model

<div align="center">

<img src="https://coding-platform.s3.amazonaws.com/dev/lms/tickets/07d42e41-6c25-4883-8b81-04fcc2c94420/UMQizQ3zQGscDIJV.png" alt="Git file lifecycle: working directory, staging area, and repository" width="520" />

<img src="https://coding-platform.s3.amazonaws.com/dev/lms/tickets/a73fee3f-caa3-4940-a088-4c8b9ed67a4f/EYu3AONtxsf2yZtI.png" alt="Git areas and file states" width="520" />

</div>

Git manages files through **three logical locations**:

#### A. Working directory (workspace)

This is your project folder on your machine.

Contains:

- New files
- Edited files
- Deleted files

Git **does NOT track** anything here until you stage it.

---

#### B. Staging area (index)

Temporary holding area before committing.

Purpose:

- Prepare a clean snapshot
- Select _which_ files should go into the next commit
- Avoid committing unwanted changes

Files enter staging using:

```bash
git add <file>
```

---

#### C. Local repository

Stores **commits**, which are _permanent snapshots_ of your project.

Once committed:

- Changes become part of history
- A unique commit ID is generated
- You can revert or compare later

---

### 2. Checking the current state — `git status`

Use this command constantly.

```bash
git status
```

It tells you:

- Which files changed
- Which are staged
- Which are unstaged
- Whether your branch is ahead/behind

Example output:

```bash
Changes not staged for commit:
  modified: index.html

Changes to be committed:
  new file: style.css
```

---

### 3. Adding files to staging — `git add`

#### Add a single file

```bash
git add file.txt
```

#### Add multiple files

```bash
git add file1.js file2.js
```

#### Add everything in the folder

```bash
git add .
```

#### Add only modified files (not deleted/new)

```bash
git add -u
```

Purpose of staging:

- Gives control
- Lets you commit only what you need
- Helps create clean, logical commits

---

### 4. Creating a commit — `git commit`

A **commit** is a permanent snapshot of staged changes.

### Basic commit:

```bash
git commit -m "Meaningful commit message"
```

### Commit messages MUST:

- Start with a verb → _Add, Update, Fix, Remove_
- Be short but descriptive
- Use present tense
- Avoid vague words like “changes”, “fixes”, “stuff”

### Examples of good messages:

- `Add navbar component`
- `Fix login validation issue`
- `Update README with setup instructions`

Bad examples:

- `done task`
- `changes made`
- `final commit`

---

### 5. Viewing commit history — `git log`

See full commit details:

```bash
git log
```

Shows:

- Commit ID
- Author
- Date
- Commit message

### Condensed view:

```bash
git log --oneline
```

Example:

```bash
a1b2c3d Add user login API
f4e5d6a Setup project structure
```

Perfect for quick history checks.

---

### 6. Comparing changes — `git diff`

Git provides powerful comparison tools.

---

#### A. Compare working directory vs staging area

```bash
git diff
```

Shows **unstaged** edits.

---

#### B. Compare staging area vs last commit

```bash
git diff --staged
```

Shows what you’re _about to commit_.

---

#### C. Compare two commits

```bash
git diff <commit1> <commit2>
```

---

#### How to read diff output

```bash
- lines removed
+ lines added
```

Diffs help you review before committing.

---

### 7. Full workflow example

### Step-by-step:

1. Edit a file
2. Check status

   ```bash
   git status
   ```

3. Stage it

   ```bash
   git add app.js
   ```

4. Review staged changes

   ```bash
   git diff --staged
   ```

5. Commit it

   ```bash
   git commit -m "Add route handler for login"
   ```

6. View commit history

   ```bash
   git log --oneline
   ```

---

### 8. Summary table

| Area / Command        | Purpose                         | When to Use                  |
| --------------------- | ------------------------------- | ---------------------------- |
| **Working Directory** | Where edits happen              | Anytime you modify files     |
| **Staging Area**      | Prepare changes for commit      | When changes are ready       |
| **Repository**        | Permanent version history       | After commit                 |
| `git status`          | View current file states        | Frequently                   |
| `git add`             | Move changes to staging         | Before committing            |
| `git commit`          | Save staged changes permanently | After reviewing              |
| `git log`             | See history                     | After commits                |
| `git diff`            | Compare changes                 | Before staging or committing |

---

To work confidently with Git, you must understand how to safely **undo mistakes** at different stages of the file lifecycle. Git provides commands to revert working directory changes, unstage staged changes, and modify the latest commit.


---

## Part IV — Undoing and correcting mistakes

### 1. Undoing working directory changes — `git restore`

<div align="center">

![Using git restore to discard working tree changes](https://coding-platform.s3.amazonaws.com/dev/lms/tickets/a0520db6-384b-4a0e-baf9-7abc56bb0d7b/rRcGtpdhLbJIJfta.png)

</div>

`git restore` discards uncommitted edits, restoring files to their last committed version.

*   **Restore a single file:** `git restore file.txt` (e.g., `git restore config.js` to revert local edits).
*   **Restore everything:** `git restore .` (discards all uncommitted changes across the project).

### 2. Unstage changes — `git reset` or `git restore --staged`

Staged changes can be moved back to the working directory without losing edits.

*   **Unstage a single file:**
    *   `git reset file.txt` (e.g., `git reset debug.log` to unstage, file remains modified).
    *   `git restore --staged file.txt` (equivalent to `git reset`, e.g., `git restore --staged index.js`).
*   **Unstage everything:** `git reset` (moves all staged files back to working directory, edits intact).

### 3. Amending the last commit — `git commit --amend`

Correct the most recent commit's message or content.

*   **Change commit message:** `git commit --amend -m "Correct message"` (e.g., fix `Addd login page` to `Add login page`).
*   **Add missing changes:** Stage missing files (`git add styles.css`), then `git commit --amend`. (e.g., `git add validation.js` then `git commit --amend`).

### What this does
*   Rewrites the last commit
*   Updates commit message or contents
*   Generates a new commit ID

### Important
*   Safe only before pushing
*   Avoid rewriting public/shared history

### 4. Understanding file lifecycle when undoing changes

| Stage             | Action Type        | Correct Command                                         |
| ----------------- | ------------------ | ------------------------------------------------------- |
| Working Directory | Discard edits      | `git restore file.txt`                                  |
| Staging Area      | Unstage file       | `git restore --staged file.txt` or `git reset file.txt` |
| Repository        | Modify last commit | `git commit --amend`                                    |

### 5. Common mistake scenarios and solutions

*   **"I made changes but want to discard them."**
    `git restore file.txt` (e.g., `git restore app.js`)
*   **"I added files by mistake."**
    `git reset file.txt` (e.g., `git reset backup-old.js`)
*   **"I forgot to include something in the last commit."**
    `git add missing.js` then `git commit --amend` (e.g., `git add login.test.js` then `git commit --amend`)
*   **"My commit message is incorrect."**
    `git commit --amend -m "Refactor authentication module"`
*   **"I want to review my changes before undoing anything."**
    Working directory diff: `git diff`
    Staged diff: `git diff --staged`

### 6. Summary table

| Command                | Purpose                           | Stage Affected    |
| ---------------------- | --------------------------------- | ----------------- |
| `git restore file`     | Discard working directory changes | Working Directory |
| `git restore --staged` | Unstage changes                   | Staging Area      |
| `git reset file`       | Unstage changes (alternative)     | Staging Area      |
| `git commit --amend`   | Modify last commit                | Repository        |
| `git diff`             | View unstaged changes             | Working Directory |
| `git diff --staged`    | View staged snapshot              | Staging Area      |

---

## Part V — Branching

### 1. Ideal scenario — why branching is needed

In a real-world setup, a stable application exists on `main`. New features, bug fixes, and experiments are developed concurrently.

If all work happens directly on `main`:
- Incomplete features can break the application.
- Bugs may reach production.
- Parallel work becomes risky.
- Code history is difficult to manage.

Branching solves this by isolating work.

<div align="center">

![Branches isolate work from main](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/python-lectures/session06/session06-branch-timeline.png)

</div>


---

### 2. What is a branch in Git

A **branch** is a lightweight pointer to a commit representing an independent line of development.

- Each branch has its own commit history.
- Changes in one branch do not affect others.
- `main` is the default stable branch.

---

### 3. Isolated development using branches

Branches provide isolation between different types of work.

Benefits:
- Feature development without risk.
- Bug fixes without blocking others.
- Experiments without fear.
- Stable and clean `main` branch.

Each branch acts like a separate workspace.

---

### 4. Viewing existing branches — `git branch`

List all local branches:

```bash
git branch
```

The current branch is marked with `*`.

### Example output:

```bash
* main
  feature-login
  bugfix-header
```

---

### 5. Creating branches — `git branch`

Create a new branch without switching to it:

```bash
git branch feature-login
```

- Branch is created.
- You remain on your current branch.

---

### 6. Switching branches — `git checkout` / `git switch`

#### A. Switch to an existing branch

```bash
git checkout feature-login
# or
git switch feature-login
```

All new work now belongs to `feature-login`.

---

#### B. Create and switch in one command

```bash
git checkout -b feature-signup
# or
git switch -c feature-signup
```

---

### 7. Working in an isolated branch

Once inside a branch:
- Edit files.
- Stage changes.
- Commit changes.

### Example workflow:

```bash
git switch feature-login
git add login.js
git commit -m "Add login form UI"
```

These changes are isolated from `main`.

---

### 8. Branch naming conventions

Clear naming improves collaboration and maintenance.

#### Recommended patterns

| Purpose    | Example Branch Name    |
| ---------- | ---------------------- |
| Feature    | `feature-login`        |
| Bug Fix    | `bugfix-navbar`        |
| Hotfix     | `hotfix-payment-issue` |
| Experiment | `experiment-ui-layout` |

### Rules:

- Use lowercase letters.
- Use hyphens.
- Avoid generic names like `test`, `new`, `temp`.

---

### 9. Deleting branches — `git branch -d`

Once a branch has served its purpose, it should be deleted.

#### A. Delete a merged branch (safe)

```bash
git branch -d feature-login
```

Deletes the branch only if it is fully merged.

---

#### B. Force delete an unmerged branch

```bash
git branch -D experiment-old-ui
```

Use only when the branch is no longer needed.

---

### 10. Branch cleanup (best practices)

Branch cleanup keeps the repository manageable and readable.

Why cleanup is important:
- Avoids clutter.
- Reduces confusion.
- Prevents working on outdated branches.
- Keeps branch list meaningful.

#### Recommended cleanup process

1. Merge branch into `main`.
2. Delete the local branch.
3. Ensure no unused branches remain.

### Example cleanup flow:

```bash
git switch main
git branch -d feature-login
```

---

### 11. Understanding branch lifecycle

| Stage              | Description                    |
| ------------------ | ------------------------------ |
| Branch creation    | New line of development begins |
| Active development | Commits added in isolation     |
| Merge (next topic) | Changes integrated into main   |
| Cleanup            | Branch deleted after use       |

This lifecycle is followed in professional projects.

---

### 12. Summary table

| Command                  | Purpose                    |
| ------------------------ | -------------------------- |
| `git branch`             | List all local branches    |
| `git branch <name>`      | Create a branch            |
| `git checkout <name>`    | Switch to a branch         |
| `git checkout -b <name>` | Create and switch branch   |
| `git switch <name>`      | Switch branch (modern)     |
| `git switch -c <name>`   | Create and switch (modern) |
| `git branch -d <name>`   | Delete merged branch       |
| `git branch -D <name>`   | Force delete branch        |

---

### 13. Key takeaway

Branches enable safe, parallel, and structured development. Equally important is **branch cleanup**, which ensures repositories remain clean and maintainable.

---

To collaborate using Git, teams rely on **remote repositories**. Git handles local history; remotes provide a shared, centralized location for synchronization, review, and control.


---

## Part VI — Remotes and collaboration (concepts)

### 1. Git and GitHub — roles
*   **Git:** Local version control system. Tracks changes, commits, branches. Works on your machine, no internet needed.
*   **GitHub:** Remote hosting platform for Git repositories. Provides shared online location, collaboration features (permissions, PRs, reviews, issues).
*   **Simply:** Git controls *how code changes*; GitHub controls *how people collaborate*.

### 2. Remote Repository
A **remote repository** is a Git repository **stored outside your local machine**, typically on a server like GitHub.
*   **Purpose:** Shared source of truth, sync work, backup history, enable collaboration.
*   Every developer has a local repo; the remote is the common meeting point.

### 3. Local & Remote Interaction
Work happens locally first: edit files, commit changes. Nothing is shared automatically.
*   Remote is updated when you **push** your commits.
*   Local receives others' work when you **pull** or **fetch** from the remote.
*   **Benefits:** Offline work, controlled sharing, isolated local mistakes.

### 4. Meaning of “origin”
*   `origin` is the conventional name for the **primary remote repository**.
*   It's a shortcut name. Projects can have multiple remotes.
*   View remotes: `git remote -v`

### 5. Repository (Repo) Definition
A repository is a structured container holding:
*   Source code, commit history, branches/tags
*   Configuration and documentation
*   **Forms:** Local (on your machine) vs. Remote (on GitHub). Remote enables teamwork.

### 6. Creating & Cloning on GitHub
*   **Creating on GitHub:** Establishes a remote project location, defines ownership/access. The repo exists only in the cloud initially.
*   **Cloning:** Creates a local copy of a remote repository.
    ```bash
    git clone <repository-url>
    ```
    Cloning downloads files, copies full history, and automatically connects local to the remote as `origin`.

### 7. Synchronizing with Remote
Explicit commands for synchronization:
*   **Pull:** Brings changes *from remote to local*.
*   **Push:** Sends changes *from local to remote*.
    ```bash
    git pull origin main
    git push origin main
    ```
    Controlled sync prevents accidental overwrites.

### 8. Collaboration Models
*   **Collaborators (Direct Model):** Contributors added to team-owned repositories. They have direct access to push branches/commits. For internal teams/trusted contributors.
*   **Forking (Independent Model):** Used when direct push access is not granted. Creates a new remote repository under the contributor's account, independent from the original. Original repo remains protected.

### 9. Pull Requests (PRs)
A Pull Request is a **request to merge changes into a remote repository**. PRs exist entirely on GitHub.
*   **Purpose:** Code review, discussion, approval control, merge tracking.
*   Connects one branch to another, or a fork to its original repository.

### 10. Pull Request Review Workflow
*   Reviewers examine changes, provide feedback.
*   **Approve:** Code is ready to merge.
*   **Request Changes:** Blocks merging until issues are resolved. Ensures quality control.

### 11. End-to-End Collaboration Flow
1.  Remote repository on GitHub.
2.  Developers clone or fork.
3.  Work locally.
4.  Push changes to remote.
5.  Pull Request created.
6.  Code reviewed.
7.  Approved changes merged.
8.  Remote repository updates.
9.  Local repositories sync again.
This cycle is continuous in professional teams.

---

## Part VII — Remote workflows and access control

### 1. Creating a remote repository
Collaboration starts with a **remote repository** (e.g., GitHub). It's a centralized host for project code, defines ownership, and enforces collaboration rules. Initially, it exists only on GitHub, defining access rules remotely. It is the **single source of truth**.

### 2. Cloning a remote repository
`git clone <URL>` creates a **local working copy**. It downloads all files, copies full commit history, and configures `origin`. Developers work locally, with the remote as the shared reference.

### 3. Connecting an existing local repository to a remote — `git remote add`
To link a local repo to a remote: `git remote add origin <URL>`. This registers the remote (named `origin`) but doesn't push code. They are **connected but not synchronized**.

### 4. Pushing code to a remote repository
`git push origin main` transfers local commits to the remote. This uploads commits, updates the remote branch, and makes changes visible. Pushing is explicit.

### 5. Upstream branches and `git push -u`
`git push -u origin main` sets an **upstream branch**, linking your local branch to the remote. This simplifies future `git push`/`git pull` commands and reduces repetition.

### 6. Pull vs fetch — understanding synchronization
- **`git fetch origin`**: Downloads remote changes but doesn't alter local branches. A safe inspection.
- **`git pull origin main`**: Fetches changes then immediately merges them. Remember: `git pull = git fetch + git merge`. Understand this to avoid unintended merges.

### 7. Collaboration through branches and pull requests
Professional teams work on feature branches, push them to the remote, and open Pull Requests for review, rather than pushing directly to `main`. This keeps shared branches stable.

### 8. Pull requests as a collaboration contract
A Pull Request (PR) is a **formal request to integrate changes**. It explains changes, enables review, records decisions, and controls merges. PRs exist only on the **remote platform**.

### 9. Repository access control and why it matters
Remote repos are shared. **Access control defines who can interact and how** (e.g., push, review, merge, manage settings). It's enforced **only on the remote platform**.

#### 9.1 Why access control is essential
Without access control: risks of breakage, deletions, and no accountability. With it: protected `main` branch, mandatory reviews, clear responsibilities. It's the foundation of **trust and safety**.

#### 9.2 Types of repository access (role-based)
GitHub uses **role-based access**:
- **Read**: View/clone.
- **Write**: Push code, open PRs.
- **Maintain**: Manage PRs, merge.
- **Admin**: Full control.
Roles intentionally restrict actions to minimize risk.

#### 9.3 How access control is enforced
GitHub checks user identity, role, and action permission. If permission is missing (e.g., for push, merge, settings), the action is immediately rejected.

#### 9.4 Adding collaborators (GitHub process)
To add collaborators on GitHub: Go to **Settings > Collaborators & Teams > Add Collaborator**, enter username/email, select permission, send invitation. Collaborator must **accept**.

#### 9.5 Modifying or removing access
Admins can change or revoke collaborator access immediately, protecting the repository from outdated permissions.

#### 9.6 Access control and pull requests
Access control impacts PRs: who can open, approve, and merge them. This separates contribution from decision-making, ensuring shared branch stability.

### 10. Typical end-to-end collaboration flow
Typical flow: remote repo creation, role assignment, cloning, feature branches, local commits, push, PRs, reviews, merge, team sync. All governed by remote access rules.

---

## Part VIII — End-to-end workflow (anchor)

**Use this section when you ask: “What exact steps do I follow in real life?”** The parts above explain *why* and *how each command works*; this part is the **single happy path** most beginners follow on a team.

### One rhythm to remember

```bash
git clone <repo-url>
cd <repository-folder>

git switch -c feature-login
# Make your changes in the editor and save files.

git add .
git commit -m "Add login feature"
git push -u origin feature-login
# In the browser: open the repo on GitHub → Create Pull Request
# (feature-login → main). Request review → merge after approval.
```

- **`git push -u origin feature-login`** links your local branch to the remote the first time you push it; later you can often use just `git push` on that branch.
- **Pull Request** is not a Git command — you create it on GitHub (or similar). It is how your team reviews and merges your branch safely.

### Before you start a new piece of work (habit)

```bash
git switch main
git pull origin main
git switch -c feature-your-next-task
```

That keeps your starting point aligned with the shared `main` branch.

### Where each step is explained in these notes

| Step in the rhythm | Deeper detail |
| ------------------ | ------------- |
| Clone / `origin` | Part VII §2 · Part VI §6 |
| Branch / `git switch -c` | Part V |
| `git add` / `git commit` | Part III |
| `git push` / `push -u` | Part VII §4–5 |
| Pull Requests & review | Part VI §9–11 · Part VII §7–10 |

If something goes wrong, use **Part IV** (undo / unstage / amend) before you push; after you push, coordinate with your team instead of rewriting history on your own.