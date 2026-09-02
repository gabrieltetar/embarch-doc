# embarch-study-designer decisions: Protocol manifests (`.eap`)

**Status:** active, 2026-09-02.

An engineer-authored state machine the tool never infers.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 58 — A protocol manifest an engineer writes and the tool never infers: `embarch/protocols/*.eap`

Opened by the repo owner with a design draft written against a real firmware's BLE stack rather than against this suite's own code, closing two things at once: decision 39's write direction, rejected at the time as premature because nothing in the model had conditional logic, branching or multi-step state; and milestone 11 §3.8's real-hardware step, blocked since 2026-08-24 on "user-supplied DUT protocol knowledge" with no mechanism for a user to supply any.

A per-repo `<firmware-repo>/embarch/protocols/<name>.eap` ("EmbArch Protocol") holds one or more named `protocol { … }` blocks: characteristic aliases, frame shapes, session variables, and a state machine. It sits beside `study-actions.toml` (decision 35) and `study-structs.toml` (decision 52), for the reason those two are there — it is engineer-authored knowledge about *this* DUT, and it belongs in the repo that knows it. A protocol block is **self-contained**: it declares its own characteristic aliases rather than referencing a `Study`'s taps, so one `.eap` protocol is a portable unit any study can invoke without first being wired up to match.

**Resolved into the submitted `Study` at build time**, as `Study.protocols`, referenced by a `u8` index from `Action::RunProtocol` the way `StreamEncoding::Struct { decoder }` indexes `Study.decoders`. Decision 52 had already settled the same question for payload layouts one day earlier and for an independent reason: **Core cannot read the firmware repo.** A study naming a manifest rather than carrying it would render on its author's machine and nowhere else, and would behave *differently* after an unrelated edit to that file.

**The draft bound a manifest by a CRC over its text, and that is the one thing here that changed.** It was proposed as the same integrity pattern `steps_crc`/`streams_crc` use, citing `StreamEncoding::OutpostTrace { manifest_crc }` as precedent. That precedent had been **reversed the day before** ([embarch-decision-reversals.md](../../embarch-decision-reversals.md) row 37) and is now a unit variant. Half of why does not apply here — the outpost's manifest is generated from a linked image, so no CRC of it exists at compile time, whereas an `.eap` file is authored and does exist. The other half applies exactly: it is the write-ahead staleness pattern [embarch-topology/design.md](../../embarch-topology/design.md) decision 3 exists to eliminate, and a saved study's pinned CRC would go stale on the author's next edit.

**Where it parts company with `decoders`, and why that costs a third seal.** `Study.decoders` is host-only and sealed by neither CRC, because a layout only decides how the host *renders* a byte already captured. A protocol is the opposite: dev-bench **executes** it (decision 60), so it crosses the wire like `steps` and gets a seal like `steps`. `protocols_crc` is a **sibling** rather than a widening, per decision 17's structural rule.

**Amended 2026-08-26, one field short.** As first shipped, this resolved a manifest into `Study.protocols` and sealed it — and stopped at the host. `StudyStart` carried no `protocols` at all, so the field existed everywhere except on the one hop that had to execute it, and `Action::RunProtocol` named an index into something dev-bench had never been sent. `StudyStart` now carries `protocols` and `protocols_crc`, **appended after `dev_bench_log_level`** rather than inserted beside `streams_crc`: postcard is positional and this wire's rule is that a new field goes on the end, so the diff a human checks is a suffix. Decision 17's structural rule — each seal immediately after the one contiguous span it covers — is a property of the *pair*, not of where the pair sits, and holds either way. [embarch-decision-reversals.md](../../embarch-decision-reversals.md) row 68; the executor is [embarch-dev-bench/decisions.md](../../embarch-dev-bench/decisions.md) decision 41.

**Syntax is a small purpose-built text grammar, not TOML/YAML/JSON.** The grammar is inherently recursive — frames select on magic bytes, records repeat other records, fields parametrize how later fields are read — and that nests far more legibly as text than as table-of-tables TOML. It stays pure data: the parser produces an AST with no code, no `eval`, and nothing executable beyond the fixed primitive set decision 59 admits. Full grammar in §4.9.

