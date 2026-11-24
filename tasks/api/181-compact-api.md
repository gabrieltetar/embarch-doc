# 181 — `embarch-api/open.md` is in reserve

**State:** blocked
**Source:** api 180 (EMB-255) added the live log's unverified-on-a-bench item to `open.md`, leaving it at 4,204 of 5,120 B (916 B left).
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/open.md
**Size debt due:** 2026-12-07
**In flux:** yes. The live log's first writer landed in api 180 and `embarch-atlas` (EMB-266, EMB-267) is about to write to the same file; what is unverified about it will change within a unit or two.
**Unparks when:** the next api unit that writes `open.md` runs out of its 916 B, or the atlas's live-log writers land and the live-log item can be rewritten once.
**Must not delete:** the dated verification debts and their decision citations; move reference detail to `open/` verbatim, as `open/bench-verification.md` was.

## What

Bring `open.md` out of reserve by moving the longest items into `open/` verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-api/open.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
