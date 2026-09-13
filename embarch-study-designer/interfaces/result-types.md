# embarch-study-designer: the result types

**Status:** active, 2026-09-13. Split out of [types.md](types.md) on 2026-09-13 (`tasks/study-designer/038`) — the results half moved verbatim, not rewritten, per [../../DOC-COMPACTION.md](../../DOC-COMPACTION.md) §3.

Current truth for the authoring types (`Study`/`Step`/`Action`) this split from: [types.md](types.md).

## Results

- **`Provenance { dev_bench_version, firmware_version, dev_bench_source, firmware_source, overrides }`** — what the study ran against, **how each version was established**, and which requirements it was allowed past. The source is `ReportedByDevBench` / `ReportedByOutpost` / `FlashedThisRun` / `Declared`, and **it is not bookkeeping**: a `Declared` version is an assertion nobody checked, and a result rendering it identically to a verified one would reintroduce exactly the mislabelling this exists to close. The bench is always `ReportedByDevBench`, read off the live handshake. `FlashedThisRun` is **structurally impossible for Core to produce alone** and is supplied by the process that sequenced both the flash and the submission.
- **`overrides`** — one entry per requirement this run proceeded past, empty in the normal case, each carrying the subject plus **both strings**. A record rather than a flag, **because neither string is recoverable from the rest of the result**: `requires` never travels into it. A bare boolean would say a rule was bent without saying which or by how far — the same half-answer `Declared` exists to stop this type giving.
- **`StudyResult { study_name, steps, provenance, streams }`** — `steps` is **not guaranteed to match the submitted length**: a failing step with `continue_on_fail` false aborts, leaving a proper prefix. `streams` carries one `StreamRef { name, bytes_written, truncated, records }` per declared tap, **including one that produced nothing** — a missing entry and an empty one are different facts. `records: Option<RecordReport>` is `None` when the study declared no record framing for that tap, and otherwise the checked-vs-declared verdict [taps.md](taps.md) describes (decision 70).
- **`StepResult { step_name, outcome, captured_data?, gatt_services?, security_level?, protocol? }`** — `Outcome` is `Pass`, `Fail { reason }`, or `TimedOut`. `security_level` is populated **for every step, not only a security one**, which is a deliberately larger claim and the one that pays: a disconnect during discovery at L1 and the same failure at L4 are different findings, and nothing in a result could distinguish them before. `None` means there was no connection to ask about, **never that nobody looked**.

`gatt_activity`, `power_samples_ref` and `waveform_ref` were here and are **retired** — see [../decisions/removed.md](../decisions/removed.md).

