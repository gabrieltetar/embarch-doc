# 152 — Core refuses a study with a tap no step subscribes to

**State:** claimed by agent/core/152-core-refuses-a-study-with-a-tap-no-step-subscribes-to, 2026-11-24 13:22
**Source:** EMB-308 — a study with an unsubscribed GATT notify tap is refused only in the UI's authoring path
**Issue:** EMB-308
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Core's study submit path (`src/study.rs`, where it already calls
`validate_wait_budgets` and `validate_monitor_windows`) also calls the
`Study` method `study-designer/093` adds, and refuses the study with its
message. `embarch-api`'s `run_study` submits through this path, so it is
refused the same way with no api change; say so in Core's interface doc.

A test submits a study whose GATT notify tap no step subscribes to and gets
the refusal.

## Why now

EMB-308: an agent's study that captures nothing passes today.

**Burndown leg: no new numbered decision.** Core decision 90 already says the
crate computes these checks and Core does not restate them.

## Done when

- [ ] Core refuses the study at submit; a test covers it.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped.
