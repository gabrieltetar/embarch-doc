# 016 — Two `embarch-outpost` docs file the CI question against `tasks/suite/021`, which has never existed

**State:** claimed — leg 076, worker on `agent/outpost/016-ci-citation`
**Source:** leg 076's refill sweep. `embarch-outpost/open.md:26` and
`embarch-outpost/decisions/testing.md:21` both hand the "outpost has no CI" question to
`tasks/suite/021`. `tasks/suite/` numbering runs 020 → 022; no 021 is on disk and none was ever
folded away from there.
**Scope:** outpost
**Hardware:** none

**Owner:** no

## What

Two documents in this sub-project say a question is filed somewhere it is not. Repoint or retire
both citations so the docs and the queue agree.

**Confirm the number was never issued before assuming it was deleted.** Run
`python3 scripts/check-task-numbers.py --next suite` and read what it says; a task that existed and
was completed is `git rm`'d, so absence from disk alone does not distinguish "never filed" from
"filed and finished". If it was never issued, the honest fix is for these two bullets to state the
question in their own words as an open one. **Do not file a `suite/021` yourself** — `suite/` tasks
are the supervisor's (`../../embarch-fleet/protocol.md` §8) and a worker writing one is out of
scope; if you conclude a suite-scoped task is genuinely owed, drop it in
`/home/gabriel/Github/embarch/embarch-doc/inbox/` by absolute path and say so.

**The CI job itself is out of scope for this task.** Adding a `.github/workflows` job that runs
`tests/run-all.sh` may well be right, but it is a separate change with its own evidence burden —
and note the standing debt that `embarch-outpost`'s Zephyr `tests/unit` suite cannot be built from
the fleet's environment at all (no `west`, no `ZEPHYR_BASE`), so no agent can currently prove such
a job green.

## Why now

Two independent documents agreeing on a wrong pointer reads as corroboration. Nothing catches it:
`check-links.py` checks file paths, not task numbers, and a task path that has never existed fails
no check anywhere.

## Done when

- [ ] Neither `embarch-outpost/open.md` nor `embarch-outpost/decisions/testing.md` cites
      `tasks/suite/021`, and each states the CI question in terms a reader can act on.
- [ ] `grep -rn 'tasks/suite/021'` across the corpus is empty.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes false.
