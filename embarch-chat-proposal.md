# Proposal: the owner's own Claude chat, in VS Code

**Status:** proposal, 2026-10-22.

Spans `embarch-chat` (new: what [`embarch-promptu`](embarch-promptu/design.md) becomes, below), `embarch-desk` and `embarch-ui`, which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). Shaped with the owner in rounds of questions from 2026-10-22. **Not built: building waits for the owner's go.**

## The ask

A Claude Code chat of the owner's own — "its own Claude Code chat basically, with improvements tailored to my needs" — so that a chat can be started, seen and answered from EmbArch itself instead of handing off to claude.ai (`embarch-desk` decision 44).

## What is possible (measured 2026-10-22)

**An EmbArch-owned process can hold a multi-turn Claude Code session on the owner's own login, over the wire Claude Code's own panel uses.** That panel's process runs `claude --input-format stream-json --output-format stream-json --verbose --permission-prompt-tool=stdio --resume=<id> --setting-sources=user,project,local --permission-mode=auto --replay-user-messages`, one per open chat. The wire is partly documented, but Anthropic's panel depends on it; the SDK wants an API key. Each of these worked, on Haiku, for about $0.17 in all:

- **Control requests in:** `interrupt` (the turn ends at once, the session goes on), `set_permission_mode`, `set_model`, `rename_session`, `get_context_usage` (tokens by category).
- **Asked out, answered in:** `can_use_tool` for every permission prompt, for `AskUserQuestion` (answered by adding `answers`) and for `ExitPlanMode` (the plan in its input; allowing it leaves plan mode).
- **User messages:** `/command args` expands, and `system/init` lists every command; `/compact` compacts; `@file` is inlined by the CLI itself; image blocks are seen.
- **Flags:** `--include-partial-messages` streams deltas; `--resume <id>` after exit keeps context; `--session-id <uuid>` fixes the id up front; `--prompt-suggestions` guesses the next prompt ("go ahead"); `--no-session-persistence` leaves no transcript.
- **Around it:** `claude agents --json` (0.2 s) lists the chat as `interactive`; a subagent's messages carry `parent_tool_use_id`; Claude titles every session itself (an `ai-title` line, renewed as it goes); **transcripts are deleted after 30 days** (`cleanupPeriodDays` unset; the oldest here is 2026-09-23).

**Memory:** 457 MB resident for a full session, 242 MB stripped; a background Bash task dies with its process.

## Decided

Numbers are permanent, grouped by topic.

### Shape

**1 —** **It lives in a VS Code panel**, an extension of EmbArch's own, beside the code.

**2 —** **It replaces the Claude Code panel for the owner's work.** VS Code stays for reading and editing code, and any chat can still open in Claude Code's panel.

**3 —** **What pulls hardest:** it knows its **work item** and starts briefed; it carries the owner's **prompt library** as one-click actions; **every thread at a glance**, waiting-on-you first; **bench-aware**; **atlas integration**.

**4 —** **Tomorrow's workflow does not wait for it**: Start work opens the Claude Code panel (`embarch-desk` decision 43) until this exists.

**6 —** **`embarch-promptu` becomes `embarch-chat`**: one new repo for the extension and the library, the sub-project count unchanged; promptu's three planned pieces become library entries. Decision 1 sets `embarch-ui` decision 3's "no webview" aside for this extension only. **Rejected:** inside `embarch-desk` (firmware prompts in a time-tracking repo), growing `embarch-ui`'s launcher (sessions in the hardware UI's repo), a sub-project beside promptu.

**29 —** **`embarch-ui`'s launcher moves into `embarch-chat`'s extension**: one sideloaded extension, so the silent drop a VS Code server update causes costs one reinstall. 436 lines move once. **Rejected:** two extensions, and one script reaching across both repos.

**23 —** **It ships whole**, as the desk's v1 did (`embarch-desk` decision 21). **Rejected:** the library first (usable in Claude Code's panel at once), the panel first.

### Sessions and windows

**5 —** **The extension runs each chat's `claude` process**, one per open chat, with the official panel's flags; a closed chat comes back with `--resume`. Chats die with their window, and **a chat belongs to the window that started it**. **Rejected:** the desk service hosting them (browser answering and surviving a reload, for 600–900 lines of Rust in a work-item service), a process per message (startup every turn, background tasks killed).

