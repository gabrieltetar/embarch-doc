# 058 — part_card and mismatch_report answer before an atlas exists

**State:** claimed by agent/atlas/058-part-card-and-mismatch-report-answer-before-an-atlas-exists, 2026-11-10 02:29
**Source:** Linear issue EMB-23
**Issue:** EMB-23
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Before the first `/atlas-build`, `boards/<label>/netlist.json`, `bom.json` and the document manifest already exist, but two lookups give nothing:

- `mismatch_report` (`src/embarch_atlas/query.py`) answers `src: none` and "atlas not found. Run /atlas-build first." whenever `a.atlas` is unset.
- `part_card` finds a part by doc id, part name or document number, but a lookup by a **board MPN** goes through `Atlas.mpn_docs`, which reads an atlas's `pins.json`, and its `board=` section reads the same file, so it answers "(no board ref is mapped to this document)".

Make both answer from what exists. **Direction (decided at the split):** with no `pins.json`, `part_card` resolves an MPN to its documents through `coverage.py` (the one reader of which document covers an MPN: `covering_docs`, `bom_parts`) and takes refs and nets from the netlists; `mismatch_report` runs the checks in `mismatch.py` that need only netlists, the BOM and distillations, and lists the ones it did not run under a "Not run" heading, each with what it lacked (a devicetree, an ELF, a build). Sorting the checks into those two groups is the core of the work: read each check in `mismatch.run` for what it reads.

## Why now

An engineer or agent planning drivers before the first build has the netlists and datasheets but gets no part-to-document or schematic-to-datasheet answer from these two tools, which is the moment that cross-check would set the plan's facts.

## Where to look

- `src/embarch_atlas/query.py` `part_card`, `mismatch_report`, `Atlas.mpn_docs`, `Atlas.pins_json`
- `src/embarch_atlas/coverage.py` `covering_docs`, `coverage_index`, `bom_parts`
- `src/embarch_atlas/mismatch.py` `run`, `Report`, `render`; `src/embarch_atlas/join.py` (makes `pins.json` and `mismatches.json`; `net_trace` already reads netlists through the join at query time)
- `DESIGN.md` "Query surface", "How a session sees the atlas" (the no-atlas placeholder from `atlas/052`)

## Dispatch notes

- Burndown is on: no new numbered decision. The atlas has none; state the rule in `DESIGN.md` "Query surface" in place.
- Both answers keep their `src:` first line, and it must say what they were read from (for example netlists and coverage, no atlas). With an atlas present both answer exactly as today: existing tests stay green unchanged.
- Nothing touches hardware; tests use synthetic netlists and manifests.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own (both made for you); `test_public_guard` must run, not skip.
- No file in `embarch-doc/embarch-atlas/` is in doc-size reserve.

## Done when

- [x] With netlists and a manifest but no atlas, `q part_card <board MPN>` returns the card, and `board=all` lists the refs and nets.
- [x] With the same inputs `q mismatch_report` returns the checks that need no build and a "Not run" list naming each check skipped and what it lacked.
- [x] Both answers start with a `src:` line saying what they were read from; with an atlas present nothing changes.
- [x] `DESIGN.md` states which lookups answer before an atlas exists, and from what.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.

## Done

`Atlas.part_docs()` (query.py) makes the part-to-document join from the netlists and `Coverage.part_docs` when no atlas exists; `part_card` answers a board MPN, `board=` lists refs and nets, and a covered-but-undistilled MPN names the covering file. `mismatch.run_netlist_only(J)` runs `run(..., netlist_only=True)` in memory, writing nothing.

- **Runs without a build:** net name agrees across a board connector, DNI parts on MCU paths, pull rail vs MCU I/O supply, MCU symbol pin name vs datasheet, far-end output level vs MCU pin tolerance (when pin records exist), driver claims vs datasheet (conflict records).
- **Not run (`mismatch.NEEDS_BUILD`, each with what it lacked):** every DT check (pinctrl, polarity, pull, reaches the board, DT use, one owner, binding, driver in the build, EXTI, I2C x4, resistor values, DT comments), open-drain far-end pull (the pull may be a DT flag), reg-* (driver sources), dt-limit-* (devicetree), second look (kept in an atlas).
- `src:` with no atlas: `boards/<labels> netlist.json + BOM + coverage + distillations, no atlas (...)` for the report; `<doc> card ... (no atlas built: ...)` for the card. With an atlas both are unchanged.
- Also: DESIGN.md's no-hint sentence now names `reg_read_bank`.
