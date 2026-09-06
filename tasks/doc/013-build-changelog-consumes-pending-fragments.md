# 013 — `build_changelog.py` consumes the owner's pending fragments into the fold that runs it

**State:** open
**Source:** leg 016's supervisor, 2026-09-06, folding `umbrella/019`. Dropped in `inbox/` as
`build-changelog-consumes-the-owners-pending-fragments.md` and drained here by leg 017.
**Scope:** doc
**Hardware:** none — re-checked at drain, `scripts/` only.
**Owner:** required — every remedy below is `scripts/`, and remedy 3 is
`../../embarch-fleet/ops.md`. Both reserved, so no worker may be sent at it.

## What

`main` carries **15 `changelog.d/` fragments the owner wrote and has not folded** — twelve
`fleet-*`, one `doc-*`, one `suite-*`, two `umbrella-*`. They are tracked and committed
(`de07c82`, 2026-09-05 20:37), so **every leg worktree has them.**

`python3 scripts/build_changelog.py` is a step of every fold and it consumes **all** pending
fragments, not the folding unit's. Leg 016's first run printed:

```
  history/doc.md  += 1 entry
  history/fleet.md  += 11 entries
  history/suite.md  += 1 entry
  history/umbrella.md  += 3 entries

16 fragment(s) consumed into window 2026-09.
```

The unit being folded owned **one** of those sixteen. The two `umbrella-*` fragments the owner
wrote landed in the **same `## 2026-09` block** of `history/umbrella.md` as the unit's own
entry, so there is no way to stage the unit's entry without staging his.

## Why the existing rule does not catch it

`protocol.md` §9 and `supervise.md` both forbid `git add -A`, on exactly the legs 004/005
precedent of sweeping the owner's `changelog.d` fragments into a fold. **This is that outcome
reached without `git add -A`**: `fold-commit.py` stages by explicit path, the path list is
correct, and the file at that path has been rewritten by a script the fold is required to run.
A supervisor following every written rule lands it.

Two things make it silent rather than loud:

- **The gate stays green.** `build_changelog.py --check` validates fragment shape, not whether
  `history/` agrees with what is pending, so nothing fails before or after.
- **The blast radius is invisible in the fold's own diff review**, because the added lines are
  well-formed changelog entries in the right file — they read exactly like the unit's own.

## The workaround leg 016 used, which is not a fix

`git checkout -- changelog.d history`; move the 15 fragments to a scratch directory outside the
repo; re-run `build_changelog.py` (`1 fragment consumed`); move them back; confirm
`git status --porcelain` lists only the unit's two paths. It works and it is entirely manual,
so it is one forgotten step away from the bug on any leg.

Leg 015 reached the same end state — its `umbrella/018` fold shows `history/umbrella.md | 4 +`,
exactly one entry, with the owner's fragments already committed and present in its worktree —
but **nothing in `supervise.md` or `ops.md` tells a leg to do this**, so that was habit or luck,
not procedure. It should not depend on either.

## Three possible remedies, all `scripts/`

1. **`build_changelog.py --only <glob>` / `--unit <scope>/<NNN>`**, so a fold consumes exactly
   the fragments its unit wrote and leaves everything else pending. Narrowest change, and it
   makes the fold's path list and the assembler agree by construction.
2. **`fold-commit.py` refuses a fold whose staged `history/*.md` diff contains entries from
   fragments outside the unit.** Turns a silent sweep into a blocked commit — the shape this
   repo generally prefers, and the same shape as its existing refusal on a malformed log entry.
3. **Do nothing to the scripts and write the park-and-restore dance into `ops.md` §3.** Cheapest,
   and the weakest: it is a manual step whose omission is invisible.

Worth noting for whichever is chosen: the problem disappears the moment the owner folds his own
15 fragments, which makes it easy to close as "not reproducible" later. **The mechanism does not
disappear** — it returns whenever anyone leaves a fragment pending across a leg.

## Done when

- [x] A fold cannot consume a fragment the unit did not write, or is refused when it would.
      **Remedies 1 and 2 both, 2026-09-06.** `build_changelog.py --only GLOB` (repeatable);
      `fold-commit.py` refuses a fold that deleted a `changelog.d/` fragment outside its
      `--path` list. Verified both directions. Remedy 3 deliberately not taken — the task
      called it weakest, and leg 015 got it right by habit rather than by procedure.
- [x] The remedy is recorded where a supervisor reads it, not only in `scripts/`.
      `supervise.md` and `changelog.d/README.md`, in `embarch-fleet/templates/`.
- [ ] **Deployed.** `deploy.py` correctly refuses while a leg is live, so the instance's
      `supervise.md` still carries the old text. Run it at a leg boundary; that closes this.

**One thing found while fixing it, worth keeping.** `fold-commit.py` is a *shim* that execs the
framework copy at run time, while the assembler it names is instance-local and **frozen in a
leg's worktree at that leg's start commit**. So a new refusal in the shimmed script went live
for a leg holding an assembler too old to satisfy it — a refusal nobody could satisfy, which is
the failure `fold-day.py`'s header already records twice. The refusal now asks `--help` and
prints the park-and-restore dance where `--only` is absent. **Any future rule split across a
shimmed script and an instance-local one has this same asymmetry.**
