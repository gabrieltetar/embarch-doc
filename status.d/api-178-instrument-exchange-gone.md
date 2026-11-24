**Target:** suite/agent-guide.md §1.1 — the tool count and the "ask" list
**Was:** "all 54 tools as of 2026-10-29"; the ask list names `instrument_exchange`, and the prose says "`instrument_exchange` is refused by Core outside a run"
**Now:** 53 tools; `instrument_exchange` is gone from the ask list (embarch-api removed the tool and its subcommand, EMB-257); the prose says a lab supply or load is driven only by a host study's `Instrument` step, run with `run_host_study`, which stays in ask.
