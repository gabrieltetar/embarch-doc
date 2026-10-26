# 086 — The Time chart says when a sample strip or a mark lane is capped

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-ui findings 6 and 15), verified by Opus against embarch-ui@aa5ffdaa
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Two caps in the Time chart drop data without saying so.

**Post-hoc sample strips.** `series_lane` keeps the first `MAX_SERIES_POINTS` (500,000) placeable rows in file order and counts the rest in `dropped_by_cap` (`src/time_chart.rs:1259-1263`). Nothing in `assets/app.js` reads a series' `dropped_by_cap`, and it is not added to `marks_dropped_by_cap` (`:832`), which is the only cap the tab reports (`assets/app.js:9819`). A capped strip therefore just stops partway through the run. Its tooltip (`:9989-9990`) gives the run's total next to the 500,000 as "placeable on this axis", which blames the projection for the cap. The constant's own comment (`:95-97`) says the strip "is drawn from a prefix and says so".

**Live mark lanes after a snapshot.** The browser keeps every mark it is sent (`tcApplyLive`, `:9629-9648`), so during an uninterrupted watch nothing is lost. A snapshot (opening or reloading the tab mid-run) or an epoch bump replaces that with the server's ring, which holds only the last `MAX_LIVE_MARKS` (20,000) per lane (`src/live_study.rs:298`, `:335-346`). The view built from it pins `marks_dropped_by_cap: 0` and never draws a lane's `dropped_by_cap` (`assets/app.js:9681`, `:9689`), so the older marks disappear without a note.

Suggested direction: report every cap where the tab already reports caps, and keep it apart from the "not placeable on this axis" counts. Whether a strip past its cap should be decimated over the whole run, as live series are (decision 31), rather than cut to a prefix is the worker's call, and so is recording that choice.

## Why now

spec/capture-rendering.md:18, "A capped ring says it is capped", and the reason decision 31 gives: "a short feed and a complete one must not look alike". Neither has fired on the bench yet, because no study on Core's disk carries a `Samples` tap (open.md). A 10 kHz rail over a two-minute study, the module's own sizing example, would hit the first.

## Done when

- [ ] A unit test builds a series lane from more than `MAX_SERIES_POINTS` placeable rows. The served view says the strip is capped and by how many, and those rows are not counted as unplaceable.
- [ ] A browser check against `stub_core.py` shows a visible note on a capped strip and on a live lane whose snapshot reported drops. A lane with no drops shows no note.
- [ ] The strip still covers the whole run, or else says which part of the run it covers.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` and `open.md` are in reserve with parked compaction debts (`tasks/ui/078`, `tasks/ui/074`), so prefer `decisions/time-chart.md` or `spec/capture-rendering.md`.
