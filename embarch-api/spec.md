# embarch-api: spec

**Status:** active, 2026-09-02.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Config schema: [interfaces/config.md](interfaces/config.md). Tools and subcommands: [interfaces/tools.md](interfaces/tools.md).

## 1. What it is

Three responsibilities on top of `embarch-core`: **(a)** exposing Core's capabilities as MCP tools for any MCP client, **(b)** exposing the identical capabilities as CLI subcommands for a human with no MCP client in front of them, and **(c)** running a configured build command and feeding the artifact to Core's `/flash`.

**Subcommand presence is the mode switch.** No subcommand → an MCP stdio server. A subcommand present → run that one operation and exit. Both front-ends call the same modules underneath; neither is privileged.

Core owns all direct hardware access — `probe-rs` and `serialport` live exclusively there, and this crate links neither. Core has no idea this crate, MCP, or Claude Code exist, and that one-way relationship is load-bearing well beyond any single feature. `embarch-umbrella` sits on the other side of the same boundary: it writes this crate's config and shells out to its CLI, and this crate has no knowledge it exists.

## 2. Invariants

- **Single user, single Core instance.** No multi-tenancy, no permission model, no database. Each engineer runs their own complete stack.
- **Core's address is never hardcoded to loopback.** It is always a config value, because Core is expected to move to a LAN-reachable machine.
- **`build_command` is an argv array, never a shell string** — no quoting or shell-dialect ambiguity. A project needing shell features declares them explicitly: `["bash", "-lc", "…"]`.
- **`chip`, `flash_format` and `base_address` are opaque pass-through.** This crate does not validate them against probe-rs's target database; that belongs to Core, and duplicating it here would be a maintenance trap.
- **A fresh artifact is proven, never assumed.** The artifact path's existence and mtime are recorded *before* spawning; after a zero exit the file must exist and, if it existed before, be newer than the build start. Without this a build that failed partway could silently "succeed" against a stale binary — the worst possible failure for hardware bring-up.
- **An expected failure comes back as tool content, not a protocol error**, so a calling agent sees the actual compiler error and can reason about it. A protocol error is reserved for this crate's own config being unloadable at all. The one exception: an unknown project name is `invalid_params`, because a bad name makes the *request* malformed rather than the operation failed.
- **This crate never runs `git checkout`.** "Reflash" means build and flash the tree **as it stands**, then verify; it never means "make my tree be that version". Enforced against the config file too, not just this code.
- **No inference presented as fact.** Anything about a DUT that this crate cannot observe is declared by the operator or reported as unknown.

## 3. Build orchestration

- **Working directory** is `source_path` joined with `build_cwd` if set, validated to exist before spawning. `artifact_path` resolves against that same directory, **not against `source_path` alone** — and that distinction is load-bearing: `west`'s default output is `<cwd>/build`, so an invocation that runs from the repo root and passes the app path as an argument must leave `build_cwd` **unset**, even though the app lives in a subdirectory. Setting it makes the resolved artifact path point at a `build/` directory nothing writes to.
- **Capture** uses two concurrent tasks draining stdout and stderr — draining one while the other fills its OS buffer is a classic way to hang a child.
- **Truncation keeps head *and* tail** (~32 KB each side of a ~64 KB budget, with a marker naming what was dropped), because for a Zephyr build the *first* compiler error is usually the actionable one and a long build can scroll it out of a tail-only cap.
- **Timeout kills the process group**, not just the immediate child — `west`/`cmake`/`make` fork subprocesses a plain kill would orphan. A killed or timed-out build is reported **distinctly** from a nonzero exit, so a hang is not misdiagnosed as a code problem.
- **One build in flight per project name**, via a per-project async lock. Separate from Core's hardware lock: this guards two calls stomping the same output directory, not USB contention.

## 4. Deployment and topology

Today `embarch-api` runs under WSL2 and Core runs native on Windows on the same physical machine, reached over the WSL2⟷Windows network boundary rather than loopback.

**Artifact transfer branches on topology class, and the reason is Session 0.** `Local` — same machine, or a declared explicit `base_url` — sends `firmware_path` as JSON. `WslHost` and `Remote` both **upload the artifact's bytes** as multipart. The WSL2 case needs it because `\\wsl.localhost\…` UNC shares are exposed by a per-session network provider tied to an interactive logon, and Core's installed service runs as `LocalSystem` in **Session 0**, which has no such provider: the identical path resolves fine from an interactive shell and fails with "the network name cannot be found" from the service. Not about which account the service uses — Windows services are always in Session 0. Every earlier "confirmed working" claim for the UNC mechanism had been validated against a *foreground* Core, never the installed service.

