# topology: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- spec.md states what a caller may hold across calls (per-operation only, no cache) — decision 29.
- `validate()` adds `validated_at_utc_ms` alongside the enrolled record's own `confirmed_at_utc_ms` (decision 26).

### Changed
- Topology decision 25 and `classify_chip`'s doc comment no longer claim `embarch-core` stops at nRF54L; core decision 49 matches `nrf54h` too. The two matchers stay separate on purpose.
- embarch-topology's CLI enroll/validate/set-dev-bench-link now refuse when a Core answers (decision 28); local-bootstrap unchanged.
- Decision 23 split from `decisions/crate.md` into `decisions/storage.md`; crate.md 11,474 -> 7,782 B.
- `spec.md` compacted out of reserve; `decisions/validation.md` split verbatim, decision 26 moving to `decisions/validate-timing.md`.
- `embarch-topology/open.md` compacted 5016->3669 B, dropping three items already answered elsewhere.
- crate.md's qualification now says embarch-umbrella/src/token.rs was closed by umbrella/036, not live.
- Decision 21 moved verbatim to its own mission file, [decisions/validation.md](../embarch-topology/decisions/validation.md); spec.md compacted 10,239 -> 8,913 B.
- Compacted topology `open.md` and `spec.md`; two settled bullets moved into decisions 18 and new decision 22.
- Dev-bench link resolution measured live with two probes: `link_port_interface` is load-bearing, `guessed_among` is not — [spec.md](../embarch-topology/spec.md).
- embarch-topology compacted to spec/decisions/open, 77 KB to 46 KB across 8 files; design.md deleted.

### Fixed
- `open.md`'s bullet on caller-side mirrors no longer cites `tasks/topology/020`, which is done.
- `NotFound` names which rule emptied dev-bench's candidate list, leads with the split-host possibility on 0 visible ports, and a declared link serial/interface can be cleared.
- hardware_id.rs: one `classify_chip` fn picks the register pair; unlisted nRF54L names no longer fall through to the classic address (decision 25).
- Decision 18's embarch-ui/Core-client alert lockstep fact, lost in the 015 compaction pass, restored (still true, re-verified in code).
- `detected_by` reports `DECLARED_SERIAL`, not a VID rule, when a direct signal route resolves with the VID gate off (decision 24).
- Decision 23's "unprivileged CLI reads Core's admin-owned file" rationale was wrong; corrected — the shared directory works because it is left unlocked, not locked.
- embarch-topology: removed all 74 stale `design.md` references and two live-push claims decision 19 had retired.
- `embarch-topology dev-bench` now says when a port was guessed, and `validate` prints `NotEnrolled`'s sentence, not its debug shape.

### Decided
- decisions/links.md split verbatim: decision 18 stays there, 17 and 24 moved to decisions/links-port.md.
- `decisions/enrollment.md` split: 20/27 moved verbatim to new `decisions/link-declares.md`, out of reserve.
- Decision 23 cites `embarch-core` decision 53 for the `%ProgramData%\embarch` ACL, replacing the stale deferral.
- `crate.md` decisions 4/8: "sole implementation"/"can't disagree" bound to the crate's own boundary, not callers — a caller can still skip the call (`api/038` found one).
- Decision 24 moved into `decisions/links.md`, beside 17 and 18 it is built on.
- topology's shared machine-wide storage directory, and why it matches embarch-core's, is now decision 23 instead of a code comment only.
- The nRF54L device-ID address pair is confirmed against real silicon, and the identity gate's mismatch refusal is on record three times — [decision 21](../embarch-topology/decisions.md).
