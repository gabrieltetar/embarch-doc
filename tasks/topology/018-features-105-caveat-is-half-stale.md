# `features.d/topology-105-validate-reports-when-the-live.md`'s caveat is now half-stale

**State:** open
**Source:** worker on `tasks/core/026` (core/026-validate-handler-2 unit)
**Scope:** topology
**Hardware:** none

## What

`features.d/topology-105-validate-reports-when-the-live.md`'s `Status` cell
reads: "Shipped — topology half only; `embarch-core`'s `/validate` and the
other three wire mirrors have not switched over". `tasks/core/026` just landed
the `embarch-core` half: `POST /validate` now calls `validate_role_timed` and
serves `validated_at_utc_ms` alongside `confirmed_at_utc_ms`
(`embarch-core/decisions/surfaces.md` decision 50). The three wire mirrors
(`embarch-api`, `embarch-umbrella`, `embarch-ui`) are still unstarted
(`tasks/api/045`, `tasks/umbrella/041`, `tasks/ui/020`).

This row is `topology` scope, not `core`, so I did not edit it myself.

## Why now

The caveat text names a state ("core has not switched over") that is now
false. Leaving it will read as a stale/wrong fact to the next reader of the
suite feature inventory.

## Done when

- [ ] `features.d/topology-105-validate-reports-when-the-live.md`'s `Status`
      cell is updated to say the `embarch-core` half is done and only the
      three wire-mirror consumers remain (naming `tasks/api/045`,
      `tasks/umbrella/041`, `tasks/ui/020`).
