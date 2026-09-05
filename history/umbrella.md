# umbrella: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB — older windows roll into [archive/](archive/).

## 2026-09

### Changed
- `doctor` check 11 reads the located `embarch-api`'s `versions`, not `embarch`'s own constant; unaskable is its own warn.
## 2026-09

### Changed
- umbrella spec.md, open.md and decisions/doctor.md off their caps; "is it built" now lives once, in spec.md's table.
## 2026-09

### Changed
- Seven `embarch-umbrella` decisions audited against the source: 18, 21, 22, 23, 26, 27/29 and 17's amendment are all unbuilt — [spec.md](../embarch-umbrella/spec.md) claimed four shipped.
## 2026-09

### Changed
- `doctor` check 11 compares real schema versions instead of a hardcoded warn, and new check 15 catches a cross-version stale Core deploy.
## 2026-09

### Changed
- embarch-umbrella compacted to spec/decisions/open, 116 KB to 54 KB; design.md and milestone-6.md deleted.

### Fixed
- Decisions 27 and 29 are one entry an insertion renumbered, not a deletion; same for api 31 and 33.
