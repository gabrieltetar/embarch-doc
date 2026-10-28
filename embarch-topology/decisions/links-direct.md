# embarch-topology decisions: What a direct signal may do

**Status:** active, 2026-10-06.

Split verbatim from [links.md](links.md), 2026-10-28, once that file sat in its reserve. Decisions 37 and 40: a direct signal toward the DUT is writable and declares its own line rate, and its missing port names the ports that are there. Decisions 18 and 46, the signal entity and the refusal of an ambiguous serial, stay in `links.md`.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 37 — A direct signal toward the DUT is writable, and a signal declares its own line rate

**Amends decision 18's scope** ("no logic … as a host-to-DUT stimulus line — none are real yet"), because one became real: an agent driving a DUT's Zephyr shell needs to write a line and read the reply, and the DUT's console is exactly a declared signal on a direct route (a USB CDC ACM port, or a UART on a USB bridge). `SignalLink::host_can_write` is true for a `host-to-dut` or `bidirectional` signal **on a direct route**; Core's `POST /signals/{name}/exchange` ([embarch-core](../../embarch-core/decisions.md) decision 79) refuses every other. **A via-dev-bench route stays read-only whatever its direction**: the relay passes bytes one way today, and its write action is dev-bench work that does not exist yet. The outpost stays `dut-to-host`, so nothing can ever write to it.

**`baud` is now part of the declared fact, optional.** A console at 115200 and the outpost at 1 Mbaud are two signals with two rates, and the single process-wide `EMBARCH_SIGNAL_BAUD` could only serve one. Absent means Core's default, so every row on disk loads unchanged and is written back without the key: no migration. A USB CDC ACM port ignores the rate, so declaring none there is correct.

**Rejected: a separate "console" entity.** A console is a signal that also accepts writes; a second table would split one wire's facts across two places, and a `Study` would still have to tap it by the same name.

### 40 — A direct signal's missing port says which ports are there, not dev-bench advice

`resolve_signal_port` used to pass `port::select`'s error through for a `Direct` route, and that error is written for dev-bench's link: its VID gate, the link VIDs it recognises, and `set-dev-bench-link --clear-serial` as the fix. A DUT's USB CDC ACM console that is gone for a second while the board resets got that whole paragraph. The reason now names the declared USB serial, the serial ports that are visible, and that a CDC ACM port is gone while its device resets and returns once it re-enumerates. The error is still a `SignalMismatch` with `declared_port_serial` set, which is what `embarch-core`'s exchange keys its port wait on (core decision 79, amended).
