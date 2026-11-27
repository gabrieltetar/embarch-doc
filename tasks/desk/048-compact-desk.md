# 048 — compact `embarch-desk/decisions/built.md`

**State:** claimed by agent/desk/048-compact-desk, 2026-11-27 04:17 — decisions/built.md only; interfaces.md is desk/049, leave it
**Scope:** desk
**Hardware:** none
**Owner:** no
**Compacts:** embarch-desk/decisions/built.md
**Size debt due:** 2026-12-11
**In flux:** no
**Must not delete:** decision 27's rejected alternatives (Windows service, hosting inside the UI, spool file), decision 94's rejected alternatives and its quoting rule, decision 69's instance rules.

## What

`decisions/built.md` is at 11,873 of 12,288 B after `desk/047` added decision 94, which puts it in reserve. The service decisions (27, 69, 94) were settled and the unit writer was not moving when this was filed; a split by topic (the service and its instances in one file) would shorten the file without restating anything.

## Done when

- [ ] The file is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can `decisions.md` plus this file answer why the desk runs as a user service and how its unit is written?
