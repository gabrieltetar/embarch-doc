# embarch-api: config and discovery tools

**Status:** active, 2026-09-02. Split out of [tools.md](tools.md) 2026-09-10 (`tasks/api/053`) — see that file's header for the one-table premise this section still honours.

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `list_projects` | — | Configured projects: name, chip, flash_format, source_path, whether serial defaults are set. `chip` is omitted for a `zephyr-west` project, resolved per call rather than stored. Pure config read — **works with Core down**, which matters when debugging config alone |
| `list_targets` | `project` | For `zephyr-west`: every file-backing-validated tuple plus `snippets_by_app`, `default_snippets`, `default_extra_args`. For `static`: exactly one row — **the project itself**, with its configured `build_command`, `chip` and resolved `artifact_path` — because a static project has one target and refuses every selection param ([decisions](../decisions/shape.md) 53) |
| `status` | — | Core `GET /status`; the probe list, or a clear "Core unreachable at `<base_url>`" |
| `versions` **(CLI only)** | — | The versions compiled into **this binary**: `api_version` and `host_type_schema_version`, the study-designer host type schema it submits studies under and what `embarch doctor` compares against Core's served copy. Loads no config, contacts no Core, so it answers where either is what is broken ([decisions](../decisions/tool-wrapping.md) 52) |
