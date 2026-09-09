# 029 — a task file can grant a worker a path the ownership map reserves

**State:** open
**Source:** supervisor, leg 059, 2026-09-09 — `tasks/core/023` did exactly this and the worker
obeyed it correctly
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix lives in `scripts/` and/or `tasks/README.md`, both reserved

## What

`tasks/core/023-embarch-token-md-says-the-directory-is-locked-down-and-only-the-file-is.md` named
the suite-level doc `embarch-doc/embarch-token.md` as in scope for a `core` worker. `protocol.md`
§3 reserves every shared suite-level doc to the supervisor, and a worker's route to changing one is
a `status.d/<scope>-*` fragment for the supervisor to apply. The worker read the task, made the
edit, reported it plainly, and pre-flagged the failing check as "an expected, task-authorized
exception". **It was not the worker's error.** `check-ownership.py --scope core` fired correctly,
after the fact, on a branch that had already been written and pushed.

So the ownership map has a hole that is not in the map or in the checker: **a task file is prose,
nothing validates its scope claims against §3, and a worker treats the task file as authority.**
The supervisor caught it here only because the check is run pre-merge; the cost was a diff that had
to be adopted as the supervisor's own write rather than merged as a worker's.

## Why now

This is the sibling of `tasks/doc/028` — that one is about a task file's `State:` field being
hand-written and verified by nobody; this one is about a task file's **scope** being hand-written
and verified by nobody, which is strictly worse because §3 is the whole conflict-avoidance
mechanism and `check-ownership.py` exists specifically to enforce it. Two instances of "a task file
asserts something no script checks" in two legs is a class, not a coincidence.

Filing them as one class is worth considering, since the fix is plausibly the same shape: a
`check-task-fields.py`-style pass over `tasks/**` that validates the mechanical claims a task file
makes.

## Options, none chosen

1. **Validate at filing time.** A check that reads each task's `Scope:` and any path it names, and
   fails when a named path is outside what `check-ownership.py` would allow that scope. Catches it
   before a worker is ever dispatched, which is the only place it is free.
2. **Validate at dispatch.** The supervisor already runs `check-dispatch.py`; it could refuse a
   task whose in-scope paths §3 reserves. Later than (1) but still before any work is done.
3. **Make the reserved route explicit in the task template.** A task needing a suite-level doc
   changed says so as *"filed for the supervisor"* or carries a `status.d/` instruction, rather
   than naming the path as if the worker owned it.

**Option 1 and option 3 are not exclusive**, and (3) costs nothing.

## Done when

- [ ] A task file naming a path its scope may not write is caught by something other than a
      supervisor reading a red check after the branch is pushed.
- [ ] `tasks/core/023`'s shape is either impossible to write or unambiguous about who executes it.

## In flux: no
