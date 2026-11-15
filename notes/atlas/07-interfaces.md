# Atlas notes: the external-interfaces plane

**Status:** draft, 2026-11-15.

## What it holds

**Both sides of every interface the firmware has with the outside**: a document that defines what the firmware must do, and what the firmware actually exposes or consumes. The owner's example is a client's BLE API the firmware has to interface with. Chosen over documents only and over the firmware side only.

- **The defining side**: a client's API document, a host or companion-app protocol, a cloud message format. **Distilled like a standard**: it binds a role, not a part; requirements carry IDs and a modality; sections are distilled from a worklist as they are needed; and the `applies` and `transitions` lookups fit an applicability table or a protocol state machine (`embarch-atlas` repo, `DESIGN.md`, "Standards and specifications", "Protocol records").
- **The firmware side**: **extracted from the build by the code index**, which already lexes `*_DEFINE(name, ...)` objects and SMF tables (same doc, "Query surface"): GATT services and characteristics with their UUIDs, properties and permissions; shell commands; settings keys; the packed structs that go on a wire. A firmware that is the client of someone else's API consumes rather than exposes: the UUIDs it discovers and the messages it sends. Keyed on the commit, like the rest of the firmware.
- **The check between them**: each item the defining document requires, against what the build exposes or consumes. A required characteristic that is absent, a property or permission that differs, a struct field whose size differs from the document's.

## Open

- **The name.** "Interfaces" already means board-to-board mating in the atlas (`interfaces.py`, `declare-interface`, `system.json`'s `interfaces`). Recommended: "external interfaces" everywhere, never the bare word.
- **The document kind.** A client's API document has none of the release lines the standard classifier looks for. Recommended: a kind of its own that reuses the standard's records and worklist, set by the engineer's `--kind` override.
- **Extraction per macro family**, and interfaces built without macros (a hand-written command parser). The second is read on demand through `code`.
- **Client material in a public repo.** A client's API document is a runtime input under `<fw>/embarch/atlas/`, never in the atlas repo, as every client document is today.
