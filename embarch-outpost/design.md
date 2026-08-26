# embarch-outpost: design

**Status: design-only, 2026-08-25.** [gabrieltetar/embarch-outpost](https://github.com/gabrieltetar/embarch-outpost) exists (created this session, empty). No code yet. Every decision below was settled in one scoping pass and every load-bearing claim about Zephyr's tracing subsystem was **verified against a real Zephyr checkout** (`zephyr/subsys/tracing`, NCS-vendored) rather than taken from memory or documentation — two of the claims that pass was originally going to assert turned out to be wrong, and are recorded as findings in §3 rather than quietly corrected.

## 1. Purpose and scope

`embarch-outpost` is **the first EmbArch component that ships inside the thing under test.** Every other sub-project observes a DUT from outside it — Core through a debug probe, dev-bench over the air, `embarch-api` over HTTP. The outpost is a small Zephyr module an engineer compiles into their *own* DUT firmware, for debug builds, that emits a running account of what the MCU is actually doing — which thread ran, when, for how long, when it was in interrupt context, and whatever application-specific spans the engineer chose to mark — out a dedicated TX-only UART, to be recorded and rendered host-side.

The question it answers is the one no external instrument in this suite can: **"the study passed, but what was the CPU doing while it did?"** A `Study` today can tell you a GATT write produced a notification 40 ms later. It cannot tell you whether those 40 ms were one busy thread, forty context switches, or an ISR storm.

**Why this is not a violation of the no-inference rule.** [embarch-study-designer/design.md](../embarch-study-designer/design.md) §3 decision 35 forbids any EmbArch component presenting an inference about what a specific piece of hardware or firmware does as established fact. The outpost is the structural opposite of an inference: the engineer compiles it in, chooses what to mark, and ships a build-time manifest declaring what every ID means. Nothing here reads a DUT's source and guesses. It is the explicit engineer-supplied-knowledge pipeline that rule implies should exist, applied to timing rather than to GATT semantics.

**v1 scope, explicitly bounded:**

- **TX-only.** The DUT talks; nothing talks back. No host commands, no runtime enable/disable, no `CONFIG_TRACING_HANDLE_HOST_CMD` equivalent. The protocol is designed so a receive direction can be added later without a reshape (§4), but there is no RX path, no flow control, and no acknowledgement of any kind in v1.
- **Study-scoped capture, rendered post-hoc.** Core opens the outpost link for the duration of a `Study` and closes it after. There is no always-on mode and **no live feed** — settled explicitly (§3 decision 10), against the original framing of this work, which asked for realtime. The timeline is drawn from the recorded stream once the study completes.
- **Zephyr only.** One vendor-neutral shared core is *not* being designed up front; this is a Zephyr module using Zephyr's own `sys_trace_*` hook contract (§3 decision 2). A bare-metal or other-RTOS port would need a real porting layer that does not exist and is not being speculatively designed.
- **No power, no GPIO, no stimulus.** The outpost observes its own MCU. It does not sample, drive, or measure anything.

`embarch-outpost` is **not**:
- A production feature. It is a debug build's instrumentation, sized and defaulted accordingly.
- A logging library. The DUT's own `printk`/`LOG_*` output is a different stream with a different shape, and pointing the outpost at it would make the two indistinguishable. A DUT console is a legitimate *second* signal under §3 decision 11's routing model — it is not this one.
- A replacement for a debugger, an ETM trace probe, or SystemView. It is deliberately the cheap, wire-thin version: one UART pin, no probe bandwidth, no vendor tool.

## 2. Architecture overview

```
        DUT firmware (engineer's own repo, debug build)
        ┌────────────────────────────────────────────────┐
        │  Zephyr kernel                                 │
        │    sys_trace_k_thread_switched_in/out()  ──┐   │   CONFIG_TRACING_USER
        │    sys_trace_isr_enter/exit()             ├──▶ │   hooks — outpost
        │    sys_trace_idle()                       │   │   implements them
        │                                           │   │
        │  application code                         │   │
        │    OUTPOST_EVT(PPG_FRAME_BEGIN, n)  ──────┘   │   engineer-placed
        │                                               │   markers, build-
        │              ▼                                │   registered IDs
        │      lock-free record ring  (outpost-owned)   │
        │              ▼                                │
        │      drain thread → COBS frames → uart_tx()   │   async/DMA, TX-only
        └───────────────────────┬────────────────────────┘
                                │  outpost UART, TX only
                                │
             ┌──────────────────┴───────────────────┐
             │                                      │
       route = direct                        route = via-dev-bench
       (today — "dev-bench bypass")          (not yet possible: no hardware)
             │                                      │
             ▼                                      ▼
    USB-UART bridge on the                 dev-bench RX pin ──▶ byte
    Core machine                           pass-through over its existing
             │                             link — dev-bench never interprets
             │                                      │
             └──────────────────┬───────────────────┘
                                ▼
                          embarch-core
              opens the tap for the study's duration, writes
              streams/outpost.bin verbatim, decodes against the
              build-time manifest into streams/outpost.trace.csv
                                │
                                ▼
                          embarch-ui — timeline, post-hoc
```

Two properties carry the design:

1. **The route is a bench fact, not a study fact.** A `Study` names the *signal* (`outpost`); [embarch-topology](../embarch-topology/design.md) resolves which carrier currently delivers it. The same study runs unchanged before and after the pass-through hardware exists (§3 decisions 11, 12).
2. **Nothing between the DUT and Core interprets a byte.** Core decodes, against a manifest the DUT's own build produced. Whichever carrier is in use moves bytes and stamps nothing but arrival.

## 3. Locked-in design decisions and rationale

1. **The outpost is a Zephyr module (C), consumed by west, compiled into the DUT's own firmware — not a library the DUT links, not a sidecar image, not something Core flashes separately.** The DUT firmware repo adds it to its west manifest and turns it on with Kconfig. This matches how `embarch-dev-bench` already consumes `embarch-study-designer` (a west-managed project, that doc's §3 decision 8) and is the only shape that can see a kernel hook at all — the instrumentation must be in the same image as the kernel it is instrumenting. §5 has the whole integration path concretely — what the engineer adds, where, and what each thing is allowed to decide.

    **Every board-specific fact is declared in the DUT's own repo, never here.** Which UART peripheral, which pins, what baud, how big the ring is: all of it is a devicetree `chosen` node plus Kconfig in the consuming project (§5). That is not just tidiness — an outpost that shipped an opinion about which UART instance to use on an nRF54L15 would be asserting a fact about someone else's board that it is in no position to know, and would be wrong for the second consumer. The module ships mechanism and defaults; the DUT repo declares the facts.

   *Rejected: a vendor-neutral portable C core with a porting layer.* Genuinely wider reach, and genuinely more design for a reach nothing currently needs — both real DUT firmware repos in play are Zephyr. Revisit when a non-Zephyr DUT is real, not before.

