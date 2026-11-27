# 126 — compact `embarch-ui/spec/tabs.md`

**State:** claimed by agent/ui/126-compact-ui, 2026-11-26 19:25
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/spec/tabs.md
**Size debt due:** 2026-12-09
**In flux:** no
**Must not delete:** each tab's row and the decision numbers it cites; the Confirm row's go card (111).

## What

`tabs.md` is 9,160 of 10,240 B after `ui/124` added the go card to the Confirm row. Compact it under `DOC-COMPACTION.md`, mostly the Desk row, which holds the longest prose. Answered by the unit that just worked in it: **the Confirm tab is not still moving**, though its prompt-modal half (EMB-575) will touch the Live Study row once.

## Done when

- [ ] `tabs.md` is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
