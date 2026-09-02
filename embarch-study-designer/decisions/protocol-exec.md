# embarch-study-designer decisions: Executing a protocol

**Status:** active, 2026-09-02.

What a `RunProtocol` step does on the bench, and what a run is allowed to report.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 60 — `Action::RunProtocol` — stateful sequencing, executed by dev-bench

`{ protocol: u8, entry_state: u8 }` hands the link to a declared state machine for the length of one step. Named states, `on_enter` writes, `on_event <frame>` transitions with `remember`/`when`/`otherwise`, `on_timeout … retry N`, and terminal states mapping to the existing `Outcome`. It spans steps the way `GattMonitorStart`/`GattMonitorStop` (decision 36) does, but where that pair opens a time window this one runs a machine — which is what decision 39's rejected `StreamSend`/`StreamExpect` was reaching for and could not express. The executor shipped the same day ([embarch-dev-bench/decisions.md](../../embarch-dev-bench/decisions.md) decision 41).

**Where the loop closes was the hard question, and the first answer was wrong.** The draft asserted both that `RunProtocol` "crosses the postcard wire to dev-bench like every other `Action`" *and* that the interpreter is `std`-only and host-side. Those are incompatible: something has to close decode → decide → write. Two arguments were made for Core closing it and **both were mistaken, recorded because the correction is the reasoning**:

- *"The board is at 98.5% of `sram0_0_seg`."* Real but stale — the pre-decision-54 number. Deleting `gatt_activity` took the ESP32-C5 to **81.12%**, and reversals row 60 found another ~10.5 KB was a mis-sized inbound buffer. There is room.
- *"Core in the loop is too slow."* At 1 Mbaud a Core↔bench round trip is single-digit milliseconds against a BLE connection interval of 7.5–30 ms that already dominates a chunked download — perhaps 1.1–1.6× on the pump loop, against a stall watchdog measured in seconds. Not the objection it was presented as.

What actually decides it is the third consideration: **under Core-side execution nothing new crosses the wire, but Core would have to send something mid-study for the first time** — the proposal's own unbuilt "v3" tier — and under bench-side execution the manifest crosses but the lifecycle does not change. The repo owner chose bench-side, which keeps `main.c`'s receive-then-run model and Core's silence after `StudyStart` exactly as they are. **The cost is stated rather than hidden:** what a payload *means* now reaches the bench, which is the knowledge decision 39 took away from it and decisions 52 and 55 each restated — `struct dbm_stream_tap` drops `encoding` for precisely this reason. Decision 59's split keeps that cost to the smallest set of primitives a machine can actually reach, and the mid-study write tier stays unbuilt, which is the compensating simplification.

**Nothing here can transition on a write's own ATT response**, whether or not it is `with_response`, and that is deliberate. On the DUT this was designed against, a control-point write's response confirms only that the write was *accepted*; the authoritative answer arrives later as an independent notification on a different characteristic. A machine that could branch on the ack would be branching on the wrong fact and would look correct doing it. `with_response` selects the ATT operation and nothing else.

**The expression evaluator**, which the draft flagged as open and did not resolve. A small fixed set, and the architecture made it smaller than the draft's:

| In | Why it is there |
|---|---|
| Integer literals (`i64`, decimal or `0x`) | The only literal a guard needs |
| `session.<var>` | A run's own carried state |
| `<frame>.<field>` | A scalar of the frame that triggered this event |
| `len(<frame>.<span>)` | The only way a byte span's contents affect anything |
| `+` (saturating) | A flow-controlled pump loop must accumulate a count and there is no other way to say it |
| `== != < <= > >=` | One comparison per guard, checkable at a glance |

Out, each for a stated reason: **`++` (byte-span concatenation)** — the draft's `buffer = buffer ++ chunk.payload` accumulated an entire download in a session variable to compare its length against a total. On the bench there is nowhere to put those bytes and nowhere they are needed: the chunks are already streaming out on their own tap as they arrive, so `received = received + len(chunk.payload)` says the same thing in eight bytes of state. Session variables are therefore **integers only**. **`-`, `*`, `/`, `%`** — no worked protocol needs one, and each is a permanent widening. **`&&`, `||`, `!`** — `a && b` is two states and `!a` is swapping `when` and `otherwise`; neither omission costs an author a protocol they could otherwise write. **Nesting and parentheses** — an expression is `operand [+ operand]` and a guard is `operand cmp operand`, one level. **Any function but `len()`**, and any user-defined one at all.

