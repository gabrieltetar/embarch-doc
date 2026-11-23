# 096 — Datasheet translation fills a module pad's port

**State:** open
**Source:** Fleet Ready issue, filed by `atlas/094`'s worker for the translation half its unit left untried
**Issue:** EMB-245
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`atlas/094` gave a module datasheet's `pin` record an optional `port` (the SoC
GPIO port behind a pad, `PA4` or `P1.05`) and made `build_pin_map` give an
unnamed module pad that port, marked `module pad table`. Nothing writes the
field: the `atlas-translate-docs` skill's pin-table step does not know it
exists, so a translated module datasheet carries no `port` and an engineer adds
it by hand or as an `engineer-declared` record. When this is done the skill's
datasheet procedure tells the translator that a module's pad table maps each
pad to an SoC port and to write it as `port` on that pad's `pin` record, in the
normalised form `build_pin_map` reads, keeping the pad's own name in `name` and
the pad number in `pin`. A deterministic check that the field is well-formed,
if the procedure's existing record checks have a place for one, is the
worker's call.

## Where

- `embarch-atlas/skills/atlas-translate-docs/reference/datasheet-procedure.md`:
  the `pin` record and its rules; `SKILL.md` if it summarises the pin table.
- `embarch-atlas/DESIGN.md`: the `pin` row and the module pad-table section,
  wherever they say the field is filled by hand.
- `embarch-doc/embarch-atlas/design.md`.

## Constraints

- **No real module datasheet enters either repo, and nothing is written into a
  client repo or its atlas directory.** If checking one real translation would
  need either, the third box is met by saying why none was run.
- No web fetch for a datasheet.

## Done when

- [ ] The skill's pin-table step writes `port` for each pad of a module's pad
      table, normalised as `build_pin_map` reads it.
- [ ] `DESIGN.md`'s `pin` row no longer says the field is filled by hand only.
- [ ] A translation of one real module datasheet is checked for `port` on its
      pad records, or this file says why none was run.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `DESIGN.md` and `embarch-doc/embarch-atlas/design.md` updated,
      `changelog.d/` fragment dropped, `status.d/` fragment for anything
      suite-level it made false.
