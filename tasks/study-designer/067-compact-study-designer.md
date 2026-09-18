# 067 — `interfaces/limits.md` and `decisions/protocols.md` are in reserve

**State:** open
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by `tasks/suite/045` — decision 75's `eap_repo` and the three advisory dev-bench caps
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/interfaces/limits.md, embarch-study-designer/decisions/protocols.md
**Size debt due:** 2026-09-24
**In flux:** no — `suite/045` closed the authoring gap `open.md` had carried since 2026-08-27, and nothing queued against this sub-project targets either file.

## What

`interfaces/limits.md` is **12,274 / 12,288 B (99.9%), 14 B left** and
`decisions/protocols.md` is **12,213 / 12,288 B (99.4%), 75 B left**. Both are
out of reserve when this closes, or the task says why not and what was deleted
instead.

The reserve was already half spent before this: decision 76 was written into
`decisions/protocols.md` and moved to `decisions/limits.md` in the same pass,
which is where a limits decision belongs and bought protocols.md ~1.4 KB. The
advisory-cap section in `interfaces/limits.md` was written twice and cut to the
table plus one line of posture, the argument living in decision 76. **Both easy
moves are already taken**, so this one is a real squeeze or a real split.

`interfaces/limits.md` is one long table plus the `.eap` block plus the new
advisory block. `DOC-COMPACTION.md` §2 prefers a split, and the seam is visible:
the `.eap` constants (decisions 58-62) are a self-contained group of eighteen
rows that nothing outside protocol work reads.

## Why now

14 bytes left means the next correction to any constant in that file cannot land
without paying first. Recording the debt is the mechanism; an unfiled file in
reserve is what `check-doc-size.py` fails on.

## Done when

- [ ] Both files out of reserve, or the task says why not.
- [ ] A split was preferred over deleting live reasoning per `DOC-COMPACTION.md`
      §2, or the report says why the seam was rejected.
- [ ] If it split: every inbound citation still resolves and the group table
      gained its row.
- [ ] Every `[measured]`/`[assumed]` marker and every provenance sentence
      survives — that column is the whole point of the file, and a constant
      whose sizing is deleted becomes a number nobody can revisit.
- [ ] Decision 75's three load-bearing properties survive in full: `scan` never
      fails on a bad file, `defs()` is the only place a duplicate name is
      refused, `save` parses before it writes.
- [ ] Byte numbers before and after, for every file touched.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.
