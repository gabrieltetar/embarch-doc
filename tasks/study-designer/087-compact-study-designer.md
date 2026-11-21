# 087 — `embarch-study-designer/interfaces/hil-shapes.md` is in reserve

**State:** blocked
**Source:** study-designer 085 (EMB-217) edited `interfaces/hil-shapes.md`, leaving it at 11,205 of 12,288 B (1,083 B left).
**Scope:** study-designer
**Hardware:** none
**Owner:** no

**Compacts:** embarch-study-designer/interfaces/hil-shapes.md
**Size debt due:** 2026-12-21
**In flux:** yes. M1.3 (verdict rules, `study-designer/086`), M1.5, M1.7, M1.9 and M1.10 each write against this file and will amend its verdict table, `measurements.json` keys or conventions; a rewrite now would be restated within a unit or two.
**Unparks when:** `study-designer/086` lands, or the next unit that writes this file runs short of its 1,083 B; the compaction rides in that unit.
**Must not delete:** the *(shape)* markers and the pointers to decisions 90 and 91, the six verdicts and their `reason` lists, and the `measurements.json` key table; move reference detail to `interfaces/` verbatim.

## What

Bring `interfaces/hil-shapes.md` out of reserve by moving reference text (the characterisation file, the key table) into a sibling file verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-study-designer/interfaces/hil-shapes.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
