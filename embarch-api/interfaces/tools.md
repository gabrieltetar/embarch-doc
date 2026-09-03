# embarch-api: MCP tools and CLI subcommands

**Status:** active, 2026-09-02.

**One table, because these are two front-ends over one implementation** — not two surfaces to keep in sync. Config: [config.md](config.md). Current truth: [../spec.md](../spec.md).

**Naming differs by convention, and it is a real difference a user hits:** MCP tools are `snake_case`, CLI subcommands are `kebab-case` — `list_projects` over MCP, `embarch-api list-projects` on a terminal. Not a design choice so much as `clap` renaming variants and `rmcp` taking the Rust function name verbatim. The CLI is a **superset**: `versions` has no tool.

`P` below is the project-selection set: `board?`, `variant?`, `revision?`, `app?`, `snippets?`, `extra_args?` (CLI: `--board`, `--variant`, `--revision`, `--app`, repeatable `--snippet`/`--extra-arg`). Selection semantics: [config.md](config.md).

## Config and discovery

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `list_projects` | — | Configured projects: name, chip, flash_format, source_path, whether serial defaults are set. `chip` is omitted for a `zephyr-west` project, resolved per call rather than stored. Pure config read — **works with Core down**, which matters when debugging config alone |
| `list_targets` | `project` | For `zephyr-west`: every file-backing-validated tuple plus `snippets_by_app`, `default_snippets`, `default_extra_args`. For `static` with declared targets: those rows verbatim. Otherwise errors **with the TOML shape** needed to declare some |
| `status` | — | Core `GET /status`; the probe list, or a clear "Core unreachable at `<base_url>`" |
| `versions` **(CLI only)** | — | The versions compiled into **this binary**: `api_version` and `host_type_schema_version`, the study-designer host type schema it submits studies under and what `embarch doctor` compares against Core's served copy. Loads no config, contacts no Core, so it answers where either is what is broken ([decisions](../decisions/surface.md) 52) |

## Build and flash

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `build` | `project`, `P` | Runs the configured or call-time-assembled build command. Selection is validated against the live scan **before** assembly. Returns success, exit code, truncated stdout/stderr, artifact path, and whether a fresh artifact was found |
| `flash` | `project`, `P`, `firmware_path?`, `erase?` | Core `POST /flash` with the resolved chip, format and offset. `firmware_path` flashes an already-built or one-off file — bypassing *build*-target resolution, but a `zephyr-west` project still needs enough selection to resolve the **chip**, none being stored |
| `build_and_flash` | `project`, `P`, `erase?` | Runs `build`, flashing only if it succeeded **and** the freshness check passed. Returns both sub-results |
| `reset` | `project`, `P` | Core `POST /reset` with the resolved chip. Same selection as `flash`, same reason |
| `serial_log` | `project`, `port?`, `baud?`, `duration_ms?` | Core `GET /serial-log`. Falls back to the project's port and baud, then 115200 / 2000 ms. `port` falls back further to Core's `GET /dev-bench/port` before erroring — **and this link is meant for the bench, not a DUT's own console** |

**`erase` is the only argument here that can leave a board unrecoverable by any other tool in the suite**, and an agent picking it because "a clean flash sounds more thorough" is a realistic failure mode. Both the MCP description and the CLI help say plainly that it is a **destructive full-chip erase**, that a non-erase flash cannot undo it, and that a normal reflash does not need it. `false` by default, never implicitly `true`. Which tool performs it, and whether a target supports one, is Core's; a refusal is surfaced verbatim.

**Why `build` and `flash` stay separate as well as bundled:** the common agent workflow wants one call, and bundling prevents flashing a stale artifact after a build error — but iterating on compiler errors should not touch hardware every call, and a re-flash after a board reset should not need a rebuild.

## Studies

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `run_study` | `study` (MCP) / `--study-file <path>` (CLI), `reflash?`, `allow_version_mismatch?`, `project?`, `P` | Recomputes and overwrites **all three seals**, then Core `POST /study`, returning `{ study_id }` at once alongside what it reflashed. `reflash` is `none` (default) / `dev-bench` / `dut` / `both`, building the tree **as it stands** — never `git checkout`. `project` is required only by `dut`/`both`: a *study* is not project-shaped, rebuilding a DUT's firmware is. `allow_version_mismatch` proceeds past an unsatisfied requirement, the override **recorded**, never silently honoured |
| `study_status` | `study_id` | Core `GET /study/{id}` verbatim. **CLI only:** `--follow` watches the study live instead (below); without it, one snapshot, unchanged |
| `study_watch` (MCP) | `study_id`, `wait_secs?`, `max_events?`, `include_samples?` | Subscribes to Core `GET /study/{id}/events` and returns every step, status change and (optionally) sample batch pushed in the window, in order. Bounded because an MCP call is request/response: `wait_secs` defaults to 60, caps at 600 — `complete: true` means terminal, otherwise call again. `include_samples` defaults to **false**, counting `SampleBatch`/`GattTranscript` per tap instead of listing them; the bulk data's exit is `study_stream_data` |
| `study_stream_data` | `study_id`, `name`, `raw?` | One declared tap's capture, by the name the study gave it. Rendered file where the encoding has one; `raw` serves the bytes. **Nothing here inspects content to decide** — an encoding is declared, never sniffed. A non-UTF-8 capture returns a clear error saying that is *expected* for a raw tap, pointing at `--out`, not a decode failure reading like the capture broke |
| `list_study_streams` | `study_id` | Per declared tap: `name`, `bytes_written`, and **`truncated`** — the reason this exists, since the aliases below structurally cannot report it. Needed no new Core route: `GET /study/{id}` returns the whole result inline. `bytes_written: 0` means a tap was declared and captured nothing, a different fact from one never declared |
| `study_power_data` · `study_waveform_data` · `study_gatt_data` | `study_id` | **Aliases kept for one release**, each serving whichever tap answers that alias. Names, params and returned bytes are pinned; their *descriptions* say what each resolves, that it is an alias, and that truncation lives in `list_study_streams` |

