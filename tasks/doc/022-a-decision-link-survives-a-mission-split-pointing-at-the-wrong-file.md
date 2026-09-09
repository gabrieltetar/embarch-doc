# A `decision N` link survives a mission split still pointing at the file that no longer holds it

**State:** blocked by agent/doc/022-decision-link-mission-split, 2026-09-08 — manual corpus
sweep done; the check itself needs `scripts/` write, which no worker has (see `## Blocked`
below and `inbox/022-b-decision-ref-check-needs-scripts-access.md`)
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
      **Blocked for a `doc`-scope worker — see below.**
- [ ] The rest of the corpus is swept once with that check. **Also blocked for this
      worker, for a second, independent reason:** `history/*.md` is not writable by *any*
      scope's worker (`check-ownership.py`'s allow-list has no `history/` entry for any
      scope, and this file's own "Already done by the supervisor" section already says so
      — history is fold-time-only, like the `topology/010` fix that motivated this task).
      I found and hand-verified the candidates before realising this (see below) and then
      reverted the edit rather than land it from the wrong row.
- [x] `topology/010`'s Outcome paragraph is corrected — done in that unit's fold, and the
      task file is deleted at the fold, so the durable record is its supervisor-log entry.

## Blocked

**Two independent blockers, both outside a `doc`-scope worker's write set.**

**1. The check.** Both candidate homes — `scripts/check-decision-refs.py` and
`scripts/check-links.py` — are under `scripts/`, which `embarch-fleet/protocol.md` §3's
ownership map does not grant to *any* worker (only supervisor and owner have write
there), and my own dispatch explicitly lists `scripts/` as a reserved path with
instructions to stop and say so rather than edit it. This is that stop.

**What is needed, for whoever picks this up next (owner session, or a leg with `scripts/`
write):** a rule that, for a link of the form `[decision N](...)`  or `([decisions](...) N)`
whose href matches `<sub>/decisions/<topic>.md`, looks up N in that sub-project's per-file
number index (`check-decision-refs.py` already builds this) and fails if the href's own
topic file is not the one that defines N. The natural home is `check-decision-refs.py`:
it already parses `DOC_PATH` against `<sub>/design.md`/`<sub>/decisions.md`; this needs a
sibling regex for `<sub>/decisions/<topic>.md` hrefs specifically (not bare prose paths),
and a lookup against the already-built number→file map instead of the current
number→sub-project set. `check-links.py` only validates that a path resolves, not what it
defines, so extending it would duplicate the number index this script already has.

**2. The sweep.** Even once the check exists, running it and landing the fixes touches
`history/*.md` across seven sub-projects (`api`, `core`, `outpost`, `study-designer`,
`suite`, `topology`, `ui`, `umbrella` all have at least one hit) — no scope's worker can
write `history/` (`check-ownership.py`'s allow-list has no `history/` entry for any
scope), so this is fold-time or owner-session work like the `topology/010` fix itself.

**What I found by hand, ahead of the check, so it is not re-derived from scratch:** every
markdown link of the `[decision N](<sub>/decisions/<topic>.md)` shape currently in
`history/*.md`, and for each, whether the linked topic file still defines N (checked
against each sub-project's `decisions.md` routing table). All of them currently *do*
resolve correctly today — this task's own bug (`history/topology.md`'s stale decision-21
link) was the only live instance, and it was fixed at `topology/010`'s fold. 26 links
match the shape; 4 are dated entries that *narrate* a split as it happened
(`history/topology.md:13`, `history/core.md:13`, `history/core.md:16`,
`history/umbrella.md:24`) and are exempt from the "link the index" convention by
`DOC-CONVENTIONS.md`'s own worked example (`history/api.md`'s decision-30 line); the other
22, in `history/{api,core,outpost,study-designer,suite,topology,ui,umbrella}.md`, are
ordinary citations that should be repointed at `<sub>/decisions.md` per
`DOC-CONVENTIONS.md`'s "link the index, not the topic file" rule, once someone with
`history/` write lands it. I drafted and verified those 22 edits, then reverted them
without committing — landing them from this row would have been the same ownership
violation as the check itself, just on data instead of code. The verified edit list is not
preserved anywhere durable beyond this note; whoever lands it should re-derive it (it is
mechanical: grep `history/` for the link shape, cross-check each href's topic file against
its sub-project's `decisions.md` table) or ask, since re-deriving is cheap and I did not
want a stale diff sitting in the inbox drop.

Nothing stops the next mission split from producing a fresh instance of the underlying
bug — that risk is exactly what the check would remove, and it remains open until someone
with both `scripts/` and `history/` access builds and runs it. An `inbox/` drop with this
content was filed at `embarch-doc/inbox/doc-decision-ref-check-topic-file-mismatch.md` so
it is not only in a task file, which is deleted at fold.

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
