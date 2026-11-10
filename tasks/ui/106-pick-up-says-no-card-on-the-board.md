# 106 — The Desk tab's Pick up list says "no card on the board"

**State:** done ( agent/ui/106-pick-up-says-no-card-on-the-board, 2026-11-09)
**Source:** Linear issue EMB-115, filed by a worker
**Issue:** EMB-115
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

The Desk tab's Pick up title and its empty note describe the list as it is: the user's open issues with no card **on the board**. Since `desk/015` (`embarch-desk` decision 43, amended) `/pickup` also lists an issue whose card exists but the view window hid, so "with no card" and "Every open issue of yours already has a card." are now untrue in that case.

## Why now

The list's own title contradicts what it shows.

## Where to look

- `assets/desk.js` `loadPickup` — the title (`"Pick up — your open issues … with no card"`) and the empty note
- `embarch-doc/embarch-desk/interfaces.md` — the `/pickup` row, which already states the rule; it is `desk`'s, so read it, do not edit it

## Dispatch notes

- A wording change in one file. Search `assets/` and `embarch-doc/embarch-ui/` for any other text saying Pick up lists only issues with no card, and fix what you find in your scope.
- Burndown is on: no new numbered decision. None should be needed.
- No `embarch-ui` doc in `embarch-doc` is in reserve at the split.

## Done when

- [x] The Pick up title and empty note say "no card on the board", or words to that effect.
- [x] No other Desk tab text says Pick up lists only issues with no card.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.
