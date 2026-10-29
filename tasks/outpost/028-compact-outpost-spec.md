# 028 — `embarch-outpost/spec.md` is in reserve

**State:** blocked — `In flux: yes`.
**Unparks when:** `tasks/outpost/027` and the layout-4 change in `open.md` have closed.
**Source:** `outpost/026` added a sentence to spec.md and left it at 9,126 B of 10,240 B (89.1%); `DOC-COMPACTION.md` §2
**Scope:** outpost
**Hardware:** none
**Owner:** no

**Compacts:** embarch-outpost/spec.md
**Size debt due:** 2026-11-26
**In flux:** yes — the wire section moves with the layout-4 change `open.md` defers, and `outpost/027` (Kconfig promises) is still open. Compacting now would restate behaviour about to change.
**Must not delete:** the manifest-refusal and unverified-join bullets in §3 with their decision pointers (9, 18, 24, 27), and the measured 1.6% vs 78.1% overhead figures in §4.

## What

`spec.md` has 1,114 B of headroom. Compact it, or split it, once the subsystem settles.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; `outpost/026` is the unit that spent it.

## Done when

- [ ] `spec.md` is clear of reserve, or a successor re-files with a concrete plan.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
