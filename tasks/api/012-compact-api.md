# 012 — Compact `embarch-api`'s spec and its studies decisions

**State:** claimed by agent/api/012-compact-api, 2026-09-05 21:26 — **unparked by the owner, 2026-09-05, by narrowing it rather than by
overriding `In flux:`.** Two of the four files left this task: `decisions/zephyr.md` was
**split by mission** and is out of reserve, and `interfaces/config.md`'s compaction now
rides in `tasks/api/013`, which is the unit that rewrites it (`DOC-COMPACTION.md` §2).
What is left — `spec.md` and `decisions/studies.md` — is settled, so `In flux:` is **no**
and this is dispatchable.
**Source:** `scripts/check-doc-size.py` — `embarch-api` files entering reserve, on tasks 009 and 011
**Scope:** api
**Hardware:** none
**Owner:** no

This path is now the rule, not a deviation. `agent/api/009` filed here rather
than at `tasks/doc/<NNN>-compact-api.md` because `check-ownership.py --scope api`
refuses `tasks/doc/**`, reported it, and `tasks/doc/004` settled it on 2026-09-05
in this file's favour: a compaction debt goes in the scope directory of the doc
being compacted. `tasks/README.md` and `check-doc-size.py`'s message say so.

**Compacts:** embarch-api/spec.md, embarch-api/decisions/studies.md

**Reserve, measured by leg 012 at dispatch (2026-09-05 21:26):** `embarch-api/spec.md`
**10,104 / 10,240 B — 136 B left, 98.7%**, the tightest file in the suite;
`embarch-api/decisions/studies.md` **11,249 / 12,288 B — 1,039 B left, 91.5%**. Those two
are the whole reserve list for `api`, and `check-doc-size.py --pressure` names no other
file in the suite. Nothing else in `api` is in reserve, so you have room to *move* text
into `decisions/build.md` (7.2K/12K), `interfaces/*.md` or `open.md` (4.5K/5K — near its
own line, do not use it as a sink). **A split is preferred over shortening wherever a file
holds more than one mission** (`DOC-COMPACTION.md` §2–3) — but `spec.md`'s 10 KB is a role
cap on a single file and cannot be split, so shortening or moving is the only move there.

**`open.md`'s item is closed, 2026-09-05** — `api/011` answered and removed decision
27's capacity bullet and the file fell to 89.2%, out of reserve. The two loose ends
leg 009 recorded there (the `none`-collision error's unfollowable advice, and the
asymmetric load-time refusal) are **still in the file and still live inconsistencies
in shipped behaviour**; a later pass may shorten them freely but must not drop either.

**`decisions/zephyr.md` is paid, and not by compacting it.** The owner split it by
mission on 2026-09-05: decisions 5, 18, 19 and 42 moved verbatim to
**`decisions/build.md`** ("Running a build"), leaving 12, 13, 20, 21, 22 and 51 in
`zephyr.md` ("Target discovery and selection"). 12,192 B became 5,234 + 7,499. A split
moves entries without restating them, so `In flux: yes` never applied to it — which is
why this was the move rather than an override. `decisions.md`'s index carries both rows,
and its two stale `Size` cells were corrected in the same pass.

**`decisions/studies.md` added by `agent/api/011`**, which spent 609 B of its reserve
(10,640 → 11,249 B, 91.5%) recording that decision 27 shipped: the message's shape,
the `serde` string it replaces, and why the check is diagnostic-only rather than a
second gate. That file specifically is settled — decision 27's both halves are built and
30/39/40/44 have no open task against them.

**In flux:** **no**, for the two files this task still names. It was `yes` for the other
two and that is what the narrowing answered rather than overrode. Three `api` tasks were
drained from `inbox/` on 2026-09-05; here is where each of them landed:

- **`tasks/api/013-target-json-not-written.md`** rewrites `interfaces/config.md`'s
  build-directory paragraph, which states decision 19's per-directory `target.json` as
  current truth while nothing in `embarch-api` writes it. Whichever way 013 answers —
  write the file, or strike the claim — that paragraph changes. **So 013 now carries that
  file's compaction itself**, with the `Must not delete:` clause it needs, and this task
  no longer names it.
- **`tasks/api/014-extra-args-hash-not-stable.md`** rewrites the `-args<hash>` segment of
  `zephyr::Target::build_dir_name` — decision 19, which used to sit in the 96-byte
  `decisions/zephyr.md` and now sits in **`decisions/build.md` with ~7 KB free.**
- `tasks/api/015-retired-targets-error-misadvises-zephyr.md` is a message-only fix in
  `config.rs` and probably does not move a doc. It cites decision 12, which stayed in
  `decisions/zephyr.md`.
**Must not delete:** decision 21's *first* paragraph as written, which asserts the
`"none"` literal "cannot collide with a real snippet name" — it is wrong, the
amendment below it says so and says how it is now checked, and a compaction that
keeps only the corrected statement destroys the record that the reasoning was
once accepted. Same for decision 18's `[assumed]` 1:3 split and decision 22's
cost bound: both are provenance that reads as measurement once shortened.
Decision 51's "verified before widening the fix" — that all six selection fields
were the same defect — is evidence, not a restatement of the rule.

## What

Two files are still in reserve here: `spec.md` 10,105/10,240 B (135 B left) and
`decisions/studies.md` 11,249/12,288 B (1,039 B left). `spec.md` is the tight one and is
the natural target.

The shape that worked on `zephyr.md` and is worth trying first: several decisions restate
parts of `interfaces/config.md`'s own prose, which is where the *surface* belongs. Move
surface description out of the decisions and leave the reasoning; do not shorten the
reasoning itself. Where a file holds more than one mission, **split it instead** — that
costs nothing and restates nothing (`DOC-COMPACTION.md` §2–3).

## Why now

**The `api/010` blocker is gone, a new one took its place, and the narrowing answered it, 2026-09-05.**
`tasks/api/010` closed, retiring `[[projects.targets]]` — decision 12's escape-hatch
sentence, decision 51's argument, `spec.md` §3's static bullet and
`interfaces/config.md`'s row have all been rewritten to match. That ground *is* stable
now. But `tasks/api/013` and `014`, filed the same day, put `interfaces/config.md` and
`decisions/zephyr.md` back in motion. See the `In flux:` note above for exactly which
paragraphs.

**What made this urgent, and is now the standing rule.** `decisions/zephyr.md` had **96
bytes** left, and on 2026-09-05 that cap did something new: `api/010` had a decision to
write about static-project build orchestration, could not fit it in `zephyr.md`, and
filed **decision 53 in `decisions/shape.md` instead**. That is the first time in this
suite a byte cap has *moved* a decision rather than shortened one — a cap that misfiles
is worse than a cap that refuses, because nothing fails and the reader never learns. It
is why `DOC-COMPACTION.md` §2 now says a parked task parks the pass and not the reserve.
**Decision 51 still lacks the pointer saying the menu is gone**, and `zephyr.md` now has
4.8 KB of room for it — carry that into whichever pass touches 51.

## Done when

- [x] `tasks/api/010` is closed, and this task is moved to `open`.
- [x] `decisions/zephyr.md` and `interfaces/config.md` are off this task — split, and
      handed to `api/013`.
- [ ] `spec.md` and `decisions/studies.md` are compacted per `DOC-COMPACTION-PASS.md`,
      one commit for the sub-project, with the `Must not delete:` list above honoured.
- [ ] The human question answered in the compactor's own words in the commit
      message: can `embarch-api/spec.md` alone answer what someone needs to work
      on this component today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
