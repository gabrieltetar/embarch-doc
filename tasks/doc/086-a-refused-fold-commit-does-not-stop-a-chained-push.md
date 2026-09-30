# doc — A refused `fold-commit.py` does not stop the push chained behind it, and two legs in a row pushed a worker commit before its fold

**State:** open
**Filed by:** the supervisor leg that ran `study-designer/032`, `core/046`, `api/111` and
`umbrella/089` on 2026-09-28, from its own `core/046` fold.
**Source:** `supervisor-log.md`'s `dev-bench/014` entry (2026-09-28 16:48) and `core/046` entry
(2026-09-28 17:52) — the same slip, logged by two consecutive legs.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/fold-commit.py` or `.claude/leg.md`, both
owner-reserved.

## What

Both legs ran the fold as one chained command,
`python3 scripts/fold-commit.py ... | tail -N && git push origin HEAD:main && ... fleet-tick.py leg-fold`.
`fold-commit.py` refused correctly both times (a stale `old_string` once; an entry not yet written
the second time) and committed nothing. But the pipe into `tail` replaced its exit status with
`tail`'s, so the `&&` chain continued: the leg worktree's HEAD — the worker's merged doc commit, its
`changelog.d` fragment still pending — was pushed to `origin/main` minutes before its fold, and a
`leg-fold` tick was recorded for a fold that had not happened.

Harmless both times (a worker commit with a pending fragment is a legal state on `main`), but the
tick log now carries two false fold markers, and the shape is one where a different refusal — say,
one on a denylisted name in the log — would push anyway.

## Candidate fixes, not chosen here

- `fold-commit.py` does the instance push and the log push itself, on success only, so there is no
  chained push to get wrong.
- `.claude/leg.md` names the shape outright: never pipe `fold-commit.py`, and never chain the push
  behind it.
- `fleet-tick.py leg-fold` refuses unless the newest instance commit is a fold commit.

## Done when

- [ ] A refused fold cannot be followed by a push or a `leg-fold` tick from the same command, by
      construction or by a rule a leg reads.
