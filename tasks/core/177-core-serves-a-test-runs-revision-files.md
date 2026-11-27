# 177 — Core serves a Test run's revision files

**State:** done — GET /test-runs/{id}/publish/{revision}/files/{name} serves a Test run revision (decision 150)
**Source:** EMB-581 — Core serves a Test run's revision files to embarch-api
**Issue:** EMB-581
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`POST /test-runs/{run_id}/report-data` and `/publish` (core decisions 148, 149)
write a revision's files under `test-runs/<run_id>.publish/r<N>/`, and no route
returns them. A Study has `GET /study/{id}/publish/{revision}/files/{*name}`
(decision 116), which serves the five publish files, any file the manifest names,
and at the pending revision the run's own Core files. `embarch-api`'s publish of
a Test run renders the PDF and the JUnit and OCP exports from `report-data.json`
and the run's study files before the manifest is signed, so it needs the same for
a Test run. When this is done:

- **`GET /test-runs/{run_id}/publish/{revision}/files/{*name}`** serves a
  revision's publish files, any file its manifest names (including
  `studies/<study_id>/...` names), and at the pending revision the run's own
  files, and nothing else: any other name is `404`, and a name that climbs out of
  the run's directory is refused.
- **It mirrors the Study route's rules** (decision 116): the same token and lease
  stance, the same refusal for a name outside the set, the same content type
  handling. Where a Test run has to differ, say why in the decision.
- **The route is listed** in the interface doc, the lease and auth route lists,
  and `DOCUMENTED_ROUTE_COUNT`.

Reuse the Study route's helpers in `src/publish.rs`, as 149 already did for the
publish itself; do not copy `file_handler`.

## Where to look

- `src/test_publish.rs`: `publish_dir`, where a revision's files sit
- `src/publish.rs`: `file_handler`, the Study route to mirror
- `embarch-doc/embarch-core/decisions/publish.md` (116);
  `decisions/test-run-publish.md` (148, 149)
- `embarch-doc/embarch-core/interfaces/publish.md`: "A Test run's publish"

## Where the doc goes

A new core decision beside 149 in `decisions/test-run-publish.md`, or 149
amended if that is the smaller honest change. The route goes in
`interfaces/publish.md` and the `interfaces.md` Publish row. **`embarch-core/open.md`
is in reserve** (893 B left; its compaction `tasks/core/171` is blocked, In flux:
yes): do not write it.

## Done when

- [x] The route serves a revision's publish files, a manifest-named
      `studies/<study_id>/...` file, and at the pending revision the run's own
      files; tests cover each.
- [x] A name outside that set is `404`, and a climbing name is refused; tests
      cover both.
- [x] The route is in the interface doc, the lease and auth route lists, and the
      route count.
- [x] Gate green (`cargo build`, `test`, `clippy --all-targets -- -D warnings`).
