# embarch-outpost decisions: The module and its boundary

**Status:** active, 2026-09-02.

A Zephyr module compiled into someone else's firmware, and what it is allowed to decide.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 1 — The outpost is a Zephyr module (C), consumed by west, compiled into the DUT's own firmware — not a library the DUT links, not a sidecar image, not something Core flashes separately. The DUT firmware repo adds it to its west manifest and turns it on with Kconfig. This matches how `embarch-dev-bench` already consumes `embarch-study-designer` (a west-managed project, that doc's §3 decision 8) and is the only shape that can see a kernel hook at all — the instrumentation must be in the same image as the kernel it is instrumenting. §5 has the whole integration path concretely — what the engineer adds, where, and what each thing is allowed to decide.

    **Every board-specific fact is declared in the DUT's own repo, never here.** Which UART peripheral, which pins, what baud, how big the ring is: all of it is a devicetree `chosen` node plus Kconfig in the consuming project (§5). That is not just tidiness — an outpost that shipped an opinion about which UART instance to use on an nRF54L15 would be asserting a fact about someone else's board that it is in no position to know, and would be wrong for the second consumer. The module ships mechanism and defaults; the DUT repo declares the facts.

   *Rejected: a vendor-neutral portable C core with a porting layer.* Genuinely wider reach, and genuinely more design for a reach nothing currently needs — both real DUT firmware repos in play are Zephyr. Revisit when a non-Zephyr DUT is real, not before.

### 14 — Repo created 2026-08-25: [gabrieltetar/embarch-outpost](https://github.com/gabrieltetar/embarch-outpost), empty, ahead of any implementation — matching how `embarch-umbrella`, `embarch-topology`, `embarch-dev-bench`, and `embarch-ui` each started, and for the same concrete reason `embarch-topology/decisions.md` decision 13 recorded: a west module needs somewhere for a DUT firmware repo's manifest to point.

### 21 — `<embarch/outpost.h>` is includable in a build that does not have the module, and `OUTPOST_EVT()` compiles to nothing there — 2026-08-27. A one-line CMake fix for a defect that made decision 6's markers unusable in exactly the code they are most worth putting in.

    The header was already written for this: its markers-compiled-out path no-ops, and its own comment says an unregistered name is a build error *"whether or not markers are enabled — the failure mode this is arranged to prevent does not depend on a Kconfig."* That design was defeated by this module's `CMakeLists.txt`, not by the header. `zephyr_include_directories(include)` sat **below** the `if(NOT CONFIG_EMBARCH_OUTPOST) return()` guard, so `#include <embarch/outpost.h>` did not resolve at all in a build without the module. The no-op path could never be reached from an application, and the compile-time name check could never run in the build where a typo costs the most — the shipping one.

    **The cost landed exactly where markers earn their keep.** A marker is worth most in a hot path: a driver's drain loop, a queue's overflow branch, a library's error return — code compiled into both the tracing image and the shipping one. Reaching any of those meant the application wrapping every call site in its own `#ifdef CONFIG_EMBARCH_OUTPOST` and hand-rolling the fallback macro the header already contained. Found placing the first real `OUTPOST_EVT()` markers into a DUT's PPG pipeline, where the alternative was adding guards to four files of someone else's product code to work around a header that had the answer built in.

    Two changes. The include directory moves above the guard — it adds no sources, no symbols and no code, since with `CONFIG_EMBARCH_OUTPOST` unset the header's entire content is an enum and two macros that expand to nothing. And the no-op degrades in **three** tiers rather than two, described in §5.2: the third tier drops the name check, because with no registration header included there is no enumerator to check against, and `(void)OUTPOST_MARKER_##id` there would fail every call site rather than catch anything.

    `tests/module_off` pins it: a compile-only application that includes the header and calls `OUTPOST_EVT` with `CONFIG_EMBARCH_OUTPOST=n`. It is in `tests/run-all.sh` alongside the ztest, stream and cross-decoder stages.

    **Validated on real hardware the same day**, which is also the first time this module's markers ran on a DUT at all: five markers declared at a PPG pipeline's sample-drop sites, all five resolved by name in `outpost-manifest.json`, and three `PPG_PULL_DROPPED` records decoded out of a study capture ~100 ms apart — the observe-poll cadence — each carrying the engineer's own argument. Decision 6 shipped 2026-08-26 and had until now only ever been exercised by this repo's own test app.

