# embarch-dev-bench decisions: The Core link

**Status:** active, 2026-09-02.

The serial hop to Core: what carries it, how it is detected and flashed, what the handshake says, and the two ceilings that had to be found on hardware.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 6, 7 — A plain UART over the board's on-board VCOM, and log output as a framed message
Originally specified as USB CDC ACM; revised once research found **the nRF54L15 SoC has no USB device peripheral at all** — the DK's USB connector belongs entirely to its on-board SEGGER debug chip, which already bridges one of the SoC's real UARTs to a virtual COM port. Firmware-side this is a completely ordinary Zephyr UART with no SEGGER-specific code and no USB stack anywhere. Everything Core-facing is unchanged; only the physical mechanism moved.

**A second interface for dev-bench's own log output was rejected in favour of framing it.** Sharing one byte stream between free-text log lines and COBS frames would corrupt the protocol — COBS frames are self-delimiting, plain text is not, so a receiver parsing for boundaries chokes on stray bytes. So a log line is just another properly-framed message. *(For its first three weeks this was implemented with the logging subsystem switched off, which read as though it had **chosen** to have no logging. It had not: what it forbids is unframed text on the wire, and a backend that emits framed lines satisfies it exactly — see [logging.md](logging.md).)*

### 12 — Detection matches the debug chip's own vendor ID, not a custom VID/PID
A custom VID/PID was originally locked in so Core could identify the bench among other serial devices — but that descriptor would have to be advertised by dev-bench's own USB stack, which decision 6 established does not exist. The port Core sees is enumerated by the on-board debug chip. **Entirely a Core-side change, no firmware-side VID/PID logic at all**; the matching rules live there.

### 13 — Core *can* flash dev-bench firmware, reversing a separation-of-concerns rule
Originally: flashing the bench is a direct `west flash`, outside Core, because "Core's probe access is scoped to the DUT — it has no business flashing the bench testing that DUT." A deliberate choice, not a technical limit, made before dev-bench had a board whose flashing mechanism Core could share. It stopped holding the moment the ESP32-C5 arrived, whose on-chip debug interface probe-rs already speaks natively — with **zero USB forwarding**, since Core runs natively on Windows and that connector was never a WSL2 device to forward.

**What this does not do:** migrate the nRF54L15DK off `west flash`. That board's SoC has been in Core's chip table since decision 12, but flashing it *through* Core was never attempted, so the original default stays the practical answer there.

### 18, 25 — `HelloAck` carries a firmware-identity string, and a doctor check consumes it
`schema_version`/`compatible` tell Core whether the wire shape matches, not which build is running — a real gap when something misbehaves and the question is "did this bench even get reflashed". A single free-form string is the simplest shape that answers it; whatever the build embeds is build-tooling's concern, not fixed at the wire-type level, and the append-only discipline leaves room for a structured field later.

Nothing consumed it until a `doctor` check compared it against the repo's own `git describe`. **A real, previously-undetected build bug surfaced doing that:** the CMake `git describe` runs at *configure* time, and CMake only reconfigures when one of its own tracked dependencies changes — not "the commit checked out right now". An incremental build after a plain commit was silently re-linking with the previous configure's stale version baked in — **exactly the false negative the check exists to catch, self-inflicted by the build system.** Fixed by adding the resolved `.git/HEAD`, its ref, and `.git/index` as configure dependencies. A plain `--dirty` edit with nothing committed is still uncatchable by any dependency list.

*Separately:* running that check against a WSL2 checkout over a `\\wsl.localhost` UNC path reports `-dirty` always, because Windows git cannot read this repo's workspace symlinks over that path, so every file under one looks modified. Not a bug in the check — the configured path should be native to whichever machine runs it.

### 19 — The bench verifies `steps_crc` itself before running any step
Restating, not reopening, the upstream decision that specifies this at this hop. The FFI function already exists and already returns exactly the "did decode succeed / does the CRC match" answer, so this calls it rather than reimplementing CRC verification.

