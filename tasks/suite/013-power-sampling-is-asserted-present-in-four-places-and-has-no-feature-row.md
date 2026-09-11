# 013 — Power sampling is asserted present in four places on the newcomer's path, has no hardware, and has no row in the doc that exists to say how far things are verified

**State:** open — **announced and parked**, leg 083, `ts` **`1789117538.021209`** (posted
2026-09-11 03:05 MDT; the 30-minute window closes **03:35:38 MDT**). Per `ops.md` §4 this runs as a
leg's last unit if no objection arrives; if leg 083 ends first, the next leg **completes** this
window from that `ts` rather than restarting the clock.
**Source:** suite review pass 2026-09-06, dimension 7 (the newcomer). Code-confirmed.
**Scope:** suite
**Hardware:** none. Doc tense corrections plus a features row plus, optionally, refusing a tap that cannot produce anything.
**Owner:** no

## What

Four present-tense assertions on the path a newcomer actually reads:

- `embarch-glossary.md:13` — dev-bench is *"the physical rig playing the DUT's BLE counterpart
  **and sampling power during a study**"*. Definitional.
- `embarch.md:46` — the architecture sketch, first thing read:
  `embarch-dev-bench firmware (BLE central/peripheral + power sampling)`.
- `suite/studies-guide.md:11` — *"an ordered list of steps, each a BLE action **or a
  power-sampling window**"* — four lines after the same file's own warning box says the hardware is
  missing.
- `suite/studies-guide.md:17` — **the first worked command in the studies guide** is
  `embarch-api study-stream-data <study_id> --name power --out power.csv`.

Plus `study_power_data` is a live MCP tool in every agent's list
(`embarch-api/src/tools.rs:1117`).

The firmware says otherwise: `embarch-dev-bench/app/src/main.c:685` —
`no power/waveform capture yet (decision 21's scope)`. `app/src/serial_protocol.c:166` accepts a
`PowerFrontEnd` tap declaration and does nothing with it, so the tap is authorable, crosses the
wire, is parsed, and yields an empty capture whose only signal is `bytes_written: 0` — which
`list_study_streams`' own description defines as *"a tap that was declared and produced nothing"*,
i.e. as a study-authoring outcome rather than as a missing subsystem.

And `grep -in power suite/features.md` returns **one row, unrelated** ("Early powered-target
check"). The doc whose entire stated job is *"every feature and **how far it is actually
verified**"* — which `embarch.md` §6 and `user-guide.md` §11 both send the newcomer to before
relying on anything — **has no row for power sampling at all.**

The deferral is real and recorded (`embarch-study-designer/open.md`, *"Deferred with power
profiling, at the repo owner's call"*; `suite/roadmap.md:33`), and I am not contesting it. It is
recorded in two docs nobody reads on hour one, while the four places that *are* on the path all
read as live. `embarch-dev-bench/spec.md:9` gets the tense right — *"will sample power"*.

Candidate direction: give power sampling its own `features.d/` row with an honest
`Status`/`Verified`; put the glossary and `embarch.md` §4's sketch into the tense the dev-bench
spec already uses; and make a declared `PowerFrontEnd` tap say what it is — refused at submit, or
named in `study_power_data`'s description — rather than producing an empty capture.

## Why now

The engineer writing their first study follows the guide's first worked command and gets a 0-byte
CSV indistinguishable from a study-authoring mistake. No other check can see this: all four
assertions are *consistent with each other*, so there is no A-versus-B difference to report — the
only inconsistency is against hardware that does not exist.

## Done when

- [ ] No doc on the newcomer's path states power sampling in the present tense while it is
      unbuilt.
- [ ] `suite/features.md` carries a power-sampling row with an honest `Status` and `Verified`.
- [ ] A study declaring a `PowerFrontEnd` tap either produces a capture or says why it cannot,
      distinguishably from a tap that produced nothing.
- [ ] Gate green.

**Constraint the worker must know:** `suite/features.md` is assembled from `features.d/` and has
**14 bytes of headroom** per `tasks/suite/004`, so a new row lands on that wall. The fragment is
`features.d/<scope>-*` (worker-writable); the size gate is `scripts/`, owner-reserved.
