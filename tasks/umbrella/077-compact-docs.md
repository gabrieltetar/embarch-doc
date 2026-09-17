# 077 — `embarch-umbrella/open.md` is back in reserve

**State:** open
**Source:** scripts/check-doc-size.py --pressure, run by `umbrella/076`
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/open.md

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

## In flux

**Yes.** `open.md` is the sub-project's running list of unresolved questions across every check and
command umbrella owns — check 13, 15, 17, decision 26's `--prune`, decision 51, check 5's
never-exercised fail branch, config fragments, macOS validation, check 10's MCP environment, and
now the mirrored-mode WSL2 bullet this unit touched (decisions 30 and 53). Any one of the open
umbrella tasks queued behind this one can plausibly touch it again. Whoever runs this task should
re-check which bullets are still open before compacting, not trust this list.

## Done when

- [ ] `open.md` back under 80% of its 5,120 B cap, by shortening or moving, not by deleting a live
      question.
- [ ] `scripts/check-duplication.py embarch-umbrella` checked before any content is moved elsewhere.
- [ ] No question disappears from `collect-open-questions.py` unless it can be named as answered.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
