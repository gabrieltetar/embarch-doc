# embarch-chat decisions: Processes, windows and transcripts

**Status:** active, 2026-10-23.

Who runs a chat's `claude`, which window owns it, how long it lives, what survives a reload, which `claude` it is, what is stored and what a workspace may not change.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 5 — The extension runs each chat's `claude` process

One per open chat, with the official panel's flags; a closed chat comes back with `--resume`. **A chat belongs to the window that started it**, and chats die with their window — a real close; a reload brings back the chats on screen (63). **Rejected:** the desk service hosting them (600–900 lines of Rust in a work-item service), a process per message (startup every turn, background tasks killed).

### 31 — A thread another window or a terminal runs is read-only here, with Jump

Every window shows the same list; a foreign thread opens from its transcript, and Jump brings up the window or terminal running it. Windows share nothing. **A past chat is offered for resume only when `claude agents` shows nothing running it**, so the panel never runs `--resume` beside a terminal still on that session. **Rejected:** taking a chat over (a lock file per session), one daemon running every chat (decision 5's rejected hosting again).

### 35 — A chat waiting on the owner off screen shows as a count

On the activity-bar icon and a status-bar item ("2 waiting") in every window, the chat on screen left out; a click opens the oldest. No pop-ups. (VS Code builds the list lazily, so the icon's count appears once the list has been opened; the status bar always shows it.) **Rejected:** a VS Code toast per wait, Claude's own phone push (untested for these chats).

### 80 — A turn that ends off screen leaves its chat unread until the owner looks

A green dot in the list, and on the tab the mark with an amber dot (waiting) or a green one (finished unread), in the palette's colours (53), never over the mark's red. Mark as Unread is in the palette and on right-click; the mark survives a reload. Unread joins no count (35). **Rejected:** unread in the badge or the status bar (Claude Code's badge counts only waiting sessions), toasts.

### 41 — A chat's process does not outlive its use

It closes 5 minutes after the later of the last input and the last reply, unless a background task runs, it waits on the owner or a Remote Control bridge the owner turned on (83), and the next message resumes it — one sent while it is closing waits for the resumed process. **The 5 minutes stand on the process's cost** (457 MB resident for a full session [measured 2026-10-22]), **not on the prompt cache**: the cache lives on the server, not in the process, and every recorded reply writes the **1-hour** cache [measured], so whether the next message reads it is the status line's to say (69). It was first argued as Claude's default 5-minute cache lifetime ([reversals](../../embarch-decision-reversals.md) row 115). **A full resume is cheap: ready in 0.66 s, first token at 1.46 s** [measured]. **Rejected:** 30 or 1 idle minutes, the end of each turn, a cap per window, never.

### 30 — The panel runs the `claude` on `PATH`

As the desk and terminals do, overridable in a setting; **outside the versions a panel release was tested with (2.1.287–2.1.322) it warns in one line and keeps working**. **Rejected:** refusing to start chats on an untested version (a CLI auto-update could lock the owner out), no guard; the official extension's bundled binary (2.1.308 when this was built), whose path changes with every extension update.

### 22 — A new chat starts in auto mode on the owner's default model

As the official panel and Start work's worktrees do; both switch per chat. **Rejected:** ask mode, a mode and model per desk.

### 12 — Nothing new is stored, and Haiku names each chat

The transcript is Claude's; session → item is the desk's. The assistant's call after the first turn (25) also returns a name, set with `rename_session`, so the official panel's history shows it too. **Transcripts keep Claude Code's 30 days** (`cleanupPeriodDays` unset): older chats leave the list; the desk keeps their time and lines. **The one exception is a chat's login** (106), kept for a `claude` wrapper to read. **Rejected:** an index of the extension's own; chat records in the desk; `--name` from the first prompt (every Start work chat "Read the issue…"); the key beside Claude's `ai-title`; keeping a year (about 18 GB); copying an archived item's transcripts into the desk.

### 75 — A hand-given name wins and is Claude's own record

`rename_session` while the process runs, else the same `custom-title` line Claude Code writes, so nothing new is stored (12). Haiku names no hand-named chat or fork; a thread run elsewhere is not renamed (31). **Rejected:** names kept by the extension or the desk, Haiku renaming a named chat.

### 48 — Nothing a workspace controls can redirect the panel

Every path or address setting is machine-scoped, so a repo's `.vscode/settings.json` cannot point the desk URL or token path elsewhere and have a one-line file such as Claude's credentials sent as a token; the desk client calls only loopback; an untrusted workspace does not run the extension. **And only the owner's own pick untracks a chat**: a resume asks the desk for its item and never sends `untracked`, which would clear its time spans.

### 101 — A window's login and desk come from the machine's settings, by folder

Someone with two Claude subscriptions runs both at once. `embarchChat.logins` names them, each with an optional `configDir` set as `CLAUDE_CONFIG_DIR`; `embarchChat.desks` names desks other than the default, each with an `env` set on the chat's processes; `embarchChat.folderRules` gives a folder its default login and desk. With more than one login the status bar shows the window's, with the account signed in to it (106), and picks it for new chats, kept in the workspace's state. **The picker moves only the login**, since a desk holds a folder's work. All three are machine-scoped, so 48 still holds. A chat reads its environment once, when it is created, and **keeps that login for life**, across idle closes (41) and resumes (106). The assistant and Promptu spawn their own processes, and take the window's login as a chat does. A desk's `env` values have `~/` expanded, because nothing else would and the desk's tools read them as paths.

The panel still calls `claude agents` and `claude --version` in its own environment, so a login's folder links `sessions` to keep the first finding every chat's process. Rejected: reading the login from a workspace setting (a repo could then spend another account), and one setting per window (a folder's account does not change, and it would be picked again in each new window).

### 63 — A reload brings back the chats on screen; an interrupted step continues only on a click

With everything the owner typed. The restored chat keeps its mode, model and effort (a fork takes its parent's; a past chat opened from the list takes its transcript's mode, else Ask), an editor tab its unsent draft, its queued messages come back above the input — or into the draft with a one-line note when the CLI cannot take them (images, a held `/compact` rest, rerun limits) — and a chat cut off mid-turn shows "Continue the interrupted step", which resumes it with the CLI's own `CLAUDE_CODE_RESUME_INTERRUPTED_TURN` under Claude Code's limits (at most 2 reruns, none for a step over an hour old, checked again at the click) [measured]. VS Code cannot tell a reload from a close, so a window back within 90 s counts as a reload, and **nothing reruns by itself**: on this bench an unasked rerun can be a flash or a study. Amends 5 for reloads only. `embarchChat.continueAfterReload` on offers Continue; off, the chats return without it. **Rejected:** Claude Code's automatic rerun, restoring a chat in auto mode whatever its mode was, restoring after a real close, resending the last prompt.

### 103 — An agent can hand its chat to a fresh session in the same panel

Decided by the owner, 2026-11-07 (EMB-61); **built 2026-11-09** (embarch-chat task 007), unit-tested against a fake CLI, not seen in a live panel. The panel's own MCP server (65) carries a `handoff(prompt)` tool in every chat, so the server is declared whenever the handoff is on, not only with `embarchChat.diagnosticsTool`. `embarchChat.handoff` (machine scope): `card`, the default, shows the prompt editable with Continue in a fresh session and Stay, and Stay answers the tool so the agent carries on; `immediate` switches at once; `off` declares no tool. Continue ends the chat's `claude` and starts a fresh one in the same panel, the prompt its first message, below a divider naming the handoff; the timeline above stays, and the fresh session keeps the chat's mode, model, effort and work item. **Amends 36's rejection of a fresh chat opened unasked**; 63 still holds, since this carries on work the owner started rather than rerunning a step. **As built:** the fresh session is a new `claude` session in a new chat record on the same item (`startChat` on the old chat's cwd, work item and mode, then its model, effort and Ultracode carried over), and the panel that showed the old chat is re-pointed at it, tab or sidebar; the old history is copied into the fresh chat's timeline, so after a reload the fresh chat shows only its own transcript, and the old session stays on the list. **Rejected:** a fenced `handoff` block in a reply (one that quotes a block would start it), the desk's tools and mailbox (two repos and processes for one panel's act), a new tab (the old panel would be left showing the ended chat, and the owner would have two views to reconcile), a fresh session in a looser mode.

### 105 — A due login is refreshed by one warm-up, alone

Decided by the owner, 2026-11-09 (EMB-91). Every `claude` that finds the login's OAuth token due (within 5 minutes of expiry; it lasts 8 hours) takes one refresh lock in the login's folder, stale after 60 s, and **a non-interactive CLI tries five times, 1–2 s apart, then ends the turn** with "Failed to refresh OAuth token: another Claude Code process is refreshing it…" [read from CLI 2.1.287]. A chat's first message starts its own process and Haiku's at once (26), and a keystroke kills a Haiku call: on 2026-11-09, just after boot, the first message and the naming call failed that way. **Which process held the lock is not known**; a slow refresh and a kill mid-refresh both fit, and this answers both.

The window reads only `expiresAt` from `<configDir>/.credentials.json`. While it is due, **one warm-up runs first and is never cancelled**, a stripped Haiku call (`claude auth status` does not refresh [measured 2026-11-09]). A chat's process spawns after it, waiting at most 60 s, with what was sent meanwhile held behind its `initialize`; the assistant starts no call. No file (an API key, the macOS keychain): nothing waits. **A turn that still ends on that error** warms up again until the login is fresh, then sends the owner's message again, once, if no step ran in the turn, nothing was sent since and the chat has not ended with its issue (104). **Rejected:** `CLAUDE_CODE_DISABLE_AUTH_REFRESH_LOCK=1` (refreshes race for one refresh token); letting cancelled Haiku calls finish (paid per keystroke, no help for a slow refresh); a timer before each expiry (fires in every open window).

### 106 — One pick decides a window's login for every panel in it, and a chat keeps its login on resume

Decided by the owner, 2026-11-11 (EMB-161). Claude Code's panel starts `claude` through a wrapper that chose the login by folder alone, so the status item and the panel beside it disagreed; the item named a label, which said nothing once a `/login` had put one account in both logins' folders; and a chat resumed in the panel on the other login spent that login's quota until its 5-hour limit. **The window mirrors its pick, the logins' folders and each chat's login into `~/.config/embarch-chat/logins.json`**, which the wrapper reads: a resumed session's login on record, else the longest picked folder holding its working folder, else its own rule, recording a session it finds none for. A chat's login goes on record when it is created, a fork's and a handoff's taken from the chat they carry on, and it resumes on that login; with no record it takes the window's and records it. Viewing records nothing. **The item shows the account in the login's folder**, with a warning while two logins hold one. Two windows on one folder: the last picked or focused wins. With one login nothing is written.
