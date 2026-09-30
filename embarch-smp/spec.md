# embarch-smp: spec

**Status:** active, 2026-09-30.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). The cross-repo design it serves: [bootload-proposal.md](../bootload-proposal.md).

**Built and tested against the reference and a simulator; no real bootloader has answered it yet.** Nothing in the suite links it yet: Core's `POST /bootload` is the first consumer, and it is not built.

## 1. What it is

**A Rust client for SMP — the Simple Management Protocol mcumgr and MCUboot speak — ported from [smpclient](https://github.com/intercreate/smpclient) 7.3.0 and the [smp](https://github.com/JPHutchins/smp) 4.2.0 package beneath it.** It exists so Core can hand a signed image to a DUT's MCUboot serial-recovery bootloader over USB CDC ACM, the second way to put firmware on a DUT after a debug probe.

**It never opens a port.** Every call takes a `Read + Write` the caller already opened; in the suite that caller is `embarch-topology`'s `hardware` feature, which stays the only code that opens a serial port ([decision 2](decisions.md)). A caller sets a short read timeout on the port; the client treats `TimedOut` as "nothing yet" and keeps its own deadline.

## 2. What it does

| Module | What | Ported from |
|---|---|---|
| `packet` | Serial framing: a start (`06 09`) or continuation (`04 14`) delimiter, base64, `\n`. The decoded frame is a big-endian `u16` length, the message, and a CRC16/XMODEM over the message alone; the length counts the CRC. `LineSplitter` separates SMP packets from console bytes sharing the line | `smp.packet`, smpclient's serial buffer state machine |
| `header` | The 8-byte header: op and version in one byte, flags, `u16` length, `u16` group, sequence, command | `smp.header` |
| `message` | Echo, reset, image state read, image upload; canonical CBOR bodies ([decision 6](decisions.md)); error responses ([decision 8](decisions.md)) | `smp.os_management`, `smp.image_management`, `smp.error` |
| `fragmentation` | How large a message the server takes: `BufferSize` (a declared reassembly buffer) or `BufferParams` (an encoded line budget, the default) ([decision 7](decisions.md)) | `smpclient.transport.serial.encoded` |
| `client` | Blocking request/response with sequence matching; `upload` fills every chunk to the buffer and follows the server's returned offset | `smpclient.SMPClient` |
| `image` | MCUboot image header and both TLV areas, so a caller can refuse an unsigned image before an upload erases the running application | `smpclient.mcuboot` |
| `sim` (feature) | A simulated serial-recovery bootloader behind `Read + Write`, modelled on MCUboot's `boot_serial.c`, for tests here and in callers | new |

**Throughput is the buffer size.** A 200 KB image takes **1,423 requests at the default, 427 declaring a 512-byte buffer, 207 declaring 1,024** — MCUboot's Kconfig default for `CONFIG_BOOT_SERIAL_MAX_RECEIVE_SIZE`. Counted against the simulator; wall-clock time on a real CDC ACM link is unmeasured.

**Out of scope:** BLE and UDP transports, every other management group, the MCUmgr-parameters handshake, async.

## 3. Testing

`cargo test --all-features`: 30 tests.

- **Byte-for-byte against the reference.** `tests/fixtures/reference.json` holds what the pinned Python releases produce — CRCs, 32 framing cases, eight requests, eleven responses including MCUboot's own `rc` shapes, two synthetic images with and without protected TLVs, and **every request smpclient would send for 18 uploads** across three buffer strategies. The Rust client sends identical bytes for all 18. `tools/gen_fixtures.py` regenerates the file; **Python is never a build or runtime dependency** ([decision 5](decisions.md)).
- **Behaviour against the simulator** and against scripted servers: flash-aligned offsets, a lost reply, a buffer declared larger than the bootloader's, console text interleaved with replies, a late reply to an earlier request, an offset that never moves, one past the end, a SHA mismatch, and a server that asks for offset 0 again.
- **No hardware yet**: the first DUT has no MCUboot ([open.md](open.md)).
