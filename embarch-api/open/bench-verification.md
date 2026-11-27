# embarch-api: open questions, bench and toolchain verification

**Status:** active, 2026-11-13. Split from [open.md](../open.md) by mission (`tasks/api/150`); bullets verbatim.

Truth: [spec.md](../spec.md). Rationale: [decisions.md](../decisions.md).

## Unverified against real hardware or toolchain

- **`bootload` has never met a real bootloader** ([decisions](../decisions/bootload.md) 80, 81). Mock-tested; the first DUT has no MCUboot yet, so no real `domains.yaml` or upload seen.
- **`bench_exchange` has never met two real consoles** ([decisions](../decisions/bench-exchange.md) 89). Mock-tested; cross-console order unmeasured: Core's receive times when sent (`api/147`), else poll-bounded.
- **`study_watch` has met a real embarch-core; the rest has not.** Leg 021: pushed frames and `polled` fallback seen ([decisions](../decisions/study-events.md) 48, 49). Unexercised: `study-status --follow`, drop path, `lagged`, reconnect. Debt: `tasks/api/059-sse-client-remaining-observations.md`.
- **The test ledger has never met a real Core or a bench** ([decisions](../decisions/test-ledger.md) 142). Owed: a real Test run's `test` entries and a manual verdict read back by `test_pending`; `dut_image.claim` is assumed to be the image hash.
- **`test_propose` and `test_plan` have met only a mock Core** ([decisions](../decisions/test-plans.md) 134). Owed against a real Core: a proposal's hash equals the one `TestDef::hash()` gives and the card shows it; Core serves a held suite manifest at `GET /definitions/<hash>` (else selecting a premade suite copies no bench); the Windows `std::fs` writes.
- **`run_test` and `test_status` have met only a mock Core** ([decisions](../decisions/test-run.md) 135). Owed against a real Core: it reproduces this crate's `run.json`, accepts the base studies a template needs beside the expanded ones, and serves a premade suite's studies by hash.
- **The bench lease client has met only a board-less dev Core** ([decisions](../decisions/lease.md) 90, 101). An MCP-taken token reaches no CLI or atlas subprocess until exported there; the 900 s default TTL is assumed. The idle-release refusal (`tasks/api/179`) has met only a mock Core: wait 30 minutes on a real Core, then `mem_read` and `lease_show`.
- **The build verdict has read one real Zephyr build and one real ztest run** ([decisions](../decisions.md) 102, 103): a sample app and its variant on a Cortex-M3 board, a ztest sample on native_sim. Unmet: real twister output (fixture-tested), a sysbuild log with MCUboot's table before the application's (the first memory table wins, decision 128), a field variant pair.
- **`build --each` has met one fixture workspace** ([decisions](../decisions.md) 104): a T2 module on Zephyr 4.4. Unmet: a sysbuild build (its `app_version.h` sits elsewhere and stays stale), a commit id computed at CMake configure time (stale too), a module that is not the manifest repo.
- **The live log has met only a mock Core** ([interfaces/live-log.md](../interfaces/live-log.md), `tasks/api/180`): the `X-Embarch-Call-*` headers, `last_images` for a real board and a real MCP client's working directory are unproven. Run `mem_read` and `reset` on a bench with a lease held and read `embarch/live/`.
