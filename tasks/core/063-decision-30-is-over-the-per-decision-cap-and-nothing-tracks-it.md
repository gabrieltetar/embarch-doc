# 063 — `embarch-core` decision 30 is over the per-decision cap, unpinned, and tracked by nothing

**State:** open
**Source:** the `core/060` **reviewer**, leg 116, 2026-09-16. It was checking `tasks/doc/052`'s
pin-orphaning defect against the `streams.md` split and, in the course of establishing that **none**
of decisions 30/38/39/62/63 was pinned in `scripts/decision-size-baseline.json`, noticed why that is
not entirely good news: **decision 30 is 4,247 B**, over [`DOC-BUDGET.md`](../../DOC-BUDGET.md)'s
**4 KB per-decision cap**, and unpinned. It is pre-existing and was untouched by `core/060`'s diff,
so the reviewer correctly reported it as outside its own mandate rather than filing against it.
**Scope:** core
**Hardware:** none — doc prose only. No board, no probe, no live Core, no deploy.
**Owner:** no
**Compacts:** `embarch-core/decisions/streams.md`
**In flux:** no — decision 30 is the manifest-binding decision and has been settled for weeks.
`core/060` split the file on 2026-09-16 but moved decisions 62 and 63 out **verbatim** and did not
touch 30's text at all.

**Doc-size reserve for `core` after `core/060`: one file.** `embarch-core/decisions/auth.md`
11,356/12,288 B, 932 B left, filed as `tasks/core/046` and **blocked**. `decisions/streams.md` is
now **6,376 B / 12,288 B** and `decisions/stream-index.md` **5,672 B / 12,288 B** — both far clear,
which is exactly why this is not a file-size problem.

## What

**This is not a file-cap debt and must not be treated as one.** `streams.md` has ~5.9 KB of headroom
after the split. The cap being exceeded is the **per-decision** one, which exists for a different
reason: a single decision entry that sprawls past 4 KB is one nobody reads to the end, and the
budget's answer is to split the *decision*, not the file.

So the question this task has to answer is whether decision 30 is:

- **one decision that has accreted several arguments**, in which case split it into two numbered
  decisions and update `embarch-core/decisions.md`'s index — the expensive option, because **a new
  decision number is the most expensive thing in this suite to reverse**; or
- **one decision stated at length**, in which case compact the entry to under 4 KB without losing the
  "why not" — [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md)'s rules apply in full,
  including quoting every cut hunk verbatim rather than naming categories.

**Read it before assuming which.** `check-doc-size.py --decisions` reports the number.

## Why now

**Because nothing is watching it, and that is the actual finding.** The file-level ledger has a clock
and a leg spends its first unit on the oldest overdue entry. The per-decision cap has **neither a
ledger entry nor a pin** here, so a decision can sit over cap indefinitely and the only reason anyone
knows is that a reviewer happened to open the baseline file while checking something else.

`tasks/doc/052` (owner-reserved, open) already records that a verbatim split silently drops the
per-decision pin of every decision it moves. **This task is the adjacent hole**: a decision that was
*never* pinned is equally invisible, and no split is needed to get there. Whether that gap should be
closed mechanically is the owner's call under `scripts/` — **this task is only about the one decision
that is actually over.**

## Watch for

- **Do not add a pin to `scripts/decision-size-baseline.json` to make the number go away.**
  `scripts/` is owner-reserved, and pinning an over-cap decision is the papering-over move, not the
  fix.
- **If you split decision 30 into two**, `embarch-core/decisions.md`'s index table needs both the
  number list and the size column updated in the same commit, and `check-decision-refs.py` must stay
  green — every existing `decision 30` citation across the suite still has to resolve to whichever
  half now carries the claim it was citing.
- **Decision 30 is cited from outside `embarch-core`.** Grep the whole doc repo before renumbering
  anything.

## Done when

- [ ] `embarch-core` decision 30 is at or under 4,096 B, or split into two decisions each under it.
- [ ] `embarch-core/decisions.md`'s index table matches, numbers and sizes.
- [ ] Every inbound `decision 30` citation still resolves to the claim it was citing.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