**31 —** **A thread another window or a terminal runs is read-only here, with Jump.** Every window shows the same list; a foreign thread opens from its transcript, and Jump brings up the window or terminal running it. Windows share nothing. **Rejected:** taking a chat over (a lock file per session), one daemon running every chat (decision 5's rejected hosting again).

**35 —** **A chat waiting on the owner off screen shows as a count** on the activity-bar icon and a status-bar item ("2 waiting") in every window; a click opens the oldest. No pop-ups. **Rejected:** a VS Code toast per wait, Claude's own phone push (untested for these chats).

**30 —** **The panel runs the `claude` on `PATH`** (2.1.287 here, as the desk and terminals do), overridable in a setting. **Rejected:** the official extension's bundled binary (2.1.308 here), whose path changes with every extension update.

**22 —** **A new chat starts in auto mode on the owner's default model**, as the official panel and Start work's worktrees do; both switch per chat. **Rejected:** ask mode, a mode and model per desk.

**12 —** **Nothing new is stored, and Haiku names each chat.** The transcript is Claude's; session → item is the desk's. The assistant's call after the first turn (25) also returns a name, set with `rename_session`, so the official panel's history shows it too. **Transcripts keep Claude Code's 30 days**: older chats leave the list; the desk keeps their time and lines. **Rejected:** an index of the extension's own; chat records in the desk; `--name` from the first prompt (every Start work chat "Read the issue…"); the key beside Claude's own `ai-title`; keeping a year (`cleanupPeriodDays: 365`, about 18 GB at 1.5 GB a month); copying an archived item's transcripts into the desk.

### Work items and the desk

**9 —** **The thread list is the window's own desk's threads, by work item, waiting-on-you first** — the desk whose repo the window's folder is in, else the open desk: every live session in its repos, terminal and Claude Code-panel ones too, plus its past chats, Untracked last; the fleet stays out through the desk's ignore list. **Rejected:** only the panel's own chats; every session on the machine (the fleet drowns the owner's few); the suite-wide open desk in every window (Start work opens a window per issue; desk decision 36 keeps a session on its own desk).

**10 —** **A chat is on its work item before it starts.** The + on a group starts on that item; the top + picks one (a card, an issue key, a new title, untracked). The extension chooses the session id, assigns it through the desk's existing `POST /sessions/{sid}/assign` (which creates a session the desk has not seen), then starts `claude --session-id`. **Rejected:** the hooks asking on every prompt (`embarch-desk` decision 7).

**11 —** **Start work on the Desk opens a chat here and sends the prompt** — `embarch-desk` decision 43's Enter press goes away. The Desk opens the worktree's window as today and leaves the start in the mailbox (33). **Rejected:** the prompt typed in and waiting; an empty chat; a `vscode://` link to the extension (VS Code hands it to one window, which one is untested — desk decision 25 waits 4 s between links for this).

**32 —** **The Desk shows each chat as one line — state, what it waits for, age — and an Open chat button**, which brings up its window with the thread open through the mailbox, resuming it there if the window has closed; a terminal session gets Jump. **This replaces `embarch-desk` decision 44's Answer and last reply.** **Rejected:** Remote Control's Answer (the hand-off the ask ends), adding the title and the last reply, a bare dot.

**33 —** **The desk is the panel's mailbox.** Start work and Open chat leave a request — start a chat on an item, in a folder, with a prompt; or focus a session — and the window whose folder matches takes it on its next poll, once: `embarch-desk` decision 25's launch claim extended to the panel, **a pending list and a route, the desk's one addition**. **Rejected:** a `vscode://` link (11).

**18 —** **A chat's header is its card in two lines**: key, title, status dropdown, PRs with their state, today's time, a link to the Desk card. **Rejected:** key and title alone, the full card folded in.

**20 —** **The extension's Node side calls the desk directly** on `127.0.0.1:4891` with the token file; **the webview never holds the token** (`embarch-desk` decision 28 — a webview is a page). The list polls `claude agents` and `GET /view` every 3 s while visible; the panel's own chats update from their streams. **Rejected:** `embarch-ui`'s proxy (nothing while the UI is down), an SSE route (a desk change to save 3 s).

### Matching Claude Code's panel

**8 —** **Day one: approve, stop and stream; diffs; @-file mentions.** Permission prompts, Stop, streamed text, the mode switch. **Claude's questions and a plan's approval count as approve** — on the wire both are permission requests — and show as forms, with options and previews or the plan. An Edit or Write shows as a diff and opens VS Code's diff editor on a click. @ completes a workspace path, with the selected lines, and the CLI inlines it. **Also day one:** a context meter in the header with a Compact button, and a subagent's steps nested under its call. **Later:** pasted images (measured working), rewind.