2. **Trace source: `CONFIG_TRACING_USER`'s kernel hooks plus engineer-placed `OUTPOST_EVT` markers — not CTF, not SystemView, not Percepio, and not a statistical sampler.** Zephyr already calls a fixed set of hooks at exactly the points that answer "what is the CPU doing": `sys_trace_k_thread_switched_in/out`, `sys_trace_isr_enter/exit`, `sys_trace_idle`, plus thread create/abort/suspend/resume/name-set/priority-set/ready/pend. The outpost implements them. No engineer instrumentation is required to get a thread timeline.

   **Verified, not assumed** (`zephyr/subsys/tracing/`), because three things about `TRACING_USER` materially shape everything below and none of them are obvious:
   - **`CONFIG_TRACING_USER` does not select `TRACING_CORE`** (`subsys/tracing/Kconfig`, `CMakeLists.txt`). Zephyr's tracing ring buffer, its sync/async format layer, its drain thread, its backends, and its drop counter are **all** compiled out. The outpost owns the entire emit path — which is why decisions 3/4/5 exist at all, and why they are not "replace Zephyr's backend."
   - **`sys_trace_named_event(name, arg0, arg1)` is an empty macro under `TRACING_USER`** (`subsys/tracing/user/tracing_user.h:447`). Zephyr's own manual-marker API does nothing here. Markers must come from us (decision 6).
   - **`sys_trace_isr_enter()` and `sys_trace_k_thread_switched_in()` take no arguments.** Which ISR, and which thread, must be recovered inside the hook — see decisions 7 and 8.

   *Rejected: `CONFIG_TRACING_CTF`.* CTF is the standard, decodable-by-babeltrace choice, and it was the leading option until the wire cost was checked: every CTF thread event carries an inline `ctf_bounded_string_t` — `CTF_MAX_STRING_LEN` is **20** (`ctf/ctf_top.h:17`) — so a thread switch is roughly 29 bytes rather than roughly 8. On a UART, at the switch rates that make a load trace interesting, that is the difference between a stream that fits and one that spends its life dropping. CTF also carries a real, undocumented-here timestamp hazard: `CTF_EVENT` stamps `k_cyc_to_ns_floor64(k_cycle_get_32())` **truncated to `uint32_t` nanoseconds**, which wraps every ~4.29 seconds regardless of clock rate (`ctf/ctf_top.h:52-60`). Rejecting CTF costs tool compatibility and buys a wire the DUT can actually sustain.

   *Rejected: SEGGER SystemView.* Requires RTT over the debug probe, which is a second carrier this suite would then have to model, and is a vendor tool with its own host application — the opposite of "one UART pin, rendered in `embarch-ui`."

   *Rejected: a periodic statistical sampler, and polled `k_thread_runtime_stats`.* Both are cheaper and both answer a smaller question. A sampler cannot see a short ISR; runtime stats give a per-window percentage with no timeline at all. The hooks give an exact timeline for less firmware than a sampler needs.

3. **The outpost owns its own transport: a lock-free record ring, a low-priority drain thread, and the asynchronous UART API (`uart_tx()`/DMA where the SoC has it).** Forced by decision 2 — with `TRACING_CORE` compiled out there is nothing to reuse — but it is also the right answer independently. **Zephyr's stock UART tracing backend writes with `uart_poll_out()`, one byte at a time, in a loop** (`subsys/tracing/tracing_backend_uart.c:70`), and additionally `depends on UART_CONSOLE`. Spinning per byte inside the drain path burns exactly the CPU time the trace is trying to measure. The outpost's own UART instance is a dedicated devicetree node, distinct from the DUT's console.

4. **Wire format: compact fixed-shape records, postcard-encoded, COBS-framed in batches — with an absolute 32-bit cycle count in every record.** The emit path from an ISR is: read the cycle counter, write one record into the ring, return. The drain thread does all framing. Records carry IDs, never strings (decision 9 is what makes IDs sufficient).

   **Timestamps are absolute `k_cycle_get_32()` per record**, not deltas. The cost is four fixed bytes per record and a host-side unwrap; the benefit is that **every record is independently interpretable after a drop**, which matters precisely because decision 5 guarantees drops happen under load. A varint delta scheme is smaller and re-synchronises worse — after a gap, a delta chain has no anchor. Given that the interesting traces are exactly the ones that overflow, resilience beat compactness.

   **The cycle rate is emitted at runtime, in the stream header, not read from the manifest.** `CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC` **defaults to 0 when `TIMER_READS_ITS_FREQUENCY_AT_RUNTIME` is set** (`zephyr/kernel/Kconfig:831-834`) — a real case on SoCs whose timer frequency is not a build-time constant — so a manifest-only rate would silently be zero on exactly those targets. The header record carries `sys_clock_hw_cycles_per_sec()` as observed by the running firmware, and the host derives the wrap period from it rather than assuming one.

