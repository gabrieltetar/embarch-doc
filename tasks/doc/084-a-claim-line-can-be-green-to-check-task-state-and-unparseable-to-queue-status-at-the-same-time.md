# 084 — A claim line can be green to `check-task-state.py` and unparseable to `queue-status.py` at the same time

**State:** open
**Source:** leg 142, 2026-09-17, found by the supervisor against **its own four claim commits**.
Not a worker report and not a reviewer finding — it surfaced because I happened to run
`queue-status.py` while one of my own claims was still live.
**Scope:** doc
**Hardware:** none — two Python scripts and one line of `tasks/README.md`.
**Owner:** required — the fix is in `scripts/`, which `check-ownership.py --supervisor` reserves to
the owner. Filed here so it is visible in the queue rather than only in `supervisor-log.md`, which
folds daily and rolls into `log-archive/`.

## What

`tasks/README.md` documents the claim line as:

```
**State:** claimed by agent/<scope>/<NNN-slug>, <yyyy-mm-dd HH:MM>
```

Leg 142 wrote all four of its claims in a different shape —
`claimed 2026-09-17 leg 142 unit 1 — ` followed by the branch name in backticks — and **nothing
told it.** Specifically:

- **`check-task-state.py` passed.** It reads `raw.split()[0]` and checks token zero is one of the
  four words. `claimed` is token zero, so it is green, and it is green by design: that narrowness is
  the whole point of the 2026-09-09 change that made the state field machine-readable.
- **`check-docs.py` passed, 11/11**, four separate times, because `check-task-state.py` is the only
  check that looks at this line at all.
- **`queue-status.py` silently downgraded the task to `recoverable`**, printing
  *"claim line carries no parseable timestamp; branch None"*.

## Why it matters, concretely

`recoverable` is the state a leg's step-0 recovery reclaims to `open`. So for the ~4 minutes between
dispatching `umbrella/086` and noticing this, **a live worker's task was advertised to any successor
leg as available to reclaim and re-dispatch** — the exact double-dispatch the claim-commit interlock
exists to prevent, arrived at from inside the interlock rather than around it.

It did not fire this time. It did not fire because one supervisor was running and it noticed; the
same defect under a leg that was killed and relayed mid-unit is `tasks/doc/048`'s territory, and
`leg 012` is on record having run two tasks twice, concurrently, for an unrelated reason.

**The three earlier claims this leg were equally malformed and are already retired**, so they cost
nothing — but each of them was `recoverable` for the whole time its worker ran.

## Why now

Cheap, and it is a **silent** disagreement between two scripts about the same line. The suite has
paid for this shape before: `tasks/doc/039` is *"a bolded `Owner: required` value is invisible to
`queue-status`"* and `tasks/doc/049` is *"`collect-open-questions` drops every continuation line of a
wrapped bullet"* — the same class, a producer and a consumer disagreeing with no check between them.

## Done when

- [ ] Decide which side moves. Two real options and they are not equivalent:
      **(a)** `check-task-state.py` gains a check that a `claimed` line also carries a parseable
      branch and timestamp, so a malformed claim fails the gate at the claim commit — the point
      where it is free to fix; or **(b)** `queue-status.py` widens its parser to accept what legs
      actually write. **(a) is the safer direction**: a claim that `queue-status.py` cannot read is
      not merely cosmetic, and widening the reader makes the two scripts agree by lowering the
      standard rather than by meeting it.
- [ ] Whichever is chosen, `tasks/README.md`'s documented shape and the checker agree afterwards,
      and a deliberately malformed claim line is shown to fail.
- [ ] Consider whether `queue-status.py` should say something louder than a parenthetical when it
      demotes a `claimed` task to `recoverable`. It is currently one line in a long listing, and a
      supervisor scanning for its own task will read the word `recoverable` as being about some
      other leg's leftovers.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

## Not this task

- **Do not change how `check-task-state.py` reads token zero.** That narrowness is deliberate and
  `tasks/README.md` explains why at length. Whatever is added is *in addition to* token zero, not
  instead of it.
