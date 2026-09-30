# 108 — Implement and verify a Windows process-tree kill for timed-out builds

**State:** open — code half done (see "Blocked"), worked by agent/api/108-windows-tree-kill,
2026-09-29
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
      after `spawn()`, `TerminateJobObject`ed on timeout. Falls back to `child.start_kill()` if the
      job could not be created/assigned. See `crates/embarch-firmware-build/src/build.rs`
      (`kill_process_tree`, `mod windows_job`) and decision 75's updated text for the full
      mechanism and why Job Object over `taskkill /T /F`.
- [ ] **Not run on an actual Windows process.** What was tried instead, and why it stopped there:
      only `x86_64-pc-windows-msvc` is installed (`rustup target list --installed`); no mingw
      target/linker is present, so no cross-build-and-run under WSL2 interop was possible per the
      dispatch note. A `cargo check --target x86_64-pc-windows-msvc` attempt (to at least
      type-check the new code against the real target) also failed, but before reaching this
      crate's code at all: `embarch-core-client`'s `reqwest` → `rustls` → `aws-lc-sys` chain tries
      to cross-compile C sources with the host Linux `cc`, which fails on
      `pthread_rwlock_t`/Windows-only headers it doesn't have — the same shape of gap
      `embarch-core`'s `hidapi` cross-build hits, and pre-existing, unrelated to this task's own
      code. So this task's new code has compiled and passed `cargo test`/`clippy` on the native
      (unix) target only, and has never been built for Windows at all, let alone run against a
      forked grandchild. **This box stays unchecked and this task stays open** until a Windows
      session (native `cargo.exe`, per the owner's documented working path, or a CI runner) builds
      and exercises it per "What would have to run to believe it".
- [ ] `decisions/build.md` decision 75 and `spec.md` §2's timeout bullet are updated to drop the
      unix-only qualifier once the Windows arm is real and verified — not before. **Decision 75's
      text is updated to describe the new code and its unverified state; the qualifier itself is
      deliberately left in place** (`spec/implementation.md` §3's timeout bullet, since §2 moved
      under `DOC-COMPACTION.md` on 2026-09-29) — not done, correctly, pending the box above.
- [x] `open.md`'s Windows-smoke-harness bullet: **left alone with a reason.** `open.md` is in its
      compaction reserve (`tasks/api/113`, ~665 B of its 5 KB cap left) — adding a pointer sentence
      there would have spent reserve this task doesn't need to spend, since the bullet's substance
      (this task, its unverified state, and the aws-lc-sys cross-compile gap) is now fully covered
      by decision 75's updated text, which `open.md`'s bullet already links to only indirectly.
      No Windows test was added to `tests/smoke_harness.rs` either — the same "cannot run it"
      reason above — so that gap is unchanged and stays exactly as `open.md` already describes it.
- [x] A `changelog.d/` fragment: `changelog.d/api-windows-tree-kill-job-object.decided.md`.
- [x] Gate green on the native (unix) target: `cargo build`, `cargo test`,
      `cargo clippy --all-targets -- -D warnings` all pass. **Not gated on Windows** — see above.

## Blocked

Code-complete, unverified. Leaving this `open` per the task's own "Not yours" section and its
"Done when" instructions: a worker cannot run this on real Windows. What would close it next:
a Windows machine or CI runner building `embarch-api` at `agent/api/108-windows-tree-kill`,
running a build with a forking child under a short `build_timeout_secs`, letting the timeout
fire, and confirming via `tasklist`/Process Explorer that the grandchild is gone — then flipping
the two boxes above and dropping the unix-only qualifier in decision 75 and
`spec/implementation.md` §3.

## Not yours (repeated from `107`, still true here)

Nothing in the fleet's WSL2 environment can execute a Windows binary. This task is **not**
dispatchable to a worker in the same way `107` was — a worker can write the Job-Object /
`taskkill` code and get it to compile, but cannot satisfy "Done when"'s verification box, so
either leave this task `open` with the code half done and the verification box unchecked and
named, or treat it as needing the owner's own Windows session. Do not mark this task `done` on a
compile-only result.
