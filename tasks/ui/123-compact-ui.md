# 123 — compact `embarch-ui/decisions/live-study.md`

**State:** claimed by agent/ui/123-compact-ui, 2026-11-26 18:14
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/decisions/live-study.md
**Size debt due:** 2026-12-09
**In flux:** no
**Must not delete:** decision 60's `Not fixed` paragraph and its measurement receipts (`tests/browser/drive_race.py`, `drive_switch.py`); decision 32's measured 0 vs 7,440 bytes; decision 109's statement that the page never paints `cancelled` itself.

## What

`live-study.md` is 11,539 of 12,288 B after `ui/122` added decision 109. Compact it under `DOC-COMPACTION.md`. Answered by the unit that just worked in it: **the live study view is not still moving** — the Cancel button was the last open item on it.

## Done when

- [ ] `live-study.md` is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