**17 —** **The list sits left, the chat right**: the list behind its own activity-bar icon, the chat in the secondary sidebar where Claude Code's panel is, any chat also openable as an editor tab. **Rejected:** both stacked on the right (the list folds away), every chat a tab (chats compete with code).

**21 —** **The webview is Preact bundled with esbuild**, in VS Code's theme variables: an event stream feeding a constantly changing UI renders better from state than by hand-patched DOM. About 4 KB. **Rejected:** plain DOM (`embarch-ui` decision 2's posture), React (about 140 KB).

### The library

**7 —** **An entry is a Claude Code command or skill**, a `.md` file with frontmatter: it works in the terminal, the official panel and the fleet, and gets its work item from `desk_whoami`, so nothing is templated. **Rejected:** panel-only templates with `{{issue}}` placeholders (usable nowhere else), a button file choosing which commands show (a second file to keep in step).

**13 —** **The library is two folders**: generic entries in a plugin in the public `embarch-chat` repo; **an entry naming a client, a client project or a client internal in `~/.claude/commands`, never in a repo**. Both become buttons. **Rejected:** the public plugin only, the open firmware repo's commands too (the client team's, not the owner's).

**14 —** **It is seeded from the owner's past prompts, and the owner cuts.** 682 prompts in 145 local transcripts; the only exact repeats are one-word replies (done ×20, continue ×15, yes ×12, go ×11, push ×7), so one `claude -p` groups them by intent and drafts entries, each ✓ or ✕; about $0.30 on Sonnet [assumed]. **Rejected:** promptu's three then add-as-you-go, starting empty.

**38 —** **Entries sit behind a 💡 by the input, one submenu per category**, beside the Haiku assistant's suggestions ([its proposal](embarch-chat-assistant-proposal.md)); context handling is one category. **Rejected:** a `/` list plus a pinned row, a toolbar of every entry, the `/` list only.

**39 —** **promptu's two install pieces become commands that apply them**: `/embarch-permissions` and `/embarch-claude-md` show what they would write into the open repo (`settings.local.json`, `CLAUDE.md`) and write it on a yes — never silent (`embarch-umbrella` decision 12). **Rejected:** leaving them to umbrella's `init`, template files copied by hand.

### Bench and atlas

**15 —** **Bench results show as cards**: an `embarch-api` build, flash, bootload, study or `serial_log` result becomes pass or fail, board, first error, steps passed and a link into `embarch-ui`, from the tool result already in the stream. **Rejected:** a live bench strip polled from Core (a second `embarch-ui`), plain output.

**16 —** **Atlas citations become links**: `atlas-use` cites every hardware fact as `<doc_id> p<N>` or `<board>:<ref>`, and each opens that page or the entry in `embarch-ui`'s Atlas tab. **Rejected:** a hardware pane for the open file (a second Atlas tab), plain text.

### The Haiku assistant

Split into [embarch-chat-assistant-proposal.md](embarch-chat-assistant-proposal.md): decisions 19, 24–28, 34 and 36 — ghost text, cards, reply chips, when it runs and what it sees.

## Order of work

One build (23), about three days in all [estimate]:

1. **The repo**: Preact and esbuild, the launcher moved in, a reinstall script. About two hours.
2. **The chat**: process, resume, streamed rendering, approve, stop, mode switch, question and plan forms. About a day with step 3.
3. **The desk**: the thread list, binding before start, the header, and **the mailbox, with the Desk's Start work and Open chat writing to it** (11, 32, 33) — the one desk-side change.
4. **Inline**: diffs, @-mentions, bench cards, atlas links. About half a day.
5. **The library**: the plugin, the seeding run the owner cuts, the buttons. About half a day.
6. **The Haiku assistant** ([its proposal](embarch-chat-assistant-proposal.md)). About half a day.
7. **Fold**: `embarch-promptu/` becomes `embarch-chat/`; amend `embarch-ui` decision 3, `embarch-desk` decisions 21, 43, 44 and spec §5, [embarch.md](embarch.md) §3, the roadmap, the features and DOC-PROTOCOL §2; the new repo's `CLAUDE.md`; delete this file.

## Open questions

- **Does Remote Control reach a chat the extension started?** Not needed at the desk (32), but it is the only way in from the phone, and nobody has opened one from claude.ai yet.
- **When does an idle chat's process close?** At 457 MB each — say after 30 idle minutes unless a background task runs, with `--resume` on the next message.
