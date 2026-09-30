# 121 — Two pre-existing Windows-only reds in embarch-api: unused imports in core-client, failing `config::` tests in firmware-build

**State:** open
**Source:** supervisor-log.md, leg entry for `api/108` (2026-09-29 22:33) — found while running native
Windows `cargo.exe` on an rsync'd copy of `embarch-api`; not filed by that leg. Supervisor-filed.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

On a native Windows build (`x86_64-pc-windows-msvc`), `embarch-api` has two pre-existing failures
that the Linux gate cannot see:

1. `crates/embarch-core-client/src/token_discovery.rs` — two imports are unused on Windows (most
   of the file is `#[cfg(unix)]`), so `cargo clippy --all-targets -- -D warnings` is red there.
   Gate the imports by `cfg` (or move them into the `cfg(unix)` items), without changing unix
   behaviour.
2. `crates/embarch-firmware-build` — the `config::` unit tests fail on Windows. Find out why
   (likely path separators or a unix-only path assumption in a test fixture) and fix the test or
   the code, whichever is actually wrong. If it is the code, say so in the changelog fragment.

## Why now

The previous leg recorded both as "pre-existing, not filed yet". `embarch-dev-workflow.md` requires
a native Windows build where Core is involved, and a permanently red Windows clippy makes that
check meaningless for every later unit.

## Done when

- [ ] Linux `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green.
- [ ] Windows check, if the worker can run it: `cargo.exe` is reachable from WSL
      (`/mnt/c/Users/tmp12/.cargo/bin/cargo.exe`) against an rsync'd copy **outside** the worktree
      (a `\\wsl$` path build is slow and unreliable). If it cannot be run, say so and leave the
      task `open` with the change landed, rather than claiming Windows green.
- [ ] `changelog.d/` fragment dropped. No decision expected.
