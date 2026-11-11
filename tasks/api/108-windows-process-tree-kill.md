# 108 — Implement and verify a Windows process-tree kill for timed-out builds

**State:** done — verified on Windows 11 by agent/api/108-windows-tree-kill, 2026-11-10
**Source:** `tasks/api/107` — correcting `spec.md` §2's unqualified "timeout kills the process
group" invariant surfaced that `src/build.rs`'s `#[cfg(not(unix))] kill_process_tree` kills only
the immediate child, and `107` was explicitly told not to implement the fix (see its own "Not
yours"): nothing in the fleet's environment can execute or verify a Windows kill path.
**Scope:** api
**Hardware:** none to write the code, but **this task cannot be marked done by a build alone** —
see "Done when". No board is needed; a Windows machine (or CI runner) able to actually run the
resulting binary is.
**Owner:** no

## What

`decisions/build.md` decision 75 records why this crate deliberately ships an asymmetric
`kill_process_tree`: on unix, the child is placed in its own process group
(`command.process_group(0)`) and the whole group is `SIGKILL`ed on timeout; on Windows,
`#[cfg(not(unix))]`'s arm only calls `child.start_kill()`, so a timed-out `west`/`cmake`/`ninja`
tree survives the report of "killed" and keeps the build directory locked.

Close it: give the Windows arm a real tree kill — most likely a Win32 Job Object created before
`spawn()` (`CREATE_SUSPENDED` isn't needed; assign the job, resume, and `TerminateJobObject` on
timeout closes every process in it including grandchildren `west` forks), or `taskkill /T /F /PID
<pid>` shelled out the way the unix arm shells out to `kill`. A Job Object is the more robust
choice — `taskkill` can itself hang or fail to enumerate a fast-forking tree — but needs the
`windows` or `windows-sys` crate added as a Windows-only dependency.

## Why now

Not urgent — `open.md` and decision 75 both already carry the gap as a documented, deliberate
asymmetry, not a silent one. This task exists so the fix has a place to land *when* something can
verify it, rather than being implemented blind the way `107` was told not to.

## What would have to run to believe it

This is the load-bearing section — do not close this task on a green `cargo build
--target x86_64-pc-windows-msvc` alone; that only proves the code compiles, which is not what is in
question.

- A **Windows** process (native build or CI runner, not cross-compiled and left unexecuted) needs
  to actually spawn a build command that forks a child of its own — a real `west build` is the
  honest case, but a minimal repro (a `.bat` or small Rust helper that spawns a grandchild and
  outlives its parent) is enough to prove the mechanism — run it under this crate's timeout path,
  let the timeout fire, and confirm via `tasklist`/Process Explorer that the grandchild is gone
  afterward, not merely the immediate `cmd.exe`/`west.exe`.
  - `tests/smoke_harness.rs` and decision 46's four end-to-end tests are `#![cfg(unix)]`
    (`open.md`) — this almost certainly wants a Windows-only test added there rather than reusing
    the unix fixtures, since the POSIX-shell fixture behind them won't run on Windows either. That
    `#![cfg(unix)]` gap is filed separately (`open.md`, mentioned in `107`'s report) and is not
    this task's to fix, but this task's new test is the natural first Windows entry in that file.
  - `.github/workflows/release.yml`'s Windows job currently only builds
    (`x86_64-pc-windows-msvc`, `windows-latest` runner) — it does not run `cargo test`. Either add
    a test step to that job for this platform, or accept that verification stays a one-time
    manual run and say so plainly rather than implying CI covers it.
- Whichever mechanism is chosen (Job Object vs `taskkill /T /F`), the verification has to cover the
  actual failure mode named in decision 75: a **forked grandchild**, not just the immediate child
  — `child.start_kill()` already kills the immediate child today, so a test that only checks the
  immediate process exits proves nothing new.

## Done when

- [x] A Windows tree-kill is implemented in `#[cfg(windows)] kill_process_tree`: a Win32 Job Object
      (`windows-sys`, `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`), created and assigned to the child right
      after `spawn()`, `TerminateJobObject`ed on timeout, falling back to `child.start_kill()` if the
      job could not be created or assigned. Landed on `main` as cfa8197 (2026-09-29).
- [x] **Run on an actual Windows process, 2026-11-10.** Windows 11 under WSL2, native
      `C:\Users\…\.cargo\bin\cargo.exe` over a `git archive` copy of this branch and its two sibling
      path deps on the Windows side (`_wt/api-108/`, not the deployed Core's checkout). Three runs:
      - `crates/embarch-firmware-build/tests/windows_tree_kill.rs` (new, `#![cfg(windows)]`):
        the build command is the test binary re-executed as a parent that waits on a grandchild;
        `build_timeout_secs` 3; after the timeout `tasklist /FI "PID eq <grandchild>"` must stop
        listing it within 10 s. **Passes, 3 of 3 runs, 3.1 s each.**
      - **Control**, same test with `windows_job::assign` replaced by `None` in the Windows copy
        only (never committed): **fails** with "grandchild PID 27488 outlived the timed-out build:
        tasklist still lists it". An earlier draft of the test, checking only that `run_build`
        returned, also failed under the control, after 180 s: the grandchild inherits the
        build's pipe handles even with its own stdio nulled, so a survivor also hangs the drain.
        That is why the test now runs the build on its own thread and checks both.
      - **End to end through the real binary**: `embarch-api.exe --config api.toml build fork-demo`,
        a static project whose `build_command` is `cmd /c fork.bat` (`start "" /b ping -n 120
        127.0.0.1` then `ping -n 120 127.0.0.1`), `build_timeout_secs = 4`. `tasklist /FI
        "IMAGENAME eq PING.EXE"`: none before, two (PIDs 22672, 25856) at 2 s, **none after**.
        The CLI printed "build timed out for 'fork-demo'", exit 1, wall time 4.8 s.
      Also on Windows: `cargo clippy -p embarch-firmware-build --all-targets --no-deps -- -D
      warnings` clean; `cargo test -p embarch-firmware-build` 92 unit tests pass (the `config::`
      failures the 2026-09-29 note saw are gone).
- [x] Decision 75 rewritten to current truth and retitled without the unix-only qualifier;
      `spec/implementation.md` §3's timeout bullet now reads "kills the whole process tree"; the
      `decisions.md` index row says the same.
- [x] `open.md` left alone, with a reason: its Windows bullet is about the root `smoke_harness.rs`
      tier, which is still unix-only. The new test went into the build crate's own `tests/`
      instead, beside `cross_process_lock.rs`, because it drives `BuildLocks::run_build`
      directly rather than the binary.
- [x] `release.yml` left alone: its Windows job still only builds. The verification is a one-time
      manual run plus a test that runs wherever `cargo test` runs on Windows; decision 75 says so.
- [x] Changelog fragment `changelog.d/api-windows-tree-kill-verified.changed.md`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — see the report.
