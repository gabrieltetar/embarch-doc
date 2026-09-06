# embarch-outpost: wire format

**Status:** active, 2026-09-02.

**Record layout 3.** Why it is this shape: [../decisions/layout.md](../decisions/layout.md). Current truth: [../spec.md](../spec.md).

`src/outpost_priv.h` is the specification, with **three implementations that must agree**: the firmware encoder, the shared crate's decoder (which Core and the UI both read a trace through), and the manifest generator's own view.

## Record

What the emit path writes into one ring slot:

```
{ cycles: u32,   // the DUT's own counter, read lock-free in the hook
  kind:   u8,    // 0 ThreadSwitchIn   1 ThreadSwitchOut  2 IsrEnter
                 // 3 IsrExit          4 Idle             5 ThreadCreate
                 // 6 ThreadName       7 Marker           8 Gap
                 // 9 GpioDispatch    10 GpioCallbackDone
  a:      u32,   // kind-dependent: thread pointer, vector number,
                 //   marker ID, dropped count, GPIO port device,
                 //   callback handler
  b:      u32 }  // kind-dependent: marker arg, the gap's cycle span,
                 //   a callback's pin mask; 0 where unused
```

**Kinds are append-only, and appending one does not bump the layout version.** The record shape is fixed precisely so a host can skip a kind it does not know — an unknown kind is a row rendered as `unknown_N`, never a decode failure. What tells a host whether a family is present at all is the header's `flags`, not the version byte; bumping for an appended kind would refuse every manifest built before it for no decoding benefit.

postcard-encoded, so each `u32` is a varint. A ring slot is **20 bytes**, and `CONFIG_EMBARCH_OUTPOST_RING_BYTES` is divided by exactly that — a `BUILD_ASSERT` pins the equality, because when it did not, **every ring had quietly been 1.25× its configured size** and the unit test asserting the product passed the whole time, since it measured the product through the same constant.

**Layouts 1 and 2 are not decoded by anything, deliberately.** A layout-2 decoder pointed at a layout-1 stream would read each timestamp's first byte as a *kind* and produce plausible, wrong rows for the whole capture. The version byte in the header is what makes that a refusal instead.

**The version is 3, although the wire is byte-for-byte what 1 was.** A version byte exists so a host can say "I decode up to N"; a number reused after a different, mutually-unreadable wire has already worn a higher one **cannot say that** — two incompatible streams would both announce `1`, separable only by which build produced them, which is the one thing the byte is there to settle.

### The two GPIO kinds each carry a trap

**`GpioCallbackDone` (10) is an *exit* marker — read the name literally.** Zephyr places the hook **after** `cb->handler()` returns, not before it. A handler's span therefore runs from the record *before* it — the dispatch, or the previous handler's completion — to this one. **A host that reads it as an entry marker attributes every handler's time to the wrong handler, and the trace stays entirely readable while it does.** `a` is the handler's function pointer and `b` is that callback's registered pin mask, at full width. On Thumb a function pointer carries bit 0 set while the manifest keys its symbol addresses with that bit masked off, so a decoder must mask before looking a handler up or every one renders unnamed.

**`GpioDispatch` (9) — one port has begun walking its callback list, from that port's own interrupt.** `a` is the port's `struct device *`. **`b` is `0` and is deliberately *not* the pin mask:** Zephyr's hook declares its mask parameter `gpio_pin_t`, a `uint8_t`, while `gpio_fire_callbacks()` passes it a 32-bit `gpio_port_pins_t`, so every pin above 7 is already gone before this module is reached, and emitting what survives would put a plausible wrong mask on the wire. Which pins a dispatch covered is recovered instead from the `pin_mask` on the `GpioCallbackDone` records that follow it.

## Frame

```
frame := COBS(body || crc32_ieee(body) as 4 bytes LE) || 0x00
body  := frame_type: u8, seq: u8, payload
```

**`frame_type` 0x01 — Records.** The payload is a varint count then that many records. Batches are capped at **127** so the count stays one byte. **A gap record, when there is one, is always the first record of its frame** — emitted directly into the frame, never through the ring, since the ring being full is the reason it exists. That position is what bounds the losses in time.

**`frame_type` 0x02 — Header.** Emitted once at startup and thereafter every `CONFIG_EMBARCH_OUTPOST_HEADER_INTERVAL_MS`, so a host attaching mid-stream can decode. **At `0` it is emitted at startup and never again** — a legal build, not a fault. The payload, in order:

