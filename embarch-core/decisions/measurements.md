# embarch-core decisions: Measurements at a study's end

**Status:** active, 2026-11-22 (`tasks/core/132`, the plan's unit M1.7, `notes/hil/14`).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Surface: [../interfaces/measurements.md](../interfaces/measurements.md). Siblings: [signing.md](signing.md) (decision 110, whose record names `measurements.json` as a subject and copies its `behaviours`), [study-record.md](study-record.md). The shape and the reducers are the shared crate's: `embarch-study-designer` decisions 90, 92 to 94, 99 and 100.

### 113 — Core computes a study's declared measurements as it ends, on its own clock, with a marker a line of a `Text` tap

**When.** After the captures close and before the record is signed, so `measurements.json` is a subject. `POST /study` refuses a declaration Core could not compute (`validate_measurements`, beside `validate_record_checks`, as a `400`). A study that declares none gets **no file** and its record's `behaviours` stays `{}`. A run whose measurements cannot be written fails, as one whose record cannot be signed does. **A failed study computes nothing.** Host studies declare none (their type has no `measurements`).

**The clock is Core's receipt stamp, always.** Every point is on `core_rx_utc_ms`, the last column of a rendered capture, never the record's own `rx_utc_ms`: that is the DUT's or dev-bench's clock on a mediated tap (suite decision 3), and a window, a marker and a point must share one clock. Core's stamp is one per read, so several samples of a read share it; that is the resolution of every time here.

**A marker is a line of a `Text` tap.** The first whitespace-delimited word of a line is its name; a marker's stamp is the arrival row (`byte_offset,core_rx_utc_ms,bytes`) covering the line's first byte, after the rebase a rotated capture needs. The earliest line of that name across every `Text` tap of the study is the marker (a console tap and the study's own log tap alike). Its `u_ms` is undeclared, because nothing declares a stamp's uncertainty, so an `interval` reads "U undeclared". A name no line carries gives `value: null` with `parse_failed`, as decision 92 of the crate says. This is the one place a marker is stamped; nothing else produces one.

**The window is the capture's own span:** `from_utc_ms` the first point's stamp and `to_utc_ms` the last's (the run's end where the tap has no point), recorded in `method.window`. `at_utc_ms` is `to`. A `rate` is the reducer's `n / T`, which over a window bounded by two samples reads high by one interval in `n - 1`; the declared-rate check below counts `(n - 1) / T` instead.

**What a tap's capture gives the reducers.** `Samples` and `Struct`: the rendered rows (the struct's declared field is the value; a cell that does not parse is a non-finite point, so `parse_failed`). `GattTranscript`: its rows, valueless (count, rate). `Text`: its stamped lines, valueless. `Raw` and `OutpostTrace`: no points, so a count of one is not invented: `count` reads 0 over nothing, and every other reducer `parse_failed`. `source` is the whole rendered file by `rows`, or by `bytes` where the file is raw or the capture is empty; a rotated capture's rows are numbered over what `read_capture` serves.

### 114 — `by`, `instrument` and `bench_image` come from the tap, and a study's declared `U` is honoured for the DUT's values only

**`by`, `instrument`, `bench_image` come from the tap, never the study.** `GattNotify` and a `Signal` leaving role `dut` are the DUT's word: `by: dut`, `instrument: null`, `bench_image: null`. `PowerFrontEnd`, `GattTranscript`, the dev-bench log, and a `Signal` leaving any other role or a bench board are `by: bench`, `instrument: {name, kind: "board", identity: null}` (`name` dev-bench, the role, or the probe serial; no identity reply is kept to cite), and **`bench_image: unverified` for every one** (milestone 1). A `Signal` Core can no longer resolve is read as the DUT's, the less-trusted reading. No instrument is read by a tap, so `calibration` and `characterisation` are absent: no release ships one.

**What is honoured from the study.** A declared `resolution`, `U` and `k` are honoured **only for a `dut` value**: `resolution` is carried, the reducer takes the standard `U / k` (`k` 2 absent), and where the reducer then states an uncertainty the measurement says **`u_source: study`, `basis: declared`**. For a bench value they are ignored and the value reads `u_source: undeclared`, `uncertainty: null`, `resolution: null`, since nothing characterises the board. `count` keeps `none`. A declared `sample_rate_hz` is honoured for any source.

### 115 — A declared rate is checked against Core's count, `declared_by` carries each declaration's scope, and the file is canonical

**`rate_check`** exists for a measurement that declares a rate: `counted_hz = (n - 1) / T` over the first and last stamp, `agree` when it is within **`tolerance_rel = 0.05 + 2 / (n - 1)`** of the declared rate. The 5 % is the base, and the second term lets each end of the window be a sample out, since a read stamps a whole batch. **[assumed]**, not measured on a bench: it is the rule this unit states, and it widens for short captures rather than refusing them. Fewer than two samples, or a zero window, is `agree: false` with `counted_hz: 0`.

**`declared_by`** has one entry per declaration the value rests on, with the scope the ledger (decision 110) holds: the `signal` a tap reads, the `role` it leaves or `dut` for GATT, and a **`study_value`** (named for the measurement) with the scope of the token that submitted the study, where a declared value or rate was honoured. **A declaration the ledger never saw (made before this Core started) reads `agent`**, the less-trusted reading, never `person`. The DUT image is not repeated per measurement: it is the record's `claimed.build`.

**`incomplete`:** `truncated_capture` where the tap's `StreamRef.truncated`, and `record_gap` where its `record_checks` report is not all verified or a row had no stamp; the reducer adds `parse_failed`.

**The file is canonical:** `serde_json` writes sorted keys, and a whole-number `f64` is written as an integer (`5`, not `5.0`), as RFC 8785 requires. Not covered: a number of 1e15 or more, which no measurement here reaches.

**Measured (113 to 115):** the unit tests over a fixture results directory (the expected file field by field; an uncharacterised bench value; a DUT value's declared `U`; the rate check's agree and disagree; a truncated capture and an unprinted marker; no file when none is declared; the submission refusal). **Not run:** a real study's capture. The declarations a real study makes and the arrival granularity of a real console are unseen.

**Out of scope, stated:** verdicts, `report-data.json` and the publish manifest (M1.8), a `person` measurement (no prompt in a device study), and a marker with a declared `u_ms`.

### 121 — `GET /study/{id}/measurements` serves the file as written, and is lease-open

A finished run's `measurements.json` is served by its own read-only route, unchanged, so a Study's prose can cite it before any publish ([interfaces/measurements.md](../interfaces/measurements.md)). **Refusals are distinct:** `404` unknown run, `409` still running, `422` no file written, `410` files gone; an empty body is never the answer. **Lease list:** `LEASE_OPEN`, beside `/study/{id}/streams` and `/events`: it reads a file already on disk, takes neither `hw_lock` nor a port, and gating it would refuse the very read an agent needs without a bench. **Why not the publish file route:** that serves a name only at a revision `report-data` opened, which is the throwaway publish this removes. **Measured:** unit tests over a fixture run (all four cases and the route sweep); not run against a live Core.

### 141 — The measurements route's `422` carries `code: "no_measurements"`, and serves a host study's file

A host study with a `parse` writes `measurements.json` to the same run directory (decision 131), so the route serves it as it does a device study's; the `422` text no longer says a host study cannot have measurements (it says "a host study with no `parse` step"). The `422` body is JSON `{error, code: "no_measurements"}` so `embarch-api` reads the code, not the sentence (EMB-553). `404`, `409` and `410` stay plain text. Decided 2026-11-25 (`tasks/core/164`).
