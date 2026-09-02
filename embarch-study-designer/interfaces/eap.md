# embarch-study-designer: protocol manifests

**Status:** active, 2026-09-02.

The `.eap` wire types and grammar. Why: [../decisions/protocols.md](../decisions/protocols.md) and [../decisions/protocol-exec.md](../decisions/protocol-exec.md).

`Study.protocols` is resolved out of the firmware repo's `embarch/protocols/*.eap` at build time and sealed by `protocols_crc` — the study's **third** seal, because unlike a payload layout this is a value dev-bench *executes* rather than one the host renders with. `Action::RunProtocol { protocol, entry_state }` indexes it; **both are indices, not names**, so no firmware compares strings and every cross-reference is range-checked once, host-side.

**Where each half lives.** The `no_std` wire types cross to dev-bench on `StudyStart`, whose last two fields are `protocols` and `protocols_crc`. The parser and a host-side **reference** interpreter sit behind a feature that implies `std`, so dev-bench firmware carries the definitions and **no parser at all**. The real-time interpreter is dev-bench's own scope, pinned against this module by a literal frame carrying the worked protocol plus semantics cases mirroring the ones below. What the host-side one is for: **pinning the semantics the C must match**, proving the primitive set against the worked protocols, and replaying a capture offline.

## Types

- **`ProtocolDef { name, sources, frames, session, states }`** — one `protocol { … }` block. **Self-contained**: it declares its own characteristic aliases rather than referencing the study's taps, so one protocol is portable across studies wired up differently.
- **`FrameDef { name, source, select_if, fields, spans }`** — `fields` are the **guard-reachable integer reads only**, not the whole packet; `spans` are byte runs whose *length* an expression can reach and whose contents it cannot. Two frames may share a source and the first matching guard wins; **an unguarded frame must be the last declared for its source**, so it cannot shadow a more specific sibling into unreachability.
- **`FrameMatch { offset, eq }`** — the guard. A length is **not stored**: it is the pattern's own length by construction, and carrying both would admit a manifest where they disagree. **A payload too short to contain the match does not match** — a truncated notification and a different format are different facts.
- **`ScalarRead { name, offset, ty }`** reuses the payload-layout `ScalarType`, so a frame lowered into a layout for rendering reads its bytes through the identical code path a guard does. **Float widths are refused where they are declared, not at runtime**, because the expression set is integer-only.
- **`SessionVarDef { name, initial }`** — integers only.
- **`StateDef { name, kind }`**, active or terminal. An active state has an optional `on_enter` write, a list of `on_event` arms, and an optional `on_timeout`. A manifest can declare `pass` or `fail`; **`TimedOut` is reachable only by running out of time and no manifest can name it.**
- **`Operand`** is a literal, a frame field, a session variable, or a span length; **`Expr`** is a term or a saturating addition; **`Condition`** is one comparison. That is the whole set — [../decisions/protocol-exec.md](../decisions/protocol-exec.md) enumerates what is deliberately absent and why.
- **`ProtocolOutcome { final_state, outcome }`** on the step result, **appended last so the wire change is a pure suffix** a hand-written C decoder adopts by reading one more optional field rather than re-walking the message.

## Grammar

The full EBNF lives beside the parser that implements it, **so the two cannot drift**. In outline:

```text
protocol   = "protocol" ident "{" { source | frame | struct | session | state } "}" ;
source     = "source" ident "=" "characteristic" "(" "service" ":" string "," "char" ":" string ")" ;
frame      = "frame" ident "on" ident [ select_if ] "{" { field } "}" ;
field      = scalar | span | repeat | bitpack | crc ;
state      = "state" ident ( "outcome" ":" ("pass"|"fail") | "{" { clause } "}" ) ;
clause     = "on_enter" ":" write
           | "on_event" ident ":" { remember } { when } [ otherwise ]
           | "on_timeout" int ["ms"] [ "retry" int ] ":" "goto" ident ;
operand    = int | "session" "." ident | ident "." ident | "len" "(" ident "." ident ")" ;
```

Whitespace and `#` comments are insignificant; a 16- or 32-bit UUID shorthand expands through the Bluetooth Base UUID, **so a manifest names a characteristic the way its firmware's own header does**. Offsets accumulate in declaration order with no padding when omitted — and **a field following a variable-length one must state its offset** rather than have one guessed on its behalf. Every error carries its source line.

## The worked protocols are tests, not illustrations

They were chosen because they are structurally representative of a real DUT's BLE stack, so they exist to **prove the primitive set is sufficient** rather than to show what it looks like. **If the grammar ever stops expressing one of them, that is a real finding about the primitive set and those tests are where it surfaces.** One is also dev-bench's own fixture, so the two interpreters are exercised against one protocol rather than each against its own.

- **A batch download** — request, chunked pump loop with flow control, consume. Driven to `Pass` over a real byte/chunk sequence; separately stalled to prove the watchdog reaches its abort state, and timed out to prove `retry` **re-sends the `on_enter` write** rather than waiting longer. Also pins that an unrelated notification is ignored rather than failing the run, and that a truncated frame does not advance the machine.
- **A self-describing batch record** — fixed header, a compile-time-capacity descriptor table, a runtime-counted chunk list, delta+zigzag bit-packed columns, and a trailing CRC at `skip` policy. Its tests assert the split directly: five header scalars are guard-reachable at known offsets, and the descriptor table, the packed columns and the CRC are **not on the wire**. A flat sibling on the same source lowers into a struct layout and really renders; the packed one **gets no layout at all**, which is the refusal by design.

**What the first real manifest changed about the worked ones.** The fixture's pump loop counts received bytes and leaves the state when the count reaches the total. Against a firmware that bursts several notifications per control write into a four-slot queue, **a single dropped chunk makes that count short forever**: the state stalls to its watchdog and aborts a transfer the device fully intended to finish. It happened three times in five minutes.

The real firmware **publishes what the count was reconstructing** — offset-equals-total as a completion sentinel — on a low-rate status characteristic, and reading completion off the device rather than inferring it took the same study from 0 completed transfers to 34 of 34. **The primitive set expressed both versions fine; what the fixture could not tell anyone is *which* to write.** So: **a manifest should branch on a state the DUT reports, not on a quantity the manifest accumulates, wherever the DUT reports one** — accumulation is only correct when no input can be lost, and this execution path can lose input by construction. The fixture is not wrong and is not being changed — it proves the primitives, which is what it was chosen for — but it is a *fixture*, and this paragraph exists so nobody reads it as a recommended shape.

**A second finding about what to declare at all:** the real manifest deliberately does **not** name the bulk data characteristic as a source, even though the download is what it exists to drive. A tap on a protocol source is fed from the interpreter's own dequeue, **so the queue's drops are the tap's drops**; the bulk characteristic belongs on a selective monitor window and the protocol keeps the control/status pair. Same five minutes: 28,548 bytes → 714,927.
