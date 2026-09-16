# 060 — Compact `embarch-core/decisions/streams.md` out of reserve

**State:** claimed — `agent/core/060-compact-core`, leg 116, 2026-09-16
**Source:** `suite/029` (leg 113, 2026-09-13). That unit added **decision 63** to this file and took it
from 9,356 B to **11,219 B**, which is 160 B inside the reserve floor. The supervisor trimmed the new
decision twice — 11,462 → 11,219 — and stopped, because the next cut came out of the clause naming why
the two alternative shapes were not taken, which is the one thing `suite/029` required the decision to
carry.
**Scope:** core
**Hardware:** none — doc prose only. No board, no probe, no live Core, no deploy.
**Owner:** no
**Compacts:** `embarch-core/decisions/streams.md`
**In flux:** no — decisions 30, 38 and 39 have been settled for weeks. **Decision 62 and decision 63
are both recent and both still live**, but neither is being rewritten: 62's own follow-up
(`embarch-ui/src/trace.rs`'s remaining duplication) changes `embarch-ui`, not this file, and 63's
implementation task (`tasks/core/061`) will *add* to its entry's accuracy rather than restate it. See
*Watch for* — this is the field answered per file, and the file is the whole task.
**Size debt due:** 2026-09-27

## What

`embarch-core/decisions/streams.md` is **11,219 / 12,288 B**, reserve floor **11,059 B**. Get it to
**11,000 B or less** — about 220 B, which is one paragraph, not one sentence.

**Read `DOC-BUDGET.md`'s split-first rule before compacting.** This file now holds **five** decisions
(30, 38, 39, 62, 63) across two visibly different subjects: manifest binding and rendering (30, 38, 39)
versus what the **stream index** reports about a tap (62, 63). A verbatim split restates nothing and is
the cheaper move if that seam is real. `scripts/check-doc-size.py --decisions` will tell you whether
this is many decisions or one sprawling one.

**If you split**, note that `tasks/doc/052` records that a verbatim split silently drops the
per-decision size pin of every decision it moves, and `tasks/doc/044` that a verbatim split is the one
move `check-decision-refs.py` cannot see. Both are owner-reserved and neither is fixed; check the pins
and the refs by hand afterwards and say in your report that you did.

## Watch for

- **Update `embarch-core/decisions.md`'s index table** — both the number list and the size column — in
  the same commit. Leg 113 set the streams row to `30, 38, 39, 62, 63 | 11.0 KB`; a split makes that
  row two rows.
- **Do not shorten decision 63's second paragraph.** `suite/029`'s `Done when` required the chosen
  shape to name why the other two were not taken, and that paragraph is the whole of it. If bytes have
  to come from 63, take them from its first or last paragraph.
- **Decision 62 quotes `embarch-ui` decision 10's column pin and cites reversals row 86.** Those are
  load-bearing citations, not decoration — `topology/043` is the cautionary case where a compaction
  target was arithmetically wrong and the sweep still had to be redone.

## Done when

- [ ] `embarch-core/decisions/streams.md` is at or under 11,000 B, or split with each half under its
      own cap.
- [ ] `embarch-core/decisions.md`'s index table matches, numbers and sizes.
- [ ] `DOC-COMPACTION-PASS.md`'s question answered in the supervisor's log entry, in the runner's own
      words: can `spec.md` alone answer what someone needs to work on this component today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