5. **Overflow policy: drop, count, and emit an explicit gap record. Never block, never overwrite.** When the ring is full the record is dropped and a counter increments; the next successfully-drained frame carries a gap record naming how many records were lost and the cycle span they were lost across. **The host renders the gap as a gap** — a hole in the timeline, labelled — rather than drawing a continuous, plausible, wrong picture across it.

   This is the one place the outpost must build something Zephyr's own tracing has but does not expose: `tracing_packet_drop_handle()` increments an atomic (`tracing_core.c:145-148`) and **the count never reaches the wire**. A trace that silently omits its own losses is worse than one that admits them, because the losses correlate with load — precisely when the trace matters.

   *Rejected: overwrite-oldest.* Right for a post-mortem ring dumped over a debugger, wrong for a continuous timeline: it discards the beginning of a busy burst and keeps the aftermath. *Rejected as a default, kept as an opt-in Kconfig: block until space.* It is the only way to lose nothing, and it perturbs the timing being measured, so it is available for a deliberate high-fidelity run and off by default.

6. **Manual markers: `OUTPOST_EVT(ID, arg)` with build-registered IDs — and the same registration generates the manifest.** The engineer declares their markers in one place (an X-macro list or a linker-section registration, settled at implementation); that declaration is simultaneously what makes `OUTPOST_EVT(PPG_FRAME_BEGIN, n)` compile and what puts `PPG_FRAME_BEGIN` in the manifest. An unregistered ID is a **build error**, not a mystery integer on the host. No strings cross the wire.

   Forced into existence by decision 2's verified finding that `sys_trace_named_event` is a no-op under `TRACING_USER`. Deliberately **not** implemented by also overriding `sys_trace_named_event` for compatibility with DUT code already using the stock API: that API takes a runtime `const char *`, which means either interning strings on the DUT or putting them on the wire, and both re-introduce exactly the cost decision 2 rejected CTF over. A DUT wanting outpost markers writes outpost markers.

7. **ISR identity: the outpost reads the active vector number in the hook and emits it raw; the manifest resolves it to a handler name from the ELF's own `_sw_isr_table`. Engineer markers stay, for spans *inside* a handler.**

    **Reversed 2026-08-25, same session it was written**, after checking the mechanism against a real Zephyr checkout instead of reasoning about it. The original decision rejected reading the vector register on two grounds — that it is arch-specific code in a module claiming to be portable Zephyr C, and that turning an exception number into a handler name is "a second inference step over the vector table, which is the kind of derived-and-presented-as-fact answer this suite has already been burned by." **The second ground was wrong, and it was the load-bearing one.** Both halves check out as facts, not inferences:

    - **Reading the number is what Zephyr itself does, at the same instant.** `sys_trace_isr_enter()` is called from **inside `_isr_wrapper()`** (`arch/arm/core/cortex_m/isr_wrapper.c:33-37`), in exception context, and three lines later the same function computes `int32_t irq_number = __get_IPSR(); irq_number -= 16;`. Evaluating that expression in the hook is not a heuristic that usually works — it is the identical expression, guaranteed valid at that point, returning the number the wrapper is about to dispatch on. IPSR is still the same exception at `sys_trace_isr_exit()`, so the number is emitted on exit too, which makes nesting and tail-chaining trivial for the host instead of a stack it has to reconstruct.
    - **Resolving the number to a name is an ELF read, not a guess.** `_sw_isr_table[]` is "an array of these structures **indexed by the irq line**" (`include/zephyr/sw_isr_table.h`), each entry `{ const void *arg; void (*isr)(const void *); }`, and `const` unless `CONFIG_DYNAMIC_INTERRUPTS`. The manifest generator walks it at exactly the index the firmware will report and resolves the function pointer against the symbol table — **the same mechanism decision 8 already uses for `_k_thread_obj_*`**, applied to a different table. Nothing is derived, nothing is matched heuristically, and the number on the wire stays raw regardless of whether a name was found.

    So the honest split is not "number vs. name" — it is **"what the kernel dispatches" vs. "what happens inside a handler."** The first is now free and exact. The second is what markers are for: an `OUTPOST_EVT` inside a handler marks a span the kernel has no visibility into, and no vector number can substitute for it. Both, not either.

    **What this genuinely costs, stated rather than buried.** `__get_IPSR()` is Cortex-M; a `CONFIG_EMBARCH_OUTPOST_ISR_IDENTIFY` Kconfig gates it, on by default where the arch supports it and off elsewhere, degrading to the anonymous enter/exit records the hooks give regardless. `CONFIG_ARM_CUSTOM_INTERRUPT_CONTROLLER` builds substitute `z_soc_irq_get_active()` for IPSR in the wrapper — a real variant, explicitly unsupported in v1 rather than assumed equivalent. `CONFIG_DYNAMIC_INTERRUPTS` makes `_sw_isr_table` runtime-filled, so ELF entries may still be `z_irq_spurious` placeholders and those IRQs render as bare numbers. Multi-level interrupt aggregators (`CONFIG_2ND_LVL_ISR_TBL_OFFSET`) put second-level IRQs at a table offset, which the generator must honour or mislabel — named here because mislabelling is the one outcome decision 9 exists to prevent. And the timestamp is wrapper-entry, not handler-entry: a fixed prologue's worth of cycles early, consistently, for every ISR.

8. **Thread names come from the build-time manifest via ELF symbol extraction; anything not covered renders as a raw pointer.** `sys_trace_k_thread_switched_in()` takes no arguments, so the hook reads the current thread pointer — a runtime address, four bytes on the wire, no name. `K_THREAD_DEFINE(name, ...)` expands to `struct k_thread _k_thread_obj_##name` (`zephyr/include/zephyr/kernel.h:858-868`, verified), so a symbol-table walk for `_k_thread_obj_*` in the built ELF yields an exact address → name table at zero wire cost, generated into the manifest alongside the marker IDs.

   **What this does not cover, stated plainly:** a thread created with `k_thread_create()` into a plain `static struct k_thread` has no distinguishing symbol prefix, and identifying it would need DWARF type inspection. Those threads render as raw pointers in the UI. Chosen over emitting runtime name-registration records — which would cover every thread — because registration records put strings back on the wire, and the uncovered case is both rarer and self-evidently fixable by the engineer (declare it with `K_THREAD_DEFINE`, or mark it).

