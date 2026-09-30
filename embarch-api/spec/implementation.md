# embarch-api: spec — implementation

**Status:** active, 2026-09-05.

Split verbatim out of [../spec.md](../spec.md) §§3-7 on 2026-09-29 under
[DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 (`tasks/api/083`) — `spec.md`'s
own natural seam, §§1-2 "what it is and what must always hold" vs this file's
"how it does it". Current truth: [../spec.md](../spec.md). Why: [../decisions.md](../decisions.md).

## 3. Build orchestration

**What a call may name, and what each project kind does with it, is [interfaces/config.md](../interfaces/config.md)** — `default_target`'s per-field narrowing, `snippets`' three-state `["none"]` ([decisions](../decisions/zephyr.md) 21), the build-directory naming. Two rules an agent must not invert: a `static` project **refuses** a selection it cannot honour rather than accepting and dropping it, on a call ([decisions](../decisions/zephyr.md) 51) and at config load for all five `zephyr-west`-only fields ([decisions](../decisions/zephyr.md) 20); and **it has exactly one target, itself** — the `[[projects.targets]]` menu nothing ever selected from is retired, refused at load ([decisions](../decisions/config-retirement.md) 53).

- **Working directory** for a `static` project is `source_path` joined with `build_cwd` if set, validated before spawning; `artifact_path` resolves against **that**, not `source_path` alone. Setting `build_cwd` is usually wrong ([decisions](../decisions/build.md) 5). A `zephyr-west` project's is per-target.
- **Capture** drains stdout/stderr in two concurrent tasks, as raw bytes not decoded text — draining one while the other fills its OS buffer hangs a child, and decoding per line rather than per stream means one non-UTF-8 byte costs one line, never the rest; a line needing lossy decoding is named in a summary marker, never silent ([decisions](../decisions/log-capture.md) 65).
- **Truncation keeps the head *and* the tail** behind a marker naming how many bytes went and how many were kept at each end, **the cap bounding the retained total rather than each half** ([decisions](../decisions/log-capture.md) 18, numbers in §7). Under the cap, text is untouched and unmarked.
- **Timeout kills the process group on unix, only the immediate child on Windows** ([decisions](../decisions/build.md) 75). A killed/timed-out build is reported **distinctly** from a nonzero exit, so a hang isn't misread as a code problem.
- **One build in flight per project**, via a per-project async lock. Separate from Core's hardware lock: guards two calls stomping one output directory, not USB contention.

## 4. Deployment and topology

Today `embarch-api` runs under WSL2, Core native on Windows, same physical machine, reached over the WSL2⟷Windows network boundary rather than loopback.

**Artifact transfer branches on topology class, and the reason is Session 0.** `Local` — same machine, or an explicit `base_url` — sends `firmware_path` as JSON. `WslHost` and `Remote` both **upload the artifact's bytes** as multipart. WSL2 needs it because `\\wsl.localhost\…` UNC shares come from a per-session network provider tied to an interactive logon, and a service runs in **Session 0**, which has none. **Failure signature:** the identical path resolves from an interactive shell and fails with "the network name cannot be found" from the service — not an account problem. **No UNC path is computed anywhere any more** ([decisions](../decisions/core-link.md) 15).

**`base_url = "auto"`** resolves per-process on first use — a short-timeout `GET /status` race over an ordered candidate list (loopback, the WSL2 default-gateway IP, a configured host), first answer wins, and a `401` **counts as an answer**: Core is there, the token is wrong. Cached for the process lifetime, never written back to config, so a WSL2 restart's new gateway IP is picked up next run. **Resolution must be lazy** — the startup check is MCP-mode-only and `list_projects` works with Core down. **That check warns, it does not refuse** — every hardware-facing tool fails per-call instead. Why refusing was worse: [decisions](../decisions/core-link.md) 14.

## 5. Modules

Two front-ends (`tools.rs` MCP, `cli.rs`) over one set of modules; the map is [interfaces/modules.md](../interfaces/modules.md). **Two** sibling crates under `crates/` are **workspace members** ([decisions](../decisions/tests.md) 56), so one `cargo test`/`cargo clippy --all-targets` at the repo root reaches both their tests: `embarch-core-client/` and, since 2026-09-18, `embarch-firmware-build/` — `config`/`zephyr`/`resolve`/`build`/`json_out`, lifted out of `src/` so `embarch-ui` can build a study's firmware through the same implementation ([decisions](../decisions/firmware-build-crate.md) 78). `embarch-ui` path-depends on both from outside that workspace — **a change there reaches a repo this one does not own.**

`main` spawns the entire tokio runtime — `block_on` included — **on a dedicated thread with a 512 MiB stack**, because `Builder::thread_stack_size` doesn't size the thread calling `block_on`, and no knob does ([decisions](../decisions/client-crate.md) 36).

## 6. Security

**Inbound is "whoever can spawn the process"** — MCP and CLI alike, no API key, bearer token or session at this layer. A deliberate simplification; [open.md](../open.md) carries what it costs.

**Outbound** is `EMBARCH_TOKEN`: config `token_env`, then `token`, then machine-wide token-file discovery. Full lifecycle: [embarch-token.md](../../embarch-token.md). Whichever value resolves is attached by **one funnel** in `embarch-core-client`, the only sender ([decisions](../decisions/client-crate.md) 55).

## 7. Constants

| Name | Value | Provenance |
|---|---|---|
| runtime thread stack | 512 MiB | [measured 2026-08-24] 64 MiB overflowed on a real GATT-heavy `StudyResult` |
| `FRESHNESS_CLOCK_GRACE` | 500 ms | [measured] WSL2 clock jitter put a child's mtime *before* the parent's pre-spawn timestamp; a real build takes seconds, so this can't mask a stale artifact |
| capture cap | 64 KB retained, first 16 KB + last 48 KB | [assumed] — no real Zephyr failure log measured here. Reasoning, and what would move it: [decisions](../decisions/log-capture.md) 18 |
| default `build_timeout_secs` | 300 | [assumed] |
| default Core port | 4884 | — |
| log retention | 7 daily files, `api.log.<date>` | Core's scheme, so one reader covers both |

The logfile is **per-user**, not machine-wide — `/var/lib` is root-owned, this runs as the engineer ([decisions](../decisions/logging.md) 43).
