# 006 — `embarch-desk/decisions/cockpit.md` is in reserve after decision 76

**State:** open
**Source:** decision 76 (the hand shows this week's tiles) crossed the reserve line on `cockpit.md`; `DOC-COMPACTION.md` §2
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/decisions/cockpit.md
**Size debt due:** 2026-11-23
**In flux:** no — 1–13, 57, 58, 60, 61 and 65 have held since October; 76 is new and stays whole.
**Must not delete:** decision 76 in full, its rejected alternatives included; 57's owner quote and its rejected fanned hand and drag piles; 61's three writers of `hours_override` and the stuck-tile failure it fixed.

## What

`cockpit.md` 12,061/12,288 B (98.2%). `spec.md` took 76 and stayed out of reserve.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it; this is that filing.

## Done when

- [ ] `cockpit.md` is clear of its reserve line.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
