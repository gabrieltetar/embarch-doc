# 002 — `core_version`/`contract_version` on `/status`, and the `{code, message, cause}` error body

**State:** open
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

- [ ] `/status` serves whatever versions were decided worth serving, with the
      shape recorded in `interfaces.md`.
- [ ] Anything deliberately not built is moved out of "Designed, not built" into
      an explicit deferral with a trigger, in `decisions.md` and `open.md`.
- [ ] `interfaces.md`'s `/status` row matches what the code emits, field for field.
- [ ] Gate green (`embarch-parallel-agents.md` §10) — including the native
      Windows build, since `embarch-core` is involved.
- [ ] `changelog.d/` fragment dropped; `status.d/` fragment for any suite-level
      fact this makes false.
