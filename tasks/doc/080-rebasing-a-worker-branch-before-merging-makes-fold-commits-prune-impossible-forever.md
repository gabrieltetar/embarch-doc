# 080 — Rebasing a worker branch before merging makes `fold-commit.py`'s prune impossible forever

**State:** open
**Filed by:** leg 138, 2026-09-17, at the end of the leg, after hitting it twice in one leg and
finding three older instances already sitting on the remote.
**Source:** `.claude/leg.md` — *"You do not delete the pushed branches — `fold-commit.py` does it,
and only once `git cherry` proves them already on `origin/main`."*
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/fold-commit.py` or in `.claude/leg.md`'s wording, both
owner-reserved.

## What

`fold-commit.py` prunes a landed worker branch only when `git cherry` proves its commits are on
`origin/main`. **A supervisor that rebases a worker's branch before merging defeats that
permanently**, because the rebase gives every commit a new SHA and the remote still points at the
old one. `git cherry` compares patch-ids, so it *should* cope — but it did not here, and the
observed behaviour is that the branch is never pruned by any subsequent fold either. The branch then
sits on the remote forever with commits on it.

**Rebasing is not an unusual thing for a supervisor to do; it is the normal thing.** A leg lands
several units, `main` moves under each subsequent worker, and `.claude/leg.md` says in as many words
to *"rebase the remaining branches after each merge"*. So every unit after a leg's first is a
candidate for this.

**Observed, 2026-09-17, leg 138.** Three branches were rebased before merging. One
(`agent/core/080-…-doc`) was **force-pushed** after the rebase, and `fold-commit.py` pruned it
normally. Two (`agent/api/110-not-attached-advice-doc` at `f34c78b`,
`agent/ui/065-consume-core-spans-doc` at `3feedc2`) were merged from the local rebased branch
without force-pushing, and neither was pruned — by their own fold or by the one after it. The leg
verified both branches' content was fully on `origin/main` (the only diffs were the changelog
fragments its own folds had consumed) and **deleted both by hand**, which is a deviation from the
rule above and is recorded in that leg's final report.

**Three older instances were already on the remote when leg 138 started**, and are still there:
`agent/api/096-deferred-source-flag-client-half-doc`, `agent/core/052-readme-bind-and-stale-claims`,
`agent/ui/059-diff-new-lines-republish`. Nobody filed them, which is the tell that this has been
happening quietly for a while.

**Leg 139, 2026-09-17 — the force-push remedy was applied to all three units and it is NOT
sufficient.** That leg rebased and **force-pushed every branch before merging**, which is what this
task's own `Done when` proposes. Results, three units, six branches:

| unit | code branch | doc branch |
|---|---|---|
| `umbrella/080` | pruned (no-op branch, identical to `main`) | **pruned** |
| `core/085` | pruned | **NOT pruned** |
| `api/109` | **NOT pruned** | **NOT pruned** |

**`core/085`'s doc branch is the counter-example and it is a clean one.** After the fold, with the
branch still on the remote at `2e7195f0`: `git cherry origin/main origin/agent/core/085-widen-spans-gap`
printed **nothing** (every commit already on `main` by patch-id), and
`git merge-base --is-ancestor 2e7195f0 HEAD` answered **yes** (the tip is literally an ancestor of
`main`, not merely equivalent). So the branch met the stated prune condition by both the test
`fold-commit.py` uses and the stronger one, and was still left behind — **while the same fold pruned
`embarch-core`'s branch in the same run**, and the previous fold pruned `umbrella/080`'s doc branch
under the same procedure.

**That narrows the defect considerably and moves it off the rebase.** It is not "a rebased branch
can never be pruned": a rebased, force-pushed doc branch *was* pruned one unit earlier. Whatever the
real condition is, it distinguishes two folds that look identical from the outside. **The most
likely candidate, and the one to check first: `fold-commit.py` evaluates the prune against
`origin/main` as it stands at fold time, and the supervisor pushes `main` only *after* the fold
commit** — so a branch whose commits reached `origin/main` only via that same push is invisible to
the check that ran a moment earlier. If that is it, the fix is ordering (or a re-check after the
push), not patch-ids, and the `Done when` below is aiming at the wrong half.

**`api/109`'s two have a different and fully understood cause, and they are not evidence about
rebasing at all:** that unit's fold was **hand-committed**, because `fold-commit.py` failed settling
its instance paths (`tasks/doc/082`). The prune is a step *inside* `fold-commit.py`, so it simply
never ran. Both tips are ancestors of their `main` — verified with `git merge-base --is-ancestor` —
so both are safe to prune whenever something does.

**The two defects compound, and that is the part worth carrying forward.** `tasks/doc/082` makes a
fold finish outside `fold-commit.py`; every fold that finishes outside it silently skips the prune;
and `.claude/leg.md` forbids a leg from deleting the branch by hand. So each occurrence of `082`
manufactures a permanent false presence of the kind this task's own "Why it matters" paragraph
describes — and the liveness rule tells a future leg that a branch with commits is a finished worker
to land.

**Left on the remote by leg 139 rather than deleted by hand**, per `.claude/leg.md`'s rule, so the
evidence is still there to inspect. Three from this leg, all verified landed:
`agent/core/085-widen-spans-gap` (`embarch-doc`), `agent/api/109-build-dir-name` (`embarch-doc` and
`embarch-api`). That brings the remote's standing total to **six**, counting the three older ones
above.

**Why it matters beyond tidiness.** `.claude/leg.md`'s own liveness rule says *"a branch present on
its remote carrying commits means that worker finished — you may gate and land it"*, and calls that
asymmetry load-bearing: presence may retire a worker, absence never may. **A permanently unpruned
branch is a false presence.** A future leg that checks `git ls-remote --heads origin 'agent/*'`
while waiting on a worker sees five branches with commits that no worker is behind, and the rule
tells it to land them.

## Why now

Twice in one leg, three older instances found sitting there, and the failure mode interacts with the
one signal a leg is allowed to use to decide a worker has finished.

## Done when

- [ ] Either `fold-commit.py` prunes a branch whose *content* is on `origin/main` regardless of SHA
      (patch-id or tree comparison), or `.claude/leg.md` says explicitly that a supervisor
      force-pushes a branch it rebased, before merging it — which is what the one pruned branch of
      the three actually did.
- [ ] The rule's current wording is reconciled either way: a leg cannot both be forbidden from
      deleting a pushed branch and be the only actor able to clean one up.
- [ ] The five stale branches named above are gone, or a decision records why they stay.
