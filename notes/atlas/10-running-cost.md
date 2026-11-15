# Atlas notes: running cost and reuse

**Status:** draft, 2026-11-15.

The options in these notes were weighed by **reuse of what already exists** and by **running cost**, the two criteria the owner set.

## Where the LLM runs

**On demand, in a Claude Code session, and nowhere else.** The hook's bump runs no LLM step today (`embarch-atlas` repo, `DESIGN.md`, "Bumping when HEAD moves"), and the design plane does not change that. Chosen over a queue that a session drains and over a scheduled headless run, which would spend quota whether or not anyone needs the answer. **The cost of that choice is that LLM-judged mismatches surface only when someone looks**; the deterministic checks still run on every join, which is why they come first ([09](09-interactions.md#worked-example-a-bus-left-unconnected)).

## Per plane

| Plane | Deterministic, on every update | LLM, and when | Frozen on |
|---|---|---|---|
| Specifications | Inventory, page text, page classes (today) | A document's sections, when translated (today) | Page text hashes |
| Hardware | The schematic's netlist; the rework merge | A rework draft, once per rework | The rework source's version key |
| Firmware | The build, the code index, the commits attached to modules | A card per changed module ([03](03-firmware.md#open)) | The module's file hashes |
| Platform | West revisions, the patch set, the HAL searches | None planned | |
| Design | Mentions over the desk's index | Claims, and which issues belong, when a session asks | The source and its `updatedAt` |
| External interfaces | The firmware side, extracted from the build | The defining document's sections, as they are needed | Page text hashes |
| Measured | The write-back | None | |

**Nothing above is measured.** The first numbers come from the first fixture and from `scripts/replay.py` in the atlas repo, which already counts the calls and characters a lookup saves against recorded sessions ([embarch-atlas/design.md](../../embarch-atlas/design.md), "Measuring a lookup against recorded sessions").

## What is reused

- **Freezing by content key** (`doc freeze`, `cache/llm/`) for module cards, claims and LLM-judged checks.
- **The engineer-owned overlay** (`pin_names.json`, `declare-pin-name`) for rework overlays.
- **The engineer's answers file** (`answers.toml`) for which issues belong to the design plane.
- **The standard's machinery** (worklist, `requirement` records, `applies`, `transitions`) for interface documents.
- **The code index's lexer** for the firmware side of external interfaces.
- **`net_trace`** for design claims about connectivity.
- **The desk**: Linear, the GitHub index and its draft flow, for the design plane and for Slack findings.
- **Core's chip identity read** for units; **the HIL live log** for measured receipts.

## What is new

- **embarch-desk**: a route serving an issue's or PR's full text, comments and `updatedAt`; a Slack connector.
- **embarch-atlas**: plane tags and per-plane staleness; mention matching; claim records; rework overlays and units; module cards; the platform checks; the external-interface extractor and check; the measured write-back.

## Open

- **The first atlas's card cost on a real firmware repo.** One read per module; not measured.
- **The desk read's latency** at question time. The desk answers its index from memory; a full issue read may go to Linear.
