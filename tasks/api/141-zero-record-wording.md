# 141 — The CLI's "0 of 0 records verified" says nothing was found

**State:** open
**Source:** core/109 (inbox drop `api-zero-record-wording.md`), following study-designer/072
**Scope:** api
**Hardware:** none — a CLI print, testable on a fabricated report.
**Owner:** no

## What

embarch-study-designer/072 made `RecordReport::all_verified()` false when `total == 0`. embarch-api `src/cli.rs` (~line 1835, may have moved) prints "0 of 0 records verified" for an empty capture or empty magic. Check it reads as "no records found" rather than as damage; reword if not. Core's half (its log text) is done in core/109 (core decision 86).

## Done when

- [ ] The zero-record case prints wording that says nothing was found, with a test.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment if reader-facing.
