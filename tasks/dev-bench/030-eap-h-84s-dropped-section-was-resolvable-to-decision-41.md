# 030 — `eap.h:84`'s dropped `§4.9` was resolvable to `decision 41`, not unresolvable

**State:** claimed — leg 108, 2026-09-13, dispatched to `agent/dev-bench/030-eap-h-decision-41`
**Source:** reviewer pass on `dev-bench/026` (embarch-doc merge `c133703573648f1c4d959f04ccd509d5ba8c400f`),
which closed as "already resolved by `dev-bench/029`" (`embarch-dev-bench` commit `4816230`).
Re-derivation against `embarch-dev-bench/decisions/protocols.md` and `conventions.md` at
`/home/gabriel/Github/embarch/.worktrees/embarch-doc/leg`.
**Scope:** dev-bench
**Hardware:** none — a citation/comment-text question, no board involved.
**Owner:** no

## What

`app/src/eap.h:84` (in `embarch-dev-bench`) used to read:

    SRAM more than 2 does. Both worked protocols in that doc's §4.9 use **one**
    arm per state; ...

`dev-bench/029` (commit `4816230`) deleted the `in that doc's §4.9` clause outright, leaving:

    SRAM more than 2 does. Both worked protocols use **one**
    arm per state; ...

`dev-bench/026`'s closure (the unit under review) re-checked this and recorded: "no numbered
decision states the one-arm-per-state rule, and the crate is already named two lines up, so
deletion was the right branch, not repointing." That check was scoped to
`embarch-study-designer`'s decisions (correctly finding nothing there — confirmed independently,
no hit for "arm" content in that repo's decisions or spec). But the sentence being edited is not
about the crate's wire types (`embarch-study-designer` decisions 58-62, already cited two lines
up at `eap.h:1`) — it is about the **event-arm cap**, a dev-bench-local sizing decision
(`EAP_MAX_EVENT_ARMS_PER_STATE`, defined three lines later at `eap.h:90`). That decision is owned,
in this same repo, by `embarch-dev-bench/decisions/protocols.md` decision **41**:

> "Every ceiling matches the crate except the per-state event-arm count, which is 2 against the
> crate's 4: ... and **both worked protocols use one arm per state.** Refused by name at decode,
> never truncated ..."

— the same claim, same reasoning, same rule, word for word, already recorded under a decision
number in the same repo as the comment being edited.

## Why this is a contradiction rather than a refinement

`embarch-dev-bench` decision 47 (`decisions/conventions.md`, one day old, the exact rule this unit
applies) states a mandatory three-way resolution for a bare `§N`: **"If the cited material is now
owned by a specific decision ... resolve to that decision"** is the first branch, and deletion is
reserved for "where no decision or document actually resolves it." Decision 41 does resolve
`eap.h:84`'s claim — in the same repo, not even cross-repo — so the citation should have become
`` `decision 41` `` (own-repo bare form, per decision 47's own citation grammar), not nothing.
Both `dev-bench/029` (who made the edit) and `dev-bench/026` (who re-verified it and closed the
task as fully resolved) checked only whether `embarch-study-designer` states the rule, not whether
`embarch-dev-bench`'s own decisions do — an incomplete check that both units then affirmed as
complete. This is not a style nit: `026`'s "Done when" checklist item for exactly this line is now
checked off as correctly handled, which closes the door on anyone looking again.

## What it would take to undo

- **Code fix** (not part of either unit's diff): `embarch-dev-bench` commit `4816230`
  (`dev-bench/029`) made the deletion; reverting that one line is clean (single-line, no
  dependents) but would restore the dead `§4.9`, not fix it — the actual fix is a small forward
  edit to `app/src/eap.h:84`, repointing to `` `embarch-dev-bench` decision 41 `` (or bare
  `decision 41`, own-repo form), not a revert.
- **Doc fix**: `embarch-doc` commit `c133703573648f1c4d959f04ccd509d5ba8c400f`
  (`dev-bench/026`)'s task-file closure asserts this line is correctly resolved; a clean revert of
  that commit (task-file-only diff) reopens the task but does not by itself correct the
  misstatement — the task's own "Done when" text would need the correction alongside the code fix.

## Done when

- [ ] `app/src/eap.h:84` cites `decision 41` (own-repo bare form, per decision 47's citation
      grammar) for the one-arm-per-state claim, as a **forward edit** — do not revert `4816230`,
      which would restore the dead `§4.9`.
- [ ] `tasks/dev-bench/026`'s closure text is corrected where it records this line as correctly
      deleted. That assertion is the reason nobody would look again, and leaving it standing is
      most of the cost of this defect.
- [ ] The same question is asked of the **other** citations `dev-bench/029` deleted rather than
      repointed: for each, was there an `embarch-dev-bench`-owned decision that resolves it? Both
      prior units checked only `embarch-study-designer`, so the own-repo half of decision 47's
      branch 1 has never been swept. Report the count either way — a clean sweep finding nothing
      is a useful result and should be recorded, not left silent.
- [ ] Gate green; `changelog.d/` fragment if anything reader-visible changed.

## Note from the supervisor (leg 107)

Filed from a reviewer's `inbox/` drop on the same leg that landed `dev-bench/026`. **The
generalisation in the third item is mine, not the reviewer's** — the reviewer found one instance
and proved it; whether there are others is unmeasured, and a worker should treat it as a question
to answer rather than a defect to assume.

**Do not read this as `026` having been wrongly closed.** Its main finding — that `dev-bench/029`
had already resolved the six citations the task named — was verified independently and holds. What
is wrong is narrower and worth stating precisely: one of those six was resolved by **deletion**
when a decision in this repo owned the claim, and two units in a row confirmed that deletion after
searching only the other repo.
