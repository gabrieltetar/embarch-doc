# 014 — Compact embarch-outpost/spec.md

**State:** claimed by agent/outpost/014-compact-outpost, 2026-09-10 14:12
**Source:** `scripts/check-doc-size.py`, run from `agent/outpost/005-verify-the-arrival-join`
**Scope:** outpost
**Hardware:** none
**Owner:** no
**Compacts:** embarch-outpost/spec.md
**In flux:** no
**Must not delete:** the `--allow-unverified-join` / `--allow-build-id-mismatch`
posture pairing in the invariant-61 paragraph — it is the reader's only pointer
from the invariant to the escape hatch and the decision it mirrors; and the
missing/short `frame_bytes` column's degrade-not-refuse behaviour, which is the
one case a reader could otherwise assume is a third refusal alongside the
manifest and build-ID ones.

## What

`agent/outpost/005-verify-the-arrival-join` implemented `spec.md:61`'s
invariant in the reference decoder and added one paragraph recording it,
which put `embarch-outpost/spec.md` at 9,515/10,240 B — inside the last 10%
of its cap (`RESERVE_PCT`), 725 B left. The file is still writable and the
gate still passes; this task exists only to name the debt per
`DOC-COMPACTION.md` §2, since the commit that spent the reserve owes the task
that files it.

## Why now

`check-doc-size.py` failed the doc gate for `embarch-outpost` with this file
named and no open task covering it (`embarch-outpost/decisions/tracing.md`'s
reserve is already covered by `tasks/outpost/008`, which is a different file).

## Dispatch note from the supervisor, leg 063

**Try a split before you try a squeeze, and `core/030` is the worked example from yesterday.**
`DOC-BUDGET.md`'s split-first rule exists because a verbatim move restates nothing and therefore
costs no accuracy, whereas a squeeze trades provenance for bytes. On 2026-09-09 `embarch-core/spec.md`
was 108 B into its reserve and the task file suggested squeezing a 12-row constants table; the worker
instead lifted the whole table out verbatim into a new `embarch-core/interfaces/constants.md`, left a
pointer paragraph in `spec.md` naming what moved and that nothing was cut, and added a row to
`interfaces.md`'s table. 9,148 B → 7,977 B, and not one fact left the corpus. **Look for that seam
here first**; only squeeze the prose if there genuinely is none.

**The numbers have moved since this task was filed.** It says 9,515 B / 725 B left; today
`check-doc-size.py` reports `embarch-outpost/spec.md` at **9,775/10,240 B, 465 B left**. Re-measure
before and after rather than trusting either figure, and note that reserve is
`max(1200 B, 10%)` from the top — so getting under 10,240 B is not enough, you need to clear the
reserve band and have `check-doc-size.py` stop naming the file.

**One caution on the `Must not delete:` list above.** Both items are there because a reader would
otherwise draw a *wrong* conclusion, not merely an incomplete one — the `frame_bytes` degrade
behaviour in particular reads as a third refusal alongside the manifest and build-ID refusals if it
goes missing. If a split moves either one, it must land verbatim on the other side.

**Docs-only is expected.** The `embarch-outpost` code branch will almost certainly have a zero diff,
which is fine and has precedent (`core/030`, `topology/023`). Do **not** invent a code change to
justify the branch. And you cannot run `embarch-outpost`'s Zephyr `tests/unit` ztest suite from this
environment — no `west`, no `ZEPHYR_BASE` — which is a standing, already-recorded debt; since this
unit touches no C, it does not deepen it. Say so rather than claiming the suite green.

## Done when

- [ ] `embarch-outpost/spec.md` reduced below its reserve threshold without
      losing any fact the `Must not delete:` list names — a paragraph
      tightened or a repeated fact folded into a cross-reference, not a
      judgement removed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `check-doc-size.py`
      no longer names this file.
- [ ] `changelog.d/` fragment dropped for the compaction itself.
