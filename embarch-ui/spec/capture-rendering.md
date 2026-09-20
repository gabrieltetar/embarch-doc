# embarch-ui spec: what a capture renders as

**Status:** active, 2026-09-19.

Split verbatim from [../spec.md](../spec.md), 2026-09-19 (`tasks/ui/069`'s `spec.md` half), when decision 44's Topology invariants took that file past its ledger grace. **Nothing below is reworded from the version that moved.** This file's mission — what a row, a gap, a clock, a step outcome and a console line *mean* once they reach the browser, live or read back from disk — is distinct from [../spec.md](../spec.md)'s, which is what this UI is and what it refuses.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

## Invariants

- **A trace whose build ID did not match is never rendered as a *named* trace**: it renders unnamed, with Core's reason verbatim, every lane the raw pointer or vector it is.
- **A dropped-record gap is drawn as a gap**, overlaid on the records that survived, never bridged into a timeline.
- **An axis tier is chosen once per view, never per span**: one row missing the stamp its tier needs drops the view a tier.
- **A capture opening with pre-reset records loses the prefix, not the microsecond axis**, only where the clock is already refused, and the axis note says what went (decision 19). **A refused row is counted, never merely skipped**: "every row in the capture" is said only when the refused and capped counts are both zero.
- **The run badge names the step *now running*, not the count finished** (decision 20): Core's `current_step` is the last step that *finished*, so the badge adds two and clamps; `null` reads as step 1, and a zero-step study gets no counter.
- **A capture that was not checked never reads as clean.** An absent `StreamRef.records` means no framing was declared, a different fact from "every record verified"; an empty one reads "nothing to check", which is why `RecordReport::all_verified()` is not used.
- **One decoder reads a step outcome in both wire shapes** (decision 23); an unrecognised one renders visibly wrong, never as a pass or a dash.
- **A capped ring says it is capped** — the feed, each console and each live series are bounded server-side and count what they dropped ("the last 5,000 of 8,412"); a series **decimates rather than dropping its oldest**, showing one point in N (decision 31).
- **A partial console line is shown as partial**: a `Text` chunk arrives verbatim and can end mid-line (`embarch-core` decision 70), and the remainder is never padded into a line the tap did not send.
- **`lagged` is displayed, never swallowed**, and this UI's own broadcast overrun is a *different* fact from Core's: the first says the disk record is complete and this feed is not, the second that a reload catches up.
- **`interrupted` is never rendered as completed or failed** (`embarch-core` decision 69), and **a terminal status is never un-said by a later poll** — Core's registry can still report `running` between the last step landing and the job closing.
- **A post-run re-read replaces a card only where its own read succeeded**: a tap Core will not serve keeps what the feed put there.
- **A shared axis reads `core_rx_utc_ms` and nothing else** — a study CSV's `rx_utc_ms` is dev-bench uptime under one name ([suite decision 3](../../suite/decisions.md)). A mark is placed, unplaceable or uncertain; unplaceable is a gutter count, never a guessed position; the tier is chosen once and an improvement is an epoch bump; live, a mark is placed once ([decisions/time-chart.md](../decisions/time-chart.md)).

## The trace chart

SVG with server-side aggregation, so **the element count is bounded by pixels × lanes, not by the dataset**. **Filtering changes the drawing and nothing else: the load repartition stays computed across every lane, and says so** — a denominator quietly following a view filter would be a measurement of nothing ([decisions/trace-chart.md](../decisions/trace-chart.md)). It is a card on the Live Study tab. Reference numbers, the bin-fetch endpoint and the two served view caps: [interfaces.md](../interfaces.md).
