# suite: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- The fleet ran a study against the real bench and green 2/2; where the DUT half stops is [studies-guide.md](../suite/studies-guide.md) §3a.
- Every release workflow now fails before building when `Cargo.toml`'s version disagrees with the pushed tag ([decisions 27, 29](../embarch-umbrella/decisions.md)).
- `history/<scope>.md`, assembled per sub-project from `changelog.d/` fragments by `scripts/build_changelog.py`, capped at 20 KB with older windows rolled to `history/archive/`.

### Changed
- Suite-wide decisions have a home, `suite/decisions.md`. `embarch.md` §5's rustfmt bullet moved into it verbatim, and §5 reads as five one-line principles again.
- The rustfmt reversal condition in [embarch.md](../embarch.md) §5 now says why neither `cargo fmt --check` nor `--all --check` is right on its own.
- Core's on-disk result layout moved from spec.md §5 to interfaces.md, beside the routes that serve it; study-designer's citation follows.
- suite/features.md is assembled from features.d/ row fragments, and a worker now writes its own inventory row.
- suite/features.md pared back to pointers: every row kept, the cells that restated an owning decision cut.

### Fixed
- Two reachable client-name leaks removed by history rewrite: embarch-api (reintroduced 2026-09-05) and embarch-study-designer (missed by the 2026-09-04 scrub). All ten repos verified clean.

### Removed
- 22 shipped milestone docs and implementation guides, 334 KB. Two open items they alone recorded moved to their design docs' open questions first; 122 dangling file references became milestone names.

### Decided
- rustfmt is not enforced and nobody runs cargo fmt: 81 files / 1,881 lines across six crates, and it decays without a check only protocol §10 can carry. embarch.md §5 has the reversal condition.
