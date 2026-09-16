# 066 — every unit leaks its local branches into the owner's checkout, and 112 have accumulated

**State:** open
**Source:** `inbox/doc-every-unit-leaks-two-local-branches-forever.md`, filed by leg 119 during
end-of-leg cleanup, drained by leg 120. Not reported by any agent — found by looking at `git branch`
in the owner's checkout; the numbers below are `git branch` output, not an impression.
**Scope:** doc
**Hardware:** none — a branch-hygiene gap in the leg procedure. No board, no probe, no live Core.
**Owner:** required — the fix belongs in `.claude/leg.md` (generated from
`embarch-fleet/scripts/install.py`) or in `scripts/fold-commit.py`, both owner-reserved.

## What

A supervisor creates each unit's branches with `git worktree add -b <branch> ...` in the **owner's
checkout**, because that is the repo the worktree is registered against. At the end of the unit it
runs `git worktree remove`, which deletes the working tree **and leaves the branch ref behind**.

`fold-commit.py` prunes the *remote* branch once `git cherry` proves it landed — correctly, four
times in leg 119. **Nothing anywhere deletes the local one.** Measured in
`/home/gabriel/Github/embarch/embarch-doc` right after that leg's cleanup:

```
local agent/* branches:                    112
  provably merged into origin/main:         75
  not an ancestor of origin/main:           37
```

Two units per leg, two repos each, every leg since the fleet started. `git branch` in that checkout
is now 112 lines of dead refs and is effectively unusable for its actual purpose.

## The 37 are a second, separate fact, and the more interesting one

They are not unlanded work — spot-checked, they are units whose log entries record a clean merge.
They fail an ancestry test because the branch was **rebased or cherry-picked somewhere other than the
ref that survives**, so the surviving local ref points at a pre-rebase commit that is not an ancestor
of `main`. That is the same root cause `tasks/doc/061` records for the fold's `git cherry` check
being unable to retire a cherry-picked doc branch — **arriving here from the local side instead of
the remote.** Whatever is decided there probably decides this too; read them together.

**A trap for whoever measures this:** `git branch --merged main` in the owner's checkout answers
against **his local `main`, which a leg never advances** — it was 113 commits behind `origin/main`
when leg 119 ran it (`fdaf9bb` vs `d88fe22`), and reported 41 unmerged rather than 37, including all
four branches that leg had just landed. Use `--merged origin/main`, after a fetch, or the number is
fiction.

## Why now

Nothing is broken and nothing is at risk — these are refs, they cost bytes, and every one of the 75
is provably redundant. Worth fixing anyway for two reasons:

1. **`git branch` is a recovery tool.** `ops.md` §3's recovery reads branch and worktree state to
   decide what a killed leg left behind. A supervisor doing that today reads 112 lines of which at
   most a couple are live — the "documentation shaped like the data it documents" problem that cost
   batch 001 its recovery greps.
2. **It grows at a fixed rate** — two per unit, four units per leg, legs end every twenty minutes.

## Where it should go

- **Cheapest:** have the supervisor delete the local branch when it removes the worktree, same step.
  `git worktree remove <path> && git branch -d <branch>` — prefer `-d` over `-D` and let a refusal be
  a real signal, which is what the 37 would produce today.
- **More durable:** `fold-commit.py` already proves a branch landed before pruning its remote. If
  that proof holds, prune the local ref in the same breath; branches it cannot prove stay, turning
  the 37 into a visible, shrinking list of things to explain rather than an invisible pile.
- **Either way, decide what to do with the 37 that exist now.** They are not a queue; they are
  archaeology. A one-time sweep of the 75 provable ones plus a decision on the rest may be the job.

## Watch for

- **Do not mass-delete with `-D` on the strength of these numbers.** They were true at `d88fe22` on
  2026-09-16 and a live fleet moves `main` every few minutes. Re-measure against a fresh
  `origin/main` first.
- **This is the owner's own checkout.** Under the live-fleet editing discipline, a sweep of it wants
  to happen at a leg boundary, not while a leg holds worktrees registered there.
- **`embarch-doc` is not the only repo affected** — every code repo the fleet branches in has the
  same pile, smaller. Count them before deciding the shape of the fix.

## Done when

- [ ] The leg procedure or the fold deletes a unit's local branches, or a decision is recorded that
      it deliberately should not.
- [ ] The existing accumulation is either swept or explicitly left, with the count recorded.
- [ ] Read against `tasks/doc/061`, which is the same root cause from the remote side.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
