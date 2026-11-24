# 071 — The linking process sets the identity store's folder

**State:** claimed by agent/topology/071-the-linking-process-sets-the-identity-stores-folder, 2026-11-24 04:02
**Source:** `notes/hil/12-prevention.md`, "The root of trust" (the protected store bullet): on an attested install the identity store lives inside Core's protected store, with Core its only writer; `notes/hil/14-implementation-plan.md`, "The later phases, in outline" (unit A.4)
**Issue:** EMB-320
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`embarch-topology` fixes the identity store's folder at
`<machine data dir>/topology/`: `paths::data_dir()` always returns it, every
`enrollment::*` and `alert::*` function goes through it, and the tests note
that the real functions cannot be pointed elsewhere. Core cannot move the
store into its protected store, so the attested phase cannot start.

When this is done the process that links the crate can set the folder once,
at start, and today's path is the default:

- A process-wide setter, `paths::set_data_dir(dir)`, callable once and before
  the first store or alert access. A second call, or a call after first use,
  is refused with an error that says which.
- Unset, every path is exactly what it is today. The CLI never calls it.
- `alert_log_path()` follows the same folder.

This is the issue's stated shape, written by the owner; take it as given.
Nothing here changes Core: Core calling the setter is a later unit.

## Why now

The HIL plan's attested phase (unit A.4, Core's store by mode) points the
identity store at `<store>/topology/` and needs this first. Every later reader
through this crate (Core's enrolment, signal, instrument and bootload routes,
the alert log) inherits the folder.

**Burndown leg: no new numbered decision.** Amend decision 23
(`decisions/storage.md`) in place: the folder is the linking process's
choice, today's path its default. If decision 43 needs a line it gets one.
Core's own docs cite decision 23 (`embarch-core/decisions/auth.md`); that is
another sub-project's file, so if anything there reads false after the
amendment, say what in this file's notes and the supervisor changes it at the
fold. Doc-size reserve: no topology file is in reserve.

**This is a shared crate.** The gate runs under every feature set a consumer
builds it with, not only defaults and `--all-features`
(`../../embarch-fleet/gate.md`, the shared-crate bullet; `Cargo.toml`'s
`[features]` comment names the set today).

## Done when

- [ ] A test sets the folder to a temp dir, enrols a board, declares an
      instrument and a signal, and finds `enrollment.toml` there and nothing
      at the default path.
- [ ] Unset, every path is what it was, and the existing tests pass
      unchanged.
- [ ] A second set, or a set after the first store access, is refused with a
      message saying why.
- [ ] `cargo build`, `test` and `clippy --all-targets -- -D warnings` green
      under every feature set the gate names.
- [ ] Decision 23 amended; `spec.md`/`interfaces/` updated where they state
      the folder; `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
