# embarch-chat decisions: Readouts and results

**Status:** active, 2026-10-30.

What the chat reads out beside the conversation: time, the cache line and the plan's usage, copying and export, how a long chat stays fast, bench results as cards and atlas citations as links.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 68 — Time on screen

`embarchChat.showMessageTimestamps` (machine scope, off) puts a 24-hour time to the second over each message and a date line where the day changes. A running step counts its time; finished steps of 10 s or more and subagents keep their duration. "Not responding" shows when a turn runs, no line has come from the CLI for 60 s, nothing waits on the owner and no tool of the turn runs. **Rejected:** hour:minute only, a duration on every step.

### 69 — Between turns the status line says whether a message now reads the prompt cache

"Warm, about N min left", "likely expired", or not covering the compacted conversation, with the lifetime read from each reply: every recorded reply writes the **1-hour** cache [measured], so 41's first reason — Claude's default 5-minute lifetime — was out of date; the 5-minute idle close stands on the process cost alone, since the cache lives on the server. **Rejected:** a permanent footer icon, assuming 5 minutes.

### 67 — The account's usage limit is a banner above the status line (retired 2026-10-30, see decision 99)

From `rate_limit_event`: nothing below 70 %, then the percent and the reset, then the limit hit. Retired at the owner's word: the rail's Usage icon shows the plan's usage instead, from the same event.

### 99 — A Usage icon in the rail: the plan's 5-hour session and week, amber from 70 %, red from 90 %

The owner's feature, 2026-10-30, replacing 67's banner at his word. **The rail (94) carries a Usage icon (📊)** showing the Claude plan's usage: the 5-hour session's and the week's share used, each with when it resets. **The source is 67's**: the `rate_limit_event` a chat's CLI sends with a turn when the account's limit changes, and on a process's first turn at least; Claude Code 2.1.287 carries both windows there as `unifiedWindows.five_hour` and `.seven_day`, `{utilization, resetsAt}` — an `@internal` field [measured 2026-10-30 from its bundle; the recorded sessions carry it] — and without it the icon reads the one limit the event names. The reading is the account's, so the host keeps the newest any of the window's chats heard, window by window — one an event leaves out stays as last heard, with its own age (review F15) — and hands it to every page; no chat keeps a copy, and nothing is stored: a new window or a reload is grey, no number, until a chat's first reply (the owner's P17). **The icon lights amber from 70 % of either window and red from 90 % or when a limit is hit**; hover opens a card, as Promptu's (95): each window's share, a bar, and the reset as "in 3h (14:05)", how old each window's reading is, the limit hit or a turn finishing past it. **A reading expires at its reset**, as 67's banner did: past it a window shows as reset, grey, and lights nothing, and a limit hit holds until the limit it names resets; with no window left the icon is grey again (review F14). **A per-model weekly limit** (`seven_day_opus`, `seven_day_sonnet`, only ever the event's own share — `unifiedWindows` carries none [measured]) is a line of its own on the card, never the Weekly window, never the icon's colour (review F16). The icon sits alone at the top of the rail (94, the owner's P16). **Rejected:** a new source of the chat's own for the numbers; the banner beside the icon; the last reading kept across windows and reloads (P17's recommendation, declined).

### 74 — Each reply copies whole; `/export` is Claude Code's own text

Copy takes the turn's whole reply as Markdown, `/copy [N]` an earlier one; `/export` asks the CLI (`export_conversation`; a closed chat is resumed for it) and saves the text the host received through VS Code's save dialog, opened in the last export folder, else home — never the chat's repo, where a conversation about client work is one `git add` from a remote. **Rejected:** a Copy per assistant message, Claude Code's untitled editor, always the panel's own text.

### 85 — A long chat stays fast: only what changed is drawn again, and every row stays in the page

A turn, and within it a row, whose entries are the objects they were is not drawn again; a streaming reply is parsed again only from its last open block [measured on a generated 60-turn, 600-step chat: a delta 12.9 → 3.5 ms p50, frame p95 33 → 17 ms, no frame dropped; a 100 KB reply in a 3× chat 39.8 → 8.0 ms]. **Rejected:** dropping the oldest rows from the page as Claude Code does (the webview's Ctrl+F would miss them, and scroll and run state would need rebuilding), `content-visibility` (estimated heights move the stick to the bottom).

### 15 — Bench results show as cards

An `embarch-api` build, flash, bootload, study or `serial_log` result becomes pass or fail, board, first error, steps passed and a link into `embarch-ui`, from the tool result already in the stream. A `serial_log` holding an assert failure, a panic, a hard fault or a fatal error is a fail, matched on the whole markers, so a pin that is "asserted" is none. **Rejected:** a live bench strip polled from Core (a second `embarch-ui`), plain output.

### 16 — Atlas citations become links

`atlas-use` cites every hardware fact as `<doc_id> p<N>` or `<board>:<ref>`, and in a repo with an `embarch/atlas` each opens in the editor: that page's text (the document's card when the page has none), or the line naming the ref in the board's nets or parts. **Rejected:** a hardware pane for the open file (a second Atlas tab), plain text.
