# core: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- `POST /validate` now returns `validated_at_utc_ms` alongside `confirmed_at_utc_ms`, additive.
- `EnrolledBoard`/`Alert` now pin their JSON shape in `embarch-core` against `embarch-api`'s mirror literals, so field drift fails on both sides.
- `GET /status` now serves `core_version`, compiled in from `CARGO_PKG_VERSION`; no `contract_version` beside it (decision 13).

### Changed
- `core`: `decisions/flashing.md` split — backend/vendor-tool decisions (36, 49, 52, 54) moved verbatim to new `decisions/flash-backend.md`.
- `decisions/surfaces.md` split along its enrollment-surface section into `decisions/enrollment.md`, clearing reserve (task 038).
- `embarch-core/open.md` squeezed 4551→3911 B, clear of the 90%-reserve floor.
- Feature inventory: per-caller-identity row now reads Declined (with trigger), not Todo — see `embarch-token.md` §5.
- `spec.md` §5's constants table moved verbatim to `interfaces/constants.md`, clearing the size reserve.
- `GET /serial-log` caps `duration_ms` (400 over it) and captured bytes, reporting `truncated`.
- Core's `decisions/platform.md` split by mission: process/install/locking stay, auth/binding/surface consistency move to [decisions/auth.md](../embarch-core/decisions/auth.md).
- `GET /dev-bench/hello`'s self-reported ID is now `self_reported_hardware_id`, not `hardware_id` — decision 47.
- `interfaces.md` split into `interfaces/<topic>.md`, index-only now, per DOC-COMPACTION.md §3.
- Core's study decisions split by mission: the version gate and handshake identity (31, 35) move verbatim to [decisions/handshake.md](../embarch-core/decisions/handshake.md).
- `embarch-core/open.md` is out of reserve: two bullets restating spec.md and decision 31 are gone, two shortened.
- The bearer-token test sweep now derives its route list from `build_router`'s own source: all 26 routes, not 12 ([decision 42](../embarch-core/decisions.md)).
- Core's spec.md and open.md compacted out of reserve (DOC-COMPACTION §9); no open question dropped.
- embarch-core/open.md compacted off its cap; all 26 questions kept, none answered by the pass.
- `embarch-core`'s 233 KB `design.md` became spec.md (9K), decisions.md (30K), interfaces.md (9K) and open.md (5K) — 53 KB, all 40 decision numbers intact.
- `embarch-core`'s decisions split by mission into seven `decisions/<topic>.md` files (largest 7.7 KB) with `decisions.md` as a 1.6 KB index; all 40 numbers still resolve.

### Fixed
- Decision 56's owed `hardware_id` doc comments landed on the two response types that exist; the third was filed to `embarch-topology`, not invented here.
- `flash_backend.rs`'s `nrfjprog` retirement comment cited decision 50/2026-09-10; corrected to decision 54/2026-09-06.
- `interfaces/studies.md` and `interfaces/result-layout.md` now document `named`, `timed` and `self_excluded` on the stream index — was two of three.
- `open.md`'s auth sweep count fixed from 27 to 26, agreeing with `decisions/auth.md`.
- `POST /validate` (and `flash`/`reset`/`run_study`'s own mid-attach check) now name a detached probe `not_attached`, never `mismatch` (decision 59).
- `embarch-core`: repointed 3 of the 4 flagged miscitations `core/032` left, and normalised the stray `` `decision N` `` form suite-wide.
- core: 170 dead `design.md` comment citations repointed to decisions/spec.md; 5 real miscitations found and flagged in tasks/core/032.
- core: spec.md §4 gains `outpost_manifest.rs`'s row; two `decision 48` and four dead `milestone-N.md` source citations corrected.
- `embarch-core` decision 1/2/7/17's "CI everywhere" clause corrected: no test workflow has ever run in this repo.
- Core's README no longer documents the four removed dev-bench env overrides (decision 23); it points at `embarch-topology` enrollment instead.
- An unrecognised `EMBARCH_FLASH_BACKEND` now names the four valid backends instead of telling you to install a nonexistent tool.
- `embarch-core --version` no longer prints a log warning ahead of the version line on stdout; the diagnostic now actually lands on stderr.
- Core refuses probe-rs for an nRF54H chip name instead of silently permitting it (decision 49).
- `interfaces.md`/`spec.md` now list all 27 routes and 11 CLI subcommands; a pinned count in `api.rs` catches future drift.
- A study stopped by a timed-out step now names that step; "did not arrive" means no step outcome was recorded at all ([decision 45](../embarch-core/decisions.md)).
- `/logs/stream` no longer splits a log line across two SSE frames; its offset advances past a `\n` or not at all (embarch-core decision 44).
- `hw_lock` contention queues silently — decision 14's `503` naming the holder was never built; three docs said it was. See [decisions/platform.md](../embarch-core/decisions/platform.md).
- `chip-list --help` and the `/resolve-chip` 404 now say to edit Core's compiled-in `SOC_TO_CHIP`, not a retired `embarch-api` config key.
- `/study/{id}/events` docs now list `GattTranscript` and note it has no `Last-Event-ID`/replay.

### Removed
- `Backend::NrfJprog` retired — never recorded on any bench. See `decisions/flashing.md` 54.
- `GET /logs/stream` (SSE) is retired — no caller ever existed; `/logs/recent` unaffected.

### Decided
- Every route's wiring is checked against the handler's own `// route:` comment; decision 60.
- Core decision 58: `/serial-log`'s duration/byte caps and `truncated: bool` (not a count) get a numbered rationale; `open.md`'s owed-decision bullet is closed.
- `decisions/surfaces.md`'s decision 54 renumbered to 57 — collided with `decisions/flashing.md` 54.
- Unprefixed `hardware_id` is the probe-read ID suite-wide; decision 47's deferred rename is cancelled, not scheduled. See [embarch-core/decisions/handshake.md](../embarch-core/decisions/handshake.md).
- `study_schema_mismatch` retired: no `code` enum exists in Core to hold it (decisions/surfaces.md 55).
- core/036: no safe 102 B cut found in open.md after core/022; debt stays dated, unpaid.
- core: `hw_lock` contention now refuses `503` naming the holder after 500ms, per decision 14.
- Decision 50's closing paragraph now names each consumer's real end state and points to decision 54.
- Core keeps `confirmed_at_utc_ms` alone on `EnrolledBoardResponse`; decision 54 says label it "Enrolled", never "Validated".
- Decision 53: `%ProgramData%\embarch`'s default ACL stays untightened — deliberate, for `embarch-topology`.
- A study's public `current_step` is the index of the last step that *finished* — stated in [interfaces.md](../embarch-core/interfaces.md), decision 43.
- The `{code, message, cause}` error body is deferred as cross-repo work with a named trigger, not left as pending (decision 12).
