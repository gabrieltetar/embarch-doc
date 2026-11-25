# embarch-study-designer: decisions

**Status:** active, 2026-09-02.

Why it is the way it is, split by mission. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). Types: [interfaces/types.md](interfaces/types.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). They address the *sub-project*, not a file — which is what let them move from `design.md` §3 to one `decisions.md` and then into the files under `decisions/` without touching one of the references pointing at them. `scripts/check-decision-refs.py` resolves every one.

| Load this for | Decisions |
|---|---|
| [Crate shape and boundaries](decisions/crate.md) — what it links, and how it reaches three consumers in two languages | 1, 2, 5, 7, 8, 23 |
| [What CI checks](decisions/ci.md) — what checks its feature cells, why it does not release, and why `cargo doc` isn't in the gate | 64, 65, 68 |
| [Bounded collections and type size](decisions/limits.md) — every capacity, 77 KB → 1 KB on the host, why the `no_std` shape stays big, and three caps that are another firmware's | 15, 46, 49, 63, 76 |
| [Serialization, framing, and the link](decisions/wire.md) — two formats, COBS, an append-only enum | 3, 4, 10, 24, 25 |
| [Schema versioning, handshake, clocks](decisions/versioning.md) — two constants, and where time comes from | 12, 30, 47, 72 |
| [Integrity seals and pre-flight validation](decisions/seals.md) — three siblings, what sits outside them, and the CSV-name and record-check rules | 17, 18, 26, 81 |
| [Study structure and execution](decisions/study.md) — steps, failure, the fuzzing loop | 9, 13, 14, 16, 29, 42, 51, 80 |
| [Host-run repeat and line counts](decisions/host-repeat.md) — a loop and a per-pass count with no verdict, and why no schema bump | 86 |
| [A prompt that names a bench configuration](decisions/host-prompt.md) — a name only, forwarded by Core and resolved by whoever shows the prompt | 88 |
| [A host step's number and a prompt's kind](decisions/host-parse.md) — `parse` on a step, `parse_step_number`, and who may answer a prompt | 108 |
| [Streams: one generic capture pipeline](decisions/streams.md) — four near-identical paths become one | 11, 20, 21, 27, 39, 82 |
| [Declared payload meaning](decisions/payload-meaning.md) — where a byte acquires a meaning | 52, 55, 70, 71 |
| [GATT discovery and monitoring](decisions/gatt.md) — walking a table, windows | 31, 32, 36, 53, 83, 89 |
| [Vendor GATT service identities](decisions/vendor-identities.md) — a built-in table, identity only | 41 |
| [GATT extraction and naming](decisions/gatt-extract.md) — reading a repo, and naming a characteristic | 33, 56, 57, 78 |
| [What the extractor reads](decisions/gatt-extract-scan.md) — comments are not definitions | 85 |
| [BLE link control](decisions/ble.md) — naming the DUT, elevating, unbonding | 43, 44, 50 |
| [What a study declares](decisions/declares.md) — firmware versions, and how each is verified | 40, 74 |
| [What a study builds](decisions/builds.md) — a study's own build spec, and the outpost mode it requires | 77 |
| [The GATT table a study declares](decisions/declared-gatt.md) — designed, never built | 45 |
| [Protocol manifests](decisions/protocols.md) — an authored state machine, never inferred | 58, 59, 61, 75 |
| [Protocol divergence](decisions/protocol-divergence.md) — a saved study checked against its `.eap` by comparing definitions, not a digest | 87 |
| [Executing a protocol](decisions/protocol-exec.md) — what a run does, what it may report, and what the parser refuses | 60, 62, 84 |
| [Authoring surfaces](decisions/authoring.md) — the table, a raw payload row, a saved-study library, one built-in vocabulary | 6, 34, 37, 38, 73 |
| [The custom-action registry](decisions/registry.md) — engineer-supplied bytes, and what `validate` refuses a hand-edited file for | 35, 66, 67, 69 |
| [The HIL file shapes](decisions/hil-shapes.md) — what the notes left open in `measurements.json`, the verdicts, `run.json`, a Study's export, and the PDF readers | 90, 91 |
| [The HIL reducers](decisions/hil-reducers.md) — one module behind `reducers` (alloc only), behaviours kept by version, what each reducer's `U` and failure are | 92, 93, 94 |
| [The HIL verdict rules](decisions/hil-verdicts.md) — one module behind `verdicts` (alloc only), evidence before limits, the guard band, the width check, the roll-up's edges | 95, 96, 97, 98 |
| [A study's measurement declarations](decisions/hil-declarations.md) — `Study.measurements`, host-only and always compiled, what `validate_measurements` refuses | 99, 100 |
| [Analog capture](decisions/analog-capture.md) — an audio-rate analog source, framed blocks checked and placed by index, a session around them, and a stop message | 104, 105, 106, 107 |
| [The HIL test, suite and plan](decisions/hil-tests.md) — JSON types behind `hil-test`, the definition hash over RFC 8785, the per-measurement derived diff; three plan choices the owner may strike | 109 |
| [A HIL test is checked when it is defined](decisions/hil-tests.md) — `check_test` returns every refusal; an energising rule that counts what it cannot place as energising; three more plan choices the owner may strike | 110 |
| [The PDF text extractor and number grammar](decisions/hil-pdf.md) — `lopdf` behind `pdf-text`, what the extractor and grammar add to the doc | 101, 102, 103 |
| [Things this crate does not have](decisions/removed.md) — removals, and two tombstones | 19, 22, 28, 48, 54 |

**The durable principle this crate keeps re-deriving**, stated once here because it generalises past it: *no EmbArch component should ever present an inference about what a specific piece of hardware or firmware does — derived from reading its source, its comments, or any heuristic — as established fact.* Where that knowledge is needed, the answer is a pipeline for the engineer who actually knows to supply it explicitly. Decisions 35, 41, 45, 52, 56 and 58 are each that rule applied somewhere else.
