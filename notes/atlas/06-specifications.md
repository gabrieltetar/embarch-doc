# Atlas notes: the specifications plane

**Status:** draft, 2026-11-15.

## Today

**The plane that is already built.** Datasheets, the reference manual and its SVD, errata, app notes and standards are distilled board-independently, tiered (card, section, page), every number anchored to its page, every LLM output frozen by the page text it rests on; a standard is distilled only for the sections asked for or measured in use (`embarch-atlas` repo, `DESIGN.md`, "Standards and specifications"; [embarch-atlas/design.md](../../embarch-atlas/design.md)). Its version key, the doc_id and the file's sha256, does not change.

## What the rework changes here

- **A plane tag on every check that reads it** ([09](09-interactions.md)).
- **The defining documents of external interfaces** (a client's BLE API) are translated with the standard's machinery ([07](07-interfaces.md)).
- **Upstream release notes and errata are tied to a platform version** ([04](04-platform.md)).
- **What the HIL side needs** lands here: requirement IDs stable across revisions, a test record on a requirement, applicability ([11](11-hil.md)).

## Open

- **An erratum item pointing at the datasheet fact it amends**, so a lookup of the fact shows the erratum beside it. Not checked how far today's `errata` handling goes.
- **A requirement ID stable across a standard's revisions.** A requirement has `rid` today; nothing says it survives a new revision ([11](11-hil.md)).
