# embarch-core interfaces: `measurements.json`

**Status:** active, 2026-11-22 (`tasks/core/132`). Index: [../interfaces.md](../interfaces.md). Why: [decisions 113 to 115](../decisions/measurements.md). The shape, key by key: `embarch-study-designer/interfaces/hil-shapes.md`; the declaration: `hil-declarations.md`; the reducers: `hil-reducers.md`.

Written by `measurements.rs` into `study_results/<id>/measurements.json` as a device study ends, after the captures close and before `record.dsse.json`, which names it as a subject and copies its `behaviours`. **Absent when the study declares no measurement**; absent for a failed study and for a host study.

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

A marker is the first word of a `Text` tap's line, stamped by the arrival row covering it.
