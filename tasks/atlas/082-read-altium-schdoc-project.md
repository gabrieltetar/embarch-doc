# 082 — Read an Altium project's SchDoc sources into parts, pin nets and variants

**State:** open
**Source:** Fleet Ready issue: the atlas reads schematics only from PDF, so a board definition cannot be checked against the CAD revision released for fabrication when the hardware repository holds only Altium sources at that commit.
**Issue:** EMB-88
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

One `embarch-atlas` command, for example `embarch-atlas cad <project dir | .PrjPcb> [--rev <commit>] [--variant <name>] [--json]`, that reads an Altium project's `.SchDoc` sources and prints its components and per-pin nets, and with `--variant` the parts that variant does not fit. This is the first half of EMB-88; `tasks/atlas/083` diffs the result against a PDF-built atlas.

- **Container.** A `.SchDoc` is an OLE compound document. Read it with `olefile`, a new dependency: an optional extra `cad = ["olefile>=0.47"]`, also added to `dev` so the gate's `uv pip install -e '.[dev,tokens,mcp]'` installs it and its tests run rather than skip. Import it lazily, so the base install still works and the verb without it exits 2 with one line naming the extra. Do not hand-write a compound-file reader.
- **Records** (from the issue, which a working throwaway script confirmed on real files). The `FileHeader` stream holds length-prefixed `|KEY=VALUE|` records: 1 component, 2 pin, 17 power port, 18 port, 25 net label, 27 wire, 34 designator, 41 parameter. Pins and parameters follow `OWNERINDEX`; keep only pins whose `OWNERPARTID` matches the component's `CURRENTPARTID`. Multi-part symbols fold into one physical part, as the PDF ingest folds `U7A`/`U7B`.
- **Connectivity, per sheet.** Wire vertices are joined, as is any point lying on a segment (T-junctions); net labels, power ports and ports attach by location; a pin attaches at either end. Across sheets, join by net name and by port name the way `smartpdf.join_board_nets` does for the PDF, so the two outputs are comparable. Hierarchical sheet entries are out of scope (that question is EMB-112's).
- **Sheets come from the `.PrjPcb`** (`[DocumentN]` entries), not from a directory glob.
- **Variants** live only in the `.PrjPcb`: `[ProjectVariantN]` sections with `VariationN=Designator=…|UniqueId=…|Kind=1` for a part not fitted. Match on the component's unique ID, not its designator, and list a variation whose unique ID no longer exists in the schematic as such rather than dropping it.
- **`--rev <commit>`** reads every file at that commit with `git show <rev>:<path>` (olefile opens bytes). It never checks out, writes or fetches anything in the project directory.
- **Output** uses `boards/<label>/netlist.json`'s component and net shape (`DESIGN.md` "`boards/<label>/netlist.json`") with `method: "altium-schdoc"`, so `083` compares like with like. It writes no atlas state and does not feed `schematic` or `join`: it is rung 1 of the schematic ingest ladder as a cross-check, not a new ingest source.

## Why now

The owner moved EMB-88 to Fleet Ready. `DESIGN.md`'s schematic ingest ladder already reserves rung 1 for a native EDA project ("future adapter"); this is that adapter, read-only.

## Dispatch notes

- **Every format fact you rely on beyond the bullets above is an assumption until a real file confirms it**: the length prefix's width and flag byte, how coordinates and their fractional parts are spelled, where a pin's two ends are. State each in `DESIGN.md` as unverified against a real `.SchDoc`, the way `atlas/080` recorded the Zephyr shell layout. The owner-side debt is one run on a real project.
- **Fixtures are synthetic and generic**: build them in the tests with a small test-only compound-file writer, and treat `olefile` opening them as the check on that writer. Small streams sit in the mini stream under the 4096-byte cutoff, so the writer handles that or the fixture stays above it; say which in the test. Designators, net names and part numbers stay generic; `test_public_guard` must run, not skip.
- One fixture project covers: two sheets joined by a port and by a same-named net label, a T-junction, a power port, a two-part symbol, a pin of a part not in `CURRENTPARTID`, and a variant with one not-fitted part and one variation naming a unique ID that no longer exists.
- CLI only: no MCP tool, so the lookup count stays 23. Add the verb to `DESIGN.md`'s CLI table and ingest ladder, `README.md`, and `embarch-doc/embarch-atlas/design.md`. `embarch-atlas` keeps no numbered decisions.
- No file of this sub-project is in reserve.

## Done when

- [ ] One command lists the components (designator, part number, value, unique ID) and per-pin nets of an Altium project read from its `.SchDoc` files, at the working tree or at `--rev <commit>`.
- [ ] With `--variant <name>` it lists that variant's not-fitted parts, matched by unique ID, and names any variation whose unique ID no longer exists.
- [ ] Tests cover the fixture project above, including a missing `olefile` and an unknown variant name, each refused in one line.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); docs updated, `changelog.d/` fragment dropped.
