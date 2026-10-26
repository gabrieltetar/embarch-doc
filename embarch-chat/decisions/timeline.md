# embarch-chat decisions: What the chat shows

**Status:** active, 2026-10-23.

The timeline: steps and what they touched, turns, compactions, answered questions, tool output, time, the cache and the usage limit, copying and export, long chats, bench cards and atlas links.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 8 — Day one matched Claude Code's panel: approve, stop and stream; diffs; @-file mentions

Permission prompts, Stop, streamed text, the mode switch. **Claude's questions and a plan's approval count as approve** — on the wire both are permission requests — and show as forms, with options and previews or the plan. An Edit or Write shows as a diff and opens VS Code's diff editor on a click. @ completes a workspace path, with the selected lines, and the CLI inlines it. **Also day one:** a context meter in the header with a Compact button, and a subagent's steps nested under its call. What this left for later — pasted images and rewind — followed (56, 73).

### 50 — A step says what the agent is doing, and quiet steps fold

A tool row reads as the call's own one-line `description` when a built-in tool carries one, the tool a muted tag; otherwise the tool and what it acts on. An MCP tool's `description` is its data, never a label. Two or more quiet steps in a row fold into one collapsed row headed live by the latest step, with "N steps", a spinner, "waits on you" or a red error count; edits, todos, questions, plans, subagents and bench cards stand alone. The owner watches the header to stop an agent heading the wrong way. **Rejected:** a Haiku sentence per run (about 1 s behind, $0.002 a call), raw commands, auto-expanding runs.

### 87 — A step that reaches Linear, GitHub, Slack, the Desk or the bench names what it touched, as a link

After the tool's muted tag (50) comes the connector's glyph in one colour — Linear's, GitHub's and Slack's marks (Simple Icons, CC0) in the theme's text colour, the EmbArch mark for the Desk and the bench — then the thing by name: `ABC-12 Make the widget`, `#7 Widget`, `#channel`, a card's title, a board, `study <id>`. It is read from the step's own input and result (the desk's tools, a Linear MCP server, `gh` and its own output lines, Slack's reads, `embarch-api`); a step carrying only a key, or a PR number with its repo, takes its title and link from the desk's index (88), else from the chat's own item. **A click opens the thing itself**: an issue in Linear, a PR in GitHub, a channel by its permalink, and a card, a study or a board in `embarch-ui` at `#desk?item=`, `#live-study?study=` or `#topology?board=` (`embarch-ui` decision 58; a board by the role the step named, else its board type). **A URL from a tool's output is a link only as https to that connector's own host** — `linear.app`, `github.com`, a `slack.com` host — with no credentials or port; anything else shows unlinked. **A `gh` step's repo is only the one it names** — `-R`/`--repo`, `GH_REPO=` — **or the one its own output names**: a bare `gh pr merge 7` shows `#7` alone, untitled and unlinked, never as the chat's folder's repo's and never as the index's only #7. `merge`, `close`, `reopen`, `ready`, `review`, `checks` and `diff` take no URL from their output — `gh` prints none there, so one is a later command's — only `gh`'s own status line, as it prints it with no terminal; `create`, `comment` and `edit` take the first URL printed, `view` its own `url:` line. A `gh` is read only in a command's place, never inside quotes or as an argument. **A folded run lists what its steps touched**, each once, up to 3 and "N more", leaving the head's own to the head; a bare `#7` and a named `owner/repo#7` stay two entries, the bare one unlinked. List and search tools, Harvest and GitHub's MCP server name nothing yet. **Rejected:** colour marks, an issue opening its Desk card rather than Linear, a tool's URL linked as it came, a PR found by its number alone, **a `gh`'s repo inferred from the chat's folder with `cd`s tracked across steps** — three review rounds each found wrong links: the shell keeps its cwd from step to step, the folder it was compared against moves with each turn and on a reopen, and comments, `if cd` and heredocs fool a parser; a link to the wrong PR is worse than none.

### 51 — Turns stand apart

A turn begins at each of the owner's messages: blocks 12 px apart within a turn, 28 px between turns with a 1 px rule, none above the first. **Rejected:** a card per reply, spacing without a rule.

### 76 — A compaction is one folded card

Claude Code's "Compacted chat · manual · 12k tokens freed" (the size before compaction), with the summary inside — live the line after the boundary, in a transcript the `isCompactSummary` line — so the owner checks what it kept before the next hardware step. **Rejected:** the old single line that dropped the summary, the summary as a message in the timeline.

### 79 — An answered question stays as a Questions row

Each option, the picks marked, the Other text — read from the CLI's record of the answers, else its result text; Other takes several lines (Shift+Enter) and Enter answers [measured: line breaks kept]. **Rejected:** the plain tool row, the result text only.

### 62 — A tool's whole input or output opens in a read-only editor tab

In a fitting language (Bash output as a log, a command as shell, JSON as JSON). **Rejected:** an untitled document (editable; closing it asks to save), a bigger preview in the panel.

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

### 89 — What the CLI sends Claude is never the owner's bubble

A `user` line whose `origin.kind` is not `"human"` never becomes a user entry (one rule, `originKind`, which `humanPrompt` reads too; a line with no `origin` falls back to `turnOrigin`, and the panel's own messages, written to a transcript with `turnOrigin` "sdk", stay the owner's). A **task-notification** — the CLI replaying a background task's end, `isReplay` with XML content — is one row worded like the CLI's own line, `Agent "<what it was asked>" completed` (or `failed`, `stopped`; a shell task's summary as it comes), whose click opens the task's card and scrolls to it, also out of a folded run. A task that ends while no turn runs gets its row ahead of the turn the CLI then starts: the system `task_notification` only notes it (`noticed`), and the reply, or the replay line if it comes first, puts it in the timeline; the owner's next message or a turn's end drops one never answered. A **peer** message without `handback` is a collapsed `Message from <name>` row; a hand-back is another task's. A transcript records a notification Claude took mid-turn as an `attachment` of type `queued_command`, and the same row comes back from it; any other queued command is the owner's typing, which has its own line. Such a row is a note, so it is never matched to a pending message, edited or rewound to. [Recorded on CLI 2.1.287: `notifymid`, `notifyidle`.] **Rejected:** a new entry kind (a note already carries a link and folds nowhere), a row for the system line alone (it is also sent for a subagent's own shell [seen in `notifyidle`], and for a task the CLI may never answer [assumed, not recorded]).
