# embarch-topology spec: What each consumer owns now

**Status:** active, 2026-10-26.

Split verbatim from [../spec.md](../spec.md), 2026-10-26, because `tasks/topology/059` had to
write into that file with 690 B left (`tasks/topology/060`). The section below is unchanged from
the version that moved; it is distinct from "What validation asserts", which stays in the spec.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

## What each consumer owns now

- **Probe selection is this crate's, not `embarch-core`'s.** `select_probe` (decision 32) is the
  suite's one implementation of which attached debug probe a caller gets; `embarch-core::resolve_probe`
  delegates to it rather than holding a copy, threading a caller `action` verb (`"enroll"`, `"flash"`,
  `"reset"`, …) through for its error text. Three observable behaviours a caller can rely on
  (decision 33): **zero probes attached** is checked first and always names the usbipd hint; **more
  than one probe attached with no serial given** refuses, naming the count and every attached probe's
  identifier and serial; **a given serial that matches nothing attached** refuses by name. Every error
  string is part of the contract — see decision 33 for the exact wording of each.
- **`embarch-core`** keeps the hardware I/O, calling the crate for which port or probe, and whether valid — no copy of that logic, and **no dev-bench port override env var.**
- **`embarch-api`** links the crate **without the hardware feature** — only its `base_url = "auto"` branch calls it; the declared-address fast path does not.
- **`embarch-umbrella`** does the same; its env module is **just "am I under WSL2"**, still needed standalone by its Windows-binary lookup.

**Three features, and the middle one is new** (decision 31). `software` (default) is topology-class detection and Core-reachability probing, needing `reqwest`/`tokio`. `wire` is `serde` and nothing else: the hardware module's plain data types — `EnrolledBoard`, `Alert`, `DetectedPort`, `SignalLink`, `Route`, `SignalDirection` — with every function that reads a probe, enumerates a port or writes `enrollment.toml` compiled out. `hardware` is those functions, implies `wire`, and needs `probe-rs`/`serialport`; `embarch-core` is its only consumer.
