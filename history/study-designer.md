# study-designer: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB — older windows roll into [archive/](archive/).

## 2026-09

### Decided
- This crate does not release: no tags, no version-reading consumer, no artifact — decision 65, with the guard that binds the first `release.yml`.
## 2026-09

### Added
- First CI for the suite's most depended-on crate: six feature cells per push, the narrow two as `cargo build` since `cargo test` cannot see them ([64](../embarch-study-designer/decisions/crate.md)).
## 2026-09

### Fixed
- `cargo test --features alloc` did not compile; two tests now use `String::from`, per crate convention.
## 2026-09

### Fixed
- `cargo test` no longer aborts: the crate sets a 64 MiB harness stack for the allocator-free shape it tests (decision 63).
## 2026-09

### Changed
- embarch-study-designer decisions compacted, 175 KB to 154 KB across 24 files.
- study-designer capacity constants moved to interfaces/limits.md, where a reference belongs.

### Fixed
- A rustdoc link and two comments still named the retired `MAX_GATT_ACTIVITY_RECORDS`; all three now read as history, and the open question is closed.
## 2026-09

### Changed
- `embarch-study-designer`'s 232 KB became spec.md, open.md, five `interfaces/` files and sixteen `decisions/<mission>.md` — 175 KB, all 62 decision numbers intact, no file over 12.2 KB.
