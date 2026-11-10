# embarch-core decisions: Chip mapping and attach

**Status:** active, 2026-11-09. Split out of [probes.md](probes.md) the same day, when that file passed its reserve line ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §3); the entries below moved verbatim.

How a Zephyr SoC name becomes a probe-rs target, and the guards in front of every attach: the guarded attach (80) and the requested-chip gate (89). Board identity and probe selection: [probes.md](probes.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Chip mapping

### 8, 34 — The SoC→chip table lives here, compiled in, plus `chip-list` as its human fallback
`embarch-api` is about to call `/flash` anyway, so resolving here costs nothing extra and keeps one copy in the one process that links probe-rs and can therefore validate a mapping against the real target database rather than trusting a hardcoded string. Matched case-insensitively and **exactly**: a plausible-but-wrong fuzzy match would silently pick the wrong physical target. A test checks every entry against the real registry, so drift fails a test run rather than a live call. `chip-list [filter]` exposes that same in-process database, because finding a probe-rs target name for an unmapped SoC otherwise meant `cargo install probe-rs-tools` — a toolchain install in the middle of a download-a-binary onboarding. *Not a UI dropdown instead*: that needs an endpoint too, so it is strictly more work and can be layered on this.

**The table is a source `const`, and that is the whole configuration story** (amended 2026-09-05). Until then this entry grounded `chip-list` in *configuring an override*, and pointed at a per-project `embarch-api` field to put the answer in. That field — [`embarch-api`](../../embarch-api/decisions.md) decision 13's `soc_chip_overrides` — was **retired unbuilt on 2026-09-05**, and a config still declaring it now fails at load. So the remedy `chip-list` feeds is unchanged in substance and different in destination: run it, then add the SoC/target pair to `SOC_TO_CHIP` in `chip_resolve.rs`, rebuild and redeploy. `chip-list` itself is untouched — it produces exactly the string the new remedy asks for.

***Rejected: give the table a config path here instead***, so an unmapped SoC needs no rebuild. It is the same escape hatch `embarch-api` 13 just retired, moved one repo over, and it re-opens the hole that retirement closed: a config-supplied mapping consulted before the table would bypass the registry validation this entry's first paragraph exists for. 13's tombstone already names **a Core the operator cannot rebuild** as the condition that reverses it — this suite rebuilds and redeploys Core routinely, so the rebuild requirement is a recorded choice, not a gap. Reverse *that* first, and the hatch belongs in Core's own machine-scoped config and still registry-validated. What this amendment fixes is only the text: `chip-list --help` and two `chip_resolve.rs` comments had gone on naming a field that no longer exists, sending an operator to write a key that stops `embarch-api` starting.

**A key may be a SoC *series*, and then the row is lossy — say which axis it loses** (amended 2026-09-09, first ST entry). Zephyr names a G0 board's SoC `stm32g0b1xx`, where the trailing `xx` stands for both the package letter and the flash-size letter, so one key faces sixteen probe-rs variants. `stm32g0b1xx → STM32G0B1VE` was chosen by dumping `Target::memory_map` for three of them rather than by reading part numbers: **VE and RE are byte-identical** (dual-bank 2×256 KiB, 144 KiB SRAM) and CB is not (single 128 KiB bank). So the package letter is pinout, which probe-rs does not model, and the **flash-size letter is the axis a series key actually loses** — the row is correct for every `stm32g0b1x`**E** board and would over-declare flash on a `B`/`C` one. When a second board makes that difference real, the key stops being expressible as one row and the table needs a `(soc, flash_size)` key; until then the mapping stands with the measurement recorded beside it in `chip_resolve.rs`.

---

### 80 — Every probe-rs attach goes through topology's guarded attach

`flash` and `reset` attached with `probe.attach(chip, …)` directly, so on an ARMv6 STM32 they ran probe-rs's sequence that read-modify-writes the target's RCC and DBGMCU while the core runs — garbage on a G0 sleeping without a DMA clock ([`embarch-topology`](../../embarch-topology/decisions.md) decision 39). Both now call `embarch_topology::hardware::attach::attach`, the same guarded attach validate and enroll use, so Core has one way to attach and it never writes a running target's clock enables.

---

### 89 — A requested chip that differs from the enrolled one is refused before any attach

`flash`, `reset`, `live::run`'s memory read and `read_dhcsr` call `embarch_topology::hardware::validate_serial_for_chip(serial, chip)` ([`embarch-topology`](../../embarch-topology/decisions.md) decision 44) instead of `validate_serial`; the result was never used, so nothing else changed. A probe moved to a board of another family used to read as a failed FICR/identity read on the old chip's target description (an STM32G0B1VE flash through a J-Link still enrolled on an nRF54L15 board, 2026-09-30). Now topology raises `RequestedChipMismatch` before the probe is opened. `describe_topology_error` (flash, reset, mem-read) renders it as **`409` with topology's own `chip-mismatch: ...` text**, and the dev-bench handshake's `describe_gate_error` as the same text; it is neither `not_attached` nor `mismatch` and writes no alert. Case and whitespace are ignored; an empty chip on either side passes.

**Assumed, not measured:** a project's `chip` and an enrolled `chip` spell the same, because enroll stores the chip the caller passed and later calls pass the project's. No normalisation lives in Core; a project spelling `nRF54L15` against an enrolled `nrf54l15_cpuapp` would be refused, and the refusal text names both. **Tested without a store:** topology's enrollment path is the fixed `/var/lib/embarch`, so the test builds an `EnrolledBoard`, runs `check_requested_chip` and the Core mapping; the attach-ordering half is topology's own tested guarantee.

