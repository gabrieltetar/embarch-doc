# embarch-api: configuration schema

**Status:** active, 2026-09-05.

Current truth: [../spec.md](../spec.md). Why the shape is this: [../decisions.md](../decisions.md). See `config.example.toml` in the repo for a runnable version with real values.

## Where the config comes from

In order: **`--config <path>`**, then **`EMBARCH_API_CONFIG`**, then **a cwd-upward search for `embarch/embarch.toml`** ([../decisions](../decisions/shape.md) 25). An explicit path or env var always wins outright.


**Conventional location: `<firmware-repo>/embarch/embarch.toml`**, one complete config per repo, scaffolded by `embarch init`. Two consequences: a repo-scoped config means `list_projects` can only offer that repo's projects, and `[core]` is duplicated into every such file — accepted for v1, being three lines once `base_url = "auto"` is used.

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
| `flash_timeout_secs` | integer | no | 120 | Its own budget: flashing takes far longer than a status check |
| `serial_timeout_secs` | integer | no | 15 | |

## `[[projects]]` — zero or more

| Field | Type | Req | Default | Notes |
|---|---|---|---|---|
| `name` | string | yes | — | Unique; a duplicate fails config load |
| `source_path` | path | yes | — | Must exist at config-load time |
| `discovery` | `"static"` \| `"zephyr-west"` | no | `"static"` | `"zephyr-west"` replaces the stored `chip`/`artifact_path`/`build_command` with a live per-call scan |
| `build_cwd` | path | no | none | Joined onto `source_path` to form the build directory — **and** the directory `artifact_path` resolves from. Usually wrong to set — [../decisions](../decisions/build.md) 5 |
| `build_command` | array of strings | yes (static) | — | argv, no shell interposed |
| `artifact_path` | path | yes (static) | — | Relative to the build directory, not to `source_path` alone |
| `chip` | string | yes (static) | — | Opaque probe-rs target name |
| `flash_format` | string | yes (static) | — | Opaque; Core parses it |
| `base_address` | integer | no | none | Flash offset. **Required in practice for `flash_format = "bin"`**, which carries no offset of its own; ignored by Core for a self-locating format. Advice, not a check ([../decisions](../decisions/build.md) 42) |
| `build_timeout_secs` | integer | no | 300 | |
| `env` | table string→string | no | empty | **Additive** over the inherited environment, not a replacement. PATH and toolchain setup stay with whatever launches this process |
| `serial_port` / `serial_baud` | string / integer | no | none | Fallbacks for `serial_log`'s params; baud then defaults to 115200 |
| `probe_serial` | string | no | none | Passed through on flash/reset — disambiguates the DUT probe when a second is attached. Omitted, Core falls back to first-probe-found |
| `[projects.default_target]` | table (`board?`, `variant?`, `revision?`, `app?`) | no | none | `zephyr-west` only; **refused at config load** on a `static` project (below) and when the table is empty. The **base** selection a call's own params narrow further, **per field**: naming `board` overrides this one's `board` and nothing else. Pins the common single-target case against a second target landing in the repo. `list_targets` reports it |
| `version_command` | array of strings | no | `git describe --always --dirty --abbrev=8` | Only consulted by a DUT reflash. argv, run in `source_path`, trimmed stdout becomes the version this run reports flashing. **It describes the tree that was built, not the image running on the board.** A `git` argv naming a tree-mutating subcommand is **refused, wherever in the argv it appears** |
| `soc_chip_overrides` | — | — | — | **Stated here, never built** ([../decisions](../decisions/zephyr.md) 13, `tasks/api/017`). Designed as the escape hatch for a SoC Core cannot map: `zephyr-west` only, consulted before `/resolve-chip` so a hit skips the call. Nothing deserializes the key, so declaring it does nothing on **either** kind |
| `[[projects.targets]]` | — | — | — | **Retired 2026-09-05** ([../decisions](../decisions/shape.md) 53). A menu nothing ever selected from; a config still declaring one **fails at load naming the retirement**, advice per `discovery`: `static` declares one `[[projects]]` entry per target, `zephyr-west` deletes the rows — it resolves targets live per call |

**For a `zephyr-west` project nothing is stored that the repo can answer.** Board, SoC, cpucluster, variant, revision and app enumeration is a pure filesystem and YAML read, re-run every call and **never cached** ([../decisions](../decisions/zephyr.md) 12). A tuple is real only if a `.dts` exists for that combination, the revision is `board.yml`'s declared default or has a revision-suffixed overlay, and a board using a custom revision format does not itself reject it.

**A `static` project refuses a selection outright** ([../decisions](../decisions/zephyr.md) 51): `board`, `variant`, `revision`, `app`, `snippets` or `extra_args` given on a call to it fail naming which were given, rather than being accepted and dropped — its `build_command` is a hand-authored argv this crate cannot splice into. **It has exactly one target — itself** ([../decisions](../decisions/shape.md) 53), which is what `list_targets` reports for it. Everything below is `zephyr-west`.

