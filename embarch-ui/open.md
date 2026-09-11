# embarch-ui: open

**Status:** active, 2026-09-04.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Whether `embarch-ui` belongs in the suite release archive is undecided, and is not this repo's call.** `assemble-suite.yml` ships three binaries, not this one, so a fresh `embarch setup` cannot author or read back a trace. **The documentation half is closed** (`tasks/suite/019`): [user-guide](../suite/user-guide.md) §3 and [studies-guide](../suite/studies-guide.md) §4 say it's a separate build and where to get it. Making it a fourth archive member is a release-surface call, [`embarch-umbrella`](../embarch-umbrella/decisions/install.md) decision 14's and the suite's. **Trigger:** the first engineer who is not the repo owner walks the studies guide end to end.

- **Where the reflash selector should live is genuinely undecided.** `run_study --reflash` is `embarch-api` orchestration; `embarch-ui` posts studies straight to Core and builds nothing. Three shapes: duplicate the orchestration here, depend on `embarch-api` (a direction the suite has nowhere), or leave reflash terminal-only. Settled as the third for now (the run dialog says so) — "the UI cannot reflash" is a limitation, not a design goal. Decision 11.

- **Nothing has compared a trace's placement against a second stream in the same study.** The DUT clock measures, the host **places** it, at an observed **4.0 ms** median placement resolution on the reference capture. Whether the two line up against, say, a power capture is what the dual-clock flag checks, and has not been run — every outpost wire constant remains an unmeasured default, overhead deliberately uncharacterised.

- **The 250,000-row cap is kept, against measurement rather than extrapolation.** `trace::scratch_view::synth_capture` builds a capture of the committed fixture's shape entirely in memory (no file, no board); `measure_the_row_cap_at_scale` and sibling `measure_the_request_path_at_scale` decode/encode it at scale [release build, in-memory synthetic capture]:

  |rows|decode|resident JSON¹|`/bins`²|encode|total|
  |---|---|---|---|---|---|
  |250k|257ms|4.48MB|165KB|4.6ms|210ms|
  |500k|604ms|9.03MB|180KB|8.3ms|518ms|
  |1M|1.69s|18.1MB|1.5KB|23.5ms|1.32s|

  ¹server-side only, never sent (decision 18); decode/JSON/bins [2026-09-09], encode/total [2026-09-10]. ²1,170-wide grid, stays small — payload bound (decision 18) holds past 250k; decode/memory, not payload, are the cost of the raised cap. **Still unmeasured:** the three awaited Core calls (`study_streams`, `get_study_stream`, `study_steps`) `decode_trace` makes before `parse` runs — no synthetic capture stands in for a live Core answering real HTTP, so the true end-to-end `/study/{id}/streams` cost is unknown. **Kept at 250,000** with this measurement as the reason; re-measure all three points and get a live-Core number before treating 1.32 s as the whole cost.

- **A signal mismatch still has nowhere durable to land, so a declared-but-wrong signal shows up in the Topology tab or nowhere.** Closed upstream as not-needed-yet, two-part trigger: half fired (signals declarable through this tab), half not (no wire, no bridge). Carried by the row's own carrier cell, not the alert list.

- **The stale-prefix drop has never met a real stale prefix** (decision 19). Tested against crafted fixtures in both signs, but the case it exists for — the **18 records** a real capture opened with, buffered inside the USB-UART bridge past `embarch-core`'s open-time purge — has not been replayed through it. **Hardware debt, the owner's own session:** run a study, open its Trace tab, and check the axis note reports a dropped prefix where the capture previously fell to the millisecond clock. Until then `STALE_PREFIX_MAX_ROWS` (512) is an assumption about a bridge FIFO nobody has measured.
