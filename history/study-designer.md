# study-designer: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- study-designer: interfaces/types.md now states Uuid's raw-array Serialize form and where hyphenated text is produced/consumed.
- `BleAddress`'s doc comment now states display order, most-significant first, for both kinds — [interfaces/types.md](../embarch-study-designer/interfaces/types.md).
- First CI for the suite's most depended-on crate: six feature cells per push, the narrow two as `cargo build` since `cargo test` cannot see them ([64](../embarch-study-designer/decisions/ci.md)).

### Changed
- `interfaces/types.md`'s `Results` section moved verbatim to `interfaces/result-types.md`, out of reserve.
- study-designer: `spec.md` §7 host/no_std sizes repointed at decision 63, which already carried them verbatim.
- `decisions/registry.md` hot/cold compacted, 11.8K to 10.1K; `spec.md` now names the custom-action registry.
- embarch-study-designer decisions compacted, 175 KB to 154 KB across 24 files.
- study-designer capacity constants moved to interfaces/limits.md, where a reference belongs.
- `embarch-study-designer`'s 232 KB became spec.md, open.md, five `interfaces/` files and sixteen `decisions/<mission>.md` — 175 KB, all 62 decision numbers intact, no file over 12.2 KB.

### Fixed
- study_builder.rs's 38 decision citations swept (comment-only): 3 wrong numbers fixed (delay_before_ms->42; one embarch-api-mislabelled cite->26; vendor no-schema-bump->41), 0 false sentences.
- `src/lib.rs`'s 41 decision citations checked; two wrong numbers fixed (v12's security_level/pair miscredited to decision 50/51, now 44/50).
- gatt_extract.rs's 36 decision citations swept (comment-only): 3 wrong numbers, 2 false sentences, 0 unlabelled cross-repo cites.
- study.rs's 52 decision citations swept (comment-only): 3 wrong numbers, 1 unlabelled cross-repo cite fixed, 0 false sentences.
- study-designer: `schema_version.rs`'s history swept; one bare `decision 29` was actually `embarch-dev-bench`'s, now labelled.
- `essd_study_decode_full`'s doc comment cited decision 19 for its `steps_crc` check; decision 17 is the one that describes it.
- Forty `§N` citations into the dead 2026-09-02 `design.md` split repointed at live files/decisions or dropped; none changed what a doc says.
- study.rs, result.rs and limits.rs doc comments no longer state removed post-hoc validation as current; citations now point at decision 19's real-time half and decision 48.
- study-designer's own doc comments (README, result.rs, limits.rs) now cite interfaces/result-types.md, not the file 038 moved that content out of.
- `taps.md`/`types.md` now show `StreamRef`'s fourth field, `records`; taps.md no longer says it was refused.
- `interfaces/limits.md` was missing `MAX_BUILD_ID_LEN` (128, `OutpostHeader`'s two build-ID fields); row added.
- `spec.md` §4 now states the real seal order (steps/streams grouped, then protocols); `record_checks` added to both field tables.
- `limits.rs`: `MAX_RECORD_MAGIC_LEN`/`MAX_DECODERS_PER_STUDY` doc comments were spliced together; restored to their own constants.
- `interfaces/limits.md` now lists `MAX_RECORD_MAGIC_LEN`/`MAX_BAD_RECORDS_REPORTED`; a full pass found no further gap.
- `Sample::rx_utc_ms` is bench uptime, not UTC; three contracts claiming a resync no firmware performs are corrected. [Decision 72](../embarch-study-designer/decisions/versioning.md).
- `render_layout` now refuses `repeat` (count_from), `bitpack`, `crc32` and `fixed` by name instead of a silent gap or, for `fixed`, a flat integer.
- study-designer: `open.md`'s power-profiling bullet no longer cites decision 24 (a wire message); no decision records the front-end pick, so it cites none.
- study-designer's README Layout table now lists every module in `src/`, matching the code.
- study-designer: README's Layout/Features sections match Cargo.toml/src/ again, not decision 48's removed `core-validation`.
- study-designer swept all remaining stale `design.md`/`§N.N` citations from `src/`, `Cargo.toml`, `tests/`, `tools/` and its `README.md` (`tasks/study-designer/018`).
- `.eap` source and session-variable errors now report their own declaration line instead of the first `state`'s.
- `MAX_DISCOVERED_SERVICES` row and `src/limits.rs` doc comment now cite decision 57 (3 services, not 2) instead of a stale two-file bounded read.
- `interfaces/limits.md` now lists all 44 `src/limits.rs` constants and fixes two DUT sizing notes it had wrong (2 services, not 3; Sensor Data Service at 7, not Device Management at 8).
- `validate` now refuses two fields of one action sharing a `name` (decision 69).
- `schema_version.rs`'s ten `design.md §3 decision N` citations now use `decision N`/`<repo> decision N`.
- Five stale/broken rustdoc intra-doc links fixed; `cargo doc` stays out of the gate (decision 68).
- Two registry fields covering the same payload byte are refused, and only a `Write` action may carry fields at all (decisions/registry.md 67).
- An over-long registered-action payload says so instead of reporting a step count, and a field's byte range is bounded at registry-validate time (decisions/registry.md 66).
- Two registered actions sharing a name are now refused on load and on save, as duplicate struct layouts already were ([decision 35](../embarch-study-designer/decisions.md)).
- `cargo test --features alloc` did not compile; two tests now use `String::from`, per crate convention.
- `cargo test` no longer aborts: the crate sets a 64 MiB harness stack for the allocator-free shape it tests (decision 63).
- A rustdoc link and two comments still named the retired `MAX_GATT_ACTIVITY_RECORDS`; all three now read as history, and the open question is closed.

### Removed
- `Study.gatt`/`DeclaredGatt` withdrawn from docs as current truth; decision 45 restated as designed-but-unbuilt.

### Decided
- `decisions/declares.md` split: decision 45 (GATT, designed-never-built) moved verbatim to `decisions/declared-gatt.md`, out of reserve.
- Decision 74: `firmware_version` is the bench's build on `HelloAck` and the DUT's on `Requirements`/`Provenance`. Names stay; every reader is told whose build it is.
- Decision 45's GATT table stays designed-but-unbuilt, now on a named trigger; open.md's duplicate bullet struck.
- Every question in `open.md` re-checked against `spec.md`/`decisions.md`: none answered, none struck; the 91.1% size debt stays parked at 2026-10-04.
- This crate does not release: no tags, no version-reading consumer, no artifact — decision 65, with the guard that binds the first `release.yml`.