9. **The manifest is a build artifact, CRC-matched against the running firmware, and a mismatch refuses to decode rather than decoding wrong.** The DUT build emits `outpost-manifest.json` — schema version, marker IDs → names, thread addresses → names, record layout version, and a CRC over the whole thing. The firmware emits that same CRC in its stream header record. Core stores the manifest with the study and **will not render a trace whose header CRC does not match the manifest it was given**; it records the raw stream and reports the mismatch.

    This is the whole reason IDs on the wire are acceptable (decisions 6, 8). It is also the failure mode that must be loud: a stale manifest against a rebuilt firmware would silently relabel every marker, producing a trace that is entirely readable and entirely wrong — the worst possible outcome and exactly the class of staleness [embarch-topology](../embarch-topology/design.md) was created to eliminate. The manifest travels to Core the same way the firmware artifact already does, through `embarch-api`'s build step (§5.4, and §7 for the remote-Core gap this inherits).

    **Selection and verification are two questions, answered by two mechanisms — and the post-link CRC patch this decision originally specified was over-engineering, corrected 2026-08-25 the same session.** "Which manifest should I decode this against?" and "is this actually the right one?" are not the same question, and trying to make one exact mechanism answer both is what drove the original design into patching a CRC into the linked image.

    **Selection: the study's own flash binds it.** The manifest belongs to the build the study just put on the DUT — same operation, so there is no interval in which the binding can rot. **This is not the write-ahead-staleness pattern [embarch-topology/design.md](../embarch-topology/design.md) §3 decision 3 exists to eliminate, and the distinction is exactly where that principle's edge lies**: what decision 3 forbids is a *persisted* record of resolved state, consulted at some later, unrelated moment. A binding whose lifetime is the study that created it has no later moment to be wrong in. The original framing of this decision rejected "Core remembers what it flashed" without making that distinction, and was wrong to.

    **Resolved 2026-08-25 by [embarch-study-designer/design.md](../embarch-study-designer/design.md) §3 decision 40**, which is what supplies the flash this selection depends on: a `Study` declares the DUT firmware version it requires, and the operator chooses per run whether to reflash to satisfy it. **Reflash is optional, which matters here** — an outpost trace captured on a run that did *not* reflash falls back entirely to the build-ID check below, and its `StudyResult.provenance` says so (`Declared` rather than `FlashedThisRun`). Note this does **not** retire `embarch-umbrella`'s doctor check 13, as an earlier draft of this entry claimed: a per-study gate only fires when a study runs, while check 13 answers "is this bench current" before anything is attempted at all. The two are complementary, not redundant.

    **Verification: a compile-time build ID in the header record.** `git describe --dirty` on the DUT repo, the outpost module's own pinned revision (§5.1), and a hash of the marker registration list — all knowable at compile time, so this is a generated header rather than an image-patching post-link step. Core compares it against the manifest's copy and refuses to render on a mismatch.

    **The route it travels settled 2026-08-25, and it is not a route of its own: an optional `manifest` part on `POST /flash`'s existing `multipart/form-data` body, plus an optional `manifest_path` field on its JSON body** — a sibling of `firmware`/`firmware_path` on the call that already carries the artifact (`embarch-core/design.md` §3 decision 30, Settlement 1). This decision said the manifest "travels to Core the same way the firmware artifact already does" without naming a shape; making it literally the same request is what makes the selection rule above hold with no machinery: the manifest and the image it describes arrive in **one operation**, so there is no interval in which Core holds one without the other and no "which manifest is current" record to keep. A separate `POST /manifests` would have needed exactly that record — the pattern this decision spent three paragraphs distinguishing itself from.

    **Not built, and closed with a named trigger rather than left as owed work.** Storage, selection, verification and refuse-to-render are four mechanisms and nothing can exercise any of them yet: no build emits a manifest until Phase C's generator exists, no header record exists to check a build ID against, and no `Route::Direct` is physically real until Phase E's bridge is. **The trigger is Phase C emitting a real `outpost-manifest.json` from a real ELF** — a single precondition, since that is also what makes a header record exist. **`embarch-api`'s half is deferred under the identical trigger, settled 2026-08-25** ([embarch-api/design.md](../embarch-api/design.md) §3 decision 39, Milestone 7 Phase B item 2): a sender and a receiver for the same manifest are useless apart, so one trigger governs both rather than each half waiting on the other. What *is* live today is this decision's failure behavior, reached from the other side: `embarch-core` writes an `OutpostTrace` tap's raw bytes and **renders nothing**, because it has no manifest and will not guess one. Same outcome, arrived at by having nothing rather than by having the wrong thing.

    **Each mechanism covers precisely the other's blind spot**, which is why both and not either. Flash-binding is exact through a dirty-tree rebuild — the common case during active debugging, and the one a `-dirty` build ID cannot distinguish. The build ID catches a DUT flashed out-of-band between the study's flash and its capture — a bare `west flash` or an IDE button, entirely normal, and the case flash-binding is blind to. Neither alone is sufficient; together they cover what the post-link CRC patch covered, without the build machinery.

    **What is genuinely given up**, stated rather than glossed: a DUT flashed out-of-band from a *dirty* tree that happens to carry the same `-dirty` string still decodes against the wrong manifest. That is the one residual hole, it is narrow, and it is the price of not patching the image. If it ever bites for real, the post-link CRC stamp is the known fix and this entry is the record of why it wasn't paid for up front.

    The same header record makes a `doctor`-style staleness check possible for the DUT, mirroring `embarch-umbrella`'s existing check 13 for dev-bench firmware ([embarch-dev-bench/design.md](../embarch-dev-bench/design.md) §3 decision 25): the running firmware reports its outpost version and manifest CRC, and that can be compared against the module revision currently checked out. Not built here; named because the mechanism is now free.

