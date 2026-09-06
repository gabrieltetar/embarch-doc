# 017 — `soc_chip_overrides` is decided and never built: build it or retire decision 13

**State:** done, 2026-09-05 — **decision 13 retired**, not built.
**Source:** `embarch-api/open.md` — "`soc_chip_overrides` is decided and unbuilt", and
`embarch-api/decisions/zephyr.md` 13's own amendment. Found 2026-09-05 by `api/016` while
closing decisions 20/21's loose ends: `open.md` listed the field among those "equally
unhonourable on a `static` project", and it turned out to be unhonourable on **both** kinds.
**Scope:** api
**Hardware:** none to decide; **verify-only** if built (see below)
**Owner:** no

## What

`embarch-api` decision 13 and `embarch-api/interfaces/config.md` describe a per-project
`soc_chip_overrides` table: an `{ soc, chip }` list consulted **before** Core's
`POST /resolve-chip`, so an operator who resolved an unmapped SoC by hand with
`probe-rs chip list` has somewhere to write the answer and a hit skips the HTTP call.

**None of it exists.** `ProjectConfig` has no such field, `resolve.rs` calls
`core.resolve_chip(&target.soc)` unconditionally, and the crate sets no
`deny_unknown_fields`, so a config declaring the key is parsed and dropped in silence on a
`zephyr-west` project as much as on a `static` one. This is
`embarch-decision-reversals.md` shape 1 — config the interface doc states as truth and
nothing implements — the same shape decision 20 was built to close for `default_target`.

**Resolve it one way or the other.** Both are legitimate:

