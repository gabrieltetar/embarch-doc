# 100 — `embarch-atlas/design.md` is in reserve

**State:** blocked
**Source:** atlas 097 (EMB-136) added the "Prior-art search" section to `embarch-atlas/design.md`, leaving it at 24,000 of 25,600 B (93.8%, 1,600 B left).
**Scope:** atlas
**Hardware:** none
**Owner:** no

**Compacts:** embarch-atlas/design.md
**Size debt due:** 2026-12-07
**In flux:** yes. `atlas/098` (claims text) and `atlas/099` (a second source) extend the prior-art section next, and the atlas translation procedure was edited as recently as `atlas/096`.
**Unparks when:** `atlas/098` and `atlas/099` have landed, or the next unit that writes `embarch-atlas/design.md` carries the compaction with it.
**Must not delete:** the prior-art section's open `robots.txt` flag and the note that `ab=`, `pa=` and `or` groups were not run live; both are evidence a later reader needs to re-establish.

## What

Bring `embarch-atlas/design.md` out of reserve: shorten the longest sections without dropping a fact or a decision pointer.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-atlas/design.md`.
- [ ] Nothing named under **Must not delete** is lost.
- [ ] The compactor's answer to "can `design.md` alone answer what someone needs to work on atlas today?" is in the commit message.
