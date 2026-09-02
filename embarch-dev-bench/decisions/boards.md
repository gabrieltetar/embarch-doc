# embarch-dev-bench decisions: Boards

**Status:** active, 2026-09-02.

Which physical board is the bench, why it changed twice, and what the power front end will be.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 4, 10 — First board nRF54L15DK; a second vendor family deliberately left unspecified
Chosen over the nRF54H20DK specifically to avoid that part's mandatory multi-core `sysbuild` build for a board whose job here — running the BLE host in both roles and bridging serial to Core — does not need multiple cores. *(The original "non-sysbuild build" phrasing was wrong: NCS 3.4 wraps every application in sysbuild regardless. It stays a single domain with one image and one flash step, so the substance holds.)*

No second vendor, board, or Zephyr flavor is committed to. The `workspaces/`-per-family convention is designed to obviously extend, and keeping it unbuilt keeps it honest — built to extend, not pre-built for a hypothetical.

### 26 — ESP32-C5-WROOM-1, an interim substitute that became the bench
The physical DK broke (SEGGER's own tooling failed to open its DLL talking to the board — a hardware fault, confirmed by ruling out every Windows-side driver cause first) and its RMA never arrived. Rather than block a milestone's hardware validation entirely, an on-hand ESP32-C5 stood in — built as a real durable workspace per decision 2's pattern rather than throwaway scaffolding, since that decision already anticipated exactly this. Zephyr has real mainline support including a genuine Zephyr BT host over Espressif's own controller blob, so `ble_bridge_real.c` needed **zero changes**.

**A caveat that mattered:** this board's Zephyr port carries `testing.ignore_tags: [bluetooth]`, so upstream CI never exercises BT here — "compiles and links cleanly" was not proof the radio works. It does; a real advertise self-test passed.

**Two things a blind copy of the Nordic board fragment would have got wrong.** The HCI driver Kconfig for Espressif's controller is *not* directly settable — it has no prompt, is selected automatically once BT is on, and setting it explicitly is a hard Kconfig error. And `CONFIG_BT_MAX_CONN=2` means something different here: Espressif's controller budgets central and peripheral independently, so it is plainly "one central plus one peripheral", not decision 15's central-role-starvation workaround.

**A real pre-existing CMake bug, not specific to this board:** the default crate-path resolution appended `../../embarch-study-designer` to `CMAKE_CURRENT_SOURCE_DIR` and resolved in one call. That directory is itself a symlink, and CMake collapses `..` components *textually* before resolving symlinks — so it landed on a nonexistent path inside `workspaces/`. `workspaces/nordic` happened not to hit it, which is exactly why a fourth workspace's symlink chain was what surfaced it.

**The devicetree gap, and the premise that was wrong.** A first live handshake timed out, diagnosed as "the console UART is wired to unconnected header pins", and the overlay repointed the console at the native USB-Serial peripheral. **Corrected: this board has two USB-C ports and `uart0` was never disconnected** — it ships a dedicated UART port with its own bridge chip, and `uart0`'s pinmux is exactly what that second port is wired to. "Unconnected" was true only in the narrow sense that nothing had been plugged into the second port. The overlay was rewritten to restore the board's own upstream default plus the link baud, and **both cables plugged in became the normal operating configuration**: JTAG flashing on the native port, the runtime link on the dedicated one.

*Rejected: [Boreas](https://github.com/intercreate/boreas)* (a Zephyr-style API shim over ESP-IDF, with no Bluetooth support) — going that route would mean writing BLE dispatch from scratch against ESP-IDF's native stack on top of first adding BLE primitives to Boreas, strictly more work than plain Zephyr where the bridge needed no changes. A real idea for its own sake, not for this task.

### 43 — The nRF54L15DK is the bench again, and the port cost one property and one wrong assumption
A replacement DK arrived. `workspaces/nordic` had been kept alive for exactly this, and the bet paid: **twelve days of app work later — the GATT transcript, the log backend, per-study verbosity, selective monitoring, the `.eap` interpreter, `close_all_taps` — it built first try with no source change at all.** One file added, one property: 1 Mbaud on `uart20`. Unlike the ESP32-C5, whose overlay had to move the console onto a second bridge chip entirely, this board's console *is already* `uart20`.

**The assumption that was wrong belonged to the host, not the firmware.** The DK's onboard J-Link exposes **two** VCOMs under one USB serial, and detection resolved the pair by silently taking the lowest interface index. `uart20`'s pins are wired to **VCOM1 — interface 2**. So the bench flashed, booted, ran, and answered nothing while port detection reported a confident result. The board-shaped fact a firmware engineer needs: **enrol this board with `link_port_interface = 2`.**

**Onboarded by re-running the last study, unchanged** — a 14-step BLE/PPG drain submitted verbatim from the saved-study library against the same DUT: 14/14 `Pass`. Against the ESP32-C5 baseline the captures match closely (`bds-data` 77,177 → 76,874 B; `gatt` 315 → 317 entries dropped, correctly unchanged since that is dev-bench's own transcript queue filling rather than a controller property). **The one real behavioural difference is gone rather than reduced:** Espressif's controller ran out of ACL buffers fifteen times in a run the SoftDevice Controller completes without a single complaint.

**The premise this retires lived in another repo:** `embarch-api` held this bench's board, chip, flash format and flash offset as *constants*, on the ground that there is exactly one dev-bench board the suite will ever know about. That premise has now been falsified twice by this same physical bench, and the two boards agree about none of the four — nor about the artifact path, since NCS defaults to sysbuild and the vanilla-Zephyr workspace does not.

### 24 — The power front end: a Nordic PPK2 as an external instrument, provisional
"Entirely unscoped" was the single largest blocker a design review identified, since `Sample`'s shape, the CSV columns and the achievable rate all wait on it. A PPK2 driven over USB from whatever machine runs Core, rather than an on-board shunt+ADC design: the fastest path to exercising the whole capture path without a board respin, and reversible, since nothing in the wire types assumes a `Sample`'s source. **Not ordered, not wired into any workspace** — a proposal to unblock the roadmap, as provisional as it says.
