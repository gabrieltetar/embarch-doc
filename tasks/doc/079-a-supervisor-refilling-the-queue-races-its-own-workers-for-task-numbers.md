# 079 — A supervisor refilling the queue races its own workers for task numbers

**State:** open
**Filed by:** leg 138, 2026-09-17, at `core/080`'s fold — **the second occurrence in two legs**, which
is the condition leg 137's own log entry named for filing it: *"the structural fact is that a
supervisor refilling the queue mid-leg races its own workers for numbers, and nothing warns either
side. Worth a `tasks/doc/` entry if it happens again."*
**Source:** `supervisor-log.md`, `core/077`'s entry (leg 137, 2026-09-17 13:59) and `core/080`'s
entry (leg 138).
**Scope:** doc
**Hardware:** none
**Owner:** required — every plausible fix lives in `scripts/` or `.claude/`, both owner-reserved.
An agent can describe this; it cannot fix it.

## What

`scripts/check-task-numbers.py --next <scope>` answers "next free number" from the checkout it is
run in. A worker runs it in its own worktree, branched from `main` at dispatch. The supervisor runs
it in the leg worktree, which moves as the leg commits. Between a dispatch and that worker's push,
**both actors can legitimately get the same answer**, because neither view is wrong — they are
simply different commits.

Two instances, one leg apart, both `core`, both caught only at the fold:

- **Leg 137, `core/077`.** Worker filed `tasks/core/078-compact-core.md`; the supervisor's refill
  sweep had already taken `078`. Renumbered by hand to `079`.
- **Leg 138, `core/080`.** Worker filed `tasks/core/081-compact-core.md`; the supervisor's refill
  sweep had already taken `081`. Renumbered by hand to `082`.

Both were real, non-duplicate tasks. Both cost the supervisor a hand-edit of another actor's file,
and the second cost more than the first: `check-task-numbers.py` reads **the branch's own history**,
not only its working tree, so a create-as-`081`-then-rename-to-`082` still reported `081` as
*reissued* once merged, and the fold was red until the supervisor squashed the worker's two commits
into one. That is a supervisor rewriting a worker's commit history to satisfy a check, which is
worth avoiding on its own terms.

**The current backstop works and is not the problem.** `check-task-numbers.py` refuses the merge, so
this is always a blocked fold rather than a silent corruption — that is why neither instance did any
harm. The cost is per-occurrence supervisor hand-work, twice in two legs, and it will keep
recurring exactly as often as a leg refills while a worker is in flight, which `.claude/leg.md`'s
low-water-mark rule makes *more* likely, not less.

**Three shapes a fix could take, none of them decided here:**

1. **Make the number late-bound.** A worker filing a debt writes a placeholder (or no number) and
   the supervisor assigns at the fold, which is the only moment one actor sees both sides. Cheapest
   to reason about; changes what a worker writes.
2. **Make the answer race-free.** `--next` could consult `origin/main` rather than the local
   checkout, and a worker could be told to fetch before allocating. Narrows the window; does not
   close it, since two workers can still race each other.
3. **Reserve a range per actor.** Workers allocate downward from a high block, or from a
   scope-and-actor-specific stripe, so the two allocators can never collide. Closes it completely;
   costs the property that numbers are monotonic and readable in filing order.

## Why now

Twice in two legs, with an explicit "file it if it happens again" left in the log by the leg that
hit it first. It is also cheap to get wrong in a worse way later: the fix touches the one mechanism
that keeps two actors from silently overwriting each other's queue entries.

## Done when

- [ ] The owner has picked one of the three shapes above, or a fourth, and it is recorded where the
      claim/filing protocol lives (`tasks/README.md` for what an actor writes,
      `embarch-fleet/protocol.md` §5 or `.claude/leg.md` for who assigns and when).
- [ ] If the fix is mechanical, `scripts/check-task-numbers.py` and whatever a worker is told to run
      agree about which view of `main` is authoritative.
- [ ] Either instance's hand-renumber is no longer necessary for the next occurrence, or the
      decision explicitly accepts the hand-renumber as the cost and says so, so this does not get
      re-filed a third time.
