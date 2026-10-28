# 095 — `embarch-ui/decisions/time-chart.md` is in reserve at 11,554 B after `ui/086`

**State:** done — landed 2026-10-28 (embarch-doc `7aa213b0`, no code commit); the worker left the claim line, set at the fold
**Dispatch note (2026-10-28 13:48 leg):** ui reserve — this file (734 B left) and `open.md` 4,366/5,120 (754 B, parked under `tasks/ui/088`); leave `open.md` alone. A verbatim split of whole decisions into a new topic file is also a legal way to clear the line (`DOC-COMPACTION.md` §2) if shortening would cost a rule, number or reversal condition.
**Source:** `ui/086` added decision 66 and left the file at 11,554 / 12,288 B (734 B left)
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/decisions/time-chart.md
**Size debt due:** 2026-11-26
**In flux:** no — the Time chart's caps and axis rules are settled; only the unrun traced-live half (open.md) could move decisions 35 and 37, and that waits on the outpost bridge.

## What

Compact decisions 34-37 and 66: shorten the *Consequences* paragraphs, keep every rule, measured number and reversal condition.

## Done when

- [x] `time-chart.md` at or under 10,500 B.
- [x] Gate green, `changelog.d/` fragment.

## Result

Verbatim split (no cuts): decision 37 moved to `decisions/time-chart-live.md`; `time-chart.md` now 8,373 B (new file 3,504 B). Index rows updated. Nothing deleted, so no quoted-hunk list.
