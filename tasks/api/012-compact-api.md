# 012 — Compact `embarch-api`'s spec, two decision groups and the config interface

**State:** blocked — **re-blocked by the supervisor, 2026-09-05 13:10.** `agent/api/011`
moved this to `open` and was right on everything it could see: `tasks/api/010` had
landed, which is what it was parked behind. **It could not see that three `api` tasks
were filed from `inbox/` twenty minutes earlier in the same leg**, and two of them
rewrite files this task compacts. `In flux:` is **yes** again, and what unparks it is
named below.
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
second gate. That file specifically is settled — decision 27's both halves are built and
30/39/40/44 have no open task against them.

**In flux:** **yes**, for the other three files, and this is the supervisor's correction
to `agent/api/011`'s `no`. Three `api` tasks were drained from `inbox/` on 2026-09-05
and two of them rewrite exactly what this task would compact:

- **`tasks/api/013-target-json-not-written.md`** rewrites `interfaces/config.md`'s
  build-directory paragraph, which states decision 19's per-directory `target.json` as
  current truth while nothing in `embarch-api` writes it. Whichever way 013 answers —
  write the file, or strike the claim — that paragraph changes.
- **`tasks/api/014-extra-args-hash-not-stable.md`** rewrites the `-args<hash>` segment of
  `zephyr::Target::build_dir_name`, which is `decisions/zephyr.md`'s territory — the
  96-byte file this task calls "the tight one and the natural target".
- `tasks/api/015-retired-targets-error-misadvises-zephyr.md` is a message-only fix in
  `config.rs` and probably does not move a doc, so it is not what blocks this.

**Unparks when 013 and 014 have both closed**, or when whoever runs this narrows it to
`decisions/studies.md` alone — that one file could be compacted today. Compacting the
other three now writes a clean statement of something about to be wrong, which is the
exact reason this task was parked behind `api/010` in the first place.
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

**The `api/010` blocker is gone and a new one took its place, 2026-09-05.**
`tasks/api/010` closed, retiring `[[projects.targets]]` — decision 12's escape-hatch
sentence, decision 51's argument, `spec.md` §3's static bullet and
`interfaces/config.md`'s row have all been rewritten to match. That ground *is* stable
now. But `tasks/api/013` and `014`, filed the same day, put `interfaces/config.md` and
`decisions/zephyr.md` back in motion. See the `In flux:` note above for exactly which
paragraphs.

**It is still worth doing and it is getting more expensive to defer.** `decisions/zephyr.md`
has **96 bytes** left, and on 2026-09-05 that cap did something new: `api/010` had a
decision to write about static-project build orchestration, could not fit it in
`zephyr.md`, and filed **decision 53 in `decisions/shape.md` instead**. That is the
first time in this suite a byte cap has *moved* a decision rather than shortened one,
and a reader who opens `zephyr.md` for the static-project mission now reads decision 51
with no sign the menu is gone. **A pass here should add the pointer 51 is missing** —
the reviewer noted it would have fitted inside the 96 bytes.

## Done when

- [x] `tasks/api/010` is closed, and this task is moved to `open`.
- [ ] The four files are compacted per `DOC-COMPACTION-PASS.md`, one commit for
      the sub-project, with the `Must not delete:` list above honoured.
- [ ] The human question answered in the compactor's own words in the commit
      message: can `embarch-api/spec.md` alone answer what someone needs to work
      on this component today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