**And the configured form of the same thing, at load** ([../decisions](../decisions/zephyr.md) 20): `west_binary`, `build_dir_root`, `default_snippets`, `default_extra_args` and `[projects.default_target]` on a `static` project fail config load in **one message naming every one set**, offering two remedies — drop them, or switch to `zephyr-west` and drop `build_command`/`chip`/`artifact_path`. The mirror of the `zephyr-west` arm. **Breaking**: a `static` project carrying any of the four newly covered loaded before and does not now.

**Selection is never guessed, but it is narrowed:** whatever subset of `board`/`variant`/`revision`/`app` is given — after `default_target` has filled in, per field, whatever the call left out — filters the live-scanned set; exactly one match proceeds, more than one errors listing the remainder, none given lists everything. **A selection error names which axes came from `default_target`**, so a value in the message is attributable to the call or to config. `reset` needs the same four as `flash`, because it sends a chip too and a `zephyr-west` project has none stored.

**`snippets`** is additive rather than narrowing — a snippet choice does not change which target tuple exists. Omitting it falls back to `default_snippets`, *not* to "no snippets"; the reserved literal `["none"]` — alone, `--snippet none` on the CLI — forces zero snippets over a configured default. Three things about that literal are checks rather than conventions ([../decisions](../decisions/zephyr.md) 21): a list mixing `"none"` with real snippet names is a call-time error naming the ambiguity; `["none"]` against an app that really declares a snippet called `none` is a call-time error naming the collision, since a snippet name is just a directory name and nothing reserves that one — **and its remedy is conditional and stated as such**: with no `default_snippets` configured it offers renaming or omitting `snippets`, with one configured it names renaming as the only remedy, since omitting would build that default rather than nothing; and `"none"` inside `default_snippets` is a **config-load** error, because as a default it says what omitting the field already says. **`extra_args`** is opaque passthrough, unvalidated, inserted right after the `build` subcommand.

**Build directory:** `build_dir_root/<board>-<variant-or-default>-<revision-or-none>-<app>[-<snippets>][-args<hash>]/`, one per distinct target — the last two segments are **absent**, not spelled `none`, when there are no snippets and no extra args, so a project that uses neither keeps the shorter name it always had. Only `extra_args` is hashed, because an arbitrary flag can contain directory-unsafe characters; every other axis is spelled out so a directory listing is readable. **`<build_dir>/target.json`** records the resolved selection — the same object a build response echoes as its descriptor, `schema_version` and all — because the name is not parseable back into a target: every segment may contain `-`. It is written after the build command, into a directory that already exists and never creating one, so **an absent one means "unattributable", never "orphaned"** ([../decisions](../decisions/build.md) 19).

## `[dev_bench]` — zero or one

The `embarch-dev-bench` build target *this machine's bench* is wired to — EmbArch's own rig, one board at a time, deliberately **not** a `[[projects]]` entry ([decisions](../decisions/dev-bench.md) 32 and 45). **None of the five board-identifying fields is defaulted**: a missing one is a startup error naming it.

| Field | Type | Req | Notes |
|---|---|---|---|
| `source_path` | path | yes | The `workspaces/*` this bench builds from, matching `board`. Must exist at config-load time |
| `west_binary` | path | yes | Often not on bare `PATH` (a workspace venv) |
| `board` | string | yes | The west board target. Must be one `app/boards/` carries a `.conf` fragment for — the shared app builds for any board, but only one with that fragment gets the BLE and logging Kconfig this firmware needs |
| `chip` | string | yes | The probe-rs target Core attaches as. **Not derivable from `board`** by anything this crate should be inventing |
| `flash_format` | string | yes | `hex` or `bin`; anything else is rejected at load |
| `artifact_path` | path | yes | Relative to `source_path`. Declared rather than derived: it varies with which SDK the workspace pulls as well as with the format, and no rule over the other fields predicts it ([decisions](../decisions/dev-bench.md) 45) |
| `base_address` | integer (TOML hex literal) | conditional | **Required when `flash_format = "bin"` and rejected when `hex`** — a raw binary carries no load address, a hex carries its own, so an offset beside one would be ignored rather than honoured. Both are config-load errors |
| `build_timeout_secs` | integer | no | 300 |
| `env` | table string→string | no | **Replaces** the inherited environment rather than extending it. `cargo` must be on `PATH` for every board (CMake cross-compiles the shared crate to a staticlib); the ESP32-C5 also needs `esptool` on bare `PATH`. The Arm and RISC-V compilers do **not** — Zephyr finds its SDK through the CMake package registry |
| `probe_serial` | string | no | Disambiguates the bench's probe from a DUT's when both are attached — **more load-bearing with an nRF54L15DK bench**, where both probes are SEGGER, than with the ESP32-C5 whose JTAG was Espressif's |

Absent `[dev_bench]` is a clear "not configured" error from the three dev-bench tools, never a silent no-op or a guessed path.
