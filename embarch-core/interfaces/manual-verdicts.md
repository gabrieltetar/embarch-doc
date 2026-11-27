# embarch-core: the manual verdict, unit and person routes

**Status:** active, 2026-11-26 (`tasks/core/174`, [decision 147](../decisions/manual-verdicts.md)). Index: [../interfaces.md](../interfaces.md).

All five take the token and are lease-open. Errors are plain text. Each write is an entry in the [run log](run-log.md), whose chain it extends.

| Method | Path | Body | Response |
|---|---|---|---|
| `POST` | `/manual-verdicts` | `{test_id, definition_hash, unit_key, verdict, reason, dut_image?, note?}`; `verdict` is `pass`, `fail` or `inconclusive`; `definition_hash` 64 lowercase hex; either token | `200 {entry, hash}` of the new `manual_verdict`; `400` a blank or over-long field, a bad hash or verdict |
| `PUT` | `/units/{unit_key}` | `{serial, board_revision}`; **the person's token only, on every Core** | `200 {entry, hash}` of the new `unit_declared`; `400`; `403` the agent's token |
| `GET` | `/units/{unit_key}` | none | `200 {entry, hash}` of the latest `unit_declared` for the key; `404` none declared |
| `PUT` | `/person` | `{name}`; **the person's token only, on every Core** | `200 {entry, hash}` of the new `person_declared`; `400`; `403` the agent's token |
| `GET` | `/person` | none | `200 {entry, hash}` of the latest `person_declared`; `404` none declared |

New [run-log](run-log.md) entry types (none has a `study_id`):

| `type` | Fields |
|---|---|
| `manual_verdict` | `test_id`, `definition_hash`, `unit_key`, `dut_image` (null when absent), `verdict`, `reason`, `note` (null when absent), `scope` (the token's), `relayed` (true when `scope` is `agent`: never counts in a requirement's verdict or in coverage), `at_utc_ms` |
| `unit_declared` | `unit_key`, `serial`, `board_revision`, `scope` (always `person`), `declared` (true), `at_utc_ms` |
| `person_declared` | `name`, `scope` (always `person`), `declared` (true), `at_utc_ms` |
