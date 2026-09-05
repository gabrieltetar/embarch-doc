# 004 — `tasks/README.md` sends a compaction debt to a path `check-ownership.py` refuses

**State:** open
**Source:** hit by `agent/api/009-config-decisions-20-21-unbuilt`, 2026-09-04
**Scope:** doc
**Hardware:** none
**Owner:** required

**Filed from `inbox/` by the supervisor, leg 009.** `Owner: required` because the fix is
in `scripts/` or in `tasks/README.md`, both reserved (`protocol.md` §3).

**Sibling of `tasks/doc/002`** — same root cause, different pair of scripts: a gate half
tells a worker to write a path the ownership half refuses. Three instances turned up in
leg 009 alone.

**What the api/009 worker actually did, which stands until this is decided:** it filed
its debt at **`tasks/api/012-compact-api.md`** rather than `tasks/doc/<NNN>-compact-api.md`,
because `check-doc-size.py` matches on the `**Compacts:**` field and rglobs all of
`tasks/`, so the debt is found either way and the scope genuinely is `api`. The
supervisor let it stand. **It is a worker deviating from a written rule because two
scripts disagree**, which is worth deciding rather than leaving as precedent.

## What

`tasks/README.md`'s reserve section, `scripts/check-doc-size.py`'s own failure
message, and the worker briefing all say a doc in reserve is recorded as

    tasks/doc/<NNN>-compact-<scope>.md

in the same commit that spends the reserve. `scripts/check-ownership.py --scope
<sub-project>` allows a worker `tasks/<its own scope>/**` and nothing else, so
`tasks/doc/...` is refused for every worker scope — including the worker that
just spent the reserve and is the only actor told to file the debt.

Two gate scripts therefore cannot both be green on the same branch: filing the
debt where the README says fails `check-ownership.py`, and not filing it fails
`check-doc-size.py`. **Same shape as
`inbox/doc-features-assembly-makes-every-worker-branch-red.md`** — a rule
enforced by one script that a second script forbids the actor from obeying.

`api/009` worked around it by filing `tasks/api/012-compact-api.md` instead:
`check-doc-size.py` matches on the `**Compacts:**` field and `rglob`s all of
`tasks/`, so a scope-directory task satisfies it, and the scope genuinely was
`api`. That works and is documented in the task file, but it is a worker
choosing which of two standing docs to disobey, which is exactly what should not
be a worker's call.

## Why now

The next worker to spend a reserve hits it, will not have this note, and will
most likely report a red gate it cannot fix — or, worse, trim real content out
of a doc to stay under 90% rather than file the debt, which is the outcome the
reserve mechanism exists to prevent.

## Done when

- [ ] One of: `check-ownership.py` allows a worker `tasks/doc/*-compact-<its own
      scope>.md`; or `tasks/README.md` and `check-doc-size.py`'s message name
      `tasks/<scope>/<NNN>-compact-<scope>.md` as the worker's path and keep
      `tasks/doc/` for the supervisor and owner. Both are one-line changes; the
      decision is which of the two docs is the one that was wrong.
- [ ] `tasks/api/012-compact-api.md` moved if the resolution says it should be,
      and its deviation note removed.
- [ ] `scripts/` and `tasks/README.md` are the owner's (`protocol.md` §3), so
      **this is not a worker task.**
