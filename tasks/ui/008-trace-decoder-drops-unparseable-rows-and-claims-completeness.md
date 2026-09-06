# Count the rows the trace decoder drops as unparseable, instead of showing "every row in the capture"

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `embarch-ui/spec.md`'s "Unreadable is rendered as unreadable" has one hole
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`src/trace.rs:1306-1307` (a short line → `continue`) and `:1316` (an unparseable `frame_index` →
`continue`) drop rows and count them nowhere. `assets/app.js:3662` then renders "every row in the
capture" whenever `rows_dropped_by_cap == 0` — which is true for a truncated capture whose tail was
silently skipped.

`TraceView` gains a counter for rows the parser refused, alongside `rows_dropped_by_cap` and
`records_lost`, and the Records stat card states it rather than claiming completeness. A capture
with a truncated final write, or any malformed row, reads as "N rows unreadable".

## Why now

`embarch-ui/spec.md`'s Invariants — "**Unreadable is rendered as unreadable**", and a dropped-record
gap "is drawn as a gap", on `embarch-outpost`'s report-the-hole standard. This is the one hole in
that view which nothing reports.

## Done when

- [ ] A `rows_unparsed` (or similarly named) field is populated by **both** `continue` arms and
      serialized.
- [ ] The Records card wording is exact when the count is non-zero and unchanged when it is zero.
- [ ] Tests: a fixture with a truncated last line and one with a bad `frame_index` both report the
      count; the committed clean fixtures still report zero.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
