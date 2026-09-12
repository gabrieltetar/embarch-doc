# 035 — Compact embarch-core/decisions/flashing.md

**State:** done — leg 099, 2026-09-12. Split verbatim per the dispatch note below:
`decisions/flash-backend.md` created (decisions 36, 49, 52, 54, byte-for-byte),
`decisions/flashing.md` kept 10/18, 21, 32. Index and both files' headers
updated; no inbound citation named the file path for the moved decisions (bare
`decision N` mentions elsewhere are stable across the move by
`DOC-CONVENTIONS.md`), so none needed repointing beyond the index row split.
**Size debt due:** 2026-09-24 (two weeks out; re-check `flash_backend.rs`'s
churn rate then and either compact or extend).
**Source:** `scripts/check-doc-size.py`, run by task `core/017` (2026-09-10):
`embarch-core/decisions/flashing.md` at 11487/12288 B (93.5%, 801 B left), no
debt filed.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

**Compacts:** `embarch-core/decisions/flashing.md`

**Unparked by leg 099, 2026-09-12, as a verbatim split rather than the shortening pass this task
was written as.** The `In flux: yes` block below is an argument that the vendor-tool discovery path
keeps moving and that its prose should not be rewritten yet. That is correct, and a verbatim split
restates nothing, so it cannot forbid one (`.claude/leg.md`, `DOC-BUDGET.md`'s split-first rule).
Better than that: the churn the block names is confined to **one half of the file**, and the file
has a clean seam down the middle of its seven decisions —

- **stays** (the flashing operation itself): 10/18 multipart + `Format::Bin`, 21 plain `attach`
  with a best-effort reset pulse, 32 `erase` must not be EmbArch's own guess;
- **moves** (backend selection and vendor-tool discovery — the churning half): 36 backend per chip
  family, 49 `requires_vendor_tool` as its own classifier, 52 `EMBARCH_FLASH_BACKEND` validated
  against known names, 54 `Backend::NrfJprog` retired.

Splitting along it gives the half that is actually in flux its own file with real headroom, so the
next `flash_backend.rs` decision — the fourth in as many weeks — does not spend a reserve that is
already gone. **Dispatch note: move those four decision bodies byte-for-byte and do not reword,
merge or shorten any of the seven.** The `Must not delete:` list below is satisfied by construction;
check it anyway. Repoint every inbound citation in `*.md` **and** in source comments — `embarch-core`
is the sub-project most cited into by the others, and `core/008` already found five stale citations
where the task predicted two.

Shorten `decisions/flashing.md` (`DOC-COMPACTION.md`/`DOC-COMPACTION-PASS.md`)
without deleting a decision number or a distinct finding. The file grew past
90% of its reserve when decision 54 (retiring `Backend::NrfJprog`) landed.

**In flux:** per file, now that the split is done.
`embarch-core/decisions/flashing.md` (10/18, 21, 32, the flashing operation
itself) is not in flux — untouched content, well under reserve at 3.6/12288 B.
The churn moved with the decisions it belongs to: `flash-backend.md` (36, 49,
52, 54, new sibling, not itself named on the `Compacts:` line) stays in flux —
`flash_backend.rs` has had three decisions land in as many weeks and the
vendor-tool discovery path is still where real hardware surprises keep showing
up (WSL PATH bleed, extensionless artifacts, now a whole unused backend); it
carries its own headroom (8.4/12288 B) rather than sharing flashing.md's, so
the next decision there does not reopen this task.

**Must not delete:** decision 32's causal-evidence framing (bricked board,
four-for-four correlation, no invented mechanism); decision 36's
licensing/no-bundling rationale; decision 49's nRF54H refusal-vs-topology
distinction; decision 52's dead-arm-removal reasoning; decision 54's
"nothing recorded ever selected it" evidence trail.

## Why now

`check-doc-size.py` names this file with no filed debt; per protocol §5 item 5,
that failure must be filed rather than left silent.

## Done when

- [x] `embarch-core/decisions/flashing.md` back under reserve (under 90% of
      12288 B), same decision numbers still resolving.
- [x] `scripts/check-doc-size.py` clean.
- [x] Gate green.
