# A `decision N` link survives a mission split still pointing at the file that no longer holds it

**State:** claimed by agent/doc/022-decision-link-mission-split, 2026-09-08 23:08
**Source:** reviewer of `topology/010` (doc merge `3079d6c`), 2026-09-06. That unit moved
`embarch-topology` decision 21 out of `decisions/enrollment.md` into a new
`decisions/validation.md`. `history/topology.md` line 8 still reads
`— [decision 21]` followed in parentheses by `../embarch-topology/decisions/enrollment.md`. Verified at the merge SHA,
not from a working tree: the commit's `--name-only` does not include `history/topology.md`.
**Scope:** doc
**Hardware:** none
**Owner:** no

## What

Two things, one root cause.

**1. The stale link itself.** `history/topology.md:8` points a reader at
`embarch-topology/decisions/enrollment.md` for decision 21, which that file no longer
contains. Repoint it at `decisions/validation.md`. Note `history/*.md` is *assembled* by
`scripts/build_changelog.py` from `changelog.d/` fragments, so a hand-edit may be
regenerated away — the durable fix may have to be in the fragment that produced that line,
or `build_changelog.py` may need to leave already-assembled windows alone. Check which
before editing.

**2. No gate can see it, and the reason generalises.** Both checks pass by construction:

- `scripts/check-links.py` validates that the *path* resolves. `decisions/enrollment.md`
  still exists, so the link is fine by its rules. It looks at filenames and fragments, not
  at whether the target still defines the thing the link text names.
- `scripts/check-decision-refs.py` resolves a number against a *sub-project*, deliberately
  (`DOC-CONVENTIONS.md`; the script's own docstring says so, and it is what makes the
  no-renumber rule cheap). `embarch-topology` still defines 21, so it resolves. Two further
  reasons it cannot catch this one even in principle: its `DOC_PATH` regex matches only
  `<sub>/design.md` and `<sub>/decisions.md`, never `<sub>/decisions/<topic>.md`; and it
  looks *backwards* `ATTRIB_WINDOW = 44` chars from the reference, while in
  a `[decision 21]` link the parenthesised path comes after. Attribution therefore falls back to the
  file's own directory — `history` — which defines no decisions, so the reference lands in
  the **warnings** bucket, which does not fail.

**This is now the common case, not a one-off.** `DOC-COMPACTION.md` §2 says a mission
split "is the other move and it is cheaper still ... Prefer it whenever the file holds more
than one mission", and `DOC-COMPACTION-PASS.md`'s procedure says "fix every inbound link in
the same commit". Every future split moves entries between `decisions/<topic>.md` files
while the sub-project's number set is unchanged — exactly the shape neither gate reports.
`topology/010` is the first split under that preference and it produced one immediately.

## Why now

`topology/010`'s own **Outcome** section states: "`history/topology.md`'s link to decision
21 was repointed to `decisions/validation.md` in the same commit, per the pass doc's rule
that no inbound link is left broken." **That did not happen** — `3079d6c` touches seven
files and `history/topology.md` is not one of them. So the landed record says the link was
fixed, the gate says green, and the link is wrong. Nothing in the queue would ever surface
that again. (This is the report, not the compaction: everything else in that unit checks
out — decision 21 is byte-identical across the move, md5 `d6337dc2df1cee27`, 4,045 bytes
both sides.)

## Already done by the supervisor at `topology/010`'s fold

The link itself is repointed and the false Outcome paragraph is corrected — both in
`topology/010`'s fold commit, where `history/` and another scope's task file are writable
and were not to the worker or the reviewer. **What is left is the gate**, which is the half
that matters: the next split will do this again.

The regeneration trap named above is **not settled** and is still the first thing to check:
`build_changelog.py` assembles `history/*.md` from `changelog.d/` fragments, and a hand-edit
to an already-assembled window may or may not survive the next fold. This fold's edit
survived one `build_changelog.py --only` run, which is evidence and not a proof.

## Done when

- [x] `history/topology.md`'s decision 21 link resolves to the file that defines decision
      21. **Whether it stays that way after `build_changelog.py` runs is still open** —
      see above.
- [ ] A check reports a `[decision N]`-plus-parenthesised-`<sub>/decisions/<topic>.md` link whose named
      target file does not define N — either as a new rule in `check-decision-refs.py`
      (it already builds the per-file number index it would need) or in `check-links.py`.
      A link is the unambiguous case: unlike bare prose, it names one file.
- [ ] The rest of the corpus is swept once with that check; earlier splits
      (`embarch-api/decisions/`, `embarch-study-designer/decisions/`, the topology split
      itself) are the places to expect hits.
- [x] `topology/010`'s Outcome paragraph is corrected — done in that unit's fold, and the
      task file is deleted at the fold, so the durable record is its supervisor-log entry.

**Note for whoever writes the check.** Three of this file's own illustrative link shapes had
to be rewritten into prose before `check-links.py` would pass, because it flags a
link-shaped string **even inside a code span** — `tasks/doc/018`. A task about link checking
was the fastest possible way to meet that defect, and it is worth fixing first: the check
you are being asked to add will want to describe the very pattern it matches.

> **`tasks/doc/018` landed 2026-09-06 (`934dfef`, owner's session).** `check-links.py` blanks
> fenced blocks and inline code spans before extracting links, so you can write the shapes
> out normally — start by restoring the three above. Two other things settled the same
> sitting, both of which this file lists as open: **a hand edit to `history/*.md` survives
> reassembly** (`build_changelog.py` inserts into the existing window; verified against a real
> assemble), so §1's regeneration trap is closed and the fix belongs in the assembled file,
> the fragment having been deleted at assembly. And `DOC-CONVENTIONS.md` now states the
> convention your sweep should apply: link `<sub-project>/decisions.md`, the routing table
> from number to topic file, not the topic file itself. **17 `history/` entries** currently
> link a topic file — that is the sweep.
