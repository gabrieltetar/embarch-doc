# 036 — `check-ownership.py` refuses a real scope, by name, when its cwd is a code repo

**State:** open
**Source:** leg 070's supervisor, 2026-09-10, running `tasks/dev-bench/008` as a `toolchain` unit
with its own hands. Hit while trying to gate the code half.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/`, which `../../embarch-fleet/protocol.md` §2 reserves.

## What

Run from inside a code repo — which is where `protocol.md` §10 tells you to run it, since it is
required "on **both** of the worker's branches" — `check-ownership.py --scope dev-bench` prints:

    unknown scope 'dev-bench' (known: doc, suite)

Run from the instance checkout against the identical argument, it prints the allowed paths and
does its job. The scope list is derived from the `embarch-*` directories the cwd can see, and a
code repo can see none of them, so **every** sub-project scope is unknown there and only the two
literals survive.

## Why this is worse than it looks

**It fails loudly and in the shape of a task-file error.** "unknown scope 'dev-bench'" reads as
*you passed a bad scope* — the thing an actor checks first is its own spelling, then
`tasks/README.md`'s scope list, then the task file's `Scope:` field, all of which are correct. The
cwd is the last thing anyone suspects, because the same command works three lines earlier in the
same session.

**It is the second instance of one defect**, and `tasks/doc/035` is the first: `queue-status.py`
reports a completely empty queue when its cwd is outside the instance. That one is worse (it is
silent and it can send a leg to `ops.md` §7's dream with 29 dispatchable tasks sitting in the
queue — leg 070 nearly did exactly that at its own step 0), but the root cause is the same and a
fix for one should probably be a fix for both: **a script that derives its universe from `os.getcwd()`
and reports the empty answer as a real one.**

## Why now

A `bench` or `toolchain` unit is run by the supervisor **in a code repo**, by design
(`protocol.md` §7), so this is not an edge case for that whole class of work — it is the normal
path. Leg 070 recorded the failure in `tasks/dev-bench/008` rather than working around it, and the
code half of that unit therefore landed with `check-client-names.py` run and `check-ownership.py`
not.

## Done when

- [ ] `check-ownership.py --scope <any real sub-project>` works regardless of cwd, or fails saying
      *what* it could not find rather than asserting the scope does not exist.
- [ ] The same question asked of `queue-status.py` (`tasks/doc/035`) — one fix or two, but decided
      together rather than twice.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
