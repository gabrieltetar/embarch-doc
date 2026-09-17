# 082 — `fold-commit.py` cannot fold a unit whose own task file it must both modify and remove

**State:** open
**Filed by:** leg 139, 2026-09-17, after hitting it **twice in one leg** — `api/109` and
`suite/044` — and completing both folds by hand.
**Source:** `scripts/fold-commit.py`, observed directly.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/fold-commit.py`, or in `.claude/leg.md`'s instruction
about what belongs in `--path`. Both are owner-reserved. An agent can measure this; it cannot fix it.

## What

`fold-commit.py` `git rm`s a task file whose `**State:**` is `done`. That is correct and wanted.
But **a task file reaches `done` by being edited**, and if that edit is still unstaged when the fold
runs, `git rm` refuses:

```
git rm -q -- tasks/suite/044-....md failed in .../leg:
error: the following file has local modifications:
    tasks/suite/044-....md
(use --cached to keep the file, or -f to force removal)
```

**The fold then half-lands, by design, in the worse of the two orderings it was built to choose
between.** `fold-commit.py` commits the log first *on purpose*, so a kill leaves either "nothing" or
"an entry for a fold that did not happen", never "a fold nobody logged". Here the log commits, the
instance paths fail, and **a retry is refused** — *"supervisor-log.md has no uncommitted change, so
this unit's entry is either already committed or was never written"* — so there is no supported way
to finish the fold. Both times, leg 139 committed the instance half by hand with an explanatory
message. That works and it is a deviation from *"`fold-commit.py` … is the only way to land a fold"*.

**When it fires:**

- **Always, for a `suite` task**, because the supervisor executes those itself and marks the task
  `done` in the same working tree in the same breath. There is no worker and no branch to carry a
  staged edit in.
- **For an ordinary unit, whenever the supervisor touches the unit's own task file at fold time** —
  `api/109`'s case, where the file needed a reference corrected after a task-number collision
  (`tasks/doc/079`). Note the two defects compose: the number collision forced the edit, the edit
  blocked the fold.

**It does not fire** when the worker marked the task `done` on its branch and the supervisor merged
that, which is the common path — which is exactly why this has gone unnoticed.

## Workaround that works today, for whoever hits it before it is fixed

`git add` the task file yourself, leave it **out** of `--path`, and let the staged change ride along
— `fold-commit.py` stages by explicit path but commits what is staged. Leg 139 did not discover this
in time for either unit and hand-committed both; it is offered here untested so the next leg can try
it before reaching for a hand commit.

## Why now

Twice in one leg, in two structurally different ways, and the failure lands the fleet in the one
state `fold-commit.py`'s own ordering argument is written to avoid being unable to leave. A
supervisor that hand-commits a fold is a supervisor writing `main` outside the mechanism that checks
folds — which works exactly as long as the supervisor doing it is careful.

## Done when

- [ ] `fold-commit.py` either stages a `done` task file's modifications before removing it
      (`git rm --cached` plus the working-tree delete, or `git add` then `git rm -f`), or refuses
      **before** committing the log so a retry is possible.
- [ ] A fold that fails after the log commit has a supported way to finish — a `--log-already-written`
      path, or the retry refusal reworded to say what to do rather than only what happened.
- [ ] `.claude/leg.md` says whether a unit's own task file belongs in `--path` at all. Leg 139 put it
      in for two units and left it out for two, with no rule either way, and the two that included it
      are exactly the two that failed.
