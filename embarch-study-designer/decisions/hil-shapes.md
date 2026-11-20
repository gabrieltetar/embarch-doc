# embarch-study-designer decisions: the HIL file shapes

**Status:** active, 2026-11-20.

What `tasks/study-designer/084` (the plan's M1.1, `notes/hil/14`) decided where the HIL notes ([02](../../notes/hil/02-study.md), [03](../../notes/hil/03-test.md), [06](../../notes/hil/06-report-and-publish.md)) were silent. **The notes are the design and the owner's rulings and were not re-decided**: every field name, enum member, rule and number the interfaces cite a note for is the note's. What is listed here is this unit's, **for the owner to see and overturn**.

Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/hil-shapes.md](../interfaces/hil-shapes.md) (the group's index), [hil-run.md](../interfaces/hil-run.md), [hil-pdf.md](../interfaces/hil-pdf.md).

### 90 — The measurement, verdict and characterisation shapes: what the notes left open

None is measured; each is a spelling or a type, chosen so M1.2, M1.3, M1.5 and M1.7 write against one fixed shape. Each is marked *(shape)* in the interface.

- **File conventions.** JSON, `snake_case`, unknown keys refused, a `schema` integer from 1; a hash is lowercase hex SHA-256 over the bytes as written, Core's JSON canonical (RFC 8785, JCS) so a rewrite reproduces it; times are `*_utc_ms` on `rx_utc_ms`'s clock, dates `YYYY-MM-DD` UTC. *Rejected:* a `sha256:` prefix, which a reader would have to strip.
- **Verdict strings and `reason`.** The six are 03's words in lowercase. 03 gives the reasons in prose; the closed lowercase list in the interface is this unit's spelling, with the five "skipped for a gap" reasons split from `not_applicable` and `not_selected` because 03 and 06 treat them differently. Severity is a number (error 5 … pass 0) where a file needs one.
- **Qualifier spellings**: the twelve in 03 and 06 as snake-case strings; `n_of_m_run` carries `n` and `m`.
- **`measurements.json` top level**: `schema`, `run_id`, `behaviours` (name to integer), `measurements`. 02 says the behaviour versions are "written into" the file without a place.
- **`value`** is a number, a string (a `person` choice) or `null` (only with `parse_failed`); **`unit`** a string from a short list with `1` for a pure number; **`at_utc_ms`** is new: 06 checks a calibration due date "against the date of each measurement it made", which needs a time on the measurement.
- **`source`** takes `rows` (0-based inclusive range) or `bytes` (offset and length) for a capture, or `step` (and `iteration`) for a step-time parse out of `events.json`: 02 says "rows or bytes" only.
- **`instrument`** is an object (`name`, `kind`, `identity`, `calibration`, `characterisation`), `null` for `dut` and `person`; `bench_image` is `null` where no board produced the value. 02 says only that `instrument` names the producer.
- **`method`** is `parse`, `reducer` (with the behaviour version and window) or `prompt`.
- **`resolution` and `uncertainty` are `null` when undeclared**, and **`u_source` is always present** with five values (`source`, `study`, `undeclared`, `derived`, `none`); 02 names `u_source` only on a Study's own declarations. `none` marks a quantity with no uncertainty (a count, a choice), told apart from an undeclared one. `uncertainty.basis` has five values: 03's three sources plus `derived`, with `type_a` present on statistical reducers.
- **`rate_check`** is absent unless a declared rate is involved, with `tolerance_rel` recording the tolerance applied; **the tolerance rule itself is M1.7's** and left open.
- **`incomplete`**, an array of `truncated_capture`, `truncated_reply`, `record_gap`, `parse_failed`, is new: 02 says a measurement over a truncated capture "says so" and 03 makes the verdict inconclusive, with no field for it.
- **`declared_by`** is an array of `{what, name, scope}`, `scope` `agent` or `person`; empty means no declaration.
- **A characterisation file**: `board`, `firmware`, `characterised` (a date), `valid_days` (at least 1, the end inclusive), `channels` (`name`, `unit`, `range`, `resolution`, `uncertainty`). 06 asks for a date and a validity period and 03 for resolution, `U` and range, with no spelling. **No milestone-1 unit ships one**, so every Study value from a bench board reads "U undeclared", as 02 already says.

### 91 — `run.json`, a Study's export and the PDF readers: what the notes left open

*Assumed, not measured*: every constant in [hil-pdf.md](../interfaces/hil-pdf.md) (0.5 and 0.3 `size` for the line and word breaks, `TICK_TARGET` 5, the footer band 8 to 15 mm and its 5 mm centring), until M1.9 renders a fixture and M1.11 reads it.

- **`run.json`**: top-level keys (`suite`, `plan_hash`, `standard`, `dut`, `resumes`, `options`, `benches`, `tests`) are 03's list given names; **a template's expansion is one entry per concrete pass, its id suffixed `#<n>`; the study is carried by hash and file name, not inlined; the limits are the tolerance limits and the acceptance limit is derived from them and w**, never stored, so the two cannot disagree. `decision_rule` is `{kind, w_multiple}`.
- **A Study's run has a `run_status`** (`completed`, `step_failed`, `interrupted`, `cancelled`), spelled apart from the six verdicts and a pure function of `events.json`, so `verify` recomputes it. 06 check 3 says a Study has no verdict and defers its "export and check shape" here; this is that.
- **A Study's JUnit and OCP T&V exports** carry steps and measurements with no `<failure>`, no `<skipped>` and no PASS or FAIL result: a Study states no limit. CI can gate on a Study only through `step_failed`, `interrupted` or `cancelled`. *Rejected:* mapping a step's `Fail` to `<failure>`, which would read as a failed requirement.
- **A Study zip carrying a verdict key or string fails check 3**, and `report-data.json` has no `tests`, `requirements` or `verdicts` keys.
- **The text extractor** is specified by contract, not by crate: glyph runs in content-stream order, one unmapped glyph fails check 4, NFKC. M1.11 picks the library.
- **The number grammar** takes `.` as the only decimal mark and no digit-group mark (so `1,234` is two numbers: conservative, a split only adds tokens that must each match), a sign only after a non-alphanumeric, and counts an integer's written digits all significant. A word byte-equal to a `report-data.json` string is opaque first, which is how a hash or date is not read as numbers.
- **`plot_ticks`** is Heckbert's nice-number rounding (thresholds 1.5, 3, 7) with a target of 5 ticks, step in {1, 2, 5} × 10^e, written by integer arithmetic; the set of tick texts of all the report's plots is what check 4 admits. One function in the shared crate serves the helper and `verify`.
- **The footer**: one centred page number added by the compile's own page setup; a `report.typ` footer is refused at publish; at most one run per page is admitted by position.
