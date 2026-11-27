# 049 — compact `embarch-desk/interfaces.md`

**State:** open
**Scope:** desk
**Hardware:** none
**Owner:** no
**Compacts:** embarch-desk/interfaces.md
**Size debt due:** 2026-12-11
**In flux:** no
**Must not delete:** the route table, the bearer and port contract, and the sentence naming the two client copies of the path rule (`desk_discovery.rs`, `rule.ts`).

## What

`interfaces.md` is at 13,938 of 15,360 B after `desk/046` added the client-copies sentence, which puts it in reserve. The HTTP surface was not moving when this was filed; routes already split into `interfaces/` sub-files can absorb more of the table.

## Done when

- [ ] The file is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can `interfaces.md` plus its sub-files still answer what each route takes and how a caller authenticates?
