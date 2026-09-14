# embarch-ui: open

**Status:** active, 2026-09-13.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Whether `embarch-ui` belongs in the suite release archive is undecided, and not this repo's call** — [`embarch-umbrella`](../embarch-umbrella/decisions/install.md) decision 14's and the suite's. `assemble-suite.yml` ships three binaries, not this one, so a fresh `embarch setup` can't author or read back a trace. **Documentation half closed** (`tasks/suite/019`): [user-guide](../suite/user-guide.md) §3, [studies-guide](../suite/studies-guide.md) §4 — separate build, and where to get it. **Trigger:** first non-owner engineer walks the studies guide end to end.

- **Where the reflash selector should live is undecided.** `run_study --reflash` is `embarch-api` orchestration; `embarch-ui` posts studies straight to Core, building nothing. Three shapes: duplicate it here, depend on `embarch-api` (a direction the suite has nowhere), or leave reflash terminal-only — settled as the third; the run dialog's string says so: a limitation, not a design goal. Decision 11.

- **Half the trace analysis moved to `embarch-core`; half is still duplicated** ([suite decision 4](../suite/decisions.md)). `ui/051` retired the aggregation — shares and coverage now come from `.../stream/{name}/load` ([`embarch-core` decision 62](../embarch-core/decisions.md)). **`Lane`/`Span`/`Gap` and the four exclusion flags are still derived in both `trace.rs` and `outpost_load.rs`**: that route answers with the rollup only. Decision 62's cost stands for this half — `RecordKind`, gap semantics or an exclusion rule changes in both. Closing it needs per-span data, or a decision it stays split.

- **Nothing has compared a trace's placement against a second stream in the same study.** The DUT clock measures; the host places it, at an observed **4.0 ms** median resolution on the reference capture. Whether the two line up against a power capture is what the dual-clock flag checks and has not run — every outpost wire constant stays an unmeasured default, overhead deliberately uncharacterised.

- **The 250,000-row cap is kept on measurement, not extrapolation.** `trace::scratch_view::synth_capture` builds an in-memory capture shaped like the fixture; `measure_the_row_cap_at_scale` and `measure_the_request_path_at_scale` decode/encode it at scale [release build, synthetic]:

  |rows|decode|resident JSON¹|`/bins`²|encode|total|
  |---|---|---|---|---|---|
  |250k|257ms|4.48MB|165KB|4.6ms|210ms|
  |500k|604ms|9.03MB|180KB|8.3ms|518ms|
  |1M|1.69s|18.1MB|1.5KB|23.5ms|1.32s|

  ¹server-side only, never sent (decision 18). ²1,170-wide grid stays small — payload bound (decision 18) holds past 250k; decode/memory, not payload, cost the raised cap. **Still unmeasured:** the three awaited Core calls (`study_streams`, `get_study_stream`, `study_steps`) `decode_trace` makes before `parse` runs — no synthetic capture stands in for live Core over real HTTP, so end-to-end `/study/{id}/streams` cost is unknown. Re-measure all three, get a live-Core number, before calling 1.32 s the whole cost.

- **A signal mismatch still has nowhere durable to land**, so a declared-but-wrong signal shows up in the Topology tab or nowhere. Closed upstream as not-needed-yet, two-part trigger: half fired (signals declarable through this tab), half not (no wire, no bridge). Carried by the row's own carrier cell, not the alert list.

- **The stale-prefix drop has never met a real stale prefix** (decision 19): tested against crafted fixtures both ways, but the case it exists for — **18 records** a real capture opened with, buffered in the USB-UART bridge past `embarch-core`'s open-time purge — has not been replayed. **Hardware debt, the owner's session:** run a study, open its Trace tab, check the axis note reports a dropped prefix where the capture fell to the millisecond clock. Until then, `STALE_PREFIX_MAX_ROWS` (512) is an assumption about a bridge FIFO nobody has measured.
