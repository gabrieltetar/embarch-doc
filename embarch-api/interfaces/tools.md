# embarch-api: MCP tools and CLI subcommands

**Status:** active, 2026-09-02.

**One table, because these are two front-ends over one implementation** — not two surfaces to keep in sync. Studies: [studies.md](studies.md). Config: [config.md](config.md). Current truth: [../spec.md](../spec.md).

**Naming differs by convention, and it is a real difference a user hits:** MCP tools are `snake_case`, CLI subcommands are `kebab-case` — `list_projects` over MCP, `embarch-api list-projects` on a terminal. Not a design choice so much as `clap` renaming variants and `rmcp` taking the Rust function name verbatim. The CLI is a **superset**: `versions` has no tool.

`P` below is the project-selection set: `board?`, `variant?`, `revision?`, `app?`, `snippets?`, `extra_args?` (CLI: `--board`, `--variant`, `--revision`, `--app`, repeatable `--snippet`/`--extra-arg`). Selection semantics: [config.md](config.md).

## Config and discovery

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `list_projects` | — | Configured projects: name, chip, flash_format, source_path, whether serial defaults are set. `chip` is omitted for a `zephyr-west` project, resolved per call rather than stored. Pure config read — **works with Core down**, which matters when debugging config alone |
| `list_targets` | `project` | For `zephyr-west`: every file-backing-validated tuple plus `snippets_by_app`, `default_snippets`, `default_extra_args`. For `static`: exactly one row — **the project itself**, with its configured `build_command`, `chip` and resolved `artifact_path` — because a static project has one target and refuses every selection param ([decisions](../decisions/shape.md) 53) |
| `status` | — | Core `GET /status`; the probe list, or a clear "Core unreachable at `<base_url>`" |
| `versions` **(CLI only)** | — | The versions compiled into **this binary**: `api_version` and `host_type_schema_version`, the study-designer host type schema it submits studies under and what `embarch doctor` compares against Core's served copy. Loads no config, contacts no Core, so it answers where either is what is broken ([decisions](../decisions/tool-wrapping.md) 52) |

## Build and flash

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `build` | `project`, `P` | Runs the configured or call-time-assembled build command. Selection is validated against the live scan **before** assembly. Returns success, exit code, truncated stdout/stderr, artifact path, and whether a fresh artifact was found |
| `flash` | `project`, `P`, `firmware_path?`, `erase?` | Core `POST /flash` with the resolved chip, format and offset. `firmware_path` flashes an already-built or one-off file — bypassing *build*-target resolution, but a `zephyr-west` project still needs enough selection to resolve the **chip**, none being stored |
| `build_and_flash` | `project`, `P`, `erase?` | Runs `build`, flashing only if it succeeded **and** the freshness check passed. Returns both sub-results |
| `reset` | `project`, `P` | Core `POST /reset` with the resolved chip. Same selection as `flash`, same reason |
| `serial_log` | `project`, `port?`, `baud?`, `duration_ms?` | Core `GET /serial-log`. Falls back to the project's port and baud, then 115200 / 2000 ms. `port` falls back further to Core's `GET /dev-bench/port` before erroring — **and this link is meant for the bench, not a DUT's own console** |

**`erase` defaults to `false` and is never implicitly `true`.** The MCP description and the CLI help both spell out what it does to a board, at a length no other argument here gets — that wording is itself the design point, and [decisions](../decisions/tool-wrapping.md) 41 is where it is argued and where a change to it belongs. Core performs the erase and decides whether a target supports one; a refusal comes back verbatim.

**Why `build` and `flash` stay separate as well as bundled:** the common agent workflow wants one call, and bundling prevents flashing a stale artifact after a build error — but iterating on compiler errors should not touch hardware every call, and a re-flash after a board reset should not need a rebuild.

## Studies

`run_study`, `study_status`, `study_watch`, `study_stream_data`, `list_study_streams` and the three data aliases, plus what `--follow` promises: [studies.md](studies.md).

