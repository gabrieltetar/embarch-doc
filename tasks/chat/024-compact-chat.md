# 024 — `embarch-chat/spec.md` is in reserve

**State:** blocked — `In flux: yes`.
**Unparks when:** `tasks/desk/025` and `tasks/desk/026` have landed and the chat's side of an ended issue has run once against a real desk.
**Source:** `chat/023` added a spec line for an ended issue's chat and left spec.md at 9,373 of 10,240 B.
**Scope:** chat
**Hardware:** none
**Owner:** no

**Compacts:** embarch-chat/spec.md
**Size debt due:** 2026-11-24
**In flux:** yes. The end-of-issue behaviour (decision 104) is new and its desk half is still landing; the chat's spec has taken a line a week since 2026-10-25, so compacting it now would restate what the next unit changes.
**Must not delete:** the `§2` bullet on an ended issue (decision 104) and the one on what a reload restores (63), which state behaviour no decision file's summary repeats.

## What

Compact `spec.md` once the subsystem settles: current truth only, history to `decisions/`.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; `chat/023` spent the reserve.

## Done when

- [ ] `spec.md` is clear of reserve (`scripts/check-doc-size.py --pressure` shows it not at all), or a successor re-files with a concrete plan.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
