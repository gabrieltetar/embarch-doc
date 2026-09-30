# Proposal: bootloading a DUT over MCUboot serial recovery

**Status:** proposal, 2026-09-30.

**Today a DUT gets new firmware one way: a debug probe, through Core's `POST /flash`. This adds a second: build, then hand the signed image to the DUT's own bootloader over its USB CDC ACM port.** Spans four repos — a new one, `embarch-smp`, plus `embarch-topology`, `embarch-core` and `embarch-api` — which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3).

**Deliberately narrow for the first cut: one bootloader (MCUboot), one mode (serial recovery), one transport (USB CDC ACM).** The first DUT it serves has the MCUboot flash layout in its devicetree but no MCUboot yet, so **everything here is validated by unit tests and a simulated bootloader until that firmware exists**; hardware validation is a later step, not a precondition for landing.

## What was decided, and why

- **MCUboot serial recovery, not an application-side SMP server.** The bootloader itself speaks SMP (Simple Management Protocol, the mcumgr wire protocol) and writes the image straight into the primary slot. It works when the application is broken, which is the case a bench most needs covered. The cost: an upload overwrites the running application, so a bad image leaves the DUT sitting in its bootloader — **recoverable by the next bootload, not a brick**, and the pre-upload header check below exists to make it rare.
- **A Rust port of smpclient, in a new repo `embarch-smp`.** [smpclient](https://github.com/intercreate/smpclient) and the [smp](https://github.com/JPHutchins/smp) protocol package it builds on are both Apache-2.0, so a port carries a `NOTICE` and per-file attribution and is otherwise unencumbered. Porting beats writing from the spec because smpclient is already exercised against real MCUboot builds, including its own reference firmware for exactly this case (MCUboot serial recovery over CDC ACM). Rejected: shelling out to `smpmgr` the way Core shells out to `nrfutil` — lighter (a day, not three), but it adds a Python-or-portable-exe dependency on the Core machine and puts a second process on a serial port, which the next point rules out.
- **`embarch-smp` never opens a port.** It speaks SMP over any `Read + Write` it is handed. `embarch-topology`'s `hardware` feature stays the only code in the suite that opens a serial port ([embarch.md](embarch.md) §4; `embarch-topology` decision 8). Same split as the Python original, where `smp` is I/O-free and smpclient owns the transports.
- **The port is found by enrolled USB identity, never by COM name.** On Windows a CDC ACM device's COM number follows its USB identity, and a bootloader that enumerates under its own PID gets a different COM number from the application it replaced. So the DUT's enrollment row declares the identities, same posture as dev-bench's `link_port_serial`/`link_port_interface` (`embarch-topology` decision 20).
- **Getting into the bootloader is an engineer-declared shell command, never a guess.** The first DUT will most likely reboot into serial recovery on a command typed at its application shell, which lives on the same CDC ACM port. What that command is, and whether the DUT has one, is DUT behaviour, so it is declared in project config — the suite's never-infer-DUT-semantics rule ([embarch.md](embarch.md) §5). **A DUT already sitting in its bootloader needs no command at all**, and that is checked first.
- **Separate tools, not a `method` on `flash`.** `bootload` and `build_and_bootload` sit beside `flash` and `build_and_flash`. They share no parameters that mean the same thing — no probe, no chip, no format, no base address — and a mode flag that makes half of `flash`'s parameters meaningless is two tools sharing a name.

## The flow

1. **API** resolves the project and target, builds if asked, and finds the signed image. Default artifact `zephyr.signed.bin`, found the same way `zephyr.<format>` is today but **sysbuild-aware** (`build/<app>/zephyr/…`, [embarch-zephyr.md](embarch-zephyr.md) §4). It uploads the image to Core as multipart, as `flash` does across a topology boundary (`embarch-core` decisions 10, 18).
2. **Core checks the image before touching the device.** It must parse as an MCUboot image — header magic, header and image sizes consistent with the file, a TLV area present. An unsigned `zephyr.bin` is refused here with a message naming the likely fix, rather than accepted by the bootloader, written over the application, and rejected at boot.
3. **Core takes `hw_lock`** and refuses if an active study's direct-route tap is reading either declared port. Those taps take no lock today (`study.rs`), and Windows lets one process open a COM port, so without this check the upload fails with an opaque open error mid-study.
4. **Into the bootloader.** If the bootloader identity is already enumerated, skip ahead. Otherwise open the application port, write the declared command and line ending, close it, and **wait for the bootloader identity to enumerate**. Timeout: a declared default, measured on real hardware before it is trusted.
5. **Upload.** Open the bootloader port (asserting DTR, which a Zephyr CDC ACM may need before it transmits), stream the image in chunks sized to the declared buffer — serial recovery cannot advertise one, and follow the bootloader's returned offset rather than a local counter.
6. **Reset** over SMP, then wait for the application identity to re-enumerate.

The result names what happened, not just whether: bytes written, duration, whether the command was needed (`entered_via`: `already-in-bootloader` or `shell-command`), and **whether the application came back**. That last one is reported, not asserted: an image the bootloader accepted and the application then failed to start is a real outcome and must not read as a transport error.

## What each repo carries

**`embarch-smp`**: built — [its spec](embarch-smp/spec.md). It sends byte-identical requests to smpclient on every recorded upload, and ships the simulated bootloader Core's tests will drive.

**`embarch-topology`**: built — `hardware::bootload`, decision 36. Declaring a pair one port could match both of is refused, which closes this proposal's first open question.

**`embarch-core`**: `POST /bootload` (multipart: the image, the optional entry command and line ending, the image index, the declared buffer size), the flow above under `hw_lock`, the image-header check, and the study-tap refusal. A new route means a new `AUTH_CASES` row and a contract-version bump the API checks (`embarch-api` decision 17). About a day.

**`embarch-api`**: `bootload` and `build_and_bootload` as MCP tools and CLI subcommands, one table row each in `interfaces/tools.md`; project config gains a `bootload` table (`entry_command`, `entry_line_ending`, `artifact`, and `buffer_size` — the DUT's `CONFIG_BOOT_SERIAL_MAX_RECEIVE_SIZE`, which serial recovery cannot report and which cuts a 200 KB upload from 1,423 requests to 207, `embarch-smp` decision 7), and signed-image resolution. About half a day. **A UI button is deliberately later**, once the flow has run on hardware.

## Open

- **Whether `bootload` should verify the image afterwards.** Serial recovery's image-state read is itself a Kconfig option, so it cannot be assumed present. First cut: application re-enumeration is the success signal, and a hash check is added only where the bootloader answers one.
- **Timeouts** (bootloader enumeration, per-chunk response, application return) are placeholders until measured on the first DUT.

## Order of work

1. `embarch-core`: `POST /bootload`.
2. `embarch-api`: the two tools and the config.
3. Later, and not blocking 1–2: hardware validation on the first DUT once it has MCUboot, then the UI button.

Each accepted piece moves into its sub-project's own docs and is **deleted from this file, not restated** ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3).
