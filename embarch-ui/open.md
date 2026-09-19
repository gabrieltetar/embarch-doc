# embarch-ui: open

**Status:** active, 2026-09-13.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Whether `embarch-ui` belongs in the suite release archive is undecided** — [`embarch-umbrella`](../embarch-umbrella/decisions/install.md) decision 14's and the suite's. `assemble-suite.yml` ships three binaries, not this one, so a fresh `embarch setup` can't author or read back a trace. **Documentation half closed** (`tasks/suite/019`): [user-guide](../suite/user-guide.md) §3, [studies-guide](../suite/studies-guide.md) §4. **Trigger:** first non-owner engineer walks the studies guide end to end.

- **The run dialog does not read a *stored* study's build spec.** It knows the step table's Build card and says so; a run-only file's spec is in the file, and the dialog tells the reader which case it is rather than describing the wrong study's build. **Trigger:** the first time somebody runs a saved study with a build spec from the Live Study tab and wants to see what it will flash before it does. Decision 38.

- **A run whose build *fails* has never been watched.** The happy path is exercised end to end on hardware (2026-09-19), but every failure branch of the build card — a compile error mid-stream, a flash that will not take, a reset that fails — has only unit tests behind it. The one that matters most is the first: a Zephyr error arrives as ordinary `stderr` lines and then a `failed` frame, and **nothing checks that the card leaves the error on screen rather than scrolling it past** the 600-line cap. **Trigger:** the next build that breaks, which needs no deliberate run — just don't clear the card when it happens.

- **Settled, decision 27, permanently — not pending.** `ui/065` checked `embarch-core`'s `GET .../load/spans` (`tasks/core/076`) against `trace.rs` field-for-field: Core's `Gap` was thinner (missing `records_lost`/`row_index`/`unbounded_start`, rendered today in `app.js`'s gap table); no axis-health diagnostics were served; and point events build in the same row pass as `Lane`/`Span`/`Gap`, so the row decode and clock-health/stale-prefix search stay regardless. `embarch-core` decision 66 widened `Gap` to full parity but keeps the diagnostics and point events out — the split stays; full reasoning there and in this crate's decision 27.

- **A trace's placement has now been compared against a second stream, and it holds — against GATT, not against a power capture.** The Time chart is the instrument (decision 34), and it was built to *show* a misalignment rather than absorb one. On study `b1e9ec7d` (traced, dual-clock, 6 ms resolution), **64 of 64** separable GATT marks land inside the band of the step their own row names; 125 of 245 rows placed and 120 fell after the capture closed, which is the tap's scope and not an error. **Still unrun:** the same check against a **power capture** — no study on Core's disk carries a `Samples` tap, so the sample strip and the struct lane are covered by unit tests and by nothing on real data. Every outpost wire constant stays an unmeasured default, overhead deliberately uncharacterised.

- **The 250,000-row cap is kept on measurement, not extrapolation.** `trace::scratch_view::synth_capture` builds an in-memory capture shaped like the fixture; `measure_the_row_cap_at_scale` and `measure_the_request_path_at_scale` decode/encode it at scale [release build, synthetic]:

  |rows|decode|resident JSON¹|`/bins`²|encode|total|
  |---|---|---|---|---|---|
  |250k|257ms|4.48MB|165KB|4.6ms|210ms|
  |500k|604ms|9.03MB|180KB|8.3ms|518ms|
  |1M|1.69s|18.1MB|1.5KB|23.5ms|1.32s|

  ¹server-side only, never sent (decision 18). ²1,170-wide grid stays small — payload bound (decision 18) holds past 250k; decode/memory, not payload, cost the raised cap. **Still unmeasured:** the three awaited Core calls (`study_streams`, `get_study_stream`, `study_steps`) `decode_trace` makes before `parse` runs — end-to-end `/study/{id}/streams` cost over real HTTP is unknown. Re-measure all three, get a live-Core number, before calling 1.32 s the whole cost.

- **A signal mismatch has nowhere durable to land**, so a declared-but-wrong signal shows up in the Topology tab or nowhere. Closed upstream as not-needed-yet, two-part trigger: half fired (signals declarable through this tab), half not (no wire, no bridge). Carried by the row's own carrier cell, not the alert list.

- **The live Time chart has never been driven by a trace.** Its no-trace half ran on the bench on 2026-09-18 (`bds-ppg-drain`, 12 steps, 349 s): live and post-hoc agree on the axis to 3 ms and on GATT to the mark. **The traced half is unrun** — the `outpost` signal's declared route is `direct/port_serial=5` and no device with that serial is present, so nothing has ever exercised `LiveAxis`'s anchor path, the epoch bump on a late header, or the non-monotone refusal against a real clock. **Trigger:** the outpost bridge attached and the signal re-declared against it. Unparks `tasks/core/093`.

- **The stale-prefix drop has never met a real stale prefix** (decision 19): tested against crafted fixtures both ways, but the case it exists for — **18 records** a real capture opened with, buffered in the USB-UART bridge past `embarch-core`'s open-time purge — has not been replayed. **Hardware debt, the owner's session:** run a study, open its Trace tab, check the axis note reports a dropped prefix where the capture fell to the millisecond clock. Until then, `STALE_PREFIX_MAX_ROWS` (512) is an assumption about a bridge FIFO nobody has measured.

- **A saved study is never checked against the `.eap` file it was built from**, and the tab will offer a protocol whose text no longer matches what a saved study carries. The check is server-side and belongs to `embarch-study-designer` — its [open.md](../embarch-study-designer/open.md) carries the question and the trigger; this repo's half is only where a divergence would be *shown*. Named here so a reader of this tab does not conclude the silence is a design choice.

- **The `Debug` level's clamp note has never fired.** Legs E and J of `tasks/ui/070` ran on a live nRF54L15 bench on 2026-09-18 and closed everything else: the same study at `Off` and at `Debug` captured **0 vs 7,440 bytes** on the reserved `dev-bench` tap, so the level reaches the firmware and it acts on it. What did not fire is the clamp itself — `app/prj.conf` is `CONFIG_LOG_DEFAULT_LEVEL=4` with runtime filtering, so `Debug` is *reachable* and there is nothing to report. Seeing the note needs a deliberately quieter build. **Its delivery path is proven** (the same `send_log_line` channel carried 129 lines); only its trigger is unexercised.

