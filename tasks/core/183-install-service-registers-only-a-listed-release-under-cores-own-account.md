# 183 — `install --service` registers only a listed release, under Core's own account

**State:** done — install --service gated on installed-release.json, registers run --service under own account; decision 157; Windows check and first elevated install owed
**Source:** EMB-324 — Core registers any binary as the service, under the default account
**Issue:** EMB-324
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

`service::install` registers `current_exe()` with `run --bind` and
`username: None`. The `sc` backend passes no account, which Windows takes as
its default service account (the issue says this is from memory and unchecked;
do not assert which account in the doc unless you can cite it). `update`
replaces `current_exe()` in place. The design this implements
(`embarch-doc/notes/hil/12-prevention.md`, "The root of trust"): "only a signed
release install runs as the service account", and "from the attested phase on,
a source install runs Core under the engineer's own account, never the service
account".

When this is done, per the issue's direction (the owner moved it to Fleet Ready
with that direction; follow it, and record any deviation in the decision):

- **`install --service --bind <addr>`** refuses unless
  `<data dir>/installed-release.json`, written by the elevated install, lists
  this binary's SHA-256. It then registers `run --service --bind <addr>` under
  Core's own account: on Windows the virtual account `NT SERVICE\com.embarch.core`
  (an `sc config ... obj=` after the create, since the `sc` backend ignores
  `username`); on Linux `User=embarch` through `ServiceInstallCtx.username`. An
  existing registration is rewritten in place, as decision 106 does today.
- **`install` without `--service`** registers nothing. It says a source build
  runs as a development Core and names `embarch deploy-core`.
- **`update`** refuses a registration that runs `--service`: a signed release
  replaces it through the elevated install.
- `start`, `stop` and `uninstall` are not changed here.

The record's own shape (`installed-release.json`) is new: define the smallest
one that lists binary hashes, say in the decision who writes it (the elevated
install, a later task: EMB-339 on Windows, EMB-340 on Linux, both waiting on
this one), and give it in `interfaces/`.

**Not yours:** `embarch-umbrella` (`embarch deploy-core` is named, not
changed), `embarch-api`, and every other repo. You never touch hardware and you
never register a real service: assert on the built arguments and the built
registration, as decision 106's tests do.

## Where to look

- `src/service.rs` — `install` (around line 65), `rewrite_windows_registration`,
  `update`
- `src/elevate.rs`, `src/main.rs` — the `Install` and `Update` arms; `run
  --service` already exists (the attested Core, store in `<data dir>/store/`)
- `embarch-doc/embarch-core/decisions/platform.md` (106, 9.3 KB of 12 KB),
  `spec.md` §3 "Deployment"; `embarch-doc/notes/hil/12-prevention.md`,
  `notes/hil/14-implementation-plan.md` (A.20, A.21)

## Where the doc goes

A new core decision (157 or later; take the next free number when you write it,
by scanning the headings as `DOC-CONVENTIONS.md` says, and cite only that
number in code comments) in `decisions/platform.md` or a new topic file, with an
index row; 106 gets a pointer if its "rewrite in place" now applies only under
`--service`. **Over or near the per-decision cap, do not grow:** `signing#110`,
`analog-capture#127`, `host-study#95`, `definitions#133`, `lease#93`,
`stopping-a-study#128`. **`spec.md` is 9,011 B, 28 B under its reserve line,
and §3 needs amending**, so expect to push it into reserve: file
`tasks/core/<NNN>-compact-core.md` in the same commit (`tasks/README.md` has the
shape; number from `scripts/check-task-numbers.py --next core`). `open.md` is
3,917 B, 2 B under its line; leave it alone if you can.

## Done when

- [x] `install --service` with no record, or a record not listing this
      binary's hash, refuses before any service-manager call.
- [x] With a matching record, the registration built runs
      `run --service --bind <addr>` under the service account, asserted on the
      built arguments for Windows and Linux.
- [x] A plain `install` registers nothing and names `embarch deploy-core`.
- [x] `update` on a `--service` registration refuses.
- [x] The Windows-gated code type-checks for `x86_64-pc-windows-msvc`
      (`cargo check --target x86_64-pc-windows-msvc` where the target is
      installed; say if it is not); a hardware-verification debt is written
      into this file for the first elevated install.
- [x] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`).
- [x] Spec §3 and the install decision amended; `changelog.d/` fragment.

## Hardware-verification debt

First elevated install, on a Windows machine and on a Linux machine (neither writable here: nothing yet writes `installed-release.json`, EMB-339 and EMB-340):

- Windows: with a record listing the built binary, run `embarch-core install --service --bind 127.0.0.1` elevated, then `sc qc com.embarch.core` must show `SERVICE_START_NAME : NT SERVICE\com.embarch.core` and `BINARY_PATH_NAME` ending `run --service --bind 127.0.0.1`, and Core must start with `mode: service`. Check the virtual account can write `%ProgramData%\embarch\store\` (the install owns its ACL, EMB-339). Re-run over the registration to confirm the in-place rewrite still sets the account.
- Linux: `systemctl cat com.embarch.core` shows `User=embarch` and `ExecStart=... run --service --bind ...`.
- `embarch-core update <exe>` against that registration refuses.
- Not run: `cargo check --target x86_64-pc-windows-msvc` installs but fails in `hidapi`'s `build.rs` (no `guiddef.h`, the known WSL limit), so the Windows-gated code (`apply_windows_account`, the `registered_command` registry read) is unchecked by a compiler.
- Caller: `embarch-umbrella` calls `install --bind`, which now registers nothing; moving it to `--service` or `deploy-core` is that repo's.
