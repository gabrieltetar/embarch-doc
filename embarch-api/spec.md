# embarch-api: spec

**Status:** active, 2026-09-05.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Config: [interfaces/config.md](interfaces/config.md). Tools and subcommands: [interfaces/tools.md](interfaces/tools.md), [interfaces/studies.md](interfaces/studies.md).

## 1. What it is

Three responsibilities on top of `embarch-core`: **(a)** Core's capabilities as MCP tools, **(b)** the same as CLI subcommands — a **superset**, `versions` having no tool — and **(c)** running a configured build command and feeding the artifact to Core's `/flash`.

**Subcommand presence is the mode switch.** No subcommand → an MCP stdio server. A subcommand → run that one operation and exit. Both front-ends call the same modules; neither is privileged.

Core owns all direct hardware access — `probe-rs` and `serialport` live exclusively there, and this crate links neither. **Core has no idea this crate, MCP or Claude Code exist**, and that one-way relationship is load-bearing well beyond any single feature. `embarch-umbrella` sits on the far side of the same boundary: it writes this crate's config and shells out to its CLI, unknown here.

## 2. Invariants

- **Single user, single Core instance.** No multi-tenancy, permission model or database; each engineer runs their own complete stack.
- **Core's address is never hardcoded to loopback.** Always a config value, Core being expected to move to a LAN-reachable machine.
- **`build_command` is an argv array, never a shell string** — no quoting or shell-dialect ambiguity. A project needing shell features says so: `["bash", "-lc", "…"]`.
- **`chip`, `flash_format` and `base_address` are opaque pass-through.** Not validated against probe-rs's target database; that belongs to Core, and duplicating it here is a maintenance trap.
- **A fresh artifact is proven, never assumed.** The artifact path's existence and mtime are recorded *before* spawning; after a zero exit the file must exist and, if it existed before, be newer than the build start. Without this a build that failed partway could silently "succeed" against a stale binary — the worst failure for hardware bring-up.
- **An expected failure comes back as tool content, not a protocol error**, so a calling agent sees the real compiler error and can reason about it. A protocol error is reserved for this crate's own config being unloadable at all; that one exception and the CLI's exit-code shapes are in [tools.md](interfaces/tools.md).
- **This crate never runs `git checkout`.** "Reflash" means build and flash the tree **as it stands**, then verify — never "make my tree be that version". Enforced against the config file too, not just this code.
- **No inference presented as fact.** Anything about a DUT this crate cannot observe is declared by the operator or reported unknown.
- **Every JSON object either front-end emits carries `schema_version`**, stamped in one place rather than per emitter, and there is no `error_kind` ([decisions](decisions/surface.md) 24, 50).
- **A live event stream is an optimisation, never the source of truth.** Losing it falls back to polling and is reported, never failing a call. Core's `lagged` frame is a fact to relay, not an error ([decisions](decisions/core-link.md) 48).

## 3. Build orchestration

**What a call may name, and what each project kind does with it, is [interfaces/config.md](interfaces/config.md)** — notably that a `static` project **refuses** a selection it cannot honour rather than accepting and dropping it, on a call ([decisions](decisions/zephyr.md) 51) and at config load for all five `zephyr-west`-only fields ([decisions](decisions/zephyr.md) 20), that a `zephyr-west` project's `default_target` narrows **per field**, and that `snippets` is three-state ([decisions](decisions/zephyr.md) 21). **A `static` project has exactly one target, itself** — what `list_targets` reports for it — and the `[[projects.targets]]` menu nothing ever selected from is retired, refused at load ([decisions](decisions/shape.md) 53).

- **Working directory**, for a `static` project, is `source_path` joined with `build_cwd` if set, validated before spawning, and `artifact_path` resolves against **that** directory, not `source_path` alone; a `zephyr-west` project's build directory is per-target instead. Setting `build_cwd` is usually wrong, and the `west` invocation that makes it so is [decisions](decisions/build.md) 5.
- **Capture** drains stdout and stderr in two concurrent tasks — draining one while the other fills its OS buffer is a classic way to hang a child.
- **Truncation keeps the head *and* the tail** behind a marker naming how many bytes went and how many were kept at each end, **the cap bounding the retained total rather than each half** ([decisions](decisions/build.md) 18, which also has the UTF-8-boundary rule both cuts obey; numbers in §7). Under the cap the text is untouched and unmarked.
- **Timeout kills the process group**, not just the immediate child — `west`/`cmake`/`make` fork subprocesses a plain kill would orphan. A killed or timed-out build is reported **distinctly** from a nonzero exit, so a hang is not misread as a code problem.
- **One build in flight per project name**, via a per-project async lock. Separate from Core's hardware lock: it guards two calls stomping one output directory, not USB contention.

