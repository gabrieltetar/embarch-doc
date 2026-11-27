# 214 — A Test run's zip carries JUnit and OCP exports mapped from its verdicts

**State:** open
**Source:** EMB-381 — the JUnit and OCP exports carry no verdicts for a Test run
**Issue:** EMB-381
**Scope:** api
**Hardware:** none
**Owner:** no

## What

A Study's zip carries a JUnit XML and an OCP T&V JSON Lines export
(`src/publish_export.rs`, api decision 114); a Test run's zip, built by
`api/213` (decision 144, `src/publish_test.rs`), carries neither. When this is
done, a Test run's zip carries both, mapped from its verdicts by the table in
`embarch-doc/notes/hil/06-report-and-publish.md`, "Publish":

- pass: no JUnit child; OCP `COMPLETE` / `PASS`.
- fail: `<failure>`; error: `<error>`; inconclusive: `<failure
  type="inconclusive">`; cancelled: `<error type="cancelled">`.
- **a test skipped for a gap: `<error type="not_verified">`**, so a default CI
  gate fails on it; skipped as not applicable or not selected: `<skipped>`.
- every qualifier as a JUnit property and as OCP metadata; a requirement's
  `not_verified` carried in each of its tests' properties.

Shape: one JUnit `<testsuite>` per bench, one `<testcase>` per test entry of
`run.json`. OCP: a run start, one step per test with status and result by the
table, measurements with value, unit, `U` and qualifiers in metadata, a run end.
**Both are pure functions of `report-data.json` and the records in the zip**, so
`verify` (EMB-382, not this task) can regenerate them byte for byte; list them
in the manifest as this crate's files, as a Study's are. Where 06 leaves a
choice open (the OCP status words, where a measurement's `U` is read from),
make it and record it.

**A Study's exports are unchanged, byte for byte.** Not in this task: `verify`
of a Test zip (EMB-382), a resumed pair (EMB-370).

## Where to look

- `src/publish_export.rs` (the Study's exports), `src/publish_test.rs` (the Test
  run's zip, decision 144)
- `embarch-doc/embarch-api/decisions/publish.md` (114),
  `decisions/publish-test-run.md` (144), `interfaces/publish.md` ("A Test run's
  zip")
- What Core writes: `embarch-core`'s `src/test_publish.rs` on `origin/main`
  (`git -C ../embarch-core show origin/main:src/test_publish.rs` from your code
  worktree's parent, or the main checkout after a fetch); the roll-up types in
  `embarch-study-designer/src/verdicts.rs`. **Read the real shapes; do not guess
  them** — `api/213` guessed `n_of_m` as an array and Core writes `{n, m}`.

## Where the doc goes

Decision 144 amended if it stays under its limit (210 B left today, per
`check-doc-size.py --pressure`), else a new decision beside it that 144 points
to; strike "the JUnit and OCP exports (EMB-381)" from 144's "Not done" list
either way. `interfaces/publish.md`'s Test run zip layout names both files.
**Over or near their limit, do not grow:** `lease#90`, `test-plans#134`,
`ledger#98`, `bench-exchange#89`, `failure-reporting#67`. `spec.md` is out of
reserve since `api/213` (8,972 B, threshold 9,039 B): a sentence there may put
it back; if so, file `tasks/api/<NNN>-compact-api.md` in the same commit.

## Done when

- [ ] One fixture per row of 06's table gives the mapped JUnit element and OCP
      status and result.
- [ ] A qualifier on a test appears as a JUnit property and as OCP metadata.
- [ ] A Test run's zip lists both exports in Core's manifest.
- [ ] A Study's exports are unchanged (their existing tests pass unchanged).
- [ ] Gate green (`cargo build --workspace`, `cargo test --workspace`,
      `cargo clippy --workspace --all-targets -- -D warnings`).
- [ ] Decisions and interfaces updated; `changelog.d/` fragment.
