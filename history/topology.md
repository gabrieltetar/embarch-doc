# topology: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Changed
- Decision 21 moved verbatim to its own mission file, [decisions/validation.md](../embarch-topology/decisions/validation.md); spec.md compacted 10,239 -> 8,913 B.
- Compacted topology `open.md` and `spec.md`; two settled bullets moved into decisions 18 and new decision 22.
- Dev-bench link resolution measured live with two probes: `link_port_interface` is load-bearing, `guessed_among` is not — [spec.md](../embarch-topology/spec.md).
- embarch-topology compacted to spec/decisions/open, 77 KB to 46 KB across 8 files; design.md deleted.

### Fixed
- embarch-topology: removed all 74 stale `design.md` references and two live-push claims decision 19 had retired.
- `embarch-topology dev-bench` now says when a port was guessed, and `validate` prints `NotEnrolled`'s sentence, not its debug shape.

### Decided
- topology's shared machine-wide storage directory, and why it matches embarch-core's, is now decision 23 instead of a code comment only.
- The nRF54L device-ID address pair is confirmed against real silicon, and the identity gate's mismatch refusal is on record three times — [decision 21](../embarch-topology/decisions/validation.md).
