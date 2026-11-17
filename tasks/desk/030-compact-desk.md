# 030 — `embarch-desk/spec.md` is in reserve

**State:** done
**Source:** desk 029 (EMB-110) added the sentence that the desk checks an issue key against Linear before making its card, and left `spec.md` at 9,168 of 10,240 B (reserve from 9,012 B).
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/spec.md
**Size debt due:** 2026-11-24
**In flux:** no. The session-start and key-check behaviour was just written and is settled; the rest of the spec has not moved this month.
**Must not delete:** any status claim in `spec.md`'s status line, or the bullet on how a session takes its work item (it states the key check, the 404 and the 502).

## What

Bring `spec.md` out of reserve: move one whole section with a natural home into a `spec/` topic file verbatim, leaving a one-line pointer. Never shorten a decision-bearing sentence.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [x] `scripts/check-doc-size.py --pressure` does not list `embarch-desk/spec.md`.
- [x] A moved section is byte-identical in its new file; `check-links.py` green.
- [x] Gate green (`../../embarch-fleet/gate.md`).

## Result

Moved §5 (what it deliberately does not do) verbatim to `embarch-desk/spec/non-goals.md`; `spec.md` keeps a one-line pointer naming each non-goal. The status line and the session work-item bullet (key check, 404, 502) are untouched.

**Human question (DOC-COMPACTION-PASS):** can `spec.md` alone still answer what someone needs to work on this component today? Yes: what it is, every invariant, the interface summary and constants stay in it, and the non-goals are named in the pointer, with the detail one click away.
