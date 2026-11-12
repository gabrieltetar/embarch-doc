# 126 — `embarch-core/open.md` is in reserve

**State:** open
**Source:** `tasks/suite/037` added the bullet saying decision 108's rename has not reached the installed service, and left `open.md` at 4,314 of 5,120 B. It sat at 3,918 B before, one byte under the reserve line, so any new bullet would have spent it. `DOC-COMPACTION.md` §2.
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/open.md
**Size debt due:** 2026-11-25
**In flux:** no. The bullets are owner-run debts and unverified diagnoses that stand still until someone runs them, and none of the code they describe is being rewritten. The one bullet that will move soon is decision 108's deploy, which closes at the next deploy of Core; leave it for that rather than shortening it.
**Must not delete:** each "Owner-run:" or "To verify:" step, because it is the only written receipt of how that debt closes; the decision 108 deploy bullet, whole, until a deploy closes it; the decision numbers each bullet cites.

## What

Bring `embarch-core/open.md` out of reserve (`scripts/check-doc-size.py --pressure` shows `out of reserve at <= 3919 B`). A split by mission is the default remedy (`DOC-BUDGET.md`): `## Never exercised` is most of the file and could move to `open/never-exercised.md` verbatim, leaving a pointer. Squeeze only what is settled, and reword nothing that moves.

## Why now

`check-doc-size.py` fails a file in reserve with no debt filed, and `suite/037` spent the reserve.

## Done when

- [ ] `embarch-core/open.md` is clear of reserve: `scripts/check-doc-size.py --pressure` shows it `PAID` or not at all.
- [ ] Moved text matches the original apart from headers and pointer lines.
- [ ] Every `Must not delete:` item is still readable.
