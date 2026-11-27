# embarch-chat: interfaces

**Status:** active, 2026-10-30.

Reference: the settings, commands, keys and views the extension contributes; how it runs `claude`; what it asks the desk; what the page is handed. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

## Settings

**Every setting is machine-scoped** (decision 48): VS Code takes it from the user settings, or in a WSL window from the Remote [WSL] settings (`~/.vscode-server/data/Machine/settings.json`), never from a workspace's `.vscode/settings.json`. In a WSL window a value in the local user settings does not apply.

| Setting | Default | Meaning |
|---|---|---|
| `embarchChat.chatLocation` | `editor` | Where a chat opens: an editor tab of its own, or `sidebar` for the secondary sidebar (92) |
| `embarchChat.claudePath` | `claude` | The `claude` each chat runs (30) |
| `embarchChat.idleMinutes` | `5` | How long an idle chat's process lives (41) |
| `embarchChat.deskUrl` | unset: `http://127.0.0.1:` + `EMBARCH_DESK_PORT`, else 4891 (124) | The desk; `127.0.0.1`, `::1` or `localhost` only, else nothing is sent |
| `embarchChat.deskTokenPath` | unset: `desk-token` in the desk's config folder (124) | The desk's bearer token |
| `embarchChat.assistant` | `true` | The Haiku assistant: ghost text, cards, chips, naming. Off, the instant prefix match and the CLI's own suggestion remain |
| `embarchChat.startupProbe` | `true` | One short `claude` per login and folder fills a chat's settings menu before its first message (108). Off, they show once the chat's own runs |
| `embarchChat.showMessageTimestamps` | `false` | A time to the second over each message, a date line where the day changes (68) |
| `embarchChat.autosave` | `true` | Save an open file's unsaved changes before Claude reads, edits or writes it (61) |
| `embarchChat.continueAfterReload` | `true` | A chat cut off by a reload offers Continue, never by itself (63) |
| `embarchChat.diagnosticsTool` | `false` | Give Claude `getDiagnostics`, the Problems panel (65) |
| `embarchChat.handoff` | `card` | Claude's `handoff(prompt)`: `card` asks, `immediate` switches at once, `off` declares no tool (103); `immediate` also starts a chat's Limits menu with Automatic handoff on, the chat's switch then deciding (109) |
| `embarchChat.continueAfterSessionLimit` | `true` | A new chat's Limits menu: continue on its own once the 5-hour limit that cut a turn off resets (109) |
| `embarchChat.continueAfterWeeklyLimit` | `false` | The same, for a weekly limit, all models' or one model's (109) |
| `embarchChat.continueMessage` | `continue` | What a chat sends on its own at a limit's reset; each chat's menu can change it (109) |
| `embarchChat.attachOpenFile` | `true` | The open file goes with each message; off, a file goes only with selected lines (60) |
| `embarchChat.attachSelection` | `true` | The selected lines go with each message; off, `@` still inserts them (60) |
| `embarchChat.atlasPath` | `embarch-atlas` | The atlas CLI the linker reads sections with, on PATH by default; not found or no atlas, no section line, one log line (114) |
| `embarchChat.promptuPath` | `promptu` | Promptu's CLI, on PATH by default; not found, the Promptu icon stays dark and Enter sends as before (95, 96) |
| `embarchUi.host` / `embarchUi.port` | `127.0.0.1` / `4890` | Where `embarch-ui.service` serves, for the launcher's probe (102); also the Desk link, bench-card links and a step's card, study and board links (87) |

## Views, commands and keys

**Views:** an activity-bar container, *EmbArch Chat*, holding the **Threads** webview; each chat opens as an editor tab, and what it opens goes into that tab's group (92); with `chatLocation` = `sidebar`, a secondary-sidebar container holds the **Chat** webview and any chat also opens as a tab (17). Status bar, right: **EmbArch** (new chat, 54), **N waiting** (35) and, with more than one login, the **login item**: the window's login and the organisation, else the email, signed in to its folder, the full account in its tooltip, `$(warning)` and the labels named while two logins hold one account (101, 106).

