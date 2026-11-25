# 166 — The Test-run prepare checks each study against its hash

**State:** open
**Source:** EMB-555 — Core's half of `study-designer/099` (`hil_test::study_hash`, study-designer decision 113)
**Issue:** EMB-555
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`POST /test-runs` accepts the study files it is sent unchecked and says so on
the go card: `src/test_runs.rs`'s `static_card` writes
`"bytes_checked_against_hash": false` for every test (core decision 134). So a
person approving the go card approves prompts and energising lines whose
content nothing has checked against the confirmed hash. `study-designer/101`
fixes the convention: `hil_test::study_hash(&HostStudy)` is the one function,
and `study-designer/100` (after this unit) makes `hil_check::check_test` refuse
a mismatch at definition time, where `src/definitions.rs` runs it. When this is done:

- At the prepare, every premade study Core was sent (the `studies` map, not an
  expanded template's, which `expand` hashes itself) is hashed with
  `study_hash` and compared with its test's `study.hash`. A mismatch refuses
  the prepare with `422`, naming the test, the file and both hashes; nothing is
  registered.
- The card's field says what was checked: `true` when the study's hash was
  checked by this rule. Rename the field only if the decision says why, since
  `embarch-ui`'s go card (`ui/124`) and `embarch-api`'s `run_test` read it.
- Nobody re-derives the hash: Core calls `study_hash`, never its own SHA-256.
- **Core's own fixtures move to `study_hash` too.** With `check_test`'s refusal
  in place (the first pass of `study-designer/099`), `src/definitions.rs`'s
  test `a_test_with_its_study_and_bench_gets_the_definition_time_checks` failed
  because its fixture's `study.hash` is not the study's `study_hash`. Fix every
  such fixture here, so `study-designer/100` (the refusal) lands on a green
  Core.

## Where to look

- `src/test_runs.rs` — the prepare, `static_card`, `kept_studies`
- `src/definitions.rs` — where `check_test` already runs
- `embarch-study-designer/src/hil_test.rs` (`study_hash`) and
  `embarch-doc/embarch-study-designer/decisions/hil-tests.md` decision 113;
  read only
- `embarch-doc/embarch-core/decisions/test-runs.md` decision 134 and
  `interfaces/test-runs.md`

## Where the doc goes

Decision 134 amended in place if it has room, else a new decision in
`decisions/test-runs.md`; the interface row for the refusal and the field.
`check-doc-size.py --pressure` lists definitions#133 over its limit and
test-run-go#135 with 95 B left: do not grow those. No `embarch-core` file is in
reserve at filing; if your work pushes one in, file
`tasks/core/<NNN>-compact-core.md` in the same commit per `tasks/README.md`.

## Done when

- [ ] A prepare whose premade study does not hash to its `study.hash` is
      refused `422` naming the test and both hashes, with a test.
- [ ] A matching study prepares, and its card says its hash was checked.
- [ ] An expanded template's study is unaffected, its tests unchanged.
- [ ] Every Core fixture's `study.hash` is `study_hash` of its study, so the
      definition-time test passes under `study-designer/100`'s refusal.
- [ ] The decision and the interface say what is checked.
- [ ] Gate green. The native Windows build is a debt the owner runs.
