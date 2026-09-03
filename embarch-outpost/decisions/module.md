# embarch-outpost decisions: The module and its boundary

**Status:** active, 2026-09-02.

A Zephyr module compiled into someone else's firmware, and what it is allowed to decide.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 1 — A Zephyr module consumed by west, compiled into the DUT's own firmware

Not a library the DUT links, not a sidecar image, not something Core flashes separately. The DUT's repo adds it to its west manifest and turns it on with Kconfig. **It is the only shape that can see a kernel hook at all — the instrumentation has to be in the same image as the kernel it is instrumenting.**

**Every board-specific fact is declared in the DUT's own repo, never here.** Which UART peripheral, which pins, what baud, how big the ring is: **all of it is devicetree plus Kconfig in the consuming project.** That is not tidiness — **an outpost that shipped an opinion about which UART instance to use would be asserting a fact about someone else's board it is in no position to know, and would be wrong for the second consumer.** The module ships mechanism and defaults; **the DUT repo declares the facts.**

*Rejected: a vendor-neutral portable C core with a porting layer.* Genuinely wider reach, and **genuinely more design for a reach nothing currently needs** — both real DUT repos in play are Zephyr. **Revisit when a non-Zephyr DUT is real, not before.**

### 14 — Repo: [gabrieltetar/embarch-outpost](https://github.com/gabrieltetar/embarch-outpost), created empty ahead of implementation

Matching how every other sub-project started, and for the concrete reason: **a west module needs somewhere for a DUT firmware repo's manifest to point.**

### 21 — The public header is includable in a build that does not have the module, and its marker macro compiles to nothing there

The header was already written for this — **its markers-compiled-out path no-ops, and its own comment says an unregistered name is a build error *"whether or not markers are enabled".*** **That design was defeated by this module's CMake, not by the header:** the include directory sat **below** the `if(NOT CONFIG_EMBARCH_OUTPOST) return()` guard, **so the header did not resolve at all in a build without the module. The no-op path could never be reached from an application, and the compile-time name check could never run in the build where a typo costs the most — the shipping one.**

**The cost landed exactly where markers earn their keep.** A marker is worth most in a hot path — a driver's drain loop, a queue's overflow branch, a library's error return — **code compiled into both the tracing image and the shipping one.** Reaching any of those meant **the application wrapping every call site in its own `#ifdef` and hand-rolling the fallback the header already contained.**

**So the include directory sits above the guard**, which is safe because **with the module off the header's entire content is an enum and two macros that expand to nothing** — no sources, no symbols, no code. And **the no-op degrades in three tiers rather than two**: the third drops the name check, because **with no registration header included there is no enumerator to check against, and referencing one would fail every call site rather than catch anything.**

**A compile-only test pins it**: an application that includes the header and calls the macro with the module disabled, in the same test runner as the rest.
