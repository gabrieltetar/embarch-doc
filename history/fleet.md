# fleet: history

**Status:** active, 2026-09-05. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB — older windows roll into [archive/](archive/).

## 2026-09

### Added
- `embarch-fleet` gets a suite directory ([spec](../embarch-fleet/spec.md)); `fleet` is refused as a worker scope so the layout does not grant one its own rules.
- `fold-day.py` folds a log day by ledger-checked splice, and an `embarch-log-folder` subagent does it, so a leg pays two lines instead of ~35 K tokens.

### Fixed
- `check-ownership.py` derives its own base — the furthest-forward merge-base — ending three legs of false reds from a stale or unpushed `main`.
