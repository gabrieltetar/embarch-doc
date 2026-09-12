# 033 — Decision 45's declared GATT table was designed, never built, and the deferral has no trigger

**State:** claimed by agent/study-designer/033-declared-gatt, 2026-09-12 01:20
**Source:** `embarch-study-designer/open.md` — "**Decision 45's declared GATT table was designed,
never built** — no `gatt` field on `Study`, no `DeclaredGatt` type, no reconciliation against live
discovery. Deferred with no trigger fired yet".
**Scope:** study-designer
**Hardware:** none for the half this task takes. Reconciliation against **live** discovery needs a
radio and is explicitly **out of scope** here.
**Owner:** no

## What

Pick one and do it, rather than leaving a third state:

- **Build the authorable half** — the `gatt` field on `Study` and the `DeclaredGatt` type, with
  parse, serialize and round-trip tests — and state plainly that reconciliation against live
  discovery is not built, so nobody reads the field as checked. **A declared table nothing
  reconciles must not read as a validated one**; that is `embarch-decision-reversals.md` shape 3,
  which this crate has already been bitten by.
- **Or rewrite the bullet as a named-trigger deferral** in the decision file, saying what has to be
  true before it is built.

**The second is a legitimate answer and may well be the right one.** Do not build machinery because
the docs mention it; this suite's stated posture is not to build first.

## Why now

**Adjacent and deliberately separate:** `tasks/study-designer/008` withdraws `Study.gatt` /
`DeclaredGatt` from the *docs* — the same "the reference teaches an unbuilt field" shape in
`interfaces/types.md`. **Read that task before starting this one**: if it has landed, the docs no
longer advertise the field and the honest answer here may simply be the trigger-deferral.

## Done when

- [x] Either the type and field exist with round-trip tests, or `decisions/declares.md` carries a
      named trigger — not both, and not neither. **Named-trigger deferral kept**: no code was
      built (correctly — decision 45 says building it before a real study needs it would be
      designing against imagined authoring), and `decisions/declares.md` 45 now states the trigger
      itself ("the first study that needs to say which GATT table it was authored against")
      instead of pointing at open.md for it.
- [x] If built: n/a — not built.
- [x] `embarch-study-designer/open.md`'s bullet is struck or replaced by the trigger. Struck: the
      trigger now lives at its source of truth, `decisions/declares.md`, so open.md no longer
      carries a second copy.
- [x] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green; gate green;
      `changelog.d/` fragment.

## Notes

`tasks/study-designer/008` had already landed before this task started (see
`decisions/declares.md` 45 and `interfaces/types.md`'s existing "designed, never built" framing) —
docs no longer advertise the field as real, confirming the task's own hint that the honest answer
here is the trigger-deferral rewrite, not a build.

**Reserve note:** `embarch-study-designer/open.md` is at **97.5%** (130 B left) and `spec.md` at
91.3%, both behind blocked compaction tasks. **Striking a bullet from `open.md` shortens it, which
is the good direction** — do not add prose there, and if this work spends a reserve elsewhere, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit.
