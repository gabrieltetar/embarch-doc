# 033 — Decision 45's declared GATT table was designed, never built, and the deferral has no trigger

**State:** open
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

- [ ] Either the type and field exist with round-trip tests, or `decisions/declares.md` carries a
      named trigger — not both, and not neither.
- [ ] If built: nothing in the docs or the code implies the declared table is reconciled against
      live discovery, because it is not.
- [ ] `embarch-study-designer/open.md`'s bullet is struck or replaced by the trigger.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green; gate green;
      `changelog.d/` fragment.

**Reserve note:** `embarch-study-designer/open.md` is at **97.5%** (130 B left) and `spec.md` at
91.3%, both behind blocked compaction tasks. **Striking a bullet from `open.md` shortens it, which
is the good direction** — do not add prose there, and if this work spends a reserve elsewhere, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit.
