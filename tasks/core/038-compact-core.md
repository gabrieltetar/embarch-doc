# 038 — `embarch-core/decisions/surfaces.md` is inside its reserve floor

**State:** done — leg 085, `core/041`, 2026-09-11. Unparked without touching decision 12 or
55's claims: `core/041` needed to add a new decision to this file (decision 59, `POST /validate`'s
`not_attached`-versus-`mismatch` split) and found the genuine verbatim split this task's own
unpark condition names — `## The human enrollment surface` (decisions 25, 27, 28, 50, 54, 57) was
never about errors or version handshakes, and split out to `decisions/enrollment.md` untouched,
word for word, along that pre-existing section boundary. `surfaces.md` went from 12,019 B to
7,025 B before decision 59 was even added, clearing the floor with room to spare. Decisions 12 and
55 are unmoved, still readable in full, still where they were.
**Source:** `core/037`'s decision 55 (`study_schema_mismatch` retired as a name) pushed
`decisions/surfaces.md` from 10,978 B to 11,937 B against a 12,288 B cap — 351 B left against a
1,229 B reserve floor (10%). `check-doc-size.py` names it in reserve with no debt filed; this task
is that debt.
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/decisions/surfaces.md
**Size debt due:** 2026-09-24 (cleared 2026-09-11)
**In flux:** no — resolved by a split, not by decision 12 or 55 settling; see `**State:**` above.

## What

`embarch-core/decisions/surfaces.md` is 11,937 B against a 12,288 B cap, 351 B left against a
1,229 B floor. It needs roughly 878 B recovered to clear reserve, or a written finding that no
safe cut exists, per `DOC-COMPACTION.md` §2.

## Why now

`check-doc-size.py` fails the gate while a file it names sits in reserve with no debt on file.
`core/037` is the unit that spent the reserve — decision 55 is 9 sentences settling a doc-sourced
claim that turned out false (no `code` enum exists in `embarch-core` at all) and retiring a name
that never had a real member to lose. Once decision 12's fate is settled, whichever of the two
entries survives can likely be tightened or the pair merged, but doing that while decision 12 is
still an open, undecided design would risk cutting a claim that has not finished changing.

## Done when

- [x] `embarch-core/decisions/surfaces.md` is clear of its reserve floor (≤ 11,059 B), **or** this
      task closes with a written argument that no safe cut or split remains, naming what was
      considered. — 7,025 B, split not squeeze; nothing deleted.
- [x] Decision 12 and decision 55's checkable claims are still readable, in full, wherever they
      end up. — unmoved, in `surfaces.md`, byte-for-byte.
- [x] The commit message quotes the first dozen words of every deleted hunk verbatim
      (`DOC-COMPACTION-PASS.md`). — N/A: nothing was deleted, only moved to `enrollment.md`.
- [x] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
