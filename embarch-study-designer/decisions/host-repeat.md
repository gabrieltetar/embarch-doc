# embarch-study-designer decisions: Host-run repeat and line counts

**Status:** active, 2026-10-26.

A loop and a count over host-run studies, additive to decision 80 (in [study.md](study.md)).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 86 — `Repeat` and `LineCount`: a loop and a count, with no verdict

Source: field use on the same PD board (34 of 96 bench tests repeated one action 2 to 30 times and reported a count, each a `grep -c` over a raw console dump). Both are additive to decision 80's types.

- **`HostAction::Repeat { count | values, steps }`.** Exactly one of `count` (1 to `MAX_HOST_REPEAT_COUNT`, 100) or a non-empty `values` list. `{value}` in an inner `Exchange.line` or `Instrument.line` is the entry, or the 1-based pass number for `count`. **One level only**; `{value}` outside a repeat is refused, in `steps` and `teardown` alike. Passes times inner steps is capped (`MAX_HOST_EXPANDED_STEPS`, 512) and so is a substituted line (`MAX_HOST_LINE_LEN`, worst case over the actual values), so a submit cannot ask for an unbounded run. The Repeat step's own `timeout_ms` is unused and its `continue_on_fail` does nothing (each inner step's governs); `delay_before_ms` applies once, before pass 1. All caps **assumed**, from field repeats of 2 to 30.
- **Markers in the result type.** `HostStepResult.iteration`, `IterationMarker { list, repeat_index, pass, value, started_utc_ms }` and `HostStudyResult { study_name, steps, iterations }`, with `pass_at` bucketing a timestamp by the markers. The clock is `StreamRecord::rx_utc_ms`'s, so a tap's lines bucket by arrival time.
- **`LineCount { name, tap, pattern, kind }` in `HostStudy.line_counts`.** `kind` is `Substring` (default) or `Regex`. `tap` must name a declared stream and `name` is unique. **No field is an expected value, min or max**: `deny_unknown_fields`, and a test adds five such fields. This keeps 2026-09-25's rule that a study collects and the engineer interprets.
- **The pattern compiles at validate time, under `std` only.** `std` now pulls `regex` (already optional for `gatt-extract`); `alloc` alone cannot compile one, so there a regex is checked non-blank only and Core, a `std` consumer, is where the check bites. `LineCount::count` counts a set of lines for the renderer.
- **Counting is post-run, from the raw bytes on disk** (the owner's 2026-09-25 choice for text taps), so a wrong pattern is fixed by re-rendering, not re-running. Core's renderer is a separate unit (inbox drop).
- **No schema bump**: nothing in `embarch-core`, `embarch-api` or `embarch-ui` references `HostStudy` (grepped 2026-10-26), so `HOST_TYPE_SCHEMA_VERSION` stays 19 on decision 80's reasoning. The unit that accepts `HostStudy` carries the bump.

Fixture `tests/fixtures/host_pd_hard_reset_counts.json`: 8 Hard Resets, a PPS sweep over 7 values (3 steps in place of 14), and four patterns on two taps.
