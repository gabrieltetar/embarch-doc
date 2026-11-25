# 096 — Expand a test selection into the resolved run file

**State:** done — expand, RunJson, selection record, decision 111, gate green
**Source:** EMB-355 — nothing expands a test selection into the resolved run file
**Issue:** EMB-355
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

A Test run is one resolved file, `run.json`, whose keys
`interfaces/hil-run.md` fixes, and nothing writes or reads one. The HIL design
has embarch-api resolve a selection into `run.json` and Core re-expand it
through this crate, refusing one it does not reproduce
(`embarch-doc/notes/hil/03-test.md`, "A run"; the run record holds "the
selection as Core expanded it at the go", every applicable test with its
status, item 10). When this is done, the crate has one pure, deterministic
expansion both call, inside the `hil-test` feature, beside `hil_test.rs` and
`hil_check.rs`:

- `expand(suites, plan, dut_inputs, benches, confirmations) -> (RunJson,
  <selection record>)`. The argument types are yours, built on `hil_test.rs`'s
  `SuiteManifest`, `Plan`, `DutInputs`, `SuiteBench` and `Capability`.
  **`hil_test.rs` already has a public `Selection` enum** (a plan's picks by id
  or tag): name the record something else, or say in the decision why you
  renamed the enum.
- **Applicability first**, over the DUT's role and capabilities and the benches
  that exist; then the plan's picks. Every test of the suite applicable to the
  inputs gets one status in the record: selected; `not_applicable` with the
  condition; `hook_unmapped`; `not_selected`; `bench_missing`.
- **A template** expands once per value of its capability, ids suffixed
  `#<n>`, `expanded_from` set, its `{capability.<field>}` placeholders filled
  in the study and the limits; each expanded study is written out with its own
  hash for the caller to send with `run.json`.
- **A measurable capability's check** (a declared or decoded value against the
  measured one) runs first on its bench, and every test expanded from that
  capability `requires` it (03, "The DUT's inputs").
- `requires` **closure**, and **bench order**: the plan's, else the suite's.
- **Each bench entry carries its bench boards' idle and hello lines** from the
  suite's bench; `hil-run.md` amended.
- `run_id` is written by the caller, a fresh random id; the function takes it
  as an argument and Core refuses one it already holds. The owner may strike
  this: Core assigning it is the alternative (plan choice 9). The decision must
  say so.
- **The canonical hash** of `run.json` through the existing `canonical_json`
  (RFC 8785), and `duration_bound(run_json)` from every step's timeout, run
  count and prompt deadline.

This is additive inside `hil-test`. If you find you must change a public type a
consumer already builds outside `hil_test.rs` and `hil_check.rs`, stop and say
so in this file rather than doing it: that would be a cross-repo pass.

## Why now

EMB-355 is the next link of the HIL Test chain after `study-designer/095`:
Core's prepare route (EMB-364), the shared verdict function (EMB-356) and
embarch-api's test plan (EMB-376) all wait on it. Design:
`embarch-doc/notes/hil/14-implementation-plan.md`, `notes/hil/03-test.md`
("Selecting and rerunning", "The DUT's inputs"), `notes/hil/04-premade-suites.md`.

## Where the doc goes

`interfaces/hil-run.md` amended for the bench entry and `run_id`, and the
expansion's statuses; a new decision in `decisions/hil-tests.md` (beside 109
and 110) for the expansion rules and plan choice 9. **Decisions near their
per-decision limit (`check-doc-size.py --pressure`):** `host-parse.md` 108
(188 B left), `authoring.md` 73 (130 B left), `protocols.md` 58 (121 B left),
`versioning.md` 12 (67 B left); do not grow them. No `study-designer` file is
in reserve. If your work pushes one into reserve, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit per
`tasks/README.md`.

## Done when

- [x] The same inputs give the same bytes and hash twice; reordering the
      suite's tests in the file does not change them.
- [x] A template over three PDOs gives three test entries; an unmapped hook
      gives `hook_unmapped`; a test on a bench that does not exist gives
      `bench_missing`.
- [x] A capability check is first on its bench and is in the `requires` of
      every test expanded from it.
- [x] `duration_bound` of a fixture equals the hand-summed timeouts.
- [x] `hil-run.md` amended for the bench entry and `run_id`, and a decision
      records the expansion and plan choice 9.
- [x] Gate green under no features, `hil-test`, and `--all-features`.

## Done

`src/hil_expand.rs` (feature `hil-test`), `tests/hil_expand.rs`, decision 111, `interfaces/hil-run.md` ("Expansion") and `hil-tests.md` amended. Decisions taken, each recorded in 111:

- `expand(suite, plan, dut, ctx)` returns an `Expansion {run, selection, studies}`, not the bare pair the task sketched, since the expanded studies must go out beside `run.json`.
- The record is `SelectionRecord`; `hil_test::Selection` untouched.
- **Additive, optional fields** (skipped when empty, so no existing file or hash changes): `TestDef.applies_when`, `TestDef.hooks`, `TestDef.checks`, `Plan.bench_order`. The notes named applicability, hooks, capability checks and plan bench order but the types had no home for them. `derived_diff` reads the three test fields. No consumer builds these types outside `hil_test.rs`/`hil_check.rs` (nothing turns `hil-test` on).
- `run.json` gained `boards` per bench, `sources`, `hooks`, `step_budget_ms` per test, `expect` per limit; setup terms carry `k` instead of `scope`. `duration_bound` reads `step_budget_ms`, so it needs no study.
- Plan choice 9 (`run_id` the caller's) is in decision 111 as strikable by the owner.
- A numeric limit cannot hold a `{capability.<field>}` placeholder (the type is `f64`); templates carry it in measurement names and `expect` values.

Not done: `SuiteTest.hash` vs the definition, `revision_range` vs the standard's revision, dev-bench studies.

Hardware-verification debt: none (host-only).
