# embarch-api: MCP tools and CLI subcommands

**Status:** active, 2026-09-02.

**One table, because these are two front-ends over one implementation** — not two surfaces to keep in sync. That premise held across a single file until this one crossed its size reserve; **split by section 2026-09-10** (`tasks/api/053`, a verbatim move, nothing restated) into the files linked below. The premise still applies across every one of them — it is a property of the crate's tools, not of any one doc file holding their description.

**Naming differs by convention, and it is a real difference a user hits:** MCP tools are `snake_case`, CLI subcommands are `kebab-case` — `list_projects` over MCP, `embarch-api list-projects` on a terminal. Not a design choice so much as `clap` renaming variants and `rmcp` taking the Rust function name verbatim. The CLI is a **superset**: `versions` has no tool.

`P` below is the project-selection set: `board?`, `variant?`, `revision?`, `app?`, `snippets?`, `extra_args?` (CLI: `--board`, `--variant`, `--revision`, `--app`, repeatable `--snippet`/`--extra-arg`). Selection semantics: [config.md](config.md).

## Sections

- [Config and discovery](tools-discovery.md) — `list_projects`, `list_targets`, `status`, `versions`
- [Build and flash](tools-build-flash.md) — `build`, `flash`, `build_and_flash`, `reset`, `serial_log`, `list_serial_ports`
- [Studies](studies.md) — `run_study`, `study_status`, `study_watch`, `study_stream_data`, `list_study_streams`, the three data aliases
- [Dev bench](tools-dev-bench.md) — `build_dev_bench`, `flash_dev_bench`, `build_and_flash_dev_bench`, `reset_dev_bench`, `dev_bench_hello`, `dev_bench_link`
- [Topology](tools-topology.md) — `enroll_probe`, `validate`, `alerts`, `declare_signal`, `list_signals`, `remove_signal`

## Error handling

**MCP.** An expected or recoverable failure — nonzero build exit, Core returning 4xx/5xx, a missing artifact — comes back as tool **error content**, never a protocol error, so the agent sees the real failure text. A protocol error is reserved for this crate's config being unloadable at all. **One documented exception:** an unknown project name is `invalid_params`, which exists precisely for "the request is malformed", as distinct from "well-formed but the operation failed".

**CLI.** No protocol layer, so: success → exit `0` and the result on stdout; **any** failure → exit `1` and one line on stderr (under `--json`, stdout — below). Malformed invocation is `clap`'s own exit `2`. **The exit code stays a single `1` for every failure kind, and there is no `error_kind` to branch on instead** — retired, never built (decision 50). A script branches on `success` and reads `error`, prose; the prerequisite is in [open.md](../open.md).

**`--json`** switches stdout to a single object carrying the same fields the MCP result does, so a script does not scrape human text. On failure the error goes into **that same object on stdout** — `{"success": false, "error": "…"}` — so a script checks the exit code, not which stream carried it. That holds for a failure *before* the subcommand ran too: unreadable config, unresolvable token.

**Every JSON object this crate emits carries `schema_version: u32`, currently `1`** — the CLI's object, **each NDJSON line** of `study-status --follow` (not only its `summary`), and every JSON MCP result. Bumped by hand on a rename, removal or retype; adding a field is not. The counter starts where the guarantee starts and says nothing about any earlier shape ([decisions](../decisions/surface.md) 24). **Not `versions`' `host_type_schema_version`**, which counts study-designer's host types, not this crate's JSON shape.

**There is deliberately no `doctor` tool here.** Adding one would mean reimplementing `embarch-umbrella`'s whole diagnostic chain or depending on its binary, both breaking the one-way relationship that keeps this crate unaware umbrella exists. An agent hitting a misconfiguration these tools' own errors cannot explain should shell out to `embarch doctor --json`. `versions` is no exception: it reports a constant, it diagnoses nothing.
