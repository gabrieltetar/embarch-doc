# embarch-core: decisions

**Status:** active, 2026-09-02.

Why it is the way it is, split by mission — Core owns more distinct jobs than any other component, and a session is usually here for one of them. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). HTTP surface: [interfaces.md](interfaces.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). They address the *sub-project*, not a file — which is what let them move from `design.md` §3 to here, and then into these seven files, without touching one of the references pointing at them. `scripts/check-decision-refs.py` resolves every one.

| Load this for | Decisions | Size |
|---|---|---|
| [Platform, process, and auth](decisions/platform.md) | 1, 2, 3, 4, 5, 6, 7, 11, 14, 15, 17, 42 | 5.8 KB |
| [Probes, board identity, and chip mapping](decisions/probes.md) | 8, 9, 22, 23, 26, 34 | 4.0 KB |
| [Flashing](decisions/flashing.md) | 10, 18, 21, 32, 36 | 5.5 KB |
| [Running a study](decisions/studies.md) | 19, 20, 24, 31, 33, 35, 40, 41 | 8.8 KB |
| [Streams, manifests, and rendering](decisions/streams.md) | 30, 38, 39 | 4.8 KB |
| [Logging](decisions/logging.md) | 16, 29, 37 | 2.7 KB |
| [Error and human surfaces](decisions/surfaces.md) | 12, 13, 25, 27, 28 | 5.6 KB |

An entry may own several numbers where decisions were merged under a byte budget; every listed number still resolves. Retired entries stay as one-line tombstones so a dangling reference lands on an explanation rather than a gap — decision 25 is the one here.
