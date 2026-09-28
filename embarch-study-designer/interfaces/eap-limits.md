# embarch-study-designer: `.eap` protocol wire constants

**Status:** active, 2026-09-28. Split out of [limits.md](limits.md) the same day
(`tasks/study-designer/067`) — a self-contained group of eighteen rows that
nothing outside protocol work reads, moved verbatim. Every other capacity
constant this crate declares is in [limits.md](limits.md); the types and
grammar these bound are in [eap.md](eap.md); why: [../decisions/protocols.md](../decisions/protocols.md).

**`.eap` protocol manifests** (decisions 58–62). These bound a value dev-bench *executes*, not one it walks past: a `ProtocolDef` rides in `Study.protocols` all the way to the firmware, so every constant below costs real ESP32-C5 SRAM in `struct dev_bench_message`'s union. Sized against the two worked protocols in `eap.md` with headroom, deliberately *not* against the generous ceilings `limits.md`'s table uses — dev-bench remains free to cap tighter still with its own internal limit, exactly as `DBM_MAX_STEPS_PER_STUDY` already does at 16 against `MAX_STEPS_PER_STUDY`'s 64 (`embarch-dev-bench` decision 27). **The SRAM cost has not been measured** — the real number comes from a `west build` ram_report, which is `embarch-dev-bench`'s own scope along with the interpreter itself.

| Constant | Value | Bounds | Sizing |
|---|---|---|---|
| `MAX_PROTOCOLS_PER_STUDY` | 2 | `Study.protocols` (decision 58) | a protocol is only reachable through a `RunProtocol` step, and a study running more than a couple of distinct handshakes is describing two studies |
| `MAX_PROTOCOL_NAME_LEN` | 32 | `ProtocolDef.name` | [assumed] the `protocol <name> { … }` identifier |
| `MAX_SOURCES_PER_PROTOCOL` | 6 | `ProtocolDef.sources` (decision 58) | sized against the real BDS download's three (`ctrl`/`status`/`data`, decision 57) with room for a protocol spanning two services |
| `MAX_SOURCE_NAME_LEN` | 24 | `ProtocolSource.name` | [assumed] the alias a `write`/`frame` refers to |
| `MAX_FRAMES_PER_PROTOCOL` | 8 | `ProtocolDef.frames` | [assumed] only frames a state machine actually reacts to live here; a frame that exists solely to render a capture is a decision-52 `StructLayout` and never reaches dev-bench |
| `MAX_FRAME_NAME_LEN` | 32 | `FrameDef.name` | [assumed] referenced by `on_event <frame>` and by field paths |
| `MAX_FRAME_FIELDS` | 8 | `FrameDef.fields` (decision 59) | the **guard-reachable** scalar reads of one frame, not every field of the real packet — only the ones a `when`, a `remember` or a `write` names |
| `MAX_FRAME_SPANS` | 4 | `FrameDef.spans` | [assumed] a span's *bytes* never reach an expression (decision 60 removed byte-span concatenation outright); only its `len()` does |
| `MAX_EAP_FIELD_NAME_LEN` | = `MAX_STRUCT_FIELD_NAME_LEN` | `ScalarRead.name`/`SpanRead.name` | shares `MAX_STRUCT_FIELD_NAME_LEN`'s size on purpose: the same `.eap` frame can also be lowered into a decision-52 `StructLayout`, and a name that fit one and not the other would be a silent authoring trap |
| `MAX_SELECT_MATCH_LEN` | 8 | `FrameMatch.eq` (decision 59's `select_if`) | sized for a four-byte format magic (`GWF1`, `BSS\x03`) with headroom |
| `MAX_SESSION_VARS` | 6 | `ProtocolDef.session` (decision 60) | [assumed] integers only — the `bytes` session variable the draft carried is gone with `++` |
| `MAX_SESSION_VAR_NAME_LEN` | 24 | `SessionVarDef.name` | [assumed] referenced as `session.<name>` |
| `MAX_STATES_PER_PROTOCOL` | 12 | `ProtocolDef.states` | [assumed] the real BDS download uses six |
| `MAX_STATE_NAME_LEN` | 24 | `StateDef.name`, `ProtocolOutcome.final_state` (decision 62) | [assumed] the one string a protocol run reports back |
| `MAX_EVENT_ARMS_PER_STATE` | 4 | `ActiveState.on_event` | [assumed] distinct frames one state reacts to |
| `MAX_GUARDS_PER_ARM` | 2 | `EventArm.when` | more than one so an author can express a small dispatch without inventing intermediate states; small enough that a real branch stays legible |
| `MAX_REMEMBER_PER_ARM` | 2 | `EventArm.remember` | [assumed] session-variable updates one arm performs before its guards are evaluated |
| `MAX_WRITE_FIELDS` | 6 | `WriteAction.fields` (decision 61) | a control-point write is a one-byte opcode and occasionally an argument; sized for the argument |
