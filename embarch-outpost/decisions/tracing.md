# embarch-outpost decisions: What gets traced

**Status:** active, 2026-09-02.

Kernel hooks, engineer markers, and keeping the instrument out of its own trace.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 2 — Trace source: Zephyr's user-tracing kernel hooks plus engineer-placed markers

Not CTF, not SystemView, not a statistical sampler. **Zephyr already calls a fixed set of hooks at exactly the points that answer "what is the CPU doing"** — thread switch in and out, ISR enter and exit, idle, plus the thread lifecycle — and the outpost implements them. **No engineer instrumentation is required to get a thread timeline.**

**Three properties of that hook layer shape everything below, and none is obvious:**

- **The user-tracing option does not select the tracing core.** Zephyr's ring buffer, format layer, drain thread, backends and drop counter are **all compiled out. The outpost owns the entire emit path** — which is why decisions 3, 4 and 5 exist at all, and why they are not "replace Zephyr's backend."
- **Zephyr's own manual-marker API is an empty macro here**, so **markers have to come from us** (decision 6).
- **The ISR-enter and thread-switch-in hooks take no arguments.** Which ISR, and which thread, **must be recovered inside the hook** — decisions 7 and 8.

*Rejected: CTF.* The standard, decodable-by-existing-tools choice, and **the leading option until the wire cost was checked: every CTF thread event carries an inline bounded string, so a thread switch is roughly 29 bytes rather than roughly 8.** On a UART, at the switch rates that make a load trace interesting, **that is the difference between a stream that fits and one that spends its life dropping.** It also carries a timestamp hazard: its event stamp is **truncated to 32-bit nanoseconds, which wraps every ~4.29 seconds regardless of clock rate.** Rejecting it costs tool compatibility and buys **a wire the DUT can actually sustain.**

*Rejected: SEGGER SystemView.* Needs RTT over the debug probe — **a second carrier this suite would then have to model** — and is a vendor tool with its own host application, **the opposite of "one UART pin, rendered in our own UI."**

*Rejected: a periodic statistical sampler, or polled runtime stats.* Both are cheaper and **both answer a smaller question: a sampler cannot see a short ISR, and runtime stats give a per-window percentage with no timeline at all.** The hooks give an exact timeline **for less firmware than a sampler needs.**

### 6 — Manual markers with build-registered IDs, and the same registration generates the manifest

The engineer declares their markers in one place, and **that declaration is simultaneously what makes a marker call compile and what puts its name in the manifest. An unregistered ID is a build error, not a mystery integer on the host.** No strings cross the wire.

**Keeping that table in the image is a real problem, not a formality.** *Nothing in the firmware reads it* — the generator reads it out of the ELF — **so section garbage collection deletes it and the build still succeeds**, producing a manifest with zero markers and a trace whose markers are bare integers, **with no error anywhere to say why.** Two mechanisms fail: **the iterable-section API looks exactly right and has no effect on the template linker-script path both real targets use**, and a keep directive **survives the Zephyr link and is collected out again by the host link on a native build.** What holds everywhere is **a volatile pointer to the table, read once at init** — a relocation from a section the compiler may not elide.

*Rejected: also overriding Zephyr's stock marker API for compatibility with DUT code already using it.* That API takes a **runtime string pointer**, which means either interning strings on the DUT or putting them on the wire — **both re-introducing exactly the cost CTF was rejected over.** A DUT wanting outpost markers writes outpost markers.

### 19 — The outpost keeps itself out of its own trace by default, and says so on the wire

No record for a context switch into or out of the drain thread, or for an ISR on the vector of the UART the outpost owns. **On a quiet board the steady state was a closed loop of ten records per frame, every one of them caused by transmitting the previous frame** — half the capture was the instrument describing its own transmission at 99% of line rate with the DUT doing nothing.

**Default off, and that is a deliberate reversal of this module's usual posture.** Everywhere else it defaults to reporting more rather than less. **Here the default *removes* information, because the information removed is almost never what anyone wants and its cost is the whole link.** Tracing self is **the honest-but-expensive setting, and exactly right when the thing being debugged *is* the outpost.**

**The header says which, and the flag's clear state is the interesting one.** It is on the wire because **an absence of records is indistinguishable from an idle subject**: a host inferring self-exclusion from "the drain thread never ran" **would be deriving a firmware build option from a measurement**, which is the class of thing the never-infer rule forbids. Core surfaces it beside `named` and `timed` — **a third independent way a trace can be incomplete, and the only one the *firmware* decides.**

**What a host sees instead is an interval no lane covers**, landing in the load summary's unaccounted total, **and a host renders the flag against exactly that number, because that is the number it explains.**

**Thread create and thread name are not excluded, deliberately.** They are two records for a whole capture rather than two per frame, and **between them they are the only thing that names the excluded subject. A self-excluded trace that also hid the drain thread's existence would leave a host with unattributed intervals and nothing to attribute them to.**

**Two limits, stated rather than discovered later.** The ISR half excludes the whole **vector**, so **under shared interrupts anything else on it goes too.** And it needs the devicetree IRQ number to equal the Cortex-M vector number, **so it compiles out under multi-level interrupts rather than comparing against an encoded number that does not match.**

*Rejected: also excluding the idle churn the drain thread causes.* With the drain thread gone, what remains is the idle thread switching out and back in. **Those records are caused by the instrument and are not the instrument: the idle thread really did run. Excluding them would be the trace lying about the CPU rather than declining to describe itself.**

*Rejected: coalescing the drain thread's run into one "the instrument ran here" record.* One record instead of six, **and it would close the hole in the timeline honestly.** Declined because it is **a new record kind, three host decoders and a layout bump for something the header flag plus the unaccounted total already communicates.**

**What it did not do, and this is the more useful half: removing half the records did not move the link's duty cycle at all.** See decision 20 — **the drain loop's shape, not its record count, sets the duty cycle, and cutting records made frames smaller rather than rarer.**
