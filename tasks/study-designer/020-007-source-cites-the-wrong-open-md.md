# `study-designer/007`'s Source cites the wrong `open.md`

**State:** open
**Source:** owner's session 2026-09-07, found while parking the bench queue
**Scope:** study-designer
**Hardware:** none

## What

`tasks/study-designer/007-bond-clearing-has-never-been-observed-firing.md` says its
`**Source:**` is `embarch-study-designer/open.md`. That file has never carried the sentence
it quotes. The bullet lives in **`embarch-dev-bench/open.md`**, under `## Never exercised` —
verify that before editing rather than trusting this drop.

Point the `Source:` line at the file that actually carries it. **Re-quote from the file as it
stands now**: that bullet was amended on 2026-09-07 to record the attempt and the owner's
parking of it, so the sentence in the task is a prefix of a longer bullet, and copying the old
quote forward would recreate the same defect one revision later.

**Do not change `**State:** blocked`, and do not treat this as a reason to run the task.**
007 is parked by the owner until he says otherwise — this is doc hygiene on a parked file, and
a unit that quietly unparks a bench task would undo a decision the owner made deliberately.

## Why now

Dead and misdirected citations were most of a day's queue on 2026-09-07 — `topology/005`
(74 of them), `study-designer/016` and `017`, `dev-bench/013`. This is the same class, and
**no gate catches it**: the `Source:` line is backticked prose rather than a markdown link, so
`check-links.py` never resolves it and `check-decision-refs.py` has no decision number to
check. It was found by reading, which is the only way it can be.

## Done when

- [ ] 007's `**Source:**` names `embarch-dev-bench/open.md` and quotes that file verbatim as
      it stands at the time of the fix.
- [ ] `**State:** blocked` and its parking note are unchanged.
- [ ] Nothing else in 007 is edited — its `Done when` list is deliberately unmet.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
