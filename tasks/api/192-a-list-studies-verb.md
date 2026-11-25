# 192 — `embarch-api list-studies` lists Core's retained studies and their taps

**State:** done — list-studies verb shipped, gate green
**Source:** EMB-405 — embarch-api cannot list Core's studies from the command line
**Issue:** EMB-405
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api [--json] list-studies [--limit N]` is a new CLI verb over the
shared client's `CoreClient::list_studies`
(`crates/embarch-core-client/src/client.rs`, `StudyListing`), beside
`list_instruments` in `src/cli.rs` and in `src/main.rs`'s `Commands`. Core's
`GET /studies` already serves every retained study with its taps and takes no
lease; the CLI has `list-study-streams <id>` and `study-status`, and no list.

- **Newest first** by `started_utc_ms`; a study without one comes after those
  that have one, ordered by id. `--limit` keeps the first N after sorting; the
  default is all.
- **The JSON is fixed in `embarch-promptu`'s `docs/contract.md` §15.3**:
  `{"success": true, "keep", "studies": [{"study_id", "study_name", "status",
  "started_utc_ms", "ended_utc_ms", "taps", "note"}]}`. Each tap carries
  Core's `encoding` as it comes (`StreamEncoding` is externally tagged:
  `"OutpostTrace"`, or `{"Samples": {...}}`) and a flat `encoding_kind`
  (`raw`, `text`, `samples`, `gatt_transcript`, `outpost_trace`), so a reader
  never parses the tagged form. `taps` stays null, never empty, where Core
  could not read them. Read §15.3 and follow it where it is more exact than
  this paragraph.
- **The human text**: one line per study (id, name, status, start), its taps
  indented under it.
- **Not an MCP tool**, as the issue states (the verb serves the chat's linker
  and a terminal), and a test says so. Takes no lease, as `GET /studies` needs
  none. Errors in the shape the other list verbs give (`error_result`).

## Why now

EMB-405: the chat linker's captures-and-traces kind (`embarch-promptu` build
step 5) runs `embarch-api --json` verbs and has no way to list a study's taps.
Promptu's contract §15 fixed the shape on 2026-11-25 (`promptu/024`), which was
this issue's blocker.

**Burndown leg: no new numbered decision.** The verb's shape and its not being
an MCP tool are fixed by the issue and the contract; record the verb in
`embarch-doc/embarch-api/`'s spec and interfaces where the CLI's read verbs are
listed. If the work needs a decision neither states, stop and say so in this
file. Decision files within 256 B of their limit: `lease` (#90, over),
`ledger` (#98, 15 B), `bench-exchange` (#89, 122 B), `failure-reporting` (#67,
192 B); do not grow them.

## Done when

- [x] Against a fake Core, `--json list-studies` prints the studies newest
      first, each tap with `encoding` and `encoding_kind`.
- [x] `--limit 2` prints two; a study with no start time comes after those
      with one.
- [x] A study whose taps Core could not read keeps `taps: null`.
- [x] An unreachable Core gives the same error shape `list-instruments` gives.
- [x] The MCP server registers no `list_studies` tool (a test says so).
- [x] `embarch-doc/embarch-api/` says it.
- [x] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment
      dropped.

## Notes

`StreamEncoding` has a sixth variant the contract's `encoding_kind` list lacks: `Struct { decoder }`. It prints `encoding_kind: "struct"` (additive). `embarch-promptu`'s contract 15.3 should add `struct` to its list; no decision was needed.
