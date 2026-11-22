# embarch-study-designer: a study's measurement declarations

**Status:** active, 2026-11-21. Code: `src/measures.rs`, always compiled; `Study.measurements` in `src/study.rs`. Why: [decisions/hil-declarations.md](../decisions/hil-declarations.md), decisions 99 and 100. What Core computes from it: [hil-reducers.md](hil-reducers.md); what it writes: `measurements.json` in [hil-shapes.md](hil-shapes.md) (Core's M1.7, `tasks/core/132`).

`Study.measurements`: up to 32 `MeasurementDecl`, `[]` when absent. `HOST_TYPE_SCHEMA_VERSION` 22.

| Field | Type | Absent means |
|---|---|---|
| `name` | string, 1 to 32 bytes, unique in the study | refused |
| `reducer` | one of `REDUCER_NAMES`: `count`, `rate`, `min`, `max`, `mean`, `percentile`, `interval`, `value_at_marker` | refused |
| `tap` | `u8`, a `StreamTap.id` of this study | refused |
| `field` | string, a field of the tap's struct layout (header or repeat) | the tap is not a struct, or the reducer reads no values |
| `unit` | one of `UNITS` (the reducers' list) | the reducer reads no values, or the tap carries one (`Samples` in mA, V or mW) |
| `window` | `{percentile?, from_marker?, to_marker?}`, unknown keys refused | `{}` |
| `declared` | `{resolution?, U?, k?, sample_rate_hz?}`, unknown keys refused | the study declares nothing about the input |

**What each reducer takes.** `count`, `rate`: no window, no values (points are counted). `min`, `max`, `mean`: no window, values. `percentile`: `percentile` (0 to 100), values. `interval`: both markers, no values. `value_at_marker`: `from_marker`, values. A key a reducer does not take is refused, and so is one it needs and lacks.

**What Core supplies, not the study:** the window's `from_utc_ms` and `to_utc_ms` (from the capture), every marker's stamp, `by` and `instrument`, and whether a declared `U` is honoured (only for a `dut` value, [02](../../notes/hil/02-study.md)). A declared `U` is expanded at coverage `k` (2 when absent); a reducer takes the standard `U / k`. Every declared value is finite and above zero.

`validate_measurements(&Study)` returns the first refusal, `MeasurementDeclError`, each carrying the declaration's index; `Display` names it.
