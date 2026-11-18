# 083 — Diff an Altium project's parts and pin nets against a PDF-built atlas

**State:** blocked — waits for the SchDoc reader it compares against.
**Unparks when:** tasks/atlas/082 lands.
**Source:** Fleet Ready issue: a netlist the atlas parsed from a schematic PDF cannot be checked against the CAD revision released for fabrication.
**Issue:** EMB-88
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

One `embarch-atlas` command, for example `embarch-atlas q board-diff --cad <project dir | .PrjPcb> [--rev <commit>] --board <label>` (name and placement to match `082`'s verb), that compares the parts and named pin nets `082`'s reader returns with the `boards/<label>/netlist.json` an atlas built from the same project's PDF, and reports:

- **Parts** present on one side only, and parts whose part number or value differ.
- **Named pin nets** that differ: a pin whose net name differs, and a pin on one side only. A net the PDF left auto-named (`auto: true`) that the CAD names is reported as named by the CAD, not as a difference in its pins.
- **A net renamed after release** — the same pin set under a different name — as a name-only difference, not as every pin moving.
- With `--variant <name>`, a part the variant does not fit that the PDF marks fitted (a PDF never shows variants, so a PDF-built atlas reports every part as fitted); say so in the output rather than as a mismatch per part.

Exit 0 when nothing differs and 1 when something does, so a session can gate on it. It writes no atlas state.

## Why now

Second half of EMB-88, after `082` gives a CAD-side netlist in the PDF netlist's shape.

## Dispatch notes

- Compare through the joined board nets (`aliases` included), never per sheet, so a net the PDF joins through off-sheet ports is one net on both sides.
- Fixtures are synthetic and generic and reuse `082`'s test writer: one CAD project and one `netlist.json` that differ by one part value, one renamed net, one pin moved to another net, and one net the PDF left auto-named. `test_public_guard` must run, not skip.
- CLI only unless a lookup is the natural home: if it goes under `q` and into MCP, update every lookup count and the test that pins the tool count, as `atlas/075` did. Docs: `DESIGN.md`, `README.md`, `embarch-doc/embarch-atlas/design.md`.

## Done when

- [ ] One command reports the parts and named pin nets that differ between an Altium project and an atlas built from the same project's PDF, with a renamed net as a name-only difference.
- [ ] A variant's not-fitted parts are reported against the PDF's all-fitted view.
- [ ] Tests cover the fixture pair above, and a clean pair exits 0.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); docs updated, `changelog.d/` fragment dropped.
