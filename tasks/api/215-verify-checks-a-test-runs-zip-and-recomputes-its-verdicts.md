# 215 — `verify` checks a Test run's zip and recomputes its verdicts

**State:** claimed by agent/api/215-verify-checks-a-test-runs-zip-and-recomputes-its-verdicts, 2026-11-26 21:22
**Source:** EMB-382 — verify cannot check a Test zip's verdicts
**Issue:** EMB-382
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`verify` (decisions 118 to 125, 140; `interfaces/verify.md`) checks a Study's
zip. A Test run's zip, built by `publish` since `api/213` and `api/214`
(decisions 144 and 145), is not recognised: check 3 answers "a Study has no
verdict; nothing to recompute". `notes/hil/06-report-and-publish.md`, "Verify",
check 3, wants every verdict recomputed so a reader of a Test report need not
trust the agent. When this is done, a Test run's zip is told from a Study's by
its own files and:

- **Check 0**: `run.json` and every study run's files (`studies/<id>/...`) are
  subjects of a signed record; the Test run's own record
  (`test-run.dsse.json`) verifies under the key.
- **Check 3**: for each test entry, its runs' verdicts recomputed through
  `embarch-study-designer`'s `judge_run` and `judge_test` with the behaviour
  versions the records name, from `run.json`'s limits, each study run's
  `events.json` and `measurements.json`, and each step's target as the record
  states it; then the requirement roll-up (`Rules::...requirement` /
  `combine`); all compared with the records and `report-data.json`. Every test
  `run.json` selected has a test record or a signed reason for its absence.
  What check 3 cannot recompute (the image readback, identities, `*IDN?`) rests
  on Core's signature, and the output says so by name.
- **Check 6**: `report-data.json` recomputed for a Test run, field by field, as
  124 does for a Study.
- **Check 7**: the JUnit and OCP exports regenerated (decision 145 made them
  pure functions of `report-data.json` and `measurements.json` for exactly
  this).
- The other checks either cover the Test run's files or answer
  `not applicable` with the reason.

**A Study's zip verifies exactly as today**, check 3's answer included.

**Concurrent work, and what is not yours.** `core/178` (an interrupted run
keeps its finished verdicts; a resume route) runs beside you; verify of an
interrupted or resumed run is not in this task, so answer such a zip with a
named `partial` or `not checked by this version` rather than guessing its
shape. The next core unit after it, EMB-585, adds each limit's decision rule to
`report-data.json`; build check 6 against the shape on Core's `origin/main`
when you read it, and the supervisor files the follow-up for the new field.

## Where to look

- `src/verify.rs`, `src/verify_report.rs`; the Test run zip's layout in
  `src/publish_test.rs` and `src/publish_test_export.rs` (or wherever 145's
  exports live)
- `embarch-doc/embarch-api/decisions/verify.md`, `verify-report.md`,
  `publish-test-run.md` (144), `publish-test-export.md` (145);
  `interfaces/verify.md`, `interfaces/publish.md` ("A Test run's zip")
- What Core writes: `embarch-core`'s `src/test_publish.rs`, its record code and
  `embarch-doc/embarch-core/interfaces/publish.md` (the `report-data.json`
  field list) **on `origin/main`** (`git -C <the embarch-core main checkout>
  fetch -q && git -C ... show origin/main:src/test_publish.rs`); the judge and
  roll-up in `embarch-study-designer/src/verdicts.rs`. **Read the real shapes;
  do not guess them** — `api/213` guessed `n_of_m` as an array and Core writes
  `{n, m}`.

## Where the doc goes

A new decision for the Test run's checks, beside 118 to 125 (which are near
nothing; 124 is check 6's), with `interfaces/verify.md`'s table saying per
check what a Test zip gets. **Over or near their limit, do not grow:**
`lease#90`, `test-plans#134`, `ledger#98`, `bench-exchange#89`,
`failure-reporting#67`, `publish-test-run#144` (199 B left). `spec.md`
(8,972 B, reserve at 9,039 B): a sentence there may put it into reserve; if so,
file `tasks/api/<NNN>-compact-api.md` in the same commit.

**Decision numbers:** the next api decision is the next free number in
`decisions.md`'s index when you write it; cite that one in code comments.

## Done when

- [ ] A fixture Test zip passes every check.
- [ ] The same zip with a verdict flipped in `report-data.json`, a test's
      record dropped, or a limit in `run.json` altered each fails, naming the
      check and the test.
- [ ] A Study zip still passes, check 3 answering as today.
- [ ] Gate green (`cargo build --workspace`, `cargo test --workspace`,
      `cargo clippy --workspace --all-targets -- -D warnings`).
- [ ] Decisions and interfaces updated; `changelog.d/` fragment; the verify
      feature row in `features.d/` if it states what verify covers.
