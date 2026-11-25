# embarch-study-designer decisions: a study's measurement declarations

**Status:** active, 2026-11-21.

What `tasks/suite/057` decided giving a `Study` a field that names its derived measurements, which [02](../../notes/hil/02-study.md) says are "declared by name in the study" and nothing yet let it declare. A cross-repo pass (`embarch-core`, `embarch-api` and `embarch-ui` each build `Study`), run by the supervisor.

Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/hil-declarations.md](../interfaces/hil-declarations.md). Reducers: [hil-reducers.md](hil-reducers.md), decisions 92 to 94.

### 99 — `Study.measurements`: one declaration per measurement, host-only, always compiled

`measurements: Vec<MeasurementDecl>`, at most 32, `#[serde(default)]` (**amended 2026-11-25:** a host study declares its step-time measurements on the step instead, `parse`, [decision 108](host-parse.md)). A declaration names the measurement, one built-in reducer, the tap by `id`, the struct field where the tap is a struct, the input's unit where the tap carries none, the reducer's window, and the values the study declares for itself (`resolution`, `U` with `k`, `sample_rate_hz`), which Core labels `u_source: study`. **The window carries no time bound**: a study is written before its run, so Core sets `from_utc_ms` and `to_utc_ms` from the capture; a declaration naming one fails to parse.

**Host-only, like `record_checks`**: never on `StudyStart`, sealed by neither CRC, named by tap `id`, so `DEV_BENCH_WIRE_SCHEMA_VERSION` stays 15. **Always compiled**, since a `Study` exists in every build while `reducers` needs `alloc`; the eight names and the unit strings are therefore repeated in `measures.rs`, and a test under `reducers` holds them equal to the registry's.

**Never skipped when empty, nor any `Option` in it when `None`**: `Study` also travels as postcard, which has no field names, so a skipped field shifts every byte after it (the crate's own postcard round trip caught the first draft). A v21 study still loads as one declaring nothing.

`HOST_TYPE_SCHEMA_VERSION` 21 to 22, on v19's reasoning (`src/schema_version.rs`): a v21 Core would accept a study declaring measurements and compute none of them, silently.

*Rejected:* reusing `reducers::Window`, which needs `alloc` and carries the time bounds; declaring the study's own values per tap, which would fit a declared rate better but split one measurement's inputs across two lists (two declarations over one tap may now declare different rates, and Core reports each); a marker list, since what stamps a marker is Core's (`tasks/core/132`).

### 100 — `validate_measurements` refuses what Core could not compute, and decides nothing about trust

Beside `validate_record_checks`, run after `validate_taps`: an empty or repeated name; an unknown reducer; a tap the study lacks; a window key the reducer does not take, or one it needs and lacks (`percentile` for `percentile`, both markers for `interval`, `from_marker` for `value_at_marker`), and a percentile outside 0 to 100; a field on a tap that is not a struct or for a reducer that reads no values, a struct tap's value reducer with no field or a field its layout lacks; a value reducer (`min`, `max`, `mean`, `percentile`, `value_at_marker`) over a tap whose records are not numbers; a unit a reducer reading no values is given, a value reducer with no unit where the tap carries none, a unit outside the reducers' list, or one other than a `Samples` tap's own; `resolution`, `U` or `k` on a reducer reading no values, `k` without `U`, and any declared value that is not finite and above zero.

**Not refused: a marker name** (a name no capture produces gives `value: null`, `parse_failed`, decision 92), **and whether a study's declared `U` applies**: 02 lets a study declare it only for a `dut` value and Core fills `by` from what the step addressed, so honouring it is Core's.
