# 082 — A one-shot monitor inside an open window is refused when the study is built

**State:** done
**Source:** `embarch-dev-bench` decision 55 (`tasks/dev-bench/042`, landed 2026-11-10), which refuses the step at run time
**Issue:** EMB-131
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`embarch-dev-bench` decision 55 makes the bench refuse a `GattMonitorAll` or `GattMonitorSelected` step while a window opened by `GattMonitorStart` or `GattMonitorSelectedStart` is still open: the step fails with `a monitor window is open; Stop it before this step`. The crate accepts the same study, so an author learns it only from a failed step on real hardware.

The bracket is static. Walking `Study.steps` in order, a window opens at a `GattMonitorStart`/`GattMonitorSelectedStart`, closes at the next `GattMonitorStop`, and a second `Start` while one is open replaces it (dev-bench decision 28, amended 2026-11-10). `continue_on_fail` does not change the bracket. A `Stop` with no open window stays legal (crate decision 36).

Add the check to the crate, following `Study::validate_wait_budgets` (decision 83) as the precedent:

- a `Study` method returning an error that names the one-shot step's index and the step that opened the window;
- `build_study` (`src/study_builder.rs`) refusing such a study the way it refuses a zero wait budget, so the UI builder cannot emit one.

**Core's pre-flight is a separate unit.** `embarch-core`'s `src/study.rs` calls `study.validate_wait_budgets()` before dispatch; calling the new method there is a one-line change in another repo, filed by the supervisor once this lands. Do not touch it here. The new method is additive, so Core and every other consumer still compile unchanged.

**Doc reserve:** `interfaces/types.md` is 11,051 of 12,288 B, 8 B short of its reserve. A sentence in its monitor rows spends it, so the same commit files `tasks/study-designer/<NNN>-compact-study-designer.md` (`tasks/README.md` has the shape; `scripts/check-task-numbers.py --next study-designer` gives the number).

## Why now

The run-time refusal landed today. A refusal at authoring time costs nothing at the bench and tells the author which step to move; the same split already exists for a zero wait budget.

## Done when

- [x] A study with a `GattMonitorAll` or `GattMonitorSelected` step between a `GattMonitorStart`/`GattMonitorSelectedStart` and its `GattMonitorStop` is refused by the new method, naming both steps, with a test.
- [x] A one-shot before the `Start`, after the `Stop`, or in a study with no window still validates, with tests; so does a `Stop` with no open window.
- [x] `build_study` refuses the bracketed one-shot, with a test.
- [x] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green, including `--no-default-features` if the crate's CI builds it that way.
- [x] A new numbered decision in `embarch-study-designer` records the rule and points at dev-bench decision 55; `interfaces/types.md`'s monitor rows say a one-shot inside an open window is refused; `changelog.d/` fragment dropped.
