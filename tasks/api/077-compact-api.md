# 077 — Compact embarch-api/decisions/tests.md out of size reserve

**State:** blocked
**Source:** `scripts/check-doc-size.py`, spent by `tasks/api/075` — decision
30's write-up pushed `embarch-api/decisions/tests.md` to 95.2% (590 B left).
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api/decisions/tests.md` is inside its size reserve. Compact it per
`DOC-COMPACTION.md`, honoring the `Must not delete:` list below.

**Compacts:** `embarch-api/decisions/tests.md`

## Why now

`check-doc-size.py` is red until this is filed or the file is compacted. Filed
in the same commit that spent the reserve, per `tasks/README.md`.

**Size debt due:** 2026-09-26

## In flux: yes

`tests/smoke_harness.rs` (decision 30) just landed and is new; decisions 54
and 56 both record verification work done within the last week. This file is
still moving — a compaction pass should read it fresh rather than trust this
task's own account of what is settled.

## Must not delete

- The verbatim reasoning for why the mock Core is hand-rolled on `tokio::net`
  rather than `wiremock`/`httpmock` (decision 46).
- The bearer-sweep mechanism description and its "not covered" limits
  (decision 54).
- The workspace-membership mechanism and its two verified-by-mutation facts
  (decision 56: `default-members` vs `members` alone; `embarch-ui`'s isolation
  established via a synthetic consumer crate).
- Decision 30's "written 2026-09-12" pointer to `tests/smoke_harness.rs` and
  what distinguishes that tier from decision 46's.

## Done when

- [ ] `embarch-api/decisions/tests.md` back under its size cap with room to
      spare, same facts intact per the list above.
- [ ] `scripts/check-doc-size.py` green for this file.
- [ ] `changelog.d/` fragment.
