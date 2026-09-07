# 013 — Two registry fields covering the same payload byte silently overwrite each other

**State:** open
**Source:** noticed while doing `study-designer/012` — `src/registry.rs`'s `ActionRegistry::validate`, `src/study_builder.rs`'s `resolve_write_payload`
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`ActionRegistry::validate` now checks that each field's `byte_offset + byte_len`
lands inside `MAX_PAYLOAD_LEN` (decision 66), but it still does not check that two
fields of one action cover *disjoint* byte ranges. `resolve_write_payload` walks
the fields in declaration order and `copy_from_slice`s each chosen value into the
buffer, so where two fields overlap the later declaration silently wins and the
step carries a payload nobody chose — with the UI still showing both choices as
honoured.

That is the same failure decision 35's duplicate-name rule exists to prevent
("the row silently carries a payload nobody chose"), applied to offsets instead of
names, and the same hand-edited file reaches it.

The neighbouring case, worth deciding in the same sitting: `RegisteredAction.fields`
is documented as meaningful only for `operation: Write` and empty otherwise, and
nothing enforces that either — a Read action carrying fields has them silently
ignored rather than refused.

## Why now

Not urgent — it is a wrong payload on a hand-edit, not a crash, and no known
registry does it. Filed because it was found while bounding the adjacent number
and it belongs to whoever next opens `validate`, not to a task that was scoped to
one bound and one error variant.

## Two corrections to carry, both from `012`'s reviewer

**The overlap is worse than "the later declaration wins".** `resolve_write_payload`
writes each value into `buffer[byte_offset..byte_offset + byte_len]` in declaration
order, so on a **partial** overlap the payload carries *neither* pick intact — the
earlier value's head survives and its tail is overwritten. Say that, not the
understated version, in whatever error you land.

**`src/registry.rs`'s test comment near the overflow case is wrong and you will be
in that file.** It says a wrapped range "passes every check and then indexes
wherever it likes". It does not: the wrap yields length `0`, the allocation
succeeds, and the following slice index **panics** — slice bounds checks are never
elided, in either profile. There is no out-of-bounds write available. Fix the
comment to say what actually happens; a security-flavoured claim that overstates
its own defect is worse than no comment.

## Done when

- [ ] `ActionRegistry::validate` refuses two fields of one action whose byte ranges
      overlap, with a named `RegistryError` naming both fields and the overlap.
- [ ] A decision, either way, on whether fields on a non-`Write` action are refused
      or documented as ignored — recorded in `decisions/authoring.md` alongside 66.
- [ ] Tests over a hand-written registry for whichever rules land.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
