# 024 — `README.md` describes a feature set that no longer exists

**State:** open
**Source:** `tasks/study-designer/018`, found while sweeping stale `design.md` citations —
out of that unit's scope (citation format, not content).
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

This crate's own `README.md` (repo root) documents a `core-validation` Cargo feature and a
`signal` module holding `SignalCheck` evaluation logic, `PostHocValidation`, `ContentValidity`,
etc. None of this exists: `Cargo.toml`'s `[features]` table has no `core-validation` (decision
48 removed post-hoc validation outright, `decisions/removed.md` entry 48), and there is no
`src/signal.rs` or `src/validation.rs`. The README also never mentions `gatt-extract`,
`study-ui`, or `eap-parse` — three real features `Cargo.toml` has had for a while — in its
Features section, and its Layout table still lists `PowerSampleWindow` under the `study` module
row, which is also retired (see `src/study.rs`'s own tombstone comment).

Bring `README.md`'s Layout table and Features section back in line with the actual
`Cargo.toml`/`src/` shape: drop `core-validation`/`signal`/`validation`/`PowerSampleWindow`,
add `gatt-extract`/`study-ui`/`eap-parse` with a one-line description each (matching
`spec.md §3`'s feature/target-split table, which already has correct descriptions to draw
from).

## Why now

A README this stale actively misleads anyone reading it before the source — it currently
promises a feature flag that fails outright (`cargo build --features core-validation` errors:
"the package 'embarch-study-designer' does not contain this feature").

## Done when

- [ ] `README.md`'s Layout table lists only modules that exist, with no retired types named.
- [ ] `README.md`'s Features section lists every real feature in `Cargo.toml`
      (`alloc`, `std`, `ffi`, `gatt-extract`, `study-ui`, `eap-parse`), with a correct
      one-line description each.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment.
