# ui: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB — older windows roll into [archive/](archive/).

## 2026-09

### Added
- The Trace view drops a stale pre-reset leading prefix and keeps the DUT clock for the rest, in place of refusing that clock for the whole capture. embarch-ui decision 19.
- The Trace view asks for the window it draws, binned server-side, not a 13 MB capture: [decision 18](../embarch-ui/decisions/trace-transfer.md).

### Changed
- embarch-ui compacted to spec/decisions/open, 92 KB to 68 KB across 12 files; design.md deleted.

### Fixed
- The study run badge names the step now running, not the count finished — Core's `current_step` is the index of the last step that finished (ui decision 20).
- The Trace view counts the rows its decoder refused — truncated or malformed — instead of claiming "every row in the capture": embarch-ui/decisions/trace-view.md, decision 10.
