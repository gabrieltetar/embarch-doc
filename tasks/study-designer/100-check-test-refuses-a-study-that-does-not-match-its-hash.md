# 100 — `check_test` refuses a study that does not match its hash

**State:** claimed by agent/study-designer/100-check-test-refuses-a-study-that-does-not-match-its-hash, 2026-11-26 11:57
**Source:** EMB-555 — the refusal half of `study-designer/099`, split out when 099 was reverted
**Issue:** EMB-555
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

Once `study-designer/101` has put `hil_test::study_hash` on `main` and both
consumers compute `study.hash` with it (`embarch-api`'s `src/hil_repo.rs`,
EMB-570; Core's fixture and prepare, `core/166`), `hil_check::check_test`
refuses a test whose host study does not hash to its `study.hash`, as
`Rule::StudyHashMismatch` on `study.hash`, naming the study file and both
hashes. `study-designer/099`'s reverted pass wrote exactly this (code `7391457`, in
`main`'s history under its revert `1dfdae1`), so start from that diff.

## Where to look

- `src/hil_check.rs` (`check_test`), `tests/hil_checks.rs`
- `7391457`'s diff to those two files (in `main`'s history, reverted by `1dfdae1`)
- `embarch-doc/embarch-study-designer/decisions/hil-tests.md` decision 113

## Where the doc goes

Decision 113 amended in place: the refusal is in force. `check-doc-size.py
--pressure` lists streams#39, versioning#12, seals#17, protocols#58,
authoring#73, declares#40, protocol-exec#60, host-parse#108 and ble#44 near
their limits; do not grow those.

## Done when

- [ ] `check_test` refuses a study that does not hash to `study.hash`, with a
      test.
- [ ] Gate green. The landing leg re-tests `embarch-api` and `embarch-core`
      against it after `cargo clean -p embarch-study-designer` in each.