## 4. Deployment and topology

Today `embarch-api` runs under WSL2 and Core native on Windows on the same physical machine, reached over the WSL2⟷Windows network boundary rather than loopback.

**Artifact transfer branches on topology class, and the reason is Session 0.** `Local` — same machine, or an explicit `base_url` — sends `firmware_path` as JSON. `WslHost` and `Remote` both **upload the artifact's bytes** as multipart. WSL2 needs it because `\\wsl.localhost\…` UNC shares come from a per-session network provider tied to an interactive logon, and a service runs in **Session 0**, which has none. **Failure signature:** the identical path resolves from an interactive shell and fails with "the network name cannot be found" from the service. It is not about the account. **No UNC path is computed anywhere any more** ([decisions](decisions/core-link.md) 15).

**`base_url = "auto"`** resolves per-process on first use — a short-timeout `GET /status` race over an ordered candidate list (loopback, the WSL2 default-gateway IP, a configured host), first answer wins, and a `401` **counts as an answer**: Core is there, the token is wrong. Cached for the process lifetime, never written back to config, so a WSL2 restart's new gateway IP is picked up next run. **Resolution must be lazy**: the startup check is MCP-mode-only and `list_projects` works with Core down; resolving at config-load time regresses both. **That check warns, it does not refuse** — every hardware-facing tool fails per-call instead, with its message plus the resolved-candidate list. Why refusing was worse: [decisions](decisions/core-link.md) 14.

## 5. Modules

Two front-ends (`tools.rs` MCP, `cli.rs`) over one set of modules, neither privileged; the map is [interfaces/modules.md](interfaces/modules.md). `crates/embarch-core-client/` is a **workspace member** ([decisions](decisions/tests.md) 56), so one `cargo test`/`cargo clippy --all-targets` at the repo root reaches its own tests; `embarch-ui` path-depends on it from outside that workspace — **a change there reaches a repo this one does not own.**

`main` spawns the entire tokio runtime — `block_on` included — **on a dedicated thread with a 512 MiB stack**, because `Builder::thread_stack_size` does not size the thread calling `block_on`, and no knob does ([decisions](decisions/core-link.md) 36).

## 6. Security

**Inbound is "whoever can spawn the process"** — MCP and CLI alike. No API key, bearer token or session at this layer. A deliberate simplification; [open.md](open.md) carries what it costs.

**Outbound** is `EMBARCH_TOKEN`: config `token`, then `token_env`, then machine-wide token-file discovery. Full lifecycle: [embarch-token.md](../embarch-token.md). Whichever value resolves is attached by **one funnel** in `embarch-core-client`, the only place there that authenticates or sends one ([decisions](decisions/core-link.md) 55).

## 7. Constants

| Name | Value | Provenance |
|---|---|---|
| runtime thread stack | 512 MiB | [measured 2026-08-24] 64 MiB overflowed on a real GATT-heavy `StudyResult` |
| `FRESHNESS_CLOCK_GRACE` | 500 ms | [measured] WSL2 clock jitter put a child's mtime *before* the parent's pre-spawn timestamp. A real build takes seconds, so this cannot mask a stale artifact |
| capture cap | 64 KB retained, first 16 KB + last 48 KB | [assumed] — the cap and the split alike. Nothing here has measured a real Zephyr failure's log, so the head share is reasoned (a compiler diagnostic plus the `cmake`/Kconfig preamble is a few KB) rather than sized against one |
| default `build_timeout_secs` | 300 | [assumed] |
| default Core port | 4884 | — |
| log retention | 7 daily files, `api.log.<date>` | deliberately Core's scheme, so one reader covers both |

The logfile is **per-user**, not machine-wide — `/var/lib` is root-owned and this runs as the engineer, verified on this bench ([decisions](decisions/core-link.md) 43).
