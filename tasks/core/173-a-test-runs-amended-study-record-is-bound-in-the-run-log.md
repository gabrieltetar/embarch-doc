# 173 — A Test run's amended study record is bound in the run log

**State:** done — test_run entry binds the amended hashes; the amend stays (decision 146)
**Source:** EMB-579 — a Test run's amended study record no longer matches its chained run-log hash
**Issue:** EMB-579
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Core decision 111 chains the hash of a study's `record.dsse.json` into the run
log's `run` entry when the study ends, so that "a replaced record is a mismatch".
Decision 145 (`core/170`) then amends and re-signs that same file at the Test
run's end (`Sealer::amend_for_test`, called from `test_run_record.rs`
`amend_studies`). The `run` entry cannot be rewritten, so every study made inside
a Test run now fails 111's own comparison: the signed record on disk never
matches its logged hash. 145 does not say so. When this is done:

- **Either the amended record's hash reaches the chain**, for example in the
  `test` entry Core already writes per test (decision 144) or in a new entry, **or
  the amend is removed** and the per-test verdict is carried outside the sealed
  record. Choose, and say why in the decision. The previous leg was unsure whether
  re-signing a sealed record is the right design at all; weigh that.
- **Decision 145 (or a new decision beside it) says which entry binds a Test
  run's study record**, and 111 points at it.
- **A test compares a Test-run study's bound hash with the file on disk** and
  passes, and a plain study's `run` entry still matches its file.
- `GET /study/{id}/log`, and anything that compares a record with its logged hash,
  reads the bound entry for a Test-run study. Find every such reader in Core and
  say what each one reads after the change.

The run log's chain must still recompute over every entry, old and new.

## Where to look

- `src/run_log.rs` (the `run` entry's `record_sha256`, the `test` entry)
- `src/signing.rs` `Sealer::amend_for_test`; `src/test_run_record.rs` `amend_studies`
- `embarch-doc/embarch-core/decisions/run-log.md` (111),
  `decisions/test-run-record.md` (144, 145); `interfaces/run-log.md`, `interfaces/signing.md`

## Where the doc goes

`decisions/test-run-record.md` (145 amended, or a new decision there).
**`run-log#111` has 120 B left**: one pointer line at most, never a restatement.
**`signing#110` is over its limit**: do not grow it. **`embarch-core/open.md` is
in reserve** (893 B left; its compaction `tasks/core/171` is blocked, In flux:
yes): do not write it.

## Done when

- [x] A Test run's study record's final hash is bound in the chained log, or the
      amend is removed; the decision says which and why.
- [x] A test checks a Test-run study's bound hash against the file on disk.
- [x] The interface doc names the binding entry.
- [x] Gate green (`cargo build`, `test`, `clippy --all-targets -- -D warnings`).
