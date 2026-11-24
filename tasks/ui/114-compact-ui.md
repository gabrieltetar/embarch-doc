# 114 — `embarch-ui/decisions/shell.md` and `spec/tabs.md` are in reserve

**State:** open
**Source:** ui/113 (EMB-283) added the Promptu section to decision 56 and the Desk row of `spec/tabs.md`: `shell.md` is at 11,553 of 12,288 B (735 B left) and `tabs.md` at 9,079 of 10,240 B (1,161 B left).
**Scope:** ui
**Hardware:** none
**Owner:** no

**Compacts:** embarch-ui/decisions/shell.md, embarch-ui/spec/tabs.md
**Size debt due:** 2026-12-08
**In flux:** per file. embarch-ui/decisions/shell.md: no, the shell decisions are settled and 56's Promptu part is complete. embarch-ui/spec/tabs.md: yes in its Desk row, which grows with each `embarch-desk` feature the tab draws (the feel route, desk/043, is the next); compact the other rows and leave the Desk row's wording to its next unit.
**Must not delete:** decision 56's Promptu paragraph (the hidden-at-zero rule and "the UI holds no Promptu logic"), and decision 63's retirement note; in `tabs.md` the Esc order on Topology and the `#topology?board=` marking rule.

## What

Move reference text out of both files into `spec/` or `decisions/` siblings verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` lists neither file.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Can `spec.md` alone answer what someone needs to work on the Desk tab today? Answered in the commit message.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
