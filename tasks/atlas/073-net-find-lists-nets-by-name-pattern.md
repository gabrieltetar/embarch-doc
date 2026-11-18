# 073 — `net-find` lists nets by name pattern across boards

**State:** done
**Reserve:** no `embarch-atlas` file is in reserve (`check-doc-size.py --pressure`, 2026-11-17 22:58).
**Source:** Fleet Ready issue: a review needed every net matching a name pattern on two boards, with its pins, and `net-trace` takes one exact name.
**Issue:** EMB-96
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

A new lookup, `embarch-atlas q net-find <pattern>`, lists every net whose name matches a pattern across every board of an atlas, one line per net: `<board>:<net>  <ref-pin> <ref-pin> ...`, sorted by board then net name. The pattern is a case-insensitive substring, or a glob when it holds `*`, `?` or `[`. An optional `board=` narrows it to one board. The output shares `net-trace`'s pin format, so a hit can be traced next without reformatting. The same lookup is registered as a read-only tool on the atlas MCP server, and every place that counts or lists the lookups (the atlas-use skill, `DESIGN.md`, the generated `MAP.md` tools line, `embarch-doc/embarch-atlas/design.md`) names it.

## Why now

The owner moved the issue to Fleet Ready. Without the verb an agent writes a script over `boards/<B>/netlist.json` to answer "which nets on these boards belong to this bus family", and grepping `boards/*/nets.md` gives no structured output.

## Done when

- [x] `embarch-atlas q net-find <pattern>` lists every matching net across all boards with board, net name and member pins.
- [x] The same lookup is an MCP tool on the atlas server, registered read-only.
- [x] A test covers a substring match, a glob match, a board filter and a pattern with no matches.
- [x] Every lookup count and list in the repo and in `embarch-doc/embarch-atlas/` agrees with the new count.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet), `changelog.d/` fragment dropped, `features.d/atlas-<NNN>-*` row if it is a user-visible feature.

## Outcome

`nettrace.find` / `query.net_find` / MCP `net_find` / `q net-find`; 19 lookups everywhere. No `features.d` row: no atlas lookup has its own row (the atlas is one inventory row, `not-yet-020`). Pins print as bare `REF-PIN` (the board is on the line), the key form `net_trace` accepts after `<board>:`.
