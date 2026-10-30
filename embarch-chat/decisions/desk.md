# embarch-chat decisions: Work items and the desk

**Status:** active, 2026-10-23.

Which threads a window lists, how a chat gets its work item, what its header shows, how the panel reaches the desk, and what it sends back. **The desk's own side** — the mailbox, the Desk's line per chat, the work item's notes — was decided here and moved to `embarch-desk` with its build (the last entry).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The routes: [`embarch-desk`'s interfaces](../../embarch-desk/interfaces.md).

### 9 — The thread list is the window's own desk's threads, by work item, waiting-on-you first

The desk whose repo the window's folder is in, else the open desk: every live session in its repos, terminal and Claude Code-panel ones too, plus its past chats, Untracked last; the fleet stays out through the desk's ignore list. **Rejected:** only the panel's own chats; every session on the machine (the fleet drowns the owner's few); the suite-wide open desk in every window (Start work opens a window per issue; `embarch-desk` decision 36 keeps a session on its own desk).

### 10 — A chat is on its work item before it starts

The + on a group starts on that item; the top + picks one (a card, an issue key, a new title, untracked). The extension chooses the session id, assigns it through the desk's existing `POST /sessions/{sid}/assign` (which creates a session the desk has not seen), then starts `claude --session-id`. **Rejected:** the hooks asking on every prompt (`embarch-desk` decision 7).

### 11 — Start work on the Desk opens a chat here and runs Promptu's pass on the issue (reversed by the owner, 2026-10-30)

`embarch-desk` decision 43's Enter press goes away while the desk's chat setting is on (4). The Desk opens the worktree's window as before and leaves a `start` entry in the mailbox (`embarch-desk` decision 46); the window whose folder matches takes it once and starts the chat on the item. **It sent the read-and-summarize starter until the owner reversed that on 2026-10-30** (prompt-first, `embarch-promptu` decision 16): the chat now runs Promptu's pass on `Work on KEY — title` with the item's brief as its `desk` source, the dialog opens over the empty chat, and the prompt waits in the draft, unsent (96). The entry keeps its `prompt` for chats and desks from before; when there is no Promptu prompt — Promptu off or not installed, or the pass failed or was skipped — that starter waits in the draft, unsent, for now (sending it as before is the owner's pick: `embarch-promptu` docs/forks.md, step 3). **Rejected:** an empty chat; a `vscode://` link to the extension (VS Code hands it to one window, which one is untested — `embarch-desk` decision 25 waits 4 s between links for this). **Rejected first, then the owner's call:** the prompt typed in and waiting — what happens now, with Promptu's prompt in place of the starter.

### 18 — A chat's header is its card in two lines

Key, title, status dropdown, PRs with their state, today's time, a link to the Desk card. **Rejected:** key and title alone, the full card folded in.

### 20 — The extension's Node side calls the desk directly; the list's live state comes from the desk alone

On `127.0.0.1:4891` with the token file; **the webview never holds the token** (`embarch-desk` decision 28 — a webview is a page). `GET /view` every 3 s while the list is visible — 15 s while hidden, for the waiting count (35) — already joins the hooks (instant) with the desk's own `claude agents` read every 30 s; the panel's own chats update from their streams. **Rejected:** `embarch-ui`'s proxy (nothing while the UI is down), an SSE route (a desk change to save 3 s), each window also running `claude agents` every 3 s (a 244 MB binary started 20 times a minute per window).

### 84 — Keep sends one of Claude's replies to the work item as a note

As a finding or a decision, through the desk's `POST /sessions/{sid}/line` (`embarch-desk` decision 48), held by the desk until a chat without an item gets one; the host takes the text from its own state, not from the webview. **Rejected:** a bookmark store (12), Keep on subagent steps.

### 32, 33, 40, 42, 43, 44, 45, 46, 47, 49 — The desk's side (moved 2026-10-23, see embarch-desk decisions 46–55)

Decided here and built in the desk, so their why now lives with the desk's: 33 is `embarch-desk` decision 46 (the mailbox), 32 is 47 (the Desk's line per chat and Open chat), and 40, 42, 43, 44, 45, 46, 47, 49 are 48–55 in that order (the work item gathers the work's knowledge; notes written unasked; notes and lines one stream; built on auto-memory; the hook captures them; the newest state on the card; the one-time import; notes in `state.json`).
