# api: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-10

### Added
- `ledger-add`, `ledger-show`, `ledger-pending` (CLI and MCP): a per-project hardware test ledger with a computed pending-by-hardware view; `run-study --test` appends a row.
- `embarch-api stack plan|fold|restack` folds review fixes into their commits by blame, backs up every branch, and restacks a PR stack with one atomic leased push.
- api: serial_log takes signal (+port_wait_ms), the preferred form; Core resolves it; project/port stay the fallback (decision 94).
- `embarch-api patches export|import|regroup`: one scratch tree for a west manifest's patch series; fixes fold by blame, regroup proves tree identity. Decision 92.
- `core_state` tool and `core-state` subcommand over Core's POST /live/core-state; `mem_read` shows found/left/halt_count and marks `halted` deprecated (decision 83).
- declare_signal tool and declare-signal --interface take a direct route's USB interface, refused on a via-dev-bench route (embarch-topology decision 46; suite/052).
- `lease_take`/`lease_renew`/`lease_release`/`lease_show` and `EMBARCH_LEASE_TOKEN` sent on every Core call; `status` shows `lease` and `last_images` (decision 90).
- `bench_exchange` / `bench-exchange`: one call runs console commands and returns every listened console as one filtered timeline; times are client-observed, see embarch-api decision 89.
- api: `capture_start`/`capture_read`/`capture_stop` tools and `capture-*` CLI twins over Core's background signal capture ([tools-capture](../embarch-api/interfaces/tools-capture.md)).
- `signal_exchange` and `signal-exchange` take `match_after_echo` (CLI `--match-after-echo false`), so a console with echo off returns at its prompt instead of the timeout.

### Changed
- embarch-api/open.md compacted 4810 B to 3905 B, out of reserve; all 11 known-wrong items and the settled-deferred reasons kept.
- Compacted embarch-api/decisions/client-crate.md out of the size reserve (11581 to 10817 B); cold incident and provenance sentences cut, rules and reversal conditions kept.
- CLI stream listing says "no records found" for a zero-record report, not "0 of 0 records verified"; see tasks/api/141.
- api: a build now waits for, and says it is waiting on, another process building the same project; one build per key across CLI, MCP and UI ([decision 91](../embarch-api/decisions/build.md))
- bench_exchange places lines at Core's first-byte receive times (core 94) when sent, poll time otherwise; time_basis names the basis per signal; client fields are Option (api 89).
- `status` reports `last_images` as null for a Core that predates it, distinct from `[]` (nothing flashed since start); decisions 58, 90.
- serial_log and serial-log carry Core's truncated flag (true marked, absent from an older Core reported as unknown, never false); config.md says flash_format is required for every project.
- `enroll-probe` (CLI and MCP) says when an enrol vacated or displaced a role; the client mirror carries `displaced`, `vacated`, `vacated_kept`.
- api: signal_exchange and signal-exchange now report Core's wire fields (port_lost, echo, port identity, core state); port_lost exits 5; decision 82 amended.
- api: signal-exchange exits 3 (--until never seen), 4 (zero bytes) or 5 (truncated) with a stderr line; new --clean drops escapes, echo and prompt. Decision 82.
- Flash results carry `erased`, the ranges Core blanked; the `erase` description now says it skips option bytes and never chip-erases (core decision 84).
- `embarch-api/open.md` compacted 4714 to 3780 B: answered bullets deleted, their facts homed in `interfaces/config.md` and decision 70.

### Fixed
- api: ledger_pending matches a role-less bench board by its enrolled name, matches instruments, and flags ambiguous needs (decision 98).
- Study stream 404s (data and arrivals) now keep Core's body, naming the declared taps; the unbuilt MCP startup check is retracted from the spec and decisions 14/17 (api/136).
- `study-status --follow` and `study_watch` now end on an unknown study id (error naming it) or an `interrupted` study (own outcome, CLI exit 1) instead of waiting forever.
- An older Core's exchange and flash replies no longer show fabricated written/bytes_read/port_lost/erased values: absent stays absent ([decision 58](../embarch-api/decisions/client-crate.md)).
- `list_targets` accepts the shortened `<board>.dts` of a single-SoC board and errors with a per-board reason when every board is dropped, not `targets: []`. Decision 86.
