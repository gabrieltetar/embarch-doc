# 010 — A reviewer reads `embarch-doc`'s working tree at the leg's start, not at the unit it is reviewing

**State:** open
**Source:** leg 012, 2026-09-05 — `umbrella/011`'s reviewer reported two facts as
"pre-existing" that were in fact *created by the unit two units earlier in the same leg*
**Scope:** doc
**Hardware:** none
**Owner:** required — the durable fix is in `.claude/agents/embarch-reviewer.md`, which
`check-ownership.py --supervisor` refuses to a leg. The leg-level workaround below is a
supervisor's and needs nobody.

## What

A leg works in a **detached worktree** of `embarch-doc` (`protocol.md` §6 step 0) and never
advances the owner's main checkout. That is the whole point of the rule — two actors in one
working tree is what swept the owner's fragments into legs 004 and 005. But an
`embarch-reviewer` is spawned into the session's ordinary working directory, so when it
reads a **file** under `/home/gabriel/Github/embarch/embarch-doc/` it sees `embarch-doc` as
it was **when the leg started**, however many units ago that was.

Its `git show <sha>` reads are fine — the objects are fetched — so **the diff it reviews is
correct and its verdict is sound.** What is wrong is everything it reads *around* the diff:
the decisions it is checking the diff against, `spec.md`, `open.md`, the reversals index.

Observed, in leg 012, on `umbrella/011`'s review:

- It reported `embarch-umbrella/decisions.md`'s index row pointing at
  `decisions/reporting.md` while "that file does not exist, and decision 37 is still at
  `decisions/doctor.md:63`". **`decisions/reporting.md` was created by `umbrella/012`, two
  units earlier in the same leg**, and decision 37 moved into it. The index was right and
  the reviewer's copy of the tree was two units old.
- It labelled that mismatch **"pre-existing (unchanged context in this diff)"** — the exact
  phrase a supervisor uses to decide not to act. `umbrella/012`'s reviewer had seen the same
  thing from the other side and said so plainly ("local `main` is behind; `811380b` is on
  `origin/main`"), which is how this was caught at all.

**The failure mode is not a wrong verdict; it is a confidently wrong `pre-existing` label**,
and that label is what routes a finding to "not this unit's problem". A reviewer that reads
stale context will systematically under-report contradictions the leg itself introduced —
which is precisely the class §10 spawned it to catch, since a leg's own units are the only
diffs it ever sees.

## Why now

It is cheap, and it gets worse as a leg gets longer: unit 1's reviewer is nearly right and
unit 4's is three units stale. It also silently degrades the one mechanism in this design
that reads for intent, and `risks.md` already names that gap as the characteristic failure.

Candidate fixes:

- **Give the reviewer the leg's worktree path** and tell it to read files there, not in the
  main checkout. This needs no file the owner reserves — a supervisor can do it in its own
  dispatch prompt today, and leg 012's log entry says so. It is a workaround, not the fix,
  because every future leg has to remember.
- **`.claude/agents/embarch-reviewer.md` states the hazard** and tells the reviewer to
  resolve its reading root from the SHAs it was given (`git -C <repo> show <sha>:<path>`)
  rather than from the working tree. That makes it correct regardless of who dispatches it.
- **The dispatch could pass the merge SHA as the reading root explicitly**, so
  "the tree as of this unit" is a thing the reviewer can name rather than infer.

## Done when

- [ ] A reviewer's reads of the docs it checks a diff against resolve to the state at the
      unit under review, not to the leg's starting state.
- [ ] The `pre-existing` judgement is only reachable when it is actually true.
