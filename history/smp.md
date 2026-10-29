# smp: history

**Status:** active, 2026-10-26. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-10

### Fixed
- `embarch-smp` upload now fails with the offsets named when the server's offset moves without progress (8, 16, 8, 16 ...) or keeps restarting at 0, not only when it stands still.

## 2026-09

### Added
- New sub-project, repo created: a Rust port of smpclient, [spec](../embarch-smp/spec.md).
- Ported smpclient 7.3.0: framing, four commands, MCUboot image parse, a simulated serial-recovery bootloader; byte-identical on 18 recorded uploads. [spec](../embarch-smp/spec.md)
