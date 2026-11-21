# embarch-study-designer decisions: the HIL reducers

**Status:** active, 2026-11-21.

What `tasks/study-designer/085` (the plan's M1.2, `notes/hil/14`) decided building the built-in reducers that [02](../../notes/hil/02-study.md) fixes by name and by `U` rule. The notes are not re-decided: the eight reducers, the `U` rules and "a statistical reducer returns its type-A term" are 02's; what follows is where 02 was silent.

Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/hil-reducers.md](../interfaces/hil-reducers.md) and [hil-shapes.md](../interfaces/hil-shapes.md). Shapes: [hil-shapes.md](hil-shapes.md), decisions 90 and 91.

### 92 — The reducers are one module behind a `reducers` feature that needs only `alloc`, with its own square root

`reducers = ["alloc"]`: its output holds a `String` and a `Vec`, and nothing in it needs the standard library. `embarch-core` and `embarch-api` (for `verify`) turn `reducers` on; the other three consumers (`embarch-core-client`, `embarch-ui`, dev-bench firmware) never name it, so they build unchanged. *Rejected:* requiring `std`, which would pull `regex` into every build that links the reducers; a `libm` dependency, for one function.

`sqrt` is Newton's method from a bit-pattern guess, using only `+ * /`, each correctly rounded on every target, so a recomputation on any machine agrees to the bit. A test checks it against `f64::sqrt` to 2 ulp. *Assumed, not measured:* the 80-iteration cap is never reached (the loop stops when the guess stops changing; subnormals need the most).

### 93 — Behaviour versions are kept in a registry keyed by name and integer, never replaced

`Registry::builtin()` lists every (name, behaviour) the crate has shipped, each behaviour its own function. A change that can alter a result adds the next integer and **leaves the old function**, so `verify` asks for the behaviour a record names and gets it; one the crate never shipped is `ReduceError::UnknownBehaviour`, which `verify` reports as "cannot recompute", never a substitute. Every reducer ships at behaviour 1. A refactor that cannot change a result does not bump. The fixture of an old behaviour is not edited, so a drift fails a test. The test that proves the contract registers a stand-in behaviour 2 on a copy and checks 1 is unchanged.

### 94 — What 02 left open in each reducer

Inputs carry **standard** uncertainties (`u`); the output is `U = k * u_c` (`k` defaults to 2) from a root sum of squares, as GUM combines. 02 says "`U`", but expanded values do not combine by RSS; this is the reading under which 02's rule is correct. Every reducer output has `basis: derived`.

- **Undeclared input term** (`u` or a stamp's or the clock's `None`): `uncertainty: null`, `u_source: undeclared`. A statistical reducer then loses its `type_a` too, since that lives in the object: a Test refuses an undeclared `U` anyway, and a Study reads "U undeclared".
- **`incomplete`**: what the caller knows (`truncated_capture`, `record_gap`, `truncated_reply`) is copied through and the value is still computed. A reducer that cannot compute (empty input where a value is needed, a non-finite sample, a missing marker, `to` before `from`, a percentile outside 0 to 100, a rate with no two-ended window) returns `value: null` with `parse_failed`, the one value the shape allows null with. A **count** of nothing is 0, complete.
- **count**: points in the window, unit `1`, `u_source: none`. **rate**: points over the window, `n / T`, Hz; needs both window ends. Instrument term `rate * sqrt(2) * clock_u / T` (two stamps bound the window); type A the Poisson `sqrt(n) / T`.
- **min, max, value_at_marker**: take `u` undivided; no type A. The value at a marker is the latest sample at or before the stamp (sample and hold); a sample later than it is never used.
- **mean**: type A `s / sqrt(n)`, `s` the sample deviation (n - 1); 0 for one point.
- **percentile**: linear interpolation at rank `p/100 * (n - 1)`; type A half the spread of the order statistics at `rank +- sqrt(n q (1 - q))`, the distribution-free one-sigma interval of a quantile. *Assumed:* a convention for a quantile's own error, not a measured one; a change is a new behaviour.
- **interval**: `to - from` in ms between the first marker of each name, RSS of the two stamps' `u_ms` and the clock's.
- **Units**: the output unit is the input's except `count` (`1`), `rate` (`Hz`) and `interval` (`ms`); `Unit` in the shape needed no change.
