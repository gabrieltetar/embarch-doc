# 038 — `embarch-core/decisions/surfaces.md` is inside its reserve floor

**State:** blocked — filed by `core/037`, parked on `In flux: yes` below.
**Source:** `core/037`'s decision 55 (`study_schema_mismatch` retired as a name) pushed
`decisions/surfaces.md` from 10,978 B to 11,937 B against a 12,288 B cap — 351 B left against a
1,229 B reserve floor (10%). `check-doc-size.py` names it in reserve with no debt filed; this task
is that debt.
**Scope:** core
**Hardware:** none
**Owner:** no

## Blocked

**Why:** decision 12 (the deferred `{code, message, cause}` error body) and decision 55 (this
file's newest entry, filed by `core/037`) are both still moving — decision 12 is an explicitly
open, unbuilt design and decision 55 amends it. Compacting either now risks cutting a claim before
it has finished changing.

**Compacts:** embarch-core/decisions/surfaces.md
**Size debt due:** 2026-09-24
**In flux:** yes — `core/037` just added decision 55 to this file, and decision 12 (the deferred
`{code, message, cause}` body) that 55 amends is itself an open, unbuilt design; either could
still move before this file is a safe compaction target. Unparks when whichever of these
stabilizes: decision 12 either gets built or is explicitly closed as "will not build", or a
compaction pass finds a genuine verbatim split/squeeze that does not touch either decision's
checkable claims.

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

- [ ] `embarch-core/decisions/surfaces.md` is clear of its reserve floor (≤ 11,059 B), **or** this
      task closes with a written argument that no safe cut or split remains, naming what was
      considered.
- [ ] Decision 12 and decision 55's checkable claims are still readable, in full, wherever they
      end up.
- [ ] The commit message quotes the first dozen words of every deleted hunk verbatim
      (`DOC-COMPACTION-PASS.md`).
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
