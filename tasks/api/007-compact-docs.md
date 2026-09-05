# 007 — embarch-api's open.md and decisions/surface.md are in reserve

**State:** blocked
**Source:** scripts/check-doc-size.py --pressure
**Scope:** api
**Hardware:** none
**Compacts:** embarch-api/open.md, embarch-api/decisions/surface.md
**In flux:** yes — `tasks/api/005` is open and rewrites both of these files
**Must not delete:** open.md's *do not derive a kind from the HTTP status* clause and its ordering (Core emits codes, the shared client carries one typed, this crate passes it on) — decision 50 exists because that shortcut was proposed and it is coarser than `embarch-core` decision 12's enum; decision 52's rejection of a `status --json` field, whose reason is that a diagnostic's input has to survive a broken machine.

## What

Both files are in reserve: `open.md` at ~94% of 5 KB, `decisions/surface.md` at
~92% of 12 KB. Both had a §9 pass on 2026-09-04 — `open.md` on 09-04 by hand,
`surface.md` in the same sitting, 12276 → 11305 — so **the sentence-level half
is spent** and §9 says do not run that pass twice.

Where the bytes are instead: `scripts/check-duplication.py embarch-api` reports
15 overlaps, the largest a 37-word run between `interfaces/modules.md` and
`spec.md` §5 (the 512 MiB runtime-thread paragraph, kept in both when the module
map was split out) and four between `decisions/surface.md` and
`interfaces/tools.md` about `erase`. Every one of those is a §3 question — which
file owns the claim — not a hot/cold one.

## Why blocked

`tasks/api/005` is open and its `Done when` explicitly rewrites `open.md`'s
build-log bullet and `spec.md`'s truncation paragraph. `DOC-COMPACTION.md` §8:
compacting a subsystem still in flux writes a clean statement of something about
to be wrong and destroys the alternatives you are about to need.

**Unparks when `tasks/api/005` lands**, and not on a timer.

## Done when

- [ ] Both files out of reserve.
- [ ] No question disappears from `collect-open-questions.py` unless you can
      name it as answered.
- [ ] `DOC-COMPACTION.md` §7's question answered in the commit message.
- [ ] Gate green, `changelog.d/api-*` fragment dropped.
