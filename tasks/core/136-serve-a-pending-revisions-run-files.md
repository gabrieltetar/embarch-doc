# 136 — The publish files route serves a run's own files at the pending revision

**State:** done 2026-11-22
**Source:** `embarch-api/interfaces/publish.md`, "What publish needs of Core that Core does not yet do", found by `tasks/api/167`
**Issue:** EMB-241
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`GET /study/{id}/publish/{revision}/files/{name}` (`embarch-core` decision 116, `src/publish.rs`'s `file_handler`) serves one of the four publish files, or a file the revision's signed manifest names. embarch-api renders the PDF, the appendix and the two exports from `measurements.json` before it calls `POST /study/{id}/publish`, which is what writes the manifest, so at that moment the route answers `404` for the run's own files and a study with measurements publishes with a warning and a PDF lacking them.

At the **pending** revision, the one `POST /study/{id}/report-data` has opened and `publish` would sign, serve the run's own Core files (`measurements.json`, `events.json`, `study.json`, `streams/*`) from the run directory, the same bytes the manifest will later sign. Serving only that revision, and only those names, keeps the route from becoming a general file read.

## Why now

`publish` (`tasks/api/167`) cannot write a complete zip for any study that declares measurements until this lands; `tasks/api/168` and `verify` (EMB-226) build on that zip.

## Dispatch notes

- `embarch-core/open.md` is out of reserve (3,842 of 5,120 B) since `core/135`; keep it there.
- Per-decision budgets near their limit: `signing#110` (over), `run-log#111` (201 B left), `lease#93` (182 B left). Amend decision 116 in `decisions/publish.md`, or add a decision there, rather than growing those.

## Done when

- [x] After `POST /study/{id}/report-data` and before `POST /study/{id}/publish`, `GET .../publish/{revision}/files/measurements.json` for that revision returns the run's file, its bytes equal to what the manifest later signs; tested over HTTP.
- [x] A name that is not one of the run's Core files, and a revision other than the pending one, still answer `404`; tested.
- [x] `interfaces/publish.md`'s row for the route says what it serves at a pending revision; decision 116 amended or a new decision added.
- [x] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.

## Debts

- **Native Windows build of embarch-core not run** (worktree cannot; protocol §10): the change is host-neutral Rust, but run it from the main checkout after landing.
- **No end-to-end check against a real Core with embarch-api's `publish`**: tested over HTTP in-process only (`pending_revision_serves_the_runs_own_files_and_nothing_else`). Pending means: revision equals published-count+1 and `report-data.json` exists for it; the served set is `events.json`, `measurements.json`, `study.json`, `record.dsse.json`, `streams/*`.
