# Proposal: the desk's side of the owner's Claude chat

**Status:** proposal, 2026-10-22.

What `embarch-desk` and its Desk tab gain for the owner's own Claude chat, split from [embarch-chat-proposal.md](embarch-chat-proposal.md) at its size cap. **Decision numbers are shared with it** and stay permanent; this part ships with the rest (decision 23). Not built: building waits for the owner's go.

## Decided

**11 —** **Start work on the Desk opens a chat here and sends the prompt** — `embarch-desk` decision 43's Enter press goes away. The Desk opens the worktree's window as today and leaves the start in the mailbox (33). **Rejected:** the prompt typed in and waiting; an empty chat; a `vscode://` link to the extension (VS Code hands it to one window, which one is untested — desk decision 25 waits 4 s between links for this).

**33 —** **The desk is the panel's mailbox.** Start work and Open chat leave a request — start a chat on an item, in a folder, with a prompt; or focus a session — and the window whose folder matches takes it on its next poll, once: `embarch-desk` decision 25's launch claim extended to the panel, **a pending list and a route, the desk's one addition**. **Rejected:** a `vscode://` link (11).

**32 —** **The Desk shows each chat as one line — state, what it waits for, age — and an Open chat button**, which brings up its window with the thread open through the mailbox, resuming it there if the window has closed; a terminal session gets Jump. **This replaces `embarch-desk` decision 44's Answer and last reply.** **Rejected:** Remote Control's Answer (the hand-off the ask ends), adding the title and the last reply, a bare dot.

**40 —** **The work item is where the work's knowledge gathers, and a chat pulls it from the desk.** At start a chat knows its item and that **the desk holds everything about it** — the issue and its comments, PRs, sessions, tile lines, bench activity, and **the notes taken about the work done locally**, which today scatter across files and transcripts and belong on the item instead. **One desk tool returns it all** — the issue with its latest comments, PRs, sessions, notes, bench activity — newest first, cut at about 4K tokens; nothing is pasted in up front. **Rejected:** the SessionStart brief growing to about 1K tokens of issue text for every session; key and title only, with `linear_get_issue` as the one way in; a brief the panel puts before the first message; an index first, then a call per kind; notes only, with the issue left to `linear_get_issue`.

**42 —** **Notes are written by the chats, unasked, and the owner cuts** — too many rather than too few, as tile lines already are (`embarch-desk` decision 13). **Rejected:** notes only when asked; Haiku extracting them after every turn (a call per turn, seeing only the last reply).

**43 —** **Notes and tile lines are one stream.** A tile line is a note of kind "done", and **what goes to Harvest is the summary of that day's notes**, in the owner's words; `desk_add_line` gains a kind rather than a second tool appearing. **Rejected:** two streams (cleaner billing text, but two tools and two places to look).

**44 —** **Notes build on what Claude Code's auto-memory already does.** On the owner's current client project the agent keeps, unprompted, a dated state file per issue — 16 of that project's 58 memory files are named by issue key, each holding the branch, commits, PR and what is pending [measured 2026-10-22]. The owner's call: capitalize on that habit rather than invent a new one. **Rejected:** a log by kind written through a new tool, one living document per item, a log plus a summary.

**45 —** **The desk's hook captures them.** The PostToolUse hook already runs on every tool call; a Write or Edit inside a `memory/` folder becomes a note on the session's work item, with the file's new text. The agent changes nothing, the file stays its own copy, and **the session decides the item, not the file's name**. **Rejected:** the desk's skill telling sessions to keep issue state with a desk tool (it competes with Claude Code's built-in memory rule); the desk scanning memory files by issue key (misses the 42 of 58 not named by key, and knows no session).

**47 —** **The per-issue memories written before capture are attached once**: on first run the desk gives each memory file whose name or text holds an item's issue key to that item as its starting state. Harvest summarizes only a day's own notes, so no past entry changes. **Rejected:** starting fresh.

**46 —** **A card shows each note's newest state; a click opens the full list.** **Rejected:** the newest with earlier versions folded under it, every change as its own line.
