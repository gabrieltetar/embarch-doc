# 104 — The umbrella README carries no counted inventory

**State:** open
**Source:** suite review audit, 2026-11-23: three code-repo READMEs describe the suite as of September
**Issue:** EMB-297
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`embarch-umbrella/README.md` says "both binaries" where `suite/user-guide.md`
says three, and its command table omits commands the `Command` enum in
`src/main.rs` has (among them `verify-release`, `deploy-core`, and the
`--uninstall` and `--dry-run` forms).

When this is done the README says what the repo is, where the guide is and
how to build, carries **no counted inventory and no command list**, and points
at the owning docs (`embarch-doc/embarch-umbrella/interfaces*` and the user
guide) instead. The glossary already states the precedent: no counts or
constant values in a page that goes stale.

## Why now

The README is the first thing anyone arriving from GitHub reads. EMB-297,
split with `api/186` and `core/149`.

**Burndown leg: no new numbered decision.** None should be needed.

## Done when

- [ ] `embarch-umbrella/README.md` states no binary or command count or list,
      and links the docs that own them.
- [ ] `cargo build` and `cargo test` still green in `embarch-umbrella`
      (README-only change; `clippy` as the gate requires).
- [ ] `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
