# topology: decision 18's embarch-ui/Core-client lockstep fact was dropped in the 015 compaction pass, but open.md still points at it

**State:** open
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
