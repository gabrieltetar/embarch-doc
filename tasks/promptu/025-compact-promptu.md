# 025 — `embarch-promptu/open.md` is in reserve

**State:** blocked
**Source:** promptu 024 (EMB-403) added the step 5 bullet to `open.md`, leaving it at 4,060 of 5,120 B (1,060 B left).
**Scope:** promptu
**Hardware:** none
**Owner:** no

**Compacts:** embarch-promptu/open.md
**Size debt due:** 2026-12-09
**In flux:** yes. Steps 4 and 5 are both under way: the step 4 bullets (half-built, unmeasured drafter) and the four unrecorded step 5 choices change with each unit, so a rewrite now states something about to be wrong.
**Unparks when:** step 4's build units land (EMB-273 to EMB-279 on real data) or the owner states choices 1, 18, 19 and 21, so the bullets can be rewritten once.
**Must not delete:** every open question with its fork or EMB reference; the unmeasured-claims list; move resolved detail to a topic file under `open/` verbatim and leave a link.

## What

Bring `open.md` out of reserve by moving settled step 1 to 3 bullets into `open/` verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-promptu/open.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
