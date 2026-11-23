# 139 — Core serves a finished run's `measurements.json` before any publish

**State:** done — GET /study/{id}/measurements serves the run file as written; 404/409/410/422 refusals; lease-open; decision 121
**Source:** Fleet Ready issue, found while writing the HIL guide's Study section
**Issue:** EMB-246
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Core writes `measurements.json` as a study ends (`src/measurements.rs`, decision
113, `embarch-doc/embarch-core/interfaces/measurements.md`), but serves it only
inside a publish: `GET /study/{study_id}/publish/{revision}/files/{name}`
answers at a revision `report-data` has opened. An agent writing a Study's prose
must read the measurements first and cite them, so the HIL guide today publishes
once with no prose, reads the file out of that zip, and publishes again.

When this is done, Core has a read-only route that returns a finished run's own
`measurements.json`, byte for byte as Core wrote it, with no publish and no
revision. The path is the worker's to choose and record;
`GET /study/{study_id}/measurements` is the obvious one. An unknown study, a run
that has not ended, and a run whose study declares no measurements (no file was
written) each get a distinct, named refusal rather than an empty body.

`embarch-api`'s tool and subcommand that call it are `api/177`, a separate task
that waits for this one. Do not touch `embarch-api`.

## Why now

The HIL guide (EMB-228, landed 2026-11-23) routes every Study through a
throwaway first revision for want of this read, and every published zip of a
real Study carries an `-r2` for that reason alone.

## Constraints

- **Read-only, and as written.** Serve the file, do not recompute it, and do
  not reshape it: the guide tells the reader to cite what is in the file.
- **Classify the route for the lease the way its neighbours are.** `src/lease.rs`
  lists routes by method and path; place the new one beside the other `GET`
  study reads (`/study/{study_id}`, `/streams`), and say in the decision or the
  interface which list it went in and why.
- The route sweep in `src/api.rs`'s tests enumerates every route; add the new
  one there.
- Where the file lives in a run's result directory is
  `embarch-doc/embarch-core/interfaces/result-layout.md`; use the same path
  resolution the publish route uses rather than a second one.

## Where

- `src/api.rs` (the `/study/{study_id}/...` routes and their sweep test).
- `src/measurements.rs` (`FILE`), `src/publish.rs` (how a run's files are found).
- `src/lease.rs`.
- `embarch-doc/embarch-core/interfaces/measurements.md` (document the route),
  `spec.md` where it lists study routes.

## Dispatch note

No `embarch-core` doc file is in size reserve. Per-decision caps in this scope:
`signing` #110 is **over** its cap by 2,486 B (do not grow it); `lease` #93 has
182 B left and `run-log` #111 201 B. If the route needs a decision, file a new
one in `decisions/measurements.md` rather than growing any of those.

## Done when

- [x] A finished run's `measurements.json` is returned unchanged by one `GET`,
      with no publish having run.
- [x] Unknown study, unfinished run and no-measurements run each refuse with a
      distinct status and message.
- [x] Tests cover all four cases and the route sweep includes the route.
- [x] Gate green on Linux (build, test 437, clippy). **Debt:** the native Windows build was not run: it cannot build from a worktree (gate.md, protocol.md step 1); run `cargo.exe build` from the main checkout once landed.
- [x] `interfaces/measurements.md` documents the route; `spec.md` and
      `decisions/` updated as needed; `changelog.d/` fragment dropped.
