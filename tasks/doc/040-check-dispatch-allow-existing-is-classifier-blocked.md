# 040 — `check-dispatch.py --allow-existing` is classifier-blocked, so the recovery path the guard names cannot be taken

**State:** done — the flag is deleted, not re-permitted; the refusal and `.claude/leg.md` name a recovery that needs no flag (commit, push, remove, re-dispatch onto the branch) (fleet `1aca63e`, owner/dispatch); lands by `deploy.py`
**Source:** leg 074, 2026-09-10, hit live while dispatching `core/036` and `api/042`.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/check-dispatch.py` or in a permission rule under
`.claude/`, both of which `../../embarch-fleet/protocol.md` §2 reserves to the owner.

## What

`scripts/check-dispatch.py` refuses when a unit's worktrees already exist, and its own refusal text
tells the supervisor what to do about it: settle worker liveness by the process tree, recover per
`ops.md` §3, **"and re-run with `--allow-existing`."**

That re-run cannot happen. `--allow-existing` is refused by the Claude Code auto-mode classifier
before the script runs:

```
Permission for this action was denied by the Claude Code auto mode classifier.
```

The plain invocation — no flag — is permitted and runs normally. So the guard is reachable and its
documented escape hatch is not.

## Why it matters

**The flag is the guard's only recovery path, and a supervisor that needs it is by definition in
recovery.** The refusal fires exactly when a killed leg left worktrees behind. Under `ops.md` §3
that is a normal state, not an incident — closing VS Code is the owner's kill switch and is meant
to be used. A leg that recovers such a worktree correctly, reclaims the claim, and then cannot get
the guard to acknowledge it has two options and both are bad: proceed with the interlock
unverified, or abandon the unit.

**It also punishes an ordering mistake far harder than the mistake deserves.** This leg created its
four worktrees before running the guard rather than after — the wrong order, and mine to get right.
But the interlock's actual safety property still held by construction: `git worktree add` refuses a
path that already exists, all four succeeded, `git ls-remote --heads origin 'agent/*'` was empty in
every repo, and no task file read `claimed`. The evidence the guard exists to collect was collected;
there was simply no way left to make the script say so.

**This is the second classifier-blocked flag recorded in this suite**, after `deploy.py --force`.
That one is blocked *by design* and the block is the point. This one is not: nothing about
`--allow-existing` is destructive — it suppresses a refusal in a read-only check that creates
nothing, writes nothing and touches no git state.

## Done when

- [x] A supervisor can complete the recovery path `check-dispatch.py`'s own refusal text names,
      either because a permission rule permits the flag or because the flag is replaced by
      something a rule can match. **Neither: the path no longer needs a flag.** Recovery is the
      commands a leg already runs — commit the tree to its branch, push, `git worktree remove`,
      re-run the plain check (it passes once the paths are gone), and for a resume `worktree add
      <path> <branch>` without `-b`, then `--created` (`tasks/doc/046`). Walked end to end in a
      scratch suite: a dirty "dead worker" tree is refused, then passes after those steps, and the
      resumed tree carries the WIP commit. A permission rule for the flag was not written: that is
      a route around the classifier, and the flag had no case it was needed for.
- [x] If the answer is that the flag should stay unreachable, `check-dispatch.py`'s refusal text
      stops recommending it and says what to do instead — a guard that names an impossible remedy
      is worse than one that names none. Deleted outright, with `--settle` and the two-sample
      activity test only it reached; the refusal says the route above, plus leg 074's own case
      (worktrees made before the guard ran: clean, so remove, check, create again).
- [x] Worth deciding alongside: whether the guard should accept the evidence directly, since
      "`git worktree add` succeeded for every path in this unit" is a strictly stronger statement
      than "these paths did not exist a moment ago" and is produced for free by the dispatch itself.
      **It does, as `--created`, and as a second run rather than a replacement.** A leg that skips
      creation and reuses a live worker's trees — leg 012 — passes any check of what exists, so
      only the pre-check refuses it; `--created` then proves the creation went where it was asked.
