# embarch-study-designer: the HIL reducers

**Status:** active, 2026-11-21. Code: `src/reducers.rs`, feature `reducers` (needs `alloc`); fixtures `tests/fixtures/reducers/<name>.json`, tests `tests/reducers.rs`. Why: [decisions/hil-reducers.md](../decisions/hil-reducers.md), decisions 92 to 94. The shape each produces is `measurements.json`'s ([hil-shapes.md](hil-shapes.md)); Core calling them is M1.7, `verify` M1.11.

A reducer is a pure function `fn(&Input) -> Measurement`. `Input`: `points` (`{t_ms, value}`), `markers` (`{name, t_ms, u_ms?}`), `unit` (one of `UNITS`), `u` (standard uncertainty of a sample, `None` undeclared), `clock_u_ms`, `k` (default 2), `incomplete` (what the caller knows), `window` (the parameters below). `Measurement`: `value` (or `null`), `unit`, `uncertainty` (`{U, k, basis: "derived", type_a?}` or `null`), `u_source` (`derived`, `undeclared` or `none`), `method` (`{kind: "reducer", name, behaviour, window}`), `incomplete`. Core adds the keys around it.

`Registry::builtin()` holds every behaviour shipped: `latest(name)`, `behaviours(name)`, `reduce(name, behaviour, input)` (an unshipped one is an error), `reduce_latest`. `NAMES` lists the eight.

**`window` keys** (absent keys omitted): `from_utc_ms`, `to_utc_ms` (inclusive; points outside are ignored), `percentile` (0 to 100), `from_marker`, `to_marker`.

| Reducer | Needs in `window` | Value, unit | `U` and `type_a` |
|---|---|---|---|
| `count` | none | points in the window, `1` | none; `u_source: none` |
| `rate` | both ends, `to > from` | `n / T`, `Hz` | instrument `rate * sqrt(2) * clock_u / T`; type A `sqrt(n) / T` |
| `min`, `max` | none | extreme, input unit | input `u` undivided |
| `mean` | none | mean, input unit | input `u` undivided; type A `s / sqrt(n)` |
| `percentile` | `percentile` | interpolated, input unit | input `u` undivided; type A half the one-sigma order-statistic spread |
| `interval` | `from_marker`, `to_marker` | `to - from`, `ms` | RSS of both stamps' `u_ms` and the clock's |
| `value_at_marker` | `from_marker` | latest sample at or before the stamp, input unit | input `u` undivided |

`U = k * sqrt(instrument^2 + type_a^2)`; an undeclared instrument term gives `uncertainty: null`, `u_source: undeclared`. **Incomplete input**: caller flags are copied and the value still computed; a reducer that cannot compute returns `value: null` with `parse_failed` (empty input, a non-finite sample, a missing marker, a bad window or percentile). Only `count` of nothing is a value, 0.
