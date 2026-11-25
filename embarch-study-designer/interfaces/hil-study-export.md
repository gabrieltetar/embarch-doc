# embarch-study-designer: a Study's export and check

**Status:** active, 2026-11-25. Split verbatim from [hil-run.md](hil-run.md) (`run.json`) on 2026-11-25. Part of the HIL file shapes ([hil-shapes.md](hil-shapes.md), the index). Design, not yet code. Choices the notes left open: [decisions/hil-shapes.md](../decisions/hil-shapes.md), 90 and 91.

## A Study's export and check

A Study has **no verdict** (03; 06 check 3). This section fixes what its run exports and what `verify` checks of it. Producers and readers: M1.7 and M1.8 write the data, M1.10 builds the exports and the zip, M1.11 checks.

**A Study run has a run status, not a verdict.** Spelled differently so the two cannot be confused, and carried in the signed record and `report-data.json` as `run_status` *(shape)*:

| `run_status` | When |
|---|---|
| `completed` | Every step, teardown included, has a `Pass` outcome |
| `step_failed` | At least one step's outcome is `Fail` or `TimedOut` (the existing `Outcome`, [result-types.md](result-types.md)) |
| `interrupted` | A Core restart ended it (03, item 9) |
| `cancelled` | It was cancelled |

It is a pure function of `events.json`'s step outcomes, so `verify` recomputes it. **No file of a Study's zip carries a verdict string**, and `report-data.json` has no `tests`, `requirements` or `verdicts` keys; a Study zip that does fails check 3.

**What a Study's run exports**, in the zip: the study file, `events.json`, `measurements.json`, every capture (raw `.bin` and CSV), `report-data.json` (the run's own claims: `run_status`, per-step outcome counts, the unit or declared subject, the attestation label, who gave the go and who published, the revision), the two interop exports, the PDF and its sources, the hash manifest (06, "One zip").

**The two interop exports of a Study** (06 maps verdicts; a Study has none) *(shape)*:

- **JUnit XML**: one `<testsuite name="<slug>">` with one `<testcase name="<step_name>">` per step. A `Pass` step has no child; a `Fail` or `TimedOut` step has `<error type="step_failed">` or `<error type="step_timed_out">`. **No `<failure>` and no `<skipped>`**: a `<failure>` says a requirement failed, and a Study checks none. The suite's properties carry `run_status`, the attestation label and the qualifiers; each measurement is a property `measurement.<name>` of the suite as `value unit ±U (k=…)`, plus its `by`, `bench_image`, `u_source` and `declared_by` scopes.
- **OCP T&V v2.0 JSON Lines**: a run start, one step record per step (`status` COMPLETE or ERROR, `result` NOT_APPLICABLE, the outcome in metadata), one measurement record per measurement carrying value, unit, `U` and the same qualifiers in metadata, and a run end whose `status` is COMPLETE for `completed` and ERROR otherwise. **No PASS or FAIL `result` is written.**

CI therefore gates on a Study only through `step_failed`, `interrupted` or `cancelled`, never on a measured value, since a Study states no limit.

**What `verify` checks of a Study zip** (06's checks, as they apply; the zip has no call log in milestone 1 and its appendix says "no call log"):

| Check | For a Study |
|---|---|
| 0 | Signatures; the study file, every capture, `events.json` and `measurements.json` are subjects of the run's signed record; an unattested key says "origin unattested" |
| 1 | Manifest hashes |
| 2 | Step outcomes re-evaluated from recorded replies with the study file's `until` and `refused_on`; step-time numbers re-parsed with the study file's patterns; every derived measurement recomputed from the raw captures **with the behaviour versions in `behaviours`**; a version `verify` lacks is "not recomputed", never a match; the `incomplete` arrays, `u_source` and `rate_check.agree` recomputed from the captures where the captures decide them |
| 3 | **No verdicts.** `run_status` recomputed from `events.json`; the run's signed record accounts for the study; any verdict key or string fails |
| 4 | The PDF's text, by [hil-pdf.md](hil-pdf.md) |
| 5 | Labels, and the notes' and prose files' hashes against Core's record |
| 6 | `report-data.json` recomputed from the signed records and the run log's segment; every count, label and fixed statement in the PDF matches it |
| 7 | JUnit and OCP T&V regenerated from the signed records match the zip's |
| 8 | The run log's chain, from the segment's first entry to its signed head; the call log's half is absent from a zip before the Live phase |
| 9 | The syntax-tree whitelist of `report.typ`; Typst packages hashed against the release's or the checkout's list |

**What a Study's `verify` reports it cannot recompute**: the DUT image (a claim; no readback path in milestone 1), a bench board's image (`unverified`), an instrument's `*IDN?`, the identities, an `analysis`-tagged number, and every `dut`-resting value's `by` (06's list, 14's first-milestone form).
