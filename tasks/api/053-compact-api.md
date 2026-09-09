# 053 — `embarch-api/interfaces/tools.md` is in reserve after the serial-port-discovery fix

**State:** blocked
**Source:** `api/041`'s fix (correcting the `serial_log` fallback row and adding
the `list_serial_ports` row) crossed the 11,059 B reserve line the same commit;
`DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/interfaces/tools.md
**Size debt due:** 2026-10-05
**In flux:** yes — this is the one-table front-end reference every new tool or
subcommand lands a row in (its own header: "one table, because these are two
front-ends over one implementation"), and it has taken a live edit in each of
the last several units that touched the CLI/MCP surface (`api/036`'s
`dev-bench-hello` row, `api/049`'s schema-version-key note, and now `api/041`'s
`serial_log`/`list_serial_ports` correction). A shortening pass now risks
compacting a row a near-term unit will need to revise again. Unparked once a
unit lands here without adding a new row or correcting an existing one, or once
a mission split (by section — Config/discovery, Build/flash, Dev bench,
Topology, Studies-pointer — already exist as natural seams) is judged safe to
do verbatim.
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

- [ ] `interfaces/tools.md` is clear of the 11,059 B reserve line, or a
      successor confirms `In flux: no` and re-blocks/re-files with a concrete
      compaction plan — most likely a split by section, per the natural seams
      named above.
- [ ] Every `Must not delete:` item above is still readable, wherever it ends up.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
