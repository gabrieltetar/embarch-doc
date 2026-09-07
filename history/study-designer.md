# study-designer: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- First CI for the suite's most depended-on crate: six feature cells per push, the narrow two as `cargo build` since `cargo test` cannot see them ([64](../embarch-study-designer/decisions/crate.md)).

### Changed
- embarch-study-designer decisions compacted, 175 KB to 154 KB across 24 files.
- study-designer capacity constants moved to interfaces/limits.md, where a reference belongs.
- `embarch-study-designer`'s 232 KB became spec.md, open.md, five `interfaces/` files and sixteen `decisions/<mission>.md` — 175 KB, all 62 decision numbers intact, no file over 12.2 KB.

### Fixed
- Two registry fields covering the same payload byte are refused, and only a `Write` action may carry fields at all (decisions/registry.md 67).
- An over-long registered-action payload says so instead of reporting a step count, and a field's byte range is bounded at registry-validate time (decisions/registry.md 66).
- Two registered actions sharing a name are now refused on load and on save, as duplicate struct layouts already were ([decision 35](../embarch-study-designer/decisions/registry.md)).
- `cargo test --features alloc` did not compile; two tests now use `String::from`, per crate convention.
- `cargo test` no longer aborts: the crate sets a 64 MiB harness stack for the allocator-free shape it tests (decision 63).
- A rustdoc link and two comments still named the retired `MAX_GATT_ACTIVITY_RECORDS`; all three now read as history, and the open question is closed.

### Decided
- This crate does not release: no tags, no version-reading consumer, no artifact — decision 65, with the guard that binds the first `release.yml`.
