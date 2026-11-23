# 172 — `publish` republishes a swept run by handing Core the earlier zip's own files

**State:** blocked
**Unparks when:** `tasks/core/137` has landed.
**Source:** `embarch-api/open.md` — "A republish after the retention sweep refuses"; `notes/hil/06-report-and-publish.md` — "A revision is built from the earlier zip, its captures included" (owner, 2026-11-20)
**Scope:** api
**Hardware:** none
**Owner:** no

## Dispatch notes

- `embarch-api` decision 117 (`decisions/publish-revisions.md`) refuses a republish after the retention sweep and writes nothing, because Core's `report-data` answered `404` once the run's directory was gone. `tasks/core/137` gives Core a way to take the earlier revision's Core files back; read the decision it lands with before designing this side.
- The earlier zip is already read for a republish (`measurements.json` and the `streams/*` renderings, decision 117), so this extends that read rather than adding a second one.
- Per-decision budgets near their limit in `embarch-api`: `ledger#98`, `bench-exchange#89`, `failure-reporting#67`. Amend 117 in `decisions/publish-revisions.md`, or add a new decision there.

## What

When Core reports that a run's directory is swept, `publish` hands Core the earlier revision's Core-produced files from the highest earlier zip, in the shape `core/137` defines, and continues the republish as it does for a run on disk. The earlier zip is still left byte for byte.

## Why now

Closes the one departure from 06's design that `tasks/api/168` recorded, once Core's half exists.

## Done when

- [ ] A test against the mock Core: a swept run republishes to `-r2` from the earlier zip, and the earlier zip is unchanged.
- [ ] A test: a swept run with no earlier zip in the publish folder refuses, saying which file it looked for.
- [ ] Decision 117 amended (or a new decision), `interfaces/publish.md` and the `open.md` line updated.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