Addition **saturates** rather than wrapping: a wrapping counter is a plausible wrong number, the failure this crate keeps refusing, and a saturated one stops a guard passing, which the step timeout catches and reports. An operand that cannot resolve — a field a truncated notification did not carry — makes a guard **false**, never true, and makes a write **not happen** rather than happen with a zero substituted in.

**One finding came out of writing the tests rather than the design**, and it is in §4.9's worked example for that reason. An `on_event` arm with no `otherwise` consumes the frame, applies its `remember`s, and stays in the state *without re-entering it* — no `on_enter` re-send, timeout still running from the original entry. `otherwise: goto <this state>` is a different thing: it re-enters, which re-sends the flow-control ack and restarts the stall watchdog. A pump loop needs the second, and the first draft of the fixture wrote the first — it consumed every chunk correctly, acked none of them, and stalled at the watchdog. Both behaviors are real and the author says which.

### 62 — A protocol run reports the state it stopped in, and nothing it could lie about

Decoded fields are addressable by name everywhere inside a manifest — in guards, in `remember`, and in a `write` (decision 61) — which is what makes the state machine expressible at all. **`ProtocolOutcome` is `{ final_state, outcome }`** and nothing more.

Two things the draft wanted here are not built, both because a decision made days earlier already answered them:

- The draft had `StepResult` carrying a bounded `heapless::Vec` of every decoded field a run saw, addressable by path. That is the exact shape decision 54 retired `StepResult.gatt_activity` for, one week earlier and on measurement: a bounded in-memory copy of something unbounded and streamed lets a result *look* complete while holding a fraction of what arrived. Decoded values reach a reader the way every other captured byte does — through the tap the study declared, rendered host-side. So `ProtocolOutcome` carries the one thing the tap file structurally cannot say. Whether that state was terminal is not stored either — it is a lookup in the `ProtocolDef` the `Study` already carries, and a stored copy could disagree with it.
- The draft had decoded output reaching `Study.validations`. **There is no such field**: decision 48 removed post-hoc validation outright. Its terminal states are the assertion instead — a manifest declares `outcome: pass|fail` where the protocol knowledge lives, and a study passes or fails on which one it reaches. §7's standing position on the rest is unchanged: checks over real capture data get designed against that data, and a real `RunProtocol` run is the first thing that will produce any.

**Where a `ProtocolOutcome` lands, confirmed rather than assumed.** `EventsJsonWriter` hand-writes only the *envelope* — `study_name`, the `steps` array's brackets, `provenance`, `streams` — and serializes each `StepResult` through serde, so this field reaches `events.json` automatically and a test asserts it does. It reaches `GET /study/{id}` with it (`result` is that file read back as a `Value`) and rides the `StepCompleted` SSE event, which carries the whole `StepResult`. `streams/index.json` deliberately says nothing about it: that file describes declared capture channels, and a protocol run is not one — it writes through whatever taps the study already declared.

**`StreamEncoding::GattDecoded` is not added either.** The draft proposed it as a passive-capture counterpart mirroring `OutpostTrace { manifest_crc }` — a precedent that no longer exists (decision 58) — and it would have been a second rendering path for GATT notifications one day after decision 52 shipped the first. Instead an `.eap` frame flat enough to be one **lowers into decision 52's own `StructLayout`**, so a frame an engineer already described for a state machine does not have to be described again in TOML to also be rendered. One rendering mechanism, two front ends. A frame the layout cannot express — a `count_from` repeat, a bitpack, a trailing CRC — gets **no layout rather than an approximate one**, decision 52's own rule: the raw `.bin` is on disk either way, so a missing rendering can be redone and a wrong one silently misreads every row.

---

