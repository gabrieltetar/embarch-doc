# 022 — `embarch-promptu/spec.md` is in reserve

**State:** blocked
**Source:** promptu 019 (EMB-279) added `week mark` and `week apply` to the status paragraph, leaving `spec.md` at 9,074 of 10,240 B (1,166 B left).
**Scope:** promptu
**Hardware:** none
**Owner:** no

**Compacts:** embarch-promptu/spec.md
**Size debt due:** 2026-12-07
**In flux:** yes. Step 4 is mid-build: the replay check (promptu 020), the sheet's numbers (promptu 021) and the terminal review skill (promptu 023) are still to land, and each rewrites the status paragraph.
**Unparks when:** `promptu/020`, `promptu/021` and `promptu/023` land (step 4's remaining units; `week timer` is built), or the next promptu unit that writes `spec.md` runs out of its reserve (1,150 B left at 9,090 B).
**Must not delete:** the step-by-step build status and its EMB references; move the long status paragraph to `spec/` verbatim, leaving a link.

## What

Bring `spec.md` out of reserve by moving the longest status text into `spec/` verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-promptu/spec.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
