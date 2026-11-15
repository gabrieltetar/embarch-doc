# Proposal: the atlas in planes

**Status:** proposal, 2026-11-15.

Spans `embarch-atlas`, `embarch-desk`, `embarch-core`, `embarch-api` and this repo, which is why it sits at the root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). **The atlas becomes seven planes, each a source of truth with its own version and its own update procedure, and one join that processes the interactions between them.** The research and every answer behind it are in [notes/atlas/](notes/atlas/README.md), gathered with the owner on 2026-11-15; this file keeps the design and the work, and links to the notes for the reasons. It is also the atlas rework that [the HIL proposal](embarch-hil-proposal.md) puts first.

## Why

**A bus between two units was described in a Linear issue and in the design document, and the schematic left it unconnected; nothing caught it**, because the atlas reads no design source ([the example](notes/atlas/09-interactions.md#worked-example-a-bus-left-unconnected)). The atlas already holds four planes unnamed: the specifications, the hardware, the firmware and, through the PRD alone, a sliver of the design. Hardware has no revision, rework or unit, the design has no version, and the join is stale as a whole ([why planes](notes/atlas/01-planes.md#why-planes)).

## The planes

| Plane | Holds | Version key | New |
|---|---|---|---|
| **Specifications** | Datasheets, manuals, errata, app notes, standards | doc_id and sha256 | A plane tag; interface documents and platform errata use its machinery |
| **Hardware** | Netlist and BOM per board revision, rework overlays, units | Board revision and rework set | Revisions; **reworks drafted by an LLM and confirmed by the engineer**; units keyed by MCU unique ID ([02](notes/atlas/02-hardware.md)) |
| **Firmware** | Build, devicetree, Kconfig, code index, states; module cards | Commit | **Module cards kept current by range replay**: the bump marks a changed module's card behind, a session rewrites it ([03](notes/atlas/03-firmware.md#who-rewrites-a-card)) |
| **Platform** | Zephyr, SDK and HAL versions, west patches, upstream known issues | West revisions and the patch set | The plane ([04](notes/atlas/04-platform.md)) |
| **Design** | Linear issues, PR discussions, commit messages, design documents | Per source: `updatedAt`, commit, sha256 | **Read live through the desk; Slack finds, never cited** ([05](notes/atlas/05-design.md)) |
| **External interfaces** | A document defining an interface (a client's BLE API); what the firmware exposes or consumes | Document sha256; commit | **Both sides, and a check between them** ([07](notes/atlas/07-interfaces.md)) |
| **Measured** | Live findings with receipts; links to Study and Test zips | Append-only | **Live write-back only** ([08](notes/atlas/08-measured.md)) |

## The design in one screen

- **Home** ([notes](notes/atlas/01-planes.md#where-they-live)): per firmware repo, as today; a second repo of the same product points at the first's shared planes.
- **An atlas stays `<target>@<commit12>`**, the target declares its board revisions and rework set, and the stamp records every plane's version key ([notes](notes/atlas/01-planes.md#the-atlas-id-and-the-stamp)).
- **The design plane reads the desk, live** ([notes](notes/atlas/05-design.md)): "never fetches a document" becomes "never fetches from the internet; reads the desk". Citable: Linear issues, PR discussions, commit messages, documents in the sources folder. **Slack is never cited**: what it holds and no issue does becomes a Linear issue draft through the desk, waiting for the owner's Send. An LLM picks which issues belong and asks the engineer when unsure.
- **Mentions are deterministic, claims are on demand.** A design source naming a net, refdes, part, devicetree label or symbol is matched for free; what it says about it is read by an LLM when a session asks.
- **One join, plane-tagged** ([notes](notes/atlas/09-interactions.md)): every check declares the planes it reads, the deterministic join reruns whole, LLM-judged comparisons are frozen on their inputs' keys, and staleness names the plane that moved.
- **LLM work runs on demand in a session only**, never in the hook or on a timer ([notes](notes/atlas/10-running-cost.md)). The deterministic checks run on every join, which is why a mentioned net left unconnected is caught without one.

## The work, by sub-project

| Sub-project | Work |
|---|---|
| `embarch-atlas` | Plane tags and per-plane staleness; mention matching and claim records; the `design-vs-hardware` check; rework overlays, units, revisions; module cards with range replay; the platform checks; the external-interface extractor and check; the measured write-back; a check catalogue rendered from the check registry; a netlist-export reader for other EDA tools; a public end-to-end example; the README's "Before you start" block |
| `embarch-desk` | A route serving an issue's or PR's full text, comments and `updatedAt` from its cache; a Slack connector scoped to channels the engineer picks; the Slack-to-Linear draft |
| `embarch-core` | The MCU's unique ID available to a client, if it is not already (checked when units start) |
| `embarch-api` | The live-log line the measured write-back takes as its receipt (the HIL proposal's live-log writer) |
| `embarch-doc` | The atlas's design moved into its four files, organised by plane, with a pipeline map, a module map by plane, the check catalogue and contributor recipes; the atlas's terms in the glossary (the owner's call: [the nine navigation items](notes/atlas/12-navigation.md#decided)) |

## Order

1. **Design × hardware** (the owner's pick): the desk route, mentions over Linear and design documents, the single-member net check, the `design-vs-hardware` class with its plane tags, proven on a synthetic fixture of a bus left unconnected.

The rest is recommended and not yet answered:

2. **The measured write-back**, which the HIL proposal's Live phase waits on.
3. **Plane tags on every existing check**, per-plane staleness and the check catalogue.
4. **Hardware revisions, reworks and units**, and the netlist-export reader.
5. **Module cards with range replay.**
6. **External interfaces**, then **the platform**, then **the Slack connector**.
7. **The design moved into this repo's four files**, once the planes it is organised by have landed, with the pipeline map, the module map and the contributor recipes.

**Any time**, being small: the atlas's terms in the glossary, the README's "Before you start" block, and the public end-to-end example grown from step 1's fixture.

## Open questions

Each note closes with its own list. The ones that touch more than one plane:

- **Where measured records live once planes are shared** ([01](notes/atlas/01-planes.md#open)).
- **The spelling rule for a name that prose and the netlist write differently** ([05](notes/atlas/05-design.md#open)).
- **Nothing here is measured**: the first numbers come from the first fixture and the atlas's replay harness ([10](notes/atlas/10-running-cost.md)).

**Fold:** each piece moves into the atlas's docs as it is accepted and deletes its part here; the notes go with it. This file is deleted once nothing in it is still proposed.
