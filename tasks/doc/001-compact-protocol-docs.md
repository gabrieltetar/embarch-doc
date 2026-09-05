# 001 — The two protocol docs are in reserve, and only the owner can compact them

**State:** open
**Source:** scripts/check-doc-size.py --pressure — both files inside the last 10% of the 12 KB protocol cap
**Scope:** doc
**Hardware:** none
**Owner:** required
**Compacts:** DOC-PROTOCOL.md, DOC-COMPACTION.md
**In flux:** no
**Must not delete:** §9's hot and cold lists and the constraint-vs-evidence refinement under them; §8's six failure modes; §7's human question; §5's entry shape; DOC-PROTOCOL §7.3's two breakage classes; §7.4's tombstone example; §7.1's state vocabulary.

## What

Both files sit in reserve — `DOC-PROTOCOL.md` at ~96.6% and `DOC-COMPACTION.md`
at ~96.5% of their shared 12 KB cap — and **no agent may edit either**
(`embarch-fleet/fleet.toml` reserves them, `check-ownership.py` enforces it), so
this can only be done in the owner's own session. It is filed here rather than
nowhere because a wall nobody can see is the failure this whole mechanism
exists to remove.

**Read this before starting: a §9 pass will not be enough.** Both were given one
on 2026-09-04 and it netted 335 bytes on ~900 bytes of gross deletion, because
the read that finds cold prose is the same read that finds the defects worth
fixing — that pass had to *add* three missing rows to §2's budget table, a
`--pressure` line, and the reserve rule itself. §9 says a doc past its hot floor
takes rules when you cut further, and these two are there. **Expect the answer
to be structural**: a split of `DOC-COMPACTION.md` §9 (the second-pass method,
run occasionally) away from §1–§8 (the standing budget, loaded constantly) is
the shape §3 prescribes for any other doc, and it has no sanctioned filename or
cap row yet. Deciding that is the work.

## Why now

They are the two docs the fleet structurally cannot fix, and every other file
that was at its cap on 2026-09-04 has been relieved. If these strangle, the
protocol the whole corpus runs under becomes uneditable, and the first symptom
is a task that cannot be written.

## Done when

- [ ] Both files are out of reserve, or the cap row that governs them has been
      changed deliberately with the reason recorded — **not raised to make room**
      (§2 is explicit that the cap is the constraint, not a target).
- [ ] If `DOC-COMPACTION.md` split, the new file has a role row in
      `check-doc-size.py`'s `CAPS`, a classification in `fleet.toml`
      (`reserved`, since it carries the same rules), and every inbound `§N`
      citation is fixed in the same commit.
- [ ] `DOC-COMPACTION.md` §7's question answered in the commit message, in your
      own words, for each file.
- [ ] Gate green (`embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/doc-*` fragment dropped.
