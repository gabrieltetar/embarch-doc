# 180 — A Test run's Exchange steps record their target in the signed files

**State:** open
**Source:** EMB-586 — Record each Exchange step's target (DUT or bench) in the signed files
**Issue:** EMB-586
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`test_executor::judge_steps` gives each `Exchange` step a target,
`target_of(origin(signal))`, with the origin read from Core's live topology by
`measurements::topology_signal_origin` when the study runs. A refusal on a
bench board judges as `error` (`bench_step_failed`); the same refusal on the DUT
judges as `fail` (`step_failed`). That target is written nowhere: not in
`events.json`, not in the study record, not in the Test run's record. So a
Test run's zip cannot say which it was, and `embarch-api`'s `verify` (api
decision 146, check 3) reads each refused or `until`-not-seen step under both
targets and goes partial where the two disagree.

When this is done, every step of a Test run's study that addressed an
`Exchange` signal records the target `judge_steps` gave it, in a file a signed
record covers, so a reader of the zip can recompute the verdict without the
live topology. The issue's direction offers two places: a `target: "dut" |
"bench"` on each `events.json` step row that has a `signal`, or a `targets`
map (signal to target) on the study record's `test` part. Pick one and say why
in the decision; the test is that `verify` can read it without re-deriving
anything from the topology, and that a host study run outside a Test run is
unchanged unless the change is free and harmless there too (say which).

**What the recorded value must be.** The same `Target` the verdict was judged
with, taken from the same origin lookup at the same moment, never a second
lookup that could disagree with it. A signal whose origin was not found must
record what `target_of(None)` judged, stated as such.

**Concurrent work, and what is not yours.** `api/216` runs beside you, in
`embarch-api` (the Test PDF's per-limit rule and `verify` check 6). Teaching
`verify` to read the new field and drop its partial is api's follow-up: name
the field and the file precisely in your report and in the interface doc, and
the supervisor files it. Do not edit `embarch-api` or the study designer.

## Where to look

- `src/test_executor.rs` (`target_of`, `judge_steps`, where the executor builds
  the study's events and record), `src/measurements.rs`
  (`topology_signal_origin`), `src/host_study.rs` (`run_job_with_origin`), the
  study record's `test` part and what signs `events.json`
- `embarch-doc/embarch-core/interfaces/host-studies.md`,
  `interfaces/publish.md`, `interfaces/test-runs.md`; the test-run decisions
  (`decisions/test-run-*.md`, 135 to 154)
- `embarch-doc/notes/hil/06-report-and-publish.md` ("Verify", check 3)

## Where the doc goes

A new core decision in a `decisions/test-run-*.md` topic file that has room (or
a new one), with an index row, and the field named in the interface doc that
describes the file it lands in. **Over or near their limit, do not grow:**
`signing#110`, `analog-capture#127`, `host-study#95`, `definitions#133`,
`lease#93`, `stopping-a-study#128` (all over), `run-log#111` (120 B left),
`test-run-go#135` (132 B left), `instruments#104` (144 B left). **`open.md` is
3,917 B, 2 B under its reserve line**: leave it alone, or if you must add to it,
file `tasks/core/<NNN>-compact-core.md` in the same commit (`tasks/README.md`
has the shape; number from `scripts/check-task-numbers.py --next core`).
`spec.md` is 9,011 B; a sentence there is fine only if it is needed.

**Decision numbers:** the next core decision is the next free number in
`decisions.md`'s index when you write it (155 at the time of writing); cite
that one, and only that one, in code comments. Two recent units cited a
neighbour's number.

## Done when

- [ ] Each step of a Test run's study that addressed an `Exchange` signal
      records the target `judge_steps` gave it, in a file a signed record
      covers; a unit test shows a bench-signal refusal and a DUT-signal
      refusal recording different targets and judging `error` and `fail`.
- [ ] `interfaces/host-studies.md` or `interfaces/publish.md` names the field.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`).
- [ ] Decision with index row; `changelog.d/` fragment.
