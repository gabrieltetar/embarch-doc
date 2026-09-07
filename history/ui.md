# ui: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- The Trace view drops a stale pre-reset leading prefix and keeps the DUT clock for the rest, in place of refusing that clock for the whole capture. embarch-ui decision 19.
- The Trace view asks for the window it draws, binned server-side, not a 13 MB capture: [decision 18](../embarch-ui/decisions/trace-transfer.md).

### Changed
- embarch-ui compacted to spec/decisions/open, 92 KB to 68 KB across 12 files; design.md deleted.

### Fixed
- `app.js` no longer restates the row cap or the stream-name cap; both are now served fields.
- embarch-ui/spec.md: the Debug tab polls Core's /logs/recent (it never subscribes to /logs/stream), and embarch-topology is linked transitively, software-only.
- The study run badge names the step now running, not the count finished — Core's `current_step` is the index of the last step that finished (ui decision 20).
- The Trace view counts the rows its decoder refused — truncated or malformed — instead of claiming "every row in the capture": embarch-ui/decisions/trace-view.md, decision 10.
