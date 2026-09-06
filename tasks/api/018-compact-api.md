# 018 — `interfaces/config.md` and `open.md` are back in reserve

**State:** blocked
**Source:** scripts/check-doc-size.py --pressure, after `api/016`
**Scope:** api
**Hardware:** none
**Compacts:** embarch-api/interfaces/config.md, embarch-api/open.md
**In flux:** yes — `tasks/api/017` is open and rewrites or deletes `interfaces/config.md`'s `soc_chip_overrides` row and `open.md`'s only remaining `api`-owned bullet. Whichever way it goes it changes both files, so a pass now would be compacting text about to be rewritten. `017` is the only thing this waits on.
**Must not delete:** the `soc_chip_overrides` row's statement that it is **stated and never built**, and that declaring it does nothing on *either* discovery kind — that fact exists in no other doc and is the whole content of `017`; decision 20's five-field load-time refusal and its two remedies, since the second remedy is what stops a reader landing in the next branch of the same check; decision 21's three-way `["none"]` rule and the sentence saying the collision remedy is *conditional* on `default_snippets` being empty — the unconditional phrasing is the defect `016` removed and it reads perfectly plausible; decision 51's "absent stays absent" clause; the `[[projects.targets]]` retired row and its per-`discovery` advice split, which is `api/015`'s whole finding.

## What

`api/012` paid this sub-project's whole debt on 2026-09-05 and both files came out. `api/016`
put two back on the same day:

- **`embarch-api/interfaces/config.md` — 11,844 / 12,288 B, 444 B left (96.4%).** It was
  11,035 B (89.8%) before, one byte off the line either way. `016` added the load-time
  refusal's field list and remedies, rewrote the `soc_chip_overrides` row into a
  designed-vs-built pair, and made the `["none"]` collision remedy conditional. It also
  *shortened* the `[projects.default_target]` row, which had restated most of decision 20's
  reasoning; that is where the cheap bytes were and they are spent.
- **`embarch-api/open.md` — 4,638 / 5,120 B, 482 B left (90.6%).** `016` closed a
  two-part bullet and replaced it with a one-part one that is longer than half its
  predecessor, because the finding underneath it grew.

`decisions/zephyr.md` took the larger share of `016`'s new text and came out at
10,966 / 12,288 B (89.2%), just under. Treat it as the third file if a pass is being run
anyway — it is one edit from the line and the compaction is per sub-project.

Run `scripts/check-duplication.py embarch-api` first. `016` deliberately states the
five-field refusal in three places — `spec.md`'s pointer sentence, `interfaces/config.md`'s
paragraph, decision 20 — at three different depths; that is the reference/reasoning split,
not duplication, and collapsing it is how the pointer stops being findable. The real
overlap to look for is between `interfaces/config.md`'s prose paragraphs and the table rows
directly above them.

## Why now

Not now: `In flux: yes`. Filed so the runway is recorded rather than rediscovered by
whoever is next blocked by arithmetic. **444 B is roughly one table row**, so the next
`api` unit that has to document a config field will hit this before it hits anything else.

## Why blocked

`tasks/api/017` rewrites both files, and its two outcomes change them by different
amounts — building `soc_chip_overrides` grows the row and the field list, retiring
decision 13 deletes both. Unparks when `017` closes.

## Done when

- [ ] `embarch-api/interfaces/config.md` out of reserve.
- [ ] `embarch-api/open.md` out of reserve.
- [ ] Every `Must not delete:` item still findable, by search, in the compacted text.
- [ ] [DOC-COMPACTION-PASS.md](../../DOC-COMPACTION-PASS.md)'s human question — *can
      `spec.md` plus `interfaces/config.md` answer what someone needs to configure this
      crate today?* — answered in the commit message.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/api-*` fragment
      dropped.
