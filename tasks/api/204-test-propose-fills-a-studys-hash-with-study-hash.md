# 204 — `test-propose` fills a study's hash with `study_hash`

**State:** blocked — needs `hil_test::study_hash` on `embarch-study-designer`'s main, which `study-designer/101` lands
**Unparks when:** study-designer/101 has landed
**Source:** EMB-570 — the reviewer's finding on `study-designer/099`: `test-propose` hashes a study's bytes, which the crate's new refusal rejected
**Issue:** EMB-570
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`src/hil_repo.rs` (around lines 186 to 203) fills `def.study.hash` with
`sha256_hex(pretty(&study))`, the SHA-256 of the study file's bytes as written,
or refuses a given hash that differs from it, then calls `check_test`.
Study-designer decision 113 (landing with `study-designer/101`) fixes the hash
as `hil_test::study_hash`, the SHA-256 of the study's canonical JSON, and
`study-designer/100` will make `check_test` refuse any other value. On
2026-11-25 the refusal landed first and four tests in
`tests/test_propose_cli.rs` went red, so it was reverted. When this is done:

- `hil_repo.rs` fills and compares `study.hash` with
  `embarch_study_designer::hil_test::study_hash(&study)`; nothing in the crate
  hashes a study's bytes.
- The refusal's message still names both hashes.
- Every test fixture that carries a study hash (`tests/test_propose_cli.rs`,
  `tests/run_test_cli.rs` near line 66) uses `study_hash`, so the suite stays
  green when `study-designer/100` lands.

## Where to look

- `src/hil_repo.rs`, `tests/test_propose_cli.rs`, `tests/run_test_cli.rs`
- `embarch-doc/embarch-api/decisions/test-plans.md` (line 13: "the SHA-256 of
  the study file's bytes as written"), the decision this reverses
- `embarch-doc/embarch-study-designer/decisions/hil-tests.md` decision 113;
  read only

## Where the doc goes

The test-plans decision amended in place, saying the hash is `study_hash` and
why (one function, so Core, the crate and the api cannot disagree), with the
bytes convention recorded as the rejected alternative; a row in
`embarch-decision-reversals.md` is the supervisor's, so name it in your report
rather than writing it. `check-doc-size.py --pressure` lists test-plans#134
over its limit: do not grow that entry; if the amendment needs room, put it in
a new decision that supersedes the line. `embarch-api/spec.md` is in reserve
(`tasks/api/201`, blocked, `In flux: yes`): do not write it in this unit.

## Done when

- [ ] `hil_repo.rs` uses `study_hash` for both the fill and the comparison.
- [ ] `cargo test --workspace` is green against `study-designer/101`'s crate
      and stays green with `study-designer/100`'s refusal applied (the first
      reverted pass of `study-designer/099`, `7391457`, is that refusal).
- [ ] The decision records the change and the rejected alternative.
- [ ] Gate green, the client crate included.
