# 015 — An issue whose card the view window hides is listed in Pick up

**State:** claimed by agent/desk/015-a-card-outside-the-view-window-is-in-pick-up, 2026-11-09 21:23
**Source:** Linear issue EMB-72, filed by a session
**Issue:** EMB-72
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

An open issue assigned to the user is always reachable from the Desk tab without a search: either its card is on the board or the issue is in Pick up. Start work or Add card on that Pick up row puts its card back on the board.

Today a card left with no activity for longer than the view window (`EMBARCH_DESK_WINDOW_DAYS`, 7 by default), not pinned and not archived, drops off the board (`visible`), and `pickup` excludes every issue with an unarchived card, visible or not, so the issue shows nowhere. Searching its key in the Pick up box lists it, but **Add card** goes through `ensure_item`, which returns the existing card without touching `last_activity_ms`, so nothing appears. Only **Start work** brings it back, because `start_work` sets `last_activity_ms`.

## Why now

The owner could not find an issue on the Desk tab to start work on it.

## Where to look

- `src/server.rs` `pickup` — excludes every issue with an unarchived card
- `src/server.rs` `visible` — the window that hides a quiet card
- `src/server.rs` `ensure_item` — returns an existing card by key without setting `last_activity_ms`
- `embarch-doc/embarch-desk/` — the Pick up and view-window rules, wherever `spec.md` and the decisions state them

## Dispatch notes

- **`embarch-ui/assets/desk.js` is not yours.** Its `loadPickup` titles the list "with no card" and its empty note says "Every open issue of yours already has a card."; if the fix makes either untrue, say so in your report and file it with `fleet-linear.py file --from worker --project embarch-ui`, and do not edit it.
- If a decision states that Pick up lists only issues with no card, amend it in place; this task authors no new numbered decision.
- No `embarch-desk` doc is in reserve at the split.

## Done when

- [ ] An open, assigned issue whose card is outside the view window is listed in Pick up, and Start work or Add card on that row puts its card back on the board.
- [ ] A `cargo test` covers `/pickup` with a card outside the window.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `embarch-desk` docs updated; `changelog.d/` fragment dropped.
