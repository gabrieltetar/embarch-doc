# embarch: glossary

**Status:** draft, 2026-08-15. Added closing item 22 of that day's design-improvement review (`.claude/design-improvements-2026-08-15.md`, local working notes — not committed): DUT, study, target, project, board qualifier, topology class, and discovery kind are all load-bearing terms used across every design doc in this repo, and none of them had one place defining what they mean. This doc doesn't restate any sub-project's design — it links to the section that owns each term, per `DOC-PROTOCOL.md` §5's "link, don't restate" rule.

| Term | Meaning | Owning doc |
|---|---|---|
| **DUT** | Device Under Test — the physical firmware/hardware being flashed, reset, or bench-tested. Distinct from dev-bench, which plays the DUT's BLE *counterpart* during a study, not the DUT itself. | [embarch-core/design.md](embarch-core/design.md) §1 |
| **Core** | `embarch-core`, the OS-level service owning the debug probe and serial console; the lowest layer in the suite. | [embarch-core/design.md](embarch-core/design.md) §1 |
| **project** | A named, configured build target in `embarch-api`'s config — one entry in `[[projects]]`, corresponding to one firmware repo/build (`discovery = "static"`) or a whole Zephyr/west repo's live-scanned surface (`discovery = "zephyr-west"`). | [embarch-api/design.md](embarch-api/design.md) §4 |
| **target** | One concrete, buildable (board, soc, cpucluster, variant, revision, app) combination within a `discovery = "zephyr-west"` project — what `list_targets` enumerates and `build`/`flash`'s four selection params narrow down to. Not the same as a *project*: one project can have many targets. | [embarch-api/design.md](embarch-api/design.md) §3 decision 12 |
| **discovery kind** | `static` (today's schema — a hand-authored `[[projects]]`/`[[projects.targets]]` entry) or `zephyr-west` (live filesystem+YAML scan, no stored build command/chip). A per-project config field, not a global mode. | [embarch-api/design.md](embarch-api/design.md) §3 decision 12 |
| **board qualifier** | Zephyr's own naming grammar for a buildable target: `<board>@<revision>/<soc>/<cpucluster>/<variant>` (revision and variant optional). What `west build -b` actually takes. | [embarch-zephyr.md](embarch-zephyr.md) §2 |
| **chip** | An opaque `probe-rs` target name (e.g. `nRF54L15`, `STM32F407VG`) — a different namespace from a Zephyr SoC name, with no mechanical mapping between them except `embarch-core`'s own `SOC_TO_CHIP` table. | [embarch-core/design.md](embarch-core/design.md) §3 decision 8 |
| **probe** | A physical debug probe (ST-Link, J-Link, CMSIS-DAP, FTDI, ESP USB-JTAG) `probe-rs` can attach to. Dev-bench's on-board J-Link counts as a second probe once dev-bench hardware exists. | [embarch-core/design.md](embarch-core/design.md) §5 |
| **hw_lock** | Core's single mutex serializing all DUT probe/serial access across `/flash`, `/reset`, `/serial-log`. Deliberately separate from the dev-bench serial link's own one-study-at-a-time lock — different physical connections. | [embarch-core/design.md](embarch-core/design.md) §3 decision 4 |
| **Study** | A scripted sequence of BLE stimulus/interaction steps plus measurement/validation, run against a DUT through dev-bench — the unit of work `POST /study` accepts. | [embarch-study-designer/design.md](embarch-study-designer/design.md) §1, §4.1 |
| **Step** | One action within a `Study` (`BleAdvertise`/`BleConnect`/`DataExchange`), plus its own timeout and optional power-sample window. | [embarch-study-designer/design.md](embarch-study-designer/design.md) §4.2 |
| **dev-bench** | `embarch-dev-bench`, the physical rig playing the DUT's BLE counterpart and sampling power during a `Study` — Zephyr-based C firmware, cross-vendor by design. | [embarch-dev-bench/design.md](embarch-dev-bench/design.md) §1 |
| **topology class** | `local` / `wsl-host` / `remote` — the three ways `embarch-api` and `embarch-core` can be arranged relative to each other, auto-detected by `embarch-umbrella`/`embarch-api`'s shared candidate-race logic. Only the class is ever persisted, never a resolved address. | [embarch-umbrella/design.md](embarch-umbrella/design.md) §3 decision 6, §4 |
| **suite** | The whole `embarch-*` set of sub-projects together — Core, API, dev-bench, study-designer, umbrella, promptu, atlas — as opposed to any one of them. | [embarch.md](embarch.md) §1 |

## Changelog

- 2026-08-15 — Initial version, closing item 22 of that day's design-improvement review.
