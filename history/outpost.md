# outpost: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- The reference host decoder now has tests that always run — stdlib `unittest`, no west, no siblings; `run-all.sh` runs them before its west guard.

### Changed
- spec.md 9235 → 8317 B: purpose cut to its three sentences, and the tunables' measured provenance now lives only with the Kconfig symbols in interfaces/integration.md.
- embarch-outpost reduced to its hot half, 69 KB to 46 KB of decisions; cap tightened to 8 KB.
- `embarch-outpost`'s 129 KB `design.md` became spec.md, open.md, two `interfaces/` files and nine `decisions/<mission>.md` — 92 KB, all 21 numbers intact, none over 9.6 KB.

### Fixed
- `tests/vocab_check.py` diffs record kinds and header flags against `src/outpost_priv.h`; see decisions/wire.md decision 23.
- `run-all.sh` runs `cross_decoder.py` above the `WEST` guard now; a skip is restated in the exit summary ([decisions/module.md](../embarch-outpost/decisions/module.md) decision 22).
- wire.md now matches the firmware: `cycles_per_sec` in the header, kinds 9/10 and flag BIT(6); integration.md lists every Kconfig symbol.
- embarch-outpost decision 16 still concluded Phase E needed a wire; it needed the right board target.
- `embarch-outpost` §1/§2 still described record layout 2 ("frame resolution, not cycle resolution") after layout 3 restored the DUT clock; `spec.md` now reflects the current state.
