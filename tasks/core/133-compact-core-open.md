# 133 — `embarch-core/open.md` is in reserve

**State:** blocked
**Source:** core 131 (run log, decision 111) rewrote the scope section of `open.md`, leaving it at 4,829 of 5,120 B (291 B left).
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/open.md
**Size debt due:** 2026-12-21
**In flux:** yes. M1.7 (`measurements.json`) and M1.8 (publish manifest) each close or reshape the scope, tail-anchor and ledger items just written; a rewrite now would be restated within a unit.
**Unparks when:** `tasks/core` M1.8 (the publish manifest signing) lands, or the next core unit that writes `open.md` runs out of its 291 B, whichever comes first; the compaction rides in that unit.
**Must not delete:** every open item's owner-run step (the `icacls` debts, the unexercised paths), and every decision citation; move reference detail to `open/` verbatim.

## What

Bring `open.md` out of reserve by moving settled detail into `open/` verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-core/open.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
