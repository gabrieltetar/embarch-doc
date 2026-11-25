# 101 — `study_hash` lands alone: one function fixes a premade study's hash

**State:** open
**Source:** EMB-555 — the additive half of `study-designer/099`, which landed and was reverted on 2026-11-25 (code `1dfdae1`, doc `29869b13`)
**Issue:** EMB-555
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## Why 099 was reverted, and what this keeps of it

099's pass (code `7391457`, doc `a9c73a20`, both in `main`'s history under
their reverts) added `hil_test::study_hash` **and** made `hil_check::check_test`
refuse a study that does not hash to `study.hash`, in one step. Both consumers still
compute the hash the old way: `embarch-api`'s `src/hil_repo.rs` fills
`study.hash` with the SHA-256 of the study file's bytes as written (api's
test-plans decision), so four tests in its `tests/test_propose_cli.rs` went red,
and one `embarch-core` test (`definitions::tests::a_test_with_its_study_and_bench_gets_the_definition_time_checks`)
did too. The crate and its consumers have to move in order, so this unit is now
the additive half only:

1. **This unit**: `study_hash` lands, and nothing refuses yet.
2. `api/204` moves `embarch-api`'s `hil_repo.rs` to `study_hash` (EMB-570)
   and `core/166` moves Core's fixture and its prepare to it.
3. `study-designer/100`: `check_test` refuses a mismatch.

**Start from 099's pass**: `git revert 1dfdae1` in the code worktree and
`git checkout a9c73a20 -- embarch-study-designer changelog.d/study-designer-099-study-hash.added.md`
in the doc worktree bring it back (099's task file is retired; leave it so). Keep `study_hash`, its pinned test and decision 113's
convention, take the `StudyHashMismatch` rule and its test out of
`hil_check.rs`, and amend 113 to say the refusal is `study-designer/100`'s. Also correct `decisions/hil-shapes.md` and
`interfaces/hil-shapes.md`, which still say a hash is over the file's bytes as
written (the reviewer's note).

## What

`TestDef.study.hash` is documented as the hash of the signed study file, but
nothing fixes how that hash is computed for a premade (non-template) study. An
expanded template's hash is the SHA-256 of its canonical JSON, computed in
`hil_expand::expand`. When this is done:

- **One pure function** in `hil_test` gives a study's hash by one fixed
  convention, the same one an expanded template's hash already uses. Core,
  `embarch-api` and later `check_test` all call it; nobody re-derives it.
- `check_test` behaves exactly as on `main` today.

## Where to look

- `src/hil_test.rs`, `src/hil_expand.rs` (`expand`, the template hash),
  `src/hil_check.rs` (`check_test`)
- `embarch-doc/embarch-study-designer/decisions/hil-tests.md` (109) and
  `hil-shapes.md`
- `embarch-api/src/hil_repo.rs` and `embarch-core/src/definitions.rs`, read
  only: the two callers that must not change behaviour in this unit

## Where the doc goes

Decision 113 as 099's pass wrote it, amended as above. `check-doc-size.py
--pressure` lists streams#39, versioning#12, seals#17, protocols#58,
authoring#73, declares#40, protocol-exec#60, host-parse#108 and ble#44 near
their limits; do not grow those. No `embarch-study-designer` file is in reserve;
if your work pushes one in, file `tasks/study-designer/<NNN>-compact-study-designer.md`
in the same commit per `tasks/README.md`.

## Done when

- [ ] `study_hash` fixes the study hash for a non-template study, with a test
      that pins a known input to its hash.
- [ ] `check_test` refuses nothing new; an expanded template's hash is
      unchanged.
- [ ] Decision 113 records the convention and names `study-designer/100` for
      the refusal; `hil-shapes.md` agrees.
- [ ] Gate green. (The landing leg re-tests `embarch-api` and `embarch-core`
      against this crate after `cargo clean -p embarch-study-designer` in
      each: a path dependency swapped by symlink is not rebuilt by mtime
      alone, which is how the first pass got through.)
