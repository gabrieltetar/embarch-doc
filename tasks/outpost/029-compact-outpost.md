# 029 — `embarch-outpost/decisions/transport.md` and `decisions/manifest.md` are in reserve

**State:** blocked — `In flux: yes`.
**Unparks when:** the layout-4 change in `open.md` has closed, since it moves both decision groups.
**Source:** `outpost/027` added decisions 28 and 29 and left transport.md at 7,908 of 8,192 B and manifest.md at 7,350 of 8,192 B.
**Scope:** outpost
**Hardware:** none
**Owner:** no

**Compacts:** embarch-outpost/decisions/transport.md, embarch-outpost/decisions/manifest.md
**Size debt due:** 2026-11-26
**In flux:** yes. Layout 4 will amend decisions 5, 9 and 20, and compacting them first would restate what is about to change.
**Must not delete:** decision 9's selection/verification split and decision 28's measured-on-native_sim-only note.

## What

Compact or split the two decision files once the subsystem settles.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; `outpost/027` spent the reserve.

## Done when

- [ ] Both files are clear of reserve, or a successor re-files with a concrete plan.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
