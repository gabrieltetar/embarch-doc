# 201 — compact `embarch-api/spec.md`

**State:** blocked
**Scope:** api
**Hardware:** none
**Owner:** no
**Compacts:** embarch-api/spec.md
**Size debt due:** 2026-12-09
**In flux:** yes
**Unparks when:** the HIL Test tools settle in embarch-api: the ledger tools renamed to `test_show`, `test_pending` and `test_add`, and the results mirror written.
**Must not delete:** the `embarch_api::person_writer` and `embarch/tests/` bullets, the lease and `EMBARCH_REQUIRE_LEASE` bullets, and the no-inference-as-fact invariant.

## What

`spec.md` is at 9,130 of 10,240 B after `api/200` added one bullet for `run_test` and `test_status` (decision 135), which puts it in reserve. Answered by the unit that just worked in it: **the HIL Test surface is still moving** (three more renames and the results mirror are ahead), so compacting the bullets about it now would state something about to be wrong. The next unit to write `spec.md` carries this compaction in the same commit.

## Done when

- [ ] `spec.md` is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can `spec.md` alone answer what someone needs to work on this component today?
