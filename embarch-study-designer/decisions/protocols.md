# embarch-study-designer decisions: Protocol manifests (`.eap`)

**Status:** active, 2026-09-02.

An engineer-authored state machine the tool never infers.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 58 — A protocol manifest an engineer writes and the tool never infers: `embarch/protocols/*.eap`

Opened with a design draft **written against a real firmware's BLE stack rather than against this suite's own code**, closing two things at once: decision 39's write direction, **rejected at the time as premature because nothing in the model had conditional logic, branching or multi-step state**; and a real-hardware step **blocked for days on "user-supplied DUT protocol knowledge" with no mechanism for a user to supply any.**

A per-repo file holds named protocol blocks: characteristic aliases, frame shapes, session variables, and a state machine. It sits beside the action registry and the struct layouts **for the reason those two are there — it is engineer-authored knowledge about *this* DUT, and it belongs in the repo that knows it.** A block is **self-contained**: it declares its own aliases rather than referencing a study's taps, **so one protocol is a portable unit any study can invoke without first being wired up to match.**

**Resolved into the submitted study at build time**, indexed the way a struct layout is. Decision 52 settled the same question for payload layouts a day earlier and for an independent reason: **Core cannot read the firmware repo.** A study *naming* a manifest rather than carrying it **would render on its author's machine and nowhere else, and would behave *differently* after an unrelated edit to that file.**

**The draft bound a manifest by a CRC over its text, and that is the one thing here that changed.** It cited the outpost trace encoding as precedent — **a precedent reversed the day before** ([reversals](../../embarch-decision-reversals.md) row 37). Half of why does not transfer: that manifest is generated from a linked image, **so no CRC of it exists at compile time**, whereas an authored file does. **The other half applies exactly: it is the write-ahead staleness pattern the topology crate exists to eliminate, and a saved study's pinned CRC would go stale on the author's next edit.**

**Where it parts company with `decoders`, and why that costs a third seal.** `Study.decoders` is host-only and sealed by neither CRC, because a layout only decides how the host *renders* a byte already captured. A protocol is the opposite: dev-bench **executes** it (decision 60), so it crosses the wire like `steps` and gets a seal like `steps`. `protocols_crc` is a **sibling** rather than a widening, per decision 17's structural rule.

**Amended 2026-08-26, one field short.** As first shipped, this resolved a manifest into `Study.protocols` and sealed it — and stopped at the host. `StudyStart` carried no `protocols` at all, so the field existed everywhere except on the one hop that had to execute it, and `Action::RunProtocol` named an index into something dev-bench had never been sent. `StudyStart` now carries `protocols` and `protocols_crc`, **appended after `dev_bench_log_level`** rather than inserted beside `streams_crc`: postcard is positional and this wire's rule is that a new field goes on the end, so the diff a human checks is a suffix. Decision 17's structural rule — each seal immediately after the one contiguous span it covers — is a property of the *pair*, not of where the pair sits, and holds either way. [embarch-decision-reversals.md](../../embarch-decision-reversals.md) row 68; the executor is [embarch-dev-bench/decisions.md](../../embarch-dev-bench/decisions.md) decision 41.

**Syntax is a small purpose-built text grammar, not TOML/YAML/JSON.** The grammar is inherently recursive — frames select on magic bytes, records repeat other records, fields parametrize how later fields are read — and that nests far more legibly as text than as table-of-tables TOML. It stays pure data: the parser produces an AST with no code, no `eval`, and nothing executable beyond the fixed primitive set decision 59 admits. Full grammar in §4.9.

### 59 — A fixed, closed set of decode primitives, split by what a running state machine can reach

The set was checked against **a real, currently-shipping protocol** exercising every awkward case this kind of description has to survive: **magic-byte format versioning with no version handshake, self-describing descriptor tables that parametrize how later bytes are read, delta-plus-zigzag bit-packed payload columns, CRC-validated records, and a real flow-controlled state machine.** **Every primitive exists because that protocol needed it; none were added speculatively.**

Sized and endian integers, scaled fixed-point, byte spans, magic-byte dispatch, descriptor-parametrized repeats, the bit-packing primitive underlying every batch format checked against, and a CRC with a per-frame skip/error/retry policy.

**Deliberately no plugin trait and no escape hatch**, unlike the extractor, which extends per firmware **because UUID extraction genuinely varies per build system.** Byte codecs do not vary that way — **every format this suite has seen is the same handful of primitives recomposed.** A future firmware needing one this list lacks is **a real decision to extend the list, not a silent per-firmware workaround.**

**The split, which is this decision's real content and was not in the draft.** With dev-bench as the executor (decision 60), every primitive the wire carries is C the bench has to run, and every future addition costs a firmware reflash and a decision 36 re-pinning pass. So the grammar divides by **what a running state machine can reach**:

**Crossing the wire:** dispatch predicates, integer reads at fixed offsets, byte-span *lengths*, write templates, and the expression set — **everything a guard, a `remember` or a write can name.** **Staying host-side**, parsed from the same file and applied at render time over the raw bytes the tap already wrote: repeats, bit-packing, CRCs and scaling.

**The line is not a compromise, it is where the consumers are.** No guard in either worked protocol references a bit-packed column — **guards read headers** — and with a run reporting only a state name, **dev-bench has no consumer at all for a bit-unpacked value.** Putting one in hand-written C **would buy a capability nothing uses, on a board this project has had to shrink things to fit three times, and would make the whole grammar reflash-costing rather than just the small half of it.**

**Two things the grammar does not have, both refusals rather than omissions.** The CRC loses its **seed parameter**: the named algorithm already *is* a fully specified one, bit for bit the stack's own, **so a configurable seed would mean constructing a custom algorithm per frame — the second CRC implementation the draft's own constraints asked not to exist.** The per-frame policy stays, **because it genuinely varies per frame.** And **the 16-bit CRC is refused by name**: the stack ships several mutually incompatible ones, **the design named none, and neither worked protocol uses one. Guessing which would be the inference this suite refuses everywhere else; implementing all four would be four primitives with no caller.** One line to add the day a real frame names a variant.

### 61 — A write is built from the same typed vocabulary as a decode

A write's payload is assembled from decision 59's primitives, each field taking a literal, a session variable, **or a field of the frame that triggered the current event.** Required for **a live epoch in a time-sync write, or the echo-back-the-length pattern where a client must reply with exactly the length it was notified — a payload computed purely from constants expresses neither.**

It **replaces literal-only writes only inside a `RunProtocol` block.** Decision 35's registered actions are enumerated-values-only by design, precisely so nobody uses a value whose meaning nothing recorded, and they are untouched.

