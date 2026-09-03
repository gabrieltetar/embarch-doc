# api: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB — older windows roll into [archive/](archive/).

## 2026-09

### Added
- The six recorded acceptance criteria now have tests: `embarch-api/tests/`, a loopback mock Core, no new dependency. See embarch-api decision 46.

### Fixed
- spec.md claimed the build-log cap keeps head and tail; it has only ever kept the 64 KB tail. Doc corrected, gap logged in open.md.
## 2026-09

### Changed
- `embarch-api`'s 158 KB `design.md` became spec.md, open.md, two `interfaces/` files and six `decisions/<mission>.md` — 71 KB, all 45 decision numbers intact.

### Fixed
- `embarch-api` decisions 31 and 33 were byte-identical — the duplicate created in the very commit that deleted 31, which is why the deletion went unnoticed. One entry now owns both numbers.
