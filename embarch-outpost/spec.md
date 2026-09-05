# embarch-outpost: spec

**Status:** active, 2026-09-02.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Wire: [interfaces/wire.md](interfaces/wire.md). Integration: [interfaces/integration.md](interfaces/integration.md).

**Working end to end on real hardware since 2026-08-27, at record layout 3:** a study captures a real nRF54L15's thread, ISR and marker timeline and the UI renders it named and timed.

## 1. What it is

**The first EmbArch component that ships inside the thing under test.** Every other sub-project observes a DUT from outside. The outpost is a small Zephyr module an engineer compiles into their *own* DUT firmware for debug builds, emitting a running account of what the MCU is doing — which thread ran, in what order, when it was in interrupt context, and whatever application spans the engineer marked — out a dedicated TX-only UART, recorded and rendered host-side.

**The question it answers is the one no external instrument here can:** *the study passed, but what was the CPU doing while it did?*

**Not a violation of the no-inference rule**, which forbids any component presenting an inference about what a specific piece of hardware or firmware does as established fact. The engineer compiles the outpost in, chooses what to mark, and ships a build-time manifest declaring what every ID means. **Nothing here reads a DUT's source and guesses.**

**v1 scope, explicitly bounded:**

- **TX-only.** The DUT talks; nothing talks back. No host commands, no runtime enable, no acknowledgement of any kind. The frame type is the field a later command channel is added to, rather than a reshape.
- **Study-scoped, rendered post-hoc.** No always-on mode and **no live feed** — settled against this work's own opening framing, which asked for realtime.
- **Zephyr only.** No vendor-neutral porting layer is being designed up front.
- **No power, no GPIO, no stimulus.** The outpost observes its own MCU. It does not sample, drive, or measure anything else.

**It is not** a production feature, a logging library (a DUT console is a legitimate *second* signal under the same routing model, not this one), or a replacement for a debugger or an ETM probe. It is deliberately the wire-thin version: one UART pin, no probe bandwidth, no vendor tool.

## 2. Architecture

```
   DUT firmware (engineer's own repo, debug build)
   ┌──────────────────────────────────────────────────┐
   │  Zephyr kernel  sys_trace_* hooks ──┐            │  CONFIG_TRACING_USER;
   │  application    OUTPOST_EVT(...) ───┤            │  the outpost implements
   │                                     ▼            │  the hooks
   │                 lock-free record ring            │  emit = write one slot,
   │                                     ▼            │  read the cycle counter,
   │            drain thread → COBS frames → uart_tx()│  return. No locks.
   └───────────────────────┬──────────────────────────┘
                           │ outpost UART, TX only
              route=direct │ route=via-dev-bench (no hardware yet)
                           ▼
                      embarch-core
        opens the tap for the study, writes the raw stream verbatim,
        stamps every frame's arrival, decodes both against the
        build-time manifest
                           ▼
                      embarch-ui — timeline, post-hoc
```

Three properties carry the design:

1. **The route is a bench fact, not a study fact.** A study names the *signal*; topology resolves which carrier currently delivers it, so the same saved study runs unchanged before and after pass-through hardware exists.
2. **Nothing between the DUT and Core interprets a byte.** Core decodes, against a manifest the DUT's own build produced. Whichever carrier is in use moves bytes and stamps nothing but arrival.
3. **Both clocks are on the wire and neither substitutes for the other.** The DUT's cycle count **measures** — a span's duration is the difference between its ends. The host's receipt time **places** — it is the same wall clock every other stream in the study carries, so laying a trace beside a power capture is an alignment rather than a guess.

## 3. Invariants

- **The emit path takes no lock and reads no locked clock.** It writes one ring slot and returns. A trace whose cost is a latency floor on unrelated interrupts distorts exactly the thing it measures.
- **No strings on the wire, ever**, except two in the header frame once a second. IDs are resolved through the manifest.
- **Overflow drops, counts, and says so** — never blocks, never overwrites. The host renders a gap **as a gap** rather than drawing a continuous, plausible, wrong picture across it.
- **A mismatched manifest refuses to render the names**, keeping the capture — a manifest from another build would silently relabel every marker, readable and entirely wrong.
- **A join that cannot be verified stamps nothing.** A trace shifted by three frames is readable, wrong, and indistinguishable from a correct one.
- **Nothing interpolates, on any clock.** Even spacing inside a frame would look better and be fabricated.
- **Every board-specific fact is declared in the DUT's own repo, never here** — which UART, which pins, what baud, how big the ring is. Why the module may not hold an opinion about any of them: [decisions/module.md](decisions/module.md) decision 1.
- **What the firmware chose is on the wire, not inferred from what is missing.** Which hook families are compiled in, and whether the outpost excluded itself, are header flags — because **an absence of records is indistinguishable from an idle subject.**

## 4. The instrument's measured cost

All on a quiet `dut_dev@7` nRF54L15 at 460800 baud, and the numbers are why several decisions read the way they do.

| | Value |
|---|---|
| record on the wire | **9.92 bytes** [measured 2026-08-27] |
| resolution, DUT clock | **1 µs** — 0 of 4955 spans below it |
| resolution, host clock | 4.0 ms — 4286 of 4955 spans below it |
| the outpost's own CPU share | **1.6%** on the DUT clock (66.3 ms over 778 drain runs, 85 µs each) |
| the same, misread on the host clock | **78.1%** — the drain thread switches in on one frame and out on the next, so it is charged the whole frame interval, 46× over |
| burst loss under a real study load | **19.7% across 3 gaps** while the link averaged 36% busy |

**Average capacity was never the constraint.** The ring is the burst knob, the fill wait is the latency knob, and the record's size is the throughput knob — and only the third is still unturned ([open.md](open.md)).

Every Kconfig symbol, its default, and the measurement that set it — the ring's, the fill wait's and self-exclusion's included: [interfaces/integration.md](interfaces/integration.md).

## 5. Host-side outputs

Three files under the study's `streams/`:

- **`<tap>.bin`** — the raw framed stream, verbatim, **written before any decoding and always**, even when the build ID does not match, so a mismatch is recoverable rather than a lost run.
- **`<tap>.arrival.csv`** — `frame_index, rx_utc_ms, frame_bytes`, one row per frame, written incrementally. Unrotated on purpose, and `frame_bytes` is what lets the post-hoc join be **verified** rather than assumed.
- **`<tap>.trace.csv`** — decoded records, one per row: `frame_index, frame_seq, rx_utc_ms, cycles, us, kind, a, b, name`. **Written even when no manifest applies** (empty `name`) and **even when no arrival stamps apply** (empty `rx_utc_ms`).

Consecutive rows repeating one `rx_utc_ms` is normal, not a defect: it is a *frame's* stamp. Both `frame_index` and `frame_seq` appear because they answer different questions — the index is this capture's own monotonic ordinal and is what an arrival stamp is keyed by; the seq is the firmware's own wrapping byte.

`streams/index.json` carries **three independent booleans** for the three ways a trace can be incomplete: `named`, `timed`, and `self_excluded` — the last being the only one the *firmware* decides.
