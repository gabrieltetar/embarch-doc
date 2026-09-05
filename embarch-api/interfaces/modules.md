# embarch-api: modules

**Status:** active, 2026-09-04.

The module map. Split out of [spec.md](../spec.md) §5 on 2026-09-04 under
[DOC-COMPACTION.md](../../DOC-COMPACTION.md) §10 — a reference table is not cold,
it is loaded deliberately. Read it when you need to know *where* something
lives; `spec.md` alone still answers what is true.

Current truth: [spec.md](../spec.md). Why: [decisions.md](../decisions.md).

| Module | Owns |
|---|---|
| `main.rs` | clap CLI, config resolution, logging init, dispatch to the MCP server or `cli.rs` — and `versions`, answered *before* config resolution so a broken config cannot hide it |
| `config.rs` | TOML schema, load, validation — unique names, path existence, discovery-branched required fields |
| `zephyr.rs` | the live `boards/`/`app/` scan, target cross-product, file-backing validation, build-dir and artifact-path assembly. **Pure filesystem and YAML reads — no `west`, no network** |
| `resolve.rs` | the one place every front-end branches on `discovery`, turning a project plus a selection into a build plan and a chip |
| `build.rs` | subprocess execution for a discovery-agnostic build plan. The one module behind this package's `lib` target, since a binary crate exposes nothing to `tests/` ([decisions](../decisions/shape.md) 46) |
| `reflash.rs` | the check → build → flash → submit sequence, and the no-`git checkout` refusal with its test |
| `study.rs` | the shared seal-recomputation helper both front-ends call |
| `tools.rs` / `cli.rs` | the two front-ends; thin glue over the same modules |
| `logging.rs` | the rolling per-user logfile |
| `json_out.rs` | the one place a `serde_json` value becomes text, so the only place `schema_version` is stamped |
| `tests/` | the recorded acceptance criteria, one file per area ([decisions](../decisions/shape.md) 46). **No hardware, no live Core, no added dependency** — a mock Core on loopback is the ceiling. `versions` is pinned to answer with no config at all |
| `crates/embarch-core-client/` | `CoreClient` — every Core endpoint, bearer injection, per-call timeouts, the topology-branched flash transport, typed `409`/`404` — plus token discovery and the study event stream, whose decoder is byte-fed with no I/O of its own. **A path dependency, not a workspace member**, and `embarch-ui` path-depends on it too, so a change here reaches a repo this one does not own |

`main` spawns the entire tokio runtime — `block_on` included — **on a dedicated thread with a 512 MiB stack**, because `Builder::thread_stack_size` does not size the thread calling `block_on`, and no knob does ([decisions](../decisions/core-link.md) 36).
