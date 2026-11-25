# embarch-core interfaces: `measurements.json`

**Status:** active, 2026-11-22 (`tasks/core/132`). Index: [../interfaces.md](../interfaces.md). Why: [decisions 113 to 115](../decisions/measurements.md). The shape, key by key: `embarch-study-designer/interfaces/hil-shapes.md`; the declaration: `hil-declarations.md`; the reducers: `hil-reducers.md`.

Written by `measurements.rs` (a host study's: `host_parse.rs`, below) into `study_results/<id>/measurements.json` as a device study ends, after the captures close and before `record.dsse.json`, which names it as a subject and copies its `behaviours`. **Absent when the study declares no measurement**; absent for a failed study, and for a host study with no `parse`.

| Key | What Core puts there |
|---|---|
| `schema`, `run_id`, `behaviours` | `1`; the study id; each reducer used, to the behaviour version it ran |
| `measurements[]` | in declaration order |
| `value`, `unit`, `method`, `incomplete`, `uncertainty.type_a` | the reducer's, unchanged |
| `at_utc_ms`, `method.window.{from,to}_utc_ms` | the capture's first and last `core_rx_utc_ms`; the run's end for an empty tap |
| `source` | `{file: "streams/<rendered or raw file>", rows: [0, n-1]}`, or `bytes: [0, len]` for a raw file or an empty capture |
| `by`, `instrument`, `bench_image` | from the tap: DUT `dut`, `null`, `null`; bench `bench`, `{name, kind: "board", identity: null}`, `unverified` |
| `resolution` | a `dut` value's declared one; else `null` |
| `uncertainty`, `u_source` | a `dut` value's declared `U` at `k` is `basis: declared`, `u_source: study`; a bench value `null` and `undeclared`; a count `null` and `none` |
| `rate_check` | present only with a declared `sample_rate_hz`; `tolerance_rel` is `0.05 + 2/(n-1)` |
| `declared_by` | `signal`, `role`, and `study_value` entries, scope from the ledger (`agent` where unseen) or the submitting token |

**A host study's** file ([decision 131](../decisions/host-parse.md)) holds one measurement per step that declared a `parse`, in step order, with `behaviours: {}`: `value` the parsed number (`null` with `parse_failed`), `method {kind: "parse", pattern}`, `source {file: "events.json", step, iteration?}`, `at_utc_ms` the step's end, `incomplete` `truncated_reply` and/or `parse_failed`, `resolution` null, `uncertainty` null, `u_source` `undeclared`, `declared_by` the signal (and the DUT's role). A Test run's **observation prompt** adds one measurement per answer, `by: person`, `method {kind: "prompt", prompt_kind: "observation"}`, `value` the chosen answer (a string) or the number, `declared_by` `[{what: "prompt", name: <step>, scope: "person"}]` (decision 138). `by`, `instrument`, `bench_image` from what the step addressed: a `dut` role's signal `dut`, `null`, `null`; another board's signal `bench`, `{name, kind: "board", identity: null}`, `unverified`; an `Instrument` `bench`, `{name, kind: "instrument", identity: null}`, `null`.

A marker is the first word of a `Text` tap's line, stamped by the arrival row covering it.

## `GET /study/{study_id}/measurements`

Returns the run's own `measurements.json` (a dev-bench study's or a host study's, [decision 131](../decisions/host-parse.md): both sit in the run directory), **byte for byte as Core wrote it**, with `Content-Type: application/json`. No publish, no revision, nothing recomputed or reshaped; read it from the same run directory the publish routes use (`RunLog::run_dir`). It lets a caller read the measurements before writing a Study's prose, instead of publishing once to get at the file. Bearer token required like every route; either scope reads it. Lease-open ([decision 121](../decisions/measurements.md)): it reads a file on disk and touches no port, so it sits in `LEASE_OPEN` beside `/study/{id}/streams`, and a caller without the bench lease reads it.

| Status | When | Body (plain text unless stated) |
|---|---|---|
| `200` | the file exists | the file |
| `404` | the run log has no run of that id (never started, or still to be entered) | `the run log has no run {id}` |
| `409` | the study is in the job registry as `running` | `study {id} is still running: its measurements are written as it ends` |
| `422` | the run is in the log and its files are there but no `measurements.json` was written: the study declared no measurements, did not complete, or is a host study with no `parse` step | **JSON** (`application/json`, the one refusal that is not plain text): `{"error": "study {id} has no measurements.json: it declared no measurements, did not complete, or is a host study with no parse step", "code": "no_measurements"}`; a caller reads `code`, not the sentence ([decision 141](../decisions/measurements.md)) |
| `410` | the run is in the log but its files are gone (discarded, or swept by retention) | `study {id}'s files are gone (discarded or swept by retention)` |

An empty body is never returned. A Core restarted mid-run has no registry entry and no log entry for it, so that run reads `404`, not `409`.
