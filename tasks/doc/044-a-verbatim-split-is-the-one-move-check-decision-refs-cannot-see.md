# 044 — A verbatim split is the one move `check-decision-refs.py` structurally cannot see, and it broke six citations in one leg

**State:** done — owner session, 2026-10-29, branch `owner/decision-refs`: inline-code and paren shapes judged against the named file outside `tasks/`/`history/`, a `:line` suffix refused outside `tasks/`; four of the six fixtures fail, the two task-file ones are exempt by design; see `## Closed`
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

- [x] A citation naming a decisions file that does not hold the cited number fails the gate.
- [x] The six citations above would each have failed it before they were repaired (use them as the
      fixture — they are recorded here with their old text). **Four of six** — the two in `tasks/`
      are exempt by design; see below.
- [x] Cross-repo citations are covered, since two of the six were cross-repo and a sub-project
      worker cannot see those.
- [x] Whether `path:line` citations into decisions files stay legal is decided either way and
      written down.
- [x] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).

## Closed

**The candidate direction, without the index.** Each sub-project's `decisions.md` table was not
needed: the script already built a number→file map from the headings themselves (`tasks/doc/027`),
which is the ground truth the table summarises. What was missing was the *shapes* that name a
file. `tasks/doc/056` added the link shapes; this adds the rest:

- **A topic path in inline code with the number beside it** — `decision N` right after the code
  span, or `decision N (` right before it. A bare `decisions/<topic>.md` belongs to the sub-project
  the sentence names just before it (`embarch-core` decision 57 (…)), else the citing file's own.
- **Any relative href**, so a decisions file citing its sibling as `core-link.md` is resolved —
  two of the six were exactly that, and the old pattern required `decisions/` in the href.
- **A `:line` suffix on a decisions file is refused outside `tasks/` and `inbox/`.** Zero such
  citations exist outside `tasks/` today, so nothing turned red. Inside `tasks/` there are 36, all
  evidence of what a file said on the day the task was filed — legal, because rewriting evidence
  is worse than a stale line number in a record.

**Why inline code is not read in `tasks/` and `history/`.** Run there, it flagged 12 lines: a
`history/core.md` entry narrating a renumber (the case `DOC-CONVENTIONS.md` says to keep), a task
quoting the bad citation it reports, a task's own title, and nine stale pointers — every one in a
`done` task. A backticked path in a record is usually the subject of a sentence about the past. A
link is a pointer, so links stay judged everywhere.

**The fixtures, as self-tests the gate runs** (old text, synthetic index mirroring both splits):
`history/api.md` (62), `embarch-api/decisions/tests.md` (55), `embarch-api/decisions/hardware-selection.md`
(58) and `embarch-topology/decisions/enrollment.md` (the `:line` one) all fail. `tasks/topology/011`
(a `:line` in a task) and `tasks/umbrella/045` (inline code in a task) pass by design; the second is
also a fixture in a current-truth doc, where it fails. Against the logic before `tasks/doc/056`
every one of them produced no finding at all.

**On `main`:** green before and after. Citations naming a topic file now checked: 87 → 257 across
this change and `tasks/doc/056`. **Not covered**, and recorded in the script header: a number near a
topic path that is not adjacent to it, `decision N in` a backticked path, and anything outside
`*.md`. `DOC-COMPACTION.md` §2 needed no change — the split stays preferred, and the gate now sees
what it breaks.