### 30 — The inbound path is interrupt-driven, closing a silent 128-byte ceiling
The dispatch loop read the link UART itself, polling and sleeping 1 ms whenever the FIFO happened to be empty. At 1 Mbaud one millisecond is ~100 bytes of arrivals against a 128-byte hardware FIFO — so **any inbound frame larger than the FIFO lost whatever landed while the reader was asleep.** Decode then failed on the truncated result and the loop simply continued, which is the worst possible presentation: Core saw no reply of any kind and reported a step timeout, indistinguishable from a dead link or a wedged board.

**Why it went unnoticed:** every study ever authored fit in the FIFO. The first stimulate-and-capture study is 132 payload bytes — the first one large enough to cross the line, which is why that whole feature had never once worked on hardware despite every unit test passing. The boundary was then confirmed directly rather than inferred, by sweeping a single step's payload length: ~128 bytes completed, ~134 timed out, repeatably. After the fix, ~450-byte frames complete.

An ISR now drains the FIFO into a ring buffer sized to **scheduling latency, not a whole frame**. Overruns are counted and reported as a log line rather than dropped silently — the entire point is that a lost inbound byte must never again look like a dead link. A poll-mode fallback stays behind an `#ifdef` for a platform with no interrupt-driven UART; it carries the original ceiling and is not what hardware uses.

**A test-methodology change this forced.** Every `StudyStart` test round-tripped through this file's own encoder, so a decoder bug the encoder mirrored exactly would pass all of them while failing against Core. The suite now also decodes **the real bytes Core puts on the wire**, COBS-framed by an independent encoder written in the test itself.

### 35 — One step decoded at a time from the retained span, and the local step cap goes away
Decision 21 solved a real stack problem with a static `StudyStart` holding a fixed step array, then shrank that array from the crate's 64 to a local **16** to keep it affordable. Both were reasonable, and together they cost ~9.2 KB of permanently-resident RAM sized for a worst-case step that almost no step is — and introduced a divergence nobody had written down: **the host accepts a 20-step study and the wire silently refuses it.** Found by reading a header, not by a test.

The decoder now keeps the raw bytes it already received and decodes step N into a **single** struct at dispatch time. RAM drops to roughly one frame plus one step, the ceiling disappears, and the crate's constant goes back to being the one authority. **`steps_crc` is still verified before step 0 runs** — the span walker this needs already existed, built for `streams_crc`, and walking a span to dispatch from it is the same motion as walking one to digest it.

*Declined: streaming steps from Core one at a time* — the smallest possible RAM, and the repo owner's own first instinct. It loses two things deliberately bought: `steps_crc` could no longer be checked before execution begins, becoming a running digest verified at the end, which **inverts the guarantee the seal exists for**; and a serial round-trip would land between every step, folding link latency into exactly the timing `delay_before_ms` was added to make authorable. Recorded rather than discarded — if a study ever gets long enough that even the raw frame is a problem, this is the next move, and the trigger is that specific.

### 36 — The bench reports its own chip ID in `HelloAck`, through Zephyr's `hwinfo`
Since the port migration the runtime link is a *physically separate USB device* from the JTAG connection, so Core could confirm "the enrolled probe is attached" and "some bench answered on the link" without either implying the other. This is the one thing the bench can say about itself that ties them together.

**`hwinfo_get_device_id()` rather than a raw register read, and that was the repo owner's call.** Reading the eFuse registers directly would produce a string byte-identical to what the JTAG side reads, needing no host-side relation at all — but it hardcodes an ESP32-specific register address into firmware meant to move back to a Nordic board, which it since has. `hwinfo` is the portable call, and the cost lands where it can be paid: the topology crate declares the relation between the two encodings once, per chip. On this part it turned out **derivable rather than guessed**, since Zephyr's own driver reads those same two registers and reorders their bytes.

A build without the driver reports an **empty string** rather than a substitute, because a plausible-looking invented ID would defeat the whole check. Core is where "no ID" acquires meaning, and it passes rather than refuses.
