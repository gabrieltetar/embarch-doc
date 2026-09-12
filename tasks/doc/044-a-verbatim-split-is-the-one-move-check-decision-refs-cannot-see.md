# 044 — A verbatim split is the one move `check-decision-refs.py` structurally cannot see, and it broke six citations in one leg

**State:** open
**Source:** leg 085, 2026-09-11. Both of that leg's two units hit it, independently, and in both
cases the **gate was green with the citations wrong** — they were caught only because a reviewer
was spawned and told to sweep for them by hand.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/check-decision-refs.py` (and possibly
`DOC-COMPACTION.md` §2's split guidance), both reserved paths.

## What

`check-decision-refs.py` validates that a cited **decision number** exists. A verbatim split —
`DOC-COMPACTION.md` §2's *preferred* way to pay a size debt — moves a decision's body to a new file
**without changing its number**. So every citation that names the old file keeps pointing at a file
that no longer contains the decision, and every check still passes:

- the number is still real, so the decision-ref check is satisfied;
- the old file still exists, so `check-links.py` is satisfied;
- nothing was deleted, so the compaction rules are satisfied.

**A split is precisely the operation this check cannot observe**, and it is the operation the size
rules actively push every compaction toward.

## The evidence, from one leg

Two units, two splits, six broken citations, gate green both times:

**`api/067`** — `decisions/core-link.md` split, decisions 36, 37/38, 55, 58, 62, 66 moved to new
`decisions/client-crate.md`. Stale afterwards:
- `history/api.md:50` (decision 62)
- `embarch-api/decisions/tests.md:32` (decision 55)
- `embarch-api/decisions/hardware-selection.md:59` (decision 58)

**`core/041`** — `decisions/surfaces.md` split, decisions 25, 27, 28, 50, 54, 57 moved to new
`decisions/enrollment.md`. Stale afterwards:
- `tasks/topology/011:45` (decision 25, cited as `surfaces.md:30`)
- `embarch-topology/decisions/enrollment.md:29` (decision 25, same line citation) — **this one is
  cross-repo**, which is the shape a sub-project worker cannot fix and would not see
- `tasks/umbrella/045:34` (decision 57) — **also cross-repo**

All six were repaired at the folds. The point of filing this is that **repairing them depended on
a reviewer being spawned and given the sweep as an explicit instruction**, which is not a
mechanism — the leg before this one split a file too, and nothing says whether its citations
survived.

## Two aggravating details

1. **Line-number citations make it worse and are common.** Three of the six cited a *line*
   (`surfaces.md:30`), which is stale after any edit to the file above that line, split or not.
   Repairing them meant reading the cited body to work out which decision was meant.
2. **A split is when this fires, but an ordinary decision *move* between topic files does it too**
   — the mission-split case `tasks/doc/022` already describes for links. That task and this one
   are the same root cause seen through two different checks; whoever takes either should read the
   other.

## Candidate direction

The information needed is already on disk and already assembled: `embarch-<scope>/decisions.md`
carries an index row per topic file listing which decision numbers it holds. So a check can
resolve `<repo> decision N` to the file that actually holds `N` and fail a citation that names a
different one — no new metadata, no convention for authors to remember.

Consider also making the **decision number the only supported citation form** and failing a
`path:line` citation into a decisions file outright. That is the form that cannot survive a split,
and every instance found in this leg was repaired by replacing it with a number.

## Done when

- [ ] A citation naming a decisions file that does not hold the cited number fails the gate.
- [ ] The six citations above would each have failed it before they were repaired (use them as the
      fixture — they are recorded here with their old text).
- [ ] Cross-repo citations are covered, since two of the six were cross-repo and a sub-project
      worker cannot see those.
- [ ] Whether `path:line` citations into decisions files stay legal is decided either way and
      written down.
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
