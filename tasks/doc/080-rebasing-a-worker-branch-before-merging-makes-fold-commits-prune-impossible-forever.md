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
