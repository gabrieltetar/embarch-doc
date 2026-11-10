# 024 — `embarch-desk/decisions/desks.md` is in reserve

**State:** claimed by agent/desk/024-compact-desk, 2026-11-10 03:42
**Source:** `desk/022` added decision 82 and left the file at 11,066 B of 12,288 B (90.1%); `DOC-COMPACTION.md` §2
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/decisions/desks.md
**Size debt due:** 2026-11-26
**In flux:** no — the desk decisions (33–42, 74, 77, 82) are settled; 82's "not done" list (no parent-folder search, every desk told) is the one edge a user complaint would reopen.
**Must not delete:** 82's read-only rule and why the desk never writes `.claude.json`; its "not done" list and the rejected list; 77's rejected list and the owner's-call attribution; 74's rejected list.

## What

`desks.md` has 1,222 B of headroom. Compact it: the older decisions (33–42) restate mechanism that `interfaces.md` and `spec.md` also hold.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; `desk/022` is the unit that spent it.

## Done when

- [ ] `desks.md` is clear of reserve.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
