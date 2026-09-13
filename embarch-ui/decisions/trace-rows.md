# embarch-ui decisions: Trace row admission and the served cap

**Status:** active, 2026-09-13.

Which rows a Trace view keeps, and how many it will ever hold — distinct from what a kept row renders and on which clock. Split out of [trace-view.md](trace-view.md) on 2026-09-13, a distinct mission from post-hoc rendering and clock choice, moved verbatim ([DOC-COMPACTION-PASS.md](../../DOC-COMPACTION-PASS.md)).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 19 — A stale leading prefix is dropped at render, so one bad head costs its own records and not the whole capture's microsecond axis

Decision 10's last rule — refuse the DUT clock when the two clocks contradict — charged every row for a fault in a handful. [`embarch-core`](../../embarch-core/open.md) clears the port on open (embarch-core decision 30) and a capture still opened with **18 stale records** seconds from the rest: those bytes were already inside the USB-UART bridge, where an OS-level purge does not reach. Only at render is the whole file in hand, which is what makes the head identifiable here and not there.

**It runs only on a capture whose clock is already refused**, which is the discrimination and not an optimisation: [`embarch-outpost`](../../embarch-outpost/open.md)'s inherent 13 µs inversion can never refuse a clock, so a capture carrying one is never searched and can never lose a record.

Four conditions, each one a way this would otherwise eat real data. **The step exceeds the other clock**, never a threshold chosen here. **It is a leading run** — within 512 rows [assumed: an order of magnitude over the 6 and 18 seen, itself bounded by a bridge FIFO] and no longer than the bulk after it. **The drop fixes the contradiction**, or this is a reset trimming cannot repair and the clock is refused as before. **Sign is not the signal**: with no reset the prefix is *behind* the fresh stream and steps forwards, and a backwards-only check read a 38-second capture as 563.

**Stated, never silent** — `rows` counts what was kept, so the axis note says how many went and how far their clock sat, on `embarch-outpost`'s own report-the-hole standard. **Unverified against the real 18-record prefix**; both signs have crafted fixtures, the bench debt is [open.md](../open.md)'s.

### 21 — The row cap is served on `TraceView`, not restated in `app.js`

`MAX_ROWS` (`src/trace.rs`) is what `rows_dropped_by_cap` counts against, but the banner naming it to the reader was a literal — `"caps at 250,000"`, unreachable from the constant. `TraceView` now carries `row_cap` beside `rows_dropped_by_cap`, and `app.js` renders that field: same reasoning as [gatt-capture.md](gatt-capture.md) 17's `max_monitor_targets` (task `ui/003`).

**No numeric fallback for a missing field** — a guessed cap next to a served one is the same restatement wearing a different hat. The read is still guarded (`typeof view.row_cap === "number"`), and renders a capped-but-unstated note rather than a wrong number if it is ever absent.
