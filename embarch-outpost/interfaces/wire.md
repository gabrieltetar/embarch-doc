# embarch-outpost: wire format

**Status:** active, 2026-09-02.

**Record layout 3.** Why it is this shape: [../decisions/layout.md](../decisions/layout.md). Current truth: [../spec.md](../spec.md).

`src/outpost_priv.h` is the specification, with **three implementations that must agree**: the firmware encoder, the shared crate's decoder (which Core and the UI both read a trace through), and the manifest generator's own view.

## Record

What the emit path writes into one ring slot:

```
{ cycles: u32,   // the DUT's own counter, read lock-free in the hook
  kind:   u8,    // ThreadSwitchIn | ThreadSwitchOut | IsrEnter | IsrExit
                 // | Idle | ThreadCreate | ThreadName | Marker | Gap
  a:      u32,   // kind-dependent: thread pointer, vector number,
                 //   marker ID, dropped count
  b:      u32 }  // kind-dependent: marker arg; 0 where unused
```

postcard-encoded, so each `u32` is a varint. A ring slot is **20 bytes**, and `CONFIG_EMBARCH_OUTPOST_RING_BYTES` is divided by exactly that — a `BUILD_ASSERT` pins the equality, because when it did not, **every ring had quietly been 1.25× its configured size** and the unit test asserting the product passed the whole time, since it measured the product through the same constant.

**Layouts 1 and 2 are not decoded by anything, deliberately.** A layout-2 decoder pointed at a layout-1 stream would read each timestamp's first byte as a *kind* and produce plausible, wrong rows for the whole capture. The version byte in the header is what makes that a refusal instead.

**The version is 3, although the wire is byte-for-byte what 1 was.** A version byte exists so a host can say "I decode up to N"; a number reused after a different, mutually-unreadable wire has already worn a higher one **cannot say that** — two incompatible streams would both announce `1`, separable only by which build produced them, which is the one thing the byte is there to settle.

## Frame

```
frame := COBS(body || crc32_ieee(body) as 4 bytes LE) || 0x00
body  := frame_type: u8, seq: u8, payload
```

**`frame_type` 0x01 — Records.** The payload is a varint count then that many records. Batches are capped at **127** so the count stays one byte. **A gap record, when there is one, is always the first record of its frame** — emitted directly into the frame, never through the ring, since the ring being full is the reason it exists. That position is what bounds the losses in time.

**`frame_type` 0x02 — Header.** Emitted at startup and every `HEADER_INTERVAL_MS`, so a host attaching mid-stream can decode: `record_layout_version: u8`, `flags: u8`, `outpost_version: string`, `build_id: string`.

**The header is a frame type, not a record kind** — settled at implementation, because its fields do not fit the fixed record shape, and because making it its own type pays off for exactly the case it exists for: a host attaching mid-stream finds a header **at a COBS boundary** rather than having to parse into a batch to look for one.

**It carries a build ID and no manifest CRC.** The manifest is generated *from the linked image* — its thread and ISR tables are ELF reads — so no CRC of it exists at compile time for the firmware to carry ([../decisions/manifest.md](../decisions/manifest.md)). The two strings are the only strings on this wire, at most one header a second, and they are what make the manifest check possible at all: the rule that rejected CTF was about *per-record* cost, and this is not that.

**`flags` says which hook families the running firmware actually has compiled in** — threads, ISRs, idle, markers, ISR identification, blocking overflow, self-tracing — **so a host never infers that from the absence of records.**

**Framing is COBS**, byte-for-byte the same routine the Core⟷dev-bench link already uses, so Core sees one framing convention on both of its links. The CRC covers the body only, sealed before COBS.

**Reserved for a future RX direction:** nothing in v1 sends anything to the DUT, but `frame_type` is exactly the field a later command channel is added to.

## Two independent decoders agree, and it is a test rather than a note

Under layout 1 this was checked by hand once — byte-identical in every column of 848 rows bar how many decimals each printed for `us` — and then **went un-rerun across a rework that rewrote both decoders**, which is precisely when it was worth having. It compares decoder against decoder, which is the check actually available: the firmware encoder is the third implementation and is the one both decoders are fed *from*. It reads committed fixtures rather than a fresh capture, because a fresh run carries a different build ID on every dirty tree.
