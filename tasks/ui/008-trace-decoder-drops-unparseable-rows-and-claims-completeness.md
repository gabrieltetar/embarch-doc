# Count the rows the trace decoder drops as unparseable, instead of showing "every row in the capture"

**State:** done
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

- [x] A `rows_unparsed` (or similarly named) field is populated by **both** `continue` arms and
      serialized.
- [x] The Records card wording is exact when the count is non-zero and unchanged when it is zero.
- [x] Tests: a fixture with a truncated last line and one with a bad `frame_index` both report the
      count; the committed clean fixtures still report zero.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Shipped

`TraceView::rows_unparsed` (`src/trace.rs`), incremented by both `continue`
arms — a line short of nine fields, and a non-numeric `frame_index` — and
serialized alongside `rows_dropped_by_cap` rather than merged into it: the cap
is this view's own limit on a file it read fine, and this is a file it could not
read. The cap is checked before the line is split, so a row past it is dropped
unread and never counted here.

`assets/app.js`'s Records card composes its subtitle from the two counts and
says "every row in the capture" only when both are zero; a non-zero
`rows_unparsed` also tones the value amber, the way Records-lost already does.

Tests: `a_truncated_or_malformed_row_is_counted_rather_than_vanishing` covers a
capture cut off mid-write, a bad `frame_index`, both together, and a blank
trailing line (absence of a row, not a broken one).
`a_real_capture_decodes_into_lanes` asserts zero on all three committed clean
fixtures.

Gate green: `cargo build`, `cargo test` (98 passed), `cargo clippy --all-targets
-- -D warnings`, `scripts/check-docs.py`, `check-ownership.py --scope ui` on both
repos, `check-client-names.py`.

**Not verified:** the browser half. There is no `node` on this bench and the
render path's only harness is the `#[ignore]`d JSON dump re-evaluated in
headless Firefox by hand (`dump_a_view_for_the_browser_harness`). The Records
card change is three lines of string composition, but nothing here executed it.

Doc-size debt: `decisions/trace-view.md` crossed its reserve line writing this
up; filed as `tasks/ui/009-compact-ui.md` in the same commit, blocked on
`ui/007`.
