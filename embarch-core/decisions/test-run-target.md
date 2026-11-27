# embarch-core decisions: A step's target in the signed events

**Status:** active, 2026-11-26 (`tasks/core/180`, EMB-586; decision 155; `notes/hil/06-report-and-publish.md`, "Verify", check 3). Index: [../decisions.md](../decisions.md). Surface: [../interfaces/host-studies.md](../interfaces/host-studies.md). Builds on [test-run-executor.md](test-run-executor.md) (136: `target_of` and the judging) and [host-study.md](host-study.md) (95).

### 155 — Each `Exchange` step row of `events.json` records `signal` and `target`

**The problem.** A refusal on a bench board judges `error` (`bench_step_failed`), the same refusal on the DUT `fail` (`step_failed`), and the target came from topology read live while the study ran, written nowhere. A reader of the zip could not recompute check 3 without the machine's topology.

**Chosen: a `target` on the step's own row in `events.json`**, beside a new `signal` (the name the step addressed). `target` is `"dut"` or `"bench"`; both fields are on `Exchange` rows only, so a row of any other step has neither. `events.json` is a subject of the study's signed record and of the Test run's, so the value is covered with no new file. **Why the row and not a `targets` map on the study record's `test` part:** the record is sealed after the study, so a map would need the executor to write after the seal, or the study to know it is in a Test run; the row is written by the study as the step ends, and `verify` reads the step it is already judging, with nothing to join.

**The same lookup, not a second.** `run_job_with_origin` resolves the signal's origin once as each step ends and records `target_of(origin)` (decision 136) there. **`judge_steps` reads that recorded `target` first** and falls back to the live origin only for a row without one (a record written before this), so the verdict and the record cannot disagree. A signal topology no longer declares records what `target_of(None)` judges, `dut`; the record does not say it was not found.

**A host study outside a Test run records the same fields.** It costs one topology read per `Exchange` step and the rows only gain two keys; nothing reads them there. Left on rather than made conditional, so the file has one shape.

**Verify's side** (embarch-api's, not done here): for an `Exchange` row, read `target` and drop the both-targets reading of a refused or `until`-not-seen step.

**Measured:** unit tests: a study over a DUT signal, a bench board's signal, an undeclared signal and a `Wait` records `dut`, `bench`, `dut` and nothing; a refusal on each judges `fail` and `error` from the recorded target even when the live topology has flipped. **Not run:** a Test run on a bench, which changes nothing the fake does not already show.
