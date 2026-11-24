# 149 — The Core README carries no counted inventory

**State:** done — README carries no counted inventory; points at interface docs
**Source:** suite review audit, 2026-11-23: three code-repo READMEs describe the suite as of September
**Issue:** EMB-297
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-core/README.md` gives an endpoint count and a six-file source
layout; `src/api.rs` routes several times that many endpoints and `src/` has
grown well past six files.

When this is done the README says what the repo is, where the guide is and
how to build, carries **no counted inventory and no file or endpoint list**,
and points at the owning interface docs (`embarch-doc/embarch-core/interfaces/`)
instead. The glossary already states the precedent: no counts or constant
values in a page that goes stale.

## Why now

The README is the first thing anyone arriving from GitHub reads. EMB-297,
split with `api/186` and `umbrella/104`.

**Burndown leg: no new numbered decision.** None should be needed.

## Done when

- [x] `embarch-core/README.md` states no endpoint or file count or list, and
      links the interface docs that own them.
- [x] `cargo build` and `cargo test` still green in `embarch-core`
      (README-only change; `clippy` as the gate requires).
- [x] `changelog.d/` fragment dropped.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
