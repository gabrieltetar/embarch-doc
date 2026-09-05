# 006 — Recovery reclaims a claim by counting commits, and a killed worker's work is not in a commit

**State:** open
**Source:** owner's session, 2026-09-05 — found while tidying after leg 009's cancellation
**Scope:** doc
**Hardware:** none
**Owner:** required

**`Owner: required`** — the fix is in `tasks/README.md`'s recovery paragraph and
`embarch-fleet/ops.md` §3's table, both reserved (`protocol.md` §3).

## What

`tasks/README.md` says recovery checks each branch: **"no commits means back to
`open`; commits mean `blocked` with the branch named, so a second worker does not
redo salvageable work."** A worker commits at the *end* of its task. Everything
between dispatch and that commit lives only in its worktree's working tree, so a
killed worker is the case where the predicate is least informative — and it reads
as "nothing was done".

That happened. Leg 009 was cancelled, `tasks/ui/002` was reclaimed to `open` on the
grounds that its branch held only the claim commit and was an ancestor of `main`,
and the handover recorded that its worker had never started. It had:
`.worktrees/embarch-ui/002-.../src/trace.rs` held **306 uncommitted insertions**
that build clean, pass 97 tests and clippy, and cover three of the task's four code
`Done when` boxes. The branch tip was identical to `main`, exactly as the rule
expects of work that never happened.

Nothing was lost, but only because the worktree removal that the same tidy-up was
supposed to do had not run either. **Two defects cancelled out.**

## Why it matters

The dangerous combination is the rule working as written: reclaim the task to
`open` *and* delete the worktree with no commits. Then a leg re-dispatches a task
whose work exists nowhere, and nobody ever learns it was done once.

## Candidate fix

Make the predicate `git status --porcelain` in the worktree, not `rev-list` on the
branch — **a dirty worktree is salvageable work whatever the branch says.** The
three outcomes then are: clean tree and no commits → `open`, delete the worktree;
anything else → `blocked`, name the branch *and the worktree path*, delete nothing.
`ops.md` §3's table and `tasks/README.md`'s recovery paragraph both state the
current rule and both need it.

Worth deciding at the same time: whether a killed worker's tree should be committed
to its branch by the recovering supervisor rather than left dirty, so that "delete
dead worktrees" stays a safe unconditional step.

## Done when

- [ ] Recovery's reclaim predicate reads the worktree's state, not only its branch's
      commit count, in `tasks/README.md` and `ops.md` §3.
- [ ] The `blocked` note a reclaim writes names the worktree path, not just the branch.
- [ ] Whether the recovering supervisor commits a killed worker's tree is decided
      either way and written down.
