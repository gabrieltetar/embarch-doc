# ui: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- `tests/element_ids.rs` fails on a duplicate or dangling element id in index.html/app.js — `embarch-ui/decisions/wiring.md` decision 24.
- The Trace view drops a stale pre-reset leading prefix and keeps the DUT clock for the rest, in place of refusing that clock for the whole capture. embarch-ui decision 19.
- The Trace view asks for the window it draws, binned server-side, not a 13 MB capture: [decision 18](../embarch-ui/decisions/trace-transfer.md).

### Changed
- Decision 23 (outcome decoder) split verbatim from `decisions/trace-chart.md` into `decisions/outcome-decode.md`, clearing its reserve.
- embarch-ui compacted to spec/decisions/open, 92 KB to 68 KB across 12 files; design.md deleted.

### Fixed
- Fixed stale `embarch-ui` src comments: `study_designer` config doc names decision 14's real behaviour, `logs.rs` says `GET`, dead `milestone-*.md` pointers replaced with live docs.
- embarch-ui/Cargo.toml's comment overstated decision 5: it never links embarch-topology's `hardware` feature, but the crate is in the tree transitively.
- An unrecognised trace-band outcome now fills with `tr-cross`, not `tr-gap` — it no longer claims the firmware lost records.
- One outcome decoder in app.js handles both wire shapes; an unrecognised one now renders visibly wrong, not a pass or neutral.
- `app.js` no longer restates the row cap or the stream-name cap; both are now served fields.
- embarch-ui/spec.md: the Debug tab polls Core's /logs/recent (it never subscribes to /logs/stream), and embarch-topology is linked transitively, software-only.
- The study run badge names the step now running, not the count finished — Core's `current_step` is the index of the last step that finished (ui decision 20).
- The Trace view counts the rows its decoder refused — truncated or malformed — instead of claiming "every row in the capture": embarch-ui/decisions/trace-view.md, decision 10.
