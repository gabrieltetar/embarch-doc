# 098 — One function turns a test's records into its verdict

**State:** done — hil_judge: judge_run, judge_test, skip, decision 112; gate green under every consumer feature set; no hardware
**Source:** EMB-356 — no shared function turns a test's records into its verdict
**Issue:** EMB-356
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`verdicts.rs` holds each verdict rule — `step_verdict`, `limit_verdict`,
`combine`, `requirement` (decisions 95 to 98) — and nothing composes them for
one test. If Core's run executor and `verify` each composed the rules, the two
could disagree. When this is done, the crate has one composition both call:

- **`judge_run(test, steps, measurements, rules) -> Judged`**: each step's
  outcome through `step_verdict` with its target (`dut` or `bench`, given by the
  caller, never by the study); each limit through `limit_verdict` on its
  measurement, `w` from the decision rule and the measurement's `U`; an
  observation's choice against the test's `expect`, a different choice being
  `fail` with reason `limit` (plan choice 27); the run's verdict is `combine` of
  those.
- **`judge_test(runs) -> Judged`**: the worst run, by `combine` ("One test" in
  `notes/hil/03-test.md`: the test's verdict is its worst run's), carrying the
  counts.
- **`skip(test, why) -> Judged`** for `requires_not_met`, `stopped_by_error`,
  `stopped_after_fail`, `bench_missing`, `hook_unmapped`, `not_applicable` and
  `not_selected`.
- **Qualifiers from the measurements**: `bench_firmware_unreleased` (or
  unverified, or flashed by the agent), `rests_on_dut_report`,
  `rests_on_person_observation`, `calibration_undeclared`,
  `declared_by_agent`, `declared_by_study`, and `unvalidated` for a premade
  test without its evidence.
- **The behaviour versions it used**, for the record (`Rules::behaviours`).

Decision 96 keeps the `verdicts` feature `alloc`-only. A function that takes a
`run.json` test entry needs `hil-test`'s types, so where the composition lives
and under which feature is the worker's call; record it in the decision.
Plan choice 27 is the owner's to strike, and the decision says so.

## Why now

`study-designer/096` (EMB-355) landed the `run.json` test entry this reads.
EMB-366 (Core runs a Test selection test by test) waits on this and on EMB-364,
which runs in the same leg as this task; `verify`'s check 3 and the report's
data wait on it too.

## Where to look

- `src/verdicts.rs` (`Rules`, `Judged`, `Summary`, `Target`, `StepOutcome`,
  `Limit`, `Evidence`), `src/hil_expand.rs` (`RunJson` and its test entry),
  `src/hil_test.rs`
- `embarch-doc/embarch-study-designer/interfaces/hil-verdicts.md`,
  `interfaces/hil-shapes.md` ("The six verdicts"),
  `decisions/hil-verdicts.md` (95 to 98)
- `embarch-doc/notes/hil/03-test.md`, "The verdict"

## Where the doc goes

A new decision in `decisions/hil-verdicts.md` beside 98, and the two functions
documented in `interfaces/hil-verdicts.md`. **In reserve:**
`interfaces/hil-run.md` (378 B left), filed against
`tasks/study-designer/097-compact-study-designer.md`, which is `blocked` with
`In flux: yes`. Do not write into it; if your work must, compact that file as
part of this unit, keeping 097's `Must not delete:` list, and say so in this
file. **Decisions near their per-decision limit:** `host-parse.md` 108 (188 B
left); do not grow it. If your work pushes another file into reserve, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit per
`tasks/README.md`.

This is a shared crate. Gate it under every feature set a consumer builds it
with (`embarch-fleet/gate.md`): Core's `std,reducers,hil-image,hil-test`, the
UI's `study-ui,gatt-extract,eap-parse`, `embarch-api`'s `alloc,reducers`,
`embarch-core-client`'s `alloc`, the defaults, and `--all-features`.

## Done when

- [x] A fixture per path: a lost port on a bench board is `error`,
      `port_lost`; `until_not_seen` on a DUT signal is `fail`; a value inside
      the guard band is `inconclusive`, `guard_band`; a `parse_failed`
      measurement is `inconclusive`.
- [x] Two runs, one pass and one fail, give `fail` with counts of one each.
- [x] A value from a bench board on an `unreleased` image carries
      `bench_firmware_unreleased`.
- [x] `hil-verdicts.md` documents the two functions, and a decision records
      where they live.
- [x] Gate green under every consumer's feature set.
