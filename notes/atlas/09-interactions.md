# Atlas notes: interactions between planes

**Status:** draft, 2026-11-15.

## One join, plane-tagged

**The join stays one step; every check declares the planes it reads.** Chosen over one join per plane pair (finer staleness, but more files and states to keep consistent) and over a claims graph that every check queries (most general, and a rewrite of the join).

- **A plane update reruns the whole deterministic join.** It runs no LLM, so rerunning all of it is cheaper than tracking which checks a change touched.
- **LLM-judged comparisons run on demand and are frozen on their inputs' keys**, as second-look verdicts are frozen today (`cache/llm/sl-<key>.json`, `embarch-atlas` repo, `DESIGN.md`, "Caching"). A design claim compared with a netlist is redone only when the claim's source or the netlist changes.
- **Staleness is reported per plane.** The stamp records every plane's version key ([01](01-planes.md#the-atlas-id-and-the-stamp)), so the MAP's stale line and every lookup's `src:` line say which plane moved ("design: 3 issues changed since the join"), not only that the atlas is stale.

## The matrix

| Planes | Checks today | New |
|---|---|---|
| Hardware × specifications | Pin records against the netlist; the MCU symbol against its datasheet; a far-end output level against the pin's tolerance; pulls against the MCU's I/O supply | A reworked part read from its own datasheet |
| Hardware × firmware | pinctrl against net names; devicetree values against the BOM; I2C identity by address strap | Joined against the target's declared revisions and reworks |
| Firmware × specifications | `codecheck`, `limits`, `fw_check` | |
| Specifications × specifications | SVD against the reference manual (`vote`); conflicts | An erratum against the fact it amends |
| **Design × hardware** | None | **A net the design names that the hardware leaves unconnected or lacks** (deterministic); a claim against `net_trace` (on demand) |
| Design × firmware | None | A symbol or node the design names that the build lacks (deterministic); a claim against a module card, the configuration or the devicetree (on demand) |
| Design × specifications | None | A claimed value against a limit or a requirement (on demand) |
| External interfaces × firmware | None | Required items against what the build exposes or consumes ([07](07-interfaces.md)) |
| Platform × firmware | None | A backport the base already carries; a missing erratum workaround ([04](04-platform.md)) |
| Measured × the rest | None | A measured value against the datasheet or the design; a unit's reworks against the target's |

The checks named under "today" are those of `mismatch_report` and the join (same doc, "Query surface", "Firmware configuration against a standard").

## Worked example: a bus left unconnected

**What happened.** A product's units share load over a bus that runs from one unit to the next. The design described that bus in a Linear issue and in the design document. In the schematic, the bus's net reached a test point and nothing else: not the inter-unit connector, not the parts on the bus. Nothing in the atlas read the design, so nothing compared it with the schematic.

**How the planes catch it, cheapest first.**

1. **Hardware alone.** A named net whose only member is a test point. Deterministic and free, but alone it is an `info` line among deliberate single-pin nets ([02](02-hardware.md#open)).
2. **Design × hardware, deterministic.** The net's name appears in the Linear issue and in the design document (a mention, [05](05-design.md#mentions-deterministic-and-free)). A mentioned net that is unconnected is a finding of its own class, citing the issue, the document's page and the netlist. **No LLM, so it runs on every join.** This step assumes the design spells the net as the schematic does; the spelling rule is open ([05](05-design.md#open)).
3. **Design × hardware, on demand.** A session asks about the bus; an LLM reads the claim ("runs from one unit to the next through the inter-unit connector"), and `net_trace` from the net does not reach that connector's declared interface. The finding states the claim, its cite and the trace.

**Step 2 alone would have caught it**, which is why the first piece of the rework is design × hardware ([the proposal](../../embarch-atlas-planes-proposal.md#order)).

## Open

- **The check registry.** Recommended: each check's letter or mismatch class, the planes it reads, its severity and its module, in one table in the code; the check catalogue a contributor reads is rendered from it ([12](12-navigation.md#open)).
- **The new class's name and severity.** Recommended: `design-vs-hardware` at `check` when the design mentions an entity the hardware leaves unconnected or lacks.
- **Which side is wrong.** The tool never decides. Recommended framing for the report: design, specifications and defining documents say what *should* be; hardware, firmware and platform say what *is*; measured says what was *observed*. A finding states both sides with their cites, and the engineer says which one moves.
- **The Atlas tab.** Problems shown per plane pair, later.
