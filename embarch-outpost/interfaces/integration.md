# embarch-outpost: integrating it into a DUT firmware project

**Status:** active, 2026-09-02.

The path from "this repo exists" to "I am reading a trace." **Nothing here is exotic — it is Zephyr's ordinary module mechanism, which is the point.** Why: [../decisions/module.md](../decisions/module.md).

## Getting the module in

A Zephyr module: a `zephyr/module.yml` at the root pointing at its own `CMakeLists.txt` and `Kconfig`. A DUT repo consumes it as a **west-managed project** — added to its own `west.yml` with a pinned revision, exactly as dev-bench already consumes the shared study crate.

**The revision is pinned in the DUT's manifest, and that pin is part of the build ID** the header frame carries, so a trace names the module revision that produced it.

## Turning it on

Kconfig in the consuming project, plus **one devicetree `chosen` node** naming the UART the trace leaves by. That node is the whole of the board-specific surface: **the module ships mechanism and defaults; the DUT repo declares the facts.**

| Symbol | Default | Provenance | What it decides |
|---|---|---|---|
| `EMBARCH_OUTPOST` | `n` | n/a | Master switch |
| `..._BAUD` | `0` | n/a | `0` = use the chosen node's `current-speed`; non-zero reconfigures at init |
| `..._RING_BYTES` | `4096` | [measured 2026-08-27] **the burst knob.** 512 slots lost 6962 records across 48 gaps under a real study load; 2048 slots lost 8036 across 5 — the ring absorbed 43 of 48 overflow events. Divided by the 20-byte slot size |
| `..._BATCH_BYTES` | `256` | [assumed] Bytes the drain thread accumulates before a transmit. **Bigger is strictly better on this wire** since layout 3 — frame size no longer affects resolution at all |
| `..._FILL_WAIT_MS` | `10` | [measured 2026-08-27] **the latency knob.** Frames had settled at 3.3 records, making ~20% of the link framing overhead; after the wait, 20.2 records per frame and the duty cycle 94% → 37% |
| `..._THREAD_PRIORITY` / `..._THREAD_STACK_SIZE` / `..._THREAD_WAIT_MS` | `10` (low, numerically high) / `1024` / `100` | [assumed] | The drain thread |
| `..._TRACE_THREADS` / `..._TRACE_ISRS` / `..._TRACE_IDLE` / `..._TRACE_MARKERS` | `y` | [assumed] | Which hook families emit at all. Reported in the header `flags` |
| `..._TRACE_GPIO` | `y` | [assumed] | Record which GPIO callback handler ran inside a GPIOTE interrupt and when it returned — the ISR records name the vector, these name the handler. **`n` removes no call from the image**: `gpio_fire_callbacks()` makes them whenever `CONFIG_TRACING` is on and without this they land in Zephyr's empty `__weak` definitions. What `n` saves is the records, which is the part that costs wire. Reported in the header `flags` |
| `..._TRACE_SELF` | **`n`** | [measured 2026-08-27] **50.4% of the reference capture was the instrument describing its own transmission.** `y` is the honest-but-expensive setting, and exactly right when the thing being debugged *is* the outpost |
| `..._ISR_IDENTIFY` | `y` on Cortex-M | n/a (capability) | Read the active vector number in the hook. `depends on` the absence of a custom interrupt controller, so such a build degrades rather than reporting a plausible wrong number |
| `..._OVERFLOW_BLOCK` | `n` | n/a (policy) | Opt into blocking instead of dropping, for a deliberate high-fidelity run |
| `..._HEADER_INTERVAL_MS` | `1000` | [assumed] | How often the header repeats, so a host attaching late can still decode |
| `..._UART_ASYNC` | `y` where the driver supports it | n/a (capability) | `uart_tx()` versus a polling fallback. **The fallback exists so such a port still produces a stream, not because it is fine** |
| `..._TX_TIMEOUT_MS` | `1000` | [assumed] | `depends on ..._UART_ASYNC`. **A stuck-transport backstop, not a pacing knob:** it must comfortably exceed one framed batch's wire time, ~275 ms for the 256-byte default at 9600 and proportionally less above it. On expiry the transfer aborts, that frame is dropped, and the drain thread carries on — the alternative is an unbounded wait, which on a build with no console fails as a trace that silently stops |
| `..._MARKER_HEADER` | `""` | n/a (per-application) | The header declaring this application's marker list |
| `..._BUILD_ID_MAX` | `64` | [assumed] | Longest build-ID string the header carries |

