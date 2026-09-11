# 053 — `embarch-api/interfaces/tools.md` is in reserve after the serial-port-discovery fix

**State:** done — `agent/api/042-signal-and-link-writers` split the file 2026-09-10
**Source:** `api/041`'s fix (correcting the `serial_log` fallback row and adding
the `list_serial_ports` row) crossed the 11,059 B reserve line the same commit;
`DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Size debt due:** 2026-10-05 — **paid**: `tools.md` (4,148 B) plus four new
section files (`tools-discovery.md` 1,457 B, `tools-build-flash.md` 3,044 B,
`tools-dev-bench.md` 3,639 B, `tools-topology.md` 3,035 B), none within a
factor of two of the 12,288 B cap.
**In flux:** no — the mission split named as this task's own unpark clause is
now done (below), each resulting file has real headroom, and this task is
closed. A future tool/subcommand addition lands its row in whichever section
file it belongs to and, if that file runs low, gets its own new compaction
task against that file's own name.
**Must not delete:** the `erase` defaults-false callout and its pointer to
`decisions/tool-wrapping.md` decision 41 (§ "Build and flash"). The
`dev-bench-hello --json` `dev_bench_schema_version`-vs-envelope-`schema_version`
collision note under `dev_bench_hello`'s row (decision 59/60,
`tasks/api/049`'s history). The one-table premise sentence in the header —
losing it would let the CLI/MCP surfaces drift undetected again, the exact
defect `tests/tool_subcommand_parity.rs` exists to catch mechanically but this
doc exists to explain in prose. `api/041`'s own corrected `serial_log` row
(no further fallback to `GET /dev-bench/port` exists) and the new
`list_serial_ports` row (Core's-own-machine framing) — reverting either
reintroduces the exact defect this task's source unit fixed.

## What

`interfaces/tools.md` is now **11,280 B against its 12,288 B cap** — 1,008 B of
headroom, inside the 11,059 B reserve line.

## Why now

`check-doc-size.py --pressure` fails on a file in reserve with no task naming
it, and the commit that spends the reserve is the one that files it
(`DOC-COMPACTION.md` §2). This task is that filing.

## Done when

- [x] `interfaces/tools.md` is clear of the 11,059 B reserve line, or a
      successor confirms `In flux: no` and re-blocks/re-files with a concrete
      compaction plan — most likely a split by section, per the natural seams
      named above.
- [x] Every `Must not delete:` item above is still readable, wherever it ends up.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Closed by `agent/api/042-signal-and-link-writers`, 2026-09-10

A verbatim split by section, exactly the move this task named as its own
unpark clause — done as part of `tasks/api/042`, whose new `declare_signal`/
`list_signals`/`remove_signal`/`dev_bench_link` rows were what would have
blown the file's headroom regardless. `tools.md` is now an index (header,
naming/one-table premise, section links, the global "Error handling"
section); each former section is its own file under `interfaces/`:
`tools-discovery.md`, `tools-build-flash.md`, `tools-dev-bench.md`,
`tools-topology.md` (`interfaces/studies.md` already existed as the
Studies-pointer). Nothing was reworded in the move — every row's text is
copied verbatim, including the three `Must not delete:` items above (the
`erase`/decision-41 pointer and the `dev_bench_hello` schema-version
collision note both landed in `tools-build-flash.md`/`tools-dev-bench.md`
respectively; the one-table premise sentence is now in `tools.md`'s own
header, restated to say it applies across the split rather than to one
file, which is the one line this move could not carry verbatim without
becoming false).
