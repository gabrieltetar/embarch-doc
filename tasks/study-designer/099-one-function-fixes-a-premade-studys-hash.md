# 099 — One function fixes a premade study's hash, and `check_test` refuses a mismatch

**State:** open
**Source:** EMB-555 — fix the hash convention for a premade study file and check it
**Issue:** EMB-555
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`TestDef.study.hash` is documented as the hash of the signed study file, but
nothing fixes how that hash is computed for a premade (non-template) study. An
expanded template's hash is the SHA-256 of its canonical JSON, computed in
`hil_expand::expand`; `hil_test`'s module comment defers "a study that does not
hash to `study.hash`" to a later unit. So Core's `POST /test-runs` (core
decision 134) accepts the study files it is sent unchecked and says so on the
card (`bytes_checked_against_hash: false`): a person approving the go card is
approving prompts and energising lines whose bytes nothing has checked against
the confirmed hash. When this is done:

- **One pure function** in `hil_test` (or `hil_expand`, beside the template
  case) gives a study's hash by one fixed convention, the same one an expanded
  template's hash already uses unless there is a reason recorded in the
  decision not to. Core and `check_test` both call it; nobody re-derives it.
- **`hil_check::check_test` refuses** a test whose study does not hash to its
  `study.hash`, naming the test and both hashes.
- Core's use of the function at the prepare is a separate `core` unit filed
  when this lands; this one stays in the crate.

## Where to look

- `src/hil_test.rs` (the module comment that defers this), `src/hil_expand.rs`
  (`expand`, the template hash), `src/hil_check.rs` (`check_test`)
- `embarch-doc/embarch-study-designer/decisions/` — the HIL test decisions
  (`hil-tests.md` and its neighbours)
- `embarch-doc/embarch-core/decisions/` 134 for what Core does with the hash
  today, read only

## Where the doc goes

A new decision, or an amendment to the HIL test decision that defined
`study.hash`, if it has room (`check-doc-size.py --pressure` lists the crate's
entries near their limit: streams#39, versioning#12, seals#17, protocols#58,
authoring#73, declares#40, protocol-exec#60, host-parse#108 and ble#44; do not
grow those). `interfaces/` if a public function is added. No `embarch-study-designer`
file is in reserve at filing; if your work pushes one in, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit per
`tasks/README.md`.

## Done when

- [ ] One function fixes the study hash for a non-template study, with a test
      that pins a known input to its hash.
- [ ] `check_test` refuses a study that does not hash to `study.hash`, with a
      test.
- [ ] An expanded template's hash is unchanged (its existing tests pass).
- [ ] A decision records the convention.
- [ ] Gate green.
