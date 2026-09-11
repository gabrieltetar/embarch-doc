# 062 — `decisions/target-json.md` decision 19 is over the per-decision cap and nothing has filed it

**State:** claimed — leg 076, worker on `agent/api/062-compact-target-json`
**Source:** `scripts/check-doc-size.py --decisions`, run during leg 076's refill sweep —
`OVER 5510 B embarch-api/decisions/target-json.md#19` against the 4,096 B per-decision cap. It is
**not** on the size ledger (`--due` lists only `core-link.md` and `zephyr.md` for this scope), so
nothing was going to pay it on a clock.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Decision 19 in [embarch-api/decisions/target-json.md](../../embarch-api/decisions/target-json.md)
is 5,510 B against a 4,096 B per-decision cap — 34% over. The file as a whole is not in reserve,
which is why the ledger never saw it: the *file* budget and the *decision* budget are separate
checks and only the first has a clock. Bring decision 19 under the cap.

**Prefer a split over a squeeze**, per [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 — a verbatim
split restates nothing and so cannot lose a fact, which is the whole reason it is preferred. If
decision 19 is really one sprawling decision rather than several wearing one number, compact it
instead and say in the body that you judged it so.

**A written "no safe cut" is an acceptable outcome.** Two of leg 075's three compaction units
concluded the cap was wrong rather than the file, and said so; that is a finding, not a failure.
What is not acceptable is manufacturing bytes by deleting a fact that only lives here.

## Why now

An over-cap decision is invisible to the one mechanism that would otherwise schedule it: the size
ledger clocks *files*, and this is a *decision*. So it will sit at 34% over indefinitely, and it
grows every time somebody amends it — which is exactly the shape that produced
`embarch-api/decisions/zephyr.md` at 14,269/12,288 B.

## Done when

- [ ] `python3 scripts/check-doc-size.py --decisions` no longer reports
      `embarch-api/decisions/target-json.md#19` as OVER — or the task is closed with a written
      argument for why no safe cut exists, naming what a cut would have destroyed.
- [ ] Every existing citation of api decision 19 still resolves: `scripts/check-decision-refs.py`
      green. **If a split moves the decision to a new file, the half with out-of-scope citers keeps
      the original filename** — see `topology/026`, leg 075, where splitting the other way would
      have left four sub-projects' citations red with no legal fix available.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes false.
