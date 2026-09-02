# embarch-outpost decisions: What gets traced, and how it is named

**Status:** active, 2026-09-02.

Kernel hooks, engineer markers, and turning a pointer or a vector number into a name.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 2 — Trace source: `CONFIG_TRACING_USER`'s kernel hooks plus engineer-placed `OUTPOST_EVT` markers — not CTF, not SystemView, not Percepio, and not a statistical sampler. Zephyr already calls a fixed set of hooks at exactly the points that answer "what is the CPU doing": `sys_trace_k_thread_switched_in/out`, `sys_trace_isr_enter/exit`, `sys_trace_idle`, plus thread create/abort/suspend/resume/name-set/priority-set/ready/pend. The outpost implements them. No engineer instrumentation is required to get a thread timeline.

   **Verified, not assumed** (`zephyr/subsys/tracing/`), because three things about `TRACING_USER` materially shape everything below and none of them are obvious:
   - **`CONFIG_TRACING_USER` does not select `TRACING_CORE`** (`subsys/tracing/Kconfig`, `CMakeLists.txt`). Zephyr's tracing ring buffer, its sync/async format layer, its drain thread, its backends, and its drop counter are **all** compiled out. The outpost owns the entire emit path — which is why decisions 3/4/5 exist at all, and why they are not "replace Zephyr's backend."
   - **`sys_trace_named_event(name, arg0, arg1)` is an empty macro under `TRACING_USER`** (`subsys/tracing/user/tracing_user.h:447`). Zephyr's own manual-marker API does nothing here. Markers must come from us (decision 6).
   - **`sys_trace_isr_enter()` and `sys_trace_k_thread_switched_in()` take no arguments.** Which ISR, and which thread, must be recovered inside the hook — see decisions 7 and 8.

   *Rejected: `CONFIG_TRACING_CTF`.* CTF is the standard, decodable-by-babeltrace choice, and it was the leading option until the wire cost was checked: every CTF thread event carries an inline `ctf_bounded_string_t` — `CTF_MAX_STRING_LEN` is **20** (`ctf/ctf_top.h:17`) — so a thread switch is roughly 29 bytes rather than roughly 8. On a UART, at the switch rates that make a load trace interesting, that is the difference between a stream that fits and one that spends its life dropping. CTF also carries a real, undocumented-here timestamp hazard: `CTF_EVENT` stamps `k_cyc_to_ns_floor64(k_cycle_get_32())` **truncated to `uint32_t` nanoseconds**, which wraps every ~4.29 seconds regardless of clock rate (`ctf/ctf_top.h:52-60`). Rejecting CTF costs tool compatibility and buys a wire the DUT can actually sustain.

   *Rejected: SEGGER SystemView.* Requires RTT over the debug probe, which is a second carrier this suite would then have to model, and is a vendor tool with its own host application — the opposite of "one UART pin, rendered in `embarch-ui`."

   *Rejected: a periodic statistical sampler, and polled `k_thread_runtime_stats`.* Both are cheaper and both answer a smaller question. A sampler cannot see a short ISR; runtime stats give a per-window percentage with no timeline at all. The hooks give an exact timeline for less firmware than a sampler needs.

### 6 — Manual markers: `OUTPOST_EVT(ID, arg)` with build-registered IDs — and the same registration generates the manifest. The engineer declares their markers in one place (an X-macro list or a linker-section registration, settled at implementation); that declaration is simultaneously what makes `OUTPOST_EVT(PPG_FRAME_BEGIN, n)` compile and what puts `PPG_FRAME_BEGIN` in the manifest. An unregistered ID is a **build error**, not a mystery integer on the host. No strings cross the wire.

   **Keeping that table in the image is a real problem, not a formality** ([embarch-decision-reversals.md](../../embarch-decision-reversals.md) row 41). *Nothing in the firmware reads it* — the generator reads it out of the ELF — so `-fdata-sections --gc-sections` deletes it and **the build still succeeds**, producing a manifest with zero markers and a trace whose markers are bare integers, with no error anywhere to say why. Two mechanisms were tried before the one that works. `zephyr_iterable_section()` looks like exactly the right API and has none: it is built on the CMake linker-script *generator*, and Cortex-M and POSIX both use the template-`.ld` path. A `zephyr_linker_sources(RODATA ...)` `KEEP()` does survive the Zephyr link — and is collected out again by the *second* link, the host link that produces `zephyr.exe` on a native build. What holds on every target is a `volatile` pointer to the table, read once at init: a relocation from a section the compiler may not elide.

   Forced into existence by decision 2's verified finding that `sys_trace_named_event` is a no-op under `TRACING_USER`. Deliberately **not** implemented by also overriding `sys_trace_named_event` for compatibility with DUT code already using the stock API: that API takes a runtime `const char *`, which means either interning strings on the DUT or putting them on the wire, and both re-introduce exactly the cost decision 2 rejected CTF over. A DUT wanting outpost markers writes outpost markers.

