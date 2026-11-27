# 208 — verify re-evaluates step outcomes and re-parses step-time numbers

**State:** done — check 2 recomputes Exchange outcomes and step numbers (decision 140)
**Source:** EMB-374 — verify does not re-evaluate step outcomes or re-parse step-time numbers
**Issue:** EMB-374
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`verify`'s check 2 says "step outcomes were not re-evaluated against their
recorded replies: not recomputed by this version" (`src/verify.rs`). The design:
"every step's outcome re-evaluated against its recorded reply with the step's
`until` and `refused_on` markers, every step-time number re-parsed from the raw
replies with the patterns" of the signed study file or `run.json`
(`embarch-doc/notes/hil/06-report-and-publish.md`, "Verify", check 2). When this
is done:

- **Each step in `events.json` has its outcome recomputed** from the recorded
  reply, `reply_truncated`, and the signed study file's `until` and `refused_on`,
  by the same rules as Core's `judge` (`embarch-core/src/host_study.rs`, read
  only). A reply that cannot decide it (a lost port, a cut reply) is reported as
  such, never as a match.
- **Each step with a `parse` has its number re-parsed** with the study designer
  crate's `parse_step_number` and compared with the step record and
  `measurements.json`.
- **A zip from before either existed still passes**, saying what it could not
  recompute.

If matching `judge` needs a rule Core does not export, copy the rule and pin it
with a test against a recorded fixture; say in the decision that it is a copy and
where the original lives.

## Where to look

- `src/verify.rs` (`check_measurements`)
- `embarch-core/src/host_study.rs` `judge`, read only
- `embarch-doc/embarch-api/interfaces/verify.md` row 2; decisions 118 to 121

## Where the doc goes

A new api decision, or one of 118 to 121 amended if it stays under its limit, and
`interfaces/verify.md` row 2. **`embarch-api/spec.md` is in reserve** (1,110 B
left; `tasks/api/201` is blocked): do not grow it. `lease#90`, `test-plans#134`,
`ledger#98` and `bench-exchange#89` are at or over their limits: do not grow them.

## Done when

- [x] A fixture zip passes check 2 with every outcome and parsed number recomputed.
- [x] The same zip with one reply byte changed so its marker vanishes fails,
      naming the step.
- [x] The same zip with a parsed number altered fails, naming the measurement.
- [x] A milestone-1 zip still passes check 2.
- [x] Gate green (`cargo build --workspace`, `test`, `clippy --all-targets -- -D warnings`).
