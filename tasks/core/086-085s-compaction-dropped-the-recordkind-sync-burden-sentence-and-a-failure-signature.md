# 086 — `core/085`'s compaction of `stream-index.md` dropped the RecordKind/five-lies sync-burden sentence and a failure-signature clause, uncounted in the fold message

**State:** open — filed by the supervisor at `core/085`'s own fold, leg 139, 2026-09-17, from its
reviewer's `inbox/` drop. Body below is the reviewer's, unchanged.

**Supervisor note — why this is a task and not a two-sentence fix I made myself.** The fix is
genuinely small: re-add two sentences to decision 62's current text. `stream-index.md` is at
**10,638/12,288 B after the compaction, ~1,650 B of headroom**, so there is no size obstacle and no
urgency to force my hand. I considered doing it inline and did not, for the same reason I declined
to edit `embarch-topology` decision 34 and `embarch-core` decision 64 earlier: **a supervisor
rewriting a sub-project's decision prose at fold time is the move this log keeps declining**, and a
restoration is still an edit to decision text that a `core` worker owns and can do with the
surrounding paragraph in front of it. The cost of routing it is one leg; the cost of the habit is
unbounded.

**Do not revert `543ffe04`.** That commit also carries decision 66 and the decision-64 correction,
which are not in question. Re-add the two sentences by hand, as the reviewer's own
`## What it would take to undo` says.

**Read this one before you start**, because it is the part that will look like texture and is not:
the sync-burden sentence names *what a maintainer of either `outpost_load.rs` or `trace.rs` must
keep in step*, and **decision 66 just made that duplication permanent rather than temporary** — so
the warning is worth more after `085` than before it, which is exactly why a squeeze reads it as
stale boilerplate.

**Also worth noting and not worth a second task:** the compaction's commit message quotes **no**
deleted hunk verbatim, which `DOC-COMPACTION-PASS.md` requires of a squeeze precisely so "carried in
substance" can be checked rather than trusted. That procedure already records three prior
occurrences (`topology/017`, `study-designer/019`, `ui/011`); this is a fourth, and the right place
for it is that file's own tally, not a new queue entry. Whoever fixes this should quote what they
restore.

**Source:** embarch-reviewer, reviewing landed unit `core/085` (`embarch-core@b6774e0`, `embarch-doc@2e7195f0`, content commit `embarch-doc@543ffe04`)
**Scope:** core
**Hardware:** none

## What

`core/085` compacted `embarch-core/decisions/stream-index.md` (11,172 B → 10,638 B) in the
same unit it added decision 66, and its commit message (`embarch-doc@543ffe04`) says the
`Must-not-delete` list from the now-deleted `tasks/core/082` was "carried in substance." Spot-
checking the deleted hunks against that claim, two carry a claim that did not make it across,
and the commit message does not quote any deleted hunk's first dozen words to make the loss
checkable — `DOC-COMPACTION-PASS.md` §"A squeeze quotes what it cut and never names a category"
requires exactly that, precisely because a squeeze cannot be trusted to classify its own cuts
(three prior legs, `ui/011` losing a live API parameter the same way).

**Residue 1 — the RecordKind/five-lies sync-burden sentence, decision 62.** Pre-085 text
(`embarch-doc@543ffe04^:embarch-core/decisions/stream-index.md`, then-decision-62's
"second implementation" paragraph) read: *"until then a change to `RecordKind`, a gap record's
semantics, or the five-lies exclusion rules has to land in both files."* This named the three
specific things a maintainer of either `outpost_load.rs` or `trace.rs` must keep in sync while
the duplication (which decision 66 now declares permanent for `Lane`/`Span`/`Gap`) stands. The
post-085 text (`embarch-core/decisions/stream-index.md` line 25) reads only *"A second
implementation of the timeline, not a second decoder — decisions 64/66 are what that
duplication resolves to."* Neither `RecordKind`, "gap record's semantics", nor "the five-lies
exclusion rules" (`embarch-ui/src/trace.rs`'s own named concept, `//! # The five lies`) appears
anywhere else in `embarch-core/`'s decisions after this commit — confirmed by grep across the
leg worktree. This is a live-property statement about another component (what must move
together), the exact class `DOC-COMPACTION-PASS.md` calls hot and non-negotiable, and now decision
66 makes the duplication permanent rather than temporary — so this warning matters *more* after
085, not less, and it is the one sentence that said it plainly.

**Residue 2 — the CSV-header pin's failure signature, decision 62.** Pre-085 text: *"a host that
inherited the arithmetic without the pin would be the same failure with a new address."* This
is the rejected-alternative's failure signature for why the `422`/`csv_header()` pin moves with
the computation (reversals row 86). Dropped; the post-085 text keeps the rule (kept the pin) but
not what skipping it would look like.

## Why this is a contradiction rather than a refinement

`DOC-COMPACTION-PASS.md` is itself a locked procedure for this repo (not a per-sub-project
decision, but the compaction gate every sub-project's pass must clear): a squeeze's commit
message must quote every deleted hunk's first dozen words, verbatim, precisely so a reviewer
can check "carried in substance" against the actual diff rather than trust it. `543ffe04`'s
message names none. That is the same failure mode `DOC-COMPACTION-PASS.md` names three prior
occurrences of (`topology/017`, `study-designer/019`, `ui/011`) — and the two hunks above are
real claims, not texture: one is a maintenance-sync warning about a live coupling decision 66
just made permanent, the other is a rejected alternative's failure signature. Neither is
recoverable from anywhere else in the compacted doc.

## What it would take to undo

`embarch-doc@543ffe04` — the compaction is entirely within this commit (the child fold
`2e7195f0` only removes `tasks/ui/067-...md` and does not touch `stream-index.md`). A revert of
`543ffe04` alone should be clean against the current tip, since nothing later in this leg
touched `embarch-core/decisions/stream-index.md`. A full revert would also undo decision 66 and
the decision-64 correction, which are not in question — undoing just the two lost sentences
by hand (re-adding them to decision 62's current text) is the narrower fix and does not need a
git revert.