10. **Capture is study-scoped and rendered post-hoc. There is no live feed.** Core opens the outpost tap when a `Study` starts and closes it when the study ends; the timeline is drawn from the recorded stream afterwards.

    **This reverses the framing this work opened with** — "debug MCU load in realtime and see what the CPU is doing over time" — and the reversal was made deliberately, by the user, when the two halves were put side by side. It is worth recording why rather than letting the doc quietly disagree with its own motivation. A live feed costs a decode-and-push path in Core, an SSE channel, and a renderer that can draw a partial timeline, all before the first byte has ever been captured — and the actual debugging question ("what was the CPU doing during that study") is answered just as well by a complete recording as by a partial live one. Always-on capture is a plausible later addition; it is not a v1 requirement, and pretending it was would have shaped the port-ownership design around a case nobody asked to use yet.

11. **"Dev-bench bypass" is not an outpost feature — it is a general routing property of a new topology entity, the DUT signal link.** [embarch-topology/design.md](../embarch-topology/design.md) §3 decision 18 introduces it: a named signal originating at the DUT, with a declared **route** — either `direct` (straight to the Core machine, bypassing dev-bench entirely) or `via-dev-bench { pins }`. The outpost UART is the first instance; a DUT console UART, an SWO pin, and eventually a dev-bench-driven stimulus line are the obvious next ones.

    **Today's route is `direct`, for a stated hardware reason, not a design preference.** The intended topology is DUT → dev-bench → Core, because dev-bench is what already owns a validated link to Core and what will eventually correlate a trace against its own BLE view. The bench does not currently have the pins or the pass-through firmware to do it, so the outpost's UART goes to a standalone USB-UART bridge on the Core machine instead. Modelling that as a first-class declared route — rather than as "the temporary way it happens to be wired" — is what makes the eventual move a declaration change instead of a redesign, and what makes the topology diagram able to draw an honest picture of a signal that skips a node.

    **When the route is `via-dev-bench`, dev-bench passes bytes through and interprets nothing** — receives on the declared pin, stamps arrival, forwards. Not decode-and-summarise: putting outpost record semantics inside dev-bench firmware would make dev-bench carry knowledge of a specific DUT's build, which decision 35 rules out and which would also mean reflashing the bench whenever the DUT's manifest changes.

12. **A `Study` names the signal; topology resolves the carrier.** The tap says `outpost`, not "COM7" and not "dev-bench pin 4". This is what makes decision 11 pay: the identical saved study — and saved studies are now a real, versioned artifact ([embarch-study-designer/design.md](../embarch-study-designer/design.md) §3 decision 38) — runs unchanged before and after the bench gains pass-through hardware, on a machine whose bridge enumerates differently, or against a Core running elsewhere. The alternative, naming the concrete source in the study, is more explicit on the wire and re-authors every saved study the day the bench is rewired.

13. **The outpost's capture is a `StreamTap` — which means [embarch-stream-pipeline-proposal.md](../embarch-stream-pipeline-proposal.md)'s inbound half is accepted, and `embarch-study-designer` decision 36's dedicated-variant route is reversed one day after it shipped.** See [embarch-study-designer/design.md](../embarch-study-designer/design.md) §3 decision 39 for the folded-in types and [embarch-decision-reversals.md](../embarch-decision-reversals.md) for the reversal row.

    **The collision was flagged before this was decided, and the decision was made anyway, knowingly.** Decision 36 (2026-08-25) deliberately chose a dedicated `DevBenchMessage::GattTranscriptRecord` plus `gatt.csv` over generalising `StreamChannel`, reasoning correctly that `Sample`'s single `f32` has no room for raw bytes, a direction, or a UUID pair. That reasoning was an argument against *the shape `StreamChannel` had*, not against a generic pipeline — and the proposal's tap model was designed around exactly that objection. The cost is real and is not being minimised: a schema bump (written here as 5 → 6; it landed 2026-08-25 as 7 → 8, since decisions 42/43 were implemented first), a second wire-contract pinning pass in both C and Rust, and edits to firmware that is code-complete and deployed. The offsetting fact, which is what made it affordable: **Milestone 6's dev-bench firmware has not been flashed or run against hardware yet**, so nothing about decision 36's wire shape is load-bearing on a real bench. This is the last moment it is cheap, which is the same argument the proposal made for itself in §1 — it just now applies to `gatt.csv` too.

