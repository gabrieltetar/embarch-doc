# 172 — `publish` republishes a swept run by handing Core the earlier zip's own files

**State:** claimed by agent/api/172-republish-a-swept-run-from-the-earlier-zip, 2026-11-23 12:38 — resumed; the 11:57 claim's worker died at its login's 5-hour limit
**Source:** `embarch-api/open.md` — "A republish after the retention sweep refuses"; `notes/hil/06-report-and-publish.md` — "A revision is built from the earlier zip, its captures included" (owner, 2026-11-20)
**Scope:** api
**Hardware:** none
**Owner:** no

## Dispatch notes

- **This is a resume** (supervisor, 2026-11-23 12:38). The first worker stopped at 12:08 when its login hit the 5-hour limit, with 120 lines changed in `src/publish.rs`, `src/verify_report.rs`, `tests/publish.rs`, `tests/core_client_http.rs` and `crates/embarch-core-client/src/client.rs`, uncommitted and never built. The supervisor committed that tree as found to the code branch (`97d58d8`, "recovered uncommitted tree"); the doc branch had nothing. Read that commit's diff first and continue from it: it is unreviewed and unbuilt, so keep what is right and change what is not. It touched `embarch-core-client`, a shared crate: keep that change additive, and say in your result what it added.
- `embarch-api` decision 117 (`decisions/publish-revisions.md`) refuses a republish after the retention sweep and writes nothing, because Core's `report-data` answered `404` once the run's directory was gone. `tasks/core/137` gives Core a way to take the earlier revision's Core files back; read the decision it lands with before designing this side. **It landed 2026-11-23 as `embarch-core` decision 120** (`embarch-core/decisions/publish.md`, `embarch-core/interfaces/publish.md`): `PUT /study/{id}/restore/{name}`, raw body, one file at a time — `manifest.dsse.json` first (`422` unless the run log recorded its hash for this run), then every Core file it names as a subject (`409` before a manifest, `422` for a non-subject, a revision output or a wrong digest). `report-data` on a swept run now answers `409` naming what to hand back (it was `404`/`500`), and runs unchanged once every named file is back. embarch-api's own files are not subjects and are not restored; they are resent with `publish` as usual.
- The earlier zip is already read for a republish (`measurements.json` and the `streams/*` renderings, decision 117), so this extends that read rather than adding a second one.
- Per-decision budgets near their limit in `embarch-api`: `ledger#98`, `bench-exchange#89`, `failure-reporting#67`. Amend 117 in `decisions/publish-revisions.md`, or add a new decision there.
- **`embarch-api/interfaces/publish.md` is in reserve** (11,437 of 12,288 B, out of reserve at 11,059 B), filed as `tasks/api/173`, blocked on `In flux: yes` because `verify` is still moving. This unit edits the publish half of that file, so compact it here: move a settled section verbatim into a new `interfaces/` file with a link left (`DOC-COMPACTION.md` §2's split), leave the `verify` section where it is, and say in your result which bytes moved. That is `tasks/api/173`'s only file, so the supervisor closes it at your fold. While there, the `verify` table's check 5 row still says "`adopted` recomputed", which `tasks/api/171` moved into check 6's whole-document compare (decision 124); correct that one cell.
- **Two stale lines this scope owns, carried here because this unit is the next to edit `embarch-api`** (added by the supervisor, 2026-11-23):
  - `decisions/report-pdf.md` decision 110's "Not verified" line ends "Sizes are for a binary that calls `render_report`; `main.rs` does not yet." `publish` has called it since `tasks/api/167`; noted by three reviewers and never filed. Correct the sentence to what is true.
  - `embarch-study-designer/interfaces/hil-pdf.md`'s footer band now reads 8 to 16 mm, measured, citing decision 123 (EMB-242, landed 2026-11-23). The comment above `FOOTER_BASE_MAX_MM` in `src/verify_report.rs`, decision 123's "on the edge of `hil-pdf.md`'s 8 to 15 mm band … (filed against the doc)" and `open.md`'s first bullet ("8 to 16 mm where `hil-pdf.md` says 8 to 15") each still say the shared doc disagrees. Make them say it agrees.

## What

When Core reports that a run's directory is swept, `publish` hands Core the earlier revision's Core-produced files from the highest earlier zip, in the shape `core/137` defines, and continues the republish as it does for a run on disk. The earlier zip is still left byte for byte.

## Why now

Closes the one departure from 06's design that `tasks/api/168` recorded, once Core's half exists.

## Done when

- [ ] A test against the mock Core: a swept run republishes to `-r2` from the earlier zip, and the earlier zip is unchanged.
- [ ] A test: a swept run with no earlier zip in the publish folder refuses, saying which file it looked for.
- [ ] Decision 117 amended (or a new decision), `interfaces/publish.md` and the `open.md` line updated.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