`artifact_path_for_core` and its UNC computation are **fully retired**, not merely superseded: multipart works identically whether Core is foreground or a service, and covers a genuinely remote Core by the same path.

**`base_url = "auto"`** resolves per-process on first use — a short-timeout `GET /status` race over an ordered candidate list (loopback, then the WSL2 default-gateway IP, then a configured host), taking the first that answers, where a `401` **counts as an answer**: Core is there and the token is wrong, which is a distinct problem needing a distinct message. Cached for the process lifetime, never written back to config, so a WSL2 restart's new gateway IP is picked up by the next invocation. **Resolution must be lazy**: the startup connectivity check is MCP-mode-only and `list_projects` deliberately works with Core down, and resolving at config-load time would regress both.

**The startup connectivity check warns; it does not refuse.** Refusing meant every MCP tool vanished from the agent's view with no way to learn why. Every hardware-facing tool now fails per-call with the same message plus the resolved-candidate list.

## 5. Modules

| Module | Owns |
|---|---|
| `main.rs` | clap CLI, config resolution, logging init, dispatch to MCP server or `cli.rs` |
| `config.rs` | TOML schema, load, validation (unique names, path existence, discovery-branched required fields) |
| `zephyr.rs` | the live `boards/`/`app/` scan, target cross-product, file-backing validation, build-dir and artifact-path assembly. Pure filesystem and YAML reads — no `west` invocation, no network |
| `resolve.rs` | the one place every front-end branches on `discovery`, turning a project plus a selection into a build plan and a chip |
| `build.rs` | subprocess execution for a discovery-agnostic build plan |
| `reflash.rs` | the check → build → flash → submit sequence, and the no-`git checkout` refusal with its test |
| `study.rs` | the shared seal-recomputation helper both front-ends call |
| `tools.rs` / `cli.rs` | the two front-ends; thin glue over the same modules |
| `logging.rs` | the rolling per-user logfile |
| `crates/embarch-core-client/` | `CoreClient` (every Core endpoint, bearer injection, per-call timeouts, the topology-branched flash transport, typed `409`/`404` errors), `CoreConfig`, token discovery, and `version.rs`. A plain path dependency, not a workspace member |

`main` spawns the entire tokio runtime — `block_on` included — **on a dedicated thread with a 512 MiB stack**. `Builder::thread_stack_size` only sizes threads the runtime spawns; the top-level future runs on whatever thread calls `block_on`, which for `#[tokio::main]` is the process main thread at the OS default, with no knob. One fix, two bugs that only looked unrelated ([decisions](decisions/core-link.md) 36).

## 6. Security

**Inbound is "whoever can spawn the process"** — for MCP and for the CLI alike. No API key, bearer token, or session exists at this layer. A deliberate simplification: if this is ever run detached from an interactive client, that needs revisiting.

**Outbound** is `EMBARCH_TOKEN`, resolved from config `token`, then `token_env`, then machine-wide token-file discovery (same-OS path, or the WSL2⟷Windows-translated path). Full lifecycle: [embarch-token.md](../embarch-token.md).

## 7. Constants

| Name | Value | Provenance |
|---|---|---|
| runtime thread stack | 512 MiB | [measured 2026-08-24] 64 MiB was empirically insufficient against a real GATT-heavy `StudyResult` |
| `FRESHNESS_CLOCK_GRACE` | 500 ms | [measured] WSL2 clock jitter put a child's file mtime *before* the parent's pre-spawn timestamp; a real build takes seconds, so this cannot mask a stale artifact |
| capture cap | ~64 KB, head+tail | [assumed] |
| default `build_timeout_secs` | 300 | [assumed] |
| default Core port | 4884 | — |
| log retention | 7 daily files, `api.log.<date>` | deliberately the same scheme as Core's, so one reader covers both |

The logfile is **per-user**, not machine-wide: this crate runs as the engineer, and `/var/lib` is root-owned, so creating a subdirectory there is permission-denied — verified on this bench rather than assumed.
