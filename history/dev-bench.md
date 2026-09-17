# dev-bench: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- The advertiser census now logs Manufacturer Specific Data (company ID + up to 4 payload bytes, capped visibly) alongside name and address (decision 44).

### Changed
- dev-bench/034: wrapped citation census, 23 lines/39 instances, 0 wrong, 2 labels fixed, 1 false sentence fixed.
- A failed `BleConnect` census now counts what it is leaving out (`no name match; 2/10 named: …`), and writes its full per-advertiser log on an address-filtered connect too — decision 46.
- DOC-COMPACTION §9 pass on dev-bench: SRAM-percentage history and superseded bound sizes dropped from [spec.md](../embarch-dev-bench/spec.md); every open question kept.
- dev-bench open.md and decisions/ble.md cut to their hot half; the 16-byte-boundary diagnosis is now a named rejection.
- dev-bench/open.md trimmed again, to 4843 B, so it clears the pressure threshold rather than sitting on it.
- `embarch-dev-bench`'s 180 KB `design.md` became spec.md, open.md and eight `decisions/<mission>.md` files — 81 KB, all 43 decision numbers intact, no file over 11.8 KB.

### Fixed
- Eight remaining files' citation sweep: 139 instances checked, 3 wrong numbers + 12 missing repo labels fixed, 0 false sentences; app/src, app/tests now swept out.
- ble_bridge_real.c/serial_protocol.c citation sweep: 5 wrong decision numbers, 4 false sentences fixed of 100 instances checked; 8 files left (dev-bench/033).
- main.c/serial_protocol.h citation sweep: 158 instances checked, 2 wrong decision numbers fixed, 0 false sentences.
- Three `.eap`/`BleAddress` C comments citing a dead `§N` now cite the owning `embarch-dev-bench` decision (41, 41, 23) instead.
- Four dev-bench files' 122 dead `design.md §3` cites now point at each cited repo's `decisions.md`.
- `ble_bridge_real.c`'s 39 dead `design.md §3` citations repointed to `decisions.md`/decision N, cross-repo form settled in api/052.
- `serial_protocol.h`'s 48 dead `design.md §3` cites now point at each cited repo's `decisions.md`.
- dev-bench: `.eap` trio's dead `design.md §3` cites repointed to `embarch-study-designer` decisions.
- A scan-census overflow no longer hides behind `(truncated)`; both markers write when both conditions hold.
- dev-bench: `fail_reason`'s name-list cut is now marked, and bounded before writing (decisions/scanning.md #45).
- Decision 35 amended: the step-cap removal it claimed never landed; the 16-step ceiling is still live (`decisions/link.md`).
- `embarch-dev-bench` decision 9's `native_sim` CI job is marked never built; this repo has never had a `.github` directory.
- dev-bench README now names the nRF54L15DK as the bench (decision 43), carries `link_port_interface = 2` in the nordic build section, and no longer links `design.md`, deleted by the four-file split.
- `DBM_MAX_INBOUND_FRAME_LEN` in spec.md §5 corrected from a stale 9,415 B to 12,507 B, per the header.
- The bench now runs firmware whose version resolves to a real commit (`d599453d`), so `doctor` check 13 passes and a study's result can be tied to a known build again.

### Removed
- Seven resolved open questions in `embarch-dev-bench` §4 — struck-through tombstones for questions closed weeks earlier. A resolved question is history, not an open question.

### Decided
- dev-bench decision 47: a bare `§N` into a deleted `design.md` resolves to a decision, a live doc, or nothing.
- decisions/ble.md split verbatim by mission: pairing/security stays, addressing/scanning moves to decisions/scanning.md.
