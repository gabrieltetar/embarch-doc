# embarch-desk decisions: The work item's notes

**Status:** active, 2026-10-23.

The work item as where the work's knowledge gathers: the one pull, notes and tile lines as one stream, memory files captured as notes, the one-time import, and where notes are kept.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

Shaped as `embarch-chat` decisions 40, 42–47 and 49, in order, in `embarch-chat-desk-proposal.md` on 2026-10-22; built the next night and deployed 2026-10-23 (d9a8efc). The proposal is folded and deleted.

### 48 — The work item is where the work's knowledge gathers, and a session pulls it from the desk
At start a session knows its item and that **the desk holds everything about it** — the issue and its comments, PRs, sessions, tile lines, bench activity, and **the notes taken about the work done locally**, which otherwise scatter across files and transcripts and belong on the item instead. **One desk tool returns it all**: `desk_work_item`, the brief (`GET /items/{id}/brief`) — the issue with its latest comments, PRs, sessions, notes, bench activity — newest first, capped at 16,000 characters (about 4K tokens); nothing is pasted in up front, and the SessionStart brief names the tool. **Rejected:** the SessionStart brief growing to about 1K tokens of issue text for every session; key and title only, with `linear_get_issue` as the one way in; a brief the panel puts before the first message; an index first, then a call per kind; notes only, with the issue left to `linear_get_issue`.

### 49 — Notes are written by sessions, unasked, and the owner cuts
Too many rather than too few, as tile lines already are (13). **Rejected:** notes only when asked; Haiku extracting them after every turn (a call per turn, seeing only the last reply).

### 50 — Notes and tile lines are one stream
A tile line is a note of kind `done`, and **what goes to Harvest is the summary of that day's notes**, in the owner's words: the polish reads that day's notes of every kind. `desk_add_line` gained a `kind` — `done` by default, or `finding`, `decision`, `handoff`, `todo` — rather than a second tool appearing. **Rejected:** two streams (cleaner billing text, but two tools and two places to look).

### 51 — Notes build on what Claude Code's auto-memory already does
On the owner's current client project the agent keeps, unprompted, a dated state file per issue — 16 of that project's 58 memory files are named by issue key, each holding the branch, commits, PR and what is pending [measured 2026-10-22]. The owner's call: capitalize on that habit rather than invent a new one. **Rejected:** a log by kind written through a new tool, one living document per item, a log plus a summary.

### 52 — The desk's hook captures them
The PostToolUse hook already runs on every tool call: a `Write`, `Edit` or `MultiEdit` whose `file_path` is under `~/.claude/projects/*/memory/` and is not `MEMORY.md` becomes a note of kind `memory` on the session's work item, holding the file's text after the write — held until the session has an item, as lines are; one note per `source_path`, its last 20 versions kept. The agent changes nothing, the file stays its own copy, and **the session decides the item, not the file's name**. **Rejected:** the desk's skill telling sessions to keep issue state with a desk tool (it competes with Claude Code's built-in memory rule); the desk scanning memory files by issue key (misses the 42 of 58 not named by key, and knows no session).

### 53 — A card shows each note's newest state; a click opens the full list
`GET /items/{id}/notes`, every note newest first. **Rejected:** the newest with earlier versions folded under it, every change as its own line.

### 54 — The per-issue memories written before capture are attached once
Once, on the first start that has notes, each file to one item at most: the first key in the file's name, else in its frontmatter (the agent's own summary of the file), in `ABC-123` or `abc123` form. On the live desk it attached 6 files to 3 items [measured 2026-10-23]. Harvest summarizes only a day's own notes, so no past entry changes. **Rejected:** starting fresh; a key anywhere in the text (20 files, two of them to two items each, one 31.8K characters); the file name only.

### 55 — Notes stay in `state.json`, and a rollback restores a copy
The worst case measured is 8.2 MB, 20 ms a write, and the state is rewritten only when something changes; the previous binary drops notes on its next write, so a deploy copies `state.json` first and a rollback restores the copy. **Rejected:** one memory version per file per day; versions older than the newest in `notes/<item>.jsonl` (also rollback-safe, about an hour more).
