# 092 — doctor check 13 should read hello's 503/409 as busy, not broken

**State:** claimed by agent/umbrella/092-doctor-check-13-reads-hello-503-409-as-busy, 2026-10-26 03:24
**Source:** core/104 (`agent/core/104-dev-bench-gate-and-hello-take-locks`), inbox drop `core-doctor-check-13-reads-hello-503-409-as-busy.md`
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 03:24

`umbrella/091` has landed (`embarch-umbrella` `c75200d`): check 13 now has a `dirty-checkout` Warn
arm (decision 19 amended), so you start on top of it and there is nothing to rebase. Read Core's
side from `embarch-core/decisions/platform.md` decisions 4, 14 and 15 and from Core's own handler,
not from this task's summary, and take the holder's name from the body Core actually sends; if the
body shape is not stated anywhere you can cite, say so in your report rather than guess. Keep the
`--json` keys stable; a new code for the busy verdict is fine if decision 19 names it. Nothing in
`embarch-umbrella/` docs is in reserve. Your worktree's parent links the main checkouts of
`embarch-topology`, `embarch-study-designer` and `embarch-api`. Never edit another repo, never run
`embarch doctor` against the live Core or bench: test against a stub.

## What

`GET /dev-bench/hello` now takes `hw_lock` for its identity gate (a `503` naming the holder after 500 ms, core decision 14) and holds `study_lock` for its handshake (a `409` while a study or another hello holds the link). `embarch doctor` check 13 calls hello; a `503` or `409` there means the bench is busy, not that firmware is broken. Make check 13 report busy (warn/skip) for those two statuses, naming the holder from the body.

`umbrella/091` item 3 also changes check 13 (its dirty-checkout verdict). The two are independent; whichever lands second rebases onto the first.

## Why now

core/104 landed 2026-10-26 (`embarch-core/decisions/platform.md` decisions 4/14/15); its log entry names doctor's check 13 as unchecked against the new statuses.

## Done when

- [x] Check 13 distinguishes `503`/`409` from `502`/`404` and says "busy" with the body's holder.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.

## Done

Check 13 and check 11 map hello `503`/`409` to a `Busy` outcome; check 13 gives Warn, code `busy`, body quoted (decision 19). Body is plain text with no structured holder field in Core (`study.rs` hello_with, `api.rs` acquire_hw_lock), so it is quoted, not parsed. Tests are host-side against injected outcomes. No hardware debt.
