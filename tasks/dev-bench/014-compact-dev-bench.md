# 014 — `embarch-dev-bench/decisions/link.md` is in reserve after decision 35's amendment

**State:** done — agent/dev-bench/014-compact-dev-bench, 2026-09-28
**Dispatch note (supervisor, 2026-09-28):** **unparked on its own clock and its own condition.**
`In flux:` named "whichever of the flash-route migration or the step-cap divergence is next quiet";
`git log -- embarch-dev-bench/decisions/link.md` shows the file untouched since `84243a33`
(2026-09-08), twenty days quiet, and no open task targets decisions 13 or 35 (`dev-bench/010`
cites 35's divergence but is `toolchain`-gated and not in flight). Same reading as `dev-bench/012`
on 2026-09-28. The file is **11,241 / 12,288 B, 1,047 B left**; re-derive it and re-check `git log`
before you shorten anything, as the field below asks. Prefer a verbatim split (`DOC-COMPACTION.md`
§2) — the 30/35 inbound-path and step-ceiling pair against the flashing/detection/identity
decisions is the seam the task names — and if a decision moves, update `decisions.md`'s group
table and every inbound citation; a citation **outside `dev-bench`** you do not edit: drop an inbox
file by absolute path (`/home/gabriel/Github/embarch/embarch-doc/inbox/`) with the exact fix and
say so in your report, and the supervisor repoints it at landing. No other `embarch-dev-bench` file
is in reserve.
**Previous state (leg 057, 2026-09-09):** blocked — `In flux:` said **yes** and named its own
unparking condition, so this was never dispatchable while it held: `.claude/leg.md` forbids sending
a worker to a compaction task whose `In flux:` says yes. Note the mirror of that correction on
`tasks/umbrella/038` in the same commit.
**Source:** `check-doc-size.py`, run during `tasks/dev-bench/002` — decision 35's amendment (the
step-cap removal it claimed was never implemented) pushed the file to 91.5% of its cap
(11,241/12,288 B, 1,047 B left)
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

**Compacts:** embarch-dev-bench/decisions/link.md
**Size debt due:** 2026-09-22
**In flux:** no — rewritten 2026-09-28: both areas the old answer named have been quiet since
2026-09-08 (evidence in the dispatch note above). The old answer, kept as history: yes — decision 13 took a live amendment on 2026-09-07 (Core-flashing the nRF54L15DK
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

- [x] `embarch-dev-bench/decisions/link.md` clear of the 90%-of-cap reserve line.
- [x] Every `Must not delete:` item above is still readable, verbatim or faithfully restated.
- [x] No decision number renumbered; `check-decision-refs.py` still resolves every citation.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Closed 2026-09-28

Verbatim split, per the dispatch note's named seam: decisions 30 and 35 (the inbound-path
FIFO ceiling and the step-cap divergence) moved out to new `embarch-dev-bench/decisions/link-limits.md`,
byte-for-byte. `link.md` kept 6, 7, 12, 13, 18, 19, 25, 36 (transport/detection/identity) and both
`Must not delete:` items — decision 35's amendment paragraph and decision 13's "what is still
unestablished" paragraph — moved/stayed verbatim, neither trimmed.

Before: `decisions/link.md` 11,241 B (91.5% of 12,288 B cap).
After: `decisions/link.md` 7,434 B; new `decisions/link-limits.md` 4,419 B.

Updated in the same commit: `decisions.md`'s group table (split the "The Core link" row into two,
dropped "two hardware ceilings" from `link.md`'s own description since the ceilings moved out) and
`decisions/dispatch.md:27`'s citation of decision 35's amendment, which now points at
`link-limits.md` instead of `link.md` (both files are this repo's own — no cross-repo citation
found, no inbox drop needed). `history/dev-bench.md`'s existing entry naming `decisions/link.md`
for decision 35's 2026-09-08 amendment was left as-is: it is a historical record of where that
amendment lived *at that time*, not a live citation, and outpost's own precedent
(`history/topology.md`) does the same after a split.

No code-repo change: this is a doc-only compaction, `embarch-dev-bench` (code) worktree stayed at
zero commits.

Gate: `check-docs.py` all 11 green; `check-ownership.py --scope dev-bench` OK (3 paths, all owned);
`check-ownership.py --code-repo` OK (0 paths changed); `check-client-names.py` clean against both
worktrees; `check-doc-size.py` exit 0, dev-bench absent from every reserve/over-cap list;
`check-duplication.py` no dev-bench overlaps. `changelog.d/dev-bench-link-limits-split.changed.md`
dropped (121 B). No `features.d/` fragment — no capability shipped, retired, or changed maturity.
No `status.d/` fragment — nothing outside `embarch-dev-bench` changed truth.
