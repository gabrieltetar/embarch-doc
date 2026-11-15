# Atlas notes: the planes

**Status:** draft, 2026-11-15.

## Why planes

**The atlas already holds four planes without naming them.** Its board-independent documents are the specifications, its schematic analysis is the hardware, its pinned build is the firmware, and its `prd` kind is a sliver of the design (the `embarch-atlas` repo's `DESIGN.md`, "Principles" 5 and 6). Its joins are already interactions between them: hardware against specifications (pin records against the netlist), hardware against firmware (the pin map, devicetree against nets), firmware against specifications (`codecheck`, `limits`, `fw_check`).

What it lacks is what the owner asked for:

- **A version per plane.** Hardware is keyed by the schematic PDF's hash alone: no board revision, no rework, no physical unit. The design has no version at all.
- **The design plane.** Linear, PRs, Slack and meetings are not read, which is why a bus the design document and a Linear issue described, and the schematic left unconnected, went unnoticed ([09](09-interactions.md#worked-example-a-bus-left-unconnected)).
- **Updating one plane, then its interactions.** The plane updates exist separately (`/atlas-translate-docs`, `schematic`, the hook's bump), but the join and its staleness are all-or-nothing: one atlas per `<target>@<commit12>`, stale as a whole.

## The seven planes

The four the owner named, plus three the owner added in the interview: **measured**, **platform** and **external interfaces** (which covers a client's API the firmware must meet, a BLE API being the example). Manufacturing (fixtures, calibration, provisioning) was offered and not taken.

| Plane | Holds | Version key | Updated by | Today |
|---|---|---|---|---|
| **Specifications** | Datasheets, reference manual, SVD, errata, app notes, standards | doc_id and sha256 | `/atlas-translate-docs`, lazy worklists | Built |
| **Hardware** | Netlist and BOM per board revision, rework overlays, units | Board label, revision, rework set | `schematic`, rework drafts confirmed by the engineer | Netlist built; revisions, reworks and units new ([02](02-hardware.md)) |
| **Firmware** | The build, devicetree, Kconfig, code index, SMF states; module cards | Commit, per target | `build`, `update`, the hook; range replay for cards | Structure built; cards new ([03](03-firmware.md)) |
| **Platform** | Zephyr, SDK and HAL versions, west patches, toolchain, upstream known issues | The west projects' revisions and the patch set | `update` after a `west update` | Revisions recorded in the stamp; the rest new ([04](04-platform.md)) |
| **Design** | Linear issues, PR discussions, commit messages, design documents (PRD, architecture PDFs, meeting notes) | Per source: an issue or PR and its `updatedAt`, a commit, a document's sha256 | Read live through the desk; claims on demand | The `prd` kind only ([05](05-design.md)) |
| **External interfaces** | Documents defining an interface the firmware must meet; what the firmware exposes or consumes | Document sha256; commit for the firmware side | Translated like a standard; extracted at build | New ([07](07-interfaces.md)) |
| **Measured** | Live findings with their receipts; links to published Studies and Tests | Append-only | The Live write-back | The `measured` provenance class exists; nothing writes it ([08](08-measured.md)) |

## Where they live

**Per firmware repo, sharable.** The atlas stays under `<fw>/embarch/atlas/`. A second firmware repo of the same product (a bootloader, a second MCU, bench firmware) points its `atlas.toml` at the first repo's shared planes instead of re-inventorying them. Chosen over a product-level folder (cleanest for multi-repo products, but a new home to set up and back up) and over duplicating (the content-keyed LLM cache keeps re-translation nearly free, but answers and reworks would be kept twice).

## The atlas id and the stamp

**An atlas stays `<target>@<commit12>`, and the target declares its hardware**: the board revisions and the rework set it is joined against ([02](02-hardware.md#which-hardware-an-atlas-joins-against)). The stamp records the version key of every plane the join read, as `inputs.json` already records the manifest, each schematic's hash and the answers' hash. That record is what lets staleness name the plane that moved ([09](09-interactions.md)).

## Principles that change

- **"The tool never fetches a document"** becomes: it never fetches from the internet, and **it reads the desk**, the suite's one access point to Linear, GitHub and, once connected, Slack ([05](05-design.md#read-live-through-the-desk)). Documents are still supplied by the engineer.
- **Board-independent against board-specific** (principle 5) gains a dimension: a hardware fact now depends on the board's revision and reworks too.
- **Pinned to one target and one commit** (principle 6) gains the target's declared hardware; the design is read live and its version is recorded per source.
- **LLM work runs on demand, in a session.** Never in the hook, never on a timer ([10](10-running-cost.md)).
- **Unchanged**: deterministic first, records are the source of truth, nothing is deleted for failing a check, LLM outputs are frozen by content hash, the only LLM is a Claude Code session.

## Open

- **Where measured records live once planes are shared.** A measurement binds to a unit (product-level) and an image (per repo). Recommended: with the firmware repo whose image ran, the unit looked up in the shared hardware plane.
- **What the stamp records for a plane read live.** Recommended: the design sources the join read, each with its `updatedAt`, so "design changed since the join" is a comparison with the desk's current values.
- **Whether the human surface says "plane".** The Atlas tab already shows layers; a plane filter there is the UI's call, later.
