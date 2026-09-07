# 023 — A spent 429 holds the fleet, and `recent_429()` reads a UTC timestamp as local

**State:** done
**Source:** leg 027 step 0 — `usage-budget.py --suggest` returned HOLD on a 429 whose own `resetsAt` had already passed
**Scope:** doc
**Hardware:** none
**Owner:** required

## What

Two independent defects in `embarch-fleet/scripts/usage-budget.py::recent_429()`, both
measured on 2026-09-06 21:35 MDT. The file is owner-reserved, so this is a report and not
a change.

**1. The 90-minute window ignores the reset time the transcript hands it, in the same JSON
line.** The rejection Claude Code records carries
`quotaLimits: {"status":"rejected","resetsAt":<epoch>,"rateLimitType":"five_hour", ...}`.
Today's newest 429 was at `2026-09-07T03:29:33Z` (21:29:33 MDT) and its own
`resetsAt` was `1788751800` = **21:30:00 MDT, 27 seconds later**. The five-hour window
reset; the owner posted `fleet go` at 21:30:16; requests were demonstrably being served
again. `--check-429` nonetheless holds the fleet for the remaining 89 minutes of a fixed
lookback, on a signal whose issuer has already declared it spent. `ops.md` §25 argues the
5-hour lockout is worth waiting out *because it refills in hours* — but here it had already
refilled, and nothing reads the field that says so.

Candidate fix: a 429 whose recorded `resetsAt` is in the past does not HOLD. That keeps the
hard-signal protection for a live throttle and drops it for an expired one. A 429 line with
no `quotaLimits` keeps today's behaviour.

**2. The timestamp is parsed as local time, so every age is off by the UTC offset.**

```python
when = time.mktime(time.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S"))
```

`ts` is UTC (`...Z`); `time.mktime` interprets the naive struct as **local**. Measured on
the same line: buggy epoch `1788773373`, true epoch `1788751773`, **skew exactly 6.0 h**
(MDT). Two consequences:

- The printed age is wrong and, west of UTC, negative — this run printed
  `HOLD -- a real 429 was recorded -356 min ago`, which is the only number the rule tells a
  supervisor to report to the owner.
- The `when >= cutoff` test compares an inflated timestamp against a correct cutoff, so the
  **effective lookback is 90 min + the UTC offset ≈ 7.5 h**, not 90 min. East of UTC it
  fails the other way: a 429 would be discarded as too old while still live.

`calendar.timegm(time.strptime(...))` is the one-line fix. Note the `getmtime` pre-reject a
few lines up is correct and unaffected.

**Neither defect caused today's HOLD to be wrong on its face.** The true age was 5 minutes,
inside the intended 90. What defect 1 changes is the *verdict*; defect 2 changes the number
reported and the width of the window. They are filed together because they are in the same
six lines.

## Why now

Leg 027 stopped without dispatching anything, correctly per `supervise.md` step 2, on a
signal that was already stale when it was read. Under defect 2 the same HOLD repeats for
about 7.5 hours, so every leg the listener spawns tonight ends the same way — the fleet is
idle until the owner intervenes, which is the failure mode `ops.md` §15 measures as the
largest hole in the fleet's uptime.

## Done when

- [ ] `recent_429()` parses the ISO timestamp as UTC.
- [ ] A 429 whose recorded `quotaLimits.resetsAt` is in the past no longer produces HOLD,
      or the reason it should is written down.
- [ ] The HOLD message reports a true age and, where known, the reset time.
- [ ] `install.py --check` clean; the shim in `embarch-doc/scripts/` is untouched.

## Closed 2026-09-07 — the owner's session, `embarch-fleet` `e7394f5`

All four `Done when` boxes, plus one defect this task did not name.

- `recent_429()` parses with `calendar.timegm`. The measured line's true epoch,
  `1788751773`, is what it now returns; the buggy `1788773373` is what
  `time.mktime` gave.
- A 429 whose `quotaLimits.resetsAt` is in the past returns `None` rather than a
  HOLD. A 429 with no `quotaLimits` keeps the old behaviour, as this task asked.
- The HOLD message reports a true age and, when it knows one, the reset time
  (`the window it names resets in 1h00m`). The no-reset arm says which it is and
  that it is holding for the full window.
- `install.py --check` is clean and the shim in `scripts/` was not touched — the
  implementation is the only thing that changed.

**The defect this task did not name, found while fixing it:** the verdict came
from a substring match on the raw transcript line, so **any session that merely
quoted the marker held the fleet for 90 minutes** — a session reading
`usage-budget.py`, or discussing a rate limit, wrote the string into its own
transcript and became indistinguishable from a live throttle. The decision is now
made on the parsed top-level `error` and `apiErrorStatus` fields; the string test
survives as a cheap pre-filter. Verified with a synthetic transcript whose only
content is the quoted marker: ignored.

**What this does not fix, and it is the bigger number.** The percentages are
still structurally unavailable on this machine — `rate_limits` reaches only a
status line, the VS Code extension runs none, and a search of every transcript
confirms the field is recorded nowhere on disk. So the verdict stays DEGRADED and
the wave stays at `degraded_workers`, which is **2 against a cap of 6**. That is
the fleet's real pace limiter, and it is a separate question from this task.

