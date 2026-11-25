# embarch-core: decisions

**Status:** active, 2026-09-02.

Why it is the way it is, split by mission — Core owns more distinct jobs than any other component, and a session is usually here for one of them. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). HTTP surface: [interfaces.md](interfaces.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). They address the *sub-project*, not a file — which is what let them move from `design.md` §3 to here, and then into these eight files, without touching one of the references pointing at them. `scripts/check-decision-refs.py` resolves every one.

| Load this for | Decisions | Size |
|---|---|---|
| [Platform, process, and locking](decisions/platform.md) | 1, 2, 3, 4, 7, 14, 15, 17, 100, 106 | 8.9 KB |
| [Auth, binding, and configuration](decisions/auth.md) | 5, 6, 11, 53, 109, 129, 132 | 9.5 KB |
| [The route sweep](decisions/route-sweep.md) | 42, 46, 60 | 8.9 KB |
| [Probes and board identity](decisions/probes.md) | 9, 22, 23, 26, 61, 124 | 6.5 KB |
| [Chip mapping and attach guards](decisions/chip-mapping.md) | 8, 34, 80, 89 | 6.3 KB |
| [Flashing](decisions/flashing.md) | 10, 18, 21, 32, 82, 84 | 6.3 KB |
| [Flashing backend selection and vendor-tool discovery](decisions/flash-backend.md) | 36, 49, 52, 54 | 9.5 KB |
| [Running a study](decisions/studies.md) | 19, 20, 33, 40, 45, 90 | 7.2 KB |
| [The study record, and reading it back](decisions/study-record.md) | 24, 41, 43, 69, 71, 86 | 8.9 KB |
| [The handshake: version gate and bench identity](decisions/handshake.md) | 31, 35, 47, 56, 108 | 10.5 KB |
| [The outpost mode pre-flight](decisions/outpost-preflight.md) | 74 | 4.6 KB |
| [Streams, manifests, and rendering](decisions/streams.md) | 30, 38, 39, 88, 125 | 10.4 KB |
| [The dev bench's analog capture](decisions/analog-capture.md) | 126, 127 | 8.9 KB |
| [Stopping a device study](decisions/stopping-a-study.md) | 128 | 4.5 KB |
| [Pushing a stream tap live](decisions/streams-live.md) | 70, 72, 73 | 5.9 KB |
| [The stream index](decisions/stream-index.md) | 62, 63, 64, 65 (retired), 66 (retired), 91 | 9.3 KB |
| [Logging](decisions/logging.md) | 16, 29, 37, 44, 51, 58, 101 | 10.9 KB |
| [Error and version surfaces](decisions/surfaces.md) | 12, 13, 55, 59, 67, 68 | 11.6 KB |
| [The human enrollment surface](decisions/enrollment.md) | 25, 27, 28, 50, 54 (moved to 57), 57, 87 | 8.8 KB |
| [What a role is made of](decisions/roles.md) | 75, 76, 83, 103 | 6.7 KB |
| [Bootloading over MCUboot serial recovery](decisions/bootload.md) | 77, 78 | 4.5 KB |
| [Writing to a declared signal](decisions/signal-exchange.md) | 79, 85, 96 | 9.6 KB |
| [Capturing a signal in the background](decisions/signal-capture.md) | 92, 94, 102 | 5.7 KB |
| [The bench lease](decisions/lease.md) | 93 | 5.5 KB |
| [Reading a target's memory](decisions/live-read.md) | 81, 97 | 4.1 KB |
| [Host-run studies](decisions/host-study.md) | 95, 98, 99 | 8.0 KB |
| [Bench instruments](decisions/instruments.md) | 104 | 4.4 KB |
| [A host step's declared number](decisions/host-parse.md) | 131 | 4.3 KB |
| [Operator prompts in a host study](decisions/host-prompt.md) | 105, 107 | 5.3 KB |
| [Signing a study run's record](decisions/signing.md) | 110 | 7.0 KB |
| [Definitions, premade suites and confirmations](decisions/definitions.md) | 133 | 4.9 KB |
| [A prepared Test run and its go card](decisions/test-runs.md) | 134 | 3.7 KB |
| [The go that starts a Test run and the lease it takes](decisions/test-run-go.md) | 135 | 4.4 KB |
| [The run log, retention before publish, and the discard](decisions/run-log.md) | 111, 112 | 7.1 KB |
| [Measurements at a study's end](decisions/measurements.md) | 113, 114, 115, 121 | 7.3 KB |
| [Core's side of publish](decisions/publish.md) | 116, 117, 118, 119, 120 | 8.3 KB |
| [The call log](decisions/call-log.md) | 122 | 4.0 KB |
| [The idle lease release](decisions/lease-idle.md) | 123 | 3.0 KB |
| [The held serial ports](decisions/port-hold.md) | 130 | 4.0 KB |

An entry may own several numbers where decisions were merged under a byte budget; every listed number still resolves. Retired entries stay as one-line tombstones so a dangling reference lands on an explanation rather than a gap — decision 25 is the one here.