### 59 — A fixed, closed set of decode primitives, split by what a running state machine can reach

The primitive set was checked against a real, currently-shipping protocol (the the client S11 reference-dut's SDS/DMS/BDS services) that exercises every awkward case this kind of description has to survive: magic-byte format versioning with no version handshake, self-describing descriptor tables that parametrize how later bytes are read, delta+zigzag+variable-bit-packed payload columns, CRC32-validated records, and a real flow-controlled state machine. **Every primitive exists because that protocol needed it; none were added speculatively.**

Sized/endian integers; `fixed(scale, unit)`; byte spans; `select_if` magic-byte dispatch; `repeat[count_from: <field>]` for descriptor-table-parametrized parsing; `bitpack[count_from:] width_from: … delta zigzag seed:` for the compression primitive underlying every batch format checked against; and `crc32` with a per-frame `skip|error|retry` policy.

**Deliberately no plugin trait and no escape hatch**, unlike decision 33's `GattConfigExtractor`, which extends per firmware because UUID extraction genuinely varies per build system. Byte codecs do not vary that way — every format this suite has seen (`BSS\x00`…`BSS\x03`, `PPG1`…`PPG8`, `GWF1`) is the same handful of primitives recomposed. A future firmware needing a primitive this list lacks is a real decision to extend the list, not a silent per-firmware workaround.

**The split, which is this decision's real content and was not in the draft.** With dev-bench as the executor (decision 60), every primitive the wire carries is C the bench has to run, and every future addition costs a firmware reflash and a decision 36 re-pinning pass. So the grammar divides by **what a running state machine can reach**:

- **Crossing the wire:** `select_if` predicates, integer scalar reads at fixed offsets, byte-span *lengths*, write templates, and the expression set — everything a `when`, a `remember` or a `write` can name.
- **Staying host-side**, parsed from the same file and applied at render time over the raw bytes the tap already wrote: `repeat`, `bitpack`, `crc32`, and `fixed`.

**The line is not a compromise, it is where the consumers are.** No guard in either worked protocol references a bit-packed column — guards read headers (`progress.total`, `chunk.bps`) — and with `ProtocolOutcome` reporting only a state name (decision 62), dev-bench has **no consumer at all** for a bit-unpacked value. Putting one in hand-written C would buy a capability nothing uses, on a board this project has had to shrink things to fit three times, and would make the whole grammar reflash-costing rather than just the small half of it.

**Two things the grammar does not have, both refusals rather than omissions.** The draft's `crc32 ieee seed: <literal>` loses its seed parameter: CRC-32/ISO-HDLC — init `0xFFFFFFFF`, reflected in and out, final XOR `0xFFFFFFFF` — already *is* what that spelling names and is bit for bit Zephyr's `crc32_ieee`, so a configurable seed would mean constructing a custom algorithm per frame, i.e. the second CRC implementation the draft's own constraints asked not to exist. `policy` stays, because it genuinely varies per frame. And **`crc16` is refused by name**: Zephyr ships several mutually incompatible CRC-16s (ANSI, CCITT, ITU, each with its own seed and reflection), the design named none, and neither worked protocol uses one. Guessing which would be the inference this suite refuses everywhere else; implementing all four would be four primitives with no caller, the shape [embarch-core/decisions.md](../../embarch-core/decisions.md) decision 30 already records as a mistake worth not repeating. One line to add the day a real frame names a variant.

### 61 — A write is built from the same typed vocabulary as a decode

Inside a `RunProtocol` block, a `write`'s payload is assembled from decision 59's primitives, each field taking a literal, a `session.*` variable, or a field of the frame that triggered the current event. Required for anything like a live epoch in a time-sync write, or the echo-back-the-last-seen-length pattern where a client must reply with exactly the length it was notified — a payload computed purely from constants expresses neither.

It **replaces literal-only writes only inside a `RunProtocol` block.** Decision 35's registered actions are enumerated-values-only by design, precisely so nobody uses a value whose meaning nothing recorded, and they are untouched.

