# embarch-core: open questions

**Status:** active, 2026-09-02.

What is unresolved and what would close it. Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Never exercised

- **`POST /bootload` has never met a real bootloader.** Tested against `embarch_smp::sim` only; the first DUT has MCUboot's partitions and no MCUboot yet. Timeouts are placeholders until timed there; whether to verify the uploaded image stays open, since serial recovery's image-state read is a Kconfig option (decision 77).
- **The signal-tap path has never run against real hardware.** Unit-tested only; this bench has no USB-UART bridge. `validate_signal` has no caller by design.
- **Decision 35's gate has never met ESP32-C5 silicon.** The Nordic arm is live; the Espressif relation is verified by construction and unit test only.
- **Decision 106's in-place install has never run on Windows.** Host-tested on the pure parts only; the registry writes and `sc failure` do not build on Linux. Owner-run: reinstall the live service with `EMBARCH_SIGNAL_BAUD` set, expect it kept; `sc qfailure` shows five restarts; `install --bind` over a registered service rewrites it. An explicit `EMBARCH_TOKEN` has also never reached the registry write.

- **Decision 89's requested-chip refusal has never met a moved probe.** Host-tested on the mapping only (the enrollment store is the fixed `/var/lib/embarch`, so no test enrolls). To verify: enrol a J-Link on one board, flash a project of another chip family through it, expect `409 chip-mismatch` and no attach. Also unmeasured: that a project's `chip` and an enrolled `chip` spell the same.

- **Background capture (decision 92) has never met a port.** Scripted ports only. Open: a capture while exchanges, flashes and resets run on either board; a boot log across a bridge reset; a CDC ACM re-enumeration reopening with a gap marker.

- **The bench lease (decision 93) has never met an installed Core or a second client.** Router-tested only; the two-client check and native Windows build are the owner's.
## Unverified diagnoses

- **Whether probe-rs writes killed the nRF54L15 is evidence, not proof** (decision 36): a J-Link erase-and-program recovered the board, but a full reprogram may have cleared something else.

## Designed, not built

- **`core.toml`** (decision 11), narrowed to `bind`/`port`.
- **A `{code, message, cause}` JSON error body** — deferred, cross-repo: the `code` enum is a wire contract three consumers branch on (decision 12).
- **A subject discriminator on `Alert`** so a signal mismatch reaches `/alerts` (decision 30); not needed until a direct route is physically possible.
- **An HTTP surface, SSE stream, or `embarch-api` tool for `dev-bench.log`** (decision 37); nothing has asked.
- **A byte count alongside `GET /serial-log`'s `truncated: bool`** — rejected (decision 58) until a caller must tell 1 byte lost from 900 KB.


## Structural limits

- **Espressif-family dev-bench port selection has no current story.** Decision 23's removed env overrides had no replacement: `link_port_interface` answers an ambiguous-VCOM board, and the ESP32-C5-WROOM-1 DK is **[assumed]** to enumerate as one USB-Serial/JTAG interface with no VCOM to name (`tasks/core/028`). Confirming needs the board; the missing knob outlives it.
- **A separate-machine deployment has no artifact transfer.** Multipart (decision 10) closed WSL2; a LAN Pi cannot flash.
- **macOS is reasoned-only.** Nothing here has run on a Mac.

## Moved elsewhere, not resolved

- **Discarding a signal port's buffered input on open is not sufficient; the defence is now `embarch-ui`'s** (decision 30). A capture began with **18 stale records** seconds off — those bytes sit inside the USB-UART bridge, past an OS-level purge. Fix built as `embarch-ui` decision 19; unresolved is that it has never met the real prefix ([embarch-ui/open.md](../embarch-ui/open.md)).
