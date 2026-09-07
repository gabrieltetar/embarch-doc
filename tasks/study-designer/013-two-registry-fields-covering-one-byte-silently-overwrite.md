# 013 — Two registry fields covering the same payload byte silently overwrite each other

**State:** done by agent/study-designer/013-disjoint-field-ranges, 2026-09-06
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

- [x] `ActionRegistry::validate` refuses two fields of one action whose byte ranges
      overlap, with a named `RegistryError` naming both fields and the overlap.
- [x] A decision, either way, on whether fields on a non-`Write` action are refused
      or documented as ignored — recorded alongside 66. **They are refused.**
- [x] Tests over a hand-written registry for whichever rules land.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## What shipped

**`RegistryError::FieldRangesOverlap`** — two fields of one action covering a
common byte, refused at `validate` (so on load and on save), naming both fields
in declaration order and the shared half-open range. **`FieldsOnNonWriteAction`**
— a `read`/`subscribe`/`notify`/`indicate` action carrying any field, refused the
same way, naming the operation with the word the TOML spells.

Both corrections carried. The message does not say "the later declaration wins":
it says the earlier field's chosen value is not in the payload, and that where
the ranges overlap only partly what is there instead is **a splice of both that
nobody registered**. `study_builder`'s
`an_overlapping_registry_the_builder_never_validated_splices_two_values`
demonstrates it — picks `[0xA1, 0xA2]` and `[0xB1, 0xB2]` produce
`[0x00, 0xA1, 0xB1, 0xB2]`, so `header`'s own bytes hold neither value, asserted
against both `values` lists. The wrong test comment on the overflow case is
fixed: the wrap yields length 0, the allocation succeeds, and the **slice index
panics** — no out-of-bounds write is available, and the un-overflowing 4 GB
offset is the larger hazard.

**Deliberate break, run before claiming anything.** With the two checks reverted
and the tests kept, `cargo test --all-features` gave **223 passed, 4 failed**:
`two_fields_covering_one_byte_are_refused_at_load` ("expected a
FieldRangesOverlap, loaded ActionRegistry {…}"), `a_read_action_carrying_fields_
is_refused_at_load`, `every_non_write_operation_refuses_a_field_and_write_keeps_
them` ("expected a FieldsOnNonWriteAction for Read, got Ok(())"), and the builder
splice test's closing `matches!` on `validate()`. Restored, 227 pass. The two
false-positive guards — `fields_that_only_meet_at_a_boundary_are_accepted` and
`a_zero_length_field_covers_no_byte_and_so_overlaps_nothing` — pass either way by
construction, and are guards rather than proofs.

**Both checks are `validate`-only**, unlike decision 66's bound, which the
builder repeats because that number sizes an allocation. Stated in 67 with its
residual: a registry assembled in memory and never validated can still build a
wrong payload, exactly as a duplicate action name is still whatever `.find()`
reaches first.

**Doc: `decisions/authoring.md` was split rather than squeezed.** It was 10,377
of 12,288 bytes, so decision 67 at full length would have put it **over cap**
(12,611), and cutting it to fit is the 96-byte remainder `tasks/README.md` names
as a real failure. `decisions/registry.md` is new and holds 35, 66 and 67 — the
registry file and what `validate` refuses it for; `authoring.md` keeps 6, 34, 37,
38, the surfaces that *use* it. 4.7K and 8.4K, neither in reserve, **so no
compaction task is owed.** `decisions.md`'s two rows and its "sixteen files"
count updated.

**One link fix is owed and a worker may not make it.** Hunting the moved-decision
links by hand (`tasks/doc/022` — no gate sees this class) turned up two in
`history/study-designer.md`, both pointing at `authoring.md` for decisions 35 and
66, which now live in `registry.md`. They still *resolve*, so `check-links.py`
stays green; they just name the wrong file. Fixing them is a two-token edit —
`decisions/authoring.md 66` → `decisions/registry.md 66` on the `012` line, and
the `decision 35` link target on the `009` line, which likewise ends in
`authoring.md` — but `check-ownership.py` refuses `history/**` to every worker
scope, so the edit was made, caught by that check, and reverted. **It is the
supervisor's to land**, in the fold that already writes that file.

`spec.md` and `open.md` are unchanged: nothing in either became false. `spec.md`
does not describe registry validation at all, and at 9,177/10,240 an added line
would have put it in reserve for a rule decision 67 already states. No
`features.d/` row: no capability shipped, retired or changed maturity — the same
call `study-designer/009` and `012` made for the identical shape of change.

**Dropped in `inbox/`:** `study-designer-two-fields-of-one-action-sharing-a-
name.md` — `validate` still accepts two fields of one action sharing a `name`,
which the UI and `resolve_write_payload` both key choices by, so the engineer
gets one pick for two ranges. Out of this task's scope, filed rather than folded
in.
