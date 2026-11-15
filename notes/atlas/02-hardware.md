# Atlas notes: the hardware plane

**Status:** draft, 2026-11-15.

## Today

**One board label, one schematic PDF.** `[[boards]]` names a label and a PDF; `schematic` reads the PDF's embedded netlist and BOM into `boards/<label>/netlist.json` and `bom.json`, keyed by the PDF's sha256, and a changed PDF makes the atlas stale (`embarch-atlas` repo, `DESIGN.md`, "Schematic ingest ladder" and "The stamp"). There is no board revision, no rework and no physical unit.

**Two engineer-owned overlays already exist, and a rework follows their pattern.** `pin_names.json`, written only by `declare-pin-name`, is merged into `netlist.json` with each pin's `name_source`, so a hand-typed name never looks like a printed one; `system.json`'s `interfaces` are never overwritten by a re-run (same doc, "`boards/<label>/netlist.json`").

## Revisions

**Each board carries its revision.** One schematic PDF per revision; `atlas.toml` may declare several revisions of one board label, and the netlist of each is kept apart.

## Rework overlays

**A rework is a netlist delta on one board revision**: a cut (a pin leaves a net), a wire (two pins join a net), a swap (a part's MPN changes), a fit or a DNP (a part enters or leaves the assembly). It is not a new schematic: reworks rarely get one, which is how they stay invisible today.

**The LLM drafts it, the engineer confirms.** A session reads the rework's source (its Linear issue, a rework instruction PDF) and writes the delta as `llm-unverified`, citing that source; the engineer confirms it (`declare-rework --confirm`, by analogy with `declare-pin-name`), which makes it `engineer-confirmed`. The merged netlist says, for every pin a rework changed, which rework changed it.

## Units

**A unit lists the reworks it carries, keyed by its MCU's unique ID.** Core already reads a factory-unique value from the chip when it checks a same-chip link ([embarch-topology spec](../../embarch-topology/spec.md)), so a measurement can name the exact hardware it ran on without anyone typing a serial number.

## Which hardware an atlas joins against

**The target declares its board revisions and rework set**; the stamp records it. **A measurement from a unit with another set is shown as measured on different hardware, never dropped** ([08](08-measured.md)). Chosen over one atlas per distinct unit configuration (exact, but more atlases to build and keep current) and over the newest revision with every rework (wrong for older units still on a bench).

## Open

- **A hardware-only check: a named net with one member, or test points only.** Deterministic and free; it flags a bus left unconnected with no design input at all. Alone it is noisy (some single-pin nets are deliberate), so recommended at `info`, promoted when a design source mentions the net ([09](09-interactions.md#worked-example-a-bus-left-unconnected)).
- **The overlay file.** Recommended: `boards/<label>/reworks.json`, engineer-owned like `pin_names.json`, one entry per rework: id, revision, operations, source cite, `prov`, note. Only confirmed reworks are merged; a drafted one is listed as proposed.
- **A new revision against the old reworks.** Recommended: when a revision's PDF arrives, each confirmed rework of the previous revision is compared with the new netlist and reported as absorbed (the new revision already has it) or still needed. Deterministic.
- **Reading the revision from the PDF.** The doc_id already reads a page-one `REV. A` block (`DESIGN.md`, "Identifiers"); a schematic's title block may give the revision the same way, with `atlas.toml` overriding.
- **Whether Core exposes the unit ID to a client.** Taken from the topology spec, not from the code; checked when the units work starts. Where the unit list lives when planes are shared: recommended in the shared hardware plane.
- **Assembly variants without a rework** (two BOMs on one PCB). Not discussed.
- **Which verb names**: `declare-rework`, `declare-unit`. Placeholders.
