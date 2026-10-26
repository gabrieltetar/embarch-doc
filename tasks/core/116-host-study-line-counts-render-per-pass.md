# 116 — Render per-pass line counts for host studies from the raw tap bytes on disk

**State:** open — unparked by the 2026-10-26 08:09 leg: `core/102` landed (`embarch-core` decision 95) and shipped none of the first box. Read the 08:09 note below before starting.
**Update, 2026-10-26 09:03 leg:** the `core/101` dependency the 08:09 note names **has landed** (`embarch-core@0ba23bf`, decision 98). A host study now accepts `Text` + `WholeStudy` direct-signal taps and writes `streams/<name>.txt` verbatim plus a per-line `.arrival.csv` on one study-wide clock, so the "if `core/101` has not landed" branch of that note no longer applies: box 2 is in scope. `line_counts` is still refused at submission until this task lifts it.
**Source:** study-designer/071 (decision 86 in `embarch-study-designer/decisions/host-repeat.md`): `Repeat` and `LineCount` types shipped in `embarch-study-designer`, validated, with no consumer yet. Field use on a USB PD charger board: 34 of 96 bench tests ended in a `grep -c` over a raw console dump. Filed from `inbox/core-host-study-line-count-render.md` by the 2026-10-26 leg.
**Scope:** core
**Hardware:** none
**Owner:** no

## Supervisor note, 2026-10-26 08:09 leg — what `core/102` left, and a new dependency

`core/102` shipped `POST /host-studies` and refuses `Repeat` and `line_counts` with a named `400` at
submission (`embarch-core/decisions/host-study.md`, decision 95). So the first box below is whole.
**A second dependency surfaced at unpark:** decision 95 also refuses a non-empty `streams` until
`tasks/core/101` lands, and a `LineCount` counts lines of a named tap, so an accepted host study has
nothing to count yet. If `core/101` has not landed when you start: ship box 1 (Core runs `Repeat`,
writes markers) and the renderer with its canned two-tap test (boxes 3-4), keep `line_counts`
refused at submission with the refusal naming `core/101`, and leave box 2 open with that reason.
While in `decisions/host-study.md`, its "`HOST_TYPE_SCHEMA_VERSION` stays 19 on this branch" line is
stale: the landing leg bumped it to 20 (`embarch-study-designer@302784c`).

## Supervisor note, 2026-10-26 leg — why blocked, and where the schema bump went

The drop asked Core to accept `HostStudy` *and* carry the `HOST_TYPE_SCHEMA_VERSION` bump. Accepting it is `core/102`'s whole job (`POST /host-studies`), and the bump is not a core worker's to make: the constant lives in `embarch-study-designer/src/schema_version.rs`, so moving it is a cross-repo edit (protocol §8). `core/102` now carries a supervisor note saying the landing leg makes that bump itself. This task keeps only what is new: running `Repeat`, iteration markers, and the per-pass count view.

## What

Core runs `HostAction::Repeat` (substituting `{value}` into `Exchange.line` and `Instrument.line`: the `values` entry, or the 1-based pass number for `count`), and records an `IterationMarker { list, repeat_index, pass, value, started_utc_ms }` as each pass starts, on the same clock as `StreamRecord::rx_utc_ms`. Each inner step's `HostStepResult.iteration` is set.

Then the report view renders each `HostStudy.line_counts` entry: lines of the named tap, split at newlines from the **raw bytes on disk** after the run, counted per pass and over the whole run. `LineCount::count` and `pass_at` in the crate are the counting and bucketing helpers (`std`). A count is **shown, never compared**: no expected value, no pass/fail colouring. A pattern fixed in the study is re-rendered over a finished run without re-running the bench. Lines before pass 1 and after the last pass fall in a "outside any pass" bucket.

## Why now

The count script was one-off bash and could not be rerun with a corrected pattern. The types exist; without Core running them and rendering the counts they are inert. Fixture: `embarch-study-designer/tests/fixtures/host_pd_hard_reset_counts.json` (8 Hard Resets, four patterns, two taps).

## Done when

- [ ] Core runs `Repeat` inside an accepted `HostStudy`, writing iteration markers into the run record.
- [ ] The report view shows each `LineCount` per pass and total, from the raw tap files, rendered again on a finished run.
- [ ] The fixture study renders its eight counts against a canned two-tap capture in a test.
- [ ] A line spanning two records is counted once, not twice (split on newline across record boundaries).
- [ ] Gate green.