**Commands** (`embarchChat.*`): New Chat, Pick Login for New Chats (101), Open Chat in Editor, Open the Oldest Waiting Chat, Refresh Threads, Show Log, Mark as Unread, Rename Chat, Focus Chat Input, Leave Chat Input, Insert @-Mention of the Selection, Reopen Closed Chat Tab; in a pending diff tab Accept the Kept Changes, Reject the Change, Reject or Keep This Change (64); on a plan tab Add Comment, Remove Comment, Send the Comments and Keep Planning (77). `embarchUi.*`: EmbArch UI: Start, Stop, Restart, Open in Browser, each driving `embarch-ui.service` (102).

**Keys** (59): Ctrl+Alt+Esc focuses the input from an editor (with lines selected, as an @-mention) and again leaves it; Alt+Shift+K inserts `@path#L10-24` at the input's caret; Ctrl+Shift+T reopens the last closed chat tab when a chat tab was the last closed, else VS Code's own reopen.

**The rail** (94): Usage alone at the top (99), then Memory, Promptu, Library, Suggestions, the 💬 side question and the settings gear (107) at the bottom of the left edge, each a one-colour SVG in `currentColor`; Usage's and Promptu's cards on hover (95, 99). **In the input:** `/` completes the session's commands and the library, `@` workspace paths and terminals; with Promptu's icon lit Enter runs the pass, and in its dialog Enter answers a page, Ctrl+Enter accepts every recommendation, Esc stops with the rest as assumptions (96); while the 💡 or 📚 shows, ↑/↓ focus a row, ←/→ change category, Enter or Tab picks the focused row, Esc closes (86); `/btw <question>` asks aside (57), as does the 💬 mode on the rail; `/rewind` and Esc twice (73), `/copy [N]` and `/export` (74), `/mcp` opens the settings menu (81, 107), `/remote-control` (83).

## How a chat runs `claude`

Per chat: `claude --input-format stream-json --output-format stream-json --verbose --permission-prompt-tool=stdio --setting-sources=user,project,local --permission-mode=<mode> --replay-user-messages --include-partial-messages --prompt-suggestions`, then `--session-id <uuid>` for a new chat, `--resume=<id>` to come back, or `--resume=<from> --fork-session --session-id <new> --resume-session-at <msg>` for a fork; `--model` and `--settings <the chat's flag settings>` when set (82). The environment drops `CLAUDECODE`, `CLAUDE_CODE_ENTRYPOINT`, `CLAUDE_CODE_CHILD_SESSION`, `CLAUDE_CODE_SSE_PORT`, `EMBARCH_DESK_INTERNAL` and every inherited `CLAUDE_CODE_RESUME_*`, and sets `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=true` (73).

**The first line is `initialize`** (66): the PreToolUse autosave hook (61), the auto-mode and refusal-fallback dialogs, and the panel's own MCP server, spoken as `mcp_message` (65), with `getDiagnostics` when `diagnosticsTool` is on `handoff` unless `handoff` is `off` (103), and `last_session` always: `{cwd?, turns?}`, the previous session's last turns, tool calls and pending background tasks as text (spec/handoff.md). The same read is `node dist/last-session.js [--cwd <path>] [--turns N] [--config-dir <login dir>]`, exit 1 when there is none. **Answered from the CLI:** `can_use_tool` (permissions, `AskUserQuestion`, `ExitPlanMode`), `request_user_dialog`, `elicitation`; any other request is refused at once. **Sent to it:** `interrupt`, `set_permission_mode`, `set_model`, `apply_flag_settings`, `get_settings`, `rename_session`, `get_context_usage`, `background_tasks`, `get_task_output`, `stop_task`, `cancel_async_message`, `side_question`, `rewind_files`, `export_conversation`, `mcp_status`, `mcp_reconnect`, `mcp_toggle`, `remote_control`.

