# embarch-api: configuration schema

**Status:** active, 2026-09-02.

Current truth: [../spec.md](../spec.md). Why the shape is this: [../decisions.md](../decisions.md). See `config.example.toml` in the repo for a runnable version with real values.

## Where the config comes from

In order: **`--config <path>`**, then **`EMBARCH_API_CONFIG`**, then **a cwd-upward search for `embarch/embarch.toml`**. An explicit path or env var always wins outright.

The upward search exists because an engineer working across several firmware repos has no single env-var value that is ever correct, and a separate MCP registration per repo is not "no `--config` needed", it is "typed once instead of every call". Walking up for a conventional filename is the pattern `git` and `west` use for their own roots.

**Conventional location: `<firmware-repo>/embarch/embarch.toml`**, one complete config per repo, scaffolded by `embarch init`. Two consequences: a repo-scoped config means `list_projects` can only offer that repo's projects, and `[core]` is duplicated into every such file — accepted for v1, since it is three lines once `base_url = "auto"` is used.

**Resolution happens once, at process start**, binding an MCP session to whichever repo spawned it. Switching repos mid-session means reconnecting the client.

## `[core]` — one instance

| Field | Type | Req | Default | Notes |
|---|---|---|---|---|
| `base_url` | URL, or the literal `"auto"` | yes | — | `"auto"` defers resolution to first use ([../spec.md](../spec.md) §4) instead of naming an address |
| `host` | string | no | — | Only consulted by `"auto"`, as its **last** candidate: a Core on a genuinely separate machine |
| `port` | integer | no | 4884 | Only consulted by `"auto"` when building candidates |
| `token` | string | no | — | Inline bearer token |
| `token_env` | string | no | — | Env var to read the token from instead. **Wins if both are set.** If neither resolves, machine-wide token-file discovery runs before failing |
| `status_timeout_secs` | integer | no | 10 | |
| `reset_timeout_secs` | integer | no | 10 | |
| `flash_timeout_secs` | integer | no | 120 | Its own budget, because flashing legitimately takes much longer than a status check |
| `serial_timeout_secs` | integer | no | 15 | |

## `[[projects]]` — zero or more

| Field | Type | Req | Default | Notes |
|---|---|---|---|---|
| `name` | string | yes | — | Unique; a duplicate fails config load |
| `source_path` | path | yes | — | Must exist at config-load time |
| `discovery` | `"static"` \| `"zephyr-west"` | no | `"static"` | `"zephyr-west"` replaces the stored `chip`/`artifact_path`/`build_command` with a live per-call scan |
| `build_cwd` | path | no | none | Joined onto `source_path` to form the build directory — **and** the directory `artifact_path` resolves from. See [../spec.md](../spec.md) §3 for why this is usually wrong to set |
| `build_command` | array of strings | yes (static) | — | argv, no shell interposed |
| `artifact_path` | path | yes (static) | — | Relative to the build directory, not to `source_path` alone |
| `chip` | string | yes (static) | — | Opaque probe-rs target name |
| `flash_format` | string | yes (static) | — | Opaque; Core parses it |
| `base_address` | integer | no | none | Flash offset. **Required in practice for `flash_format = "bin"`**, which carries no offset of its own; ignored by Core for a self-locating format. Advice, not a check — enforcing it is one step from validating the offset itself, which this crate declines to do |
| `build_timeout_secs` | integer | no | 300 | |
| `env` | table string→string | no | empty | **Additive** over the inherited environment, not a replacement. PATH and toolchain setup stay with whatever launches this process |
| `serial_port` / `serial_baud` | string / integer | no | none | Fallbacks for `serial_log`'s params; baud then defaults to 115200 |
| `probe_serial` | string | no | none | Passed through on flash/reset — disambiguates the DUT probe when a second is attached. Omitted, Core falls back to first-probe-found |
| `default_target` | table (`board?`, `variant?`, `revision?`, `app?`) | no | none | `zephyr-west` only. Applied as the **base** selection before a call's own params narrow further, pinning the common single-target case so it does not start erroring the moment a second real target lands in the repo |
| `version_command` | array of strings | no | `git describe --always --dirty --abbrev=8` | Only consulted by a DUT reflash. argv, run in `source_path`, trimmed stdout becomes the version this run reports flashing. **It describes the tree that was built, not the image running on the board.** A `git` argv naming a tree-mutating subcommand is **refused, wherever in the argv it appears** |
| `soc_chip_overrides` | array of `{ soc, chip }` | no | empty | `zephyr-west` only. Consulted **before** calling Core's `/resolve-chip`; a hit short-circuits the HTTP call entirely. The escape hatch for a SoC Core has no mapping for |
| `[[projects.targets]]` | rows of `{ name, build_command, chip, artifact_path }` | no | — | `static` only. A hand-declared menu, returned verbatim by `list_targets`; without any, that tool errors with the exact TOML shape needed rather than a bare "not applicable" |