**The one Kconfig failure mode that produces a working build and the wrong transport:** the async symbol here is a *module* symbol, while whether the **driver** offers the async API for the chosen instance is a separate, per-instance decision — and on nrfx the per-instance async option depends on the interrupt-driven one being *off*, which is itself `default y` whenever the global UART interrupt option is on. A build can therefore satisfy the module symbol and still fall back.

## Placing markers

`OUTPOST_EVT(ID, arg)`, with IDs declared in one place that is **simultaneously** what makes the call compile and what puts the name in the manifest. **An unregistered ID is a build error, not a mystery integer on the host.**

**`<embarch/outpost.h>` is includable in a build that does not have the module**, where `OUTPOST_EVT()` compiles to nothing — which matters because **a marker is worth most in a hot path compiled into both the tracing image and the shipping one**: a driver's drain loop, a queue's overflow branch, a library's error return. The no-op degrades in **three** tiers, the third dropping the name check, because with no registration header included there is no enumerator to check against and the check would fail every call site rather than catch anything.

## Reading the trace

Nothing to configure: declare the signal's route in topology, add a `StreamSource::Signal` tap named for it to a study, and the capture and rendering happen host-side. Outputs: § Host-side outputs, below.

## Host-side outputs

Three files under the study's `streams/` — moved here verbatim from `../spec.md`
§5, which now points at this section:

- **`<tap>.bin`** — the raw framed stream, verbatim, **written before any decoding and always**, even when the build ID does not match, so a mismatch is recoverable rather than a lost run.
- **`<tap>.arrival.csv`** — `frame_index, rx_utc_ms, frame_bytes`, one row per frame, written incrementally. Unrotated on purpose, and `frame_bytes` is what lets the post-hoc join be **verified** rather than assumed.
- **`<tap>.trace.csv`** — decoded records, one per row: `frame_index, frame_seq, rx_utc_ms, cycles, us, kind, a, b, name`. **Written even when no manifest applies** (empty `name`) and **even when no arrival stamps apply** (empty `rx_utc_ms`).

**`rx_utc_ms` here is Core's real epoch clock**, unlike the column of the same name in a *study's* CSV and transcript, which is dev-bench uptime ([decision 17](../decisions/clocks.md), [suite decision 3](../../suite/decisions.md)). Do not join the two on that column.

Consecutive rows repeating one `rx_utc_ms` is normal, not a defect: it is a *frame's* stamp. Both `frame_index` and `frame_seq` appear because they answer different questions — the index is this capture's own monotonic ordinal and is what an arrival stamp is keyed by; the seq is the firmware's own wrapping byte.

**`us` carries exactly three decimals whenever it carries a value at all** — `1234.500`, never `1234.5`, and the empty string when `cycles_per_sec` is 0, which both decoders agree on rather than guessing a rate. That is a contract between the decoders and not a rendering preference: rounding instead of formatting disagrees on every value whose fraction is shorter than three digits. **`cycles` is the DUT's counter unwrapped host-side, and a *small* backwards step is not a wrap** — a gap record is stamped when its losses started, so it legitimately goes backwards a little, and treating that as a wrap threw every later timestamp forward by 2**32. Both rules are pinned by a host test that needs no toolchain ([wire.md](wire.md)).

**The manifest travels with the flash that binds it** — an optional part on the same call that already carries the firmware artifact, so the manifest and the image it describes arrive in one operation and there is no interval in which Core holds one without the other.
