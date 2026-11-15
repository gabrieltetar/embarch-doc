# notes/atlas: the atlas in planes

The research behind [embarch-atlas-planes-proposal.md](../../embarch-atlas-planes-proposal.md): the atlas reorganised into **planes**, each a source of truth with its own version and its own update procedure, and **one join that processes the interactions between them**. Gathered in an interview with the owner on 2026-11-15. **Every answer recorded in these files is the owner's, 2026-11-15, unless it sits under Open.**

The atlas as it stands is the `embarch-atlas` repo's `DESIGN.md` and [embarch-atlas/design.md](../../embarch-atlas/design.md); a claim here about the atlas's code or behaviour cites one of them. The HIL side is [notes/hil/](../hil/README.md), whose [04](../hil/04-premade-suites.md#what-the-hil-side-needs-from-the-atlas-rework) lists what it needs from this rework.

## Files

| File | Subtopic |
|---|---|
| [01-planes.md](01-planes.md) | The seven planes, the version key and update procedure of each, where they live, and the principles that change |
| [02-hardware.md](02-hardware.md) | Board revisions, rework overlays and physical units |
| [03-firmware.md](03-firmware.md) | What the firmware does: module cards kept current by range replay |
| [04-platform.md](04-platform.md) | Zephyr, SDK and HAL versions, west patches, upstream known issues |
| [05-design.md](05-design.md) | Linear, PRs, commits and design documents read live through the desk; Slack as a finder that is never cited |
| [06-specifications.md](06-specifications.md) | Datasheets, manuals, errata and standards: what changes in a plane that is already built |
| [07-interfaces.md](07-interfaces.md) | External interfaces: a document that defines one (a client's BLE API) against what the firmware exposes or consumes |
| [08-measured.md](08-measured.md) | Live findings written back with their receipts; Studies and Tests linked, not copied |
| [09-interactions.md](09-interactions.md) | One plane-tagged join, the matrix of plane pairs, and the worked example: a bus the schematic left unconnected |
| [10-running-cost.md](10-running-cost.md) | Where the LLM runs, what each plane costs per update, and what is reused |
| [11-hil.md](11-hil.md) | What the HIL proposal needs from the rework, plane by plane |
| [12-navigation.md](12-navigation.md) | What else is missing, and how a new contributor finds their way |

## Vocabulary

These words mean exactly this in every file here.

- **Plane**: one source of truth about the product, with its own version key and its own update procedure. Seven: specifications, hardware, firmware, platform, design, external interfaces, measured. **Not a graph layer**: `graph.json`'s layers (external, app, middleware, drivers, SoC, components) are depths of one architecture; a plane is where a fact comes from.
- **Version key**: what identifies one state of a plane: a commit, a document's sha256, a board revision and rework set, a Linear issue's `updatedAt`.
- **Entity**: a thing two planes can both name, in the atlas's existing identifiers: a net (with its aliases), a board-qualified refdes or part pin (`A:U3-12`), an MPN, a devicetree node or label, a Kconfig symbol, an MCU pin, a requirement ID, an interface item.
- **Mention**: a design source naming an entity, found by deterministic matching. Free.
- **Claim**: what a source says about an entity (connects to, a value, a direction, a purpose), structured by an LLM on demand, cited, with a provenance class.
- **Interaction check**: a check that reads two or more planes, and declares which.
- **Rework overlay**: a confirmed netlist delta (cut, wire, swap, fit or DNP) on one board revision.
- **Unit**: one physical board, identified by its MCU's unique ID, with its revision and the reworks it carries.
