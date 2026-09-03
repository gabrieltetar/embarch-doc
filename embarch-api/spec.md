# embarch-api: spec

**Status:** active, 2026-09-03.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Config schema: [interfaces/config.md](interfaces/config.md). Tools and subcommands: [interfaces/tools.md](interfaces/tools.md).

## 1. What it is

Three responsibilities on top of `embarch-core`: **(a)** exposing Core's capabilities as MCP tools for any MCP client, **(b)** exposing the identical capabilities as CLI subcommands for a human with no MCP client, and **(c)** running a configured build command and feeding the artifact to Core's `/flash`.

**Subcommand presence is the mode switch.** No subcommand → an MCP stdio server. A subcommand → run that one operation and exit. Both front-ends call the same modules underneath; neither is privileged.

Core owns all direct hardware access — `probe-rs` and `serialport` live exclusively there, and this crate links neither. Core has no idea this crate, MCP or Claude Code exist, and that one-way relationship is load-bearing well beyond any single feature. `embarch-umbrella` sits on the far side of the same boundary: it writes this crate's config and shells out to its CLI, unknown to this crate.

## 2. Invariants

- **Single user, single Core instance.** No multi-tenancy, permission model or database. Each engineer runs their own complete stack.
- **Core's address is never hardcoded to loopback.** Always a config value, because Core is expected to move to a LAN-reachable machine.
- **`build_command` is an argv array, never a shell string** — no quoting or shell-dialect ambiguity. A project needing shell features says so: `["bash", "-lc", "…"]`.
- **`chip`, `flash_format` and `base_address` are opaque pass-through.** This crate does not validate them against probe-rs's target database; that belongs to Core, and duplicating it here would be a maintenance trap.
- **A fresh artifact is proven, never assumed.** The artifact path's existence and mtime are recorded *before* spawning; after a zero exit the file must exist and, if it existed before, be newer than the build start. Without this a build that failed partway could silently "succeed" against a stale binary, the worst possible failure for hardware bring-up.
- **An expected failure comes back as tool content, not a protocol error**, so a calling agent sees the actual compiler error and can reason about it. A protocol error is reserved for this crate's own config being unloadable at all — that and its one exception, with the CLI's shapes, in [tools.md](interfaces/tools.md).
- **This crate never runs `git checkout`.** "Reflash" means build and flash the tree **as it stands**, then verify; never "make my tree be that version". Enforced against the config file too, not just this code.
- **No inference presented as fact.** Anything about a DUT this crate cannot observe is declared by the operator or reported as unknown.
- **Every JSON object either front-end emits carries `schema_version`**, stamped in one place rather than remembered per emitter, and there is no `error_kind` ([decisions](decisions/surface.md) 24, 50).
- **A live event stream is an optimisation, never the source of truth.** Losing it falls back to polling and is reported; it never fails a call. Core's `lagged` frame is a fact to relay, not an error ([decisions](decisions/core-link.md) 48).

## 3. Build orchestration

- **Working directory** is `source_path` joined with `build_cwd` if set, validated to exist before spawning. `artifact_path` resolves against that same directory, **not against `source_path` alone** — and that is load-bearing: `west`'s default output is `<cwd>/build`, so an invocation that runs from the repo root and passes the app path as an argument must leave `build_cwd` **unset**, even though the app is in a subdirectory. Setting it makes the resolved artifact path point at a `build/` directory nothing writes to.
- **Capture** uses two concurrent tasks draining stdout and stderr — draining one while the other fills its OS buffer is a classic way to hang a child.
- **Truncation keeps the tail only** — the last 64 KB behind a marker naming the cap, cut on a UTF-8 character boundary because an offset inside a codepoint panics `String::replace_range`. Head-and-tail was the intent and has never been built: [open.md](open.md) carries the gap.
- **Timeout kills the process group**, not just the immediate child — `west`/`cmake`/`make` fork subprocesses a plain kill would orphan. A killed or timed-out build is reported **distinctly** from a nonzero exit, so a hang is not misdiagnosed as a code problem.
- **One build in flight per project name**, via a per-project async lock. Separate from Core's hardware lock: it guards two calls stomping the same output directory, not USB contention.

## 4. Deployment and topology

Today `embarch-api` runs under WSL2 and Core runs native on Windows on the same physical machine, reached over the WSL2⟷Windows network boundary rather than loopback.

