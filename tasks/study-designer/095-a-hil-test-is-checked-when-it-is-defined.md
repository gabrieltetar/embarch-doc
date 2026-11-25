# 095 — A HIL test is checked when it is defined

**State:** claimed by agent/study-designer/095-a-hil-test-is-checked-when-it-is-defined, 2026-11-25 06:12
**Source:** EMB-354 — a HIL test is not checked when it is defined
**Issue:** EMB-354
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`verdicts::acceptance_width` refuses a too-narrow limit given numbers, and
nothing calls it on a definition; no check exists for the other rules the HIL
design puts at definition time. When this is done, the crate has one function,
`check_test(test, study, bench, sources) -> Result<(), Vec<Refusal>>` (the exact
argument types are yours, built on `hil_test.rs`'s `TestDef` and
`SuiteManifest` from `study-designer/094`), and each refusal names the test,
the field and the reason. It refuses:

- **A bench with no DUT**, naming the bench (`embarch-doc/notes/hil/03-test.md`,
  "Benches"; `notes/hil/13-research-phase.md`).
- **A source with no declared `U`, resolution or range**, by name (03, "The
  verdict"). A `dut` measurement's come from the test's `sources`; an
  instrument's from its declaration; a bench board's from its
  characterisation. Instrument metrology does not exist in `embarch-topology`
  yet (EMB-358, a later suite pass), so take an instrument's numbers as an
  input to the function rather than reading a topology type.
- **A limit no result could be judged against**: `acceptance_width` with `U`,
  then with the resolution.
- **A prompt with no kind**, and **an action prompt** whose confirming
  measurement is not `by: bench` or feeds no limit or `until` that can fail
  (`notes/hil/12-prevention.md`, "Operator prompts, by kind").
- **An energising step after a setup or action prompt with no clearance prompt
  between them** (12, same section). What energises: an instrument set, and any
  bench-board line the bench does not list as read-only; every DUT line, since
  Core cannot classify it. The owner may strike this: the alternative lists
  energising lines per board and treats the rest as read-only (plan choice 5).
- **A precondition its bench does not declare**: `power_cycle` and `detach`
  need the bench to say how (plan choice 21).
- **A test whose study is a dev-bench study**: "not in this phase". The owner
  may strike this: running both kinds now is the alternative (plan choice 18).
- **Two limits on one measurement.** `derived_diff` keys limits by measurement
  name, so a second limit on the same name would hide a change to the first
  (the reviewer's note on `study-designer/094`); refuse it here.

`energises(step, bench)` is public: Core will use it for the go card and the
prompt's "outputs on" line.

This is additive inside the `hil-test` feature. If you find you must change a
public type a consumer already builds (anything outside `hil_test.rs`), stop and
say so in this file rather than doing it: that would be a cross-repo pass.

## Why now

EMB-354 is the next link of the HIL Test chain after `study-designer/094`: the
selection expansion (EMB-355) and Core's definitions and confirmations
(EMB-363) wait on it, and embarch-api and Core must refuse the same test for the
same reason. Design: `embarch-doc/notes/hil/14-implementation-plan.md`.

## Where the doc goes

`interfaces/hil-tests.md` lists every check; the energising rule gets a new
decision in `decisions/hil-tests.md` (beside 109), marking the plan choices the
owner may strike. **Decisions near their per-decision limit
(`check-doc-size.py --pressure`):** `host-parse.md` 108 (188 B left),
`authoring.md` 73 (130 B left), `versioning.md` 12 (67 B left); do not grow
them. If your work pushes a file into reserve, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit per
`tasks/README.md`.

## Done when

- [ ] One fixture per refusal above, each refusal naming the test, the field
      and the reason.
- [ ] The example test in `interfaces/hil-tests.md` passes every check.
- [ ] A raw DUT exchange after an action prompt with no clearance between is
      refused; with a clearance prompt between, it passes.
- [ ] `hil-tests.md` lists every check, and a decision records the energising
      rule.
- [ ] Gate green under no features, `hil-test`, and `--all-features`.
