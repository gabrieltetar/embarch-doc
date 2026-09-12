# 033 — `suite/decisions.md` is over its cap and splits along an obvious seam

**State:** open
**Source:** `scripts/check-doc-size.py` went RED during leg 094's `suite/027` fold. The file was
already at **88.2%** (9,035/10,240 B) with two decisions in it; decision 3 took it to
**12,034 B**, 1,794 B over — inside the once-on-a-clock allowance, so it landed on this ledger
entry rather than being trimmed into something less true.
**Scope:** suite
**Hardware:** none
**Owner:** no
**Compacts:** suite/decisions.md
**Size debt due:** 2026-09-19
**In flux:** no — all three decisions are settled records with reversal conditions written; none
of the three subjects is under active change.

**This file was compacted out of reserve two hours earlier**, by `tasks/suite/031` on leg 093 at
23:22 — that is what got it to 9,035 B. It went over again on the next suite decision anyone wrote.
**A compaction that a single new decision undoes is evidence the file is the wrong shape, not
evidence the compaction was bad**, which is the whole of the argument below.

## Why a split and not a compaction

**Nothing here restates anything**, which is the split-first test in
[DOC-BUDGET.md](../../DOC-BUDGET.md). Three decisions, three unrelated subjects, each carrying its
own measurements and its own reversal condition:

- **1 — `rustfmt` is not enforced** (~7.0 K of the file on its own): a tooling/process sequencing
  call, with the `fmt`-vs-`clippy` manifest-field analysis attached.
- **2 — `embarch-outpost` host-only CI**: a CI-position call.
- **3 — `rx_utc_ms` keeps its name in both homes**: a field-naming and clock-semantics call.

1 and 2 are both "how the suite's checks are run"; 3 is not. The suite has no `suite/decisions/`
directory yet — every sub-project has one — so this is also the unit that creates the shape the
rest of the corpus already uses.

## What to do

1. Create `suite/decisions/` and split **verbatim**, byte for byte, no re-wording: `tooling.md`
   (1, 2) and `naming.md` (3), or a seam the splitter argues for better.
2. Keep `suite/decisions.md` as the **index** — the pattern every sub-project's own `decisions.md`
   already follows — not as a redirect stub, because it is genuinely an index and not a moved file.
3. **Re-point every citation.** `suite/decisions.md` is cited from at least
   `embarch-outpost/spec.md`, `embarch-outpost/decisions/clocks.md`,
   `embarch-outpost/interfaces/integration.md`, `embarch-study-designer/decisions/versioning.md`,
   `history/suite.md` and `embarch.md` §5. `check-decision-refs.py` and `check-links.py` are the
   gate; **note that `tasks/doc/044` records that a verbatim split is the one move
   `check-decision-refs.py` cannot see**, so re-check the movers by hand as well.

## Must not delete

- Decision 1's measured numbers: 87 files / 1,289 hunks / 1,947 lines; the 24-files-each split;
  the 172 → 212 hunks decay measurement; the 57-files/33-outside `--all` figure; and the
  `members` vs `default-members` distinction.
- Decision 2's `WEST="${WEST:?…}"` argument for why the workflow does not invoke `run-all.sh`, and
  the "a permanent skip is worse than an absence" reasoning for excluding the cross-decoder leg.
- Decision 3's two-clock statement, its list of sibling `*_utc_ms` fields, the four-repos-plus-
  already-written-captures cost of the rename, and its reversal condition.
- Every one of the three reversal conditions, whole.

## Done when

- [ ] `suite/decisions.md` and each new file are under cap; `check-doc-size.py` green with this
      ledger entry removed.
- [ ] No decision text is re-worded — `git diff` on the moved prose is a pure move.
- [ ] Every citation of `suite/decisions.md` resolves to the file that now holds that decision.
- [ ] Gate green; `changelog.d/` fragment.
