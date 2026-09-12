# 059 — `study-status --follow`, the drop path, `lagged`, and a reconnect have still never met a real Core

**State:** open — **attempted and not startable, leg 085, 2026-09-11.** Core was reachable
(`api_version 0.1.0`, `host_type_schema_version 17`) and reported `"probes": []`; `validate
dev-bench` answered `recorded hardware_id 6fcddc36cb781b71, live None`. **Both boards are
unplugged**, so there is nothing to run a study against. Left `open` rather than `blocked` per
`.claude/leg.md` — a board coming back is normal and needs no human to un-block anything. Note
that `scripts/fleet-hardware.py`'s buffer said `attached: yes` for both roles; it was 5,902
minutes stale and `--refresh` is broken (`tasks/doc/041`), so **the buffer's attach state is not
usable for selection right now and the live check is the only answer.** The conflated error text
that check returns is filed as `tasks/core/041`.
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
