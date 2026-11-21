# embarch-study-designer: the HIL verdict rules

**Status:** active, 2026-11-21. Code: `src/verdicts.rs`, feature `verdicts` (needs `alloc`); fixtures `tests/fixtures/verdicts/<rule>.json`, tests `tests/verdicts.rs`. Why: [decisions/hil-verdicts.md](../decisions/hil-verdicts.md), decisions 95 to 98. The strings are [hil-shapes.md](hil-shapes.md)'s, "The six verdicts"; Core calling the rules is the Test phase, `verify` M1.11, the report's rendering M1.9 and M1.10.

Every rule is a pure function of its arguments, reached through `Rules`. **`Rules::latest()`** pins all five rules at their newest behaviour; **`Rules::pinned(&[(name, behaviour)])`** pins what a record's `behaviours` names, and a name or behaviour the crate never shipped is an error `verify` reports as "cannot recompute". `RULE_NAMES` are the keys `measurements.json` carries beside the reducers': `step_verdict`, `limit_verdict`, `acceptance_width`, `combine`, `requirement`, all at behaviour 1.

**`Verdict`** (`pass`, `fail`, `error`, `inconclusive`, `skipped`, `cancelled`), `severity()` (error 5, fail 4, inconclusive 3, cancelled 2, skipped 1, pass 0), **`Reason`** (the closed list, `verdict()` and `is_gap()`), **`Qualifier`** (the twelve, in the order a roll-up lists them; `n_of_m_run` beside `NOfM {n, m}`), **`Judged {verdict, reason?, qualifiers}`**, **`Counts`** (an object keyed by the six strings).

## `step_verdict(target, outcome)`

`Target` is `dut` or `bench` (a bench board or an instrument), which Core derives and no study writes. `StepOutcome` is Core's outcome, `prompt_*` carrying `observation`.

| Outcome | On `dut` | On `bench` |
|---|---|---|
| `pass` | pass | pass |
| `refused_on` | fail, `step_failed` | error, `bench_step_failed` |
| `timed_out`, `until_not_seen` | fail, `step_timed_out` | error, `bench_step_failed` |
| `empty_reply` | error, `empty_reply` | error, `empty_reply` |
| `port_lost` | error, `port_lost` | error, `port_lost` |
| `prompt_timed_out`, `prompt_cancelled` | observation prompt: inconclusive, **`observation_unanswered`**; any other kind: error, `prompt_not_confirmed` (either target) | same |

A failed smoke check is `error`, `smoke_check`, decided by Core's gate and handed to `combine`. `marker_rule` is the fail a marker rule gives; the rule is not this unit's.

## `limit_verdict(value, limit, w, evidence)`

`Limit` is the **tolerance** limit: `band {lo, hi}`, `at_most {max}` or `at_least {min}`. `w` is the guard band's width in the value's unit (`DecisionRule::width(U)`: 0 for `simple`, `w_multiple * U` for `guard_band`; the premade default is 1). The acceptance limit is the tolerance limit moved inward by `w`, never stored. In order, the first that applies:

1. **Evidence**: `evidence.incomplete` holds `truncated_capture`, `truncated_reply`, `record_gap` or `parse_failed` (first in that order): inconclusive with it. A non-finite value or `w`: inconclusive, `parse_failed`.
2. **`calibration_expired`**: inconclusive, `calibration_expired`.
3. **Fail** when the value is beyond the tolerance limit by more than `w`: `value < lo - w` or `value > hi + w`; reason `limit`.
4. **Pass** when the value is inside the acceptance limit, ends included: `lo + w <= value <= hi - w`.
5. **Otherwise inconclusive, `guard_band`**: from the acceptance limit to the tolerance limit, and from it outward to `w` past (`lo - w <= value < lo + w`, and the same at `hi`), **both sides**.

With `w = 0` the guard band is empty: `lo <= value <= hi` passes, anything else fails. A one-sided limit has the band on its one side.

## `acceptance_width(limit, w, source)`

The check made when a test is defined. `Source {range_min, range_max, resolution, u}`. It refuses, and says why: **a band whose width `hi - lo` is not more than `2 * max(w, x)`** (`band_too_narrow`); **a one-sided limit whose distance to the nearer end of the range is not more than `max(w, x)`** (`limit_too_close_to_range`). It runs twice, with `x` the expanded `U` (`basis: uncertainty`) and the resolution (`basis: resolution`), and reports the first refusal with the `needed` it had to exceed. Strict at the edge: a band exactly `2 * max(w, x)` wide is refused. A non-finite number, a negative `w`, `U` or resolution, `lo > hi` or an inverted range is `malformed`. A source with no declared `U`, resolution or range is refused earlier, by name (03); this takes numbers.

## `combine(items)`

Runs into a test, tests into a run's summary: the **worst by severity** (`error > fail > inconclusive > cancelled > skipped > pass`), **`counts`** of every verdict, and the **union of the qualifiers**, each once, in the closed list's order. **An empty list is `skipped`**, never a pass: nothing ran.

## `requirement(tests)`

Rolls a requirement's tests into `{verdict, counts, qualifiers, n_of_m, skipped, relayed_listed_apart}`; `verdict` is `pass`, `fail`, `error`, `inconclusive`, `cancelled` or **`not_verified`**.

1. A test carrying the `relayed` qualifier (a manual verdict entered with the agent's token) is **listed apart** (`relayed_listed_apart`) and counted in nothing.
2. The worst verdict among the tests that **ran** (not `skipped`), by severity; anything worse than `pass` is the requirement's verdict and **outranks `not_verified`**.
3. Else **`not_verified`** when a test was skipped for a **gap** (`hook_unmapped`, `bench_missing`, `requires_not_met`, `stopped_by_error`, `stopped_after_fail`), or a skip names no reason, **or no test ran**.
4. Else **`pass`**. A `not_applicable` or `not_selected` skip sits under it, listed in `skipped`. With `not_selected` tests it reads "N of M tests run": `n_of_m {n: tests that ran, m: n + not_selected}` and the qualifier `n_of_m_run`; `not_applicable` is outside `m`.
5. `qualifiers` are the union of those of the tests that ran.
