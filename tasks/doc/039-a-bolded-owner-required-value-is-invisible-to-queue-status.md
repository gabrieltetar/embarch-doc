# 039 — `Owner: **required**` parses as not-required, so an owner-only task is offered to a worker

**State:** open
**Source:** leg 074's own queue read, 2026-09-10. Found while selecting, not by a check.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/queue-status.py`, which `../../embarch-fleet/protocol.md`
§2 reserves to the owner.

## What

`scripts/queue-status.py` classifies a task as `owner-only (reserved paths)` by reading its
`**Owner:**` line. It matches the literal word, and a **bolded** value does not match.

Eight `tasks/doc/` files carry an owner-required line. Seven write it plainly:

```
**Owner:** required — the fix is in `scripts/`, which `protocol.md` §2 reserves.
```

One writes it bolded:

```
**Owner:** **required** — `DOC-PROTOCOL.md` is owner-reserved (`check-ownership.py --supervisor`),
```

That one is `tasks/doc/038`. It is the only one of the eight that `queue-status.py` reports as
`open` in the dispatchable list rather than gating out under `owner-only`, and it was offered to
this leg as ordinary worker-dispatchable work in the `doc` scope.

## Why it matters more than a parse bug

**A task that has to be gated out is exactly the task where a missed gate is expensive.**
`doc/038`'s whole subject is two enumerations inside `DOC-PROTOCOL.md`, a file
`check-ownership.py --supervisor` rejects for both supervisor and worker. A worker dispatched to it
would have done the work, had the ownership check go red on its own branch, and burned a unit to
discover a fact the task file already stated in its own header.

**The backstop held and the primary did not.** Nothing would have reached `main` —
`check-ownership.py` runs pre-merge and would have refused the branch. What fails here is the
scheduling gate, which is meant to mean a supervisor never *selects* the task at all.

**This is the third instance of one root cause in this suite, and it is worth naming as such.**
A field whose value is parsed by a literal match is silently broken by ordinary Markdown emphasis:

1. `supervisor-log.md`'s `**Hardware debts: one, and it is free.**` — the whole phrase bolded, so
   the fold's ledger saw no field at all; three of 2026-09-05's ten entries lost a field that way.
   Fixed by `fold-commit.py` refusing a bent marker.
2. A `Compacts:` line annotated with `~~strike~~` instead of having the paid path deleted, which
   made `check-doc-size.py` stop recognising the line and report two filed files as unfiled
   (leg 057; two quieter instances survived on `main` until 2026-09-09).
3. This one.

The first two were each fixed where they were found. Whether the general shape — *a task-file or
log field whose value is matched literally and can be bolded, struck or wrapped* — deserves one
check rather than three is the owner's call and the interesting half of this task.

## Done when

- [ ] `queue-status.py` classifies `tasks/doc/038` as `owner-only`, whether or not its value stays
      bolded.
- [ ] A decision on the general shape: either a single normalising helper every field-reading
      script shares, or a `check-task-state.py` arm that rejects a `**Field:**` line whose *value*
      carries emphasis, or an explicit note that three instances did not clear the bar for one.
- [ ] If the choice is to normalise rather than reject, `tasks/doc/038`'s bolding is left alone —
      it is legitimate Markdown and the script is what was wrong.
