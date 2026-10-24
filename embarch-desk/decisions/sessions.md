# embarch-desk decisions: Picking up an issue

**Status:** active, 2026-10-23.

Start work, live sessions on a card, and no always-on window.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

Shaped as `embarch-desk-sessions-proposal.md` on 2026-10-22 and built the same evening; its finishing half (the PR, In Review, removing the worktree) is still proposed there.

### 43 — Start work: a worktree on the issue's branch, the issue moved, VS Code with the prompt typed in
From the **pick-up list** (the user's open issues in the open desk's scope with no card, or a search) or any issue card. It **moves the issue to In Progress — forward only**, never back from started, done or canceled; makes a **worktree beside the main clone**, `<repo>-<issue key>`, on **Linear's branch for the issue** — the worktree already holding that branch is reused, a remote branch is tracked, otherwise it branches from the fresh remote default; **a folder of that name not on the branch is never touched**; writes **auto mode** into the worktree's `.claude/settings.local.json`, kept out of git through the repo's shared `info/exclude`; claims the next session there for the card (25); and opens the worktree in VS Code, then the Claude panel with a **read-and-summarize prompt typed in. The owner presses Enter** — nothing documented submits a VS Code chat from outside. The card's own repo is the main clone when it is one, else the desk's first. **Rejected:** starting a background session (`claude --bg`) with no click — the owner wants to land in VS Code and drive.

### 44 — Each card lists its live sessions; Answer is Remote Control, Jump is VS Code
State comes from `claude agents --json`, which lists interactive sessions too [measured 2026-10-22, also from the service's own environment]: busy, waiting (and for what), idle. The `Stop` hook adds the last reply, `Notification` what a session waits for. **Answer** opens `claude.ai/code/<session id>`, with **Remote Control on for every session** (`remoteControlAtStartup` in the owner's user settings, 2026-10-22), where answers are the owner's own input, permission prompts included; **Jump** opens the session's folder in VS Code, then the session. **Rejected: typing into a chat from the Desk through the session's inbox socket** — from a script its format is undocumented, a message arrives as another session's rather than the owner's, and it cannot approve anything.

### 45 — No always-on Claude window
A fresh session starts from VS Code; nothing has to sit idle relaying, unlike the fleet's listener.
