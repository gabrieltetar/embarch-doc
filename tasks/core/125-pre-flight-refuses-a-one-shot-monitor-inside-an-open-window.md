# 125 — Core's pre-flight refuses a one-shot monitor inside an open window

**State:** claimed by agent/core/125-pre-flight-refuses-a-one-shot-monitor-inside-an-open-window, 2026-11-10 04:46
**Source:** `tasks/study-designer/082` (landed 2026-11-10, `embarch-study-designer` `6874b81`), which added the check this calls
**Issue:** EMB-131
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-study-designer` decision 89 added `Study::validate_monitor_windows()`, which refuses a `GattMonitorAll` or `GattMonitorSelected` step inside a window a `GattMonitorStart`/`GattMonitorSelectedStart` opened and no `GattMonitorStop` closed. `build_study` calls it, so the UI builder cannot emit such a study, but a hand-written or saved one still reaches the bench, where `embarch-dev-bench` decision 55 refuses the step at run time.

Core's pre-flight already calls the crate's other additive authoring check: `embarch-core/src/study.rs` `validate_study` runs `study.validate_wait_budgets()` (core decision 90, "computed by the crate, not restated"). Call `study.validate_monitor_windows()` beside it, the same way, so the study is refused before dispatch with the crate's own message naming both steps.

The method is not feature-gated, and Core already depends on the crate with `features = ["std"]`, so this needs no manifest change.

## Why now

The crate half landed today. Until Core calls it, a submitted study with the mistake still costs a bench run to find out.

## Done when

- [ ] `validate_study` refuses a study with a one-shot monitor step inside an open window, returning the crate's message, with a test beside the existing wait-budget one.
- [ ] A study with the one-shot outside every window still passes pre-flight, with a test.
- [ ] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green, and the native Windows build if this repo's gate asks for one (`../../embarch-fleet/gate.md`).
- [ ] The decision that records Core's pre-flight checks says this one runs too; `changelog.d/` fragment dropped.
