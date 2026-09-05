# 003 — `embarch setup --dry-run` is one flag and an early return away, and does not exist

**State:** done
**Source:** embarch-umbrella/002 (design-only decisions audit, 2026-09-03) — decision 21 read against the source and found unbuilt
**Scope:** umbrella
**Hardware:** none
**In reserve for this sub-project:** `embarch-umbrella/spec.md` — 9671/10240 B,
**569 B of headroom**, already filed against `tasks/umbrella/009-compact-docs.md`
(which is `blocked`, `In flux: yes`). `open.md` is out of reserve (88.1%). Plan
the `setup` row edit inside 569 bytes; if you spend past the cap or push
`open.md` back into reserve, file `tasks/doc/<NNN>-compact-umbrella.md` in the
same commit per `tasks/README.md` § "Compaction tasks".

## What

`embarch-umbrella` decision 21 says `embarch setup --dry-run` runs every
detection step exactly as `setup` does and prints the concrete actions — which
service calls, which files, whether elevation is needed — **reusing `setup`'s own
detection path rather than a second implementation.**

The flag does not exist. `Command::Setup` in `src/main.rs` carries `--host`,
`--port`, `--uninstall` and `--dev-bench-repo` only; the sole `--dry-run` in the
binary is `deploy-core`'s.

**The hard part is already done.** `setup::make_plan` runs every detection step
and returns a `Plan` before anything is acted on, and `setup` already prints the
elevated commands it would have a human paste. What is missing is the flag and a
return before the first side effect — plus deciding what `--dry-run` prints for
the steps that currently only print *while* acting (the canonical install and the
`PATH` write, decision 28, which post-date decision 21's text).

## Why now

Decision 21's reason is that elevation is partly a "what is this about to do to
my machine" problem, and worse when the answer requires trusting a binary you
just downloaded — which is exactly the first-day case umbrella exists for.
Cheap, and `spec.md` advertised the flag as shipped until 2026-09-03.

## Done when

- [x] `embarch setup --dry-run` prints the plan and makes no change: no service
      call, no token file, no copy, no `PATH` or registry write.
- [x] Decision 28's install and `PATH` steps are represented in the printed plan,
      not silently omitted.
- [x] A test proves the dry run reaches no side-effecting call.
- [x] `spec.md`'s `setup` row and decision 21's implementation note updated.
- [x] Gate green; `changelog.d/` fragment dropped.

## What shipped

**The early return was not enough, and that is the finding.** `make_plan` did
already run every detection step first, but decision 28's binary copy and `PATH`
write — which post-date decision 21's text — only ever printed *while* acting,
so returning before them would have omitted them from the plan entirely.

Code (`embarch-umbrella`):

- `install.rs`: `install()` → `install_into(source_dir, bin_dir, home)`, every
  writable location a parameter; new read-only `plan_install` + `InstallPlan`
  built from the same `SUITE_BINARIES`, `paths_refer_to_the_same_file` and
  sourcing-line predicate the real install uses, so the two cannot drift;
  `windows_path::is_on_path` reads `HKCU\Environment` with `KEY_READ` only.
- `setup.rs`: a `Locations` struct resolves the four writable paths once;
  `setup` = `make_plan` + a new `apply_plan` that both modes walk.
- `locate.rs`: `FoundBy::PendingInstall` ("would be installed by this run"), so
  a dry run never claims `JustInstalled`.
- `state.rs`: `save_to(path, state)`, with `save` as the env-resolving wrapper.
- `main.rs`: `--dry-run`, `conflicts_with = "uninstall"`.

Tests: `a_dry_run_reaches_no_side_effecting_call` points every writable location
at a sandbox and makes `embarch-core` a script that would leave a sentinel if
executed, then asserts the sandbox untouched;
`the_dry_run_plan_names_the_install_and_the_path_write` asserts the rendered plan
names the bin dir, each binary (including the one absent from the archive), the
rc file and `PATH`.

Docs: `spec.md`'s `setup` row, decision 21 in `decisions/install.md`, `open.md`'s
unbuilt list (seven → six), `changelog.d/umbrella-setup-dry-run.added.md`, and
`status.d/umbrella-setup-dry-run.md` for `suite/features.md`'s "`--dry-run`
unbuilt".

Gate: `cargo build` / `test` (114 pass) / `clippy --all-targets -D warnings`
clean; `check-docs.py` 7/7; `check-ownership.py --scope umbrella` on both.

**Verification debt, host-side not hardware.** Only the Unix `PathPlan` arm ran:
`plan_path`'s Windows arm and `windows_path::is_on_path` are `#[cfg(windows)]`
and there is no Windows linker here — the same named gap decision 28 already
carries for `ensure_path`. A `--dry-run` on a real Windows machine would settle
both at once. Also unexercised: the `wsl-host` and `remote` arms print the same
text in both modes (they were already print-only), so nothing new is at risk
there, but no dry run has been done on a `wsl-host` machine.
