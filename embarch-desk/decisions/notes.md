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

### 78 — A session can put a note on another work item
`desk_add_line` and `POST /sessions/{sid}/line` take an optional `item`, an issue key (any case) or a desk item id, on any desk. Absent or blank, nothing changes, held line included. Set, the note is an ordinary note on that item's tile for today carrying the calling session's id, so it joins that item's Harvest note (50), and an item with no time that day gets an open tile waiting in the hand at 0 h. An unknown `item` is a 404 naming it; nothing is written and nothing is held, even for a session with no item. The body is serde-defaulted, so the old body still parses. **Rejected:** a session's tool for the tile route (its notes are the user's, and it refuses a sent tile); holding a note for an item that does not exist yet; filing an unknown key on the session's own item, which is the wrong-item failure this fixes.

### 85 — A line body the desk cannot honour is refused, and a session takes back its own line
`POST /sessions/{sid}/line` and `POST /tiles/{id}/line` share `LineBody`, which collects any field it does not know and answers a 400 naming each (`unknown field later, target; a line takes text, kind and item, and nothing was written`), in the shape of the desk's other refusals. Cause: against a desk built before `item` (78), `{"item":"w608",…}` landed on the session's own tile, silently, and nothing could undo it. `deny_unknown_fields` would answer 422 from axum's extractor, so the check is in the handler. `DELETE /sessions/{sid}/line/{nid}` and the MCP tool `desk_remove_line` take back one line by note id: only a line that session wrote (a note with `source` `agent` and its `session_id`; another's is a 403, an unknown id a 404), and only while its tile is open. A tile approved, folded or discarded is a record, so its line stays and the 400 says to add a correcting line; archived lines are no longer on a tile and read as unknown. A held line has no id and cannot be taken back. **Callers checked** (2026-11-12): `embarch-chat` `src/desk/client.ts` (`text`, `kind`), `embarch-ui` `assets/desk.js` and `tests/browser/drive_desk.py` (`text`, `kind`), the MCP tool (`text`, `kind`, `item`): none sends an unknown field. **Rejected:** `deny_unknown_fields` alone (a 422); letting a session remove any line (the user's and other sessions' notes are theirs); removing from a sent tile (it would rewrite what Harvest was sent).
