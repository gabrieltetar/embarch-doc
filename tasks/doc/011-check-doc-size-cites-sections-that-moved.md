# 011 — `check-doc-size.py` cites `DOC-COMPACTION.md` §8 and §9, which no longer exist

**State:** open
**Source:** `umbrella/015` (leg 013, 2026-09-05) — hit while answering the compaction pass's human question and finding it was not where the task said it was
**Scope:** doc
**Hardware:** none

## What

`DOC-COMPACTION.md` §6–§9 moved into `DOC-COMPACTION-PASS.md` on 2026-09-04 when
that doc reached its size cap. Four comments in `scripts/check-doc-size.py` still
cite the old numbers, three of them dangling:

- line 29 — "in flux (DOC-COMPACTION.md §8)"
- line 119 — "(DOC-COMPACTION.md §9) is held at a tighter cap"
- line 226 — "DOC-COMPACTION.md §8 warns against compacting a subsystem still in ..."
- line 99 is *correct* and is the reason this is worth fixing rather than ignoring:
  it already says "(DOC-COMPACTION-PASS.md came out of DOC-COMPACTION.md §6-§9)".
  So the file knows about the split in one place and not in three others.

All three should point at `DOC-COMPACTION-PASS.md` by section name — "Failure
modes" for §8's in-flux warning, "The second pass" for §9's tightening rule —
rather than at a number, since the numbers are what moved.

`tasks/umbrella/016` carried the same dangling reference as "`DOC-COMPACTION.md`
§7's question"; `umbrella/015` corrected that copy in the task file. **The same
stale citation is also in the fleet's worker-dispatch prose**, which a worker
cannot see the source of — whoever fixes this should check there too.

**Why it needs the owner:** `scripts/` is `never` for a worker and for a
supervisor (protocol §3), so nobody in the fleet can fix it.

## Why now

Cheap, and it is a citation *inside the enforcement script for the very protocol
it cites* — the reader most likely to follow it is someone deciding whether a
compaction is allowed to proceed. It sends them to a section that is not there,
in a repo whose whole point is that a doc's surface text is what a reader acts on
(`embarch-api` decision 51).

## Done when

- [ ] The three dangling `DOC-COMPACTION.md §8`/`§9` comments in
      `scripts/check-doc-size.py` name `DOC-COMPACTION-PASS.md` and a section title.
- [ ] A grep for `COMPACTION.md §[6789]` across the suite returns nothing but
      line 99's deliberate mention of the split itself.
- [ ] The fleet's dispatch prose checked for the same "`DOC-COMPACTION.md` §7"
      citation.
