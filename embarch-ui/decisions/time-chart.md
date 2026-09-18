# embarch-ui decisions: The Time chart

**Status:** active, 2026-09-18.

One axis, and everything a study did on it. The trace's own lanes stay below it, unchanged: [trace-view.md](trace-view.md), [trace-chart.md](trace-chart.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## One axis for a whole run

### 34 — One chart, one axis, and `core_rx_utc_ms` is the only clock it reads
The Live Study tab showed everything a study produced and none of it *together* — steps a table, GATT a table, consoles two scrolling panes, a plot per tap, the trace an axis of its own. "What was the DUT doing when that notification arrived" meant reading four surfaces and holding the times in your head. The Time chart is one surface: step bands, GATT, struct rows, console lines, sample strips and the trace's markers, on one X axis, above the Trace card.

**It reads `core_rx_utc_ms` and never a study CSV's `rx_utc_ms`.** One field name carries two clocks ([suite decision 3](../../suite/decisions.md)): in a trace it is embarch-core's real epoch clock, in a study's rendered rows it is **dev-bench uptime**. Merging streams is exactly where that confusion returns, and it has already cost this suite a 46× misreport (reversals row 86). `axis_column` returns `None` rather than falling back, so a tap with no Core stamp is one the chart *says* it cannot place.

**The projection is not new, it is `trace.rs`'s, extracted.** `Projection` is now the one crossing between Core's clock and a capture's counter, with two constructors and no third code path: with a usable trace the DUT's counter draws the axis and everything else is projected onto it carrying `accuracy_ms`; without one, Core's receipt clock **is** the axis and every mark is exact. `drop_stale_prefix` and `parse_rows` came out with it, so the live path cannot grow a second copy of either.

*Consequences.* `Table::time_column` preferred whichever stamp came first, and `rx_utc_ms` is column 0 in every rendering this suite writes — so **every Data-card plot ever drawn was drawn against dev-bench uptime**. Within one tap that is not wrong, which is why nothing looked broken. Fixed in the same pass, and `/rows` and `/series` now name the clock they plotted against (`core-clock`, `bench-uptime`, `row-index`). A sample tap is a binned min/max strip and **not** a mark lane: 10 kHz over 147 s is 1.47 M points, which is a smear.

*Declined:* carrying each mark's payload in the view. `GET .../mark/{id}` fetches the row, and the id is `(lane << 40) | row_index`, so a mark and a table row are the same object by construction — carrying payloads inline would reproduce [decision 18](trace-transfer.md)'s 12.6 MB defect.

### 35 — The axis is chosen once and is never silently promoted
One run can walk three axes: no trace → Core's clock; a trace tap opens with no header frame → host arrivals; the header arrives → DUT microseconds, a new unit *and* a new origin. Every mark's position changes meaning twice. **So the tier is chosen once per view and never promoted under a reader.** A study that declares a trace draws no axis until its first stamped-and-dated frame and says it is waiting.

Where a placement genuinely must change — a stale-prefix drop firing mid-run, the header frame arriving — the server bumps `axis_epoch` and the browser **re-snapshots**. Never patched across: patching would be the chart quietly moving marks somebody has already looked at. A binned reply whose epoch does not match the view is refused, not drawn. A completed study's axis cannot change at all, which is what `axis_epoch == 0` says.

*Consequences.* Marks are never placed eagerly — a session stores each one's `core_rx_utc_ms` only and places at serialisation time. That is sound because **anchors append monotonically in the host clock**: a new anchor can never land between two existing ones, so a mark already bracketed never moves, and only marks past the last anchor are affected — which the projection already refuses to place.

### 36 — Three states for a mark, and a band clamps where a point does not
A mark is placed, unplaceable, or placed-and-uncertain. **`t: None` is drawn as a count in the gutter, never at a guessed position** — the posture `placeable: false` already takes on the step row. `uncertain` is a placed mark on a projected axis: good to the axis's `accuracy_ms`, not to the microsecond the lanes beneath it measure in.

**A band clamps to the capture's edge and a point mark does not.** Clamping a band is still a truthful drawing of a step that ran past the capture; clamping a point would draw it at a time it was not at. The two counts are kept apart per end — "214 before this trace opened" says to widen the tap's scope earlier, where one merged total says nothing.

*Consequences.* **Most marks may be unplaceable, and that is the cost of drawing on the DUT's clock rather than a defect.** A tap's scope is routinely narrower than the study and the projection refuses outside the *anchors'* range: on a real traced study, 125 of 245 GATT rows placed and 120 fell after the capture closed. A merged bin carries a count and is **not** clickable, the same rule `BinRun::one` holds about never reporting a merged block as one thing.

*Consequences.* **A `Text` tap's capture on disk carries no timestamp anywhere**, so console lines are unplaceable post-hoc — the one stream this chart most wants. The lane is drawn as a count with the reason beside it rather than omitted, because a reader who cannot see the lane cannot tell it from a console that captured nothing.