**The assistant's call** (26): `claude -p --model haiku --max-thinking-tokens 0 --no-session-persistence --output-format stream-json --verbose --include-partial-messages --strict-mcp-config --setting-sources "" --system-prompt <its own> --tools ""`, the prompt on stdin, `EMBARCH_DESK_INTERNAL=1`. **The cards prompt alone** carries a `<desk_references>` block when the draft matches the desk's index (88), one line each: `[r1] ABC-12 "Make the widget" Done · PR owner/repo#7 "Widget" merged`. A reference card answers `{"category":"refs","ref":"r1","find":"<the phrase, as the draft has it>","title","why"}` with no edit (an older `"missing"` with a `ref` is read the same; any other card of decision 28's kinds is dropped, 97); the extension writes the replacement from the line's entry, and drops a card whose `ref` was not sent or whose `find` is not in the draft.
**Promptu's CLI** (`embarch-promptu`'s docs/contract.md §5, §7–§8), in the chat's folder, the binary `promptuPath`: `promptu prep --have <desk,embarch-api|none> [--pattern <id>] [--rec] [--start] [--desk <file>]`, the rough prompt on stdin; `promptu next <run>` and `promptu render <run> [--rest recommended|assume]`, the answers as JSON on stdin; `promptu patterns --json` for the card; `promptu memory --json` for the Memory menu (95, 96, 98), and `promptu week status --json` for the card's weekly line and the icon's dot (95; exit 2 is an old binary: no line), and `promptu week run --json` on a click (95; exit 4 is a run already going). The `--desk` file is `{key, title, url, id, text}` from the brief, 0600 in a folder of its own, removed after `prep`.
**The login file** (106): `~/.config/embarch-chat/logins.json`, `{"logins": {name: absolute config folder, or null for the CLI's default}, "folders": {window folder: picked login}, "sessions": {session id: login}}`, written whole and renamed into place, only while more than one login is configured; the window's folders lose their entry when it has no pick. A `claude` wrapper reads it, and records a session it finds none for. At most 3,000 sessions, the oldest dropped. **The account** comes from `oauthAccount` (`emailAddress`, `organizationName`, and the account and organisation ids to compare) in `<configDir>/.claude.json`, `~/.claude.json` for the CLI's default; that file and `.credentials.json` are polled every 2 s.
**Also read:** `claude agents --json` (Jump, and the resume guard of 31); `claude --version` (30); Claude Code's transcripts under `~/.claude/projects` for past chats and the prompt prefix match, kept in memory only (26).

## What it asks the desk

The desk calls (`/view`, `/sessions`, `/items`, `/mailbox`, `/refs`) and the entries the chat takes: [interfaces/desk.md](interfaces/desk.md).

## The wire probe

Ask the live `claude` one question, unfiltered, before raising `TESTED_RANGE`: [interfaces/wire-probe.md](interfaces/wire-probe.md).

## What the page is handed

What the host hands a chat's webview from the desk and the chat's folder; the webview never holds the desk token (20):

| Message | What |
|---|---|
| `{t:"refs", refs}` | The window's desk's reference index, `{issues, prs}` whole, each time it changes; `null` with none (88) |
| `{t:"usage", usage}` | The plan's usage from any chat's `rate_limit_event` (`unifiedWindows`), merged window by window, each `{used, resetsAt, at}`; per-model limits under `models`; `null` before one (99) |
| `limitPrefs`, `handoffTool`, `limitWait` in a chat's state | The Limits menu (109): `{session, weekly, text, handoff}`; whether the handoff tool is declared; the hit the chat waits on, `{limit, window, resetsAt, hitAt, armed, stopped?}`, folded from the host's `_limitPrefs` and `_limitWait`. The page answers `{t:"limits", prefs}` and `{t:"limitCancel"}` |
| `{t:"promptuState"}`, `{t:"promptu", view}`, `{t:"promptuResult"}`, `{t:"promptuMemory"}` | Promptu's card, a chat's dialog as `prep`/`next` printed it, how a run ended (the prompt, or one line and Start work's starter), the Memory menu's data; the brief itself never (95, 96, 98) |
| `githubRepo` in each snapshot's view | The chat's folder's GitHub repo, `owner/repo`, from its git config on disk — regular files of 64 KB or less, a FIFO, a device or a larger file read as none — github.com only, picked as `gh` picks one with no terminal: the remote `gh repo set-default` marked, else upstream, github, origin; `null` with none. Used for a prose or draft `PR #N` only, never for a step (88) |
