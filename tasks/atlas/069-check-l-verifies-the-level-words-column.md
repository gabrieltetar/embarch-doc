# 069 — Check L verifies the level word's column, like check K

**State:** done — 2026-11-17
**Source:** EMB-160, filed from the protocol-records work (atlas task 011), which added check L
**Issue:** EMB-160
**Scope:** atlas
**Hardware:** none
**Owner:** no

## Resume, read before anything else

The worker dispatched at 14:51 died on a usage-limit 429 with its tree
uncommitted. Recovery committed that tree as it stood, ungated, as `6301f43` on
`agent/atlas/069-check-l-verifies-the-level-words-column` in `embarch-atlas`
(on `90f70f2`): edits to `src/embarch_atlas/check.py`, `tests/test_protocol.py`,
`DESIGN.md` and the translate procedure, about 135 lines. Review it as someone
else's draft, finish it, and run the whole gate; do not trust that it passes.
The doc branch has no commits yet.

## What

Check L (`applicability_check` in `src/embarch_atlas/check.py`) confirms that an
applicability record's level word (Required, Recommended and the like) occurs
somewhere in the quoted source row. A row usually holds one column per role, so a
record that took its level from the neighbouring role's column still passes, and
a Required/Recommended swap between roles is exactly the mistake these records
exist to prevent.

Check K already verifies a value's column position for another record kind
(`compare_columns`, and the `out["K"]` branch beside `out["L"]`). Give check L
the same test: the record names its column (role), and the check confirms the
level word sits in that column of the quoted row. Reuse check K's column
machinery rather than writing a second one. Where the record or the row gives no
column to test, report check L as not checkable with the reason, the way check K
does, rather than passing it.

If the record shape has no field naming the role's column today, add the
smallest one that does, update the procedure under
`skills/atlas-translate-docs/reference/` that tells a session how to write the
record, and say in `DESIGN.md` what check L now proves.

**Public repo.** Tests use synthetic records and rows only.

**Burndown leg: no new numbered decision** (`embarch-atlas` keeps none anyway).
A real design fork goes to `scripts/fleet-linear.py file --from decision`.

**What you may change.** Only `embarch-atlas` and `embarch-doc/embarch-atlas/`.

**Doc reserve.** Nothing of `embarch-atlas`'s is in reserve.

## Why now

The owner moved EMB-160 to Fleet Ready. Check L reads as a column check and is
not one.

## Done when

- [x] Check L fails a record whose level word is in the quoted row but in another role's column.
- [x] A test covers both the right-column pass and the wrong-column failure, and a record with no column to test reports not checkable.
- [x] `DESIGN.md` (and the translate procedure, if the record shape changed) says what check L proves.
- [x] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.

## Outcome

Resumed worker reviewed the recovered draft (6301f43) and kept it: check L reuses K's word-position approach (`_level_column`), no new record field (`role`/`as` already name the column), not-checkable reasons: no-words, no-role, row-not-found, no-header, level-not-in-words, level-from-note. Cells whose level comes from a footnote are not checkable, so the procedure-example and the fixture count moved to 14/16. Gate: pytest 858 passed, 3 skips (west workspace, built atlas, SVD; test_public_guard ran).
