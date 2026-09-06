# Refuse two registered actions sharing a name, as struct layouts already are

**State:** open
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

- [ ] `DuplicateRegisteredAction { name }` exists, with a message shaped like its sibling's.
- [ ] `ActionRegistry::validate` returns it, so both `load` and `save` refuse.
- [ ] Tests cover a duplicate-name registry rejected on load and a single-name registry still
      accepted.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features study-ui`.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
