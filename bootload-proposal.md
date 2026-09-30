# Proposal: bootloading a DUT over MCUboot serial recovery

**Status:** proposal, 2026-09-30.

**Today a DUT gets new firmware one way: a debug probe, through Core's `POST /flash`. This adds a second: build, then hand the signed image to the DUT's own bootloader over its USB CDC ACM port.** Spans four repos — a new one, `embarch-smp`, plus `embarch-topology`, `embarch-core` and `embarch-api` — which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3).

**Deliberately narrow for the first cut: one bootloader (MCUboot), one mode (serial recovery), one transport (USB CDC ACM).** The first DUT it serves has the MCUboot flash layout in its devicetree but no MCUboot yet, so **everything here is validated by unit tests and a simulated bootloader until that firmware exists**; hardware validation is a later step, not a precondition for landing.

## What was decided, and why

The rest moved to `embarch-smp` decisions 1–2, `embarch-topology` decision 36 and `embarch-core` decision 77.

- **Separate tools, not a `method` on `flash`.** `bootload` and `build_and_bootload` sit beside `flash` and `build_and_flash`. They share no parameters that mean the same thing — no probe, no chip, no format, no base address — and a mode flag that makes half of `flash`'s parameters meaningless is two tools sharing a name.

## The flow

**API** resolves the project and target, builds if asked, and finds the signed image. Default artifact `zephyr.signed.bin`, found the same way `zephyr.<format>` is today but **sysbuild-aware** (`build/<app>/zephyr/…`, [embarch-zephyr.md](embarch-zephyr.md) §4). It uploads the image to Core as multipart, as `flash` does across a topology boundary (`embarch-core` decisions 10, 18). Everything after that is Core's: [`embarch-core` decision 77](embarch-core/decisions/bootload.md).

## What each repo carries

**`embarch-smp`**: built — [its spec](embarch-smp/spec.md). It sends byte-identical requests to smpclient on every recorded upload, and ships the simulated bootloader Core's tests will drive.

**`embarch-topology`**: built — `hardware::bootload`, decision 36. Declaring a pair one port could match both of is refused, which closes this proposal's first open question.

**`embarch-core`**: built — `POST /bootload` and `/bootload/ports`, decisions 77 and 78.

**`embarch-api`**: `bootload` and `build_and_bootload` as MCP tools and CLI subcommands, one table row each in `interfaces/tools.md`; project config gains a `bootload` table (`entry_command`, `entry_line_ending`, `artifact`, and `buffer_size` — the DUT's `CONFIG_BOOT_SERIAL_MAX_RECEIVE_SIZE`, which serial recovery cannot report and which cuts a 200 KB upload from 1,423 requests to 207, `embarch-smp` decision 7), and signed-image resolution. About half a day. **A UI button is deliberately later**, once the flow has run on hardware.

## Order of work

1. `embarch-api`: the two tools and the config.
2. Later, and not blocking 1: hardware validation on the first DUT once it has MCUboot, then the UI button.

Each accepted piece moves into its sub-project's own docs and is **deleted from this file, not restated** ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3).
