# embarch-core: the publish routes

**Status:** active, 2026-11-22 (`tasks/core/135`, [decisions 116 to 119](../decisions/publish.md)). Index: [../interfaces.md](../interfaces.md). Consumer: embarch-api's `publish` (M1.10) and `verify` (M1.11).

All take the token (either) and are lease-open. Errors are plain text. A **Study's** publish only: no Test phase exists.

| Method | Path | Body | Response |
|---|---|---|---|
| `POST` | `/study/{id}/adopt` | `{"kind": "note"\|"prose", "name": "<relative file name>", "text": "..."}` | `200` the `adopted` `{entry, hash}` (`scope`, `text_sha256`); `400` bad kind or name; `404` no such run; `413` text over 1 MiB |
| `POST` | `/study/{id}/report-data` | none | `200 {revision, report_data_sha256, keyid, report_data}`; `404`; `409` the run has no signed record or was discarded |
| `POST` | `/study/{id}/publish` | `{"files": [{"name", "sha256"}]}`, embarch-api's own files | `200 {revision, entry, keyid}`; `400` a bad or duplicate name, or a Core-produced name; `409` no `report-data` yet or it changed since (a later adoption, or another token scope than the asker's), or another publish took the revision; `404` |
| `GET` | `/study/{id}/publish/{revision}/files/{name}` | none | `200` the bytes of one of the four below or any file the revision's manifest names; **at the pending revision** (the one `report-data` opened, before `publish` signs it) the run's own Core files: `events.json`, `measurements.json`, `study.json`, `record.dsse.json`, `streams/*`, the bytes the manifest will sign; `404` otherwise (any other name or revision, or a revision `report-data` has not opened) |

Files in `study_results/<id>/publish/r<N>/`: `report-data.json` (plain), `report-data.dsse.json`, `run-log-segment.jsonl` (every log line before the publish's entry, as in `GET /run-log`) and `manifest.dsse.json`. Both envelopes are DSSE v1 under the [signing](signing.md) key.

**`report-data.json`** (canonical, no clock, no log head): `schema` 1, `study_id`, `kind`, `revision`, `run_status` (`completed`/`step_failed`), `steps` `{total, pass, fail, timed_out, other}`, `subject` `{study_name, provenance}`, `attestation` `{label, core_attested, reason}` (`person's acts not protected` or `agent-scoped only`), `go_by`, `published_by`, `adopted` `[{kind, name, text_sha256, scope, attribution, at_utc_ms}]` (`attribution`: `relayed by the agent`, `the person's`, `entered with the agent's token`, `the person's token`), `observed` `{image_status, declarations}`, `claimed` `{build}`, `core` `{version, keyid}`, `record_sha256`. No `tests`, `requirements` or `verdicts`.

**The manifest Statement:** `subject` is every file Core produced, `[{name, digest: {sha256}}]` sorted (`events.json`, `measurements.json`, `study.json`, `record.dsse.json`, `streams/*`, `report-data.json`, `report-data.dsse.json`, `run-log-segment.jsonl`), `predicateType` `urn:embarch:predicate:publish-manifest:v1`; `predicate`: `schema`, `study_id`, `revision`, `supersedes` (`{revision, manifest_sha256}` or null), `published_by`, `published_utc_ms`, `core.version`, `run_log` `{head, length}` (the chain the segment holds), `record_sha256`, `report_data_sha256`, `embarch_api_files` `[{name, sha256}]` (listed, **not** vouched for). The `published` log entry adds `manifest_sha256` (the SHA-256 of `manifest.dsse.json`'s bytes), `revision`, `log_head` and `report_data_sha256` to [the run log's entry](run-log.md). A `run` entry also carries `go_by`.
