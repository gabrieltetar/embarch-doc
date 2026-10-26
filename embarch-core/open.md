# embarch-core: open questions

**Status:** active, 2026-09-02.

What is unresolved and what would close it. Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Never exercised

- **`POST /bootload` has never met a real bootloader.** The flow is tested end to end against `embarch_smp::sim` with a simulated re-enumeration; the first DUT has MCUboot's partitions and no MCUboot yet. Its timeouts are placeholders until timed there, and whether the uploaded image should be verified afterwards stays open: serial recovery's image-state read is a Kconfig option, so re-enumeration of the application is the success signal until a bootloader answers a hash (decision 77).
- **The signal-tap path has never run against real hardware.** Unit-tested on Linux and native Windows; no real port has been resolved or read — this bench has no USB-UART bridge. `validate_signal` has no caller by design: resolving a route at use *is* the validation.
- **Decision 35's gate has never met ESP32-C5 silicon.** The Nordic arm is live and answers `match`; the Espressif relation is verified only by construction against the checked-out HAL headers and by unit test, that board being unplugged.
- **The Windows registry write for an *explicit* `EMBARCH_TOKEN` has never executed on real hardware.** A real install/start is verified with no explicit token; only an explicit one reaches that path, and the common case — auto-generated — never does.

- **Decision 89's requested-chip refusal has never met a moved probe.** Host-tested on the mapping only (the enrollment store is the fixed `/var/lib/embarch`, so no test enrolls). To verify: enrol a J-Link on one board, flash a project of another chip family through it, expect `409 chip-mismatch` and no attach. Also unmeasured: that a project's `chip` and an enrolled `chip` spell the same.

- **Background capture (decision 92) has never met a port.** Tested against scripted ports only. Open on the bench: a capture on one console while exchanges run on the other and a flash and reset of either board; an exchange on the captured signal; a boot log across a UART-bridge reset; a CDC ACM re-enumeration reopening with a gap marker.

- **The bench lease (decision 93) has never met an installed Core or a second real client.** Host-tested through the router only; the two-client check and the native Windows build are the owner's.

## Unverified diagnoses

- **Whether probe-rs writes killed the nRF54L15 is evidence, not proof** (decision 36). One erase-and-program over J-Link recovered a board unresponsive across a whole session, but the counterfactual is not established: a full erase-and-reprogram may have cleared something else.

## Designed, not built

- **`core.toml`** (decision 11), narrowed to `bind`/`port`.
- **A `{code, message, cause}` JSON error body** — deferred with a trigger, not pending: the `code` enum is a wire contract three consumers branch on, so it is cross-repo work, not Core's alone. Cost and trigger: decision 12.
- **A subject discriminator on `Alert`**, so a signal mismatch would reach `/alerts` (decision 30). Not-needed-*yet*, with a named trigger: nothing can raise one until a direct route is physically possible.
- **An HTTP surface, SSE stream, or `embarch-api` tool for `dev-bench.log`** (decision 37). Nothing has asked; this suite's posture is not to build machinery first.
- **A byte count alongside `GET /serial-log`'s `truncated: bool`** — rejected, not deferred (decision 58). Trigger: a caller that must act differently on 1 byte lost versus 900 KB.

- **A bench study's signal tap is still a second port owner beside a capture** (a host study's taps are captures, decision 98). A capture refuses a tap's port; a study started on a captured signal is refused only by the OS.

## Structural limits

- **Espressif-family dev-bench port selection has no current story.** Decision
  23's four removed env overrides had no stated replacement: `link_port_interface`
  answers an ambiguous-VCOM board, and the ESP32-C5-WROOM-1 DK is **[assumed]**,
  unmeasured, to enumerate as a single USB-Serial/JTAG interface with no VCOM to
  name — `tasks/core/028` cites `dev-bench/005`, which declined to assert it.
  Confirming the enumeration needs the board; the missing replacement knob
  outlives that confirmation.
- **A separate-machine deployment has no artifact transfer.** Multipart (decision 10) closed the WSL2 case; a LAN Pi remains reachable by design, unusable for flashing.
- **macOS is reasoned-only.** The elevation paths are written, unexercised; nothing here has run on a Mac.

## Moved elsewhere, not resolved

- **Discarding a signal port's buffered input on open is not sufficient; the defence is now `embarch-ui`'s** (decision 30). A capture began with **18 stale records** seconds off — those bytes sit inside the USB-UART bridge, past an OS-level purge. Fix built as `embarch-ui` decision 19; unresolved is that it has never met the real prefix ([embarch-ui/open.md](../embarch-ui/open.md)).
