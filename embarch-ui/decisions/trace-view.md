# embarch-ui decisions: The Trace view

**Status:** active, 2026-09-02.

Reading an [embarch-outpost](../../embarch-outpost/decisions.md) capture post-hoc: what it renders and on which clock. Navigating the chart is in [trace-chart.md](trace-chart.md); the routing half of decision 10 is in [topology-tab.md](topology-tab.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 10 — Trace half: a Trace view renders an outpost capture post-hoc

**Post-hoc, deliberately**, because outpost capture is study-scoped with no live feed — the one surface in this UI that is not live, and the honest shape for the data rather than an omission. Two things it must not do, both being the visual form of a lie the rest of the suite works hard to avoid: **a dropped-record gap is drawn as a gap**, labelled with what was lost, never bridged into a continuous timeline; and a trace whose build ID did not match is **never rendered as a *named* trace**.

**"Not rendered at all" was too strong.** Core settled something better: the rows *are* written, unnamed, with the reason recorded — because **a timeline of numeric thread pointers is a real answer**, and it is honestly distinguishable from a named one. So a banner leads with Core's reason verbatim and every lane below is the raw pointer or vector number it actually is. Nothing over HTTP could tell a refused trace from a named one, which made that unbuildable as stated: the field recording *why* a trace has no names had no HTTP caller at all. Settled with a new route rather than a field on the per-tap result type — that type rides inside the study result, so growing it would be **a host schema bump for a fact that is Core-side bookkeeping and means nothing to dev-bench.** Named and timed are read as **two separate booleans**, because a trace can be either without the other.

**Reading the rendered CSV rather than the raw bytes, deliberately.** Decoding raw here would have **no manifest at all** — it is on Core's side, bound by the flash — and so would produce an unnamed trace every time, strictly less true than what Core already produced. What is *not* re-derived here is trace knowledge: the column list is checked against the shared crate's own header and **refused if it differs**, and the record vocabulary comes from that crate, so `app.js` knows nothing about a trace's shape.

**A gap band is not an empty interval** — the finding that changed the drawing. A gap says *records were lost in here*, not *nothing happened here*: the records at both ends survived. So the band is an **overlay over what survived**, with every span it touches flagged continuity-not-established, rather than a hole punched through real data. **Erasing real records to make the picture tidier would be its own version of the lie this half exists to avoid.**

**A band is a measurement on the DUT's clock and a bound on the host's.** On the host's, a gap record is guaranteed to be the *first record of its frame*, so the losses fall between the previous frame's arrival and that frame's — drawn deliberately *wider* than one frame when a header frame arrived in between, because a rendered trace carries only frames that held records. **Too wide is still a bound; too narrow would be a claim.** On the DUT's, the firmware states the interval outright, so the band is arithmetic, never open-started, and typically far tighter. A gap's own stamp legitimately runs *ahead* of the rows after it — the ring is FIFO and records reserved before the overflow are still draining — which is why the band's end comes from the firmware's own figure and never from "the next row".

**What the timeline looks like was designed against the closest thing that existed** — a committed `native_sim` capture from the real firmware encoder, and stated as such rather than as a DUT. Three of its seven thread pointers resolve to no name and every ISR reports unknown, because that ELF has no interrupt table at all; both are the **common** case on a real image, so **"unnamed" is a first-class state here rather than an error path**, drawn italic and dotted with the number as the label. One thing the fixture changed directly: markers began as full-height rules and 132 across 760 ms swamped every span, so they became a tick in their own strip plus a faint rule. Relatedly, an empty markers table now says markers are **opt-in** — the reference-dut declares none and will not, and rendering "0 markers" the way a dropped record is rendered reads as an absence where there is none.

**The load repartition, and the one thing it refuses to do.** Understanding load repartition is what a results UI is *for*; the timeline came first only because a gap is visible on a timeline and invisible in a total. Per subject — each thread, each ISR vector, idle — entries, measured spans, total time, share of the window, as arithmetic over spans the parser already built. **Not a second decode**, which is the property that matters: every caveat it reports is one a span already carried.

**A repartition computed across an interval where records were dropped is not a measurement**, so classes of span whose drawn width is an *extent* rather than a duration are **excluded from the total and counted separately** rather than folded in or dropped. Three are properties of the *records* — crossing a gap, no closing record, no opening record. **The fourth is a property of the clock:** below-resolution means both ends arrived in one frame on the host's clock, and is **never set on the DUT's**, because both ends stamped themselves. Entries count every span regardless, because "this subject ran N times" survives all four doubts. **The gap-covered fraction of the window renders above the table, not as a footnote, because it is the number deciding whether the rest is a measurement at all.**

**Idle is reported twice by construction** — found by building it, claimed by no doc. Zephyr's idle thread appears both as idle records *and* as ordinary switches into the thread the manifest names idle, so a total over "threads plus idle" claimed nearly twice the window. **Thread lanes alone are the mutually-exclusive set; the idle-record lane is a corroborating figure that is never added** — and the two are allowed to *disagree*, which they do on the committed capture, with the disagreement surfaced rather than averaged away. ISR time stays out of the same sum because an ISR runs inside whatever it interrupted. **So the shares deliberately do not total 100%, and the card says why.** Found only because the assumption was written down as an assertion and run.

**The axis is a three-tier choice over the two clocks the wire carries, and picking the wrong tier was worth a 46× error.** Written when the DUT had no clock; layout 3 restored a per-record microsecond stamp and **this view did not follow for a day**, going on charging every span the whole frame interval. It reported the outpost's own drain thread at **78% of the measured extent** where the DUT's clock says **1.6%** — 3.9 ms for 85 µs of work — and **4286 of 4955 spans as below the resolution when none were.** Nothing was wrong with the wire; the coarser of two available clocks was being read.

| unit | clock | requires | for |
|---|---|---|---|
| `us` | `dut-cycles` | every row has a DUT stamp | **measuring** — both ends of a span stamp themselves |
| `ms` | `host-arrival` | every row's frame is stamped | **placing** — the clock every other stream in the study is on |
| `frame` | `frame-index` | neither | order, with no duration claimed |

Five rules, each a lie this view would otherwise tell:

- **A tier is chosen for a whole view, never per span.** A mixed axis arrived at one span at a time is unauditable. **One row missing the stamp its tier needs drops the entire view to the next tier down.**
- **Both clocks are reported even though one draws the axis.** The frame resolution stays populated on the DUT clock, labelled as the **placement** resolution: how finely this trace lays against a power capture, which is the one job the DUT's counter cannot do.
- **Records in one frame are drawn at one instant *on the host's clock*.** Spreading them across the interval would look better and be fabricated. On the DUT's they have their own instants — not interpolation, the stamp the firmware wrote.
- **What is below the resolution is a property of the clock, not of the wire.** On the host's clock most ISR spans are exactly that, so **on that clock this view reports ISR entries and refuses to report ISR time.** On the DUT's it reports both.
- **A backwards axis position is reported, not smoothed**, and the axis note says which clock stepped — the wall clock (an NTP correction) or a lost counter wrap.

### 19 — A stale leading prefix is dropped at render, so one bad head costs its own records and not the whole capture's microsecond axis

Decision 10's last rule — refuse the DUT clock when the two clocks contradict — charged every row for a fault in a handful. [`embarch-core`](../../embarch-core/open.md) clears the port on open (embarch-core decision 30) and a capture still opened with **18 stale records** seconds from the rest: those bytes were already inside the USB-UART bridge, where an OS-level purge does not reach. Only at render is the whole file in hand, which is what makes the head identifiable here and not there.

**It runs only on a capture whose clock is already refused**, which is the discrimination and not an optimisation: [`embarch-outpost`](../../embarch-outpost/open.md)'s inherent 13 µs inversion can never refuse a clock, so a capture carrying one is never searched and can never lose a record.

Four conditions, each one a way this would otherwise eat real data. **The step exceeds the other clock**, never a threshold chosen here. **It is a leading run** — within 512 rows [assumed: an order of magnitude over the 6 and 18 seen, itself bounded by a bridge FIFO] and no longer than the bulk after it. **The drop fixes the contradiction**, or this is a reset trimming cannot repair and the clock is refused as before. **Sign is not the signal**: with no reset the prefix is *behind* the fresh stream and steps forwards, and a backwards-only check read a 38-second capture as 563.

**Stated, never silent** — `rows` counts what was kept, so the axis note says how many went and how far their clock sat, on `embarch-outpost`'s own report-the-hole standard. **Unverified against the real 18-record prefix**; both signs have crafted fixtures, the bench debt is [open.md](../open.md)'s.
