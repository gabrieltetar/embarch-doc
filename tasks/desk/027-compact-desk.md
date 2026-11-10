# 027 — `embarch-desk/spec.md` is in reserve

**State:** blocked — `In flux: yes`.
**Unparks when:** `tasks/chat/023` lands, the close-out's last half (the folder removal landed 2026-11-10, desk `1997108`, decision 84 in the same spec paragraph).
**Source:** `desk/025` added decision 83 and left sessions.md at 12,177 of 12,288 B and spec.md at 9,197 of 10,240 B.
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/spec.md
**Size debt due:** 2026-11-17
**In flux:** yes. The close-out is two-thirds built (026 removes the folder, the chat's 023 acts on the entries); compacting decision 83 first would restate what 026 amends.
**Must not delete:** decision 83's contract with the chat (the `end` and `unfinished` fields, no expiry on the launch clock, `/items/{id}/finish`), and decision 80's **Unverified** note.

## Update (desk/026, 2026-11-10)

`sessions.md` is out of reserve: decision 83 moved verbatim to `decisions/closeout.md` (8,930 of 12,288 B left behind), so it is off this task's `Compacts:` line. `spec.md` is at 9,440 of 10,240 B, still in reserve, so this task stays open for it. `closeout.md` is 6,783 B, clear. The `Must not delete:` list still holds: decision 83 is in `closeout.md` whole, decision 80's **Unverified** note is untouched in `sessions.md`.

## What

Compact or split `spec.md` once the close-out settles.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; `desk/025` spent the reserve.

## Done when

- [ ] `spec.md` is clear of reserve, or a successor re-files with a concrete plan.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
