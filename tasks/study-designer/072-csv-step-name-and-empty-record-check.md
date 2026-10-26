# 072 — A sample row cannot shift its CSV's columns, and a record check that checked nothing does not report every record verified

**State:** done on agent/study-designer/072-csv-step-name-and-empty-record-check, 2026-10-26
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-study-designer findings 2 and 3), verified by Opus against embarch-study-designer@b9a2d5df
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26

- **Shared crate.** `embarch-core`, `embarch-api`, `embarch-ui` and `embarch-umbrella` path-depend
  on this crate. Keep the public surface additive. A new error variant on a public enum that a
  consumer matches exhaustively would break that consumer's build, which you may not edit: grep
  the four main checkouts under `/home/gabriel/Github/embarch/` for matches on any enum you extend,
  and if one would break, stop and report it rather than landing a change that turns another
  repo's `main` red. A change to what Core logs or blanks is an inbox drop for `core`, as the task
  says (write it by absolute path: `/home/gabriel/Github/embarch/embarch-doc/inbox/`).
- **Wire schema.** If the change alters any serialized type's shape, check decision 12's bump rule
  (`decisions/versioning.md`) and say whether a bump is owed; a bump is a cross-repo pass and is not
  yours to make — report it.
- **`study-designer/070` landed an hour ago** (`HostStudy`, decision 80, `alloc`-gated tests): run
  `cargo test --all-features` as well as the default, as that unit's gate did.
- **Doc reserve:** `embarch-study-designer/open.md` is in reserve (4,473 / 5,120 B, parked under
  `study-designer/026`) — do not add to it. `decisions/gatt-extract.md` is 11,053 B, **6 B under**
  its 11,059 B reserve line; `decisions/protocols.md` 10,876 B; `interfaces/types.md` 10,707 B;
  `decisions/study.md` 10,658 B. `interfaces/decoders.md` (4.9 K) is where the task says the
  step-name rule goes. If your work pushes any file into reserve, file
  `tasks/study-designer/<next NNN>-compact-study-designer.md` in the same commit
  (`scripts/check-task-numbers.py --next study-designer`).

## What

Two of the crate's outputs claim more than they checked.

**The sample CSV row.** `Sample::to_csv_row` writes `step_name` into the row as given. A step name with a comma, a quote or a newline (for example "wait, then write") gives every sample row of that step one more column than the header, and every column after it in `data.csv`/`waveform.csv` shifts. The crate's sibling renderer refuses such a name (`gatt::csv_escape_ok`). Core blanks it on decoded rows. The sample row does neither. `build_study` checks a step name's length only, so a name typed in the UI reaches the CSV too. One direction: a single crate-level rule for what a step name may contain in a CSV cell, used by both renderers. The worker chooses whether that rule refuses at build or validation time or blanks the cell at render time. Core drops a row when the renderer returns `None`, so a sample-row refusal at render time loses samples.

**The record check.** `verify_records` returns an all-zero report when the framing's `magic` is empty, and `RecordReport::all_verified()` reads `total == verified && leading_bytes == 0` as true for it. Core then logs "every record in this capture verified" and stores the report as `Some`. The `None`-versus-`Some` distinction exists to keep "nobody checked" apart from "all verified". A second path ends the same way: an empty capture with a real magic also reports `total 0, leading 0`, so it reads as all verified, although the doc on the crate's own test says this case is not a false pass. One direction: an empty magic is refused when the study is validated, and a report with zero records does not answer `all_verified()` with true. The worker decides how "zero records" is reported.

## Why now

- `src/sample.rs:98-111` has no escaping and no refusal. Compare `src/gatt.rs:243-249`, and `embarch-core src/study.rs:2901-2904`, which blanks the name "so both rendered files agree on what a legal name is". The sample path at `embarch-core src/study.rs:2988` passes the name straight through. `interfaces/decoders.md` line 19: "this crate refuses to produce a CSV value that would break the column shape rather than quoting it."
- `src/records.rs:98-104` and `:129-131`. The empty capture case is at `:328-338`, whose test asserts the counts but never `all_verified()`. Core's consumer is at `embarch-core src/study.rs:2237-2244`. The UI never writes an empty magic (`embarch-ui src/study_designer.rs:816`), so hand-written study JSON reaches the first path, and any study whose tap captured nothing reaches the second.

## Done when

- [x] A sample whose step name contains a comma, a quote or a newline never produces a row with more columns than `Sample::csv_header()`. A test covers each of the three characters.
- [x] The rule for a step name in a CSV cell is defined once in the crate and used by both the sample and the GATT transcript renderers.
- [x] A study whose `record_checks` carries an empty magic is refused when validated, with a named error.
- [x] Neither an empty magic nor an empty capture yields a report for which `all_verified()` is true. A test covers both.
- [x] If Core's log line or its blanking rule must change to match, an inbox drop for `core` is filed.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated (`interfaces/decoders.md` for the step-name rule), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.

## Result, 2026-10-26

Decision 81 (`decisions/seals.md`). Step name: `sample::csv_cell_ok`, sample row blanks, GATT row refuses, `build_study` refuses (`BuildStudyError::NameBreaksCsv`). Records: `validate_record_checks` / `RecordCheckError::EmptyMagic`; `all_verified()` false when `total == 0`. No serialized shape changed, no schema bump. No consumer matches `BuildStudyError`; `RecordCheckError` is new. Core must call the validator and may delegate blanking: inbox drop `core-call-validate-record-checks-and-csv-cell-ok.md` filed. Hardware debt: none.
