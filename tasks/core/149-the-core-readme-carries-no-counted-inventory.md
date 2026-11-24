# 149 — The Core README carries no counted inventory

**State:** claimed by agent/core/149-the-core-readme-carries-no-counted-inventory, 2026-11-24 03:45
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

- [ ] `embarch-core/README.md` states no endpoint or file count or list, and
      links the interface docs that own them.
- [ ] `cargo build` and `cargo test` still green in `embarch-core`
      (README-only change; `clippy` as the gate requires).
- [ ] `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
