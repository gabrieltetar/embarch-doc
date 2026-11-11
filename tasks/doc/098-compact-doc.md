# 098 — Compact `DOC-CONVENTIONS.md` back out of its reserve

**State:** open
**Source:** `tasks/suite/023`'s closing commit, 2026-11-10: the owner landed its drafted "measured arm" paragraph in `DOC-CONVENTIONS.md` "Measured vs. assumed", which took the file to 11,590 of 12,288 B (94.3%), inside the reserve
**Scope:** doc
**Hardware:** none
**Owner:** required — `DOC-CONVENTIONS.md` is owner-reserved.
**Compacts:** DOC-CONVENTIONS.md
**Size debt due:** 2026-11-17
**In flux:** no
**Must not delete:** the "Measured vs. assumed" section's arm paragraph, landed the day this was filed; the 2026-09-05 collector story in "`open.md` needs no "Open questions" heading", which is why that rule is written down at all.

## What

`DOC-CONVENTIONS.md` is out of the reserve per `DOC-COMPACTION-PASS.md`: at most `max(1.2 KB, 10%)` short of its 12,288 B cap.

## Why now

`check-doc-size.py` fails a file in reserve that no open task names. This is that task, filed in the commit that spent the reserve.

## Done when

- [ ] `DOC-CONVENTIONS.md` is out of the reserve, and `check-doc-size.py` passes without this task.
- [ ] Nothing named under **Must not delete** is lost.
