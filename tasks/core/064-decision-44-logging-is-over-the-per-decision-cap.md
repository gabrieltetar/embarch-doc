# 064 — `embarch-core` decision 44 (logging.md) is over the per-decision cap, unpinned, and retired

**State:** claimed by agent/core/064-decision-44-over-cap, 2026-09-16 12:54
**Reserve (leg 118):** `embarch-core/decisions/auth.md` is at 92.4% — 932 B left of 12288 — and is
already filed against `tasks/core/046-compact-core.md`, which is **blocked**. Do not write into
`auth.md` at all in this unit; you have no reason to. If your work does spend reserve anywhere in
`embarch-core`, file `tasks/core/<NNN>-compact-core.md` in the same commit.
**Source:** `core/063`, 2026-09-16 — while compacting decision 30, `check-doc-size.py --decisions`
(via `decision_state()` directly, since `--decisions` only prints its top 20 by size) showed
`embarch-core/decisions/logging.md#44` at **4,352 B**, over the 4,096 B per-decision cap and
**unpinned** — the same shape of gap `core/063` closed for decision 30, found in the course of that
same run rather than searched for. `core/063` was scoped to decision 30 only; this is the sibling
finding, filed rather than fixed so it is not lost.
**Scope:** core
**Hardware:** none — doc prose only. No board, no probe, no live Core, no deploy.
**Owner:** no
**Compacts:** `embarch-core/decisions/logging.md`
**In flux:** no — decision 44 documents a route (`GET /logs/stream`) that was **retired by
`tasks/core/021`** and is already headed `*(retired)*`. Nothing about it is moving.

## What

Decision 44 is a full, unshortened entry (5 paragraphs) for a route that no longer exists. Unlike
decision 30 (`core/063`), this one is not "several arguments under one head" — it is one retired
decision, stated at full pre-retirement length, with a closing retirement paragraph appended rather
than the entry being cut down. **Prefer compacting over splitting** — a new decision number is the
most expensive thing in this suite to reverse, and a retired entry with no live consumer is exactly
the shape `DOC-COMPACTION-PASS.md`'s hot/cold test is for: the corrected offset-advance rule, the
"why hold rather than publish" reasoning, and the retirement itself are what a reader might still
need (hot); the specific incident narrative, the UTF-8 torn-character walkthrough, and the
"originally priced the case as..." self-correction are provenance and investigation log (cold).

**Read it before compacting.** `embarch-core/decisions/logging.md`, decision 44 (`### 44`).
`DOC-COMPACTION-PASS.md` applies in full if compacted, including quoting every cut hunk verbatim.

## Why now

Same reason as `core/063`: the per-decision cap has no ledger entry and no pin here, so an over-cap
decision is invisible except to someone who happens to read `decision_state()` directly (`--decisions`
only prints its 20 largest). Filing this now, while it is in hand, is cheaper than it being found a
second time by accident later.

## Watch for

- **Do not add a pin to `scripts/decision-size-baseline.json` to make the number go away.**
  `scripts/` is owner-reserved.
- **Decision 44 may be cited from outside `embarch-core`.** Grep the whole doc repo for
  `decision 44` before touching the text (`core/063`'s method: `grep -rn "decision 44\b"` across the
  doc repo, cross-checked against `check-decision-refs.py`).
- **This is retired, not live** — the retirement paragraph itself (`**Retired by
  `tasks/core/021`.**`) and the corrected rule it retired are the load-bearing part; the incident
  detail underneath is the more compactable half.

## Done when

- [ ] `embarch-core` decision 44 is at or under 4,096 B.
- [ ] `embarch-core/decisions.md`'s index table's `logging.md` size column matches.
- [ ] Every inbound `decision 44` citation still resolves to the claim it was citing.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
