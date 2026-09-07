# 001 — Five of `embarch-fleet`'s eight docs are in reserve, and two cannot take a single byte

**State:** open
**Source:** `embarch-fleet/scripts/check-fleet-doc-size.py`'s reserve warning, added 2026-09-07 — the first time this corpus reported pressure rather than only refusal
**Scope:** fleet
**Hardware:** none
**Owner:** required
**Compacts:** embarch-fleet/risks.md, embarch-fleet/protocol.md, embarch-fleet/ops.md, embarch-fleet/DEVELOPING.md, embarch-fleet/open.md

## What

Measured 2026-09-07, after the day's edits:

| File | Size / limit | Left | Limit is |
|---|---|---|---|
| `protocol.md` | 32,466 / 32,466 | **0 B** | baseline |
| `ops.md` | 29,701 / 29,701 | **0 B** | baseline |
| `risks.md` | 12,285 / 12,288 | **3 B** | cap |
| `DEVELOPING.md` | 11,966 / 12,288 | 322 B | cap |
| `open.md` | 11,717 / 12,288 | 571 B | cap |

**`protocol.md` and `ops.md` show 0 B because the ratchet is working, and that
is the finding, not a bug.** Both are over their 25 KB role cap and live on a
baseline that may only shrink, so a baseline equals the file's current size the
moment anything shrinks it. The consequence is exact: **the fleet's two largest
rule documents cannot accept one byte of new rule without a split or an equal
deletion.** That was already true before today and nothing reported it.

`risks.md` at 3 bytes is the sharp end. It is also the file with no obvious
seam: one `#` heading and no `##` sections at all, so a split needs the sections
invented before they can be moved.

## Why now

**The argument that this corpus needed no reserve band was tested and failed.**
That script's own docstring said a reserve exists to stop a *worker* meeting a
wall mid-flight, and no worker writes these files — the only actor is the owner,
who "can shorten a paragraph on the spot". What actually happened on 2026-09-07:
one new rule pushed `ops.md` 1.2 KB past its baseline, and the owner spent
**four squeeze passes** paying for it, the last of which shortened a paragraph
carrying the evidence for an open question about whether `fleet stop` is
reliably seen. The signal available was "you are over", never "you are close",
and by the time it fired the cheap move was gone.

A warning now exists and is advisory — it never changes the exit status, because
this corpus still has no worker to protect. Filing the debt is this task.

## Prefer a split, and there is a worked example in this repo

[DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2, as of 2026-09-07: a split moves
sections verbatim, so it restates nothing and no argument is shortened to pay
for a new one. Two landed the same day:

- `ops.md` §2 → `budget.md`, leaving a pointer so every `§2` citation still
  resolves. That lowered `ops.md`'s baseline **2,553 B permanently**, which four
  squeeze passes had not managed.
- `open.md`'s quota-percentages question → `budget.md`'s `# Still open`, on the
  mission argument: the question is about that doc's own mechanism, and
  `open.md` had 61 bytes while `budget.md` had 8 KB.

## Done when

- [ ] `risks.md` is out of reserve. It has no `##` sections, so say whether the
      split invented them or whether an answered risk was deleted instead.
- [ ] `protocol.md` and `ops.md` each carry a **stated** next seam — the section
      that would move and the file it would move to — so the next rule addition
      is a split someone has already thought about rather than a squeeze under
      time pressure. Neither has to be split now.
- [ ] `DEVELOPING.md` and `open.md` are either out of reserve or named here with
      the reason they stay.
- [ ] Byte numbers before and after, for each file touched.

## Not dispatchable, on purpose

`check-ownership.py` refuses `fleet` as a worker scope and `fleet.toml` reserves
both `embarch-fleet/` and `tasks/fleet/`. A leg never checks that repo out, so
this task can only ever be executed in the owner's own session — which is the
same reason its size gate files no debts of its own.