- **Build it.** Small: one `Vec<SocChipOverride>` on `ProjectConfig`, consulted in
  `resolve.rs` before `resolve_chip`, plus the load-time refusal on a `static` project that
  decision 20 now applies to the whole zephyr-west-only class (so it joins the five, and
  `interfaces/config.md`'s "five fields" sentence becomes six). The reason to: the dead end
  decision 13 names is real — Core's resolver 404s and the operator has nowhere to put the
  answer they already have.
- **Retire decision 13** per `DOC-CONVENTIONS.md`'s tombstone shape, and say plainly that a
  404 naming the unmapped SoC is where an unmapped SoC stops — the fix belongs in Core's
  chip table, not in a per-project override that makes one machine's config disagree with
  every other machine's. Then delete the `soc_chip_overrides` row from
  `interfaces/config.md` and the `open.md` bullet with it.

**Do not close this by quietly deleting the doc text**, and do not close it by building the
field without saying why the "fix it in Core" alternative was rejected. The entry has to
carry the argument against whichever half is not taken.

## Why now

`embarch-api/open.md` states it, and it is the one remaining half of the loose-ends bullet
`api/016` closed. It is cheap either way and it removes a doc that lies.

**What would sharpen the choice, and is not required to make it:** a real SoC Core has no
mapping for. Nobody has hit one recently, which is itself evidence for the retire half —
an escape hatch nothing has needed in three months is a hatch, not a door.

## Reserve, and the compaction you are carrying (added by the supervisor, leg 014)

**Both files this task rewrites are already in reserve, and `tasks/api/018-compact-api.md`
— the pass that would fix them — is `blocked` with `In flux: yes` **on this very task**.**
So the pass cannot run before you and the reserve will not survive you: you are the actor
making the flux, which under [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 makes the
compaction yours to carry inside this unit.

`api`'s reserve right now:

- `embarch-api/interfaces/config.md` — **11,844 / 12,288 B, 444 B left (96.4%)**. Roughly
  one table row. You are editing the `soc_chip_overrides` row in it either way.
- `embarch-api/open.md` — **4,608 / 5,120 B, 512 B left (90.0%)**. You delete its
  `soc_chip_overrides` bullet either way.
- `embarch-api/decisions/zephyr.md` — 10,966 / 12,288 B (89.2%), just under the line and
  one edit from it. Decision 13 lives there and you are rewriting it. Treat it as a third
  file if you are compacting anyway.

**What you owe:** bring `interfaces/config.md` and `open.md` **out of reserve** (below 90%)
in this unit's own commit, and tick those two items on `tasks/api/018-compact-api.md`. If
your outcome is *retire decision 13*, the deletions may do most of it on their own —
measure with `python3 scripts/check-doc-size.py --pressure` rather than assuming. If both
come out and nothing else in `api` is left in reserve, close `018` and `git rm` it; if one
file is still in, leave `018` open, flip its `In flux:` to `no` (this task will be closed),
and update its numbers.

**Carry `018`'s `Must not delete:` list** — read it, it is the whole reason the pass is not
free. Two clauses of it are about text you are about to rewrite:

- The `soc_chip_overrides` row's statement that it is **stated and never built on both
  discovery kinds** is on that list *because it existed nowhere else and was the whole
  content of this task*. Once you resolve it, that clause is discharged rather than
  protected — say so when you tick the item, so the next reader does not preserve a fact
  that stopped being true.
- The list also asserts that decision 20's second remedy "stops a reader landing in the
  next branch of the same check". **That overclaims and it is written down wrong.** A
  `static` project that follows the remedy literally — drop `build_command`/`chip`/
  `artifact_path`, set `discovery = "zephyr-west"` — next meets `has no west_binary`, then
  `has no build_dir_root`, in the following arm of the same `validate()`. `api/016`'s
  reviewer found this and correctly declined to file it (the advice is *incomplete*, not
  contradictory). **Correct that clause on `018` while you are in the file.** Fixing the
  remedy string itself is optional and in scope if it is one clause; do not grow it into a
  second task.

Run `scripts/check-duplication.py embarch-api` before shortening anything, and do not
collapse the deliberate three-depth statement of the five-field refusal (`spec.md` pointer,
`interfaces/config.md` paragraph, decision 20) — that is the reference/reasoning split.

## Outcome — retired, 2026-09-05

**Decision 13 is a tombstone**, and the argument against building sits in it. Two reasons,
one of which was not in the task's framing and is the stronger:

- **The short-circuit was the whole design and the short-circuit is the defect.** Core
  validates every SoC→chip mapping against probe-rs's own registry — at load *and* per
  call, so even a stale entry in Core's own table fails like an unmapped SoC
  (`embarch-core` decision 8). A per-project override consulted *before* the call skips
  that check, so one typo reaches `/flash` as a plausible chip name and attaches the wrong
  physical target — the exact failure decision 8 refused fuzzy matching to avoid. The
  saving it bought was one local HTTP call this crate makes `/flash` right after anyway.
- **It is per-project for a per-silicon fact**, and consulted first: restated per project
  and per repo, and still winning after Core's table is corrected.

***Rejected: build it.*** The dead end is real — a 404 naming the SoC and nowhere to put
the answer — but bounded: one row in the repo that owns the table plus a redeploy this
suite already runs, and nothing has hit an unmapped SoC in three months. **The reversal
condition is written into the entry**: a Core the operator cannot rebuild. The hatch then
belongs in Core's *own* config — machine-scoped, one copy, still registry-validated — not
in a per-project `embarch-api` field. No `inbox/` drop filed for that: it is a deferred
design with no demand, and the trigger is now recorded where the next reader will look.

**Not closed by deleting doc text.** `soc_chip_overrides` is now **refused at config load
naming the retirement, on both discovery kinds** — decision 53's posture, since nothing
deserialized the key and an author could not see the silence. `ProjectConfig` keeps the
key only so a config written from the old interface doc is told; the remedy names Core's
table and `chip-list`. One test covers both kinds and asserts the remedy, not just the
refusal.

**`api/018` is closed and deleted** — `check-doc-size.py --pressure` reports both files
PAID and nothing else in `api` in reserve. Its two flagged clauses:

- The `soc_chip_overrides` "stated and never built on both kinds" clause is **discharged,
  not preserved**: it stopped being true with this commit. It survives only as history, in
  decision 13's tombstone.
- The clause asserting decision 20's second remedy "stops a reader landing in the next
  branch of the same check" **was an overclaim, and the remedy itself is now fixed**: it
  said drop `build_command`/`chip`/`artifact_path` and stopped, so a `static` project
  following it literally met `has no west_binary` and then `has no build_dir_root` in the
  next arm of the same `validate()`. It now also says to add `west_binary`/`build_dir_root`,
  and `static_project_setting_any_zephyr_only_field_fails_validation` asserts that half.

`decisions/zephyr.md` was compacted alongside the two named files and comes out at
10,962 / 12,288 B (89.2%) — the byte it went in on. Decision 13's full retirement argument
therefore cost nothing net, but the file is still one edit from reserve.

## Done when

- [x] Decision 13 is a tombstone, rewritten in place — heading, body and rejected
      alternative are one entry, with no correction appended under a contradicted body.
- [x] `embarch-api/interfaces/config.md`'s `soc_chip_overrides` row now reads as a retired
      row beside `[[projects.targets]]`'s, naming the load-time refusal and the remedy.
- [x] Not built, so no short-circuit test. Instead:
      `a_retired_soc_chip_overrides_table_is_refused_on_both_discovery_kinds` — one config
      per discovery kind, asserting the refusal names the key, the retirement *and* the
      remedy (`chip-list`, Core's table), because a refusal whose remedy is a second dead
      end is not a fix.
- [x] `embarch-api/open.md`'s bullet is deleted; nothing replaces it.
- [x] Both **out of reserve**: `interfaces/config.md` 10,923 / 12,288 B (88.9%),
      `open.md` 3,957 / 5,120 B (77.3%). `tasks/api/018-compact-api.md` closed and `git rm`ed.
- [x] Gate green; `changelog.d/api-soc-chip-overrides-retired.removed.md` and
      `features.d/api-220-soc-chip-overrides-a-per.md` dropped. No `status.d/` fragment: no
      suite-level doc named `soc_chip_overrides` or api decision 13.
