# embarch-smp: spec

**Status:** planned, 2026-09-30.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). The cross-repo design it serves: [bootload-proposal.md](../bootload-proposal.md).

**Repo created, no code yet.** Everything below the first section is the committed scope, not shipped behaviour.

## 1. What it is

**A Rust client for SMP — the Simple Management Protocol mcumgr and MCUboot speak — ported from [smpclient](https://github.com/intercreate/smpclient) and the [smp](https://github.com/JPHutchins/smp) package beneath it.** It exists so Core can hand a signed image to a DUT's MCUboot serial-recovery bootloader over USB CDC ACM, the second way to put firmware on a DUT after a debug probe.

**It never opens a port.** Every call takes a `Read + Write` the caller already opened; in the suite that caller is `embarch-topology`'s `hardware` feature, which stays the only code that opens a serial port ([decision 2](decisions.md)).

## 2. Scope of the first cut

| Layer | What | Ported from |
|---|---|---|
| Serial framing | Line-oriented packets: a start (`06 09`) or continuation (`04 14`) delimiter, base64 body, `\n`. The decoded frame is a big-endian `u16` length, the SMP message, and a CRC16/XMODEM over the message alone; the length counts the CRC. Fragmented to a caller-chosen line length (default 127) | `smp.packet` |
| Header | The 8-byte SMP header: op and version packed in one byte, flags, `u16` length, `u16` group, sequence, command | `smp.header` |
| Commands | OS group: echo, reset. Image group: state read, upload. CBOR bodies | `smp.os_management`, `smp.image_management` |
| Client | A blocking request/response loop over `Read + Write`, sequence-number matching, and an upload that follows the server's returned offset | `smpclient` |
| Image check | Parse an MCUboot image header and TLV area, so a caller can refuse an unsigned image before it touches a device | `smpclient.mcuboot` |
| Test double | An in-process simulated serial-recovery bootloader, driven over a pipe, behind a feature flag so Core's tests can use it too | new |

**Out of scope:** BLE and UDP transports, every other management group, async.

## 3. Testing

Unit tests over committed fixtures, generated once from the Python `smp` package by a script kept in the repo (`tools/`). **Python is a fixture generator, never a build or runtime dependency** ([decision 5](decisions.md)). Integration tests run the client against the simulator. **No hardware validation yet**: the first DUT has no MCUboot, so a real-bootloader run is a later step ([bootload-proposal.md](../bootload-proposal.md), "Order of work").
