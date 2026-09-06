# Refuse two registered actions sharing a name, as struct layouts already are

**State:** done, agent/study-designer/009-duplicate-action-names, 2026-09-06
**Source:** owner's repo survey, 2026-09-06 — the sibling registry in the same file already implements this
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`src/registry.rs:211-227` (`ActionRegistry::validate`) checks only that each value's byte count
matches its field. `:316-321` (`StructRegistry::validate`) refuses a duplicate name outright with
`DuplicateStructLayout`. `src/study_builder.rs:450-451` resolves a row's action by
`.find(|a| &a.name == name)`, so the second of two same-named actions in a hand-edited
`study-actions.toml` is silently unreachable and a row builds the wrong payload.

Add `DuplicateRegisteredAction { name }` with a message in the same shape as
`DuplicateStructLayout`'s, and return it from `ActionRegistry::validate` so both `load` and `save`
refuse the file.

## Why now

`registry.rs:243-249` states the posture — a hand-edited file's mistakes become a named error rather
than something a bounded type swallows — and two registries in one module currently treat the
identical hand-edit mistake differently.

## Done when

- [x] `DuplicateRegisteredAction { name }` exists, with a message shaped like its sibling's.
- [x] `ActionRegistry::validate` returns it, so both `load` and `save` refuse.
- [x] Tests cover a duplicate-name registry rejected on load and a single-name registry still
      accepted.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features study-ui`.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false. Decision 35 and a `changelog.d/` fragment;
      `spec.md`, `open.md` and `status.d/` needed no change, and Done says why.

## Done

`RegistryError::DuplicateRegisteredAction { name }` sits beside `FieldLengthMismatch` in the enum
and prints "two actions are both named '<n>'; a row referencing it could resolve to either" —
`DuplicateStructLayout`'s sentence with *structs/tap* swapped for *actions/row*. A test asserts both
strings verbatim, so the two cannot drift apart silently. `ActionRegistry::validate` gained the
duplicate scan in `StructRegistry::validate`'s exact shape (`self.actions[..index].iter().any(...)`,
before the per-field work), and both `load` and `save` already call `validate`, so a duplicate file
can be neither read nor written — `save` refuses before it creates `embarch/`, which the test
asserts by checking the file was never made.

Decision recorded in `decisions/authoring.md` under 35, not in `decisions/crate.md`: this is the
registry's authoring surface, and it is where decision 52 already states the identical rule for the
struct registry. `crate.md` (in reserve, `tasks/study-designer/006` blocked) untouched.

`spec.md` deliberately not edited: nothing in it became false, and it has ~136 B before the reserve
line, which is not enough for an honest invariant sentence. No `status.d/` fragment (no suite-level
fact changed) and no `features.d/` row (no capability shipped, retired or changed maturity — this
hardens one already-shipped).

Gate green: `cargo build`, `cargo test`, `cargo test --no-default-features --features study-ui`
(175 pass), `cargo clippy --all-targets -- -D warnings` on both feature sets. No hardware debt —
the change is host-side file validation with no DUT involvement.
