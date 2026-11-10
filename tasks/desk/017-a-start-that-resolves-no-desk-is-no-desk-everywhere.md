# 017 — A start that resolves no desk is no desk everywhere, one start names one desk, and a shrinking note edit is accepted

**State:** claimed by agent/desk/017-a-start-that-resolves-no-desk-is-no-desk-everywhere, 2026-11-09 22:26
**Source:** Linear issue EMB-48, filed by an audit (points 1 to 3; points 4 and 5 are `tasks/ui/108`)
**Issue:** EMB-48
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

Three low findings from the second review of desk notes (decision 74).

1. **A start that resolved no desk.** `Session.start_desk` is `None` both for "no start yet" and for "the last start resolved no desk". A session first seen in desk A's repo that later resumes in a folder with no desk hears no notes, but `notes_desk` falls back to `session_desk(session_id, &sess.cwd)`, which can still resolve A — so `GET /sessions/{sid}`, `desk_work_item` and `desk_add_desk_note` still use A. Record a start that resolves no desk as such: store the start's cwd and fall back to `session_desk(session_id, start_cwd)`, so every reader agrees with the start.
2. **One start block, two desks.** `ask_text` picks its cards from `Session.desk_id` (set by the session's first event), so one start block can list desk A's cards and then name desk B in the switch question (`switch_text`) and the notes (`start_notes`). The cards should come from the desk the start resolved (`desk_for_path(cwd)`), the one `switch_text` and `start_notes` name.
3. **A full desk refuses a shrinking edit.** `check_desk_note` refuses any edit while `others + note.cost() > DESK_NOTES_MAX_CHARS` (4,000), even when the edit shrinks the note. Reachable only with notes written before the costs changed. An edit whose cost does not grow is always accepted; one that grows it past the cap is refused as now.

## Why now

Filed by an audit; points 1 and 2 let a session hear or use the wrong desk.

## Where to look

- `src/store.rs` `State::notes_desk` — the fallback in point 1
- `src/store.rs` `Session.start_desk` — the field that is `None` for two meanings
- `src/events.rs` `start_notes` — writes `start_desk`
- `src/events.rs` `ask_text` — the cards' scope from `s.desk_id` (point 2); `switch_text` for the desk it names
- `src/store.rs` `State::check_desk_note` — the `others + note.cost()` test (point 3)
- `embarch-doc/embarch-desk/decisions/notes.md` — decision 74, amended in place if it states any of the three

## Dispatch notes

- Points 4 and 5 of the issue are the Desk tab's (`embarch-ui/assets/desk.js`) and are `tasks/ui/108`; do not touch `embarch-ui`.
- A stored session shape that gains a field must still read a state file written before it (serde default), and say so in a test if the store has round-trip tests.
- Burndown is on: no new numbered decision. These are bugs against decision 74; amend it in place where its text is wrong.
- No `embarch-desk` doc in `embarch-doc` is in reserve at the split.

## Done when

- [ ] A session that starts in desk A's repo and resumes in a folder with no desk is given no desk by `notes_desk`, `GET /sessions/{sid}`, `desk_work_item` and `desk_add_desk_note` alike.
- [ ] One start block lists only the cards of the desk it names in the switch question and the notes.
- [ ] On a desk over the 4,000 cap, an edit that does not raise a note's cost is accepted, and one that raises it is refused.
- [ ] Each of the three has a test.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.
