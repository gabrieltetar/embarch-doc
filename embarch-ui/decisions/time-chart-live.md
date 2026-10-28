# embarch-ui decisions: The Time chart, live

**Status:** active, 2026-10-28.

Split verbatim from [time-chart.md](time-chart.md), which holds decisions 34-36 and 66. Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

## Live

### 37 — The Time chart is fed live through the same projection, and a mark is placed once
The chart is the answer to "what was the DUT doing when that notification arrived", and that question is asked *while the run happens*. So the live session builds the same axis from the events Core pushes — `OutpostRows` for the trace, `core_rx_utc_ms` on GATT and console chunks, and `StepCompleted`'s own three stamps for the bands — through the **same** `Projection` and the **same** `parse_rows`. A run watched live and the same run reloaded are one picture, not two.

**A mark is never placed eagerly.** A lane stores each mark's `core_rx_utc_ms` only; placement happens when a frame is serialized, and a lane hands out what the axis can place *now*, walking forward and stopping at the first mark it cannot. That is sound rather than a dodge because **anchors append monotonically in the host clock**: a new anchor can never land between two existing ones, so a mark already bracketed never moves, and only marks past the last anchor are affected — which the projection already refuses to place. Those are a **pending count at the leading edge**, never a guessed x. A mark already sent is never re-sent, which is what stops a reader watching one move.

**A non-monotone anchor is rejected and counted, never inserted.** `current_utc_ms()` is not monotonic — an NTP correction mid-capture makes an arrival go backwards — and the post-hoc path sorts and dedups its anchors, which an append-only feed cannot do. One inserted backwards would break the projection's binary-search precondition and land a mark anywhere.

**A study that declared no trace does not wait for one.** Whether one is declared is read once off the stream index before the first event, because getting it wrong means either opening on Core's clock and flipping to the DUT's counter a second later, or waiting forever for a trace that is not coming. With none declared, Core's receipt clock *is* the axis from the first two instants and every mark on it is exact — the same `Projection::core_clock` the post-hoc chart uses, and growing it moves nothing already on it.

*Consequences.* Where a placement genuinely must change — the header frame arriving and promoting the tier, or a stale prefix dropping mid-run — the server **bumps `axis_epoch` and the browser re-snapshots**, and a binned reply from another epoch is refused rather than drawn. Until the trace has given two frames carrying both clocks there is **no axis**, and the tab says which of the three reasons it is waiting on rather than drawing one. On a terminal status the tab re-reads `/api/time-chart/{id}` and redraws: the rendered files are authoritative (`embarch-core` decision 72). **Measured on the bench** (`bds-ppg-drain`, 12 steps, 349 s): live and post-hoc agree on the axis to 3 ms and on GATT to the mark; the consoles are one line longer on disk, which is the partial-line rule working rather than a disagreement. The Time chart's live marks are binned **in the browser**, which is drawing rather than decoding — they are already here, bounded by a server-side ring, and a round trip per frame would buy nothing; the rule a merged bin is not clickable is stated in both binners.
