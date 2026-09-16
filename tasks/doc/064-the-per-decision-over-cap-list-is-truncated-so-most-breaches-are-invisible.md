# 064 — `check-doc-size.py --decisions` truncates its over-cap list, so most breaches are invisible

**State:** open
**Source:** leg 118, 2026-09-16, while landing the four tasks leg 117 filed off its own per-decision
census. `umbrella/068`'s worker found a **sixth** unpinned over-cap decision
(`embarch-umbrella/decisions/mirrors.md#16`, 4,347 B, over cap since before 2026-09-13) that the
census had missed, and filed it to `inbox/`. I re-ran the census myself to find out how one was
missed, and the answer is that **the census was never capable of seeing it.**
**Scope:** doc
**Hardware:** none — a `scripts/` change and a reading of its output. No board, no probe, no live
Core.
**Owner:** **required** — this is `scripts/check-doc-size.py`, which is owner-reserved. No agent may
write it. Filed here so it is visible in the queue rather than nowhere.

## What

`check-doc-size.py --decisions` builds `drows` (every numbered decision in the corpus, 379 of them),
then prints:

```python
for key, rel, head, size, limit, pin in sorted(drows, key=lambda r: -r[3])[:20]:
    mark = "OVER" if size > limit else ("pin " if pin else "    ")
```

**The `[:20]` is taken over *every* decision by raw size, not over the over-cap ones.** 27 decisions
are pinned above the 4,096 B cap, and most of them are larger than an unpinned breach. So the twenty
slots are filled almost entirely by pinned entries, and an unpinned over-cap decision only appears
if it happens to be one of the twenty largest decisions in the whole suite. Everything below that
line is over cap, unpinned, and printed nowhere.

**Measured, at this leg's end, with `decision_state()` called directly rather than through the
printer:** five decisions are over cap and unpinned. The printer showed **three** of them.

```
4347 B  embarch-umbrella/decisions/mirrors.md#16
4307 B  embarch-ui/decisions/shell.md#25
4301 B  embarch-topology/decisions/validation.md#21      <- printed
4193 B  embarch-umbrella/decisions/sticky-host.md#48     <- not printed
4176 B  embarch-topology/decisions/link-declares.md#20   <- not printed
```

It is also self-concealing in the worst direction: **fixing the big ones reveals the small ones one
at a time.** This leg landed four compactions, and two entries that were invisible this morning are
visible now. A census run today and repeated tomorrow will disagree, with no defect to point at.

## Why it matters more than one miscount

Leg 117 ran this census, reported **five**, and filed four tasks off it — the work this leg just
landed. Its own framing was *"nothing is watching it, and that is the actual finding."* That was
right, and the reason is one line deeper than it looked: **the thing meant to watch it shows the
twenty largest decisions, which is a different question from the one anybody is asking.** A pinned
6 KB decision is *recorded*; an unpinned 4.2 KB one is the breach. The output ranks them the other
way round.

`DOC-BUDGET.md`'s file-level ledger has a clock, a `--due` list and a `--pressure` list, and none of
that exists for the per-decision cap. `tasks/doc/052` records the adjacent defect (a verbatim split
silently drops the pin of every decision it moves).

## Possible shapes, for the owner to choose between

- **Print every unpinned over-cap decision, and cap the list only for the in-budget ones.** Smallest
  change; makes the census answer the question it is asked.
- **Give the per-decision cap a ledger and a clock**, the way the file cap has one — an entry per
  breach, a due date, and a leg's first unit spending on the oldest overdue. This is the larger
  change and it is the one that would stop the class rather than the instance.
- **Separate the two exit codes**, so "over cap and unpinned" is a non-zero exit rather than a line
  in a list that may not be printed.

**Do not close this by pinning the five entries.** Pinning an over-cap decision is the papering-over
move, and every task this leg dispatched said so to its worker.

## Done when

- [ ] `check-doc-size.py --decisions` lists every unpinned over-cap decision, whatever its rank by
      size.
- [ ] Re-running the census twice in a row, with a fix landed in between, does not reveal entries
      that were over cap the whole time.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