## Dev bench

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `build_dev_bench` | — | `west build -b <board> app` in `[dev_bench] source_path`. No project or selection params: the bench is one board at a time, and *which* board is config, not a call-time choice |
| `flash_dev_bench` | `firmware_path?`, `erase?` | Core `POST /flash` with `[dev_bench]`'s chip, format, offset and probe serial |
| `build_and_flash_dev_bench` | — | Both, flashing only on a successful, fresh build |
| `reset_dev_bench` | — | Core `POST /reset` with `[dev_bench]`'s chip. Needed after `flash_dev_bench`/`build_and_flash_dev_bench`, since flashing halts the core rather than starting it running |
| `dev_bench_hello` | — | Core `GET /dev-bench/hello` — runs the Hello/HelloAck handshake alone, no `Study`, and closes the link again. Returns `schema_version`, `compatible`, `firmware_version`, and the identity cross-check: `self_reported_hardware_id` (what the bench itself claims), `probe_hardware_id` (JTAG-read by the enrolled probe), and `link_identity` — their comparison as `match`/`mismatch`/`not-reported`/`undeclared`. All three identity fields are `Option<String>` on the client (`embarch-api` decision 58): against an older Core (predating `embarch-core` decision 47's rename of `hardware_id`→`self_reported_hardware_id`) one or more comes back `None`, and the tool renders that as an **unavailable** cross-check, leading with which field(s) this Core did not send, rather than a partial or misleading pass. Against a Core that sends all three, the response reads **complete** and each field is rendered verbatim under its own label. **Read `link_identity` itself; `not-reported`/`undeclared` is not a pass**, it means the comparison could not be made, not that identity was confirmed — `compatible` says nothing about it either way, and neither state above is reachable from the other ([decisions](../decisions/tool-wrapping.md) 59). `409` (a study already has the link; not a fault, retry after) and `502` (the handshake itself failed) come back as distinct error text. Has a CLI twin (`dev-bench-hello`) as of [decisions](../decisions/shape.md) 61 — restores CLI ⊇ MCP; `versions` stays the only reverse case. **`dev-bench-hello --json`'s success object carries this handshake `schema_version` under the key `dev_bench_schema_version`, not `schema_version`** — that literal key belongs to the envelope stamp every `--json` object carries (decision 24/50), and `tasks/api/049` is the collision that shipped when the field was first named the same as the stamp (mirrors decision 52's `host_type_schema_version` precedent for the same collision) |

## Topology

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `enroll_probe` | `role`, `chip`, `probe_serial?` | Core `POST /probes/enroll`. No selection params — enrollment is not build-target selection. The guided flow is conversational: ensure only the intended board's probe is attached, *then* call. **Core's refusal on anything but exactly one attached probe enforces that**, nothing client-side |
| `validate` | `role` | Core `POST /validate` — the live identity re-check flash and reset run mid-attach, callable without touching hardware otherwise. On a match, returns two distinct timestamps: `confirmed_at_utc_ms` (enrolment time, unmoved by a re-check) and `validated_at_utc_ms` (this call's own check, `embarch-topology` decision 26 / `embarch-core` decision 50) — read the latter for freshness when present; `null`/`None` against a Core older than `tasks/core/026` means it never reported one, not that the check happened at an unknown time (decision 58). A mismatch names recorded vs. live hardware ID **and a `fix_it_url` as plain text, never auto-opened** |
| `alerts` | `limit?` | Core `GET /alerts`, most recent topology-mismatch alerts, default 20 |

## Error handling

**MCP.** An expected or recoverable failure — nonzero build exit, Core returning 4xx/5xx, a missing artifact — comes back as tool **error content**, never a protocol error, so the agent sees the real failure text. A protocol error is reserved for this crate's config being unloadable at all. **One documented exception:** an unknown project name is `invalid_params`, which exists precisely for "the request is malformed", as distinct from "well-formed but the operation failed".

**CLI.** No protocol layer, so: success → exit `0` and the result on stdout; **any** failure → exit `1` and one line on stderr (under `--json`, stdout — below). Malformed invocation is `clap`'s own exit `2`. **The exit code stays a single `1` for every failure kind, and there is no `error_kind` to branch on instead** — retired, never built (decision 50). A script branches on `success` and reads `error`, prose; the prerequisite is in [open.md](../open.md).

**`--json`** switches stdout to a single object carrying the same fields the MCP result does, so a script does not scrape human text. On failure the error goes into **that same object on stdout** — `{"success": false, "error": "…"}` — so a script checks the exit code, not which stream carried it. That holds for a failure *before* the subcommand ran too: unreadable config, unresolvable token.

**Every JSON object this crate emits carries `schema_version: u32`, currently `1`** — the CLI's object, **each NDJSON line** of `study-status --follow` (not only its `summary`), and every JSON MCP result. Bumped by hand on a rename, removal or retype; adding a field is not. The counter starts where the guarantee starts and says nothing about any earlier shape ([decisions](../decisions/surface.md) 24). **Not `versions`' `host_type_schema_version`**, which counts study-designer's host types, not this crate's JSON shape.

**There is deliberately no `doctor` tool here.** Adding one would mean reimplementing `embarch-umbrella`'s whole diagnostic chain or depending on its binary, both breaking the one-way relationship that keeps this crate unaware umbrella exists. An agent hitting a misconfiguration these tools' own errors cannot explain should shell out to `embarch doctor --json`. `versions` is no exception: it reports a constant, it diagnoses nothing.
