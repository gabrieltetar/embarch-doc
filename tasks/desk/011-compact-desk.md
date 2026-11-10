# 011 — `embarch-desk` decisions/agents.md is in reserve after decision 59's issue-read amendment

**State:** claimed by agent/desk/011-compact-desk, 2026-11-09 20:18
**Source:** `desk/007` amended decision 59 and crossed the reserve line; `DOC-COMPACTION.md` §2
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/decisions/agents.md
**Size debt due:** 2026-11-23
**In flux:** no — the agent-facing read tools (decisions 29, 59) were just worked and are settled.
**Must not delete:** decision 59's caps (2,000 / 500, chosen not measured), its "newest-first listing assumed, not measured" sentence, and its Rejected list.

## What

`decisions/agents.md` 11,455/12,288 B.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it; this is that filing.

## Dispatch notes

- **Doc only**: you get an `embarch-doc` worktree and no `embarch-desk` one. Out of reserve means 11,059 B or less.
- `DOC-COMPACTION.md` §2 and `DOC-BUDGET.md` prefer a verbatim split into a new topic file under `decisions/` where one fits, since a move restates nothing; update `decisions.md`'s index and every link that pointed at a moved decision (`python3 scripts/check-docs.py` catches a broken one). Shorten in place only what a split cannot reach.
- Answer `DOC-COMPACTION-PASS.md`'s question in this file, in your own words: can `spec.md` alone answer what someone needs to work on this component today?
- This leg runs in burndown: no new numbered decision.

## Done when

- [x] The file is clear of its reserve line.
- [x] Every `Must not delete:` item is still readable.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Result

Decisions 29–32, 56 and 59 moved verbatim into `embarch-desk/decisions/access-point.md` (6,373 B); `decisions/agents.md` is now 5,455 B (was 11,455). `decisions.md`'s index has a row per file. `history/desk.md` line 33 still links decision 59 to `agents.md` (not desk-owned; left for the fold). Decision 59's caps, its "assumed, not measured" sentence and its Rejected list moved unedited.

**DOC-COMPACTION-PASS question: can `spec.md` alone answer what someone needs to work on this component today?** Not tested by this pass: the split touched decisions only and restated nothing, so spec.md was neither read for gaps nor changed. Unverified.
