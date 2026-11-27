# 122 — `install-core` on Linux makes Core's `logs/` folder

**State:** claimed by agent/umbrella/122-install-core-on-linux-makes-cores-logs-folder, 2026-11-27 00:53
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

Amend decision 70 in place. **`decisions/install-core.md` is now 11,774 of
12,288 B, in reserve** (out at 11,059 B or less) since `umbrella/121` added
decision 71, and its debt is `tasks/umbrella/123-compact-umbrella.md`,
`blocked` on `In flux: yes`. A blocked compaction parks the pass, not the
reserve, so **this unit pays it** (`DOC-BUDGET.md`, split first): split the
file **verbatim** by mission before you amend 70 — for example the two
platform halves, 69 and 70, into a topic file of their own, or 71 into the
file of its subject — with index rows and every inbound link checked
(`scripts/check-duplication.py umbrella` first). Carry 123's
`Must not delete:` list. Once the file is out of reserve, close
`tasks/umbrella/123` `done` in your commit and leave its `In flux: yes` as
written. If no verbatim seam fits, say why in 123 and leave it open.
`open.md` is 3,762 B, about 150 B under its reserve line: net-neutral or
smaller. **Do not grow:** `agent-runtime#67`, `agent-container#62`,
`prune-policy#26`, `deploy#32`, `mirrors#20`.

**Two stale lines to correct while you are here** (the `umbrella/121`
reviewer's note, against decision 71): `spec/commands.md` row 9 still says
`setup` will "install Core as a service", and `decisions/setup-reversal.md`
(around line 23) has the dry run naming the `embarch-core install --bind`
line. Correct both to what 71 says `setup` does now, net-neutral.

## Done when

- [ ] The generated script creates `logs/` for `embarch`, asserted by a golden
      test.
- [ ] Decision 70 and the plan text name `logs/` and its owner and mode.
- [ ] The task's hardware-verification debt adds: after the first install in a
      scratch systemd distro, `logs/` holds a dated core log and
      `GET /logs/recent` returns lines.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
