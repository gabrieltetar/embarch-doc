# topology: decision 18's embarch-ui/Core-client lockstep fact was dropped in the 015 compaction pass, but open.md still points at it

**State:** claimed by `agent/topology/016-lockstep-fact-restored`, leg 039, 2026-09-07
**Source:** `embarch-reviewer` on topology/015 (merge `2b414cc428d6ae65572d7d37426a4c17a6181496` in embarch-doc; no code merge), filed from `inbox/` by the supervisor, leg 038
**Scope:** topology
**Hardware:** none — two doc files; confirming it needs a `git show` of the merge's parent, not a board.
**Owner:** no

## What

`topology/015`'s DOC-COMPACTION-PASS second pass over `embarch-topology/decisions/links.md`
decision 18 deleted a specific factual claim that decision 18 used to carry and
that nothing else in the suite states:

> "Two facts about what that landing costs, recorded here so they need not be
> re-derived: `embarch-ui` needs no change — it renders only an alert's reason,
> role and timestamp — while the mirrored alert type in the shared Core client
> declares those fields non-optional and would have to move in lockstep."

(pre-trim `embarch-topology/decisions/links.md`, decision 18, in the commit's
parent `2b414cc428d6ae65572d7d37426a4c17a6181496~1`)

The trimmed decision 18 (same file, post-commit) keeps the "half fired /
half has not, because no capture has been read off a DUT" fact and the
"deliberately held busy" fact — both of those also survive verbatim in
`embarch-topology/open.md` line 7-8, confirming the pass did carry those two
forward correctly. But the embarch-ui / Core-client non-optional-fields fact
has no surviving copy anywhere: it is not in the trimmed decision 18, not in
`open.md`, and a suite-wide grep for "non-optional", "move alongside",
"move in lockstep", "reason, role" at the merge SHA turns up exactly one hit —
`open.md`'s own reference to it, not a restatement of it.

`open.md` line 7 still reads: "Decision 18 holds the shape, the trigger ...
**and what has to move alongside it when it lands**." That clause is no longer
true — decision 18 no longer states what has to move alongside it, or that
`embarch-ui` is exempt while the Core client type is not.

## Why now

This is exactly the failure mode DOC-COMPACTION-PASS exists to avoid: the
commit message says the pass "kept every claim, constraint, rejected
alternative and failure signature," and every other check in this review
confirms that held for decisions 17, 18 (its other clauses) and 24. This one
clause is the exception — a measured, load-bearing observation (which
component needs a change, which doesn't, and why) that got compacted away
under general "amendment-chain narrative" trimming, while the pointer to it
in `open.md` survived unedited and now dangles.

Not a code contradiction (there is no code merge for this unit) and not a
retraction anyone made a case for — it looks like an oversight in what counted
as "cold" during the pass.

## Done when

Either the fact is restored into decision 18 (or `open.md` itself, or wherever
the suite decides it belongs) in its own right, or `open.md` line 7's "and what
has to move alongside it when it lands" clause is removed/rewritten to stop
citing decision 18 for a fact decision 18 no longer contains.

## Supervisor's note, leg 039

**Verify the fact before you restore it — do not copy it forward on the strength of
this task file.** It is a claim about two other repos: that `embarch-ui` renders only an
alert's reason, role and timestamp, and that the mirrored alert type in
`embarch-api/crates/embarch-core-client/src/client.rs` declares those fields non-optional.
Both are checkable in the code as it stands today, and a fact that was true when decision 18
was written may not be true now — restoring a stale claim verbatim is a worse outcome than
the dangling pointer. **Read `AlertResponse` in `client.rs` and the alert rendering in
`embarch-ui/assets/app.js` yourself, and say in your commit message what you found.** You may
read any repo; you may only *write* `embarch-topology` and `embarch-doc/embarch-topology/`.

**Prefer restoring the fact over deleting the pointer** if it checks out: it is a measured
observation about what a future landing costs, and `open.md` already advertises it. If it does
*not* check out, do not restore it — fix `open.md`'s clause instead and record what you found
in the same commit, because "the fact was wrong" is the more valuable finding.

**Reserve, this scope:** `embarch-topology/open.md` is 4,322/5,120 B — **798 B left**, filed
against `tasks/topology/014-compact-topology.md`, which is `open`, not blocked. If your work
pushes that file further into reserve or leaves it there, `tasks/README.md`'s rule applies and
you file/update the compaction task in the same commit rather than doing the compaction.
`decisions/links.md` was just compacted by `topology/015` and has room.
