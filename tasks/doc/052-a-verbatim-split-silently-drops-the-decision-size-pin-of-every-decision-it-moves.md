# 052 — A verbatim split silently drops the decision-size pin of every decision it moves

**State:** open
**Source:** `inbox/doc-reseed-locate-api-decision-42-pin.md`, filed by the worker on
`agent/umbrella/059-split-locate-api-doc`, 2026-09-13, and drained into this file by the supervisor
(leg 108) in `umbrella/059`'s fold. **Generalised on the way in** — the drop asked for one key to be
renamed; this task asks for the class, because the fleet has started doing verbatim splits routinely
and every one of them has this defect.
**Scope:** doc
**Hardware:** none
**Owner:** required — `scripts/decision-size-baseline.json` and `scripts/check-doc-size.py` are both
under `scripts/`, which `embarch-fleet/protocol.md` §2 reserves to the owner. No worker and no
supervisor may write either, which is why this is filed rather than done.

## What

`scripts/decision-size-baseline.json` pins decisions that sit over the 4 KB per-decision cap, keyed
by **`<file>#<decision-number>`**. A verbatim split moves a decision to a different file without
changing its number or a byte of its text — so the key stops matching, the old entry orphans, and
the decision reappears as `OVER` with no baseline at all.

It happened this leg, in `umbrella/059`:

| | before | after |
|---|---|---|
| key | `embarch-umbrella/decisions/doctor.md#42` | `embarch-umbrella/decisions/locate-api.md#42` |
| baseline | 5,376 B | **none** |
| `--decisions` reports | `pin   5157 B` | `OVER  5157 B` |

The decision did not grow. Nothing about it changed. The ledger simply lost sight of it.

## Why it is worth a task rather than a one-line fix

**The one-line fix is right and is the first `Done when` item.** The reason this is filed as a class
is that the fleet's behaviour changed on 2026-09-13 and this defect changed with it.

Until this week a verbatim split was a rare move. `tasks/ui/043` demonstrated on 2026-09-13 that a
split pays a size-reserve debt without deleting a sentence of live reasoning, and leg 108 then ran
**three** of them in one leg — `api/081`, `study-designer/038`, `umbrella/059` — specifically because
fourteen size debts are parked on `blocked` compaction tasks that `In flux: yes` will not release,
while a verbatim split restates nothing and so cannot be forbidden by flux. That is now the standard
way this suite pays a reserve debt. **So the rare case just became the common one**, and it silently
un-pins a decision every time it moves one that was pinned.

**The silence is the expensive half.** `check-doc-size.py` returns 1 only for `dfails` — a *pinned*
decision that grew past its baseline. An over-cap decision with **no** baseline entry is printed as
an informational note and the gate stays green, which is correct for a decision nobody has pinned yet
and wrong for one whose pin was just dropped on the floor. The two are indistinguishable in the
output. There are already four unpinned overages elsewhere in the suite
(`embarch-topology/decisions/validation-classifier.md#25`,
`embarch-umbrella/decisions/probe-vendors.md#49`, `embarch-outpost/decisions/clocks.md#17`,
`embarch-core/decisions/logging.md#44`), so an orphaned pin lands in a crowd and does not stand out.

**And the cost lands later, on someone else.** The ratchet only shrinks. Whoever next runs
`--adopt-decisions` re-seeds an unpinned decision at whatever size it happens to be that day — so a
decision that had been held at 5,376 B for months gets re-seeded at whatever a later edit left, and
the tightening the ratchet had already won is quietly given back. The person doing it has no way to
know a pin was ever there.

## Why a worker cannot fix it, and why that is not obviously right

`decision-size-baseline.json` is **data**, not check logic — a list of recorded sizes. It lives under
`scripts/` because that is where the script that reads it lives, and `scripts/` is reserved wholesale.
That is a defensible line and this task does not propose moving it; a supervisor that can edit the
ledger its own gate reads is the thing the reservation exists to prevent. **But the consequence is
worth naming:** the actor who performs a split is structurally unable to record its effect on the
ledger, so every split will keep filing a drop like this one and waiting for the owner. If splits stay
routine, the second `Done when` item below is what stops that from being a standing tax.

## Done when

1. `scripts/decision-size-baseline.json`'s key `embarch-umbrella/decisions/doctor.md#42` is renamed
   to `embarch-umbrella/decisions/locate-api.md#42`. **Pin it at 5,157 B, not the old 5,376 B** —
   the ratchet only shrinks, and tightening to the decision's true current size is correct rather
   than a regression. `python3 scripts/check-doc-size.py --decisions` should then report
   `embarch-umbrella/decisions/locate-api.md#42` as `pin`.
2. **The class is handled, by whichever of these the owner judges right.** Three shapes, no
   recommendation — this is a call about how much mechanism a rare-but-now-routine move deserves:
   - **Key the ledger by decision number within a sub-project** rather than by file path, so a
     decision that moves between files in the same sub-project keeps its pin by construction. Costs
     a one-time migration of the whole file and gives up the ability to pin two same-numbered
     decisions in different files of one sub-project — which should never exist anyway, and
     `tasks/doc/033` (decision-number uniqueness) is the check that would guarantee it.
   - **Make an orphaned pin loud.** Keep the keying, but have `check-doc-size.py` report a baseline
     entry whose file no longer contains that decision as its own line — *"pinned decision N is no
     longer in `<file>`"* — rather than letting it sit in the JSON unmatched while the decision
     shows up as an unpinned overage somewhere else. This is the cheapest of the three and it turns
     a silent loss into a visible one without deciding anything about keying.
   - **Do nothing mechanical**, and accept a drop-and-task per split as the cost. Defensible while
     splits are rare; the argument above is that they are not any more.
3. Whatever is chosen is written down where the next person doing a split will meet it — a note in
   `DOC-COMPACTION.md` §2 beside the split-first rule, or in `check-doc-size.py`'s own header.

## Not in scope

- The four pre-existing unpinned overages listed above. They are unpinned because nobody pinned
  them, not because a split dropped them, and they are a separate judgement.
- Anything about decision 42's own size. It is 5,157 B, it is over the cap, and shortening it is not
  what this task is about — `tasks/umbrella/059` explicitly forbade that and was right to.
