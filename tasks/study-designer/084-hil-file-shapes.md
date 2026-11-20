# 084 — Fix the HIL file shapes in one interface doc

**State:** claimed by agent/study-designer/084-hil-file-shapes, 2026-11-20 15:50 — resumed: the 14:39 claim's worker died with its leg (last write 14:51); its uncommitted tree is `5322a69c` on the branch
**Source:** Fleet Ready issue: the HIL design needs its file shapes fixed in one doc before any code, so a Study's zip is not reshaped when Test lands. `notes/hil/14-implementation-plan.md`, unit M1.1; `notes/hil/10-review.md`, R24 ("the file shapes are fixed as a doc before Study publish").
**Issue:** EMB-216
**Scope:** study-designer
**Hardware:** none
**Owner:** no

**Resume, 2026-11-20:** the first worker died mid-run; its tree (`5322a69c`) was read against every Done-when item, tick fixtures re-derived by hand, and kept unchanged. Gate and `check-ownership.py --scope study-designer` re-run green. Design only: no hardware or code debt.

## What

One interface doc under `embarch-study-designer/interfaces/` that fixes, field by field, the shapes every later milestone-1 unit writes or reads:

- **The six verdicts**, named, with what each means (`notes/hil/03-test.md`, "The verdict").
- **`measurements.json`**: every field `notes/hil/02-study.md` ("Measurements") gives a measurement (`name`, `value`, `unit`, `source`, `by`, `instrument`, `bench_image`, `method`, `resolution`, `uncertainty`, `declared_by`), plus `u_source` and `rate_check`, each with its type, whether it may be absent, and what absent means.
- **`run.json`** (`notes/hil/03-test.md`, "A run").
- **A Study's export and check shape**: what a Study's run exports and what `verify` checks of it. A Study has no verdict.
- **The PDF text extractor and the number grammar** `verify` uses to read numbers back out of the PDF (`notes/hil/06-report-and-publish.md`, "Verify").
- **The plot helper's tick algorithm and the footer rule** (`notes/hil/06-report-and-publish.md`, "The report").
- **A bench board's characterisation**: resolution, `U`, range, and the date and validity period 06's "Instruments" row gives it.

Each shape says which unit produces it and which reads it (the plan's table), so M1.2, M1.5, M1.7, M1.8, M1.9, M1.10 and M1.11 can each be written against this doc alone.

## Why now

The owner's order puts the file shapes first (R24) and the plan marks M1.1 as needing nothing; M1.2, M1.3, M1.5 and M1.9 all wait on it.

## Dispatch notes

- **Doc-only unit.** You get an `embarch-doc` worktree and no code worktree. Read the crate at `/home/gabriel/Github/embarch/embarch-study-designer` (the main checkout, on `origin/main`) where a shape should match a type that already exists, such as `interfaces/result-types.md`'s; do not edit it.
- **The notes are the design and the owner's rulings; do not re-decide them.** Where 02, 03 or 06 states a field or a rule, the doc states it the same way and cites the note. Where they leave a detail open that a shape needs (a type, an enum's spelling, the exact number grammar), decide it and record each such choice in a new `embarch-study-designer` decision, listed so the owner can see what was the notes' and what was yours.
- **`notes/hil/` is not yours to write.** For "notes 02, 03 and 06 point at it", drop one `status.d/study-designer-<slug>.md` fragment per note (one fragment, one target doc), each naming the section and the pointer sentence to add. The supervisor folds them.
- **Size.** `interfaces/<topic>.md` is capped at 12 KB (`DOC-BUDGET.md`). If the shapes do not fit one file, use a small group, `interfaces/hil-*.md`, with one of them as the index the notes point at; say so in `spec.md`'s map. No file of this sub-project is in reserve. Decisions within 256 B of their limit, which you should not need to touch: `streams#39`, `versioning#12`, `seals#17`, `protocols#58`, `authoring#73`, `declares#40`, `protocol-exec#60`, `ble#44`.
- **Out of scope:** the reducers' contracts (M1.2) and the verdict rules' logic (M1.3). This doc names the verdicts and the fields; it does not define how a verdict is reached.

## Done when

- [x] The shapes doc exists under `embarch-study-designer/interfaces/` and covers every bullet in **What**.
- [x] A `status.d/` fragment for each of notes 02, 03 and 06 names where its pointer goes.
- [x] `spec.md`'s map and `decisions.md` updated; a decision records the choices the notes left open.
- [x] Gate green (`../../embarch-fleet/gate.md`, the doc bullet; `check-ownership.py --scope study-designer`); `changelog.d/` fragment dropped.
