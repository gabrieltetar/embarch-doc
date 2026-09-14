# 058 — A compaction task's `Done when` target is computed from a percentage the gate does not use

**State:** open
**Source:** `topology/043`, leg 112, 2026-09-13. The worker compacted `embarch-topology/spec.md` from
9,825 B to 9,110 B, **met its task's stated target exactly**, protected everything on the
`Must not delete:` list, wrote a clean `DOC-COMPACTION-PASS.md` answer — and the fold's
`check-docs.py` went **red on `check-doc-size.py`** anyway, 70 bytes short.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix lands in `scripts/` and/or `tasks/README.md`, both reserved.

## What is wrong

`tasks/topology/043-compact-topology.md`'s `Done when` box said:

> back under its reserve line (< 90% of 10,240 B, i.e. under roughly 9,216 B)

`check-doc-size.py` does not use that number. It computes

```python
RESERVE_PCT   = 90.0
RESERVE_FLOOR = 1200
reserve = max(RESERVE_FLOOR, (100 - RESERVE_PCT)% of limit)   # from the top
```

For a 10,240 B cap, `(100-90)%` is **1,024 B**, which is **below the 1,200 B floor**, so the floor
wins and the real line is **9,040 B**. The percentage in the task file was 176 bytes optimistic.

**The floor dominates for every cap below 12,000 B**, which is most of this corpus: the 10,240 B
`spec.md` tier and the 5,120 B `open.md` tier are both floor-governed, and only the 12,288 B decision
groups and the 25,600 B guides are percentage-governed. So a compaction task that states its target
as a percentage is **usually** wrong, and wrong in the direction that makes a worker stop too early.

## Why it is worth fixing rather than noting

**It converts a correct unit into a red gate**, and a red gate on a fold is expensive out of all
proportion to 70 bytes: `.claude/leg.md` says a red gate blocks the task and the leg carries on, so
the cheapest outcome is a clean piece of work recorded as blocked. Here the supervisor filed
`tasks/topology/044` for the remaining 70 bytes instead, which costs a whole second unit to finish
something that was one sentence away.

**And the failure is silent at authoring time.** Nothing checks a `Done when` box against the script
whose verdict it is paraphrasing. The number is written by whoever files the task — often from
`--pressure` output that reports a *percentage* — and it is read by a worker with no reason to doubt
it.

## Options, not a chosen fix

1. **Make `tasks/README.md`'s compaction-task shape say: never state a byte target, state
   `python3 scripts/check-doc-size.py` exits 0 with this file unlisted.** Cheapest, no code, and it
   removes the arithmetic from the place that keeps getting it wrong. `tasks/topology/044` is
   already written this way as a worked example.
2. **Have `check-doc-size.py --pressure` print the target byte count** beside each file, so whoever
   files the task copies a number the gate itself produced rather than deriving one.
3. Both. (1) is the rule, (2) makes the rule easy to follow.

**Not recommended: changing `RESERVE_FLOOR` or `RESERVE_PCT`.** The floor's own comment argues for it
at length and the argument is sound — a percentage of a small cap is not runway, and the floor files
debts earlier on purpose, when a file can still be *split* rather than only squeezed. The defect is
the task-authoring arithmetic, not the threshold.

## Done when

- [ ] A compaction task can no longer state a target the gate disagrees with — by rule, by tooling,
      or both.
- [ ] `tasks/README.md`'s compaction-task shape reflects whatever is chosen.
- [ ] Gate green.
