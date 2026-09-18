# embarch-ui decisions: The Live Study tab

**Status:** active, 2026-09-18.

One tab that runs a study, watches it land, and reads a past one back. What the chart inside it draws is [trace-view.md](trace-view.md) and [trace-chart.md](trace-chart.md), unchanged by the move.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Running, watching, and reading back

### 31 — Live Study replaces Trace, owns running, and keeps the run so far server-side
A run and its results were split across two tabs and a download link. The Study Designer authored *and* ran, and during a run **the only live thing was a badge**: `running 3/7`, with the step rows, the provenance and the stream list all appearing at once when the study ended, because that tab learned about the run by **polling `GET /study/{id}`**. The Trace tab was post-hoc, reachable only by pasting a `study_id`, and rendered one `OutpostTrace` tap; every other tap was a row in a table with a byte count and a download button. And **no route listed past studies at all** — a result was reachable only if you had kept its id.

Meanwhile embarch-core had been pushing step completions, sample batches and GATT entries live since its own decision 24, and the shared client had consumed them since `embarch-api`'s `study_watch`. **embarch-ui had never subscribed.**

**The rings live here, in this process, not in the browser.** One `LiveSession` per study subscribes **once** to embarch-core's stream and keeps the run so far in bounded rings; `GET /api/live/events` sends a **full snapshot frame on connect** and incremental frames after it. That ordering is the whole feature: embarch-core keeps no replay ([its decision 41](../../embarch-core/decisions/study-record.md)), so a browser opening or reloading mid-run would otherwise start at "now" with a hole of unknown size. It also means a second tab costs embarch-core nothing, the same shape the Dashboard's single `poll_loop` already has.

**Every ring counts what it dropped**, because a short feed and a complete one must not look alike. A sample series **decimates 2:1 rather than dropping its oldest** and reports its stride: dropping the oldest would silently change what window a plot covers as a run goes on, which is a plot that lies about its own extent rather than one that is coarse.

**The polled path is kept as the documented fallback, not deleted.** The tab runs on the shared client's `follow_study`, which subscribes, polls once for a study that was already over, falls back to polling on a drop, and reports `lagged` — and the tab **says which mode is in force**. Re-implementing that here would have meant two copies of the one piece of logic that has to be right about missing data.

*Consequences.* The Trace tab is gone with no back-compat, and `#trace?study=…&tap=…` with it: the chart is a card on this page now, on whichever study the page has open, so a fragment carrying a study id addressed a view that no longer exists. The Study Designer's own run card, its `RunState`/`run_tx`/`watch_study` plumbing and `GET /api/study-designer/events` are deleted; its Run buttons post and switch tabs. **`decodeOutcome`, `outcomeBadge`, `stepDetail`, `recordsCell`, `renderProvenance`, `renderRunStreams` and `sdRunningStepLabel` moved rather than being copied** — they carry decisions 20 and 23 and the record-check invariants, and a second copy is the exact defect those decisions exist to stop.

*Declined:* inner sub-views. One long page of stacked cards, because every card is about the same run and a tab bar inside a tab is a place to lose one.

### 32 — A `Text` tap renders as a console; that is the whole rule
Two consoles were wanted — dev-bench's, and the DUT's own shell — and the temptation was two mechanisms: one for the reserved `dev_bench_log_tap` and one for whatever a study declares on a notify characteristic. There is one. **A `Text`-encoded tap gets a console card.** `dev-bench` is simply the reserved one every study carries; a DUT shell is a `Text` tap the study declared, and a study that declares none shows **no console card at all** rather than an empty one.

**Lines are assembled server-side, and the remainder is published as partial.** embarch-core carries a chunk exactly as it arrived and refuses to invent line boundaries ([its decision 70](../../embarch-core/decisions/streams.md)); a chunk can split a line *and* a UTF-8 character. So `live_study.rs` carries the partial remainder between chunks and the UI draws it dimmed and marked — **never padded into a line the tap did not send.** A line past 8 KB is cut and says so, for the same reason: a `Text` tap streaming a megabyte with no newline is a binary tap somebody declared wrong, and the honest answer is to say so rather than grow.

*Consequences.* `Raw` gets a hex head and a download, not a console — nothing was declared to render those bytes as ([`embarch-study-designer` decision 39](../../embarch-study-designer/decisions.md)), and embarch-core deliberately pushes no event for one.

### 33 — The browser parses no CSV here either, and a post-run re-read never blanks a card
The Data cards' tables and plots are decoded in Rust and handed over as columns, rows and bins — the same rule the chart already held ([decisions/trace-transfer.md](trace-transfer.md) 18; [suite decision 4](../../suite/decisions.md)). A tap's rendered file is a CSV whose column order is `embarch-study-designer`'s, and a browser that learned it would be a second place that knowledge lives. Which columns are numeric is decided **from the data, not from a name table**, and a column that is numeric *most* of the time is not one — `payload_hex`/`decode_note` hold the reason a Struct row did not fit its layout, and plotting that column would drop exactly the rows that say what went wrong.

**A live plot is labelled a preview and re-rendered from the file when the run ends** — but the re-read replaces a card **only where its own read succeeded.** Found by the browser harness on its first run: the post-run re-read tore every card down and rebuilt it from disk, which on a tap embarch-core would not serve left a blank card where a watched console had been, and re-rendered a stale polled `running` over an observed `failed`. **A terminal status is never un-said by a later poll**: embarch-core's job registry can still report `running` for the moment between the last step landing and the job closing.
