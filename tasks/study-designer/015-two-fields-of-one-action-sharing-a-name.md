# 015 — Two fields of one action sharing a name cannot be chosen independently

**State:** done, agent/study-designer/015-duplicate-field-name, 2026-09-07
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

- [x] `ActionRegistry::validate` refuses two fields of one action sharing a
      `name`, with a named `RegistryError` naming the action and the name.
      `RegistryError::DuplicateActionField { action_name, field_name }`,
      checked per-field before the range/value checks, in
      `embarch-study-designer/src/registry.rs`.
- [x] A test over a hand-written registry that fails without the check.
      `registry.rs::tests::two_fields_of_one_action_sharing_a_name_are_refused_at_load`
      (validate-level, asserts both the variant and the exact message).
      Also added `study_builder.rs::tests::two_fields_sharing_a_name_the_builder_never_validated_write_one_pick_into_both`,
      which pins down **which** of the two bad outcomes the task named: with a
      shared `field_choices` map keyed by name, a label that also names a value
      on the *other* field writes both byte ranges from that one pick
      (`[0x01, 0x03]`, not the `0x02` the second field's own "Low" would have
      given), silently — the double-write, not the `UnknownFieldChoice` case —
      demonstrated on a registry `validate()` itself refuses, the same posture
      as the existing overlap-residual test.
- [x] The rule recorded in `embarch-study-designer/decisions/registry.md` —
      either as its own decision or as an amendment to 67. **Decided: its own
      decision, 69** — not an amendment, on the same precedent 66→67 already
      set inside this function: closely related, incrementally discovered
      rules get their own numbers so each stays independently citable
      (`check-decision-refs.py`), and folding a new failure mode into 67's
      prose would make that citation ambiguous about which rule a reader means.
      Argued in full in `registry.md`'s decision 69 entry.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). See report below.
- [x] `spec.md`/`decisions.md`/`open.md` updated where anything became false,
      `changelog.d/` fragment dropped. `spec.md` and `open.md` say nothing
      about the registry's `validate` rules, so neither became false — left
      alone rather than touched to touch them, per the supervisor's reserve
      note below. `decisions.md`'s index row for `registry.md` gained `69`.
      `changelog.d/study-designer-duplicate-field-name.fixed.md` dropped.

## Report

**No sibling-consumer break.** Grepped `embarch-{ui,api,core}` read-only for `RegistryError`,
`ActionRegistry`, `registry::` — the only real hit is `embarch-ui/src/study_designer.rs`, which
resolves the whole error via `.map_err(|e| e.to_string())`, never a match arm. No consumer
matches `RegistryError` exhaustively, so the new variant is not a breaking change and no
`status.d/` fragment or `inbox/` drop was needed for this half of the check.

**Second "worth deciding alongside it" question, decided: no shared `RegistryError` variant
family.** `DuplicateRegisteredAction`, `FieldRangesOverlap`, `FieldsOnNonWriteAction` and this
task's `DuplicateActionField` stay four separate flat variants. Argument (full version in
`registry.md`'s decision 69): the crate's own founding move in decision 35 is a *named, literal*
refusal in place of an inferred one, which a shared family would blur behind an inner match; no
consumer needs to match "any field-shape rule" as a group (the one real consumer only calls
`.to_string()`); and `RegistryError` already mixes `ActionRegistry` and `StructRegistry` failures
in one flat enum, so grouping three of twelve variants would be a partial regrouping around one
function, not a real simplification — bought at the price of every future field rule asking
which family member it is before it asks what it refuses.

**Doc-size reserve.** `decisions/registry.md`'s decision 69 entry pushed it from 8,927/12,288 B
to 11,827/12,288 B — 461 B left, inside the `max(1.2 KB, 10%)` reserve floor, which the
supervisor's note did not anticipate (it named `spec.md`/`open.md` as the close files, not this
one, and neither was touched here). Filed
`tasks/study-designer/019-compact-study-designer.md` in this commit, per `tasks/README.md`,
listing `registry.md` on its `Compacts:` line and answering `In flux:` **no** — nothing pending
names a fourth rule in this family, and `open.md` says nothing about the registry.

**Gate, both repos:**
- `embarch-study-designer`: `cargo build`, `cargo test` (both default and `--all-features`;
  `registry.rs` is gated behind the `study-ui` feature), `cargo clippy --all-targets -- -D
  warnings` (and `--all-features`) — all clean. 229 tests pass under `--all-features` including
  the two new ones.
- `embarch-doc`: `python3 scripts/check-docs.py` — all 10 checks green.
- `scripts/check-ownership.py --scope study-designer` (in the doc worktree) and
  `--code-repo --repo <code worktree>` — both OK.
- `scripts/check-client-names.py --repo <code worktree>` — clean against 7 denylist entries.

No hardware touched; nothing here needed it.

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
