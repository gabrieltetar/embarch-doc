# embarch-chat decisions: Readouts and results

**Status:** active, 2026-10-23.

What the chat reads out beside the conversation: time, the cache line and the usage limit, copying and export, how a long chat stays fast, bench results as cards and atlas citations as links.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 68 — Time on screen

`embarchChat.showMessageTimestamps` (machine scope, off) puts a 24-hour time to the second over each message and a date line where the day changes. A running step counts its time; finished steps of 10 s or more and subagents keep their duration. "Not responding" shows when a turn runs, no line has come from the CLI for 60 s, nothing waits on the owner and no tool of the turn runs. **Rejected:** hour:minute only, a duration on every step.

### 69 — Between turns the status line says whether a message now reads the prompt cache

"Warm, about N min left", "likely expired", or not covering the compacted conversation, with the lifetime read from each reply: every recorded reply writes the **1-hour** cache [measured], so 41's first reason — Claude's default 5-minute lifetime — was out of date; the 5-minute idle close stands on the process cost alone, since the cache lives on the server. **Rejected:** a permanent footer icon, assuming 5 minutes.

### 67 — The account's usage limit is a banner above the status line

From `rate_limit_event`, by Claude Code's rules: nothing below 70 %, then percent used and the reset, then the limit hit and "wrapping up"; × hides it until the numbers change. **Rejected:** always showing the weekly percent, toasts.

### 74 — Each reply copies whole; `/export` is Claude Code's own text

Copy takes the turn's whole reply as Markdown, `/copy [N]` an earlier one; `/export` asks the CLI (`export_conversation`; a closed chat is resumed for it) and saves the text the host received through VS Code's save dialog, opened in the last export folder, else home — never the chat's repo, where a conversation about client work is one `git add` from a remote. **Rejected:** a Copy per assistant message, Claude Code's untitled editor, always the panel's own text.

### 85 — A long chat stays fast: only what changed is drawn again, and every row stays in the page

A turn, and within it a row, whose entries are the objects they were is not drawn again; a streaming reply is parsed again only from its last open block [measured on a generated 60-turn, 600-step chat: a delta 12.9 → 3.5 ms p50, frame p95 33 → 17 ms, no frame dropped; a 100 KB reply in a 3× chat 39.8 → 8.0 ms]. **Rejected:** dropping the oldest rows from the page as Claude Code does (the webview's Ctrl+F would miss them, and scroll and run state would need rebuilding), `content-visibility` (estimated heights move the stick to the bottom).

### 15 — Bench results show as cards

An `embarch-api` build, flash, bootload, study or `serial_log` result becomes pass or fail, board, first error, steps passed and a link into `embarch-ui`, from the tool result already in the stream. A `serial_log` holding an assert failure, a panic, a hard fault or a fatal error is a fail, matched on the whole markers, so a pin that is "asserted" is none. **Rejected:** a live bench strip polled from Core (a second `embarch-ui`), plain output.

### 16 — Atlas citations become links

`atlas-use` cites every hardware fact as `<doc_id> p<N>` or `<board>:<ref>`, and in a repo with an `embarch/atlas` each opens in the editor: that page's text (the document's card when the page has none), or the line naming the ref in the board's nets or parts. **Rejected:** a hardware pane for the open file (a second Atlas tab), plain text.