14. **Repo created 2026-08-25**: [gabrieltetar/embarch-outpost](https://github.com/gabrieltetar/embarch-outpost), empty, ahead of any implementation — matching how `embarch-umbrella`, `embarch-topology`, `embarch-dev-bench`, and `embarch-ui` each started, and for the same concrete reason `embarch-topology/design.md` decision 13 recorded: a west module needs somewhere for a DUT firmware repo's manifest to point.

15. **First consumer: `reference-dut-fw`.** The nRF54L15 already enrolled as `dut`, already flashed through Core, already the target of every milestone here. Cortex-M33, so the concrete numbers this design defers (cycle rate, wrap period, sustainable record rate at a given baud) get measured on a board that is already on the bench rather than estimated.

## 4. Wire format

Concrete enough that implementation is mechanical; every constant below is provisional until the first real capture (§7), and each is exposed as a Kconfig (§5.3).

**Record** — what the emit path writes into the ring:

```
{ cycles: u32,        // k_cycle_get_32(), absolute, host unwraps (decision 4)
  kind:   u8,         // ThreadSwitchIn | ThreadSwitchOut | IsrEnter | IsrExit
                      // | Idle | ThreadCreate | ThreadName | Marker | Gap | Header
  a:      u32,        // kind-dependent: thread pointer, marker ID, dropped count
  b:      u32 }       // kind-dependent: marker arg, gap cycle-span; 0 where unused
```

**Header record**, emitted once at startup and repeated periodically so a host attaching mid-stream can decode: `manifest_crc: u32`, `cycles_per_sec: u32` (runtime-read, decision 4), `record_layout_version: u8`, `outpost_version`.

**Framing**: the drain thread postcard-encodes a batch of records, COBS-frames it, and hands it to `uart_tx()`. COBS matches what the Core⟷dev-bench link already uses ([embarch-study-designer/design.md](../embarch-study-designer/design.md) §3), so Core's existing framing code shape applies. A CRC over each frame lets the host discard a partial frame rather than mis-decode it.

**Reserved for a future RX direction**: nothing in v1 sends anything to the DUT, but the frame header reserves a type field so a later command channel is an added frame type rather than a reshape.

**Host-side outputs**, both under the study's `streams/` directory:
- `outpost.bin` — the raw framed stream, written verbatim as it arrives, before any decoding. Always written, even when the manifest CRC does not match, so a mismatch is recoverable rather than a lost run.
- `outpost.trace.csv` — decoded records, one per row, with names resolved through the manifest and gaps present as explicit rows.

## 5. Integration into a DUT firmware project

The full path from "this repo exists" to "I am reading a trace." Nothing here is exotic — it is Zephyr's ordinary module mechanism, which is the point.

### 5.1 Getting the module in, and pinning its version

`embarch-outpost` is a Zephyr module: a `zephyr/module.yml` at its root pointing at its own `CMakeLists.txt` and `Kconfig`. A DUT firmware repo consumes it the way `embarch-dev-bench` already consumes `embarch-study-designer` — as a west-managed project (that doc's §3 decision 8) — by adding it to its own `west.yml`:

```yaml
  - name: embarch-outpost
    url: https://github.com/gabrieltetar/embarch-outpost
    revision: v0.1.0          # <- this is where the version lives
    path: modules/embarch-outpost
```

**`revision` is the answer to "how does the outpost version end up in the DUT firmware project."** It is pinned in the consuming repo's manifest, committed alongside that firmware's own history, and updated by a deliberate bump plus `west update` — never floating. A repo that does not own its west manifest (a downstream app in someone else's workspace) uses `ZEPHYR_EXTRA_MODULES` instead; same module, different plumbing.

That pinned revision then shows up in three places that have to agree, which is the property worth having: the module's `git describe` goes into the manifest (§5.3), the firmware emits it in its header record, and a `doctor`-style check can compare the running DUT against the revision currently checked out — the mechanism [embarch-dev-bench/design.md](../embarch-dev-bench/design.md) §3 decision 25 already established for dev-bench firmware.

### 5.2 Turning it on, and declaring the board facts

Three things in the DUT repo, none of them in this one:

**A Kconfig fragment**, kept in a debug-only overlay (`overlay-outpost.conf` or a build type) rather than in `prj.conf`, since this is debug instrumentation and should not be in a shipping image by accident:

```
CONFIG_EMBARCH_OUTPOST=y
```

which `select`s `TRACING`, `TRACING_USER`, `TRACING_ISR`, and `THREAD_NAME` itself — the engineer sets one symbol, not five, and cannot half-enable it.

**A devicetree `chosen` node**, in the DUT's own board overlay, naming the UART the trace goes out of:

```dts
/ {
    chosen { embarch,outpost-uart = &uart21; };
};
&uart21 {
    status = "okay";
    current-speed = <1000000>;
    pinctrl-0 = <&uart21_default>;   /* the engineer's pins, on the engineer's board */
};
```

This is deliberately the identical shape Zephyr's own tracing backend uses (`DT_CHOSEN(zephyr_tracing_uart)`, `subsys/tracing/tracing_backend_uart.c`) — a convention a Zephyr engineer already knows, not an EmbArch invention. **It is also what removes "which UART instance and pin on the nRF54L15" from this doc's open questions**: it was never this project's fact to hold.

**Marker declarations**, if the engineer wants spans the kernel cannot see — one registration list in one header, which is simultaneously what makes the macro compile and what generates the manifest's ID → name table (decision 6):

```c
#define OUTPOST_MARKERS(X)      \
    X(PPG_FRAME_BEGIN)          \
    X(PPG_FRAME_END)            \
    X(RADIO_IRQ_BODY)
```

then, anywhere including inside an ISR: `OUTPOST_EVT(PPG_FRAME_BEGIN, frame_no);`

### 5.3 Kconfig surface

Everything tunable is a Kconfig on the module, so no consuming repo ever edits outpost source. Provisional defaults; §7 is explicit that none of them are measured yet.

| Symbol | Default | What it decides |
|---|---|---|
| `EMBARCH_OUTPOST` | `n` | Master switch; selects the tracing symbols above |
| `EMBARCH_OUTPOST_BAUD` | `0` | `0` = use the chosen node's `current-speed`; non-zero calls `uart_configure()` at init, so the trace can run faster than a board overlay other things also depend on |
| `EMBARCH_OUTPOST_RING_BYTES` | `4096` | Record ring size — the direct trade against drop rate (decision 5) |
| `EMBARCH_OUTPOST_BATCH_BYTES` | `256` | Bytes the drain thread accumulates before a `uart_tx()` |
| `EMBARCH_OUTPOST_THREAD_PRIORITY` / `_STACK_SIZE` / `_WAIT_MS` | low / `1024` / `100` | The drain thread. Mirrors `CONFIG_TRACING_THREAD_*`'s own shape |
| `EMBARCH_OUTPOST_TRACE_THREADS` / `_ISRS` / `_IDLE` / `_MARKERS` | `y` | Which hook families emit at all — turning one off is the first lever when the drop rate is too high |
| `EMBARCH_OUTPOST_ISR_IDENTIFY` | `y` on Cortex-M | Read the active vector number (decision 7); off degrades to anonymous ISR enter/exit |
| `EMBARCH_OUTPOST_OVERFLOW_BLOCK` | `n` | Opt into blocking instead of dropping, for a deliberate high-fidelity run (decision 5) |
| `EMBARCH_OUTPOST_HEADER_INTERVAL_MS` | `1000` | How often the header record repeats, so a host attaching late can still decode |

### 5.4 Build output, and what the engineer never has to do

The module adds a post-link CMake step emitting **`outpost-manifest.json`** into the build directory beside `zephyr.hex`, and patching its CRC into the image (decision 9). It contains the outpost version, the record layout version, the runtime cycle-rate symbol, the marker ID table, the `_k_thread_obj_*` thread table (decision 8), and the `_sw_isr_table` handler table (decision 7).

**The engineer never handles that file.** `embarch-api`'s `build`/`build_and_flash` picks it up and hands it to Core alongside the artifact ([embarch-api/design.md](../embarch-api/design.md) §3 decision 39) — because the failure mode of forgetting is not a visible error but a silently mislabelled trace, and the only reliable fix is for the manifest to travel automatically with the build that produced it.

### 5.5 The whole loop, once

Per bench, once: declare the signal's route in `embarch-ui`'s Topology tab ([embarch-ui/design.md](../embarch-ui/design.md) §3 decision 10) — `direct`, plus the USB bridge's serial.

Per firmware repo, once: the four steps in §5.1/§5.2.

Per study, thereafter: add an `outpost` tap to the `Study`, run it, read the trace. `west update`s and rebuilds carry the manifest along on their own.

## 6. Relationship to existing sub-projects

- **[embarch-topology](../embarch-topology/design.md)** — owns the new DUT-signal-link entity and its route (§3 decision 11; that doc's §3 decision 18). It is the only place that knows whether `outpost` currently arrives via a USB bridge on the Core machine or via dev-bench, and the only place a human declares it.
- **[embarch-core](../embarch-core/design.md)** — opens the tap for the study's duration, writes `streams/`, stores the manifest the study's own flash bound to it, decodes against that manifest, and serves the results. Core is the only process that touches the serial port, exactly as it is for the dev-bench link and for `/serial-log`. **Half of this is built as of 2026-08-25** (that doc's §3 decisions 30/31, Milestone 7 Phase B item 1): the tap opens a `Route::Direct` signal's own port, `streams/` is written raw-first, and an `OutpostTrace` tap keeps its bytes and renders nothing. Manifest storage and the build-ID check are **deliberately not built**, closed with a named trigger — Phase C emitting a real manifest — since nothing can produce one to store. **[embarch-api](../embarch-api/design.md)'s pickup-and-send half is closed under the same trigger** (2026-08-25, Phase B item 2), rather than shipping a sender against a receiver that does not exist.
- **[embarch-study-designer](../embarch-study-designer/design.md)** — owns `StreamTap` and the accepted inbound pipeline types (§3 decision 13; that doc's §3 decision 39). The outpost adds one `StreamSource` variant and one `StreamEncoding` variant; it does not get its own parallel type family.
- **[embarch-dev-bench](../embarch-dev-bench/design.md)** — no work in v1, and that is the point: the bypass route exists so the outpost is not blocked on bench hardware. Gains a pass-through role only when the `via-dev-bench` route becomes real.
- **[embarch-api](../embarch-api/design.md)** — carries the manifest from the build to Core alongside the firmware artifact, and exposes the trace to agents the way `study_gatt_data`/`study_power_data` already expose their streams.
- **[embarch-ui](../embarch-ui/design.md)** — two surfaces: the Topology tab is where a signal's route is declared (§3 decision 11), and a trace view renders the recorded timeline.
- **[embarch-promptu](../embarch-promptu/design.md)** — eventually the natural home for "read this trace and tell me where the time went," but nothing here depends on it.

## 7. Open questions

- **Every wire constant's *value*** — the Kconfig defaults in §5.3. Baud, ring depth, batch size, drain-thread priority and wait threshold, and the sustainable record rate that follows from all of them; each is now a knob rather than a hardcoded guess, which makes them tunable but no more measured. Nobody has put a single outpost byte through a real UART. The binding measurement is records-per-second at the chosen baud versus the actual switch rate of a real reference-dut build — the drop rate is the answer, and decision 5 exists because it will not be zero.
- ~~**Which UART instance and pin on the nRF54L15.**~~ **Resolved — it was never this project's question.** Both are declared by a `chosen { embarch,outpost-uart = ... }` node and its `current-speed` in the DUT repo's own board overlay (§5.2), the same shape Zephyr's own tracing backend uses. Baud, ring size, and every other tunable are Kconfigs on the module (§5.3). **Still open: which USB-UART bridge**, a real bench fact — declared by its own USB serial, with the same disambiguation hazard as dev-bench's `link_port_serial` ([embarch-topology/design.md](../embarch-topology/design.md) §3 decision 17), made worse by being the *third* such device on the bench.
- **The cycle counter's actual rate and wrap period on the nRF54L15.** Deliberately not asserted here (decision 4 reads it at runtime for exactly this reason). It determines whether the host's unwrap needs to handle multiple wraps within one study, which is a real correctness question, not a detail.
- ~~**Whether `run_study` gains a flash step.**~~ **Resolved 2026-08-25** — [embarch-study-designer/design.md](../embarch-study-designer/design.md) §3 decision 40: a `Study` declares the versions it requires, and reflash is the operator's per-run choice (`embarch-api/design.md` §3 decision 40). **What stays open is narrower and worth watching**: reflash defaults to off, so the common path still leans on the compile-time build ID alone, with the dirty-tree blind spot decision 9 names. Whether that bites in practice is a question only real use answers.
- **Whether the manifest reaches a Core running on another machine.** It rides the firmware-artifact path, which inherits [embarch-api/design.md](../embarch-api/design.md) §9's known artifact-transfer gap for a remote Core. Same gap, not a new one — but the outpost makes it bite in a second place.
- **What the trace view actually looks like.** A flame-chart-style thread timeline, a per-thread load summary, or both. Deferred to the first real capture rather than designed against imagined data — the same posture [embarch-ui](../embarch-ui/design.md) took to its own tabs.
- ~~**Whether the anonymous interrupt-load total is enough in practice.**~~ **Resolved by revisiting decision 7 the same session** — vector numbers are read directly and resolved against `_sw_isr_table`, so ISRs are named without instrumentation. What replaces it is narrower and real: **the build variants that defeat that resolution** — `CONFIG_DYNAMIC_INTERRUPTS`, multi-level aggregator offsets, and `ARM_CUSTOM_INTERRUPT_CONTROLLER` — none of which have been checked against the reference-dut build's actual configuration yet.
- **Overhead of the instrumentation itself.** Every design choice above is aimed at making the emit path cheap, and none of it is measured. A trace that changes the timing it reports is a real hazard, and the honest check is a build with the outpost compiled out versus one with it in, on the same study.

## Changelog

- 2026-08-25 — **Decision 9's transport settled and its build deliberately deferred, both written into the decision** ([embarch-core/design.md](../embarch-core/design.md) §3 decision 30's two settlements, Milestone 7 Phase B item 1). The manifest reaches Core as an optional `manifest` part on `POST /flash`'s existing multipart body (and `manifest_path` on its JSON body) rather than through a `POST /manifests` of its own — the same request that carries the artifact, which is what makes "the study's own flash binds it" hold with no "current manifest" record to go stale. Storage, selection, verification and refuse-to-render are **not built**: four mechanisms with nothing able to exercise any of them until Phase C emits a real manifest, which is the named trigger. The decision's failure behavior is nonetheless live from the other side — Core writes an `OutpostTrace` tap's raw bytes and renders nothing, because it has no manifest and will not guess. §6's `embarch-core` row updated to say which half exists.

- 2026-08-25 — **Decision 9's remaining dependency resolved by [embarch-study-designer/design.md](../embarch-study-designer/design.md) §3 decision 40**, which supplies the flash its manifest selection leaned on: a `Study` now declares the dev-bench and DUT versions it requires, and reflash is the operator's per-run choice. Two corrections to the entry below, made rather than left standing: reflash is **optional**, so a trace from a non-reflashing run falls back to the build ID alone and its `provenance` records that; and this does **not** retire `embarch-umbrella`'s doctor check 13 — a per-study gate fires only when a study runs, check 13 answers whether the bench is current before anything is attempted.

- 2026-08-25 — **Decision 9's manifest binding reworked, same session — the post-link CRC patch was over-engineering, and the objection that produced it was over-applied.** Prompted directly: *"if we say that every study starts by flashing dev bench and DUT, I think it's not crazy to assume we know the version."* Correct, and the earlier rejection of "Core remembers what it flashed" missed where [embarch-topology](../embarch-topology/design.md) §3 decision 3's principle actually stops — it forbids a **persisted** record consulted at a later, unrelated moment, and a binding whose lifetime is the study that created it has no later moment to be wrong in. Split into two questions with two mechanisms: **selection** by the study's own flash, **verification** by a compile-time build ID (generated header, not an image patch). They cover each other's blind spots exactly — flash-binding is exact through the dirty-tree rebuilds a `-dirty` ID cannot tell apart, the build ID catches the out-of-band `west flash` that flash-binding is blind to. One residual hole kept and named rather than paid for up front. Also surfaced a real dependency this leans on and the suite does not have: **studies flash nothing today**, so flash-per-study is a proposed invariant (§7) whose adoption would retire `embarch-umbrella`'s doctor check 13 and would require a `Study` to reference a build at all.

- 2026-08-25 — **New §5 (integration into a DUT firmware project), and decision 7 reversed the same session it was written.** §5 makes the consuming path concrete — west manifest `revision:` as the version pin, `CONFIG_EMBARCH_OUTPOST=y` selecting the tracing symbols, a `chosen { embarch,outpost-uart }` node plus `current-speed` in the DUT's own board overlay, a marker registration list, and a full Kconfig table — which **closed an open question by relocating it**: which UART instance and pin was never this project's fact to hold, and an outpost that shipped an opinion about it would be asserting something about someone else's board it cannot know. **Decision 7 reversed**: reading the active vector number is not an inference — `sys_trace_isr_enter()` runs inside `_isr_wrapper()` and `__get_IPSR() - 16` is the identical expression Zephyr uses three lines later — and resolving that number to a handler name is an ELF read of `_sw_isr_table[]`, the same mechanism decision 8 already uses for threads. The original rejection conflated "read the number" with "guess the name"; only the latter would have been inference, and it isn't one either. ISRs are now named without instrumentation, with the defeating build variants (`DYNAMIC_INTERRUPTS`, aggregator offsets, `ARM_CUSTOM_INTERRUPT_CONTROLLER`) named as the real remaining limit. **Decision 9 sharpened**: the manifest CRC is stamped post-link into a reserved symbol, because the cheaper compile-time build-ID alternative fails precisely during active debugging, when every rebuild carries the same `-dirty` string — and Core simply remembering which manifest it flashed was rejected as the write-ahead-staleness pattern `embarch-topology` exists to eliminate.

- 2026-08-25 — **Initial design, in one scoping pass.** New sub-project: a Zephyr module compiled into a DUT's own debug firmware, emitting a thread/ISR/marker timeline out a TX-only UART, captured by Core for the duration of a `Study` and rendered post-hoc. Fifteen decisions settled, each with its rejected alternatives recorded. Three claims about Zephyr's tracing subsystem were verified against a real checkout rather than asserted, and each changed the design: `CONFIG_TRACING_USER` compiles out Zephyr's entire ring/drain/backend layer (so the outpost owns its transport), `sys_trace_named_event` is a no-op there (so markers are ours), and the stock UART backend is `uart_poll_out` per byte (so async UART is a real deliverable, not a swap). CTF was rejected on measured wire cost — a 20-byte inline thread name per event — and on a `uint32_t`-nanosecond timestamp that wraps every ~4.29 s. Two decisions reverse things stated elsewhere and say so: capture is post-hoc with no live feed, against this work's own opening framing (decision 10); and the outpost's tap accepts [embarch-stream-pipeline-proposal.md](../embarch-stream-pipeline-proposal.md)'s inbound half, reversing `embarch-study-designer` decision 36's dedicated-variant route one day after it shipped, affordable only because that firmware has not yet run on hardware (decision 13). Repo created, empty. First consumer: `reference-dut-fw`.
