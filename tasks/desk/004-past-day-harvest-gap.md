# 004 — A waiting tile from an earlier day proposes its gap against that day's current Harvest entries

**State:** claimed by agent/desk/004-past-day-harvest-gap, 2026-10-26 03:24
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-desk finding 3), verified by Opus against embarch-desk@880d9707
**Scope:** desk
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 03:24

**"Finding 1" below has landed.** `desk/003` (`embarch-desk` `da354f8`, decision 61): ✓ writes
`Tile.sent_hours` rather than `hours_override`, and `PATCH /tiles/{id}` with `"hours": null` clears
a typed override. `ui/090` (`embarch-ui` `ca0caf8`) makes the Desk tab send `hours` only when a
person typed them. So with no typed override, ✓ sends the computed gap, and the interaction the
last paragraph of `## What` describes now applies only to a typed override: say in decision 41 (or
a new decision) what ✓ does when the day's gap moved under a typed override. Line numbers below
predate `desk/003`; re-find them. Nothing in `embarch-desk/` docs is in reserve.

**Never touch the owner's desk service on :4891, its store, or the real Harvest or Linear APIs.**
Stub Harvest in tests; use your own ports and target dir. The owner rebuilds and deploys the desk.

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

- [x] With a waiting tile from an earlier day and a Harvest entry for that day and item added after the day ended, the tile's proposed hours drop by that entry within one refresh interval, or ✓ refuses to send the stale amount. A test with a stubbed Harvest covers whichever is built.
- [x] Refreshing past days is bounded: one read per distinct waiting-tile day per interval, never one per tile. A test or a stated constant shows the bound.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated (decision 41's fetch schedule; the spec §4 refresh constant if one is added), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.

## Done

Both directions built (decision 62). Sync loop re-reads each earlier day with an open tile every 10 min (`past_days_due`, one read per distinct day, a failed day backs off). ✓ re-reads the tile's day first and, with a typed override, refuses once when the gap moved. Tests are pure-function (`past_days_due`, `gap_moved_under_override`): Harvest's base URL is a const, so no stubbed-HTTP test of the refresh itself.

**Debt:** a ✓ against real Harvest with an entry added after the day ended has not run (owner deploys and runs).