```
record_layout_version: u8
flags:                 u8
cycles_per_sec:        varint(u32)
outpost_version:       postcard string (varint len, then bytes)
build_id:              postcard string
```

**`cycles_per_sec` is read at runtime** — `sys_clock_hw_cycles_per_sec()`, never `CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC`, which legitimately defaults to `0` on targets whose timer reads its own frequency at runtime, so a build-time rate would be silently zero on exactly those. **A host that receives `0` anyway has no rate and must say so rather than guess one:** both decoders leave `us` empty there ([../spec.md](../spec.md) §5).

**Header frames share the records frames' `seq` counter and advance it**, so a host counting lost frames by a gap in `seq` counts both kinds together.

**The header is a frame type, not a record kind** — settled at implementation, because its fields do not fit the fixed record shape, and because making it its own type pays off for exactly the case it exists for: a host attaching mid-stream finds a header **at a COBS boundary** rather than having to parse into a batch to look for one.

**It carries a build ID and no manifest CRC.** The manifest is generated *from the linked image* — its thread and ISR tables are ELF reads — so no CRC of it exists at compile time for the firmware to carry ([../decisions/manifest.md](../decisions/manifest.md)). The two strings are the only strings on this wire, at most one header a second, and they are what make the manifest check possible at all: the rule that rejected CTF was about *per-record* cost, and this is not that.

**`flags` says which hook families the running firmware actually has compiled in**, one bit each, **so a host never infers that from the absence of records:** `BIT(0)` threads, `BIT(1)` ISRs, `BIT(2)` idle, `BIT(3)` markers, `BIT(4)` ISR identification, `BIT(5)` blocking overflow, `BIT(6)` GPIO callback dispatch, `BIT(7)` self-tracing. **`BIT(7)` is the one whose *clear* state is the interesting one** — clear means the trace deliberately describes neither the outpost's own drain thread nor its own UART's interrupt, so intervals no lane covers are expected rather than a defect ([../decisions/tracing.md](../decisions/tracing.md) decision 19).

**Framing is COBS**, byte-for-byte the same routine the Core⟷dev-bench link already uses, so Core sees one framing convention on both of its links. The CRC covers the body only, sealed before COBS.

**Reserved for a future RX direction:** nothing in v1 sends anything to the DUT, but `frame_type` is exactly the field a later command channel is added to.

## The host decoder's rules are tested, and one of the two tests always runs

`tests/decoder_unit.py` in the module repo is stdlib `unittest` over bytes it
synthesises itself, and it is the only check here with **no** external
requirement — no `west`, no `ZEPHYR_BASE`, no sibling repos, no fixtures.
`tests/run-all.sh` runs it **before** the west guard for exactly that reason:
the other three legs need a Zephyr toolchain and the cross-decoder leg needs two
sibling checkouts, so until it existed the reference decoder for a wire with
three implementations that must agree had **no test guaranteed to execute**.
That is `cross_decoder.py`'s own argument — a check nobody is forced to run is
not a check — applied to itself.

It pins the rules that already carry scar tissue in comments, because those are
the ones a rewrite silently undoes: COBS round-trip including the 0xFF run that
carries no implicit zero; a bad CRC costing exactly one frame **while still
consuming a `frame_index`**, since the receiver burned one stamping it; a
truncated batch counting `bad_body` and yielding nothing; an unknown kind
rendering as `unknown_N`; the wrap-vs-gap rule **in both directions**; and `us`
as three fixed decimals rather than a rounded float. Both directions of the wrap
rule matter and asserting one is worthless: the naive `cycles < last` passes a
test that only checks a real wrap, and a decoder that never unwraps at all
passes one that only checks the gap case.

**What it deliberately does not do is round-trip through the decoder's own
inverse.** Its COBS encoder and varint writer are written out separately, on the
same reasoning `tests/unit`'s literal-byte assertions use: a format with three
implementations is not served by a test that agrees with itself.

## Two independent decoders agree, and it is a test rather than a note

Under layout 1 this was checked by hand once — byte-identical in every column of 848 rows bar how many decimals each printed for `us` — and then **went un-rerun across a rework that rewrote both decoders**, which is precisely when it was worth having. It compares decoder against decoder, which is the check actually available: the firmware encoder is the third implementation and is the one both decoders are fed *from*. It reads committed fixtures rather than a fresh capture, because a fresh run carries a different build ID on every dirty tree.
