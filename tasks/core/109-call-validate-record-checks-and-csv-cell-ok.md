# 109 — Call the study-designer record-check validation, and delegate step-name blanking to csv_cell_ok

**State:** open
**Source:** study-designer/072 (DeepSeek review findings 2 and 3), inbox drop `core-call-validate-record-checks-and-csv-cell-ok.md`
**Scope:** core
**Hardware:** none
**Owner:** no

## What

study-designer/072 added, additively:
- `embarch_study_designer::validate_record_checks(&study.record_checks) -> Result<(), RecordCheckError>` (refuses an empty magic). Core's `POST /study` pre-flight (next to `validate_taps`, `src/study.rs:383`) must call it and return the Display text as the 4xx. Until it does, a hand-written empty-magic study is still accepted.
- `embarch_study_designer::csv_cell_ok(&str) -> bool`, the single step-name rule (comma, quote, CR, LF). Core's blanking at `src/study.rs:2901-2904` can delegate to it (it also misses CR today). `Sample::to_csv_row` now blanks such a name itself.
- `RecordReport::all_verified()` is now false when `total == 0`. Core's log at `src/study.rs:2238` therefore takes the warn branch for an empty capture or empty magic; check the warn text says "no records found" rather than implying damage. (embarch-api `src/cli.rs:1835` prints "0 of 0 records verified" for the same case; that half is api's and out of scope here: if it reads badly, drop it in `inbox/` for api.)

Line numbers are from the drop and may have moved.

## Why now

study-designer decision 81 (`embarch-study-designer/decisions/seals.md`) refuses an empty magic and a CSV-breaking step name, but the refusal guards nothing until Core calls it at `POST /study`; the study-designer/072 log entry names this as the leg's least-sure point.

## Done when

- [ ] `POST /study` refuses an empty magic with the named error, with a test.
- [ ] Core's step-name blanking uses `csv_cell_ok`.
- [ ] The empty-capture log wording is checked.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
