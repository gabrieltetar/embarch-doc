# 042 — `embarch-core/open.md` says the auth sweep covers 27 routes; the router registers 26

**State:** open
**Source:** refill sweep, leg 087, 2026-09-11. `embarch-core/open.md`'s route-sweep bullet, checked
against `src/api.rs` and against `decisions/auth.md`, which already carries the corrected number.
**Scope:** core
**Hardware:** none — a count of `.route()` registrations and a test constant, both readable.
**Owner:** no

## What

`embarch-core/open.md` says *"Decision 42 asserts all 27 registered routes answer `401` without a
token and with a wrong one"*. The router registers **26**: `src/api.rs` has 25 `.route(` lines, one
of which (`/signals`) chains `.post().get()`. `AUTH_CASES` in the same file has exactly 26 rows, and
`const DOCUMENTED_ROUTE_COUNT: usize = 25;` is pinned by a test beside it.

**`decisions/auth.md` already agrees with the code** — *"All 26 registrations are one contiguous
block in `api.rs` today (`GET /logs/stream` retired)"* — so `open.md`'s 27 is a stale
pre-retirement count that survived the retirement it should have been updated by. The two docs
disagree with each other, which is the part that matters: a reader who checks one is told a
different number than a reader who checks the other.

**Settle the second number while you are here, and only if it is genuinely wrong.**
`DOCUMENTED_ROUTE_COUNT = 25` and `AUTH_CASES`' 26 rows are not obviously the same quantity —
one may be counting `.route()` calls and the other registrations, which is a real distinction given
`/signals`. **Read both and say which it is in the decision or the comment**; if they are two
correct counts of two different things, make each say which thing, and do not change either number
to match the other. Do not change behaviour.

## Why now

The sweep's whole value is that it is exhaustive, and the only place a reader learns how exhaustive
is a sentence carrying a number. A stale one is worse than none: it says the sweep covers a route
that no longer exists, which would hide the retirement of a route that *should* have been swept.

## Done when

- [ ] `embarch-core/open.md`'s route-sweep bullet says 26, agreeing with `decisions/auth.md`.
- [ ] `DOCUMENTED_ROUTE_COUNT` and `AUTH_CASES`' row count each say, in a comment or in the
      decision, what they are a count *of* — or the wrong one is corrected, whichever reading the
      code actually supports.
- [ ] No route behaviour changes and no auth case is added or removed by this task.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
