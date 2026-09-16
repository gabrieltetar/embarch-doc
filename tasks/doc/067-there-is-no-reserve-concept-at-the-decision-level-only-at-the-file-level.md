# 067 — the doc-size reserve exists for files and not for decisions, so a decision hits its cap with no warning

**State:** open
**Source:** leg 120, 2026-09-16, folding `ui/056`. Not reported by any agent — found by calling
`decision_state()` directly after that unit landed, and the numbers below are its output.
**Scope:** doc
**Hardware:** none — a gap in `scripts/check-doc-size.py`'s reporting. No board, no probe, no live
Core.
**Owner:** required — `scripts/` is reserved, and so is `DOC-BUDGET.md` if the rule is stated there.

## What

`check-doc-size.py --pressure` implements a **reserve**: a file inside the last 10% of its cap is
still writable and the gate still passes, but the pressure is printed, a debt is filed, and a
supervisor tells the next worker into that file what its headroom is. `DOC-BUDGET.md`'s whole
argument for it is that a cap used to be a wall a worker met only when its edit was refused, which
converted unrelated work into a compaction task mid-flight.

**None of that exists at the decision level.** A decision has a hard 4,096 B cap; `decision_state()`
reports only `fails` (a pinned entry above its own baseline) and `over_unpinned` (a breach). There is
no third bucket for "under cap and nearly out of room", nothing prints it, and no supervisor can tell
a worker what margin the entry it is about to edit has left — the dispatch notes this fleet writes
carry *file* reserve and say nothing about decisions.

The distribution at `b67da91`, with 0 breaches and 0 pinned failures across 379 decisions:

```
4,080 B   16 B left   embarch-ui/decisions/debug-tab.md#13
4,070 B   26 B left   embarch-outpost/decisions/clocks.md#17
4,064 B   32 B left   embarch-umbrella/decisions/mirrors.md#20
4,041 B   55 B left   embarch-outpost/decisions/testing.md#26
4,026 B   70 B left   embarch-ui/decisions/topology-tab.md#10
4,019 B   77 B left   embarch-umbrella/decisions/locate-api.md#42
```

Six entries under 80 B. **This is a condition, not an incident.** Five of the six got there through a
compaction that landed them just under the line, which is the predictable result of paying a debt to
the cap rather than to a target.

## Why now

Two of this leg's own units ran straight into it and both had to be told the number by hand:

- `tasks/umbrella/071`'s dispatch note has to say decision 42 has **77 B** of margin, because nothing
  would have told the worker.
- `ui/056` drafted decision 13's Part B addition at 4,656 B — **over cap** — discovered it when the
  gate refused, and trimmed to fit at 4,080 B. That is exactly the mid-flight conversion the file
  reserve exists to stop, happening one level down where the reserve does not reach.

## Where it should go

- **Cheapest:** a `--pressure`-style decision line. `decision_state()` already returns every row with
  its size and limit; printing the ones inside the last N bytes (or last 5%) of their cap costs a
  sort. That alone lets a supervisor put decision margin in a dispatch note the way it already puts
  file margin.
- **Consider:** whether a decision-level debt should be *filed* the way a file-level one is, or
  whether printing it is enough. Filing a task per thin decision would add six tasks today and more
  after every compaction; printing it costs nothing and is read at dispatch time, which is when it
  matters. **Lean toward printing, and say why in the decision.**
- **Related, and worth reading together:** `tasks/doc/064` (the over-cap list is truncated at 20 and
  the 27 pinned entries fill it, so smaller breaches are invisible). Both are "the census reports the
  breach and nothing else".

## Watch for

- **A compaction that targets the cap produces this.** If a rule is added, the useful form may be a
  *target* below the cap for a compaction to aim at, not just a warning after the fact.
- **Do not turn the reserve into a second cap.** The file-level reserve is explicitly still writable
  and still green; a decision-level one that failed the gate would be a cap of 3,891 B wearing a
  different name.

## Done when

- [ ] Decision margin is visible somewhere a supervisor reads before dispatch, or a decision is
      recorded that it deliberately should not be.
- [ ] The relationship to `tasks/doc/064` is settled — one mechanism or two.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
