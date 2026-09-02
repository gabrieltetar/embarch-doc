# embarch-outpost decisions: The bench

**Status:** active, 2026-09-02.

The first consumer, and the wire that turned out not to exist.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 15 — First consumer: `reference-dut-fw`. The nRF54L15 already enrolled as `dut`, already flashed through Core, already the target of every milestone here. Cortex-M33, so the concrete numbers this design defers get measured on a board that is already on the bench rather than estimated. The list shrank on 2026-08-26: cycle rate and wrap period stopped being questions when decision 4 took every timestamp off the wire. What is left is the sustainable record rate at a given baud, the drop rate that follows from it — and the one number that is now the instrument's headline spec: **how many milliseconds a frame actually takes to arrive**, which is the resolution of everything the trace says.

### 16 — The outpost's UART reaches the Core machine over the DUT board's own USB — there is no separate bridge, and none gets bought, 2026-08-25. §7 carried this as an open hardware pick, and it was the wrong question. On the board actually being used, the DUT's UART is wired to the USB connector already plugged into the PC. That arrangement *is* `Route::Direct` ([embarch-topology/design.md](../../embarch-topology/design.md) §3 decision 18) in the most literal form: the signal leaves the DUT and goes straight to the Core machine, around the bench, exactly as the route was drawn.

    This dissolves the hazard §7 was most worried about. The concern was a *third* USB-serial device joining dev-bench's CP2102N and the DUT's SEGGER J-Link, distinguishable only by a serial-number string a human has to get right — the same shape as the stale-`EMBARCH_DEV_BENCH_SERIAL` incident that created `embarch-topology`. There is no third device: the DUT board is one the bench already has and already identifies. The `SignalLink` still declares a `port_serial`; it just names a port that already exists.

    ~~**One fact is genuinely not known and is deliberately not inferred here**: whether that USB exposes a second serial interface the dedicated `chosen { embarch,outpost-uart }` node can have to itself, or whether it contends with the DUT's console. That is a bench observation, and the honest answer is that nobody has looked. It does not change the route — a contended interface is still `Route::Direct` — but it decides whether Phase E starts with a wiring task or a console-multiplexing problem.~~

    **Amended 2026-08-26, and the bench observation overturned the decision rather than the open fact inside it** ([embarch-decision-reversals.md](../../embarch-decision-reversals.md) row 49). Somebody finally looked, and **the DUT's trace UART reaches the host over nothing at all.** The answer to "does it contend with the console" is yes — `uart20` *is* the console on `dut_dev` rev 6/7, and the `outpost` snippet takes the console off it — but that is the small half. The large half is that this decision's own premise is false: the DUT's UART is **not** wired to a USB connector plugged into the PC.

    Established by construction, not by absence of output. A build with `CONFIG_SHELL=y`/`CONFIG_UART_CONSOLE=y` was flashed and **proved to be running** — dev-bench connected to it over BLE and read back its real GATT table — and then every COM port on the machine was watched across a hardware reset. `COM5` is the *same* J-Link attached to this DUT (its VCOM reports probe serial `000852006107`), so the debug connector does carry a virtual COM port — and it returned **zero bytes**, meaning that VCOM is not wired to `uart20`. `COM4` is a genuine Microchip MCP2200 USB-UART bridge and returned only `0x00` at 9600/115200/230400/1M, which is a line held low rather than a baud mismatch. The chip transmits; nothing listens.

    So `Route::Direct` remains the right *model* and has still never existed physically. What Phase E starts with is exactly the wiring task this bullet hoped to rule out: a bridge's RX on **P1.05** — not P1.04, whose `DBG_TX` schematic label is on a net physically crossed on both rev 6 and rev 7 — and a ground. milestone 1 §5 had predicted this outright ("needs hardware that does not exist yet: a USB-UART bridge … and a wire"), and this decision is what talked the plan out of believing it.

