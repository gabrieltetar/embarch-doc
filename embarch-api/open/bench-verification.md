# embarch-api: open questions, bench and toolchain verification

**Status:** active, 2026-11-13. Split from [open.md](../open.md) by mission (`tasks/api/150`); bullets verbatim.

Truth: [spec.md](../spec.md). Rationale: [decisions.md](../decisions.md).

## Unverified against real hardware or toolchain

- **`bootload` has never met a real bootloader** ([decisions](../decisions/bootload.md) 80, 81). Mock-tested; the first DUT has no MCUboot yet, so no real `domains.yaml` or upload seen.
- **`bench_exchange` has never met two real consoles** ([decisions](../decisions/bench-exchange.md) 89). Mock-tested; cross-console order unmeasured: Core's receive times when sent (`api/147`), else poll-bounded.
- **`study_watch` has met a real embarch-core; the rest has not.** Leg 021: pushed frames and `polled` fallback seen ([decisions](../decisions/study-events.md) 48, 49). Unexercised: `study-status --follow`, drop path, `lagged`, reconnect. Debt: `tasks/api/059-sse-client-remaining-observations.md`.
- **The test ledger has never met a bench** ([decisions](../decisions/ledger.md) 98). Owed: a study run lands a row; `ledger_pending` matches attached roles.
- **The bench lease client has met only a board-less dev Core** ([decisions](../decisions/lease.md) 90, 101). An MCP-taken token reaches no CLI or atlas subprocess until exported there; the 900 s default TTL is assumed.
- **The build verdict has read one real Zephyr build and one real ztest run** ([decisions](../decisions.md) 102, 103): a sample app and its variant on a Cortex-M3 board, a ztest sample on native_sim. Unmet: real twister output (fixture-tested), a sysbuild log (the last memory table wins), a field variant pair.
- **`build --each` has met one fixture workspace** ([decisions](../decisions.md) 104): a T2 module on Zephyr 4.4. Unmet: a sysbuild build (its `app_version.h` sits elsewhere and stays stale), a commit id computed at CMake configure time (stale too), a module that is not the manifest repo.
