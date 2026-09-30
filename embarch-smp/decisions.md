# embarch-smp: decisions

**Status:** active, 2026-09-30.

Why it is the way it is. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)).

## Shape

### 1 — A port of smpclient, not a fresh implementation and not a wrapper around smpmgr
smpclient and `smp` are already exercised against real MCUboot builds, including smpclient's own reference firmware for serial recovery over CDC ACM — the exact case this serves. Porting inherits that behaviour and a test suite to mirror; writing from the protocol description would rediscover the same edge cases on hardware. **Rejected: shelling out to `smpmgr`** the way Core shells out to `nrfutil` (`embarch-core` decision 36). It is about a day instead of three, but it adds a Python-or-portable-exe dependency on the Core machine and a second process on a serial port, which decision 2 rules out. Full comparison: [bootload-proposal.md](../bootload-proposal.md).

### 2 — It never opens a port; every call takes a `Read + Write`
`embarch-topology`'s `hardware` feature is the only code in the suite that opens a serial port (`embarch-topology` decision 8), and this crate does not become a second. The split mirrors the original: `smp` is I/O-free and smpclient owns the transports. Here the transport is whatever stream the caller hands in, so a pipe in a test and a COM port in Core are the same code path.

### 3 — Apache-2.0, not the suite's MIT
The rest of the suite is MIT. This crate is a derivative of two Apache-2.0 works, so it stays Apache-2.0, with a `NOTICE` naming both and a header on every ported file pointing at its original. MIT-licensed crates depend on it without conflict.

### 4 — Serial transport and four commands only, blocking
The first consumer is MCUboot serial recovery, which answers echo, reset, image state and image upload — echo and image state only when built with them. Anything more is surface with no caller. **Blocking, not async**: Core runs every hardware operation inside `spawn_blocking` already, and the Python original's asyncio exists for BLE, which is out of scope.

### 5 — Python generates fixtures; it is never a dependency
Byte-exact agreement with the reference is checked against fixtures the Python `smp` package produced, committed next to the script that produced them. Regenerating is a deliberate act with a diff to review, and `cargo test` needs no Python on the machine.

## Behaviour

### 6 — CBOR through `ciborium`'s `Value`, keys in canonical order
The reference encodes with `cbor2.dumps(..., canonical=True)`: map keys shortest first, then bytewise. Sorting keys the same way before encoding is what lets the fixtures be compared byte for byte rather than decoded and compared as maps. A dynamic `Value` is used over typed derives because replies vary by server: MCUboot sends `rc` alone, `rc` beside `off`, or an `images` array, and the simulator and the scripted test servers build arbitrary maps. **Rejected: `minicbor`** — no dynamic value type, so each of those shapes would need its own decoder.

### 7 — No `Auto` fragmentation: a conservative default, and a buffer size the engineer declares
smpclient's default, `Auto`, asks the server for its buffer size with the MCUmgr-parameters command. **MCUboot serial recovery does not implement it**: `boot_serial.c` answers echo, echo control and reset in the OS group and `ENOTSUP` to anything else. So `Auto` is not ported, and its fallback before the server answers — two 128-byte lines, a 169-byte message — is the default. It is safe for any serial-recovery build and slow: a 200 KB image is 1,423 requests. **`BufferSize` with `CONFIG_BOOT_SERIAL_MAX_RECEIVE_SIZE` is the fast path** (207 requests at its Kconfig default of 1,024), and it is a DUT fact, so a caller declares it rather than guesses. Declaring it too large is loud rather than silent: MCUboot drops a frame larger than its buffer without replying, and the client times out on the first chunk, before anything is written.

### 8 — A non-zero `rc` is an error in any response; `rc: 0` is success
MCUboot serial recovery answers every failure as `{"rc": N}`, **whatever version the request header carried**, and echoes the request's version back; its dispatch reads only the op bits, so v1 and v2 requests both work, and v2 stays the default as in the reference. A Zephyr SMP server speaking v2 answers with an `err` map instead, and both are read. The reference tries each command's success shape first, so an upload reply of `{"rc": 3}` parses as a success with no offset and fails one step later with a less useful message. Here the error is named where it arrives.

### 9 — Four places it deliberately differs from the reference
Each is a gap the reference leaves, not a disagreement with it: **a reply whose sequence number answers an earlier, timed-out request is skipped and counted**, not raised; **an upload whose offset does not move for five replies is abandoned**, where the reference loops forever; **a frame longer than its declared length is named as such**, where the reference reads a CRC off its end; **a TLV type is read as the `u16` MCUboot defines**, where the reference reads a byte and skips one — identical below `0x100`. Everything else is a port, and the fixtures hold it to that.
