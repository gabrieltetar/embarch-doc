# 018 — `desk_add_line` can put a note on another work item

**State:** open
**Source:** Linear issue EMB-82
**Issue:** EMB-82
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

A session can only add a note to its own work item. `desk_add_line` and the route behind it, `POST /sessions/{sid}/line`, always file the note on the session's item, or hold it until the session has one. `POST /tiles/{item@date}/line` takes any item, but only the Desk tab uses it, and its notes are the user's, not an agent's. A session that learns something about another work item while working on its own has nowhere to put it, so the finding lands on the wrong item or nowhere.

Add an optional target, **with this direction (the issue's own, stated by the owner):**

- `desk_add_line` takes an optional `item`: an issue key or a desk item id, on any desk. Absent, the tool behaves exactly as today, the held line included.
- `POST /sessions/{sid}/line` takes the same optional `item` in its body.
- An unknown key or id is an error that names it: nothing is written and nothing is held.
- The note is an ordinary note on the target item's tile for that day, carrying the calling session's id, so it joins that item's Harvest note as every note does (decision 50).
- A note on an item with no time that day opens a tile there; reading `open_tile_keys`, that tile waits in the hand at 0 h.
- The tool's description says when to set `item`, and `plugin/skills/desk/SKILL.md` says when a session sends a note to another item.

## Why now

The owner filed it: a chat working on one issue that finds something about another has no way to record it where it belongs.

## Where to look

- `src/mcp.rs` `LineParams`, `desk_add_line` — the tool, its parameters and its description
- `src/server.rs` `session_line` — the route
- `src/store.rs` `item_by_key` — an issue key to its item
- `plugin/skills/desk/SKILL.md`
- `embarch-doc/embarch-desk/decisions/notes.md` (decisions 48 to 55) and `interfaces.md` (the route's row)

## Dispatch notes

- Normal mode: a new numbered decision is expected. Write it in `embarch-desk/decisions/notes.md`, numbered per `DOC-CONVENTIONS.md` (the next free number across the desk's decisions), and update the route's row in `interfaces.md`.
- A request body that gains a field must still accept the old body (serde default); say so in a test.
- No `embarch-desk` doc in `embarch-doc` is in doc-size reserve at the split.
- Nothing touches hardware or a live desk.

## Done when

- [ ] `desk_add_line` with `item` set to another item's issue key files the note on that item's tile for today, carrying the calling session's id.
- [ ] `desk_add_line` without `item` behaves as before, the held line included.
- [ ] An unknown `item` returns an error naming it and writes nothing.
- [ ] The tool's description says when to set `item`.
- [ ] `interfaces.md` and a new `embarch-desk` decision describe the field.
- [ ] Each of the first three has a test.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.
