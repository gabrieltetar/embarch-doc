# 061 — A cherry-picked doc branch can never be retired by the fold's `git cherry` check

**State:** open
**Source:** leg 115's step 0, 2026-09-14. Observed directly on `origin/main`, not inferred: three
`agent/*` branches were still on `embarch-doc`'s remote at the top of the leg, and two of them can
never be deleted by the mechanism that is supposed to delete them.
**Scope:** doc
**Hardware:** none — a script change and a policy question. No board, no probe, no live Core.
**Owner:** required — the fix is in `scripts/fold-commit.py`, which `check-ownership.py` reserves
to the owner from both a worker and a supervisor. (Value deliberately unbolded: leg 115 first wrote
`**required**` here and `queue-status.py` counted the task as dispatchable, which is exactly
`tasks/doc/039`'s defect, hit by the leg that had just read the queue listing it.)

## What

`.claude/leg.md` says the supervisor does **not** delete a worker's pushed branches: `fold-commit.py`
does it, a fold behind, and only once `git cherry` proves them already on `origin/main`. That is the
right shape — before the push, the remote branch is the remote's only copy of a unit — but
**`git cherry` is patch-id equality, and a cherry-pick that conflicted does not preserve the patch
id.** So the branches that most need retiring are exactly the ones it can never retire.

Measured on `embarch-doc` at leg 115's step 0, `git cherry origin/main <branch>`:

```
-  e4e9f3e  agent/outpost/022-citation-sweep-non-c-sources-doc     (on main; will be retired)
+  caee440  agent/api/096-deferred-source-flag-client-half-doc     (on main; NEVER retired)
+  dda7d6c  agent/core/052-readme-bind-and-stale-claims            (on main; NEVER retired)
```

The `-` branch is an ordinary clean cherry-pick, one fold behind its deletion. The two `+` branches
are landed work — their content is on `main` and was verified there, by diffing each branch against
`origin/main` and finding only files where the *branch* is behind — but `git cherry` reports them as
unmerged and always will. `core/052` has been stranded since **2026-09-13**, a full day and roughly
thirty units.

`api/096`'s own log entry records why its patch id changed: *"`--ff-only` refused because two folds
had already moved `main`, and the cherry-pick **conflicted** on the task file — resolved to the
worker's version."* A conflict resolution is a different patch by construction.

## Why it matters, and why it is small

**It is not data loss.** Both branches' content is on `main`; nothing is at risk and no revert
handle is lost, because the log records the *merge* SHA and not the branch. The cost is a slow leak:
every unit whose doc half needs a conflicted cherry-pick — which is the common case in a busy leg,
since two folds routinely move `main` under a twenty-minute worker — leaves one permanent `agent/*`
branch on the remote.

**The cost lands on step 0, not on storage.** A leg's recovery scans `agent/*` branches to decide
whether a worker died holding finished work, and `.claude/leg.md` makes that scan load-bearing:
*"a branch present on its remote carrying commits means that worker finished — you may gate and land
it."* Under that rule a stranded branch is a **false positive for finished work**, and the
asymmetry the rule leans on ("presence may retire a worker, absence never may") is precisely what
makes a false presence expensive. Leg 115 spent four tool calls establishing that these three were
already landed rather than three units owed.

## Done when

- [ ] `fold-commit.py`'s deletion check recognises a branch whose content is on `main` by a means
      that survives a conflicted cherry-pick — candidates, in the owner's judgement: an empty
      `git diff origin/main <branch> -- <the paths the fold staged>`, or the fold recording the
      branch name beside the merge SHA it produced and retiring by name.
- [ ] The two currently stranded branches are deleted, or a deliberate decision is recorded that
      stranded branches are acceptable and step 0's scan must tolerate them.
- [ ] If the answer is the second, `.claude/leg.md`'s "a pushed branch is a presence, and it can
      only have been produced by a worker that reached its own bookkeeping" is amended — it is that
      sentence this defect falsifies.

## Watch for

- **Do not have a leg delete these by hand.** `.claude/leg.md` forbids it for a real reason: before
  the push, the remote branch is the remote's only copy of that unit, and a supervisor that has
  learned to tidy branches is one that will eventually tidy one that has not landed.
- **`git cherry`'s `-` answer is still trustworthy** — it has no false negatives here, only false
  positives. Whatever replaces it should keep that direction.
