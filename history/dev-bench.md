# dev-bench: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Changed
- DOC-COMPACTION §9 pass on dev-bench: SRAM-percentage history and superseded bound sizes dropped from [spec.md](../embarch-dev-bench/spec.md); every open question kept.
- dev-bench open.md and decisions/ble.md cut to their hot half; the 16-byte-boundary diagnosis is now a named rejection.
- dev-bench/open.md trimmed again, to 4843 B, so it clears the pressure threshold rather than sitting on it.
- `embarch-dev-bench`'s 180 KB `design.md` became spec.md, open.md and eight `decisions/<mission>.md` files — 81 KB, all 43 decision numbers intact, no file over 11.8 KB.

### Fixed
- The bench now runs firmware whose version resolves to a real commit (`d599453d`), so `doctor` check 13 passes and a study's result can be tied to a known build again.

### Removed
- Seven resolved open questions in `embarch-dev-bench` §4 — struck-through tombstones for questions closed weeks earlier. A resolved question is history, not an open question.
