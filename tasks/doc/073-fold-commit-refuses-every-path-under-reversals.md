# 073 — `fold-commit.py` refuses every path under `reversals/`, so a suite unit that touches one cannot fold

**State:** open
**Source:** `suite/042` (leg 130, 2026-09-16). The unit added reversals row 110 and extended
`reversals/rows-93-109.md` to `rows-93-110.md`. `fold-commit.py` refused the fold with **5 path(s)
outside what a unit's fold may stage**, naming every `reversals/*.md` path including the rename's
both halves. The work landed as two commits instead of one (`b7f96ca` plus the fold).
**Scope:** doc
**Hardware:** none — a path-classification list in a Python script. Nothing is built, no board, no
probe, no live Core.
**Owner:** required — the fix is in `scripts/fold-commit.py` (or whatever list it shares), and
`scripts/` is owner-reserved. A supervisor that widened the allowlist guarding its own folds would
have no allowlist, so leg 130 filed this rather than fixing it.

## What

`scripts/fold-commit.py` validates every `--path` against a list of what a unit's fold may stage.
`reversals/` is not on it. The exact refusal:

```
5 path(s) outside what a unit's fold may stage:

  reversals/rows-93-109.md
  reversals/rows-93-110.md
  reversals/rows-1-50.md
  reversals/rows-51-72.md
  reversals/rows-73-92.md
```

`embarch-decision-reversals.md` itself **is** accepted. So the top-level index can be folded and the
range files holding the actual rows cannot — which is backwards, because the index is a four-row
table and the range files are where every row lives.

## Why this is the same defect twice

`reversals/` is a [DOC-COMPACTION.md](../../DOC-COMPACTION.md) split out of
`embarch-decision-reversals.md`. `.claude/leg.md` already warns, for `check-ownership.py`, that **a
doc that appears from a split carries its old file's rules and none of its old file's protection**,
and tells a leg to report an unclassified path rather than guess a classification. The same thing is
true of `fold-commit.py`'s staging list, and nothing said so — the first leg to write a range file
found out by being refused mid-fold, with the work already on disk and the task file already
`git rm`'d.

**The blast radius is small but the failure mode is bad:** a refusal arrives *after* a unit's edits
exist and its task has been retired, at the one moment a supervisor is most likely to reach for a
workaround. The script's refusal text does name the legal move (*"it is the owner's commit or a
separate one — not this fold"*), which is what made this recoverable.

## Done when

- [ ] `reversals/` is either added to `fold-commit.py`'s stageable list or deliberately excluded with
      a stated reason — **the choice is the owner's**, since it is the same question as whether a
      `suite` unit may fold a shared suite-level doc at all.
- [ ] If it is added, check whether any other DOC-COMPACTION split directory is in the same position
      (`reversals/` is the one leg 130 hit; `log-archive/` and any future split are worth a look).
- [ ] If it is excluded, say so somewhere a supervisor reads **before** it starts a `suite` unit —
      `tasks/README.md` or `.claude/leg.md` — so the next one plans two commits rather than
      discovering them.
- [ ] Consider whether the same list should be checked **up front**, when `--path` is parsed, rather
      than after the unit's edits are on disk. The script already settles paths before committing the
      log, which is what kept this cheap; the gap is that nothing warns earlier than that.

## Not yours

Do not change what a `suite` unit is allowed to write — `../../../embarch-fleet/protocol.md` §3 already
settles that, and it says the supervisor writes the shared suite-level docs. This is about which
paths one *commit* may carry, not about who may edit them.
