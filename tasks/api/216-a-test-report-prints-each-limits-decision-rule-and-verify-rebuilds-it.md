# 216 — A Test report prints each limit's decision rule, and `verify` rebuilds it

**State:** open
**Source:** EMB-588 — A Test report omits each limit's decision rule, and verify skips it
**Issue:** EMB-588
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Core decision 154 (`core/179`) adds two fields to each `tests[]` entry of a
Test run's `report-data.json`: `decision_rule` (`{kind, w_multiple}`) and
`limits` (each `measurement`, `unit`, `lower`, `upper`, `expect`, `rule`,
`w_multiple`, `u`, `k`, `u_declared`, `w`; `limits` is `[]` for a test with
none, and both are `null` when Core could not find the test in `run.json`).
embarch-api does not use them yet:

- `publish`'s Test PDF (decision 144, `src/publish_test.rs`) still says the
  limit and decision rule of each test are not carried, twice (the roll-up
  rules paragraph and the appendix's "Not carried in this report" line).
- `verify`'s check 6 (decision 146, `src/verify_test.rs`) rebuilds
  `report-data.json` field by field without these two fields, so a real Test
  zip from a Core carrying 154 fails check 6.

When this is done:

- **The PDF prints, per test, each limit with its rule, `w` and `U`** (`U` is
  `k × u`, the expanded uncertainty the test was judged with). Under simple
  acceptance it adds the false-accept sentence `notes/hil/03-test.md` asks for
  (read it for the wording's intent; do not invent a probability it does not
  give). Where `u_declared` is false it says "U not declared" rather than a
  number. A test whose two fields are `null` says so in words, never a blank.
  Both "not carried" sentences lose the per-limit rule.
- **`verify` check 6 rebuilds both fields from `run.json`**, by test id and
  definition hash, as Core does, and compares them with `report-data.json`;
  a mismatch fails check 6 naming the test. Check 4 (the PDF's text) admits the
  numbers the PDF now prints, the way it admits the others.
- **A Study zip verifies exactly as today.**

**Read Core's real shape, do not guess it.** Core's
`src/test_publish.rs` and `embarch-doc/embarch-core/decisions/test-run-publish.md`
(154) on `origin/main`: `git -C <the embarch-core main checkout> fetch -q &&
git -C <the embarch-core main checkout> show origin/main:src/test_publish.rs`.
In particular: `u` and `k` are the test's declared source for the measurement,
not the study record's own per-measurement uncertainty; `w` is `w_multiple × u`
under a guard band and 0 under simple acceptance; a guard-band measurement with
no source reads `u` null, `u_declared` false, `w` 0. `api/213` once guessed a
Core shape (`n_of_m` as an array; Core writes `{n, m}`) and the fix was a
landing patch.

**Concurrent work, and what is not yours.** `core/180` runs beside you and adds
each Exchange step's target to `events.json`; check 3's reading of a step
under both targets is not this task. Do not touch `embarch-core-client`: a
`suite` task (`tasks/suite/065`) edits its `study_events.rs` after you.

## Where to look

- `src/publish_test.rs` (lines near "are not carried in report-data.json" and
  "Not carried in this report"), `src/verify_test.rs` (check 6), the Test zip
  fixture its tests use
- `embarch-doc/embarch-api/decisions/publish-test-run.md` (144),
  `decisions/verify-test-run.md` (146); `interfaces/publish.md` ("A Test run's
  zip": its last sentence lists the per-limit rule as not built),
  `interfaces/verify.md`
- `embarch-doc/notes/hil/03-test.md` (statement of conformity, decision rule,
  false accept)

## Where the doc goes

A new api decision for the per-limit print and check 6's two fields, beside
144 and 146, with 144's and `interfaces/publish.md`'s "not built" lines
trimmed rather than grown. **Over or near their limit, do not grow:**
`lease#90`, `test-plans#134`, `ledger#98`, `bench-exchange#89`,
`failure-reporting#67`, `publish-test-run#144` (204 B left). **`spec.md` is
9,019 B and its reserve line is 9,039 B** — 20 B away: one added clause puts it
in reserve. Leave it alone if you can; if you do push it in, file
`tasks/api/<NNN>-compact-api.md` in the same commit (`tasks/README.md` has the
shape; number from `scripts/check-task-numbers.py --next api`).

**Decision numbers:** the next api decision is the next free number in
`decisions.md`'s index when you write it; cite that one, and only that one, in
code comments. Two recent units cited a neighbour's number.

## Done when

- [ ] A fixture Test zip carrying both fields passes `verify`; the same zip
      with one limit's `w` altered in `report-data.json` fails check 6 naming
      the test.
- [ ] The Test PDF prints each limit's rule, `w` and `U` ("U not declared"
      where `u_declared` is false), the simple-acceptance sentence, and no
      longer says the per-limit rule is not carried.
- [ ] A Study zip still passes `verify` as today.
- [ ] Gate green (`cargo build --workspace`, `cargo test --workspace`,
      `cargo clippy --workspace --all-targets -- -D warnings`).
- [ ] Decision written; 144 and `interfaces/publish.md` trimmed; `changelog.d/`
      fragment; the `api-360` feature row's caveat if it names the per-limit
      rule as missing.
