# 068 — `embarch-study-designer/decisions/declares.md` is in reserve

**State:** done
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by decision 77
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/decisions/declares.md
**Size debt due:** 2026-09-25
**In flux:** no

## What

The declares group is **12,200 / 12,288 B (99.3%), 88 B left**. Out of reserve
when this closes, or the task says why not.

The entry that crossed the floor is **77** — a study's own build spec and the
outpost mode it requires. It was trimmed five times on the way in.

## Why the seam is a split, not a squeeze

The file's own header says it is about "firmware versions, and how each is
verified", and decision 40 is that. Decision 77 is a different thing wearing the
same field: **what a study builds**, and **what it refuses to run against** —
one is a version string compared after the fact, the other a selection resolved
before the run and a mode read off the wire. The GATT half already left this
file on 2026-09-13 for exactly this reason.

So: `decisions/builds.md`, decision 77 moved verbatim, per
[../../DOC-BUDGET.md](../../DOC-BUDGET.md) §3. Decision 40 stays, and its
"verification asymmetry" paragraph gains a pointer to the file that closes the
DUT half of it.

## No longer in flux

**A study carrying a real `BuildSpec` built and ran on 2026-09-19** with two
snippets and no extra args — well inside `MAX_SNIPPETS_PER_BUILD` (8) and
`MAX_BUILD_EXTRA_ARGS` (8), and nothing in that run argues for moving either.
The entry is stable; the split is now ordinary compaction work.

## Dispatch note (supervisor, 2026-09-28)

Three days past its clock. **Also in reserve in `study-designer`, not yours to write:**
`decisions/gatt-extract.md` **36 B left** (`tasks/study-designer/069`, open — a separate unit, so
leave it alone even if a seam looks shared), `spec.md` 840 B left (`tasks/study-designer/032`,
blocked), and `open.md` at 5,447 / 5,120 B, over its role cap (`tasks/study-designer/026`,
blocked). A new sibling file and a `decisions.md` routing-table row are the only other writes this
should need; if your work pushes any other file into reserve, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit.

## Done when

- [x] Out of reserve: `decisions/declares.md` 12,200 B (99.3%) -> 8,896 B
      (72.4% of the 12,288 B cap).
- [x] **The three rules a reader will try to simplify survive**: no pinned
      `build_id`, no project name in the spec, and two masks rather than one.
      Each is a rejected alternative, not a detail. Moved verbatim into
      `decisions/builds.md`, so all three are byte-identical to the original.
- [x] `decisions.md`'s index row updated (new row for `decisions/builds.md`,
      77), and the "seventeen files" count corrected to twenty — the directory
      held 19 files before this split (`tasks/study-designer/066` was right
      that seventeen was already stale) and holds 20 after it.
- [x] Every inbound reference to 77 still resolves within this sub-project
      (`check-decision-refs.py`). **One inbound reference from a different
      sub-project does not**: `embarch-ui/decisions/firmware-build.md:7` links
      decision 77 straight at `declares.md`, which no longer defines it. A
      `study-designer`-scope worker cannot write `embarch-ui/`
      (`check-ownership.py`), so this is not fixed here — filed instead at
      `/home/gabriel/Github/embarch/embarch-doc/inbox/ui-decision-77-link-stale-after-study-designer-split.md`,
      per the `tasks/doc/022` precedent for exactly this failure mode (a
      mission split's old topic-file link going stale). `check-decision-refs.py`
      (part of `check-docs.py`) is RED on this repo until that inbox item
      lands — the only red in the gate.
- [x] Byte numbers before and after: `declares.md` 12,200 -> 8,896 B;
      `builds.md` 0 -> 4,059 B (new); `decisions.md` 3,618 -> 3,730 B.
      Decision 40 (stayed in `declares.md`, gained the pointer to 77) is
      pinned at a 4,608 B baseline; it is now 4,462 B, under it.
- [x] Gate green except the one known, filed, cross-scope red above; `changelog.d/`
      fragment dropped (`study-designer-declares-builds-split.changed.md`).
