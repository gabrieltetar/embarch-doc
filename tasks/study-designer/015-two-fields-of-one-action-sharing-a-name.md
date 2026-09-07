# 015 — Two fields of one action sharing a name cannot be chosen independently

**State:** open
**Source:** noticed while doing `study-designer/013` — `src/registry.rs`'s `ActionRegistry::validate`, `src/study_builder.rs`'s `resolve_write_payload`
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`ActionRegistry::validate` now refuses two actions sharing a name (decision 35),
two fields covering the same byte and fields on a non-`Write` action (decision
67). It still accepts **two fields of one action sharing a `name`**.

`resolve_write_payload` resolves a field's choice with
`field_choices.get(&field.name)`, and the UI keys its dropdowns the same way, so
two fields called `mode` get **one** label between them: the engineer cannot pick
different values for the two byte ranges, and whether the study builds at all
depends on whether the second field happens to have a value carrying the first
one's label — if it does, both ranges are written from that one pick; if it does
not, the row fails with `UnknownFieldChoice` naming a label the engineer did
choose. Either way the registry advertises two choices and offers one.

That is decision 35's duplicate-name failure one level down, in the same
hand-edited file, and it is the third rule this family has grown. It is
deliberately **not** in `013`, which was scoped to disjoint ranges and to the
non-`Write` question; filing it rather than folding it in.

## Why now

Not urgent — no known registry does it, and the failure is a wrong or refused
payload on a hand edit, not a crash. Filed because `013` closed the two
neighbouring holes in the same function and this is the one it left, so whoever
next opens `validate` should find it named rather than rediscover it.

Worth deciding alongside it: whether `decisions/registry.md` (new in `013`) is
where the rule lands, and whether the three field rules want one error variant
family rather than three unrelated ones.

## Done when

- [ ] `ActionRegistry::validate` refuses two fields of one action sharing a
      `name`, with a named `RegistryError` naming the action and the name.
- [ ] A test over a hand-written registry that fails without the check.
- [ ] The rule recorded in `embarch-study-designer/decisions/registry.md` —
      either as its own decision or as an amendment to 67.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated where anything became false,
      `changelog.d/` fragment dropped.
