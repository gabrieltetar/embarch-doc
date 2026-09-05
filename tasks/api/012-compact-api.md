# 012 — Compact `embarch-api`'s spec, zephyr decisions and config interface

**State:** blocked
**Source:** `scripts/check-doc-size.py` — three `embarch-api` files entered reserve on task 009's commit
**Scope:** api
**Hardware:** none
**Owner:** no

This path is now the rule, not a deviation. `agent/api/009` filed here rather
than at `tasks/doc/<NNN>-compact-api.md` because `check-ownership.py --scope api`
refuses `tasks/doc/**`, reported it, and `tasks/doc/004` settled it on 2026-09-05
in this file's favour: a compaction debt goes in the scope directory of the doc
being compacted. `tasks/README.md` and `check-doc-size.py`'s message say so.

**Compacts:** embarch-api/decisions/zephyr.md, embarch-api/spec.md, embarch-api/interfaces/config.md, embarch-api/open.md

**`open.md` added by the supervisor, leg 009**, in the commit that spent its reserve
(4371 → 4981 B, 97.3%). What spent it: a bullet recording the two loose ends the
`api/009` reviewer found — the `none`-collision error's unfollowable advice, and the
asymmetric load-time refusal. I wrote it long and it cost more than I estimated;
**a compaction pass may shorten it freely, but must not drop either fact**, because
each is a live inconsistency in shipped behaviour with nothing else recording it.
**In flux:** yes — unparked when `tasks/api/010-static-project-target-menu.md` closes
**Must not delete:** decision 21's *first* paragraph as written, which asserts the
`"none"` literal "cannot collide with a real snippet name" — it is wrong, the
amendment below it says so and says how it is now checked, and a compaction that
keeps only the corrected statement destroys the record that the reasoning was
once accepted. Same for decision 18's `[assumed]` 1:3 split and decision 22's
cost bound: both are provenance that reads as measurement once shortened.
Decision 51's "verified before widening the fix" — that all six selection fields
were the same defect — is evidence, not a restatement of the rule.

## What

All three files are in reserve after task 009 built decisions 20 and 21:
`decisions/zephyr.md` 12,192/12,288 B (96 B left), `spec.md` ~9.9K/10K,
`interfaces/config.md` ~11.4K/12.3K. Nothing is blocked and nothing is being
asked for yet — this records that the runway is nearly spent.

`decisions/zephyr.md` is the tight one and is the natural target: it carries ten
entries, several of which (12, 18, 20, 21, 51) now restate parts of
`interfaces/config.md`'s own prose, which is where the *surface* belongs. The
likely pass is moving surface description out of the decisions and leaving the
reasoning, not shortening the reasoning itself.

## Why now

**Blocked, deliberately.** `tasks/api/010` reopens exactly this subsystem: it
either adds a `target` param for a `static` project's `[[projects.targets]]`
menu or drops the rows, and either answer rewrites decision 12's escape-hatch
sentence, decision 51's reject-not-splice argument, `spec.md` §3's static bullet
and `interfaces/config.md`'s `[[projects.targets]]` row. Compacting before that
lands writes a clean statement of something about to be wrong.

## Done when

- [ ] `tasks/api/010` is closed, and this task is moved to `open`.
- [ ] The three files are compacted per `DOC-COMPACTION-PASS.md`, one commit for
      the sub-project, with the `Must not delete:` list above honoured.
- [ ] The human question answered in the compactor's own words in the commit
      message: can `embarch-api/spec.md` alone answer what someone needs to work
      on this component today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
