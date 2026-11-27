# embarch-core: the run log routes

**Status:** active, 2026-11-21 (`tasks/core/131`, [decisions 111 and 112](../decisions/run-log.md)). Index: [../interfaces.md](../interfaces.md).

All four take the token and are lease-open (they touch files, never a port). Errors are plain text.

| Method | Path | Body | Response |
|---|---|---|---|
| `GET` | `/run-log` | none | `200 {verified, error, length, head, entries}`; `entries` are the `{entry, hash}` lines, `error` names the first line that breaks the chain |
| `GET` | `/study/{id}/log` | none | `200 {run, record_sha256, published, discarded, head, length}`: the run's entry, `record_sha256` the hash the chain binds to the study's record (a Test-run study's `test_run` entry's, else `run`'s; decision 146), its latest `published` and `discarded` (or null) and the log head; `404` no such run; `500` the log does not verify |
| `POST` | `/study/{id}/published` | `{"manifest_sha256": "<64 lowercase hex>"}` | `200` the new `{entry, hash}`; `400` malformed hash; `404` no such run. Either token; the entry records which |
| `POST` | `/study/{id}/discard` | none | `200` the `discarded` `{entry, hash}`; `403` the agent's token on a run that did not end clean or has a publish (nothing deleted); `404`; `409` still running or already discarded |

`run-log.jsonl` sits beside the token files; each line is `{"entry": {...}, "hash": "<sha256 hex of the entry's JSON>"}`. Every entry has `type`, `seq`, `prev`, and (but a `confirmed`, `test` or `test_run*` one) `study_id`, and:

| `type` | Fields |
|---|---|
| `run` | `kind` (`device`/`host`), `status` (`completed`/`failed`), `reason`, `clean`, `ended_utc_ms`, `record_sha256` (null if never signed), `captures` `[{name, sha256}]`, `go_by` (the scope that began the run) |
| `published` | `manifest_sha256`, `scope`, `at_utc_ms`; from the publish route also `revision`, `log_head`, `report_data_sha256` ([publish](publish.md)) |
| `adopted` | `kind` (`note`/`prose`), `name`, `text_sha256`, `scope`, `at_utc_ms` ([publish](publish.md)) |
| `discarded` | `scope`, `files_removed`, `at_utc_ms` |
| `test_run_started` / `test_run_ended` | **no `study_id`**: `run_id`; started `run_hash`, `scope` (the go's, `person`), `session` (the lease holder), `at_utc_ms`; ended `status`, `reason`, `scope` (the cancelling token's, `core` for the executor), `at_utc_ms` ([test runs](test-runs.md), decision 135) |
| `confirmed` | **no `study_id`**: `kind` (the definition's), `sha256` (what was confirmed), `scope` (always `person`), `surface` (a label the caller names), `core_holds` (a suite only), `at_utc_ms` ([definitions](definitions.md), decision 133) |
| `test` | **no `study_id`**: one per test of a Test run, entered as it ends: `run_id`, `test_id`, `definition_hash`, `requirements`, `unit_key` (the DUT's hardware ID; null when unread), `dut_image` (`holds`, `differs`, `claim`; null when unchecked), `verdict` (null when the test was never reached) |
| `test_run` | **no `study_id`**: once per Test run: `run_id`, `status` (`completed`, `cancelled`, `deadline`, `interrupted`), `record_sha256` (the run's signed record, [signing](signing.md); null if signing failed), `study_ids` (every study run it made), `study_records` (`[{study_id, record_sha256}]`: each study's record as the run's amend left it, which is what the chain binds for a Test-run study, [decision 146](../decisions/test-run-record.md); null hash when none), `at_utc_ms` ([decision 144](../decisions/test-run-record.md)) |

**Retention** holds a Test run's study runs while no `published` entry carries its `run_id`, even one published alone, and sweeps them as one unit toward `keep`.
