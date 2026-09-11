# 059 — `study-status --follow`, the drop path, `lagged`, and a reconnect have still never met a real Core

**State:** open
**Source:** `tasks/api/035`, replacing the debt `open.md` and `tasks/api/026`
named as `tasks/api/001-sse-client.md` — a file that was never filed
**Scope:** api
**Hardware:** bench — needs a real installed `embarch-core` and a live study
**Owner:** no

## What

`api/035` (leg 072, 2026-09-10) confirmed on the bench that `study_watch`
against a real `embarch-core` receives pushed live frames — not a mock, not a
poll — on study `4d7bcc93cb38f7d01fae509a790d22bd` (`transport: live`,
`StepCompleted`/`StatusChanged` events). That leaves four things decisions 48
and 49 (`decisions/study-events.md`) describe that are still only tested
against the mock or not exercised at all:

- `study-status --follow`, the CLI call site — a different code path from
  `study_watch`, not exercised by that run.
- The drop/fallback-to-polling path (a subscriber falling behind or a refused
  subscription).
- The `event: lagged` frame itself.
- A reconnect after a drop.

## Why now

`open.md`'s stream bullet and `026`'s unpark condition both need to name a real
debt. Filed to close that gap.

## Done when

- [ ] Each of the four items above is exercised once against a real, installed
      `embarch-core` and the result recorded (which decision it confirms or
      contradicts).
- [ ] `open.md`'s stream bullet updated to reflect what ran.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
