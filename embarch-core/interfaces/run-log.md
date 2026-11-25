# embarch-core: the run log routes

**Status:** active, 2026-11-21 (`tasks/core/131`, [decisions 111 and 112](../decisions/run-log.md)). Index: [../interfaces.md](../interfaces.md).

All four take the token and are lease-open (they touch files, never a port). Errors are plain text.

| Method | Path | Body | Response |
|---|---|---|---|
| `GET` | `/run-log` | none | `200 {verified, error, length, head, entries}`; `entries` are the `{entry, hash}` lines, `error` names the first line that breaks the chain |
| `GET` | `/study/{id}/log` | none | `200 {run, published, discarded, head, length}`: the run's entry, its latest `published` and `discarded` (or null) and the log head; `404` no such run; `500` the log does not verify |
| `POST` | `/study/{id}/published` | `{"manifest_sha256": "<64 lowercase hex>"}` | `200` the new `{entry, hash}`; `400` malformed hash; `404` no such run. Either token; the entry records which |
| `POST` | `/study/{id}/discard` | none | `200` the `discarded` `{entry, hash}`; `403` the agent's token on a run that did not end clean or has a publish (nothing deleted); `404`; `409` still running or already discarded |

`run-log.jsonl` sits beside the token files; each line is `{"entry": {...}, "hash": "<sha256 hex of the entry's JSON>"}`. Every entry has `type`, `seq`, `prev`, and (but a `confirmed` one) `study_id`, and:

| `type` | Fields |
|---|---|
| `run` | `kind` (`device`/`host`), `status` (`completed`/`failed`), `reason`, `clean`, `ended_utc_ms`, `record_sha256` (null if never signed), `captures` `[{name, sha256}]`, `go_by` (the scope that began the run) |
| `published` | `manifest_sha256`, `scope`, `at_utc_ms`; from the publish route also `revision`, `log_head`, `report_data_sha256` ([publish](publish.md)) |
| `adopted` | `kind` (`note`/`prose`), `name`, `text_sha256`, `scope`, `at_utc_ms` ([publish](publish.md)) |
| `discarded` | `scope`, `files_removed`, `at_utc_ms` |
| `confirmed` | **no `study_id`**: `kind` (the definition's), `sha256` (what was confirmed), `scope` (always `person`), `surface` (a label the caller names), `core_holds` (a suite only), `at_utc_ms` ([definitions](definitions.md), decision 133) |