### Watching a study live

`study-status --follow` (CLI) and `study_watch` (MCP) are **an addition to polling, never a replacement** — `study_status` with no flag is byte-for-byte what it was. Both consume the same client ([decisions](../decisions/core-link.md) 48, 49); they differ only in that a CLI user can be handed a stream and an MCP caller cannot.

- **`event: lagged` is a reported fact, not an error.** Core emits it deliberately when a subscriber falls behind, rather than skipping messages silently. The CLI prints a `[lagged]` line inline and repeats the count in its summary; the MCP result carries a `lagged: {events, note}` object. Both say the same: the events are missing **from this live feed only**, the study is unaffected, and `study_status`/`study_steps` hold the complete record. Neither fails the call.
- **A dropped or refused stream falls back to polling** `GET /study/{id}` and says so on its own line (`transport` in the MCP result, `[polling]` on the CLI) with the reason. No reconnect: Core keeps no replay, so reconnecting would resume with a silent hole. The only genuine failure is neither mechanism answering.
- **`events_omitted` (this crate's `max_events` cap) and `lagged` (Core's) are different facts**, reported as two. A caller told only that events are missing cannot tell which happened, and the remedies differ.
- **CLI `--follow --json` is NDJSON**, not one object: one compact record per line, ending with a `{"type": "summary", ...}` line. The only `--json` here shaped that way, and it has to be — a stream cannot be one object. `--follow-timeout <secs>` stops watching early and **exits 1**; a study that *fails* still exits 0, because reporting a failed study is a successful report.

CLI data subcommands take `[--out <path>]`. **`--out` is how a binary capture gets out intact** — a raw tap's bytes are not text, and the no-`--out` path writes them to stdout untouched. `list-study-streams` marks a short capture on its own row, not a column an eye slides past.

## Dev bench

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `build_dev_bench` | — | `west build -b <board> app` in `[dev_bench] source_path`. No project or selection params: the bench is one board at a time, and *which* board is config, not a call-time choice |
| `flash_dev_bench` | `firmware_path?`, `erase?` | Core `POST /flash` with `[dev_bench]`'s chip, format, offset and probe serial |
| `build_and_flash_dev_bench` | — | Both, flashing only on a successful, fresh build |

## Topology

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `enroll_probe` | `role`, `chip`, `probe_serial?` | Core `POST /probes/enroll`. No selection params — enrollment is not build-target selection. The guided flow is conversational: ensure only the intended board's probe is attached, *then* call. **Core's refusal on anything but exactly one attached probe enforces that**, nothing client-side |
| `validate` | `role` | Core `POST /validate` — the live identity re-check flash and reset run mid-attach, callable without touching hardware otherwise. A mismatch names recorded vs. live hardware ID **and a `fix_it_url` as plain text, never auto-opened** |
| `alerts` | `limit?` | Core `GET /alerts`, most recent topology-mismatch alerts, default 20 |

## Error handling

**MCP.** An expected or recoverable failure — nonzero build exit, Core returning 4xx/5xx, a missing artifact — comes back as tool **error content**, never a protocol error, so the agent sees the real failure text. A protocol error is reserved for this crate's config being unloadable at all. **One documented exception:** an unknown project name is `invalid_params`, which exists precisely for "the request is malformed", as distinct from "well-formed but the operation failed".

**CLI.** No protocol layer, so: success → exit `0` and the result on stdout; **any** failure → exit `1` and one line on stderr (under `--json`, stdout — below). Malformed invocation is `clap`'s own exit `2`. **The exit code stays a single `1` for every failure kind, and there is no `error_kind` to branch on instead** — documented from the first commit, never built, retired (decision 50). A script branches on `success` and reads `error`, prose; the prerequisite is in [open.md](../open.md).

**`--json`** switches stdout to a single object carrying the same fields the MCP result does, so a script does not scrape human text. On failure the error goes into **that same object on stdout** — `{"success": false, "error": "…"}` — so a script checks the exit code, not which stream carried it. That now holds for a failure *before* the subcommand ran (unreadable config, unresolvable token), which until 2026-09-03 escaped to stderr as a Rust error.

**Every JSON object this crate emits carries `schema_version: u32`, currently `1`** — the CLI's object, **each NDJSON line** of `study-status --follow` (not only its `summary`), and every JSON MCP result. Bumped by hand on a rename, removal or retype; adding a field is not. `1` is the shape as of 2026-09-03, when it was built after being documented and absent since the first commit. **Not `versions`' `host_type_schema_version`**, which counts study-designer's host types, not this crate's JSON shape.

**There is deliberately no `doctor` tool here.** Adding one would mean reimplementing `embarch-umbrella`'s whole diagnostic chain or depending on its binary, both breaking the one-way relationship that keeps this crate unaware umbrella exists. An agent hitting a misconfiguration these tools' own errors cannot explain should shell out to `embarch doctor --json`. `versions` is no exception: it reports a constant, it diagnoses nothing.
