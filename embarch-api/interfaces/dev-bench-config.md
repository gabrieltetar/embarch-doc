# embarch-api: dev-bench config schema

**Status:** active, 2026-09-13. Split out of [config.md](config.md)'s `[dev_bench]` section (`tasks/api/081`), verbatim — nothing restated.

Current truth: [../spec.md](../spec.md). Why the shape is this: [../decisions.md](../decisions.md).

The rest of the config schema: [config.md](config.md).

## `[dev_bench]` — zero or one

The `embarch-dev-bench` build target *this machine's bench* is wired to — EmbArch's own rig, one board at a time, deliberately **not** a `[[projects]]` entry ([decisions](../decisions/dev-bench.md) 32 and 45). **None of the five board-identifying fields is defaulted**: a missing one is a startup error naming it.

| Field | Type | Req | Notes |
|---|---|---|---|
| `source_path` | path | yes | The `workspaces/*` this bench builds from, matching `board`. Must exist at config-load time |
| `west_binary` | path | yes | Often not on bare `PATH` (a workspace venv) |
| `board` | string | yes | The west board target. Must be one `app/boards/` carries a `.conf` fragment for — the shared app builds for any board, but only one with that fragment gets the BLE and logging Kconfig this firmware needs |
| `chip` | string | yes | The probe-rs target Core attaches as. **Not derivable from `board`** by anything this crate should be inventing |
| `flash_format` | string | yes | `hex` or `bin`; anything else is rejected at load |
| `artifact_path` | path | yes | Relative to `source_path`. Declared rather than derived — no rule over the other fields predicts it ([decisions](../decisions/dev-bench.md) 45) |
| `base_address` | integer (TOML hex literal) | conditional | **Required when `flash_format = "bin"` and rejected when `hex`** — a raw binary carries no load address, a hex carries its own. Both are config-load errors |
| `build_timeout_secs` | integer | no | 300 |
| `env` | table string→string | no | **Additive** over the inherited environment, not a replacement — same as `[[projects]]`'s `env`. `cargo` must be on `PATH` for every board (CMake cross-compiles the shared crate to a staticlib); the ESP32-C5 also needs `esptool` on bare `PATH`. The Arm and RISC-V compilers do **not** — Zephyr finds its SDK through the CMake package registry |
| `probe_serial` | string | no | Disambiguates the bench's probe from a DUT's when both are attached — **more load-bearing with an nRF54L15DK bench**, where both probes are SEGGER |

Absent `[dev_bench]` is a clear "not configured" error from the four dev-bench tools that need it (`build_dev_bench`, `flash_dev_bench`, `build_and_flash_dev_bench`, `reset_dev_bench` — `src/tools.rs:767, 796, 824, 884`), never a silent no-op or a guessed path.
