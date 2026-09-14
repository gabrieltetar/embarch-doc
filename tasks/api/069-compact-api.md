# 069 — `embarch-api/decisions/surface.md` is in reserve after decision 71

**State:** done
**Source:** `api/068`'s fix (decision 71, `validate`'s `kind`-branching wrapper) landed the
same commit that put this file into its reserve band; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

## Why now

`python3 scripts/check-doc-size.py` named `embarch-api/decisions/surface.md` at 11258 B
against a 12288 B cap (91.6%) — inside the last 10% of its reserve, same mechanism
`api/057` already named for `zephyr.md`. Parked `blocked`/`In flux: yes` until a mission
split was judged safe, since this was the file every JSON/error-shape change to the
tool/CLI surface landed a decision in.

## Done when

- [x] `embarch-api/decisions/surface.md` is back under its reserve band, its "must not
      delete" facts intact — a mission split (JSON shape/versioning vs failure-reporting)
      is one honest way to do it, not the only one.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment.

## Closed

Done by `api/087`, as this task's own body named it: a **verbatim** mission split at the
seam this task itself proposed. Decisions 57, 67 and 71 moved unchanged into a new
`embarch-api/decisions/failure-reporting.md`; decisions 16, 24 and 50 stayed in
`surface.md`, which now sits at 4,998/12,288 B (40.7%) — out of reserve.
`embarch-api/decisions/surface.md` is therefore **removed from this task's `Compacts:`
line** (deleted, not struck through) rather than carried forward: nothing here is over its
reserve band anymore.

All three "must not delete" facts are accounted for: decision 50's `error_kind` argument
stayed in `surface.md` untouched; decision 67's `tool-wrapping.md`-headroom scope note
moved with it to `failure-reporting.md` and still parses there, since it argues why the
entry sits in *this* file rather than in `tool-wrapping.md` regardless of which file that
now is. Decision 71's three facts are intact, with the first amended in place, dated,
rather than silently rewritten: `api/087` gave a `kind`-less body a third `"unknown"`
value instead of defaulting it to `"mismatch"`, so that one fact — "`kind` defaults to
`"mismatch"` for an older Core" — no longer holds and decision 71 says so under an
`Amended 2026-09-13 (decision 73)` line. The other two facts (`503`/`409` share one parse;
both wrappers call `is_not_attached()` rather than `live_hardware_id.is_none()`) are
unchanged.

Baseline check per `tasks/doc/052`: `scripts/decision-size-baseline.json` carried no pin
for 57, 67 or 71, so none needed to move with them.
