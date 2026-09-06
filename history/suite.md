# suite: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB — older windows roll into [archive/](archive/).

## 2026-09

### Changed
- The rustfmt reversal condition in [embarch.md](../embarch.md) §5 now says why neither `cargo fmt --check` nor `--all --check` is right on its own.
## 2026-09

### Decided
- rustfmt is not enforced and nobody runs cargo fmt: 81 files / 1,881 lines across six crates, and it decays without a check only protocol §10 can carry. embarch.md §5 has the reversal condition.
## 2026-09

### Changed
- Core's on-disk result layout moved from spec.md §5 to interfaces.md, beside the routes that serve it; study-designer's citation follows.
## 2026-09

### Changed
- suite/features.md is assembled from features.d/ row fragments, and a worker now writes its own inventory row.
## 2026-09

### Added
- Every release workflow now fails before building when `Cargo.toml`'s version disagrees with the pushed tag ([decisions 27, 29](../embarch-umbrella/decisions/release.md)).
## 2026-09

### Changed
- suite/features.md pared back to pointers: every row kept, the cells that restated an owning decision cut.
## 2026-09

### Added
- `history/<scope>.md`, assembled per sub-project from `changelog.d/` fragments by `scripts/build_changelog.py`, capped at 20 KB with older windows rolled to `history/archive/`.

### Removed
- 22 shipped milestone docs and implementation guides, 334 KB. Two open items they alone recorded moved to their design docs' open questions first; 122 dangling file references became milestone names.
