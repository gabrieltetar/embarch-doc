# 092 — doctor check 13 should read hello's 503/409 as busy, not broken

**State:** open
**Source:** core/104 (`agent/core/104-dev-bench-gate-and-hello-take-locks`), inbox drop `core-doctor-check-13-reads-hello-503-409-as-busy.md`
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`GET /dev-bench/hello` now takes `hw_lock` for its identity gate (a `503` naming the holder after 500 ms, core decision 14) and holds `study_lock` for its handshake (a `409` while a study or another hello holds the link). `embarch doctor` check 13 calls hello; a `503` or `409` there means the bench is busy, not that firmware is broken. Make check 13 report busy (warn/skip) for those two statuses, naming the holder from the body.

`umbrella/091` item 3 also changes check 13 (its dirty-checkout verdict). The two are independent; whichever lands second rebases onto the first.

## Why now

core/104 landed 2026-10-26 (`embarch-core/decisions/platform.md` decisions 4/14/15); its log entry names doctor's check 13 as unchecked against the new statuses.

## Done when

- [ ] Check 13 distinguishes `503`/`409` from `502`/`404` and says "busy" with the body's holder.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
