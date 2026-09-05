# 012 — Compact `embarch-api`'s spec, two decision groups and the config interface

**State:** open
**Source:** `scripts/check-doc-size.py` — `embarch-api` files entering reserve, on tasks 009 and 011
**Scope:** api
**Hardware:** none
**Owner:** no

This path is now the rule, not a deviation. `agent/api/009` filed here rather
than at `tasks/doc/<NNN>-compact-api.md` because `check-ownership.py --scope api`
refuses `tasks/doc/**`, reported it, and `tasks/doc/004` settled it on 2026-09-05
in this file's favour: a compaction debt goes in the scope directory of the doc
being compacted. `tasks/README.md` and `check-doc-size.py`'s message say so.

**Compacts:** embarch-api/decisions/zephyr.md, embarch-api/spec.md, embarch-api/interfaces/config.md, embarch-api/decisions/studies.md

**`open.md`'s item is closed, 2026-09-05** — `api/011` answered and removed decision
27's capacity bullet and the file fell to 89.2%, out of reserve. The two loose ends
leg 009 recorded there (the `none`-collision error's unfollowable advice, and the
asymmetric load-time refusal) are **still in the file and still live inconsistencies
in shipped behaviour**; a later pass may shorten them freely but must not drop either.

**`decisions/studies.md` added by `agent/api/011`**, which spent 609 B of its reserve
(10,640 → 11,249 B, 91.5%) recording that decision 27 shipped: the message's shape,
the `serde` string it replaces, and why the check is diagnostic-only rather than a
second gate. **In flux:** no. Decision 27's subsystem is settled — both halves are now
built, and 30/39/40/44 in that file are closed decisions with no open task against
them. A pass may compact it whenever it is convenient.
**Must not delete:** decision 21's *first* paragraph as written, which asserts the
`"none"` literal "cannot collide with a real snippet name" — it is wrong, the
amendment below it says so and says how it is now checked, and a compaction that
keeps only the corrected statement destroys the record that the reasoning was
once accepted. Same for decision 18's `[assumed]` 1:3 split and decision 22's
cost bound: both are provenance that reads as measurement once shortened.
Decision 51's "verified before widening the fix" — that all six selection fields
were the same defect — is evidence, not a restatement of the rule.

## What

Four files are in reserve: `decisions/zephyr.md` 12,192/12,288 B (96 B left),
`spec.md` 10,105/10,240 B (135 B left), `interfaces/config.md` 11,415/12,288 B,
and `decisions/studies.md` 11,249/12,288 B. Nothing is blocked and nothing is being
asked for yet — this records that the runway is nearly spent.

`decisions/zephyr.md` is the tight one and is the natural target: it carries ten
entries, several of which (12, 18, 20, 21, 51) now restate parts of
`interfaces/config.md`'s own prose, which is where the *surface* belongs. The
likely pass is moving surface description out of the decisions and leaving the
reasoning, not shortening the reasoning itself.

## Why now

**Unblocked 2026-09-05**: `tasks/api/010` closed, retiring `[[projects.targets]]`,
which is what this was parked behind — compacting before it landed would have
written a clean statement of something about to be wrong. Decision 12's
escape-hatch sentence, decision 51's argument, `spec.md` §3's static bullet and
`interfaces/config.md`'s row have all now been rewritten to match, so the ground
under a pass is stable.

## Done when

- [x] `tasks/api/010` is closed, and this task is moved to `open`.
- [ ] The four files are compacted per `DOC-COMPACTION-PASS.md`, one commit for
      the sub-project, with the `Must not delete:` list above honoured.
- [ ] The human question answered in the compactor's own words in the commit
      message: can `embarch-api/spec.md` alone answer what someone needs to work
      on this component today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