### 19 — The outpost keeps itself out of its own trace, by default, and says so on the wire. 2026-08-27. `CONFIG_EMBARCH_OUTPOST_TRACE_SELF`, default **n**: no record is emitted for a context switch into or out of the drain thread, or for an ISR enter/exit on the vector of the UART named by the `embarch,outpost-uart` chosen node.

    **The measurement that forced it.** On a quiet `dut_dev@7` the steady state was a closed loop of exactly ten records per frame, and every one of the ten was caused by transmitting the previous frame:

    ```
    thread_switch_in idle / idle / isr_enter uarte / isr_exit uarte (17 µs)
    thread_switch_out idle / thread_switch_in drain_thread
    isr_enter uarte / isr_exit uarte (3 µs) / thread_switch_out drain_thread / thread_switch_in idle
    ```

    Of the reference capture's 9205 records, **50.4% were the drain thread plus its own UART's ISR** (IRQ 198, confirmed as uart20 out of the devicetree — `interrupts = <0xc6 0x1>`) and **18.6% were the application**, at 99% of line rate with the DUT doing nothing. A frame carried almost exactly the story of its own transmission. Measured after the change: **0.0% self, 68.3% application.**

    **Default n, and that is a deliberate reversal of this module's usual posture.** Everywhere else the outpost defaults to reporting more rather than less. Here the default *removes* information, because the information removed is almost never what anyone wants and its cost is the whole link. `y` is the honest-but-expensive setting and it is exactly right when the thing being debugged **is** the outpost.

    **The header says which, and the flag's clear state is the interesting one.** `OUTPOST_FLAG_TRACE_SELF` is set only under `y`. It is on the wire because **an absence of records is indistinguishable from an idle subject**: a host that inferred self-exclusion from "the drain thread never ran" would be deriving a firmware build option from a measurement, which is precisely the class of thing [embarch-study-designer/decisions.md](../../embarch-study-designer/decisions.md) §3 decision 35 forbids. Core reads the bit onto `streams/index.json`'s `self_excluded`, beside `named` and `timed` — a third independent way a trace can be incomplete, and the only one the *firmware* decides.

    **What a host sees instead of the drain thread's run** is an interval no lane covers, which lands in the load summary's unaccounted total — 1.6% of the reference window. `embarch-ui` renders the flag against exactly that number, because that is the number it explains.

    **`thread_create` and `thread_name` are not excluded**, deliberately. They are two records for a whole capture rather than two per frame, and between them they are the only thing that names the excluded subject. A self-excluded trace that also hid the drain thread's existence would leave a host with unattributed intervals and nothing to attribute them to.

    **Two limits, stated rather than discovered later.** The ISR half excludes the whole **vector**, so under `CONFIG_SHARED_INTERRUPTS` anything else sharing it goes too. And it needs `DT_IRQN` to equal the Cortex-M vector number, so it compiles out under `CONFIG_MULTI_LEVEL_INTERRUPTS` rather than comparing `__get_IPSR() - 16` against an encoded number that does not match it — the same posture `EMBARCH_OUTPOST_ISR_IDENTIFY`'s own `depends on` already takes.

    *Rejected: excluding the idle churn the drain thread causes.* With the drain thread gone, what remains of the loop is the idle thread switching out and back in. Those records are caused by the instrument and are **not** the instrument: the idle thread really did run. Excluding them would be the trace lying about the CPU rather than declining to describe itself.

    *Rejected: coalescing the drain thread's run into one "the instrument ran here" record.* One record instead of six, and it would close the hole in the timeline honestly. Declined for now because it is a new record kind, three host decoders and a layout bump for something the header flag plus the unaccounted total already communicates — revisit if the hole turns out to confuse a reader in practice.

    **What it did not do, and this is the more useful half.** Self-exclusion removed half the records and **did not move the link's duty cycle at all** — 99% before, 96% after. See decision 20: the drain loop's shape, not its record count, is what sets the duty cycle, and cutting records made frames smaller rather than rarer.

