# 004 — A waiting tile from an earlier day proposes its gap against that day's current Harvest entries

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-desk finding 3), verified by Opus against embarch-desk@880d9707
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

A tile proposes only the time Harvest does not already hold for its item that day (decision 41). The desk re-reads Harvest for today every two minutes. Any other day is re-read only when `GET /day/{date}` asks for it, which happens when the user picks that day in the day list. The hand (decision 57) shows tiles from earlier days, but `GET /view`, opening a tile, Polish and ✓ never re-read that tile's day. ✓ re-reads the day only after it has created the entry.

So a tile from an earlier day computes its gap from whatever was fetched while that day was today. An entry logged for that day afterwards is invisible. A typical case is time typed into Harvest the next morning and dated the day before. The tile proposes the full time again, and one ✓ logs it twice. Decision 41 exists to prevent exactly this.

When done, the gap a waiting tile proposes reflects that day's Harvest entries as of a recent read. Two directions, which can be combined:

- The sync loop also re-reads the distinct days that have waiting tiles, less often than today.
- ✓ re-reads the tile's day before sending, and refuses with a message when the gap moved.

Finding 1's override behaviour (`desk-hours-set-by-hand`) interacts with the second direction: while the dialog PATCHes hours on every ✓, the hours sent are the stale prefill, not the recomputed gap.

## Why now

- `src/server.rs:2275-2281`: the sync loop refreshes `harvest_logged` for today only.
- `src/server.rs:1765-1777`: `GET /day` refreshes the day it is asked for, older than two minutes.
- `src/server.rs:482-496`: `GET /view`, which carries the hand, never fetches.
- `src/server.rs:1033-1064`: ✓ calls `refresh_logged` after `create_entry`, not before.
- `src/store.rs:1160-1169`: `logged_hours` reads whatever was last stored for the date. A past day's stored entries are kept for 14 days (`:1296-1299`).
- Decision 41 says other days are fetched "when it is read". The hand reads past-day tiles without reading their day, and no decision records that as intended.

## Done when

- [ ] With a waiting tile from an earlier day and a Harvest entry for that day and item added after the day ended, the tile's proposed hours drop by that entry within one refresh interval, or ✓ refuses to send the stale amount. A test with a stubbed Harvest covers whichever is built.
- [ ] Refreshing past days is bounded: one read per distinct waiting-tile day per interval, never one per tile. A test or a stated constant shows the bound.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated (decision 41's fetch schedule; the spec §4 refresh constant if one is added), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
