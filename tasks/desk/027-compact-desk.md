# 027 — `embarch-desk/decisions/sessions.md` and `spec.md` are in reserve

**State:** blocked — `In flux: yes`.
**Unparks when:** `tasks/desk/026` (the folder's removal) has landed and its decision is written, since it extends decision 83 and the same spec paragraph.
**Source:** `desk/025` added decision 83 and left sessions.md at 12,177 of 12,288 B and spec.md at 9,197 of 10,240 B.
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/decisions/sessions.md, embarch-desk/spec.md
**Size debt due:** 2026-11-17
**In flux:** yes. The close-out is two-thirds built (026 removes the folder, the chat's 023 acts on the entries); compacting decision 83 first would restate what 026 amends.
**Must not delete:** decision 83's contract with the chat (the `end` and `unfinished` fields, no expiry on the launch clock, `/items/{id}/finish`), and decision 80's **Unverified** note.

## What

Compact or split the two files once the close-out settles; sessions.md is a candidate for a split by decision group.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; `desk/025` spent the reserve.

## Done when

- [ ] Both files are clear of reserve, or a successor re-files with a concrete plan.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
