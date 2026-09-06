# 016 — `history/api.md` line 28 points decision 30 at a file that no longer holds it, and the suite has no rule for that

**State:** open
**Source:** `inbox/doc-history-api-line-28-points-at-the-wrong-file.md`, dropped by `agent/api/023-split-shape-by-mission` 2026-09-06 on its seam check. That unit moved embarch-api decisions 30, 46 and 54 out of `decisions/shape.md` into a new `decisions/tests.md`, repointed every inbound reference inside `embarch-api/`, and is not permitted to edit `history/`.
**Scope:** doc
**Hardware:** none. One or two lines of prose, plus one convention written down.
**Owner:** required — the convention's only sensible home is a `DOC-*.md`, and every `DOC-*.md` is owner-only (`../../embarch-fleet/protocol.md` §3). If the answer turns out to need no `DOC-*.md` edit, this drops to `Owner: no`.

## What

Two lines in `history/api.md` name embarch-api decisions that have since moved:

- **Line 28** — "`spec.md` is 12% smaller and out of reserve: selection semantics
  point at `interfaces/config.md`, and decision 30 moved to `decisions/shape.md`
  where the test tiers live." **Decision 30 is now in `decisions/tests.md`.** It
  is plain text in backticks rather than a markdown link, so no gate catches it.
- **Line 91** — "See embarch-api decision 46." No path, resolves by number, still
  correct. Named only so a fixer does not think it needs touching.

**The judgement, which is the actual task.** Line 28 is a dated history entry and
it was true on the day it was written — decision 30 really did move into
`shape.md` then. Amending it makes the pointer useful to a reader today and makes
the record of that day slightly false; leaving it sends the one reader who
follows it to a file with no decision 30 in it. Both readings are defensible and
the suite has no stated rule, which is why this arrived as a drop rather than as
a repoint.

`api/023`'s reviewer supplied one input the drop did not have:
`DOC-CONVENTIONS.md` already says a decision number addresses a **sub-project**
and not a file, which is why line 91 needs nothing. The open question is whether
that principle also says a `history/` entry should never have carried a file path
in the first place — in which case the rule may be "history entries cite decisions
by number only", and line 28 gets its path removed rather than repointed.

## Why now

Small, and it will only get more common. `DOC-COMPACTION.md` §3 makes splitting a
decisions file the standard response to a byte cap, and this relay has done four
such splits in two days — every one leaves history entries naming the old file.
Deciding the convention after the second occurrence is cheaper than after the
tenth.

## Done when

- [ ] The suite has a stated position on whether a `history/` entry's stale path
      pointer is amended, removed, or left as the dated record — written where an
      author would find it.
- [ ] `history/api.md` line 28 handled per that position. Line 91 left alone.
- [ ] Whether `history/*.md` is hand-editable at all is settled in passing: it is
      assembled by `build_changelog.py` from `changelog.d/` fragments, and this
      task assumes a hand edit survives reassembly. Confirm that before relying on it.
- [ ] `changelog.d/` fragment if anything changed. Gate green
      (`../../embarch-fleet/protocol.md` §10).
