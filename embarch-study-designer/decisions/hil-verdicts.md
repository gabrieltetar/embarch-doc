# embarch-study-designer decisions: the HIL verdict rules

**Status:** active, 2026-11-21.

What `tasks/study-designer/086` (the plan's M1.3, `notes/hil/14`) decided building the verdict rules that [03](../../notes/hil/03-test.md), "The verdict" and "The report", fix in prose. The notes are not re-decided: the six verdicts, the severity order, the guard band on both sides, the `2 * max(w, U)` rule and the roll-up are 03's; what follows is where 03 and [hil-shapes.md](../interfaces/hil-shapes.md) were silent.

Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/hil-verdicts.md](../interfaces/hil-verdicts.md). Shapes: [hil-shapes.md](hil-shapes.md), decisions 90 and 91. Versioning: [hil-reducers.md](hil-reducers.md), decision 93.

### 95 — An observation prompt that gets no answer is `inconclusive` with `observation_unanswered`

03 makes a `prompt_timed_out` or `prompt_cancelled` on an observation prompt `inconclusive`, and 084's closed `reason` list had no reason for it (found by 084's reviewer). The reason joins `inconclusive`'s list: `observation_unanswered`, for both outcomes, since to the verdict a person who did not answer and one who cancelled gave the same evidence, none. Any other prompt kind stays `error`, `prompt_not_confirmed`. `hil-shapes.md` is amended in the same commit; no file carries the string yet, so no `schema` bump.

### 96 — The rules are one module behind a `verdicts` feature that needs only `alloc`, versioned by `Rules`

`verdicts = ["alloc"]`, a sibling of `reducers` (decision 92): `Vec` in the output, no `std`. `embarch-core` and `embarch-api` turn it on; no other consumer names it, so all build unchanged. Five rules carry a behaviour version, spelled into `measurements.json`'s `behaviours` beside the reducers': `step_verdict`, `limit_verdict`, `acceptance_width`, `combine`, `requirement`, each at 1. Decision 93's mechanism, adapted: a reducer is one function type, so its `Registry` stores pointers; five rules have five signatures, so `Rules` pins a version per rule and each method dispatches on it by `match`, an unshipped behaviour being `RuleError::UnknownBehaviour`. A change that can alter a result adds the next arm and leaves the old one; a fixture of an old behaviour is not edited. *Rejected:* one `Registry` of boxed closures, which gives up the typed signatures for nothing.

### 97 — The order in which a limit's reasons apply, and the edges of the guard band

03 fixes which results are `inconclusive` and leaves the order. **Evidence first**: a measurement with `incomplete` (`truncated_capture`, then `truncated_reply`, `record_gap`, `parse_failed`) is `inconclusive` with that reason even when its number is far outside the limit, because 03 defines `inconclusive` as "the evidence is incomplete" and a truncated capture's number is not one to fail a DUT on; then `calibration_expired`; then the limit. The first of several evidence defects names the verdict, and a non-finite value is `parse_failed`. **The edges**: the acceptance limit is inside (a result exactly `lo + w` passes), `lo - w` and `hi + w` are inside the band (inconclusive), and a fail is strictly beyond. With `w = 0` that is plain `lo <= value <= hi`. *Assumed:* these edges are a reading of "between its acceptance limit and its tolerance limit", which 03 leaves open at the ends; a change is a new behaviour.

### 98 — The width check and the roll-up: what 03 left open

- **Width.** 03's "a one-sided limit must sit more than `max(w, U)` inside the range its source measures" is read as the distance to the *nearer end*, strict, because a result must be able to land on both sides of a limit's band. A band exactly `2 * max(w, x)` wide is refused ("wider than"). The refusal carries the number it had to exceed and which of `U` or resolution applied.
- **Relayed.** 03 says a relayed manual verdict "never counts in a requirement's verdict or in coverage". The marker is the `relayed` qualifier the entry carries; the roll-up lists them apart and leaves them out of counts and qualifiers.
- **N of M.** "Pass, N of M tests run": `n` is the tests that ran, `m` is `n` plus those `not_selected`; `not_applicable` tests were never owed a run, so they are outside `m`.
- **No test ran, or a skip with no reason**, is `not_verified`: 03 says a requirement with no test run is never a pass, and a skip whose reason is unknown cannot be shown to be no gap.
- **An empty `combine`** is `skipped`, not `pass`.
- **Qualifiers** of a roll-up are those of the tests that *ran*; a skipped test measured nothing to qualify.
- **`requirement` has no `skipped` verdict**: the worst of what ran is never `skipped`, and the all-skipped case is `not_verified`.

### 112 — One run's records become its verdict in `hil_judge`, behind `hil-test`, so Core and `verify` cannot compose the rules twice

EMB-356: the five rules (95 to 98) composed nowhere. **Where:** a new module `hil_judge` behind `hil-test`, not in `verdicts`. A function that reads a `run.json` test entry needs `RunTest`, which is `hil-test`'s, and `hil-test` already implies `verdicts`; moving it into `verdicts` would pull `sha2` and `serde_json` into an `alloc`-only feature (decision 96). `embarch-core` already turns `hil-test` on and `verify` will; `embarch-api` and the UI are unchanged. **What:** `judge_run` (each step through `step_verdict` with a caller-given `Target`; each limit through `limit_verdict`, `w` from the test's decision rule and the measurement's `U`; an observation's choice against `expect`; then `combine`), `judge_test` (the worst run by `combine`, with the counts), `skip` and `unvalidated`. **Choices past the task's text:** a limit with no measurement is `inconclusive`, `record_gap` (a failed step outranks it in the combine); a run's qualifiers come from every measurement it was handed; the reason of a combined verdict is the first item at the worst verdict; an unknown `decision_rule.kind` is an error, not `simple`; `judge_test` returns `TestVerdict {judged, counts}` since `Judged` has no counts. *Plan choice 27 (a different observation choice is `fail`, `limit`) is the owner's to strike*: it is applied here as 03 and the plan state it, and a reversal is a new behaviour of `limit_verdict`'s caller, not an edit.
