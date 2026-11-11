# embarch-api decisions: Running a build

**Status:** active, 2026-09-05.

The generic per-project command.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). What gets built — the Zephyr exception decision 5 scopes — is [zephyr.md](zephyr.md). What a build produces: log capture and truncation is [log-capture.md](log-capture.md), `target.json` provenance is [target-json.md](target-json.md), the flash offset is [flash-address.md](flash-address.md).

### 5 — A generic configurable command per project, not toolchain-specific logic
Originally motivated by an assumption that the two day-one projects used different toolchains. On inspection **both turned out to be Zephyr/west-based** — one reads as an Arduino board by name and its own `board.yml` confirms otherwise, confirmed by reading the real repo rather than assuming from the name. The generic design is kept regardless: it is the right call on its own merits, even though the two-toolchain premise did not hold.

**`build_cwd` is usually wrong to set, and the reason is `west`'s own default.** It is a `static` project's field only — a `zephyr-west` build directory is per-target. The build runs in `source_path` joined with `build_cwd`, and `artifact_path` resolves against **that** directory rather than `source_path` alone. `west`'s default output is `<cwd>/build`, so an invocation from the repo root with the app path as an argument must leave `build_cwd` **unset**, or the configured artifact path points at a `build/` nothing writes to — a build that "succeeds" and then fails its freshness check, or worse, flashes a stale image from an older tree. Shapes: [../interfaces/config.md](../interfaces/config.md).

### 75 — A timed-out build kills its whole process tree: a process group on unix, a Job Object on Windows
`west`/`cmake`/`ninja` fork children that killing the immediate child orphans, holding the build's pipes. Unix puts the child in its own process group (`process_group(0)`) and kills the group. Windows creates a Job Object with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` (`windows-sys`), assigns the child right after `spawn()` and calls `TerminateJobObject` on timeout; a job that cannot be created or assigned falls back to `child.start_kill()`. After spawn, not `CREATE_SUSPENDED`: a grandchild forked before assignment escapes, accepted. Not `taskkill /T /F`: an outside process can hang or miss a fast-forking tree.

**Verified on Windows 11 with native `cargo.exe`, 2026-11-10** (`tasks/api/108`). `crates/embarch-firmware-build/tests/windows_tree_kill.rs` times out a parent waiting on a grandchild, and `tasklist` no longer lists the grandchild; with the job disabled the same test fails, the grandchild still listed. An `embarch-api build` forking two `ping.exe` under `build_timeout_secs = 4` reported a timeout after 4.8 s and left none. **CI does not run it**: `release.yml`'s Windows job only builds.

### 91 — The build guard is an OS advisory file lock, so it holds across processes
`BuildLocks` was an in-memory mutex map: it serialized two builds of one lock key only inside one process, while every CLI subcommand, every agent session's MCP server and `embarch-ui` each hold their own. It now takes, after the in-process mutex, an exclusive advisory lock on `<temp dir>/embarch-build-locks/<key>-<fnv1a>.lock`, inside `run_build` and `run_build_streaming` — so all three consumers get it with no code change and the public API is source-compatible (`BuildLocks::with_lock_dir` is additive).

- **Wait, do not refuse.** The in-process behavior was to queue, and a build's own `timeout_secs` bounds the holder. A waiter polls `File::try_lock` every 200 ms (cancel-safe, parks no thread), says "another process is already building <key>; waiting" once through `tracing::warn!` and the streaming sink, and prefixes the returned `stderr` with "note: waited Ns for another process's build of <key> to finish".
- **A dead holder frees it.** The OS drops the lock with the descriptor, so a killed process never blocks the next build; the lock file itself is never deleted.
- **No new dependency**: `std::fs::File::try_lock` (stable since Rust 1.89), which also covers Windows. Hash is FNV-1a by hand, not `DefaultHasher`, so `embarch-ui` and `embarch-api` built by different compilers agree on the file.
- **Scope is one machine and one temp dir.** A WSL process and a native Windows process do not share `/tmp`, and a different `TMPDIR` or user gets a different lock; keys are not path-qualified, so two checkouts of one project name serialize (conservative). Tests are unix-only; the Windows arm compiles by the same std call but has [assumed] behavior, never run.
Tests: `crates/embarch-firmware-build/tests/cross_process_lock.rs` (two re-executed processes, parallel keys, killed holder).


### 103 — Named build variants, each in its own directory, for both discovery kinds
`[projects.build_variants.<name>]` declares `extra_conf_files`, `overlays` and `defines`, passed after `west build`'s `--`. A `zephyr-west` variant builds in `<build_dir_root>/<target dir>.<name>`; a `static` one in `<build cwd>/build-<name>`, which needs a plain `west build` argv (no `-d`, no `--`) and an artifact under `build/` — refused at load otherwise, never spliced into a shell command. `default` names the build with none.
- **Incremental by default.** Wiped (`-p always`) only when asked or when `target.json` shows other variant settings, since CMake keeps a dropped `-D`. A matching cache gets no CMake arguments, so west does not reconfigure [measured 2026-11-10: 0.5 s against 6.8 s pristine, sample app].
- **`vs`** reads the other build's record before building, so naming the same variant compares against its previous build.
- **Not on `Selection`**: `embarch-ui` builds that struct field by field. **Not `pristine` on a `static` default build**: its argv is the operator's.
