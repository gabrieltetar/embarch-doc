# 122 — `install-core` on Linux makes Core's `logs/` folder

**State:** open
**Source:** EMB-594 — install-core Linux leaves no writable logs dir for the embarch user (reviewer finding on `umbrella/120`)
**Issue:** EMB-594
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

Decision 70 (`umbrella/120`, merge `b641c2a`) has `install-core` on Linux
create `store/` (`embarch` `0700`) and `study_results/`
(`embarch:embarch-users` `0750`), and leave the data dir `root:root` `0755`.
Its "Deviations" reason that anything a service Core writes in the data-dir
root must be made for `embarch` beforehand, and name only `study_results/`.

Core also writes `<data dir>/logs/`, outside `store/`:
`embarch-core/src/main.rs` `build_log_file_writer`
(`local_data_dir()?.join("logs")`, daily rolling) and `src/logs.rs`
`log_dir`, which `GET /logs/recent` and the dev-bench log mirror read. As
`embarch`, Core cannot create it, `init_tracing` falls back to stderr only, and
`/logs/recent` finds nothing. Read from source, not run.

When this is done: `step_store` creates `<data dir>/logs/` writable by
`embarch`, and decision 70 and the plan text name it. Choose the owner and
mode the same way 70 chose `study_results/`'s, and say why in 70 (does the
engineer need to read the log files directly, or only through Core?). Before
you write, check `embarch-core/src` once more for any other data-dir-root
write a service Core makes, and name the result in 70 either way.

**Not yours:** `embarch-core` (read only) and every other repo; the Windows
half of `install-core` (`%ProgramData%`'s ACL is a separate question). You
never touch hardware.

## Where to look

- `src/install_core_linux.rs` (`step_store`, `LinPaths`, the generated script
  and its golden tests)
- `embarch-doc/embarch-umbrella/decisions/install-core.md` (61, 69, 70),
  `interfaces/install-core.md`, `spec/commands.md`
- `embarch-core/src/main.rs`, `src/logs.rs` (read only)

## Where the doc goes

Amend decision 70 in place (`decisions/install-core.md`, 9,385 B, room).
`open.md` is 3,818 B, about 100 B under its reserve line: net-neutral or
smaller. **Do not grow:** `agent-runtime#67`, `agent-container#62`,
`prune-policy#26`, `deploy#32`, `mirrors#20`.

## Done when

- [ ] The generated script creates `logs/` for `embarch`, asserted by a golden
      test.
- [ ] Decision 70 and the plan text name `logs/` and its owner and mode.
- [ ] The task's hardware-verification debt adds: after the first install in a
      scratch systemd distro, `logs/` holds a dated core log and
      `GET /logs/recent` returns lines.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
