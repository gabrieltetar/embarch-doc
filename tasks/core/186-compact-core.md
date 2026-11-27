# 186 — compact `embarch-core/spec.md` and `decisions/platform.md`

**State:** open
**Scope:** core
**Hardware:** none
**Owner:** no
**Compacts:** embarch-core/spec.md, embarch-core/decisions/platform.md
**Size debt due:** 2026-12-10
**In flux:** no
**Must not delete:** spec §3's decision references (129, 156, 157); decision 106's measured `CreateService FAILED 1073` and `Environment` loss, and decision 157's rejected alternatives and the unverified-on-Windows note.

## What

`spec.md` is at 9,082 of 10,240 B (line 9,039 B) after its §3 named decision 157; `decisions/platform.md` is at 11,527 of 12,288 B after `core/183` added decision 157, which puts it in reserve. Decisions 1 to 17 are settled prose a verbatim split into a new topic file would not restate; 106 and 157 are the install pair and move together.

## Done when

- [ ] Both files are out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can `spec.md` alone answer what someone needs to work on this component today?
