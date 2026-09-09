# embarch-ui: interfaces

**Status:** active, 2026-09-09. Split out of [spec.md](spec.md) ([DOC-COMPACTION.md](../DOC-COMPACTION.md) §3) when it reached its size cap — a reference section, not cut. Why: [decisions.md](decisions.md).

## The trace chart

The reference reference-dut capture is the working shape to design against: **147.5 s, 225,606 rows, 112,801 spans, 26 lanes.** Wheel zooms at the pointer, drag pans, the window is clamped to the capture. Lanes scroll vertically with the axis and step row pinned; they can be filtered, hidden and reordered. **What filtering may and may not touch is an invariant and it is stated in [spec.md](spec.md), not here** — a reference file is the wrong home for a fact someone has to hold in their head before they change lane filtering ([DOC-COMPACTION.md](../DOC-COMPACTION.md) §3's hot/cold split; the reasoning is `decisions/trace-chart.md`).

It stays SVG. Sub-pixel spans aggregate into per-pixel occupancy runs per lane, so **the element count is bounded by pixels × lanes, not by the dataset**: ~2,500 rects worst case, 27 ms to redraw. Aggregation is exact — a run splits wherever a gap, a below-resolution flag or an open edge changes.

**That aggregation runs on the server, and the view asks for the window it is about to draw** (decision 18). `GET /api/trace/{study}/{tap}/bins?from&to&width` returns at most `width` runs per lane; the view's own payload carries no spans at all, only each lane's `span_count`. The spans were not part of the payload, they were the payload — 12.6 MB of a 12.6 MB JSON on a reference-shaped capture — so first paint is **12.7 KB + 30.5 KB** and a window costs **1–6 ms** end to end. The browser never draws from a window's bins that is not the window it is drawing.

Two view caps, both served rather than restated (`decisions/trace-view.md` 21, `decisions/study-designer.md` 22): **250,000 rows per view** (`MAX_ROWS`, `TraceView::row_cap`), reported rather than swallowed, and a name-length limit (`MAX_STREAM_NAME_LEN`, `ActionsResponse::max_stream_name_len`) applied where a name is chosen rather than at submit.
