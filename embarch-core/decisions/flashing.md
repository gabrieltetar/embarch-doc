# embarch-core decisions: Flashing

**Status:** active, 2026-09-02.

How bytes reach a board: artifact transfer, image formats, and attach and reset strategy. Backend selection and vendor-tool discovery split out to [flash-backend.md](flash-backend.md) 2026-09-12 along the file's own churn seam (`tasks/core/035`).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Flashing

### 10, 18 — Multipart upload, and `Format::Bin` at the merge address
`firmware_path` only works when caller and Core share a filesystem. Multipart is needed not just for a remote Core but for WSL2→Windows: the installed service runs as `LocalSystem` in Session 0 and **cannot reach `\\wsl.localhost` at all**, which is why the earlier UNC mechanism is retired — its "confirmed working" claim held only for a foreground Core. Separately, **`Format::Idf` does not work for a Zephyr image**, confirmed by inspection before attempting a flash: its loader requires an ESP-IDF app-descriptor section Zephyr does not emit, while Zephyr's runner merges bootloader+partition-table+app at build time and writes one `.bin` at a fixed offset. Hence `base_address`, meaningful only for `bin` and silently ignored otherwise so a caller passing it unconditionally need not special-case.

### 21 — Plain `attach`, not `attach_under_reset`; a best-effort reset pulse instead
A real hardware scare traced to two documented quirks rather than corruption: a target in low-power sleep can stop answering a plain SWD attach, and the ESP32-C5's USB-Serial/JTAG peripheral resets only the *core* without re-sampling boot-strap pins, so it can stay latched in ROM download mode — which also explains the earlier handshake decode failures, since a chip in its bootloader was never running the protocol.

**`attach_under_reset` made it worse and was reverted**: it needs the reset pin wired to the debug connector, which this board does not do. `reset` calls `target_reset()` first instead — a silent no-op on this probe, whose driver hardcodes `Err(NotImplemented)` regardless of wiring while its lower-level assert/deassert genuinely drive the line, so the fallback pulses manually. **The real pulse then reproduced the original symptom deterministically**, wedging the same device's CDC interface while JTAG stayed enumerated. **Resolved by moving the link to the board's second, dedicated UART port** rather than replicating the vendor's own watchdog-register hack.

### 32 — `erase` must not be EmbArch's own guess: it bricked a real board
The first implementation set probe-rs's `do_chip_erase`. [Measured] two runs each way, same artifact and probe: without `erase` the DUT comes up and advertises, with it the board goes silent. A plain non-erase flash does *not* recover it; the vendor's own runner with `--erase`, on the same image, does. **The mechanism is not established and this decision does not invent one** — probe-rs models the part as one flat NVM region with a sequence implementing only `debug_device_unlock`. Four-for-four correlation and a known recovery path; the causal story stays a guess.

*Rejected, and it was the option already written and compiling:* sector-erasing the declared NVM regions — **another EmbArch-authored guess about what a Nordic part needs erased, the same class of guess that produced the brick.** *Not adopted: a post-flash liveness check.* Recorded because the cost was paid in full: a whole session went into BLE scan diagnostics to explain a DUT that Core's own flash had bricked, and nothing ever verified a board was running after a flash. Core reports what the flasher reports; liveness is a study's job.

---
