# 052 — compact `embarch-dev-bench/spec.md`

**State:** blocked
**Scope:** dev-bench
**Hardware:** none
**Owner:** no
**Compacts:** embarch-dev-bench/spec.md
**Size debt due:** 2026-12-10
**In flux:** yes
**Unparks when:** the PD bench's HIL characterisation session has run `pd idle` and `pd hello` on both shields and settled what the bench's shell holds (decision 68).
**Must not delete:** the `pd-bench/` paragraph's decision references (48, 49, 58, 68), the `patch-sums.py` and `bench-firmware-list.py` descriptions, and the workspace layout tree.

## What

`spec.md` is at 9,138 of 10,240 B after `dev-bench/051` added the `pd idle` and `pd hello` sentence, which puts it in reserve. Answered by the unit that just worked in it: **the PD bench is still moving** (its shell commands are ahead of the HIL characterisation session), so compacting its paragraph now would state something about to change.

## Done when

- [ ] `spec.md` is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can `spec.md` alone answer what someone needs to work on this component today?
