# embarch-ui: open

**Status:** active, 2026-09-13.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Whether `embarch-ui` belongs in the suite release archive is undecided** — [`embarch-umbrella`](../embarch-umbrella/decisions/install.md) decision 14's and the suite's. `assemble-suite.yml` ships three binaries, not this one, so a fresh `embarch setup` can't author or read back a trace. **Documentation half closed** (`tasks/suite/019`): [user-guide](../suite/user-guide.md) §3, [studies-guide](../suite/studies-guide.md) §4. **Trigger:** first non-owner engineer walks the studies guide end to end.

- **Where the reflash selector should live is undecided.** `run_study --reflash` is `embarch-api` orchestration; `embarch-ui` posts studies straight to Core, building nothing. Three shapes: duplicate it here, depend on `embarch-api` (a direction the suite has nowhere), or leave reflash terminal-only — settled as the third: a limitation, not a design goal. Decision 11.

- **Settled, decision 27, permanently — not pending.** `ui/065` checked `embarch-core`'s `GET .../load/spans` (`tasks/core/076`) against `trace.rs` field-for-field: Core's `Gap` was thinner (missing `records_lost`/`row_index`/`unbounded_start`, rendered today in `app.js`'s gap table); no axis-health diagnostics were served; and point events build in the same row pass as `Lane`/`Span`/`Gap`, so the row decode and clock-health/stale-prefix search stay regardless. `embarch-core` decision 66 widened `Gap` to full parity but keeps the diagnostics and point events out — the split stays; full reasoning there and in this crate's decision 27.

- **Nothing has compared a trace's placement against a second stream in the same study.** The DUT clock measures; the host places it, at an observed **4.0 ms** median resolution on the reference capture. Whether the two line up against a power capture is what the dual-clock flag checks and has not run — every outpost wire constant stays an unmeasured default, overhead deliberately uncharacterised.

- **The 250,000-row cap is kept on measurement, not extrapolation.** `trace::scratch_view::synth_capture` builds an in-memory capture shaped like the fixture; `measure_the_row_cap_at_scale` and `measure_the_request_path_at_scale` decode/encode it at scale [release build, synthetic]:

  |rows|decode|resident JSON¹|`/bins`²|encode|total|
  |---|---|---|---|---|---|
  |250k|257ms|4.48MB|165KB|4.6ms|210ms|
  |500k|604ms|9.03MB|180KB|8.3ms|518ms|
  |1M|1.69s|18.1MB|1.5KB|23.5ms|1.32s|

  ¹server-side only, never sent (decision 18). ²1,170-wide grid stays small — payload bound (decision 18) holds past 250k; decode/memory, not payload, cost the raised cap. **Still unmeasured:** the three awaited Core calls (`study_streams`, `get_study_stream`, `study_steps`) `decode_trace` makes before `parse` runs — end-to-end `/study/{id}/streams` cost over real HTTP is unknown. Re-measure all three, get a live-Core number, before calling 1.32 s the whole cost.

- **A signal mismatch has nowhere durable to land**, so a declared-but-wrong signal shows up in the Topology tab or nowhere. Closed upstream as not-needed-yet, two-part trigger: half fired (signals declarable through this tab), half not (no wire, no bridge). Carried by the row's own carrier cell, not the alert list.

- **The stale-prefix drop has never met a real stale prefix** (decision 19): tested against crafted fixtures both ways, but the case it exists for — **18 records** a real capture opened with, buffered in the USB-UART bridge past `embarch-core`'s open-time purge — has not been replayed. **Hardware debt, the owner's session:** run a study, open its Trace tab, check the axis note reports a dropped prefix where the capture fell to the millisecond clock. Until then, `STALE_PREFIX_MAX_ROWS` (512) is an assumption about a bridge FIFO nobody has measured.

- **A saved study is never checked against the `.eap` file it was built from**, and the tab will offer a protocol whose text no longer matches what a saved study carries. The check is server-side and belongs to `embarch-study-designer` — its [open.md](../embarch-study-designer/open.md) carries the question and the trigger; this repo's half is only where a divergence would be *shown*. Named here so a reader of this tab does not conclude the silence is a design choice.

- **Legs E and J of `tasks/ui/070` are unrun.** Everything else was driven headless against the deployed binary (44 checks, `geckodriver`), but two need the dev bench plugged in: **17 steps against a live bench** — the caps note reading `17 · 16 · 64` and then reading *unknown* once the bench is unplugged, which is the branch that renders on a real `dev_bench_limits` rather than a synthetic one — and **a `Debug` run against a quieter build**, which is the only way to see the firmware report its clamp on its own log stream. The note's prose says to read the clamp there; nobody has. **Hardware debt, the owner's session.**

