# 169 — A Test run leaves a signed run record and a run-log entry per test

**State:** claimed by agent/core/169-a-test-run-leaves-a-signed-run-record-and-a-run-log-entry-per-test, 2026-11-26 14:29
**Source:** EMB-369 — a Test run leaves no signed record of itself and no run-log entry per test
**Issue:** EMB-369
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Core signs one record per study run, with `image_status: "unverified"` and no
verdict (`src/signing.rs`), and its run log's `run` entries carry no test id,
definition hash, unit, DUT image or verdict (`src/run_log.rs`, `end`). The HIL
design wants Core to "sign a record of the whole run as it ends, a cancel or an
interruption included" (`embarch-doc/notes/hil/03-test.md`, "A run", item 10),
every run-log entry on a unit "grouped by test or study, requirement ID, DUT
image and definition hash" (03, "The report"), and a Test run's captures
counted "as one unit in Core's retention sweep" (item 7). The report's coverage,
the interruption and resume, the manual verdict, Core's side of publish and
`verify` all read these. When this is done:

- **The run's record**, `test-run.dsse.json`, signed as the run ends — a
  finish, a cancel or an interruption: `run.json`'s hash, the `Selection` as
  Core expanded it at the go, each selected test with its study record's hash
  and its verdict, or the reason it has none (not run, cancelled, error), the
  run it `resumes` (absent when none), the unit key, and the call log's range in
  the shape a study record already carries it.
- **Run-log entries**: one per test run,
  `{type: "test", run_id, test_id, definition_hash, requirements, unit_key, dut_image, verdict}`,
  and one `test_run` entry for the whole run carrying its record's hash.
- **Retention**: the study runs of a Test run are swept as one unit, and none
  is swept while the Test run is unpublished.
- The record verifies with the standard DSSE check, as a study record does.

**Not in this unit**: the per-test study record's predicate gaining the verdict,
image status, identities and answer scopes. That is `tasks/core/170`, which
builds on the record this one adds. Keep the study record's predicate as it is.

## Where to look

- `src/signing.rs` — `seal`, `SealJob`; `src/run_log.rs` — `end`,
  `unpublished_ids`; `src/test_executor.rs` — the run's end, cancel and error
  paths; the retention sweep
- `embarch-doc/embarch-core/interfaces/signing.md`, `interfaces/run-log.md`
- `embarch-doc/embarch-core/decisions/signing.md` (110), `run-log.md` (111),
  `test-run-executor.md` (136, 137), `smoke-check.md` (143, the unit key)

## Where the doc goes

A new core decision, in a new topic file (for example
`decisions/test-run-record.md`). `check-doc-size.py --pressure` lists
`signing#110` (2,486 B over), `analog-capture#127`, `host-study#95`,
`definitions#133`, `lease#93`, `stopping-a-study#128` (over), `test-run-go#135`
(95 B left), `run-log#111` (120 B left) and `instruments#104` near or over
their limits: do not grow any of them; point at them from the new decision.
Amend `interfaces/signing.md` and `interfaces/run-log.md`.

## Done when

- [ ] A fixture run cancelled on its second bench has a signed run record that
      names every selected test with a verdict or a reason.
- [ ] Each test run has a run-log entry with its test id, definition hash, unit
      key, DUT image and verdict, and the run has its `test_run` entry.
- [ ] The retention sweep leaves every study run of an unpublished Test run in
      place.
- [ ] The run record verifies with the standard DSSE check.
- [ ] `interfaces/signing.md` and `interfaces/run-log.md` amended.
- [ ] Gate green (`cargo build`, `test`, `clippy --all-targets -- -D warnings`).
