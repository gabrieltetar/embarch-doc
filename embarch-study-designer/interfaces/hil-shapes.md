# embarch-study-designer: the HIL file shapes (index)

**Status:** active, 2026-11-20. Written by `tasks/study-designer/084`, the plan's unit M1.1 (`notes/hil/14`): the doc R24 asked for, so a Study's zip is not reshaped when Test lands. **Design, not yet code** except two halves: M1.2 built the measurement keys a reducer owns ([hil-reducers.md](hil-reducers.md)) and M1.3 the verdict rules ([hil-verdicts.md](hil-verdicts.md)); the file types and the rest are M1.5 to M1.11's.

Group: this file (verdicts, `measurements.json`) · [hil-characterisation.md](hil-characterisation.md) (a bench board's characterisation) · [hil-run.md](hil-run.md) (`run.json`, a Study's export and check shape) · [hil-pdf.md](hil-pdf.md) (the PDF text extractor and number grammar, built behind `pdf-text`; the tick algorithm and the footer rule are design). Why each open detail went the way it did: [decisions/hil-shapes.md](../decisions/hil-shapes.md), decisions 90 and 91.

Where a note is the source the doc cites it. A value marked *(shape)* is this doc's choice where the notes were silent; each is listed in decision 90 or 91.

## Conventions, all HIL files

- **JSON, UTF-8, no BOM; keys are `snake_case`.** Unknown keys are refused by a reader (as `deny_unknown_fields` does elsewhere in this crate) *(shape)*.
- **Every file carries `schema`: an integer, starting at 1**, bumped when a reader of the old shape would misread the new one *(shape)*.
- **A hash is 64 lowercase hex characters of SHA-256 over the file's bytes as written**, no prefix. A JSON file Core writes is canonical (RFC 8785, JCS) so a rewrite reproduces its hash *(shape)*.
- **Times are `*_utc_ms`: integer milliseconds since the Unix epoch, the clock of `StreamRecord::rx_utc_ms`**; a date is `YYYY-MM-DD`, UTC *(shape)*.
- **Absent and `null` differ, and each field says which it uses.** "Required" means the key is always present; `null` then means "not known or not declared", never "zero".

## Who writes each shape, who reads it

From the plan's table (`notes/hil/14`); a unit written against this group needs no other doc.

