# 043 — the reversals corpus records only the first of two decision-32 drifts

**State:** open
**Source:** `inbox/core-071-reversals-gap-decision-32-second-drift.md`, filed by the
`embarch-reviewer` for `core/071` (code `641fd15`, doc `4219867`) after that unit's worker found the
gap and correctly refused to act on it — `embarch-decision-reversals.md` and `reversals/` are
supervisor-owned, so no worker can write the row.
**Scope:** suite
**Hardware:** none — one row of prose in a markdown range file. Nothing is built, no board, no
probe, no live Core.
**Owner:** no — but this is a `suite`-scope task, so it is the supervisor's own hands
(`../../embarch-fleet/protocol.md` §8) and it carries the announce-and-park window of
`../../embarch-fleet/ops.md` §4. **Never dispatch it to a worker.**

## What

`embarch-decision-reversals.md` records the **first** decision-32 drift and only the first. Rows 19,
28 and 55 (in `reversals/rows-1-50.md` and `reversals/rows-51-72.md`) all sit in the
2026-08-25–08-27 window: the `do_chip_erase` brick, the "rejected as written vs. shipped" gap, and
the pre-migration `design.md`'s own correction note catching it. `grep -n "core 32" reversals/*.md`
across all four range pages returns those three rows and nothing else.

Nothing records the **second** occurrence. The 2026-09-02 four-file migration (`c767f8d`) dropped
the same-day *"Correction 2026-08-25"* paragraph and the *"Superseded 2026-08-27 by decision 36"*
paragraph that `decisions/flashing.md`'s decision 32 carried, reverting it to the flat, wrong
*"Rejected … sector-erasing the declared NVM regions"* framing. That reverted framing then stood
uncorrected — through the 7-file split (`3854e13`) and everything after — until `core/071` struck it
again on 2026-09-17 (`4219867`).

## Why now

This is a second, unrecorded instance of exactly the shape the reversals file exists to catch: a
decision that had already corrected itself, silently reverted to the wrong claim by a mechanical
restructuring that touched no code and broke no gate. It went unrecorded for over two weeks, and it
surfaced only because `core/071` was told to re-derive a git history it had been handed
second-hand. Absent the row, nothing would catch a third recurrence — and the recurrence mechanism
(a DOC-COMPACTION split dropping a decision's own corrections) is still live.

## Done when

- [ ] A new row is added to the appropriate `reversals/rows-*.md` page — or a new page per the
      file's own convention, `rows-93-110.md` currently ending at row 110 — recording the
      2026-09-02 `c767f8d` migration dropping decision 32's two correction paragraphs, the framing
      that then stood until `core/071` (2026-09-17, `4219867`), and citing `| core 32 |`.
- [ ] The row follows the existing shape: drift statement → **what actually happened** → how and
      when it was caught.
- [ ] `embarch-decision-reversals.md`'s index table is updated if the row count or page range moved.

## Two known mechanical traps, both filed and both the owner's to fix

Plan for them rather than discovering them mid-fold:

- **`fold-commit.py` refuses every `--path` under `reversals/`** (`tasks/doc/073`). The top-level
  `embarch-decision-reversals.md` is accepted and the range files are not. `suite/042` hit this and
  landed as two commits. Commit the `reversals/` edit separately, *before* the fold.
- **`fold-commit.py`'s `git rm` fails on a task file carrying an unstaged modification**
  (`tasks/doc/072`), which is every `suite/` task, because the supervisor edits it in its own
  working tree. `git add` this file before the fold.

## Announcement window

`../../embarch-fleet/ops.md` §4: post to #embarch-fleet, record the `ts` **here**, keep running
other units, and execute this as a leg's last unit only if no objection arrived and 30 minutes have
passed. If a leg ends before the window closes, this stays `open` with the `ts` below and the next
leg completes the window rather than restarting it.

**Announcement `ts`:** `1789631349.946519` — posted by leg 134 at 2026-09-17 ~01:49 local. The
window closes 30 minutes later. No objection as of that post; the leg polls
`scripts/fleet-read.py --thread 1789631349.946519` at every unit boundary.
