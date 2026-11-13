# embarch-core open: never exercised

**Status:** active, 2026-09-02.

Paths and decisions that have only met unit tests, a simulator or a scratch build, and what closes each. Current truth: [../spec.md](../spec.md). The rest, and the decision 108 deploy: [../open.md](../open.md).

- **`POST /bootload` has never met a real bootloader.** Tested against `embarch_smp::sim` only; the first DUT has MCUboot's partitions and no MCUboot yet. Timeouts are placeholders until timed there; whether to verify the uploaded image stays open, since serial recovery's image-state read is a Kconfig option (decision 77).
- **The signal-tap path has never run against real hardware.** Unit-tested only; this bench has no USB-UART bridge. `validate_signal` has no caller by design.
- **Decision 35's gate has never met ESP32-C5 silicon.** The Nordic arm is live; the Espressif relation is verified by construction and unit test only.
- **Decision 106's in-place install has never run on Windows.** Host-tested on the pure parts only; the registry writes and `sc failure` do not build on Linux. Owner-run: reinstall the live service with `EMBARCH_SIGNAL_BAUD` set, expect it kept; `sc qfailure` shows five restarts; `install --bind` over a registered service rewrites it. An explicit `EMBARCH_TOKEN` has also never reached the registry write.

- **Decision 89's requested-chip refusal has never met a moved probe.** Host-tested on the mapping only (the enrollment store is the fixed `/var/lib/embarch`, so no test enrolls). To verify: enrol a J-Link on one board, flash a project of another chip family through it, expect `409 chip-mismatch` and no attach. Also unmeasured: that a project's `chip` and an enrolled `chip` spell the same.

- **Background capture (decision 92) has never met a port.** Scripted ports only. Open: a capture while exchanges, flashes and resets run on either board; a boot log across a bridge reset; a CDC ACM re-enumeration reopening with a gap marker.

- **The bench lease (decision 93) has never met an installed Core or a second client.** Router-tested only; the two-client check and native Windows build are the owner's.
