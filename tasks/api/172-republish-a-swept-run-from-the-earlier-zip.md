# 172 — `publish` republishes a swept run by handing Core the earlier zip's own files

**State:** blocked
**Unparks when:** `tasks/core/137` has landed.
**Source:** `embarch-api/open.md` — "A republish after the retention sweep refuses"; `notes/hil/06-report-and-publish.md` — "A revision is built from the earlier zip, its captures included" (owner, 2026-11-20)
**Scope:** api
**Hardware:** none
**Owner:** no

## Dispatch notes

- `embarch-api` decision 117 (`decisions/publish-revisions.md`) refuses a republish after the retention sweep and writes nothing, because Core's `report-data` answered `404` once the run's directory was gone. `tasks/core/137` gives Core a way to take the earlier revision's Core files back; read the decision it lands with before designing this side.
- The earlier zip is already read for a republish (`measurements.json` and the `streams/*` renderings, decision 117), so this extends that read rather than adding a second one.
- Per-decision budgets near their limit in `embarch-api`: `ledger#98`, `bench-exchange#89`, `failure-reporting#67`. Amend 117 in `decisions/publish-revisions.md`, or add a new decision there.
- **`embarch-api/interfaces/publish.md` is in reserve** (11,437 of 12,288 B, out of reserve at 11,059 B), filed as `tasks/api/173`, blocked on `In flux: yes` because `verify` is still moving. This unit edits the publish half of that file, so compact it here: move a settled section verbatim into a new `interfaces/` file with a link left (`DOC-COMPACTION.md` §2's split), leave the `verify` section where it is, and say in your result which bytes moved. That is `tasks/api/173`'s only file, so the supervisor closes it at your fold. While there, the `verify` table's check 5 row still says "`adopted` recomputed", which `tasks/api/171` moved into check 6's whole-document compare (decision 124); correct that one cell.
- **Two stale lines this scope owns, carried here because this unit is the next to edit `embarch-api`** (added by the supervisor, 2026-11-23):
  - `decisions/report-pdf.md` decision 110's "Not verified" line ends "Sizes are for a binary that calls `render_report`; `main.rs` does not yet." `publish` has called it since `tasks/api/167`; noted by three reviewers and never filed. Correct the sentence to what is true.
  - If `tasks/study-designer/089` has landed when you start (it amends `embarch-study-designer/interfaces/hil-pdf.md`'s footer band to 8 to 16 mm, measured), the comment above `FOOTER_BASE_MAX_MM` in `src/verify_report.rs`, decision 123's "on the edge of `hil-pdf.md`'s 8 to 15 mm band … (filed against the doc)" and `open.md`'s first bullet ("8 to 16 mm where `hil-pdf.md` says 8 to 15") each say the shared doc disagrees. Make them say it agrees. If 089 has not landed, leave all three.

## What

When Core reports that a run's directory is swept, `publish` hands Core the earlier revision's Core-produced files from the highest earlier zip, in the shape `core/137` defines, and continues the republish as it does for a run on disk. The earlier zip is still left byte for byte.

## Why now

Closes the one departure from 06's design that `tasks/api/168` recorded, once Core's half exists.

## Done when

- [ ] A test against the mock Core: a swept run republishes to `-r2` from the earlier zip, and the earlier zip is unchanged.
- [ ] A test: a swept run with no earlier zip in the publish folder refuses, saying which file it looked for.
- [ ] Decision 117 amended (or a new decision), `interfaces/publish.md` and the `open.md` line updated.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