**Artifact transfer branches on topology class, and the reason is Session 0.** `Local` — same machine, or a declared explicit `base_url` — sends `firmware_path` as JSON. `WslHost` and `Remote` both **upload the artifact's bytes** as multipart. WSL2 needs it because `\\wsl.localhost\…` UNC shares come from a per-session network provider tied to an interactive logon, and Core's installed service runs as `LocalSystem` in **Session 0**, which has none: the identical path resolves from an interactive shell and fails with "the network name cannot be found" from the service. Not about which account it runs as — services are always in Session 0. So `artifact_path_for_core` and its UNC computation are **fully retired**, not merely superseded: multipart works identically foreground or service, and covers a remote Core by the same path.

**`base_url = "auto"`** resolves per-process on first use — a short-timeout `GET /status` race over an ordered candidate list (loopback, then the WSL2 default-gateway IP, then a configured host), taking the first that answers, where a `401` **counts as an answer**: Core is there and the token is wrong, a distinct problem needing a distinct message. Cached for the process lifetime, never written back to config, so a WSL2 restart's new gateway IP is picked up next invocation. **Resolution must be lazy**: the startup check is MCP-mode-only and `list_projects` deliberately works with Core down; resolving at config-load time would regress both.

**The startup connectivity check warns; it does not refuse** — every hardware-facing tool fails per-call instead, with that message plus the resolved-candidate list. Why refusing was worse: [decisions](decisions/core-link.md) 14.

## 5. Modules

| Module | Owns |
|---|---|
| `main.rs` | clap CLI, config resolution, logging init, dispatch to MCP server or `cli.rs` |
| `config.rs` | TOML schema, load, validation (unique names, path existence, discovery-branched required fields) |
| `zephyr.rs` | the live `boards/`/`app/` scan, target cross-product, file-backing validation, build-dir and artifact-path assembly. Pure filesystem and YAML reads — no `west` invocation, no network |
| `resolve.rs` | the one place every front-end branches on `discovery`, turning a project plus a selection into a build plan and a chip |
| `build.rs` | subprocess execution for a discovery-agnostic build plan. The one module behind this package's `lib` target, because a binary crate exposes nothing to `tests/` ([decisions](decisions/shape.md) 46) |
| `reflash.rs` | the check → build → flash → submit sequence, and the no-`git checkout` refusal with its test |
| `study.rs` | the shared seal-recomputation helper both front-ends call |
| `tools.rs` / `cli.rs` | the two front-ends; thin glue over the same modules |
| `logging.rs` | the rolling per-user logfile |
| `json_out.rs` | the one place a `serde_json` value becomes text, and so the only place `schema_version` is stamped |
| `tests/` | the six recorded acceptance criteria: `core_client_http.rs` (bearer, timeouts, non-2xx, against a loopback mock Core), `build_capture.rs` (drain, truncation, freshness), `study_events_sse.rs` (SSE framing, `lagged`, fallback), `json_surface.rs` (the `--json` stamp). No hardware, no live Core, no added dependency |
| `crates/embarch-core-client/` | `CoreClient` (every Core endpoint, bearer injection, per-call timeouts, the topology-branched flash transport, typed `409`/`404` errors), `CoreConfig`, token discovery, `version.rs`, and the study event stream (`sse.rs`, a byte-fed decoder with no I/O; `study_events.rs`, the follow loop and its polling fallback). A path dependency, not a workspace member |

`main` spawns the entire tokio runtime — `block_on` included — **on a dedicated thread with a 512 MiB stack**, because `Builder::thread_stack_size` does not size the thread that calls `block_on`, and there is no knob that does ([decisions](decisions/core-link.md) 36).

## 6. Security

**Inbound is "whoever can spawn the process"** — MCP and CLI alike. No API key, bearer token or session exists at this layer. A deliberate simplification; [open.md](open.md) carries what it costs.

**Outbound** is `EMBARCH_TOKEN`, resolved from config `token`, then `token_env`, then machine-wide token-file discovery (same-OS path, or the WSL2⟷Windows-translated path). Full lifecycle: [embarch-token.md](../embarch-token.md).

## 7. Constants

| Name | Value | Provenance |
|---|---|---|
| runtime thread stack | 512 MiB | [measured 2026-08-24] 64 MiB was empirically insufficient against a real GATT-heavy `StudyResult` |
| `FRESHNESS_CLOCK_GRACE` | 500 ms | [measured] WSL2 clock jitter put a child's file mtime *before* the parent's pre-spawn timestamp; a real build takes seconds, so this cannot mask a stale artifact |
| capture cap | 64 KB, tail only | [assumed] |
| default `build_timeout_secs` | 300 | [assumed] |
| default Core port | 4884 | — |
| log retention | 7 daily files, `api.log.<date>` | deliberately the same scheme as Core's, so one reader covers both |

The logfile is **per-user**, not machine-wide — `/var/lib` is root-owned and this runs as the engineer, verified on this bench ([decisions](decisions/core-link.md) 43).
