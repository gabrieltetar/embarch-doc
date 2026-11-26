# 171 — compact `embarch-core/open.md`

**State:** blocked
**Scope:** core
**Hardware:** none
**Owner:** no
**Compacts:** embarch-core/open.md
**Size debt due:** 2026-12-10
**In flux:** yes
**Unparks when:** the Test run's publish route and its interruption and resume land in embarch-core, so the open item on a Test run's held captures and the unchecked interrupted record are settled.
**Must not delete:** the Test run captures-held item, the Espressif dev-bench port item, and the macOS reasoned-only item.

## What

`open.md` is at 4,227 of 5,120 B after `core/169` added the item on a Test run's captures being held until a publish route exists (decision 144), which puts it in reserve. Answered by the unit that just worked in it: **the Test run subsystem is still moving** (its publish route, the interruption and resume, and the manual verdict are ahead), so compacting the items about it now would state something about to be wrong. The next unit to write `open.md` carries this compaction in the same commit.

## Done when

- [ ] `open.md` is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can `open.md` alone answer what someone needs to work on this component today?
