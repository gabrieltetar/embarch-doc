# 002 — Folding refuses an earlier or invalid day, ✓ keeps the folded lines, and a folded day reports what it carried

**State:** claimed by agent/desk/002-fold-and-approve-edges, 2026-10-26 00:40
**Reserve, for the worker:** no `embarch-desk` doc is in reserve today.
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-desk findings 2, 4 and 6), verified by Opus against embarch-desk@880d9707
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

Decision 58's fold has three gaps in the server. Each is small, and all are in the same code.

1. **The fold route trusts its caller for the direction.** `fold_tile` checks only that `from ≠ into` and that both tiles are open. Folding a Wednesday tile into Monday is accepted, and the one Harvest entry is then dated two days before the work. Decision 58's premise is "an earlier tile folds into a later one, one entry dated the later day". The Desk tab offers only a later tile, but the server is the access point and has no check of its own. Separately, a tile on a non-date can be created with `PATCH /tiles/{item@anything}`, and the tile id is never parsed as a date.
2. **✓ with no written note drops the folded lines.** When the tile's note is empty, `approve_tile` builds the Harvest note from the tile's own `lines` only. The dialog shows the folded tiles' lines, and the polish reads them, but this fallback does not. A target with no lines of its own sends an empty note.
3. **A folded day's row subtracts Harvest twice.** `fold_tile` freezes the gap (captured minus logged) as the folded tile's `final_seconds`. `tile_json` then treats that as captured time and subtracts the same day's logged hours again. `GET /day` reports the result as the folded row's `hours` and `captured_hours`. Today the Desk tab shows a folded row's logged hours and a badge, never these two fields, so the wrong number has not reached the screen yet.

When done, the server refuses a fold the decision does not allow, the ✓ fallback note carries everything the tile sends, and a folded row's numbers state what it carried. The worker chooses how a folded row reports its hours.

## Why now

- `src/server.rs:1091-1096` passes `into` through unchanged. `src/store.rs:757-781` checks only equality and openness. The UI's guard is `embarch-ui assets/desk.js:870`. Non-date tiles: `src/server.rs:821-825` (`split_tile_id`) and `:857-875` (`patch_tile` creates the record).
- `src/server.rs:1039-1043` (fallback note from `t.lines`) vs `src/store.rs:924-939` (`day_notes`, used by the polish, chains the folded lines) and `src/server.rs:198-200`.
- `src/store.rs:768-779` freezes the gap. `src/server.rs:186-194` subtracts `logged` from it again, and `:1697-1706` publishes it.

## Done when

- [ ] Folding into a date earlier than or equal to the source, or into a string that is not `YYYY-MM-DD`, answers 400 and changes nothing. A tile id whose date part is not a date is refused by every tile route. Tests cover each.
- [ ] ✓ on a fold target with an empty note sends a note containing the folded tiles' lines. A test covers a target with no lines of its own.
- [ ] `GET /day` for a folded source day reports, for that row, the hours it carried into its target, and never a value with that day's Harvest hours subtracted twice. A test pins it with 3 h captured and 0.5 h logged.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated (`interfaces.md` for the fold refusal), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
