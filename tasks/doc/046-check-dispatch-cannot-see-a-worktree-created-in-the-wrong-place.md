# 046 — `check-dispatch.py` proves a worktree is absent and nothing proves it was then created *there*

**State:** done — both: `check-dispatch.py --created` is the post-condition, and `.claude/leg.md` carries the absolute `worktree add` and brackets it with the two runs (fleet `a78e4e0`, with `5a95406` from `tasks/doc/059`; owner/dispatch); lands by `deploy.py`
**Source:** leg 095, 2026-09-12, first hand. All four of its units were dispatched to workers whose
worktrees did not exist; all four workers correctly refused and stopped without touching anything,
costing ~4 minutes and four spawns.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/` and/or `.claude/leg.md`, both reserved.

## What

The supervisor's worktree-creation step has a silent failure mode and there is no check between it
and `Dispatch`.

The command that did it:

```sh
git -C embarch-core worktree add -q -b agent/core/045-route-sweep-reach \
    .worktrees/embarch-core/045-route-sweep-reach origin/main
```

`git -C <repo>` changes the working directory for the whole invocation, so the **relative** target
path resolves against the repo, not against the suite root. The worktree was created at
`embarch-core/.worktrees/embarch-core/045-route-sweep-reach` — inside the repo it was cut from —
and `git worktree add` exited **0**. The sibling path-dep symlinks in the same script were made with
a plain `ln` from the suite root, so they landed correctly, which makes the parent directory *look*
right in an `ls`.

What makes this worth a task rather than a note: **`scripts/check-dispatch.py` ran immediately
before, on the intended paths, and passed — correctly.** Its contract is "none of these exist, safe
to dispatch", and that was true both before creation and after, because creation put them somewhere
else. The guard that exists is a pre-condition; there is no post-condition. The first thing that
noticed was the worker, twenty seconds into its own run.

## Why now

`.claude/leg.md` spells out the `--detach`, the `-T` on the fleet symlink, the sibling-link closure
table and the `check-dispatch.py` guard — every part of worktree setup that has bitten a leg before
— and gives no literal command for the per-unit worker worktrees, which is the one a leg writes
fresh every time. Two of the three documented footguns in that section are about a path resolving
one level away from where it was written (`ln -sfn` descending into a tracked directory, `-T`); this
is the third instance of the same class and the only one still unguarded.

It is also cheap to make impossible: the paths are already enumerated for `check-dispatch.py`, so
the same list re-run after creation answers it.

## Done when

- [x] `check-dispatch.py` grows a post-condition mode (a `--created` / `--verify` inversion: every named
  path exists, is a registered worktree of the expected repo, and is on the expected branch), **or**
  `.claude/leg.md` carries the literal creation command with absolute target paths, or both.
  **Both.** `--created` checks those three, plus that each path sits at
  `<worktree_root>/<repo>/<slug>` and that the unit's worktrees share one `agent/<scope>/<slug>`
  branch, and it resolves every relative Cargo path-dep from the worktree as cargo would — the check
  `tasks/doc/037` asked for in place of a generated link table. A path that is missing is reported
  with where the repo actually registered a worktree of that name.
- [x] If it is the script: a leg that skips the verification is no worse off than today, and a leg that
  runs it cannot dispatch into a path that was never created. Opt-in; exit 1 on any miss. Both modes
  now also refuse a relative `--worktree`, which is how a check passes on paths never created.
- [x] The `git -C` + relative-path interaction is named explicitly wherever the fix lands, because the
  exit code is 0 and the directory listing of the intended parent looks plausible. In leg.md beside
  the command, in the script's docstring, and in the refusal text itself.
