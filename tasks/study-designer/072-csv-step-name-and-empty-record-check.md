# 072 — A sample row cannot shift its CSV's columns, and a record check that checked nothing does not report every record verified

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-study-designer findings 2 and 3), verified by Opus against embarch-study-designer@b9a2d5df
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

Two of the crate's outputs claim more than they checked.

**The sample CSV row.** `Sample::to_csv_row` writes `step_name` into the row as given. A step name with a comma, a quote or a newline (for example "wait, then write") gives every sample row of that step one more column than the header, and every column after it in `data.csv`/`waveform.csv` shifts. The crate's sibling renderer refuses such a name (`gatt::csv_escape_ok`). Core blanks it on decoded rows. The sample row does neither. `build_study` checks a step name's length only, so a name typed in the UI reaches the CSV too. One direction: a single crate-level rule for what a step name may contain in a CSV cell, used by both renderers. The worker chooses whether that rule refuses at build or validation time or blanks the cell at render time. Core drops a row when the renderer returns `None`, so a sample-row refusal at render time loses samples.

**The record check.** `verify_records` returns an all-zero report when the framing's `magic` is empty, and `RecordReport::all_verified()` reads `total == verified && leading_bytes == 0` as true for it. Core then logs "every record in this capture verified" and stores the report as `Some`. The `None`-versus-`Some` distinction exists to keep "nobody checked" apart from "all verified". A second path ends the same way: an empty capture with a real magic also reports `total 0, leading 0`, so it reads as all verified, although the doc on the crate's own test says this case is not a false pass. One direction: an empty magic is refused when the study is validated, and a report with zero records does not answer `all_verified()` with true. The worker decides how "zero records" is reported.

## Why now

- `src/sample.rs:98-111` has no escaping and no refusal. Compare `src/gatt.rs:243-249`, and `embarch-core src/study.rs:2901-2904`, which blanks the name "so both rendered files agree on what a legal name is". The sample path at `embarch-core src/study.rs:2988` passes the name straight through. `interfaces/decoders.md` line 19: "this crate refuses to produce a CSV value that would break the column shape rather than quoting it."
- `src/records.rs:98-104` and `:129-131`. The empty capture case is at `:328-338`, whose test asserts the counts but never `all_verified()`. Core's consumer is at `embarch-core src/study.rs:2237-2244`. The UI never writes an empty magic (`embarch-ui src/study_designer.rs:816`), so hand-written study JSON reaches the first path, and any study whose tap captured nothing reaches the second.

## Done when

- [ ] A sample whose step name contains a comma, a quote or a newline never produces a row with more columns than `Sample::csv_header()`. A test covers each of the three characters.
- [ ] The rule for a step name in a CSV cell is defined once in the crate and used by both the sample and the GATT transcript renderers.
- [ ] A study whose `record_checks` carries an empty magic is refused when validated, with a named error.
- [ ] Neither an empty magic nor an empty capture yields a report for which `all_verified()` is true. A test covers both.
- [ ] If Core's log line or its blanking rule must change to match, an inbox drop for `core` is filed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated (`interfaces/decoders.md` for the step-name rule), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
