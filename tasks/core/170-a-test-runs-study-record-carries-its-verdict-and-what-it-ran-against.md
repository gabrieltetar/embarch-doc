# 170 — A test run's study record carries its verdict and what it ran against

**State:** done — amended each test study record with its verdicts, smoke findings, prompt scopes and run.json (decision 145); host-side, unit-tested
**Source:** EMB-369 — a Test run leaves no signed record of itself and no run-log entry per test
**Issue:** EMB-369
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Each test in a Test run runs a study, and Core signs that study's record as it
does any other: `image_status: "unverified"` and no verdict (`src/signing.rs`).
The HIL design wants each test's record to say what it concluded and what it
ran against (`embarch-doc/notes/hil/03-test.md`, "A run", item 10). `core/169`
adds the run's own record over these; this unit fills the per-test one. When
this is done, a study record sealed for a test in a Test run carries in its
predicate:

- **the verdict** and its reason, with its qualifiers and behaviours;
- **the image status** of the DUT and of every bench board, from the readback
  the smoke check already runs (core decisions 142, 143);
- **the identities**: each board's hardware ID and each instrument's `*IDN?`
  reply as the smoke check kept it;
- **the scope of each prompt's answer** (core decision 138);
- and `run.json` joins the record's subjects.

A study run outside a Test run is sealed exactly as before.

## Where to look

- `src/signing.rs` — `seal`, `SealJob`; `src/test_executor.rs`; the smoke
  check's findings (`Progress.smoke`, `RunOutcome.smoke`)
- `embarch-doc/embarch-core/interfaces/signing.md`
- `embarch-doc/embarch-core/decisions/signing.md` (110), `smoke-check.md`
  (143), `image-readback.md` (142), `host-prompt.md` (138), and `core/169`'s
  new decision

## Where the doc goes

`core/169` landed decision 144 in `decisions/test-run-record.md`; a new
decision there, beside it. Do not grow
`signing#110` (2,486 B over its limit) or any other decision
`check-doc-size.py --pressure` lists as near or over; point at them.
**`embarch-core/open.md` is in reserve** (893 B left; its compaction
`tasks/core/171` is blocked, In flux: yes): do not write it. If you must, carry
`core/171`'s compaction in the same commit and keep its `Must not delete:` items.

## Done when

- [x] A fixture Test run's per-test record carries the verdict, the image
      status of the DUT and each bench board, the identities and `*IDN?`
      replies, and each prompt answer's scope, with `run.json` among its
      subjects.
- [x] A plain study run's record is unchanged, byte for byte in its predicate
      fields.
- [x] The record still verifies with the standard DSSE check.
- [x] `interfaces/signing.md` amended.
- [x] Gate green (`cargo build`, `test`, `clippy --all-targets -- -D warnings`).
