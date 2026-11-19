# 056 — Compact `embarch.md` back out of its reserve

**State:** open
**Source:** EMB-213's proposal commit, 2026-11-18: `embarch-analog-capture-proposal.md`'s row in `embarch.md` §6 took the file from 23,026 to 23,314 of 25,600 B (91.1%), inside the reserve, which began 14 B above where it stood
**Scope:** suite
**Hardware:** none
**Compacts:** embarch.md
**Size debt due:** 2026-11-25
**In flux:** no
**Must not delete:** a row of §6 for any top-level file: the index is useful only while exhaustive ([DOC-PROTOCOL.md](../../DOC-PROTOCOL.md) §5), and the next top-level file needs room for its own row.

## What

`embarch.md` is out of the reserve per `DOC-COMPACTION-PASS.md`: at most `max(1.2 KB, 10%)` short of its 25,600 B cap.

## Why now

`check-doc-size.py` fails a file in reserve that no open task names. This is that task, filed in the commit that spent the reserve.

## Done when

- [ ] `embarch.md` is out of the reserve, and `check-doc-size.py --pressure` shows it `PAID`.
- [ ] Nothing named under **Must not delete** is lost.
- [ ] The commit message answers `DOC-COMPACTION-PASS.md`'s human question for `embarch.md`: can it alone tell a new reader what the suite is and where each doc lives?
