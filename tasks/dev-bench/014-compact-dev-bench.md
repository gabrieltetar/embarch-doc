# 014 — `embarch-dev-bench/decisions/link.md` is in reserve after decision 35's amendment

**State:** blocked — **state corrected by leg 057, 2026-09-09.** `In flux:` below says **yes** and
names its own unparking condition (whichever of the flash-route migration or the step-cap
divergence is next quiet), so this was never dispatchable: `.claude/leg.md` forbids sending a worker
to a compaction task whose `In flux:` says yes, and an `open` state on one is the filer having got
the state wrong rather than the flux having ended. Nothing about the file changed; only the state
line did. Note the mirror of this correction on `tasks/umbrella/038` in the same commit — two
`In flux: yes` compaction tasks sitting `open` in one queue is a pattern, not a slip.
**Source:** `check-doc-size.py`, run during `tasks/dev-bench/002` — decision 35's amendment (the
step-cap removal it claimed was never implemented) pushed the file to 91.5% of its cap
(11,241/12,288 B, 1,047 B left)
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

**Compacts:** embarch-dev-bench/decisions/link.md
**Size debt due:** 2026-09-22
**In flux:** yes — decision 13 took a live amendment on 2026-09-07 (Core-flashing the nRF54L15DK
attempted for the first time) and decision 35 just took one in this same commit. Two of this
file's ten entries have been actively corrected within the last two days; do not compact until
whichever of those areas (the flash-route migration, or the step-cap divergence) is next quiet,
and re-check this file against `git log` immediately before shortening anything.
**Must not delete:** decision 35's amendment sentence stating the cap removal was never
implemented and naming the still-live divergence (crate `MAX_STEPS_PER_STUDY` 64 vs. bench 16) —
dropping it re-creates the exact defect this task exists to fix. Decision 13's "what is still
unestablished" paragraph (one success is not a migration; erase-behaviour and non-`wsl-host`
machines are unchecked) — the qualification that keeps that entry from overclaiming the same way
decision 35 did.

## What

`embarch-dev-bench/decisions/link.md` is in reserve (last 10% of its 12,288 B cap). Compact it per
`DOC-COMPACTION.md` and `DOC-COMPACTION-PASS.md`, keeping every decision number and the
load-bearing content of each entry — a shortening pass, not a content change. Prefer a split
(`DOC-COMPACTION.md` §2) over a squeeze if a clean topic seam exists (e.g. flashing/detection vs.
the frame/step ceilings), since this file has several genuinely distinct hardware-hop decisions
bundled under one "Core link" heading.

## Why now

`check-doc-size.py` fails the gate on a file in reserve with no task naming it. This task is that
filing, dropped in the same commit that spent the reserve (decision 35's amendment, `tasks/dev-bench/002`).

## Done when

- [ ] `embarch-dev-bench/decisions/link.md` clear of the 90%-of-cap reserve line.
- [ ] Every `Must not delete:` item above is still readable, verbatim or faithfully restated.
- [ ] No decision number renumbered; `check-decision-refs.py` still resolves every citation.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
