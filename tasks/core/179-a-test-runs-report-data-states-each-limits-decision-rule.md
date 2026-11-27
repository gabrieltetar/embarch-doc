# 179 — A Test run's `report-data.json` states each limit's decision rule

**State:** open
**Source:** EMB-585 — a Test run's report-data carries no per-limit decision rule
**Issue:** EMB-585
**Scope:** core
**Hardware:** none
**Owner:** no

## What

The Test report must state each limit's decision rule — simple acceptance, or a
guard band with w as a stated multiple of the measurement's `U` — per
`notes/hil/03-test.md`, "The verdict" and the paragraph on checking a limit
against what can measure it. `POST /test-runs/{id}/report-data`
(`src/test_publish.rs`, core decision 148) writes `rules` as the roll-up's
behaviours only, and `tests[]` holds no limit, `U`, w or rule, so
`embarch-api`'s Test PDF (api decision 144) says the per-limit rule is not
carried. When this is done, `report-data.json` lists, **per test, each limit
with its decision rule, w and the measurement's `U`** (with its coverage factor
if the record carries one), read from the study records the run amended — a
schema addition, deterministic, no clock. Where the records do not carry a
field, say so in the data rather than inventing it, and record which.

**Downstream, not yours:** `embarch-api`'s `publish` prints these and its
`verify` check 6 recomputes them (`api/215`, which may land before you, builds
check 6 against the shape it read). Say in your report exactly which fields you
added, so the supervisor files the api follow-up.

## Where to look

- `src/test_publish.rs` (the report-data builder), the Test run record and
  executor code that hold the limits (`src/test_executor.rs`, `src/test_run*.rs`)
- `embarch-study-designer`'s limit and decision-rule types (`src/verdicts.rs`
  and wherever a test's limits are declared) — read them; do not mirror a shape
  by guess
- `embarch-doc/embarch-core/decisions/test-run-publish.md` (148),
  `interfaces/publish.md` (the `report-data.json` field list)

## Where the doc goes

Amend 148 if it stays under its limit, else a new decision it points to;
`interfaces/publish.md`'s `report-data.json` list names the new fields.
**Over or near their limit, do not grow:** `test-run-go#135` (95 B left),
`run-log#111` (120 B), `instruments#104` (144 B), `signing#110`, `host-study#95`,
`lease#93` (all over). **`open.md` is in reserve** (4,227 of 5,120 B); this
task should not need it — if it does, compact it in the same commit, keeping
`tasks/core/171`'s `Must not delete:` list.

**Decision numbers:** cite the number you actually wrote, in code comments too;
twice in a row a worker cited a neighbouring decision's.

## Done when

- [ ] `report-data.json` of a Test run lists, per test, each limit with its
      decision rule and w (and `U`).
- [ ] A unit test over a fixture run with a guard band and one with simple
      acceptance asserts both.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`).
- [ ] Decision and interface updated; `changelog.d/` fragment.