| Shape | Written by | Read by |
|---|---|---|
| Verdicts, `run.json` | M1.3 built the rules over them; no milestone-1 unit writes a `run.json` (Test phase) | M1.3, M1.5 (a subject), M1.10, M1.11 |
| `measurements.json` | M1.7 (values and `U` from M1.2) | M1.5 (a subject), M1.9 (`report.typ`), M1.10, M1.11 |
| A Study's export and check | M1.8 (`report-data.json`), M1.10 (the exports, the zip) | M1.11 |
| Extractor, number grammar | the shared crate (M1.2's home) | M1.10 (source rescan), M1.11 |
| Tick algorithm, footer rule | M1.9 (draws them) | M1.11 (derives and checks them) |
| Characterisation | an EmbArch release (none in milestone 1) | M1.7, M1.10 (appendix), M1.11 |

## The six verdicts

From `notes/hil/03-test.md`, "The verdict". The spelling is the string in every file, record and export; **no other string is a verdict** *(shape: lowercase, as the note writes them)*. A Study has none ([hil-run.md](hil-run.md#a-studys-export-and-check)). **How a verdict is reached is built**: [hil-verdicts.md](hil-verdicts.md), `verdicts` feature, decisions 95 to 98.

| String | Means (03) | `reason` values |
|---|---|---|
| `pass` | Every limit held, on every run, on complete evidence | none |
| `fail` | The DUT broke a limit or a marker rule | `limit`, `marker_rule`, `step_failed`, `step_timed_out` |
| `error` | The setup could not judge the DUT: a bench board, an instrument or a port failed, or the smoke check did | `bench_step_failed`, `port_lost`, `empty_reply`, `prompt_not_confirmed`, `smoke_check` |
| `inconclusive` | The evidence is incomplete, or the result is inside a guard band (both sides of the tolerance limit) | `truncated_capture`, `truncated_reply`, `record_gap`, `parse_failed`, `guard_band`, `calibration_expired`, `observation_unanswered` |
| `skipped` | Not run, with the reason | gap: `hook_unmapped`, `bench_missing`, `requires_not_met`, `stopped_by_error`, `stopped_after_fail`; no gap: `not_applicable`, `not_selected` |
| `cancelled` | The run was cancelled | none |

- **`reason` is a closed list of lowercase strings** *(shape)*; a verdict carries one reason where the table lists any, the first that applies in [hil-verdicts.md](hil-verdicts.md)'s order. **Gap versus no gap** is the split 03 and 06 draw for a requirement's `not verified` and the JUnit mapping: the first five `skipped` reasons are gaps *(03's list, spelled here)*.
- **Severity order**, as a number where a file needs one: `error` 5, `fail` 4, `inconclusive` 3, `cancelled` 2, `skipped` 1, `pass` 0 (03). Every combined verdict carries its per-verdict counts, an object keyed by the six strings.
- **A verdict carries its qualifiers**, an array of strings from the closed list in 03 and 06: `bench_firmware_unreleased`, `bench_firmware_unverified`, `bench_firmware_flashed_by_agent`, `unvalidated`, `unit_identity_not_read`, `calibration_undeclared`, `declared_by_agent`, `declared_by_study`, `relayed`, `rests_on_dut_report`, `rests_on_person_observation`, `n_of_m_run` (with `n` and `m` beside it) *(shape: the spellings)*.

## `measurements.json`

Written by Core as each study ends (M1.7, reducers from M1.2), signed as a subject of the run's record (M1.5), and read by `report.typ` (M1.9), the numeric oracle, exports and appendix (M1.10) and `verify` (M1.11). Source: `notes/hil/02-study.md`, "Measurements".

```json
{ "schema": 1, "run_id": "…", "behaviours": { "rate": 1, "mean": 1 },
  "measurements": [ { "name": "rate", "value": 49.8, "unit": "Hz", … } ] }
```

Top level, all required: `schema`; `run_id` (string); **`behaviours`**: an object from every reducer and verdict-rule name used to its integer behaviour version (02: "written into … `measurements.json`") ; `measurements`: an array, in the order the study declared them, names unique within the file.

**One measurement**, every key below always present unless the table says "absent":

| Key | Type | What it holds, and what `null` or absent means |
|---|---|---|
| `name` | string | The study's name for it; what `#m("name")` and `[name]` cite |
| `value` | number, string or `null` | A number; a string for a `person` choice among declared answers; `null` only when `incomplete` holds `parse_failed` |
| `unit` | string | `V`, `mV`, `A`, `mA`, `W`, `mW`, `s`, `ms`, `us`, `Hz`, `B`, `1` (a pure number, a count); a choice has `1` *(shape: the list is the crate's `Unit` widened; M1.2 needed no extension)* |
| `at_utc_ms` | integer | When it was measured; a window's end. What a calibration due date or validity period is checked against *(shape)* |
| `source` | object | `{file, rows? , bytes?, step?}`: `file` a name in the zip; **exactly one of** `rows` `[first, last]` (0-based, inclusive) or `bytes` `[offset, length]` for a capture; `step` (the step's name, and `iteration` if in a `Repeat`) instead of both for a step-time parse out of `events.json` (the step's `parse`, decision 108) |
| `by` | `bench`, `dut` or `person` | Who measured (02). Core fills it from what the step addressed, never from the study |
| `instrument` | object or `null` | `null` for `dut` and `person`. Else `{name, kind (board or instrument), identity, calibration?, characterisation?}`: `identity` the `*IDN?` reply or the board's identity reply (`null` if unread); `calibration` (an instrument) `{serial, certificate_ref, due, declared_by_scope}` or absent when undeclared; `characterisation` (a board) the hash of its file below, or absent when it ships none |
| `bench_image` | `released`, `unreleased`, `unverified` or `null` | The producing board's image status (03). `null` where no bench board produced it. In milestone 1 every board is `unverified` (14) |
| `method` | object | `{kind: "parse", pattern}` (`pattern` the step's `StepParse.pattern`, read by `parse_step_number`, decision 108), `{kind: "reducer", name, behaviour, window}` (the version of `behaviours[name]`; `window` the reducer's own parameters: `from_utc_ms`, `to_utc_ms`, `percentile`, `from_marker`, `to_marker`, absent keys omitted, [hil-reducers.md](hil-reducers.md)) or `{kind: "prompt", prompt_kind}` for a `person` value (`prompt_kind` the prompt's `PromptKind`) |
| `resolution` | number or `null` | In `unit`. `null` is undeclared: a Test refuses it at definition; a Study keeps it and `u_source` says `undeclared` |
| `uncertainty` | object or `null` | `{U, k, basis}`, plus `type_a` (the standard uncertainty of its own estimate, present only on a statistical reducer's value): `U` expanded, in `unit`; `k` the coverage factor; `basis` one of `datasheet`, `calibration`, `characterisation`, `declared`, `derived` *(shape: the list is 03's four sources plus the reducers' derived)*. `null` with `u_source` `none` means a quantity with no uncertainty (a count, a choice) |
| `u_source` | string | **Always present** (02 names it for a Study's own declarations; every value gets one so a reader never infers it) *(shape)*: `source` (the instrument's or board's own declaration), `study` ("declared by the study, unconfirmed"), `undeclared` ("U undeclared"), `derived`, `none` |
| `rate_check` | object or absent | **Absent** unless the value rests on a declared sample rate (02). Else `{declared_hz, counted_hz, window_ms, samples, tolerance_rel, agree}`; `agree` is Core's. The tolerance rule is M1.7's to state; the value it applied is recorded here *(shape: the keys)* |
| `declared_by` | array | One `{what, name, scope}` per declaration the value rests on (`what`: `role`, `signal`, `tap`, `instrument_u`, `study_value`), `scope` the token's scope that made it, `agent` or `person`, from Core's signed record (02). Empty means it rests on none |
| `incomplete` | array of strings | Empty when complete. Else `truncated_capture`, `truncated_reply`, `record_gap`, `parse_failed`: 02's "says so", which makes a verdict resting on it `inconclusive` (03) *(shape: the key)* |

## A bench board's characterisation

Moved verbatim to [hil-characterisation.md](hil-characterisation.md): `characterisation.json`, shipped with a bench board's released firmware, never by a study; nothing in milestone 1 ships one *(shape, decision 90)*.
