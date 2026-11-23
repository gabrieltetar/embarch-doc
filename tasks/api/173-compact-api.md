# 173 — `embarch-api/interfaces/publish.md` is in reserve

**State:** blocked
**Source:** api 171 (EMB-226) filled `verify`'s table rows for checks 4, 6 and 9, leaving `interfaces/publish.md` at 11,437 of 12,288 B (reserve from 11,059 B).
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/interfaces/publish.md
**Size debt due:** 2026-12-06
**In flux:** yes. `verify` is still moving: check 2's step outcomes and markers, a first real Core zip, the call log's segment and `verify --core` each change its table, and the publish half gains a revision-aware path with them.
**Unparks when:** `verify` reads a real Core's zip, or the next unit that edits the `verify` section lands, whichever is first; the compaction rides in that unit.
**Must not delete:** the `verify` table's per-check statements of what is and is not recomputed, the decision pointers (118 to 125), and the "not checkable offline" line of check 8.

## What

Bring `interfaces/publish.md` out of reserve: split the `verify` section into `interfaces/verify.md` verbatim (the page is two surfaces under one name), update the links, and leave `publish.md` with the publish half. Never shorten a sentence that states what a check does not do.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-api/interfaces/publish.md`.
- [ ] The moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
