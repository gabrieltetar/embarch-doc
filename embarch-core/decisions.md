# embarch-core: decisions

**Status:** active, 2026-09-02.

Why it is the way it is, split by mission — Core owns more distinct jobs than any other component, and a session is usually here for one of them. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). HTTP surface: [interfaces.md](interfaces.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). They address the *sub-project*, not a file — which is what let them move from `design.md` §3 to here, and then into these eight files, without touching one of the references pointing at them. `scripts/check-decision-refs.py` resolves every one.

| Load this for | Decisions | Size |
|---|---|---|
| [Platform, process, and locking](decisions/platform.md) | 1, 2, 3, 4, 7, 14, 15, 17 | 5.9 KB |
| [Auth, binding, and configuration](decisions/auth.md) | 5, 6, 11, 53 | 3.8 KB |
| [The route sweep](decisions/route-sweep.md) | 42, 46, 60 | 8.5 KB |
| [Probes, board identity, and chip mapping](decisions/probes.md) | 8, 9, 22, 23, 26, 34, 61, 80 | 9.7 KB |
| [Flashing](decisions/flashing.md) | 10, 18, 21, 32, 82 | 5.3 KB |
| [Flashing backend selection and vendor-tool discovery](decisions/flash-backend.md) | 36, 49, 52, 54 | 9.5 KB |
| [Running a study](decisions/studies.md) | 19, 20, 33, 40, 45 | 6.3 KB |
| [The study record, and reading it back](decisions/study-record.md) | 24, 41, 43, 69, 71 | 8.9 KB |
| [The handshake: version gate and bench identity](decisions/handshake.md) | 31, 35, 47, 56 | 8.8 KB |
| [The outpost mode pre-flight](decisions/outpost-preflight.md) | 74 | 4.6 KB |
| [Streams, manifests, and rendering](decisions/streams.md) | 30, 38, 39 | 5.8 KB |
| [Pushing a stream tap live](decisions/streams-live.md) | 70, 72, 73 | 5.9 KB |
| [The stream index](decisions/stream-index.md) | 62, 63, 64, 65, 66 | 11.0 KB |
| [Logging](decisions/logging.md) | 16, 29, 37, 44, 51, 58 | 9.1 KB |
| [Error and version surfaces](decisions/surfaces.md) | 12, 13, 55, 59, 67, 68 | 11.6 KB |
| [The human enrollment surface](decisions/enrollment.md) | 25, 27, 28, 50, 54 (moved to 57), 57 | 8.8 KB |
| [What a role is made of](decisions/roles.md) | 75, 76 | 4.1 KB |
| [Bootloading over MCUboot serial recovery](decisions/bootload.md) | 77, 78 | 4.5 KB |
| [Writing to a declared signal](decisions/signal-exchange.md) | 79 | 2.7 KB |
| [Reading a target's memory](decisions/live-read.md) | 81 | 2.1 KB |

An entry may own several numbers where decisions were merged under a byte budget; every listed number still resolves. Retired entries stay as one-line tombstones so a dangling reference lands on an explanation rather than a gap — decision 25 is the one here.
