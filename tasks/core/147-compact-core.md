# 147 — `embarch-core/spec.md` is in reserve

**State:** blocked
**Source:** core 145 (EMB-250) added a call-log-range line to `spec.md`, leaving it at 9,160 of 10,240 B (1,080 B left).
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/spec.md
**Size debt due:** 2026-12-07
**In flux:** yes. The signing, publish and call-log surface is still moving: `verify`'s call-log half (EMB-254) and a published report's call-log line (EMB-265) wait on core 145, and the HIL plan (`notes/hil/14`) has more units after them.
**Unparks when:** EMB-254 and EMB-265 have landed, or the next core unit that writes `spec.md` runs out of its 1,080 B; the compaction rides in that unit.
**Must not delete:** the invariants bullets (lease gate, call log, challenge route) and the decision citations; move reference detail into `spec/` verbatim.

## What

Bring `spec.md` out of reserve by moving reference text into `spec/` verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-core/spec.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
