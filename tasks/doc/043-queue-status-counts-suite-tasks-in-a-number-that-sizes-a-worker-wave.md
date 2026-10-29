# 043 — `queue-status.py` counts `suite/` tasks in `dispatchable`, the one number that sizes a wave of workers

**State:** done — `queue-status.py` puts an open `suite` task in its own bucket, listed and counted on a `suite` line, out of `dispatchable` and the refill gate exactly as `bench` is. On the queue as filed (`b286e89f`): dispatchable 13 to 1, and `LOW QUEUE` prints. embarch-fleet `31f4846`.
**Source:** leg 085, 2026-09-11, step 0. Found while sizing a wave of 6 against a queue that
reported `dispatchable: 12` and could feed exactly **one** worker.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/queue-status.py`, a reserved path.

## What

`scripts/queue-status.py` prints `dispatchable: N`. `.claude/leg.md` is explicit about what that
number is for, in the passage that explains why **bench** tasks are excluded from it:

> `queue-status.py` prints them under `bench` and, **deliberately, does not count them in
> `dispatchable`** — that number sizes a wave of workers, and no worker can take these.

`suite/` tasks are the identical case by the same rule, three paragraphs earlier in the same file:

> **Never dispatch a `suite/` task to a worker** — you execute those yourself (§8), and only after
> announcing and parking it.

No worker can take a `suite/` task. They are nonetheless counted in `dispatchable`.

## What it looked like on this leg

```
dispatchable: 12
bench (supervisor-only, run one at a time): 1
```

All twelve were `suite/`. The true worker-dispatchable count was **zero** — every other scope was
`done`, `blocked`, `owner-only` or `hw-gated`. A supervisor sizing a wave of 6 against "12
dispatchable" is reading a number that says the queue is deep when no worker can be given anything
at all.

**Reproducing it:** the twelve were the whole of `b["open"]` —
`dispatchable = len(b["open"]) + len(b["recoverable"]) + len(drops)`, with no drops pending and
every non-`suite` scope sitting in `done`, `blocked`, `owner_only`, `hw_gated` or `bench`. Filing
this very task (`Owner: required`) did **not** move the count, so `owner_only` is excluded
correctly and `suite` is the outlier. Separately and not part of this finding: claiming a task
moved the count **up** by one (12 → 13), so a `claimed` task is reaching `recoverable` while a
supervisor is live — plausibly intended, noted here only so the numbers above reproduce.

## Why the existing guard did not cover it

The **scope-spread** half of `--refill-owed` did fire, correctly:

```
REFILL OWED -- 1 distinct scope(s) (suite), below a wave of 6
```

So a supervisor that runs `--refill-owed` is told to sweep. Two things still go wrong:

1. **`LOW QUEUE` never prints.** The plain form's thin-queue warning — the line `.claude/leg.md`
   tells a leg to relay to the owner, precisely so a queue gets topped up *before* it reaches
   zero — is gated on the inflated count. On this leg the worker queue was empty and the owner was
   told nothing. The relay's own early-warning path is the thing this defect disables.
2. **The two halves disagree about the same queue**, which is the shape that gets a number
   trusted over a warning. `dispatchable: 12` reads as an answer; `1 distinct scope` reads as a
   caveat about concurrency. It is not a caveat — it is the same fact, stated correctly.

## Suggested fix

Count `suite/` out of `dispatchable` exactly as `bench` already is, and print it on its own line
with the same parenthetical honesty:

```
suite (supervisor-only, announced and parked before it runs): 12
```

Then `LOW QUEUE` fires off a number that means what its one consumer uses it for.

## What not to do

Do **not** hide `suite/` tasks or drop them from the listing — they are real, runnable work and the
supervisor needs to see them to pick one to announce. This is about which bucket they are totalled
into, nothing else. The same applies to `owner-only`, which is already listed separately and
already excluded.

## Shipped

As suggested, and nothing hidden: the suite tasks still list, one per line, marked as the
supervisor's own. `--json` gains a `suite` key. **The `12 → 13` on claiming was `tasks/doc/076`**:
the snapshot's one remaining dispatchable task is `api/067`, live and claimed, read as
`recoverable` because its claim line did not parse — not a property of `suite`.

**The listener's count moves with it.** Its cron block runs `--count` and was left alone, so no
re-arm is owed; a suite-only queue now reads 0 there, which still spawns a leg unless a dream is
under 6 hours old. So `.claude/leg.md` now says an open suite task is no reason to dream, and the
script's `NOTHING DISPATCHABLE` line says so whenever suite tasks are listed.