**For a `zephyr-west` project nothing is stored that the repo can answer.** Board, SoC, cpucluster, variant, revision and app enumeration is a pure filesystem and YAML read, re-run every call and **never cached** — caching would reintroduce the staleness this exists to eliminate. A tuple is real only if a `.dts` exists for that combination, the revision is `board.yml`'s declared default or has a revision-suffixed overlay, and a board using a custom revision format does not itself reject it.

**Selection is never guessed, but it is narrowed:** whatever subset of `board`/`variant`/`revision`/`app` is given filters the live-scanned set; exactly one match proceeds, more than one errors listing the remainder, none given lists everything. `reset` needs the same four as `flash`, because it sends a chip too and a `zephyr-west` project has none stored.

**`snippets`** is additive rather than narrowing — a snippet choice does not change which target tuple exists. Omitting it falls back to `default_snippets`, *not* to "no snippets"; the reserved literal `["none"]` forces zero snippets over a configured default, and any other list containing `"none"` is a call-time error naming the ambiguity. **`extra_args`** is opaque passthrough, unvalidated, inserted right after the `build` subcommand.

**Build directory:** `build_dir_root/<board>-<variant-or-default>-<revision>-<app>-<snippets-or-none>-<extra-args-hash>/`, one per distinct target. Only `extra_args` is hashed, because an arbitrary flag can contain directory-unsafe characters; every other axis is spelled out so a directory listing is readable, and each build directory gets a `target.json` recording the full resolved selection so a human can recover what produced it without reverse-engineering a hash.

## `[dev_bench]` — zero or one

The `embarch-dev-bench` build target *this machine's bench* is wired to. Deliberately **not** a `[[projects]]` entry: dev-bench is not a DUT anyone configures per repo, it is EmbArch's own rig, one board at a time, addressed by no project name. **Every field is required and none is defaulted** — a default would have to pick one of two real boards, and picking wrong means building the wrong image and handing it to Core to flash through the wrong debug interface at the wrong chip.

| Field | Type | Req | Notes |
|---|---|---|---|
| `source_path` | path | yes | The `workspaces/*` this bench builds from, matching `board`. Must exist at config-load time |
| `west_binary` | path | yes | Often not on bare `PATH` (a workspace venv) |
| `board` | string | yes | The west board target. Must be one `app/boards/` carries a `.conf` fragment for — the shared app builds for any board, but only one with that fragment gets the BLE and logging Kconfig this firmware needs |
| `chip` | string | yes | The probe-rs target Core attaches as. **Not derivable from `board`** by anything this crate should be inventing |
| `flash_format` | string | yes | `hex` or `bin`; anything else is rejected at load |
| `artifact_path` | path | yes | Relative to `source_path`. Declared rather than derived because it varies by more than the format: **NCS defaults sysbuild on and vanilla Zephyr does not**, which puts the image a directory deeper |
| `base_address` | integer (TOML hex literal) | conditional | **Required when `flash_format = "bin"` and rejected when `hex`.** A raw binary carries no load address, so an absent offset is nobody having said where the image goes; a hex carries its own, so an offset beside one would be ignored rather than honoured. Both are config-load errors |
| `build_timeout_secs` | integer | no | 300 |
| `env` | table string→string | no | **Replaces** the inherited environment rather than extending it. `cargo` must be on `PATH` for every board (the build cross-compiles the shared crate to a staticlib from CMake), and the ESP32-C5 additionally needs `esptool` on bare `PATH`. The Arm and RISC-V compilers do **not** — Zephyr finds its SDK through the CMake package registry |
| `probe_serial` | string | no | Disambiguates the bench's probe from a DUT's when both are attached. **More load-bearing since 2026-08-31, not less:** with an nRF54L15DK bench beside an nRF54L15 DUT, both probes are SEGGER, where the ESP32-C5's JTAG was Espressif's |

Absent `[dev_bench]` is a clear "not configured" error from the three dev-bench tools, never a silent no-op or a guessed path.
