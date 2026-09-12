# embarch-outpost: spec

**Status:** active, 2026-09-02.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Wire: [interfaces/wire.md](interfaces/wire.md). Integration: [interfaces/integration.md](interfaces/integration.md).

**Working end to end on real hardware, at record layout 3:** a study captures a real nRF54L15's thread, ISR and marker timeline and the UI renders it named and timed.

## 1. What it is

**The first EmbArch component that ships inside the thing under test.** Every other sub-project observes a DUT from outside. The outpost is a small Zephyr module an engineer compiles into their *own* DUT firmware for debug builds, emitting a running account of what the MCU is doing — which thread ran, in what order, when it was in interrupt context, and whatever application spans the engineer marked — out a dedicated TX-only UART, recorded and rendered host-side.

**The question it answers is the one no external instrument here can:** *the study passed, but what was the CPU doing while it did?*

**Not a violation of the no-inference rule**, which forbids any component presenting an inference about what a specific piece of hardware or firmware does as established fact. The engineer compiles the outpost in, chooses what to mark, and ships a build-time manifest declaring what every ID means. **Nothing here reads a DUT's source and guesses.**

**v1 scope, explicitly bounded:**

- **TX-only.** The DUT talks; nothing talks back. No host commands, no runtime enable, no acknowledgement of any kind. The frame type is the field a later command channel is added to, rather than a reshape.
- **Study-scoped, rendered post-hoc.** No always-on mode and **no live feed** — settled against this work's own opening framing, which asked for realtime.
- **Zephyr only.** No vendor-neutral porting layer is being designed up front.
- **No power, no pin sampling, no stimulus.** The outpost observes its own MCU. A GPIO record names the *handler* that ran, never a pin's level.

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
- **A mismatched manifest refuses to render the names**, keeping the capture — a manifest from another build would silently relabel every marker, readable and entirely wrong. This holds over every row, including pre-header ones: the decoder reads the whole stream first, so an unnamed row still gets a correct `us` once any header is seen. `--allow-build-id-mismatch` renders anyway (decision 24).
- **A join that cannot be verified stamps nothing.** A trace shifted by three frames is readable, wrong, and indistinguishable from a correct one. `scripts/decode_outpost.py` checks this: each frame's actual delimiter-separated chunk length against the arrival CSV's `frame_bytes` for that index, refusing every `rx_utc_ms` stamp in the capture on the first disagreement and naming its index on stderr — `--allow-unverified-join` stamps anyway, mirroring `--allow-build-id-mismatch`'s posture toward decision 9 (decision 24 records both overrides). An arrival CSV whose `frame_bytes` column is missing or short (an older, two-column file) degrades to the unverified join rather than refusing to read the file.
- **Nothing interpolates, on any clock.** Even spacing inside a frame would look better and be fabricated.
- **Every board-specific fact is declared in the DUT's own repo, never here** — which UART, which pins, what baud, how big the ring is. Why the module may not hold an opinion about any of them: [decisions/module.md](decisions/module.md) decision 1.
- **What the firmware chose is on the wire, not inferred from what is missing.** Which hook families are compiled in, and whether the outpost excluded itself, are header flags — because **an absence of records is indistinguishable from an idle subject.**

## 4. The instrument's measured cost

All on a quiet `dut_dev@7` nRF54L15 at 460800 baud.

| | Value |
|---|---|
| record on the wire | **9.92 bytes** [measured 2026-08-27] |
| resolution, DUT clock | **1 µs** — 0 of 4955 spans below it |
| resolution, host clock | 4.0 ms — 4286 of 4955 spans below it |
| the outpost's own CPU share | **1.6%** on the DUT clock (66.3 ms over 778 drain runs, 85 µs each) |
| the same, misread on the host clock | **78.1%**, 46× over — a stale host reading frame arrival as the clock (decisions/layout.md, reversals row 86) |
| burst loss under a real study load | **19.7% across 3 gaps** while the link averaged 36% busy |

The ring is the burst knob, the fill wait is the latency knob, and the record's size is the throughput knob (decisions/transport.md decision 20) — only the third is still unturned ([open.md](open.md)).

Every Kconfig symbol, its default, and the measurement that set it — the ring's, the fill wait's and self-exclusion's included: [interfaces/integration.md](interfaces/integration.md).

## 5. Host-side outputs

Three files under the study's `streams/`, their exact columns and the
formatting/wrap rules that bind both decoders: [interfaces/integration.md](interfaces/integration.md)
§ Host-side outputs. In short: `<tap>.bin` (raw, verbatim, always written),
`<tap>.arrival.csv` (the join), `<tap>.trace.csv` (decoded records).

**A trace's `rx_utc_ms` is Core's real epoch clock. A *study's* column of the same name is not** — it is dev-bench uptime ([suite decision 3](../suite/decisions.md)).

`streams/index.json` carries **three independent booleans** for the three ways a trace can be incomplete: `named`, `timed`, and `self_excluded` — the last being the only one the *firmware* decides.
