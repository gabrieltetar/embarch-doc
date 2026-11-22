# 167 — `publish <run id>` turns a finished study run into one zip

**State:** open
**Source:** `notes/hil/14-implementation-plan.md`, unit M1.10 ("The zip"), after M1.8 (`embarch-core` decisions 116 to 119, `tasks/core/135`) and M1.9 (`embarch-api` decision 110)
**Issue:** EMB-225
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`publish <run id>`, an MCP tool and a subcommand, writes one zip for a finished Study run, built through Core's publish routes, so a reader holds every file `notes/hil/06-report-and-publish.md` ("One zip") lists that milestone 1 produces. This is the first half of M1.10; the numeric-oracle listing, per-block authorship and revisions are `tasks/api/168`.

- **The publish folder** is a setting in embarch-api's configuration **with no default**: `publish` refuses until it is set, and the refusal says how to set it (06, "Written to a local folder").
- **Core's side** is `embarch-core/interfaces/publish.md`: `POST /study/{id}/adopt` for each note (the `notes` parameter, the person's words passed verbatim; Core records the token's scope and the text's hash, decision 117), `POST /study/{id}/report-data`, then the render, then `POST /study/{id}/publish` with embarch-api's own files' hashes, and `GET /study/{id}/publish/{revision}/files/{name}` for Core's files. **Read nothing of Core's disk directly**; the files route exists so the zip never needs it.
- **What embarch-api produces** and lists as its own: the PDF (decision 110's `render_report`, with `report.typ` when the run has one; a Study with no `report.typ` still publishes, `notes/hil/02-study.md`, "The report"), the fixed audit appendix rendered from `report-data.json` (06, "The audit appendix", the rows that apply to a Study), the two interop exports (JUnit XML and OCP T&V v2.0 JSON Lines, exactly as `embarch-study-designer/interfaces/hil-run.md`, "A Study's export and check", fixes them), each capture as CSV beside its raw `.bin`, `report.typ` and the Typst packages it used (`vendored_files()`), and the notes.
- **The zip's layout** is this unit's to fix in `interfaces/`, precisely enough that `verify` (EMB-226) can be built from the doc without reading this crate's source.

## Why now

M1.10 is next on the milestone 1 path now that Core signs the manifest, and `verify` (EMB-226) waits on a zip existing.

## Dispatch notes

- **Per-decision budgets near their limit** (`check-doc-size.py --pressure`): `ledger#98` (15 B left), `bench-exchange#89` (122 B), `failure-reporting#67` (192 B). Do not grow those entries; this unit's reasoning goes in new numbered decisions, in a new topic file under `decisions/` with its row in `decisions.md`'s index.
- Decision 110 says `plot_ticks` lives in this crate, not the shared crate; leave that as it is.
- If the zip needs a shape change in `embarch-study-designer` or `embarch-core-client`, stop and report: that is a cross-repo change.

## Done when

- [ ] A fixture run publishes one zip, against a fake Core in a test, holding the PDF, the study file, `events.json`, `measurements.json`, Core's signed record, `report-data.json` and its envelope, the signed manifest, the run log's segment, every capture raw and as CSV, both exports, `report.typ` and its packages, and the notes.
- [ ] Every embarch-api file's SHA-256 in the zip equals the hash sent to Core's `publish` route, in that test.
- [ ] `publish` refuses with no publish folder configured, and the message says how to set one.
- [ ] A Study run with no `report.typ` publishes, with the appendix and a data section.
- [ ] The MCP tool and the subcommand are in `interfaces/`, with the zip's layout; `spec.md` amended.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
