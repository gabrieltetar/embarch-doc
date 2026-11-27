# 213 — A Test run publishes as one zip

**State:** done — Test run publishes as one zip with a PDF by requirement (decision 144); mock Core only
**Source:** EMB-380 — a Test run cannot be published
**Issue:** EMB-380
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`publish` takes a Study run only ("Only a Study run publishes", `src/tools.rs`,
`src/publish.rs`). Core now has a Test run's three routes: `POST
/test-runs/{id}/report-data`, `POST /test-runs/{id}/publish` (core decisions
148, 149) and `GET /test-runs/{run_id}/publish/{revision}/files/{*name}` (core
decision 150). When this is done, `publish <run id>` (the MCP tool and the CLI
subcommand, one function behind both, api decision 112) accepts a Test run too:

- **One zip for the whole run.** Each study run's files sit under a folder of
  their own (`studies/<study_id>/...`, as Core's manifest names them); `run.json`,
  `result.json`, the signed Test run record and `report-data.json` with its
  envelope at the top; the signed manifest and both run-log segments, as Core
  signs them.
- **The PDF is built from `report-data.json` and organised by requirement**:
  each requirement's verdict with its counts and qualifiers ("pass, bench
  firmware unreleased", "pass, 3 of 5 tests run"), each test's verdict citing the
  run behind it; the tests that did not run, and why; every run of each test on
  the unit, an earlier failed one included; the unit, who gave the go and who
  published; the decision rule per limit; the audit appendix as a Study's has
  it, with `run.json`'s hash and the plan's and suite's.
- **A fixed statement** says the report is pre-compliance evidence, not a
  certification and not an accredited test report.
- **A Study run publishes exactly as before.**

The design is `embarch-doc/notes/hil/06-report-and-publish.md` ("Publish", "The
report") and `notes/hil/03-test.md` ("The report"). Where they leave a choice
open, make it and record it.

**Not in this task:** a resumed pair (EMB-370 is not built; core decision 149
says how it will publish as one) — say in your decision that it is not handled.
The JUnit and OCP exports for a Test run are EMB-381, and `verify` of a Test zip
is EMB-382; both wait on this. Do not build them.

## Where to look

- `src/publish.rs`, `src/publish_report.rs`, `src/tools.rs` (the `publish`
  description), `src/cli.rs`
- `crates/embarch-core-client/src/`: add what the three Core routes need.
  **This is a shared crate** (`embarch-ui` path-depends on it): additive methods
  only, no change to an existing type's fields, and record what you added.
- `embarch-doc/embarch-core/interfaces/publish.md` ("A Test run's publish") and
  `embarch-core/decisions/test-run-publish.md` (148 to 150): what Core serves
- `embarch-doc/embarch-api/decisions/publish.md` (112 to 114),
  `publish-revisions.md`, `report-pdf.md`; `interfaces/publish.md`

## Where the doc goes

A new api decision for the Test run's publish, in a new topic file or
`decisions/publish.md` (4.5 KB). `interfaces/publish.md`'s `run_id` row says "A
Test run does not exist in milestone 1": make it true, and give a Test run's zip
layout its own section.

**In reserve:** `embarch-api/spec.md`, 1,147 B left (out of reserve at 9,039 B).
Its compaction, `tasks/api/201`, is parked `In flux: yes`. If you write
`spec.md`, compact it out of reserve in the same commit, keeping `api/201`'s
`Must not delete:` list, and say so in your report; I close `api/201` at the
fold. **Decisions over or near their limit** (`check-doc-size.py --pressure`):
`lease#90`, `test-plans#134`, `ledger#98`, `bench-exchange#89`,
`failure-reporting#67` — do not grow any of them; point at them from the new
decision.

## Done when

- [x] A fixture Test run publishes one zip holding every study run's files,
      `run.json` and both signed records.
- [x] Its PDF names a `not_verified` requirement and the test skipped for a gap
      behind it.
- [x] Its PDF carries the fixed statement and lists an earlier failed run of a
      passing test.
- [x] A Study run still publishes as before (its existing tests pass unchanged).
- [x] The `publish` tool description no longer says only a Study run publishes.
- [x] Gate green (`cargo build --workspace`, `cargo test --workspace`,
      `cargo clippy --workspace --all-targets -- -D warnings`).
- [x] `decisions`, `interfaces` updated; `changelog.d/` fragment; a
      `features.d/` row if a feature row's caveat changed.

## Notes

- Decision 144 (`decisions/publish-test-run.md`). `spec.md` was edited and compacted out of reserve in the same commit (9,093 to 8,972 B; line for `verify` shortened, `api/201`'s `Must not delete:` items untouched).
- **Debt, not hardware:** only a mock Core has served these routes; run `publish` on a real ended Test run against a Core carrying core/175 and 177.
- Not built, by the task: a resumed pair, the JUnit and OCP exports (EMB-381), `verify` of a Test zip (EMB-382). Not possible from Core's data: the per-limit decision rule (filed to Core, EMB-585).
