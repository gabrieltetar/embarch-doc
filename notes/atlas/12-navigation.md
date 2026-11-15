# Atlas notes: what else is missing, and finding your way as a new contributor

**Status:** draft, 2026-11-15.

The owner asked, during the interview, whether anything is missing from the atlas beyond the planes and what would make it easier for a new contributor to navigate. **Nothing below is answered yet: the findings are measured or read on 2026-11-15, and every recommendation sits under Open.**

## What a new contributor meets today

- **The design is one file in the code repo**: the `embarch-atlas` repo's `DESIGN.md`, 1,292 lines in 35 headings [measured 2026-11-15]. Owner decisions sit inline with their dates, with no index of them. This repo's [embarch-atlas/design.md](../../embarch-atlas/design.md) is a summary that points back to it. **Every other built sub-project here has four files** (spec, decisions, interfaces, open: [DOC-PROTOCOL.md](../../DOC-PROTOCOL.md) §3), and the atlas repo's own `CLAUDE.md` says `DESIGN.md` moves here once this repo is free to edit.
- **46 modules, about 33,000 lines, in one flat package** (`src/embarch_atlas/`) [measured 2026-11-15]. The CLI table maps verbs to modules; nothing groups the modules by stage or by plane.
- **Checks are named by letter** (G, K, L, E, M, N, R, W, X among them) and by mismatch class, each defined where it was introduced, with no table of them.
- **No recipe for the common changes.** Adding a record kind touches the schema, `doc check`, `render`, `facts.txt`, a lookup and its MCP tool, and the tests that walk the tool list; that list is read from `DESIGN.md`'s structure, not confirmed by doing it.
- **"Interfaces" already means board-to-board mating** (`interfaces.py`, `declare-interface`), a collision with the new external-interfaces plane ([07](07-interfaces.md#open)).
- **The atlas's terms are not in [embarch-glossary.md](../../embarch-glossary.md)**: twins, second look, freeze and thaw, worklist, unit key, the provenance classes.
- **An earlier review walked the engineer's first run, not a contributor's** (the atlas repo's `review/round1/R10-capability-newcomer.md`, finding R10-21): install, `init`, the first build. It proposed a "Before you start" block in the README.

## What else is missing from the atlas

From `DESIGN.md`'s own "Not yet built (deliberately)": a native EDA adapter, geometric tracing as a fallback, the vision rung of the schematic ladder, and a part's package read from the BOM. Its "PRD → code trace links" become design × firmware here ([09](09-interactions.md#the-matrix)). Beyond that list:

- **A schematic that is not an embedded-netlist PDF gives no netlist** (the ladder's rung 2 needs net bookmarks; rung 3 is only a cross-check). A reader for an EDA tool's netlist export would widen hardware intake; the earlier review proposed one (R10-05). Its status is not checked here.
- **No end-to-end example on public data.** The tests hold an upstream Zephyr sample for the code lookups; there is no single command that builds a whole atlas from public fixtures, so a contributor can see every output.

## Open

Recommendations, in the order they would help a newcomer most.

1. **Move the design into this repo's four files as part of the rework**, with the planes as the spec's table of contents: `spec.md` and `spec/<plane>.md`, `decisions.md` with the dated owner decisions pulled out of `DESIGN.md` and numbered, `interfaces.md` (CLI verbs, lookups and MCP tools, `atlas.toml`, the on-disk layout, the record schema), `open.md`. The budget is 10 KB per spec file and 12 KB per interface group ([DOC-BUDGET.md](../../DOC-BUDGET.md)), so the move is also a compaction, not a copy.
2. **A one-screen pipeline map** at the top of the spec: inventory, document prep, records, `doc check`, render, freeze, build, join, MAP and graph, second look, each with its modules and its plane.
3. **A module map grouped by plane**: specifications (`inventory`, `pdftext`, `columns`, `records`, `check`, `render`, `freeze`, `regparse`, `rm`, `svd`, `vote`, `standard`, `coverage`, `missing`, `answers`), hardware (`smartpdf`, `geom`, `interfaces`, `pinnames`, `nettrace`), firmware (`build`, `buildq`, `kconfig`, `dt`, `codeq`, `footprint`, `update`, `bump`), interactions (`join`, `mismatch`, `codecheck`, `limits`, `fwcheck`, `secondlook`, `diff`, `graph`, `mapgen`, `cmsisalias`), measured and live (`live`, `corestate`), surface (`query`, `mcp_server`, `cli`, `project`, `stale`, `common`). Moving the package into sub-packages is a separate, later call: it touches every import and every branch in flight.
4. **A check catalogue** (letter or class, what it compares, planes read, severity, module), rendered from the check registry the plane tags need, so it cannot drift ([09](09-interactions.md#open)).
5. **Contributor recipes**: add a record kind, a check, a lookup, a document kind. Each lists the files it touches and the test that guards it.
6. **The atlas's terms in the suite glossary.**
7. **A public end-to-end example**: one command builds an atlas from public fixtures.
8. **The README's "Before you start" block** from R10-21, for an engineer's first run.
9. **A netlist-export reader** for schematics from other EDA tools.
