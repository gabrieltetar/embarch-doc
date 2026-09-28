# 077 — `embarch-umbrella/open.md` is back in reserve

**State:** done — paid out by `umbrella/088`, riding on that unit's own edit to the check-15 bullet
(077's `Must not delete:` list's first item) per `.claude/leg.md`'s "the compaction rides in this
unit" rule for a file in reserve that a task is already editing. `open.md` went from **4,372 B
(85.4%, PARKED)** to **3,905 B (76.3%, PAID)** — `scripts/check-doc-size.py --pressure` now reports
it out of reserve. Every bullet's fact survived; `check-duplication.py embarch-umbrella` was run
before and after (two real overlaps found and resolved: the check-15 bullet against
`decisions/schema-skew.md` decision 34, and the `apply_plan` hardware-debt bullet against
`decisions/sticky-host.md` decision 51 — both now point at the decision instead of restating its
mechanism). The check-5 bullet's protected clause (which outcome udev-rules-restored actually
produces) and the check-17 bullet were left untouched. Previously: blocked — see the original
`**In flux:**` note below, superseded now that the pay-out landed.
**Source:** scripts/check-doc-size.py --pressure, run by `umbrella/076`
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/open.md
**Unparks when:** umbrella's `open.md` bullets stop moving — concretely, when check 17's two Fail
arms (`tasks/umbrella/033`), check 13's bench run (`tasks/umbrella/037`) and check 5's
never-exercised fail branch have each either landed or been closed, since each of those rewrites
the file. Any one of them landing is reason to re-read this field rather than to unpark on sight.
**Must not delete:** `open.md`'s note that check 15 is not a hash comparison and must not be read
as one; its note that check 17's two Fail branches have never met a real narrow-bound Core **and
which half of that debt each arm settles**; its note that `saved.host` is sticky and `doctor`
check 2 still reads it **including why that was left unfixed** — a deliberate abstention that
reads as an oversight without the reason; and the mirrored-mode WSL2 bullet `umbrella/076` just
corrected, in particular **which outcome check 5 actually produces with udev rules restored**
(`probes-present`, not `no-probe-found`) — that correction exists because the old text named an
unreachable code path, and shortening it back into vagueness would re-open the same trap.

**Size debt due:** 2026-10-17

**Reserve:** `open.md` was last paid out by `umbrella/023` (2026-09-06, 4,527 B) per the history in
[tasks/umbrella/009-compact-docs.md](009-compact-docs.md), which struck it off that task's own
`Compacts:` line on 2026-09-09 once `038` (now folded and deleted) took over. `umbrella/076`
(2026-09-17) corrected the check-5 settling protocol's unreachable outcome and cross-referenced
the new decision 53 it filed for `doctor.rs`'s USB-scan fix, pushing the file from 3,843 to
**4,127 B (80.6% of the 5,120 B role cap), 993 B left.** Both edits were load-bearing — the old
text named a code path `check_probes` cannot reach — so nothing here was speculative padding.

Not filed against `009`, which is currently scoped to `decisions/bind.md` only and whose own `In
flux: yes` is about that file's check-17 history, not `open.md`'s. Mixing the two would put a
compaction task in the position of naming a pass across unrelated reserve episodes.

## What

Bring `open.md` back under 80% (4,096 B) without deleting a live question, the way `022` and `023`
did last time: read for duplication against `spec.md` and the `decisions/*.md` files first
(`scripts/check-duplication.py embarch-umbrella`), then shorten wording before considering a move.
Run `scripts/check-doc-size.py --pressure` before and after and record the new percentage here.

## Why now

Not yet blocking anything — 993 B of headroom remains. Filed now per this repo's own reserve
convention (`DOC-COMPACTION.md`, `check-doc-size.py`'s "RESERVE" band) so the debt survives past
this leg rather than living only in a supervisor's report.

## In flux (at filing — resolved by the pay-out above)

**Yes, at filing.** `open.md` is the sub-project's running list of unresolved questions across every check and
command umbrella owns — check 13, 15, 17, decision 26's `--prune`, decision 51, check 5's
never-exercised fail branch, config fragments, macOS validation, check 10's MCP environment, and
now the mirrored-mode WSL2 bullet this unit touched (decisions 30 and 53). Any one of the open
umbrella tasks queued behind this one can plausibly touch it again. Whoever runs this task should
re-check which bullets are still open before compacting, not trust this list.

## Done when

- [x] `open.md` back under 80% of its 5,120 B cap (in fact under the script's real reserve line,
      3,920 B — 3,905 B, 76.3%), by shortening wording, not by deleting a live question.
- [x] `scripts/check-duplication.py embarch-umbrella` checked before any content is moved elsewhere
      (run before and after; the two flagged overlaps are what got shortened).
- [x] No question disappears from `collect-open-questions.py` unless it can be named as answered —
      the routing half of the check-5 bullet was the one thing removed outright, and decision 49
      itself already names that half settled, not open.
- [x] Gate green, `changelog.d/umbrella-*` fragment dropped.
