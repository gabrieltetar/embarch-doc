# 155 — A host step parses its declared number, and a host study writes `measurements.json`

**State:** open
**Source:** EMB-359 — Core records a reply as text and parses no number out of it
**Issue:** EMB-359
**Scope:** core
**Hardware:** none
**Owner:** no

## What

A host study's `Exchange` or `Instrument` step records its reply raw today, and
`measurements.json` is written for a dev-bench `Study` only. Since `suite/062`
(landed 2026-11-25) a study may declare `parse: Option<StepParse {name, pattern,
unit}>` on an `Exchange` and a queried `Instrument`, and
`embarch-study-designer` exports `parse_step_number(reply, parse) -> Result<f64,
Incomplete>` behind `std` and `reducers` (study-designer decision 108). Core
accepts such a study and computes nothing from it, which is the silent accept
`suite/062`'s reviewer named. When this is done:

- After an `Exchange` or `Instrument` step with a `parse`, Core calls
  `parse_step_number` on the reply and records `parsed {name, value}` or
  `parsed {name, incomplete}` in the step's record in `events.json`, beside the
  raw reply (`src/host_study.rs`: `run_step`, `StepRecord`, the events writer).
- `incomplete` is `truncated_reply` when the reply was cut (`reply_truncated`),
  and `parse_failed` when the pattern found no number (`value: null`).
- At the study's end, Core writes `measurements.json` for a host study from its
  parses, in `hil-shapes.md`'s measurement shape: `method {kind: "parse",
  pattern}`, `source {file: "events.json", step}`.
- **`by` and `instrument` come from what the step addressed, never from the
  study**: a signal whose origin is the `dut` role is `by: dut`; a bench
  board's signal or an instrument is `by: bench`, the instrument named.
  `SignalOrigin` in `src/measurements.rs` already resolves a signal's origin for
  dev-bench measurements: reuse it.
- A bench value's `U` stays "undeclared" until an instrument's metrology
  (EMB-358/EMB-360) or a characterisation supplies it.
- The file is a subject of the signed record, as `measurements.json` already is
  (`src/signing.rs`; its `submitted_by` comment for a host study changes with
  this).
- A host study with no parse writes no `measurements.json`, as today.

Core's `Cargo.toml` must turn on whatever study-designer feature exports
`parse_step_number`, if it does not already. Prompts' kinds and answers
(EMB-367) are not this unit.

## Why now

`suite/062` added the fields and the parser and left Core accepting a `parse`
it ignores. This unit closes that, and unblocks the verdict executor, `verify`'s
re-parse (EMB-374) and an instrument's uncertainty reaching its measurements
(EMB-360). Design: `embarch-doc/notes/hil/03-test.md`, "The verdict".

## Where the doc goes

**Decisions near or over their per-decision limit (`check-doc-size.py
--pressure`):** `host-study.md` decision 95 is 799 B over and `signing.md`
decision 110 is 2,486 B over. Do not grow either. Put the new decision in a new
topic file (`decisions/host-parse.md` fits, mirroring study-designer's); if 95
or 110 needs a pointer to it, make room in that entry by shortening its own
text by at least as much. `interfaces/measurements.md` (3,527 B) and
`interfaces/host-studies.md` (4,486 B) take the shapes; if either would cross
its cap, split by topic rather than trim. Core's `open.md` is 3,912 B; if your
debts push a file into reserve, file `tasks/core/<NNN>-compact-core.md` in the
same commit per `tasks/README.md`.

## Done when

- [ ] Over a fake port, a DUT reply with a declared parse gives a step record
      with the number and a `measurements.json` entry with `by: dut`.
- [ ] The same over a bench board's signal gives `by: bench`; over an
      instrument, `by: bench` with the instrument named.
- [ ] A truncated reply gives `truncated_reply`; a reply with no number gives
      `value: null` and `parse_failed`.
- [ ] A host study with no parse writes no `measurements.json`, as today.
- [ ] `interfaces/measurements.md` and a new decision say it.
- [ ] Gate green (`../../embarch-fleet/gate.md`): `cargo build`, `cargo test`,
      `cargo clippy --all-targets -- -D warnings`.
- [ ] `spec`/`decisions`/`open.md` updated, `changelog.d/` fragment dropped,
      `status.d/` fragment for anything suite-level it made false.
