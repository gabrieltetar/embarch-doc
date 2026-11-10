# 027 — `embarch-desk/spec.md` is in reserve

**State:** done
**Source:** `desk/025` added decision 83 and left sessions.md at 12,177 of 12,288 B and spec.md at 9,197 of 10,240 B.
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/spec.md
**Size debt due:** 2026-11-17
**In flux:** no. All three halves of the close-out landed 2026-11-10; a live run is still owed, and a change it forces would amend decisions 83 and 84 in `decisions/closeout.md`, not `spec.md`'s paragraph wholesale.
**Must not delete:** decision 83's contract with the chat (the `end` and `unfinished` fields, no expiry on the launch clock, `/items/{id}/finish`), and decision 80's **Unverified** note.

## Update (desk/026, 2026-11-10)

`sessions.md` is out of reserve: decision 83 moved verbatim to `decisions/closeout.md` (8,930 of 12,288 B left behind), so it is off this task's `Compacts:` line. `spec.md` is at 9,440 of 10,240 B, still in reserve, so this task stays open for it. `closeout.md` is 6,783 B, clear. The `Must not delete:` list still holds: decision 83 is in `closeout.md` whole, decision 80's **Unverified** note is untouched in `sessions.md`.

## What

Compact or split `spec.md` once the close-out settles.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; `desk/025` spent the reserve.

## Done when

- [x] `spec.md` is clear of reserve, or a successor re-files with a concrete plan.
- [x] Every `Must not delete:` item is still readable.
- [x] Gate green (`../../embarch-fleet/gate.md`).

## Shipped

Verbatim split by mission: the suite-desk, west-module and login-flag paragraphs (decisions 70, 80, 82) moved to `embarch-desk/spec/suite-desk.md`; spec.md keeps a one-line pointer. spec.md 9,440 -> 8,882 B, out of reserve. Decision 83's contract stays in spec.md §2 and `decisions/closeout.md`; decision 80's Unverified note untouched.
