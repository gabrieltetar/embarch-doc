# Proposal: picking up an issue, and Claude sessions on the Desk

**Status:** proposal, 2026-10-22.

Spans `embarch-desk`, `embarch-ui` and the `embarch-desk` Claude Code plugin, which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). Shaped with the owner in four rounds of questions on 2026-10-22.

## Why

Picking up an issue today is a run of hand steps — find it, make a clone or worktree on the right branch, move the issue, open VS Code, paste the issue into Claude — and once several chats run, nothing shows which is waiting on the owner. The owner wants to **pick an issue on the Desk and land in a ready VS Code session**, and to **see the live chats from the Desk and answer them**.

## What Claude Code allows (its docs, read 2026-10-22)

- **No documented way lets an outside process type into a chat open in a VS Code panel.** `vscode://anthropic.claude-code/open?prompt=…` pre-fills and never submits; `?session=<id>` opens or focuses a session belonging to the window's workspace.
- **`claude agents --json` lists live sessions** — interactive ones too [measured 2026-10-22] — with `status` (`busy`, `waiting`, `idle`) and `waitingFor` (`permission prompt`, `input needed`, …).
- **Hooks give the rest**: `Stop` carries `last_assistant_message`; `Notification` says a session waits on the user.
- **Remote Control** puts every interactive session — VS Code included — on claude.ai/code and the phone, once `remoteControlAtStartup` is on; permission prompts and questions can be answered there. **A third-party app cannot be its client**, so the Desk links to it.
- **Cross-session messages** reach any local session's inbox, but from a script the format is undocumented, they arrive as another session's message rather than the user's, and they can approve nothing. **Rejected for this** (below).

## What the owner chose (2026-10-22)

**Picking up an issue**

1. **From a pick-up list or from a card.** The Desk lists the owner's open issues in the open desk's Linear scope that have no card yet, plus search; every list row and every card has **Start work**.
2. **Start work sets up**: the card (if new); **the issue moved to In Progress**; a **git worktree beside the main clone** — `<project folder>/<repo>-<issue key>`, the pattern the owner's per-feature clones already follow — **on Linear's branch for the issue, checked out if it exists locally or on the remote, else branched from the fresh remote default branch**.
3. **Then it opens the worktree in VS Code with the first prompt pre-filled; the owner presses Enter.** The prompt asks Claude to **read and summarize** the issue, its description, comments and PR, then wait for the first real instruction. The session lands on the card by the existing launch claim (desk decision 25).
4. **Any number of sessions per issue**, all on its card.
5. **Sessions the Desk opens run in auto mode**: Claude Code's classifier approves routine actions and blocks risky ones.

**The live chats**

6. **Every card lists its sessions**: name, busy / waiting (and for what) / idle, and what each last said.
7. **Answer → the session on claude.ai/code** (phone too), through **Remote Control, turned on for every session** (`remoteControlAtStartup` in the owner's user settings). Answers there are the owner's own input, permission prompts included.
8. **Jump → the session in VS Code**: the worktree's window, focused on that chat.
9. **No always-on Claude window.** A fresh session starts from VS Code; nothing has to sit idle relaying.

**Finishing**

10. **The session drafts the PR**, and it waits on the Desk like any draft (desk decision 30) until the owner sends it; **the issue moves to In Review when its PR opens**; **the worktree is removed when the PR merges**, asking first if it holds uncommitted work.

## Shape

### `embarch-desk`

- **Pick-up list**: `GET /pickup` — `linear_my_issues` in the open desk's scope minus issues with cards; Linear's `branchName` per issue.
- **Start work**: `POST /items/{id}/start` — status move to In Progress; `git worktree add` from the card's repo (else the desk's first firmware repo) on the issue's branch; `.claude/settings.local.json` with `"defaultMode": "auto"` written in the worktree and kept out of git through the repo's `info/exclude`; the launch claim; returns the two `vscode://` links.
- **Sessions per card**: `claude agents --json` read on the sync clock, joined to the desk's own session records by `sessionId`; `Stop` and `Notification` hooks add the last reply and what it waits for. A session's Remote Control link is `claude.ai/code/<id>`.
- **PR draft**: a `github_pr` draft kind (title, body, head branch); Send opens the PR through the GitHub API. A merged PR's worktree is removed on the next sync after asking.

### The plugin

- The `Stop` and `Notification` hooks forward to the desk (they already run `embarch-desk hook`).
- A skill line: when the user asks for a PR, draft it with the desk's PR tool.

### `embarch-ui`

- The pick-up list above the cards; Start work on rows and cards; per-card session rows with Answer and Jump; the PR draft in the Drafts area.

## Rejected, and why

- **Typing into a chat from the Desk through the session's inbox socket**: the script-side format is undocumented, a message arrives as another session's rather than the owner's, and it cannot answer a permission prompt — Remote Control does all three properly.
- **Starting sessions in the background (`claude --bg`)**: it would start without a click, but the owner wants to land in VS Code and drive.
- **An always-on dispatcher window, like the fleet's listener**: only needed if a fresh session could not be started otherwise.

## Order of work

1. **Remote Control on for every session** — one user setting; already approved.
2. **Pick-up and Start work**: the list, the worktree, the status move, the VS Code links. About half a day.
3. **Sessions on cards**: the join of `claude agents --json` and the hooks, Answer and Jump. About two hours.
4. **Finishing**: the PR draft kind, In Review, worktree removal. About half a day.
5. **Fold** into the desk's and the UI's docs; delete this file.

## Open questions

- **Is `claude.ai/code/<id>` the local session id, or a remote one?** The docs name the URL's id the session id without saying which; to check on the first live session, falling back to the claude.ai/code list.
- **A worktree for a repo whose build lives in a west workspace** (the project's firmware sits under a manifest repo): does the worktree need its own `west update`, or share the main clone's modules? To settle on the first Start work.
- **Which repo a card starts in** when a desk has several (the firmware repo, the manifest repo): the card's own, else the desk's first — a picker if that proves wrong.
