# 015 — Two fields of one action sharing a name cannot be chosen independently

**State:** claimed by agent/study-designer/015-duplicate-field-name, 2026-09-07 15:22
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

## Doc-size reserve for `study-designer` — supervisor, leg 036, 2026-09-07

**Nothing in this scope is in reserve, and `decisions/registry.md` — the file this task names as
the rule's likely home — has real room: 8,927 / 12,288 B, 3,361 B left.** Write the argument out
properly; you are not short of space and should not write as though you were.

Two files are close enough to name, both filed under `tasks/study-designer/006-compact-study-designer.md`,
which is **`blocked`**:

- `embarch-study-designer/spec.md` — 9,183 / 10,240 B, **1,057 B left**. Just outside the
  `max(1.2 KB, 10%)` reserve floor, so an edit of ~150 bytes or more puts it in.
- `embarch-study-designer/open.md` — 4,331 / 5,120 B, **789 B left**. Likewise close.

**So the realistic risk here is `spec.md`, and the cheap answer is not to write to it.** This unit
adds a validation rule to a function whose two neighbours are already recorded in
`decisions/registry.md`; if `spec.md` does not currently say something this makes false, leave it
alone and say so. If it does, and your edit crosses the floor, file
`tasks/study-designer/<next NNN>-compact-study-designer.md` in the same commit
(`tasks/README.md` has the shape) — or add the path to `006`'s `**Compacts:**` line and say why
that is the truer home. Do not resolve `006`'s `In flux: yes` to make the queue move.

**On the second half of the task's "worth deciding alongside it" question** — whether the three
field rules want one `RegistryError` variant family rather than three unrelated ones — that is
yours to decide inside this sub-project and it needs nobody's approval (`protocol.md` §5 rule 4).
Decide it either way, in writing, with the argument. "Left for later" is a worse answer than
either choice, because the next unit to open `validate` will face the same fork with one more rule
in it.
