# 027 — A `[decision N]` link to a topic file is never checked against what that file defines

**State:** open
**Source:** `inbox/doc-decision-ref-check-topic-file-mismatch.md`, filed 2026-09-08 by
`agent/doc/022-decision-link-mission-split` after it found both halves of `tasks/doc/022`
outside a worker's write set. Drained into the queue by leg 056, which also declined to do
the sweep half at a fold — see "Why this is not dispatchable" below.
**Scope:** doc
**Hardware:** none
**Owner:** required for item 1; **item 3 is a supervisor's, at a fold.** Neither is a
worker's, so this task must not be dispatched.

## Why this is not dispatchable

`scripts/` is `never` for both worker and supervisor (`embarch-fleet/protocol.md` §3), and
`history/*.md` has no scope entry in `check-ownership.py`'s allow-list at all, so no worker
can write it — the `doc/022` worker drafted the 22 edits, verified each, and then **reverted
them without committing** rather than land rows it does not own. That was the right call and
it is why this task exists rather than a branch.

## What

A mission split (`DOC-COMPACTION.md` §2) moves a numbered decision from one
`<sub-project>/decisions/<topic>.md` into another without renumbering
(`DOC-CONVENTIONS.md`'s no-renumber rule). A link elsewhere shaped
`[decision N](<sub-project>/decisions/<old-topic>.md)` keeps resolving — the file still
exists — while naming the wrong file for N. **Neither gate catches it:**

- `check-links.py` validates that a path resolves, not what the target defines.
- `check-decision-refs.py` resolves a number against a *sub-project*, deliberately, and its
  `DOC_PATH` regex matches only `<sub>/design.md` and `<sub>/decisions.md` — never
  `<sub>/decisions/<topic>.md`. A link naming the old topic file therefore falls back to
  attributing by the *linking* file's own sub-project, which is usually wrong, and when it
  happens to be right it reports a WARNING for an unrelated reason (`ATTRIB_WINDOW` looks
  backwards, and a `[decision N](path)` link's path comes after).

`topology/010` (doc merge `3079d6c`, 2026-09-06) produced exactly this: decision 21 moved
`enrollment.md` → `validation.md` and a link in `history/topology.md` kept pointing at
`enrollment.md`.

**A manual sweep of the corpus was done and not landed.** Every `history/*.md` link of this
shape was checked against its sub-project's `decisions.md` routing table: **all 26 resolve
correctly today** — the `topology/010` link was the only live instance and was fixed at that
fold. Of the 26, **22** are ordinary citations that `DOC-CONVENTIONS.md`'s "link the index,
not the topic file" rule says should point at `<sub>/decisions.md`, spread across
`history/{api,core,outpost,study-designer,suite,topology,ui,umbrella}.md`; the other **4**
narrate a split as it happened and are exempt per that doc's own worked example.
**That list was not preserved** and must be re-derived — mechanically, by grepping `history/`
for the link shape and cross-checking each href's topic file against the sub-project's
`decisions.md` table.

## Why now

`DOC-COMPACTION.md` §2 prefers a mission split "whenever the file holds more than one
mission", and `DOC-COMPACTION-PASS.md` requires fixing every inbound link in the same commit.
Leg 056 alone performed **three** mission splits in four units — `outpost/012` (decision 22 →
`decisions/testing.md`), `topology/017` (decision 26 → `decisions/validate-timing.md`) and
`ui/019` the leg before. This is now a routine event, and it is exactly the shape no gate
reports.

## Done when

- [ ] **(1, owner)** A check reports a `[decision N](…)` link whose href matches
      `<sub>/decisions/<topic>.md` when N is not among the numbers that topic file defines.
      The natural home is `check-decision-refs.py`: it already builds a per-file number index.
      It needs (a) a regex for `<sub>/decisions/<topic>.md` *hrefs* specifically, distinct
      from the existing `DOC_PATH`, and (b) a lookup against the number→file map rather than
      the current number→sub-project set. Extending `check-links.py` instead would duplicate
      that index — prefer the former unless there is a reason not to.
- [ ] **(2)** Run it once against the corpus. Expected clean today, which is itself the
      confirmation that the manual sweep was right.
- [ ] **(3, supervisor at a fold, or the owner)** Land the 22-link repoint into `history/*.md`.
      Re-derive the list first; do not trust the counts above without re-checking, since the
      corpus has moved three splits since they were taken. **This is a unit of work, not a
      ride-along** — leg 056 considered doing it inside `doc/022`'s fold and declined, because
      each of the 22 needs a routing-table lookup and a wrong one writes a false link into
      `history/` silently, which is the same class of defect this task exists to close.
- [ ] `DOC-CONVENTIONS.md`'s "link the index, not the topic file" rule needs no change; this
      is only the check and the sweep that make it self-enforcing.

**Not a new decision.** A check/tooling fix and a mechanical sweep, no design choice about any
sub-project.
