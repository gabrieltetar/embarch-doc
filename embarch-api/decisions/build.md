# embarch-api decisions: Running a build

**Status:** active, 2026-09-05.

The generic per-project command.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). What gets built — the Zephyr exception decision 5 scopes — is [zephyr.md](zephyr.md). What a build produces: log capture and truncation is [log-capture.md](log-capture.md), `target.json` provenance is [target-json.md](target-json.md), the flash offset is [flash-address.md](flash-address.md).

### 5 — A generic configurable command per project, not toolchain-specific logic
Originally motivated by an assumption that the two day-one projects used different toolchains. On inspection **both turned out to be Zephyr/west-based** — one reads as an Arduino board by name and its own `board.yml` confirms otherwise, confirmed by reading the real repo rather than assuming from the name. The generic design is kept regardless: it is the right call on its own merits, even though the two-toolchain premise did not hold.

**`build_cwd` is usually wrong to set, and the reason is `west`'s own default.** It is a `static` project's field only — a `zephyr-west` build directory is per-target. The build runs in `source_path` joined with `build_cwd`, and `artifact_path` resolves against **that** directory rather than `source_path` alone. `west`'s default output is `<cwd>/build`, so an invocation from the repo root with the app path as an argument must leave `build_cwd` **unset**, or the configured artifact path points at a `build/` nothing writes to — a build that "succeeds" and then fails its freshness check, or worse, flashes a stale image from an older tree. Shapes: [../interfaces/config.md](../interfaces/config.md).

### 75 — A timed-out build's process-tree kill is unix-only, and stays that way until something can exercise a Windows one
`west`/`cmake`/`make` fork subprocesses a plain `kill()` on the immediate child orphans, so the unix arm of `src/build.rs`'s `kill_process_tree` puts the child in its own process group (`process_group(0)`) and kills the group. The `#[cfg(not(unix))]` arm — same function name — calls only `child.start_kill()`, so on Windows a timed-out `west`/`cmake`/`ninja` tree outlives the "killed" report and keeps the build directory locked.

Not closed here **on purpose**, not from oversight: `x86_64-pc-windows-msvc` is a real `release.yml` target, but that job only builds it — the same gap [open.md](../open.md) already names for the smoke-harness tier — and this environment cannot run a Windows process to verify a `taskkill /T /F` or Job-Object kill against. Shipping one unexercised would trade a documented gap for an invariant that looks closed and has never run — the exact failure mode [spec.md](../spec.md) §2's no-inference-as-fact posture exists to keep out of the *code*, not only out of DUT claims. What would have to run to believe an implementation: `tasks/api/108`.
