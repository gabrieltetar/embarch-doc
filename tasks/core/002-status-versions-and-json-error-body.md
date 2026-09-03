# 002 — `core_version`/`contract_version` on `/status`, and the `{code, message, cause}` error body

**State:** claimed by agent/core/002-status-versions-and-json-error-body, 2026-09-03 01:30
**Source:** embarch-core/open.md — "Designed, not built": "**A `{code, message, cause}` JSON error body**, and `core_version`/`contract_version` on `/status` (decisions 12, 13). The study schema version is the only one of the three that is real."
**Scope:** core
**Hardware:** none

## What

Decisions 12 and 13 designed two things Core still does not do. One or both are
worth building, and the task is to build what is worth building and retire what
is not — not to leave the docs describing a design nobody implemented.

1. **`/status` carries only the study schema version.** `core_version` and
   `contract_version` were designed and never added. `embarch-umbrella`'s
   `doctor` (its own `open.md`, check 11) wants Core's served host version, so
   there is a named consumer waiting.
2. **The `{code, message, cause}` JSON error body** was designed and never
   built, so an HTTP error's `code` enum — including `study_schema_mismatch`,
   which has never fired — is reachable by nothing.

Take each on its own merits. Building `/status` fields is small and has a
consumer; the error body is larger and touches every error path, so **it is
legitimate to build the first and record the second as a deliberate deferral
with a named trigger** rather than half-building both.

## Why now

Both are `embarch-core`'s own designed-not-built list, and the first one has a
consumer named in another sub-project's open questions this batch also filed a
task for. Two sub-projects reading the same missing field is the trigger.

## Done when

- [x] `/status` serves whatever versions were decided worth serving, with the
      shape recorded in `interfaces.md`.
- [x] Anything deliberately not built is moved out of "Designed, not built" into
      an explicit deferral with a trigger, in `decisions.md` and `open.md`.
- [x] `interfaces.md`'s `/status` row matches what the code emits, field for field.
- [x] Gate green (`embarch-parallel-agents.md` §10) — including the native
      Windows build, since `embarch-core` is involved.
- [x] `changelog.d/` fragment dropped; `status.d/` fragment for any suite-level
      fact this makes false.

## What was decided

**Built: `core_version` on `/status`**, from `env!("CARGO_PKG_VERSION")`.
Mechanical rather than hand-maintained, which is the whole reason it is worth
serving: `Cargo.toml`'s version already tracks the release tags, so the field
cannot drift from the build that answers. The gap it closes is not the one the
task named (see below) — it is that Core's version was reachable **only by
running the binary**, so nothing talking to it over HTTP could say which build
answered, and `embarch-dev-workflow.md` §4a's "`deploy-core` reports `landed`
whether or not it was" had no remote check at all.

**Retired: the hand-bumped `contract_version`.** Nothing forces the bump, so
its failure mode is a number reading "same" across contracts that differ —
worse than no number. Decision 13's own history is the evidence: the endpoint
table described all three designed fields as shipped for months when none were.
`core_version` covers the case mechanically and **over**-warns rather than
under-warns, the safe direction under that decision's own warn-not-refuse
posture. Trigger to revisit is written into decision 13.

**Deferred with a trigger: the `{code, message, cause}` error body**, and the
reason is stronger than "it is large". Its value is *entirely* in consumers
branching on `code`, which makes the `code` enum a wire contract shared with
`embarch-api`, `embarch-ui` and `embarch-umbrella`'s `doctor` — so it is
**cross-repo sequenced work under `embarch-parallel-agents.md` §8, not a
worker's task at all.** Core-side alone it re-shapes ~40 error-construction
sites, each needing a stable `code` invented for it, while every consumer still
reads plain text: the whole cost, none of the benefit. Trigger: the first
consumer that must distinguish two error kinds sharing one HTTP status.

**A drift guard, in place of a note.** Two tests pin `StatusResponse`'s
serialized key set exactly, so **adding** a field without editing
`interfaces.md`'s `/status` row fails the suite just as loudly as removing one.
That is the mechanism for the shape decision 13 was itself an instance of.

## What the task got wrong about the consumer

The task says `embarch-umbrella`'s `doctor` check 11 "wants Core's served host
version, so there is a named consumer waiting." **That consumer is not waiting
on this change.** `embarch-umbrella/open.md`'s own text for check 11 names the
three numbers worth comparing as *"Core's served **host** version, the version
the located `embarch-api` was built against, and the wire version the bench
reports"* — and says in the same bullet that "Core has served the version on
`/status` since 2026-08-25". That is `study_designer_schema_version`, which
already existed. **Check 11 could have been built without this task**, and
nothing it needs changed here.

So `core_version` was built on its own merits, not on that consumer's. It is
newly *available* to check 11 as a fourth number — a `doctor` that reports
which Core binary answered alongside the schema numbers — but that is an
addition to an `embarch-umbrella` task, not a dependency of one. **Nothing
about what check 11 should read has changed.**

## Gate

Green, per step, run in the two worktrees:

- `cargo build`, `cargo test` (171 passed, 2 ignored, incl. the two new
  `/status` tests), `cargo clippy --all-targets -- -D warnings` — all clean.
- **Native Windows build: real, not a cross-check.** `cargo check --target
  x86_64-pc-windows-msvc` fails from WSL on `hidapi`'s C sources needing MSVC
  headers (`guiddef.h`), which is `embarch-dev-workflow.md` §4's documented
  cross-build failure class and unrelated to this change. So the three crates
  were rsynced to a **scratch** tree on the Windows side —
  `C:\Users\tmp12\embarch-agent-scratch\core-002`, deliberately **not** the
  `source/repos` deploy tree §4a syncs to — and built with the native
  `cargo.exe`: `build` and `test --no-run` both exit `0`. Tests were compiled
  natively but **not executed** there, since that is the machine with the
  hardware on it.
- All six `embarch-doc` checks, plus `check-ownership.py` on both branches.

`open.md` was **77 bytes** from its 5 KB cap before this edit, so the deferral
bullet points at decision 12 rather than restating it. Worth knowing before the
next edit to that file.

## Hardware-verification debt

**None.** `core_version` is a compile-time constant serialized into a JSON
response, and the test that asserts it goes through the real router. There is
nothing a board could tell you that the host-side test does not.

One thing a *deploy* would confirm and nothing here does: that the live Windows
service, once redeployed, actually answers with the version of the binary
installed — which is the footgun the field exists to catch, and cannot be
demonstrated without the deploy §7 forbids a worker. Not debt in this change;
it is the first useful thing to look at on the next real `deploy-core`.
