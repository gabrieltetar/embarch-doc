# 130 — `embarch-core/spec.md` is in reserve

**State:** blocked
**Source:** core 129 (signing, decision 110) added the run-record paragraph and the challenge exception to `spec.md`, leaving it at 9,458 of 10,240 B (782 B left).
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/spec.md
**Size debt due:** 2026-12-15
**In flux:** yes. The HIL plan's remaining core units (M1.6 run log, M1.7 `measurements.json`, M1.8 publish manifest) each add to the signing and record sections of `spec.md`, and decision 109's scope enforcement is still to come; a rewrite now would be restated within a unit or two.
**Unparks when:** `tasks/core` M1.8 (the publish manifest signing) lands, or the next core unit that writes `spec.md` runs out of its 782 B, whichever comes first; the compaction rides in that unit.
**Must not delete:** the invariants (every route takes the token but `POST /auth/challenge`, the route sweep, the two scopes) and every decision citation; move reference detail to `spec/` verbatim.

## What

Bring `spec.md` out of reserve by moving reference text into `spec/` verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-core/spec.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
