# 008 — `embarch-promptu/decisions/patterns.md` is in reserve

**State:** blocked
**Source:** promptu 007 (EMB-196) added the footer and log pointers to decisions 13 and 14, leaving `decisions/patterns.md` at 11,138 of 12,288 B (reserve from 11,059 B; it stood at 11,058 B on `main`, at the edge).
**Scope:** promptu
**Hardware:** none
**Owner:** no

**Compacts:** embarch-promptu/decisions/patterns.md
**Size debt due:** 2026-11-24
**In flux:** yes. The rewrite (decision 42) was just built, the chat's card (EMB-197) is the next unit and the owner has not settled the rewrite's model or wait; decisions 9, 13, 14 and 24 are each amended by 42 and will be restated once he settles it.
**Unparks when:** the owner records the rewrite's model and wait after the ten-prompt measurement (owed, `embarch-promptu/open.md`), or EMB-197 lands, whichever is first; the compaction rides in the unit that next writes `decisions/patterns.md`.
**Must not delete:** decision 42 whole, the "Amended by 42" pointers on 9, 13, 14 and 24, and the rejected-alternative lists of 9, 13 and 24.

## What

Bring `decisions/patterns.md` out of reserve: move whole decisions whose subject is settled (the pass's and patterns' questions, 22 to 28) into a new topic file verbatim, leaving the index row in `decisions.md` updated. Never shorten a decision-bearing sentence.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-promptu/decisions/patterns.md`.
- [ ] Moved decisions are byte-identical in their new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
