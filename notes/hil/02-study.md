# HIL notes: the Study mode

**Status:** draft, 2026-11-15.

## What a Study is

**A custom, almost scientific question, answered by measurement on exactly one bench.** A bench here is one DUT, zero or one dev bench, and any companion boards and instruments wired to that setup ([README](README.md#vocabulary)). Two benches in one piece of work make it a Test.

**The runner is not what makes it a Study.** A dev-bench study (`run_study`, the bench plays the DUT's BLE counterpart) and a host study (`run_host_study`, Core drives serial exchanges, instruments and operator prompts itself) are both Studies when what they produce is measurements.

**The worked example is a BLE GATT data-acquisition study**: the bench connects to the DUT, subscribes to its data characteristics, and captures what arrives, so the report can state the rate and the losses. The owner reports this path already runs on hardware; **the report half is what is missing.**

## How a Study runs (as the procedure would say it)

1. **Lease.** `lease_take` with a purpose ([01-modes.md](01-modes.md#the-lease)).
2. **The bench is the one the study expects.** The saved bench is live, and `validate` passes for the DUT and the dev bench.
3. **The firmware is the one the study declares.** The study's build declaration and `--reflash` decide whether anything is built and flashed ([studies guide §2](../../suite/studies-guide.md)); `status`'s `last_images` against the agent's own image says what is on the board now.
4. **Run.** `run_study` or `run_host_study`; `study_watch` or `study_status` until it ends.
5. **Read the losses before the data.** `list_study_streams`: every tap, its bytes, and **whether it was truncated** ([studies guide §1](../../suite/studies-guide.md)).
6. **Draft the prose the study asks for**, then **publish** ([06-report-and-publish.md](06-report-and-publish.md)).

## The report

**Its shape is free, and decided by the study itself.** Each study carries its own `report.typ`, a Typst source that reads the run's files and draws its own plots. embarch-api compiles it at publish time, so **every number in the body comes from the run's files, never typed by the agent.** The lab-report shape (question, method, setup, results, analysis, limits, conclusion) is the shape the guide recommends and the example uses, and nothing enforces it.

**Who writes each prose section is decided by the study too**, not by the procedure.

**A Study with no `report.typ` still publishes**: the audit appendix plus a data section listing each capture with its row count, so a Study is never unpublishable.

**embarch-api always appends a fixed audit appendix** that the study cannot leave out: pinned inputs, losses and overrides, the study design, operator notes and the hash manifest ([06-report-and-publish.md](06-report-and-publish.md#the-audit-appendix)).

## Where its files live

**Both study kinds are saved in the firmware repo's `embarch/studies/<slug>/`**: the study file, its `report.typ`, and the prose files the agent writes, side by side. A dev-bench study is saved under `embarch/studies/` by the Study Designer today ([embarch-ui spec](../../embarch-ui/spec.md)); **a host study is not saved in a repo at all** ([embarch-ui decision 96](../../embarch-ui/decisions/bench-configs.md)), so this is new for host studies.

**The prose the agent writes for a run is one file per run in the study's folder** (`embarch/studies/<slug>/runs/<run id>`), which `report.typ` includes by the run's ID, so a republish renders the same words.

## Open

- **Which plots Typst can draw offline.** Plot packages are normally fetched from the Typst package registry; a binary that must work offline has to vendor the ones it supports. To measure when the work starts.
- **The Study Designer UI** gains host-study rows later ([host-study proposal](../../embarch-host-study-proposal.md), "What is left" item 3); nothing in the Study mode waits on it.
