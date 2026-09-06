# embarch-study-designer: decisions

**Status:** active, 2026-09-02.

Why it is the way it is, split by mission. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). Types: [interfaces/types.md](interfaces/types.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). They address the *sub-project*, not a file — which is what let them move from `design.md` §3 to one `decisions.md` and then into these sixteen files without touching one of the references pointing at them. `scripts/check-decision-refs.py` resolves every one.

| Load this for | Decisions |
|---|---|
| [Crate shape and boundaries](decisions/crate.md) — what it links, how it reaches three consumers in two languages, what checks its feature cells, and why it does not release | 1, 2, 5, 7, 8, 23, 64, 65 |
| [Bounded collections and type size](decisions/limits.md) — every capacity, 77 KB → 1 KB on the host, and why the `no_std` shape stays big | 15, 46, 49, 63 |
| [Serialization, framing, and the link](decisions/wire.md) — two formats, COBS, an append-only enum | 3, 4, 10, 24, 25 |
| [Schema versioning, handshake, clocks](decisions/versioning.md) — two constants, and where time comes from | 12, 30, 47 |
| [Integrity seals and pre-flight validation](decisions/seals.md) — three siblings, and what sits outside them | 17, 18, 26 |
| [Study structure and execution](decisions/study.md) — steps, failure, the fuzzing loop | 9, 13, 14, 16, 29, 42, 51 |
| [Streams: one generic capture pipeline](decisions/streams.md) — four near-identical paths become one | 11, 20, 21, 27, 39 |
| [Declared payload meaning](decisions/payload-meaning.md) — where a byte acquires a meaning | 52, 55 |
| [GATT discovery and monitoring](decisions/gatt.md) — walking a table, windows, vendor identities | 31, 32, 36, 41, 53 |
| [GATT extraction and naming](decisions/gatt-extract.md) — reading a repo, and naming a characteristic | 33, 56, 57 |
| [BLE link control](decisions/ble.md) — naming the DUT, elevating, unbonding | 43, 44, 50 |
| [What a study declares](decisions/declares.md) — firmware versions and the GATT table | 40, 45 |
| [Protocol manifests](decisions/protocols.md) — an authored state machine, never inferred | 58, 59, 61 |
| [Executing a protocol](decisions/protocol-exec.md) — what a run does, and what it may report | 60, 62 |
| [Authoring surfaces](decisions/authoring.md) — the UI, the registry, where knowledge enters | 6, 34, 35, 37, 38 |
| [Things this crate does not have](decisions/removed.md) — removals, and two tombstones | 19, 22, 28, 48, 54 |

**The durable principle this crate keeps re-deriving**, stated once here because it generalises past it: *no EmbArch component should ever present an inference about what a specific piece of hardware or firmware does — derived from reading its source, its comments, or any heuristic — as established fact.* Where that knowledge is needed, the answer is a pipeline for the engineer who actually knows to supply it explicitly. Decisions 35, 41, 45, 52, 56 and 58 are each that rule applied somewhere else.
