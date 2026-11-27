# 175 — Core publishes a Test run

**State:** done — two routes, decisions 148 and 149, tests green; revision-file route filed as EMB-581
**Source:** EMB-373 — Core cannot publish a Test run
**Issue:** EMB-373
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Core's publish takes one study run (`src/publish.rs`, decisions 116 to 120). The
HIL design publishes a Test run "as one zip for the whole run", organised by
requirement, with a `report-data.json` that Core writes and signs from its own
records (`embarch-doc/notes/hil/06-report-and-publish.md`, "Publish";
`notes/hil/03-test.md`, "The report"). When this is done:

- **`POST /test-runs/{id}/report-data`** builds the data from the Test run's
  record (`core/169`, `core/170`), the run log's `test_run` entries and manual
  verdicts (core decisions 146, 147), and the unit's declarations (serial,
  revision, the person's name):
  - each test's verdict and each requirement's, through
    `embarch-study-designer`'s `verdicts` roll-up (`src/verdicts.rs`), with
    their qualifiers and the per-verdict counts;
  - a manual verdict the agent relayed (`relayed: true`) listed apart, never
    counted in a requirement's verdict or coverage;
  - coverage counts from the run record's selection, and the tests that did not
    run with their reason;
  - every run-log entry for a test on this unit, failed ones included, grouped by
    test, requirement ID, DUT image and definition hash;
  - who gave the go and who published, and the fixed statement: pre-compliance
    evidence, not a certification, not an accredited test report.
- **With no atlas joined**, the standard's own requirement count is absent and
  the data says no atlas was joined (`notes/hil/04-premade-suites.md`).
- **`POST /test-runs/{id}/publish`** writes the manifest over every study run's
  files, the Test run's `run.json`, both records and `report-data.json`, signs
  it, and enters its hash in the run log, the way a Study's publish does (116 to
  120). It carries the unit's run-log segment, as a Study's publish carries one.
- **A resumed pair** (a Test run interrupted and resumed) is out of scope: resume
  is EMB-370, not landed. Say in the decision how a resumed pair will publish as
  one once it exists, and do not build it.

Reuse the Study publish's signing, manifest and segment code rather than copying
it. If a route needs a reader in `embarch-api` or `embarch-ui`, that is a
follow-up for their scope (`scripts/fleet-linear.py file --from worker
--project <repo>`); Core is the only repo you write.

## Where to look

- `src/publish.rs`: `report_data`, `publish`, `call_log_segment`, `attribution`
- `src/test_executor.rs`, `src/run_log.rs`: the Test run record and its entries
- `embarch-study-designer/src/verdicts.rs`: the requirement roll-up, read only
- `embarch-doc/embarch-core/decisions/publish.md` (116 to 120),
  `decisions/test-run-record.md` (146), `decisions/manual-verdicts.md` (147)
- `embarch-doc/embarch-core/interfaces/publish.md`, `interfaces/test-runs.md`
- `embarch-doc/notes/hil/06-report-and-publish.md`, `03-test.md`,
  `14-implementation-plan.md` (rows T.18, T.21, T.29, T.31)

## Where the doc goes

A new core decision in `decisions/publish.md` (out of reserve) for the Test run's
report data and publish. The two routes go in `interfaces/publish.md` or
`interfaces/test-runs.md`. **Decisions near their limit**
(`scripts/check-doc-size.py --pressure`): `signing#110` and `run-log#111` (120 B
left), `test-run-go#135` (95 B): write a new decision rather than grow one of
them. **`embarch-core/open.md` is in reserve** (893 B left; its compaction
`tasks/core/171` is blocked, In flux: yes, and this route is half of what unparks
it): do not write it. If you must, carry `core/171`'s compaction in the same
commit and keep its `Must not delete:` items.

## Done when

- [x] A fixture Test run publishes a signed `report-data.json` whose requirement
      verdicts equal the crate's roll-up.
- [x] A requirement with a test skipped for a gap reads `not_verified`, and the
      skipped test is listed with its reason.
- [x] Every earlier run of a test on the unit, failed ones included, is listed.
- [x] The manifest names every study run's files and is entered in the run log.
- [x] Interface doc names both routes; gate green (`cargo build`, `test`,
      `clippy --all-targets -- -D warnings`).

## Done

Decisions 148 (report data) and 149 (publish) in `embarch-core/decisions/test-run-publish.md` (a split from `publish.md`, whose 12 KB group cap the pair would have passed). Code: `src/test_publish.rs`; a Study's publish moved onto the shared `sign_manifest` in `src/publish.rs`, output unchanged. Left undone and filed: a route serving a revision's files (EMB-581). Not built: a resumed pair (EMB-370), restoring a swept Test run, requirements of tests the selection excluded.

**Hardware / deploy debt:** none for hardware. Core is not deployed; the native Windows build was not run.

