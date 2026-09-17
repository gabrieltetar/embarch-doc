# 108 — Implement and verify a Windows process-tree kill for timed-out builds

**State:** open
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

- [ ] A Windows tree-kill is implemented in `#[cfg(not(unix))] kill_process_tree`.
- [ ] It has been **run on an actual Windows process** per "What would have to run to believe it"
      above, and the result — pass or fail, and what was run, by whom, on what — is recorded here
      before this task closes. A worker dispatched this task and unable to run it on real Windows
      leaves this `open` with what it tried, the same way hardware-gated tasks do, rather than
      reporting green on a build alone.
- [ ] `decisions/build.md` decision 75 and `spec.md` §2's timeout bullet are updated to drop the
      unix-only qualifier once the Windows arm is real and verified — not before.
- [ ] `open.md`'s Windows-smoke-harness bullet is either linked from here or left alone with a
      reason, since a Windows test added for this task is the first crack in that gap.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`.

## Not yours (repeated from `107`, still true here)

Nothing in the fleet's WSL2 environment can execute a Windows binary. This task is **not**
dispatchable to a worker in the same way `107` was — a worker can write the Job-Object /
`taskkill` code and get it to compile, but cannot satisfy "Done when"'s verification box, so
either leave this task `open` with the code half done and the verification box unchecked and
named, or treat it as needing the owner's own Windows session. Do not mark this task `done` on a
compile-only result.
