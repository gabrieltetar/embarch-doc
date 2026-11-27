# 209 — compact `embarch-api/decisions/client-crate.md`

**State:** blocked
**Scope:** api
**Hardware:** none
**Owner:** no
**Compacts:** embarch-api/decisions/client-crate.md
**Size debt due:** 2026-12-26
**In flux:** yes
**Unparks when:** the client's Core-reported types stop growing: the HIL Test prompt types (decision 137) have settled and `StatusResponse` carries what the UI's Core identity line reads.
**Must not delete:** the two token scopes (decision 109 and its person-token order) and the struct-literal break warnings of 137 and 139.

## What

`client-crate.md` is at 11,808 of 12,288 B after decision 139 (`StatusResponse` gains `mode` and `keyid`), which puts it in reserve. Answered by the unit that just worked in it: **still moving**, since the client keeps gaining fields as Core's bodies grow (137, 139), so compacting now would state something about to be wrong.

## Done when

- [ ] `client-crate.md` is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can the decisions alone answer why the shared client is shaped as it is?
