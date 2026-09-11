# 024 — `decisions/topology-tab.md` decision 10 is over the per-decision cap and nothing has filed it

**State:** open
**Source:** `scripts/check-doc-size.py --decisions`, run during leg 076's refill sweep —
`OVER 4430 B embarch-ui/decisions/topology-tab.md#10` against the 4,096 B per-decision cap. Not on
the size ledger, because the ledger clocks files and this is a decision.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Decision 10 in [embarch-ui/decisions/topology-tab.md](../../embarch-ui/decisions/topology-tab.md)
is 4,430 B against a 4,096 B cap — 334 B over, the mildest instance of this shape in the suite.
Bring it under.

**Prefer a verbatim split** ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2). At 334 B over, a
compaction of this one decision is also plausibly the honest answer; whichever you pick, say in the
body which and why. **A written "no safe cut" is an acceptable outcome** — but at 8% over it is a
weaker claim than it was for the files leg 075 refused to shave, so make the argument explicitly
rather than by assertion.

## Why now

`embarch-ui` is the sub-project with the fewest open tasks in the queue — every file under
`tasks/ui/` is `done` or `blocked` — so a worker dispatched to `ui` has nothing else to take, and
"at most one task per sub-project" is per *slot*: an empty scope costs the fleet a whole worker's
concurrency, not just a task.

## Done when

- [ ] `python3 scripts/check-doc-size.py --decisions` no longer reports
      `embarch-ui/decisions/topology-tab.md#10` as OVER — or the task is closed with a written
      argument for why no safe cut exists, naming what a cut would have destroyed.
- [ ] Every citation of ui decision 10 still resolves: `scripts/check-decision-refs.py` green. If a
      split moves it, the half with out-of-scope citers keeps the original filename.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes false.
