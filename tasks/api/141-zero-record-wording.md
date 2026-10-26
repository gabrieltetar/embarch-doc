# 141 — The CLI's "0 of 0 records verified" says nothing was found

**State:** claimed by agent/api/141-zero-record-wording, 2026-10-26 08:11
**Reserve (2026-10-26 08:09 leg):** `embarch-api/decisions/client-crate.md` 707 B left (`api/140` filed),
`embarch-api/open.md` 832 B left (`api/144` filed). If your unit pushes either further into reserve, say
so in your report.
**Source:** core/109 (inbox drop `api-zero-record-wording.md`), following study-designer/072
**Scope:** api
**Hardware:** none — a CLI print, testable on a fabricated report.
**Owner:** no

## What

embarch-study-designer/072 made `RecordReport::all_verified()` false when `total == 0`. embarch-api `src/cli.rs` (~line 1835, may have moved) prints "0 of 0 records verified" for an empty capture or empty magic. Check it reads as "no records found" rather than as damage; reword if not. Core's half (its log text) is done in core/109 (core decision 86).

## Done when

- [x] The zero-record case prints wording that says nothing was found, with a test.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment if reader-facing.

## Done

Wording fix, no decision: `record_summary` in `src/cli.rs` prints `[no records found]` (plus leading bytes if any) when `total == 0`; test `a_zero_record_report_says_no_records_found_not_damage`. No docs made false.
