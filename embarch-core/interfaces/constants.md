# embarch-core: constants and knobs

**Status:** active, 2026-09-09. Split out of [spec.md](../spec.md) §5 the same
day, when that file reached its size cap ([DOC-COMPACTION.md](../../DOC-COMPACTION.md)
§3) — a reference table, not cut, the same way [interfaces.md](../interfaces.md)
splits into `interfaces/<topic>.md`.

| Name | Value | Provenance |
|---|---|---|
| `WATCHDOG_GRACE_MS` | 10,000 | [measured 2026-08-27] 2,000 threw away a completed 300 s capture; the margin covers post-deadline flush backlog, which scales with how much the step captured — not link latency |
| `RESET_PULSE_MS` | 50 | [assumed] |
| dev-bench link baud | 1 Mbaud | [assumed] |
| `EMBARCH_SIGNAL_BAUD` | 1 Mbaud | [assumed] a `SignalLink` records where a signal goes, not how fast it talks |
| `EMBARCH_STREAM_MAX_BYTES` | 32 MiB, 2 segments | [assumed] |
| `/serial-log` duration/byte caps | 10,000 ms / 1 MiB | [assumed] `400` over the ms cap, under the client's 15,000 ms timeout (decision 58) |
| `EMBARCH_STUDY_RESULTS_KEEP` | 50 (`0` disables) | [assumed] |
| `MAX_UNDECODABLE_FRAMES` | 10 | [assumed] separates one lost frame from a noise stream |
| log retention | 7 daily files | [assumed] |
| `EMBARCH_FLASH_BACKEND` | — | forces a backend (`probe-rs`, `jlink`, `nrfutil`); an unrecognised value is refused by name before any tool lookup runs, and forcing probe-rs onto a refused family logs a warning |
| `EMBARCH_JLINK_EXE` / `_NRFUTIL_EXE` | — | vendor-tool overrides, searched after `PATH` and before default install dirs |
| `EMBARCH_TOKEN` | — | explicit env var wins over the machine-wide file |

Paths follow one convention: `%ProgramData%\embarch\` on Windows,
`/var/lib/embarch/` elsewhere — token, `logs/core.log.<date>`,
`logs/dev-bench.log.<date>`, `study_results/`, and `embarch-topology`'s
`enrollment.toml`.
