# embarch-desk decisions: Picking up an issue, and the chat's side

**Status:** active, 2026-10-23.

Start work, live sessions on a card, and what `embarch-chat` added: the mailbox and a line per chat.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

Shaped as `embarch-desk-sessions-proposal.md` on 2026-10-22 and built the same evening; its finishing half (the PR, In Review, removing the worktree) is still proposed there.

### 43 — Start work: a worktree on the issue's branch, the issue moved, VS Code with the prompt typed in
From the **pick-up list** (the user's open issues in the open desk's scope with no card, or a search) or any issue card. It **moves the issue to In Progress — forward only**, never back from started, done or canceled; makes a **worktree beside the main clone**, `<repo>-<issue key>`, on **Linear's branch for the issue** — the worktree already holding that branch is reused, a remote branch is tracked, otherwise it branches from the fresh remote default; **a folder of that name not on the branch is never touched**; writes **auto mode** into the worktree's `.claude/settings.local.json`, kept out of git through the repo's shared `info/exclude`; claims the next session there for the card (25); and opens the worktree in VS Code, then the Claude panel with a **read-and-summarize prompt typed in. The owner presses Enter** — nothing documented submits a VS Code chat from outside. **With the chat setting on** (`chat_panel`, off by default), it instead leaves a `start` entry for the worktree in the mailbox (46) and answers without the prompt link, and `embarch-chat` opens the chat there and sends the prompt itself (`embarch-chat` decision 11). The card's own repo is the main clone when it is one, else the desk's first. **Rejected:** starting a background session (`claude --bg`) with no click — the owner wants to land in VS Code and drive.

### 44 — Each card lists its live sessions; Jump is VS Code
State comes from `claude agents --json`, which lists interactive sessions too [measured 2026-10-22, also from the service's own environment]: busy, waiting (and for what), idle. The `Stop` hook adds the last reply, `Notification` what a session waits for. **Answer** opened `claude.ai/code/<session id>` — **Remote Control is on for every session** (`remoteControlAtStartup` in the owner's user settings, 2026-10-22), where answers are the owner's own input, permission prompts included — until 47 replaced it and the last reply with one line per session; **Jump** opens the session's folder in VS Code, then the session. **Rejected: typing into a chat from the Desk through the session's inbox socket** — from a script its format is undocumented, a message arrives as another session's rather than the owner's, and it cannot approve anything.

### 45 — No always-on Claude window
A fresh session starts from VS Code; nothing has to sit idle relaying, unlike the fleet's listener.

## The chat's side

Shaped as `embarch-chat` decisions 33 and 32 in `embarch-chat-desk-proposal.md` on 2026-10-22, built the next night and deployed 2026-10-23; the proposal is folded and deleted.

### 46 — The desk is `embarch-chat`'s mailbox
Start work and Open chat leave a request — start a chat on an item, in a folder, with a prompt; or focus a session — and the window whose folder matches takes it on its next poll, once: decision 25's launch claim extended to the panel, **a pending list and a route, the desk's one addition**. An entry expires after 10 minutes, as a launch claim does. **A `start` entry is written only by Start work, server-side**: a route that let a caller supply the prompt would let any page that reaches the desk run one in auto mode, so `POST /mailbox` takes `focus` only. **Rejected:** a `vscode://` link (`embarch-chat` decision 11).

### 47 — The Desk shows each session as one line, with Open chat for a chat the panel runs
State, what it waits for, age. **Open chat**, on a session `embarch-chat` runs, brings up its window with the thread open through the mailbox (46), resuming it there if the window has closed; every other session gets Jump (44). **A card keeps its ended `embarch-chat` sessions**, so Open chat can resume one. **This replaced 44's Answer and the last reply.** **Rejected:** Remote Control's Answer (the hand-off `embarch-chat` exists to end), adding the title and the last reply, a bare dot.
