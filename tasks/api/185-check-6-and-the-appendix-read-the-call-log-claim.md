# 185 — Check 6 recomputes the report's call-log claim, and the appendix prints it

**State:** open
**Source:** decision 124 (`decisions/verify-report.md`); `embarch-core/interfaces/signing.md` (`observed.call_log`) and `interfaces/publish.md` (`report-data.json`)
**Issue:** EMB-265
**Scope:** api
**Hardware:** none
**Owner:** no

## What

A zip now carries a call-log segment when the run's signed record names a
call-log range (`core/145`, `api/182`, `api/183`), but `report-data.json` has
no call-log field and the appendix still prints "Not carried in milestone 1: a
call log (this zip has none)". Core will add the field in `core/148`, and
check 6 compares `report-data.json`'s keys whole (decision 124), so a key
`verify` does not know fails. **This unit and `core/148` are one change in two
repos: the supervisor lands both together or neither.**

**The field, fixed here so both units write the same thing.** `report-data.json`
gains `observed.call_log`: `{head, first_seq, last_seq, count}`, copied from the
signed record's `observed.call_log` (`head`, `first_seq`, `last_seq`, which are
both null when the run made no call) with `count` the number of entries in the
range (0 when the range is null). It is **present exactly when the signed record
carries `observed.call_log`**, absent otherwise. `schema` stays 1: decision 124
already treats a key Core adds as the same check's, with no bump.

When this is done:

- **Check 6** recomputes `observed.call_log` from the signed record and the
  call-log segment, and compares it like every other key. A zip whose record
  names a range and whose `report-data.json` lacks the field fails, naming it;
  so does one whose field disagrees (a changed `count`, say). A zip whose
  record has no `observed.call_log` (milestone 1) passes with no field.
  State in decision 124's amendment that a zip published by a Core between
  `core/145` and `core/148` fails check 6 for the missing field.
- **The appendix** (`src/publish_report.rs`) prints the head, the range and
  the count, with the sentence that the call log holds the calls made to Core,
  and that hardware reached without Core is not in it. A zip with no field
  keeps "no call log".
- `interfaces/verify.md` row 6 and `interfaces/publish.md` say so. The
  matching sentence in `embarch-core/interfaces/publish.md` is `core/148`'s,
  not this unit's.

Where to start: `src/verify_report.rs` (check 6), `src/publish_report.rs` (the
appendix line), and the fixture zips the verify tests build.

## Why now

The call-log range and segment landed in `core/145` and `api/183`; the report a
reader opens still says there is none.

**Burndown leg: no new numbered decision.** Amend decision 124 in place. If the
work needs a new decision, or a `schema` bump, stop and say so in this file and
in your report: either one changes how this pair lands.

**Doc size:** `embarch-api/open.md` is in reserve, 916 B left, with its debt
parked as `tasks/api/181` (blocked). Leave `open.md` alone if you can.

## Done when

- [ ] A fixture zip whose `report-data.json` carries the call log's head, range and count passes check 6.
- [ ] The same zip with the count altered fails check 6, naming the field.
- [ ] A milestone-1 fixture zip still passes check 6, and its appendix reads "no call log".
- [ ] The appendix of the fixture publish prints the head, range, count and the Core's-calls sentence.
- [ ] Gate green (`../../embarch-fleet/gate.md`), with `EMBARCH_DOC_DIR` at your doc worktree if a test reads the docs.
- [ ] Decision 124 amended in place, `interfaces/` updated, `changelog.d/` fragment dropped.
