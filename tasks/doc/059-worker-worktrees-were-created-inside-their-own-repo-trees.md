# 059 — Worker worktrees were created inside their own repo trees, not outside them

**State:** open
**Source:** `core/061`'s worker, 2026-09-13, as an `inbox/` drop; filed here by leg 114 in the same
leg that caused it. The body below is the worker's own text, unaltered, plus the supervisor's answer
to its last `Done when` box — see **What actually happened** at the end.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `.claude/leg.md` and/or `embarch-fleet/scripts/`, both reserved
to the owner by `../../embarch-fleet/protocol.md` §2. No agent may write either.

## What

This unit's two worktrees were dispatched at:

- `/home/gabriel/Github/embarch/embarch-core/.worktrees/embarch-core/061-power-tap-says-so-in-stream-index`
- `/home/gabriel/Github/embarch/embarch-doc/.worktrees/embarch-doc/061-power-tap-says-so-in-stream-index`

— i.e. **inside** the `embarch-core` and `embarch-doc` repo trees themselves (`<repo>/.worktrees/<repo>/<slug>`),
confirmed via `git worktree list` in both repos. `../../embarch-fleet/protocol.md` §5 requires both
worktrees to live under `embarch/.worktrees/<repo>/<NNN-slug>/`, **outside every repo tree** — and
names the exact failure mode this risks: `embarch-study-designer` decision 57 records a repo checked
out inside itself making a naive scan find six GATT service blocks instead of three.

The task's own dispatch message additionally named a *third*, different path
(`/home/gabriel/Github/embarch/.worktrees/embarch-core/061-...` and the `embarch-doc` equivalent),
which does not exist at all — only the two nested paths above do, per `git worktree list`. So there
are (at least) two disagreeing ideas of where this unit's worktrees should be, and the one that was
actually created is the one the protocol says not to use.

**Consequence for the sibling path-dep symlinks**: `embarch-core`'s `Cargo.toml` path-deps on
`embarch-study-designer` and `embarch-topology` need those two repos symlinked one level above the
worktree. That staging had been done correctly, but at the "outside" location
(`/home/gabriel/Github/embarch/.worktrees/embarch-core/` — a plain directory of symlinks, not a
worktree), which sits beside nothing, because the actual worktree is nested one level *inside*
`embarch-core` instead. `cargo build` failed on arrival with "unable to update
`embarch-study-designer`" until this worker added matching symlinks beside its own (wrongly-placed)
worktree. Both worktrees were otherwise clean on arrival — no other worker's dirt, correct branches
checked out — so this was worked around rather than stopped on.

## Why now

A worker cannot fix its own dispatch — this is the supervisor/listener's worktree-creation step,
which is `embarch-fleet/scripts/` and out of any worker's ownership row. Left unfixed, every unit
this leg or a future one dispatches this way both risks decision 57's scan bug and silently costs
a `cargo build` failure the worker has to route around by hand (or, if the worker does not think to
create the symlinks, a false-red gate that looks like a code problem and isn't).

## Done when

- [ ] The worktree-creation step (wherever in `embarch-fleet/scripts/` it lives) is confirmed to
      place both worktrees at `embarch/.worktrees/<repo>/<NNN-slug>/`, outside every repo tree, and
      whatever produced the nested path for `core/061`/`061`'s doc pair is fixed or explained.
- [ ] The sibling path-dep symlink step is confirmed to run against wherever the worktree actually
      ends up, not a fixed "outside" location assumed to be beside it.
- [x] Say whether `core/061`'s nesting was a one-off (e.g. a stale script version at dispatch time)
      or reflects the current state of `embarch-fleet/scripts/` — if the latter, every leg since is
      affected. **Answered below.**

## What actually happened — leg 114's own answer, 2026-09-14

**No script created these. The supervisor did, by hand, and the cause is one flag.** Leg 114
dispatched all four of its units with

```
git -C embarch-<repo> worktree add -q -b <branch> .worktrees/embarch-<repo>/<slug> origin/main
```

run from `/home/gabriel/Github/embarch`. **`git -C <dir>` changes directory before doing anything**,
so the *relative* worktree path resolved against the repo's own root rather than against the suite
root, and every one of the eight worktrees landed at `<repo>/.worktrees/<repo>/<slug>` — inside the
repo. The symlinks in the same script were written with **absolute** paths, so they went to the
correct outside location, beside nothing. That is exactly the split the worker observed.

So: **not a one-off caused by a stale script, and not a defect in `embarch-fleet/scripts/` either.**
It is a hazard in the hand-written dispatch that `.claude/leg.md` describes in prose, which spells
the worktree path relative (`embarch/.worktrees/<repo>/<NNN-slug>/`) and leaves `git -C` to the
supervisor. Two things are worth the owner's judgement, and neither is an agent's to write:

1. Whether `.claude/leg.md`'s dispatch section should require **absolute** worktree paths, the way
   its own leg-worktree recipe already does.
2. Whether `scripts/check-dispatch.py` should verify where the worktrees *are* rather than only that
   the intended paths are free — it passed here, checking eight paths that were never created, while
   eight others were. That is `tasks/doc/046` exactly, now with a second instance behind it.

Leg 114 removed all eight nested worktrees as it landed each unit, so nothing is left inside a repo
tree; `git worktree list` in all five repos is clean.
