# 160 — Core runs a Test selection test by test

**State:** claimed by agent/core/160-core-runs-a-test-selection-test-by-test, 2026-11-25 09:19
**Source:** EMB-366 — Core has nothing that runs a Test selection test by test
**Issue:** EMB-366
**Scope:** core
**Hardware:** none
**Owner:** no

## What

A Test run is a sequence of host studies, grouped by bench, with
preconditions, run counts and a failure policy (`notes/hil/03-test.md`, "One
test", "The verdict", "A run", items 1, 5 and 6). Core runs one host study at a
time (`src/host_study.rs`); since `core/159` a go takes the lease and marks the
run started, and nothing then runs it. When this is done, Core's executor runs
a started Test run:

- **Order.** After the go, bench by bench in `run.json`'s order, test by test.
- **Precondition** before every test. `reset` resets the DUT through Core's
  own reset path and sends each bench board's `idle` line from the bench
  entry, waiting for its `until`; `none` does nothing; the others as the bench
  declares them.
- **Each run** of a test is the host study by hash from Core's definitions,
  through the existing executor with its teardown. **Each step's target** is
  derived by Core, never written by a study: a signal whose origin is the `dut`
  role is `dut`; another role, a bench board or an instrument is `bench`. A
  step's failure is charged by what it addressed.
- **Verdicts** through the shared crate's `judge_run` and `judge_test`
  (`embarch-study-designer` decision 112, `src/hil_judge.rs`), with the
  measurements Core already records.
- **The policy.** A fail goes on to the next test; an error skips the rest of
  its bench `stopped_by_error` and goes on to the next bench; a cancel stops
  the run, the rest `cancelled`; with `stop_on_fail` the first fail skips the
  rest `stopped_after_fail`; a test whose `requires` did not pass is
  `requires_not_met`.
- **`GET /test-runs/{run_id}`** answers the current bench and test, the
  verdicts so far, and a waiting prompt with its text.
- **Host studies only in this phase.** Record in the decision that dev-bench
  studies too is the alternative, the owner's to strike (plan choice 18).

`core/159` left the seam for this: `test_runs::end_run(state, run_id, status,
reason, by)` and an empty `RUN_ADMITTED` list in `src/api.rs`. Two notes from
the reviewers of earlier units belong to this one: while the run lock is held,
decision 95's one route a running study still admits (`/study/{id}/cancel`)
gets `409` until `RUN_ADMITTED` names it; and the `expect` (choice) path of
`judge_run` checks incomplete evidence but not `calibration_expired`, so decide
whether that check applies when a person's choice is judged. Core decision 135
also names a deadline as the executor's to own.

## Where to look

- `src/host_study.rs` (`execute`, `HostBackend`, `run_step`),
  `src/measurements.rs` (`SignalOrigin`), `src/api.rs` (the reset path,
  `RUN_ADMITTED`), `src/test_runs.rs`
- `embarch-doc/notes/hil/03-test.md`, "A run"
- `embarch-doc/embarch-core/decisions/test-runs.md` (134),
  `decisions/test-run-go.md` (135)

## Where the doc goes

A new core decision in a new topic file (for example
`decisions/test-run-executor.md`), with `interfaces/test-runs.md` amended for
`GET /test-runs/{run_id}`. **Do not grow 135** (79 B under its per-decision
limit) or 134; point at them from the new decision instead. No core file is in
doc-size reserve at dispatch. If your work pushes one into reserve, file
`tasks/core/<NNN>-compact-core.md` in the same commit per `tasks/README.md`.

## Done when

- [ ] Over fake backends: a fail in test 1 still runs test 2; an error on bench
      A skips the rest of A and runs bench B; a cancel marks every remaining
      test `cancelled`.
- [ ] With `stop_on_fail`, the tests after the first fail are
      `stopped_after_fail`; a test requiring a failed one is
      `requires_not_met`.
- [ ] A test with a run count of three and one failing run is `fail` with
      counts.
- [ ] A lost port on a bench board's signal is `error`; `until_not_seen` on the
      DUT's is `fail`.
- [ ] `GET /test-runs/{run_id}` during a fake run names the bench, the test and
      the verdicts so far.
- [ ] Gate green.
