# EmbArch: getting started

**Status:** draft, 2026-08-05. For a firmware engineer who has never used EmbArch.

> **Read this first.** Chapters 3–9 describe the real `embarch` setup tool — it shipped as part of `v0.1.0` ([embarch-roadmap.md](embarch-roadmap.md)'s Shipped foundation, Onboarding). This guide was originally written ahead of that tool as its specification; it now describes the real, released binaries. If you're setting up a machine right now, this is the path to follow. [Appendix A](#appendix-a--the-manual-path-that-works-today) is kept only as the pre-release manual procedure, for reference or if you hit something `setup`/`init` genuinely can't do yet (§8's "separate-box Core" row).

---

## 1. What EmbArch gives you

EmbArch lets you build and flash your firmware, reset your board, and read its serial console **from wherever your code lives** — including from an AI coding agent — without fighting over who owns the USB port.

The concrete problem it was built for: your firmware builds in WSL2, but your debug probe is a Windows USB device, and forwarding USB into WSL2 is miserable. EmbArch splits the job in two so the boundary stops mattering.

Three pieces:

| Piece | What it does | Where it runs |
|---|---|---|
| **`embarch-core`** | Owns the debug probe and the serial port. Flash, reset, read the console. Nothing else. | On the machine the probe is physically plugged into |
| **`embarch-api`** | Knows about your *projects*: how to build each one and which chip it targets. Runs the build, hands the artifact to Core. | On the machine your source lives on |
| **`embarch`** | Sets the other two up, and tells you what's broken. Not involved once things work. | Wherever you're setting up |

You reach `embarch-api` two ways, and **both are first-class** — neither is a wrapper around the other:

```
you, at a terminal:   embarch-api build-and-flash my-project
Claude Code:          "build this and flash it to the board"  (over MCP)
```

Use whichever suits the moment. Typing the command yourself is often faster; the agent path matters when the agent needs to see a compiler error or a serial log to fix its own change.

## 2. Pick your setup

Find your row. This determines nothing you have to configure — setup detects it — but it tells you what to expect.

| Your machine | Core runs | API runs | Status |
|---|---|---|---|
| **Windows + WSL2**: code in WSL2, probe on Windows | Windows, natively | WSL2 | **Best supported.** This is the topology in daily use |
| **Mac**: everything on the Mac | macOS | macOS | Supported, **never tested on a real Mac** |
| **Linux**: everything on the one box | Linux | Linux | Supported, mechanically the simplest |
| **Windows only**: no WSL2 | Windows | Windows | Supported, untested |
| **Probe on a separate box** (a Pi on your wifi) | that box | your laptop | **Partial** — status/reset/serial work, **flashing does not**. See [§8](#8-when-something-breaks) |

Prerequisites, all topologies:
- A debug probe your board supports — J-Link, ST-Link, CMSIS-DAP, and FTDI all work, as does an on-board debugger like an nRF DK's.
- Your existing firmware toolchain, working. EmbArch runs *your* build command; it doesn't install or replace `west`, `idf.py`, or anything else.
- An elevated shell, **once**, to install Core as a service that starts at boot: Administrator on Windows, `sudo`/root on Linux and macOS. Every OS needs this — it's what installing a system service costs — and it's the only step that ever does.

## 3. Install

Download **one archive per operating system you're setting up** from [embarch-umbrella releases](https://github.com/gabrieltetar/embarch-umbrella/releases). Each archive contains all three binaries as a version-tested set, built for that one OS.

| Platform | Archive |
|---|---|
| Windows | `embarch-<version>-x86_64-pc-windows-msvc.zip` |
| Linux | `embarch-<version>-x86_64-unknown-linux-gnu.tar.gz` |
| macOS (Apple silicon) | `embarch-<version>-aarch64-apple-darwin.tar.gz` |

**On Windows + WSL2, this means downloading two archives, not one** — the Windows `.zip` *and* the Linux `.tar.gz` — because WSL2 is a separate Linux environment from the Windows host, not just another shell into the same binaries. Unpack the Windows archive somewhere on the Windows filesystem (for the elevated Windows leg below), and separately unpack the Linux archive **inside WSL2's own filesystem** — your WSL2 home directory (`~`), not a `/mnt/c/...` path — for the WSL2 leg. Running the Windows `.exe`s from WSL2 via `/mnt/c/...` is not the intended flow and won't work as `embarch setup` (WSL2's shell won't resolve `embarch` to a Windows `.exe` without the `.exe` suffix, and even if invoked as `embarch.exe`, it's the wrong binary for the WSL2-side API — it needs to run as a native Linux process, not through interop).

Unpack it, then run setup from the unpacked directory:

```sh
./embarch setup          # Linux, macOS
```
```bat
embarch setup            :: Windows, cmd.exe — no ./ prefix, cmd.exe doesn't understand it
```
```powershell
.\embarch setup           # Windows, PowerShell
```

Run this from an elevated shell — Administrator on Windows, `sudo` on Linux/macOS. Installing a system service requires it on every OS, and this is the only step that ever does.

On **Windows + WSL2**, run it **twice, in this order, from the two separately-unpacked archives (see above)**: once in the elevated Windows shell against the Windows archive (which installs and starts Core), then once inside WSL2, in your WSL2 home directory, against the **Linux** archive (which sets up the API side and finds the Core you just started). **Order matters** — run the WSL2 leg first (easy to do if that's the shell you already have open) and, with no Core installed anywhere yet, `setup` can't tell your machine apart from a plain single-OS one: it reports `Topology: local` and fails with "`embarch-core: not found`", which doesn't point you back at the Windows-first step. If you see that, it's this trap, not a broken archive — go run the elevated Windows leg first, then retry.

**`Topology: local` from the elevated Windows leg itself, with no failure alongside it, is expected — not the trap above.** From native Windows alone, before the WSL2 leg has run, `setup` has no way to see that a WSL2 side exists at all; `local` just means "nothing WSL2-specific detected yet." Confirm Core actually started (or was already running) and the token file is present, then move on to the WSL2 leg — that's the step that resolves the pairing and reports the real topology (`wsl-host`).

On **macOS**, the binaries aren't code-signed yet, so Gatekeeper will block them on first run. Right-click → Open, or `xattr -d com.apple.quarantine ./embarch`.

`setup` figures out which row of §2 you're on, installs Core as a service that starts at boot, makes sure the shared auth token exists, prints (but does not run) the `PATH` line from §3.1 below, and finishes by running `doctor`.

**Core stays running from now on.** It starts at boot; you don't launch it, and neither does the agent. That's the whole reason there's nothing to "start up" every morning.

### 3.1 Add the binaries to your PATH

**Fixed in source 2026-08-17 (`embarch-umbrella/design.md` §3 decision 28), not yet in a released binary.** Once the release you downloaded includes it, `setup` copies `embarch`/`embarch-core`/`embarch-api` to a canonical per-user location (`~/.local/share/embarch/bin` on Linux/macOS/WSL2, `%LOCALAPPDATA%\embarch\bin` on Windows) and adds it to `PATH` for real — no manual step, nothing printed to translate by hand. A brand-new shell picks it up automatically; a shell already open when `setup` ran still needs restarting, since that's an OS-level constraint no installer works around.

**If your release predates that fix**, `setup` only prints the line to add, and prints it as POSIX `export PATH=...` syntax unconditionally — including on native Windows `cmd.exe`, where that line isn't valid (`export` isn't a `cmd.exe` builtin). Translate it by hand for the shell you're actually in:

```sh
export PATH="<dir>:$PATH"          # bash/zsh (Linux, macOS, WSL2) — usable as printed
```
```powershell
$env:Path += ";<dir>"              # PowerShell, current session only
```

On native Windows, the durable fix is the **System Properties → Environment Variables** GUI (`sysdm.cpl` → Advanced → Environment Variables), adding `<dir>` to your user `Path` — a `setx`/registry edit from a script risks truncating an already-long `PATH`, so the GUI is the safer default here. Until you've done that, just run the binaries from inside the unpacked directory instead of relying on `PATH`.

## 4. Check it worked

```sh
embarch doctor
```

Every line is a check, and every failure comes with the command that fixes it. Run this any time something behaves oddly — it's the first thing to try, always.

For a quick "is the stack alive," use the cheap version — a fast, unauthenticated reachability check, not the full picture:

```sh
embarch status
# Core: up at http://127.0.0.1:4884 (local)
#   auth: not checked (this probe is unauthenticated)
```

Probe count, model, and dev-bench connection aren't `status`'s job — those need an authenticated call, and only `doctor` (checks 5 and 12) makes one.

Both accept `--json` if you want to script against them.

## 5. Add your firmware project

From inside your firmware repo:

```sh
cd ~/src/my-firmware
embarch init
```

That creates an `embarch/` folder in your repo, holding just `embarch.toml` at first:

```
my-firmware/
└── embarch/
    └── embarch.toml     what your project is and how to build it
```

`embarch/build/` — EmbArch's own build directory — isn't created by `init`. It shows up the first time you actually build (`west` creates it); an empty directory at that path would be a lie about having built something.

Three things worth knowing about what just happened:

- **Nothing tracked by your repo was modified.** The `embarch/` folder is excluded via `.git/info/exclude`, which is local to your clone — your repo's committed `.gitignore` is untouched, and `git status` stays clean. Safe to run in a repo you don't own. `embarch init --uninstall` reverses everything.
- **EmbArch builds into its own directory** (`embarch/build/`), separate from wherever your interactive `west build` goes. Without this, you and EmbArch clobber each other's build tree — different board revisions, different pristine-vs-incremental state — and you spend an afternoon confused.
- **Your project is scoped to this repo.** An agent working in this repo can only see and flash this repo's project, not the unrelated board on your other USB port.

### 5.1 Finish the config

**If your repo has one board, skip to here.** If `init` detected a Zephyr/west project with `boards/*/*.yml` and picked `discovery = "zephyr-west"` instead — you'll see that field in the generated `embarch.toml`, and no `chip`/`build_command`/`artifact_path` fields at all — read [§5.2](#52-multi-board--zephyrwest-repos) instead; this section's placeholder-filling steps don't apply to that schema.

`init` derives what it safely can and leaves the rest as placeholders. Open `embarch/embarch.toml`:

```toml
[core]
base_url = "auto"          # don't replace this with an IP — see below

[[projects]]
name = "my-firmware"
source_path = "/home/me/src/my-firmware"
build_command = ["west", "build", "-b", "my_board", "--build-dir", "embarch/build", "app/firmware"]
artifact_path = "embarch/build/zephyr/zephyr.hex"
chip = "CHANGE-ME"    # <- you have to fill this in; init leaves this exact placeholder
flash_format = "hex"
build_timeout_secs = 900
```

On Windows+WSL2 specifically, `init` also writes an `artifact_path_for_core` line automatically — the `\\wsl.localhost\...` form of the same artifact, for the Windows-side Core to read (see [§8](#8-when-something-breaks)'s "Flash fails with a path error" row). You'll see it in the generated file even though it isn't in the example above.

**`chip`** is a **probe-rs** target name, which is *not* the same as your Zephyr board name — `roadrunner@1/nrf54l15/cpuapp` is a board, `nRF54L15` is a chip. There's no mechanical mapping between the two, so EmbArch won't guess: a wrong guess would flash the wrong target instead of erroring. Find yours with the probe-rs CLI (`cargo install probe-rs-tools`, once):

```sh
probe-rs chip list | grep -i nrf54
```

**`base_url = "auto"`** means "find Core wherever it is, every time." Leave it alone. If you're on WSL2 and tempted to write in the gateway IP you found with `ip route`: don't — that IP changes every time WSL2 restarts, and hardcoding it is a bug you'll rediscover in two weeks. `auto` re-checks on every invocation.

**`build_command`** is an argv array with no shell involved. If your build genuinely needs shell features — activating a venv, chaining with `&&` — use the escape hatch explicitly:

```toml
build_command = ["bash", "-lc", "source .venv/bin/activate && west build ..."]
```

And if `west` isn't on your `PATH` (common when it lives in a workspace venv), give the absolute path to it rather than fighting your environment.

> **The one trap worth knowing about.** `west`'s build directory is relative to *the directory west runs in*, not to the app path you pass it. If your real invocation is `west build -b <board> app/firmware` run from the repo root, then the output lands in `<repo-root>/build`, **not** `<repo-root>/app/firmware/build`. Get this wrong and EmbArch reports a "fresh" artifact that's actually a stale leftover — the worst possible failure during hardware bring-up. `init` reads your repo's `build/build_info.yml` (which west writes, recording the exact command it ran) to get this right automatically when you've built at least once. If you're editing by hand, check that file rather than assuming. Passing `--build-dir` explicitly, as `init` does, sidesteps the question entirely.

Then re-check:

```sh
embarch doctor
```

### 5.2 Multi-board / Zephyr-west repos

Some real firmware repos don't have one board — they have several real boards, each with several variants, some of which only have real hardware-revision overlays for *some* revisions, not every one their `board.yml` declares. A hand-written, single `chip`/`board` config can't represent that safely: it either picks one board and hides the rest, or risks silently building against a revision that has no real overlay and falls back to un-revisioned base files without telling you. `discovery = "zephyr-west"` exists for exactly this shape.

`init` picks this schema automatically when your repo looks like a Zephyr/west project — you don't ask for it. The config it writes is deliberately smaller than §5.1's:

```toml
[[projects]]
name = "my-firmware"
source_path = "/home/me/src/my-firmware"
discovery = "zephyr-west"
west_binary = "/path/to/.venv/bin/west"   # or bare "west" on PATH, with a warning if init had to guess
build_dir_root = "embarch/build"
flash_format = "hex"
build_timeout_secs = 900
```

No `chip`, `build_command`, or `artifact_path` — there's nowhere safe to write those down once a repo has more than one real board. Instead, every board/variant/revision/app combination is scanned live, off `boards/`/`app/` on disk, on every call — never cached, so it can't go stale the way a hand-maintained entry would.

**See what's actually there:**

```sh
embarch-api list-targets my-firmware
```

Prints every combination that's file-backing-validated right now — not just what `board.yml` *declares*, but what actually has the files a build needs. This is the step that would have caught, for example, a revision overlay that only exists for one variant out of four.

**Pick one.** `build`/`flash`/`build-and-flash`/`reset` all take the same four optional selection flags:

```sh
embarch-api build-and-flash my-firmware --board roadrunner --variant os_5led --revision evt1
```

- Give enough of `--board`/`--variant`/`--revision`/`--app` to narrow the live-scanned set to **exactly one** match, and the call proceeds.
- Give a combination that still matches **more than one** — the call errors instead of guessing, and the error lists the narrowed remainder so you can see what's left to disambiguate.
- Give **none of the four** and it lists everything `list-targets` would, rather than guessing a default — unless the project sets `default_target` (§4 of `embarch-api/design.md`), in which case that's the fallback, still overridable per-field on any individual call.
- `--snippet <name>` and `--extra-arg <flag>` (both repeatable) layer on top of a resolved target — additive, not narrowing. Omit them to fall back to the project's `default_snippets`/`default_extra_args`; pass `--snippet none` on its own to force zero snippets regardless of the default.
- `flash --firmware-path <path>` still needs enough of the four selection flags to resolve a **chip** — the override only bypasses picking *which build*, not chip resolution, since a `zephyr-west` project has no stored chip to fall back to either.

**No interactive picker exists.** `list-targets` shows you the options; you re-run the command with more flags. There's nothing to click or number-select.

`embarch doctor` check 8 for this schema is `list-targets`'s own count being nonzero — if it's failing, its fix output is the same listing `list-targets` would print, not a separate scan.

Then re-check:

```sh
embarch doctor
```

## 6. Using it yourself, from a terminal

Every invocation needs to know which config file to use — there's no auto-discovery the way `doctor`/`init` have. Point at it once per shell with `EMBARCH_API_CONFIG`, or pass `--config` every time:

```sh
export EMBARCH_API_CONFIG=~/src/my-firmware/embarch/embarch.toml

embarch-api list-projects                    # what's configured
embarch-api status                           # is Core up, what probes does it see
embarch-api build my-firmware                # just build
embarch-api flash my-firmware                # flash the configured artifact
embarch-api build-and-flash my-firmware      # build, then flash only if the build succeeded
embarch-api reset my-firmware
embarch-api serial-log my-firmware --duration-ms 5000
```

Without either, every one of these — including `list-projects` — exits immediately with `no config path given: pass --config <path> or set EMBARCH_API_CONFIG`.

**Note the naming split**: CLI subcommands are kebab-case (`list-projects`, `build-and-flash`, `serial-log`), while the MCP tools in §7 are snake_case (`list_projects`, `build_and_flash`, `serial_log`). Each front-end follows its own convention; `--help` is authoritative.

Add `--json` to any of them for machine-readable output — useful if you're wrapping this in a script or a `west flash` replacement.

Why all three of `build`, `flash`, and `build_and_flash` exist: `build_and_flash` is what you want most of the time, and it refuses to flash a stale or failed artifact. But iterating on compiler errors shouldn't touch hardware every time (`build`), and re-flashing the same binary after a manual board reset shouldn't rebuild (`flash`).

Flashing a one-off file that isn't your configured artifact:

```sh
embarch-api flash my-firmware --firmware-path /path/to/some.hex
```

**Failures print the full error chain**, not just a summary line — the actual cause (a probe I/O error, a path Core couldn't open) is usually several lines down. Read the whole thing.

## 7. Using it from Claude Code

`embarch init` already registered the MCP server for this repo, at local scope — nothing was written into the repo for your teammates to trip over. Open Claude Code in the repo and the tools are there: `list_projects`, `status`, `build`, `flash`, `build_and_flash`, `reset`, `serial_log`.

You don't call them by name. You say what you want:

- *"Build this and flash it to the board."*
- *"Flash it, then show me the serial log for the first 5 seconds after reset."*
- *"This won't compile — build it and fix the errors."* ← the one that pays for the whole setup, because the agent sees the real compiler output and iterates without you relaying it.
- *"The device isn't advertising after boot. Flash the current build and read the console."*

### 7.1 Which operations should need your approval

Reading and building are safe and frequent; anything that touches the board should be a decision you make. A reasonable split in `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__embarch__list_projects",
      "mcp__embarch__status",
      "mcp__embarch__build",
      "mcp__embarch__serial_log"
    ],
    "ask": [
      "mcp__embarch__flash",
      "mcp__embarch__build_and_flash",
      "mcp__embarch__reset"
    ]
  }
}
```

If your `CLAUDE.md` tells the agent never to build firmware on its own — a sensible rule when a stray `west build` can blow away a build tree — note the exemption explicitly, or the agent will keep asking:

```markdown
Never build firmware or flash devices autonomously — ask me to run it.
  Exception: builds routed through EmbArch's `build` tool, which uses its own
  build directory and can't disturb my interactive build tree.
```

## 8. When something breaks

Run `embarch doctor` first. It checks these in order and tells you the fix. What each failure actually means:

| What you see | What it means |
|---|---|
| **Core unreachable** | Core isn't running, or isn't reachable from here. Try `embarch up`. On Windows+WSL2, check Core is running on the *Windows* side — WSL2 restarts don't restart it, but they do change the address, which is why `base_url` must stay `"auto"` |
| **401 Unauthorized** | Core *is* running — the auth token doesn't match. Different problem, different fix: see [§9](#9-the-token) |
| **No probes found** | The probe isn't plugged in, or the OS hasn't enumerated it. Check it appears in Device Manager / `lsusb` on the machine **Core** runs on, not the one you're typing on |
| **`chip` is still a placeholder** | [§5.1](#51-finish-the-config) — fill it in from `probe-rs chip list` |
| **`build_command[0]` not found** | Your toolchain isn't on the `PATH` the API inherits. Use an absolute path in `build_command` rather than trying to fix the environment |
| **Artifact not fresh** | The build succeeded but didn't write where `artifact_path` says. Almost always the west build-directory trap in [§5.1](#51-finish-the-config) |
| **Flash fails with a path error** | Core reads the firmware file from **its own** disk. On Windows+WSL2 that needs `artifact_path_for_core` — the `\\wsl.localhost\...` form of the same file. `init` sets this; `doctor` verifies both paths name the same file |
| **Flashing on a separate-box Core** | Not a bug, not fixable today. There's no way to get the artifact's bytes onto a remote Core's filesystem. Status, reset, and serial work; flashing doesn't |
| **Wrong board flashed** | You're past what EmbArch checks. `chip` is passed to probe-rs verbatim, and only one probe is supported — the first one found. Unplug the other one |

## 9. The token

Core protects its endpoints with a single shared secret, and in the normal case **you never see or handle it**: Core generates one on first start and writes it to a machine-wide file (`%ProgramData%\embarch\token` on Windows, `/var/lib/embarch/token` on Linux/macOS), and `embarch-api` finds that file on its own — including across the WSL2⟷Windows boundary, since that's one physical machine with one filesystem to reach.

The exception is a Core on a separate box: no shared filesystem, so no discovery. Copy the value across by hand once:

```sh
export EMBARCH_TOKEN=<the contents of the token file on the Core machine>
```

`embarch doctor` prints the exact line for you. To rotate: delete the token file, restart Core, restart anything talking to it. Full detail — storage, permissions, threat model, what this does and doesn't protect against — is in [embarch-token.md](embarch-token.md). Worth knowing: **there's no TLS**, so the token crosses your network in cleartext. Fine on localhost or a WSL2 loopback; think twice on a shared wifi.

## 10. Dev bench and studies

> **Not usable yet.** The pieces exist and compile, but no board has ever been flashed with this firmware and none of the endpoints below are implemented. This chapter is here so you know what's coming, not so you can follow it. Progress: [embarch-roadmap.md](embarch-roadmap.md)'s Next bucket.

`embarch-dev-bench` is a second board — a **test fixture**, not your DUT — that plays your device's BLE counterpart on demand. Instead of manually pairing with a phone to check whether your peripheral advertises correctly, you describe what should happen and the bench does it, reproducibly, every build.

The unit of work is a **Study**: an ordered list of steps, each a BLE action (advertise, connect as central or peripheral, read/write/notify/indicate/subscribe a GATT characteristic, capture a stream) or a power-sampling window, with pass/fail checks. You'll submit one and poll it:

```sh
embarch-api run_study --study-file my-study.json     # returns a study_id
embarch-api study_status <study_id>                  # pending | running | completed | failed
```

Where it plugs in: your DUT keeps its own probe on Core, and the bench connects to Core over a **second, separate serial link**. Core auto-detects which port the bench is on (it's already implemented — `embarch-core detect-dev-bench`). One dev bench, one DUT, one study at a time; testing two DUTs means two independent Core+bench pairs.

What's genuinely not there yet: the `/study*` endpoints in Core, `run_study`/`study_status` in the API, power-sampling hardware (no BOM decision yet), GPIO/analog stimulus, and any physical DUT connector. Today it's BLE-proximity-only, and only in principle.

Flashing the bench itself is a plain `west flash` you run by hand — Core's probe access is scoped to your DUT and deliberately has no business reflashing the fixture that's testing it.

## 11. Working on EmbArch itself

Skip this unless you're changing EmbArch, not just using it. Everything above needs only the release archive.

All the repos live as siblings under one parent — the docs cross-reference each other by relative path, so this layout matters:

```
embarch/
├── embarch-core/              Rust · probe-rs, Axum · the hardware service
├── embarch-api/               Rust · rmcp, reqwest · MCP server + CLI + build orchestrator
├── embarch-umbrella/          Rust · the `embarch` binary (this guide's chapters 3–5)
├── embarch-study-designer/    Rust · no_std shared study data types
├── embarch-dev-bench/         C · Zephyr firmware for the bench, multiple west workspaces
└── embarch-doc/               these docs
```

Build any of the Rust ones the obvious way — a plain `cargo build` (no `--release`) is enough for day-to-day iteration; reach for `--release` only when actually producing something you'll run day-to-day or ship, not for every edit-compile-test cycle:

```sh
cargo build
cargo clippy --all-targets -- -D warnings      # expected clean before you commit
cargo test
```

**Iterating across repos — wiring a dev `embarch-core`/`embarch-api`/`embarch-umbrella` together, or safely testing an `embarch-umbrella` change without it overwriting your real install** — is its own doc: [embarch-dev-workflow.md](embarch-dev-workflow.md).

Platform notes that will cost you time otherwise:
- **Building on Windows natively needs Visual Studio Build Tools' "Desktop development with C++" workload** — a `rustup`-installed toolchain alone has no linker for the MSVC target.
- **Don't build Core from a `\\wsl$`-mounted source tree.** Use a native Windows checkout.
- `embarch-dev-bench` is Zephyr C, not Rust, and needs a west workspace per vendor — see its own [design doc](embarch-dev-bench/design.md) §2.

**Docs are part of the work, not a follow-up.** Each sub-project's `design.md` in `embarch-doc` is the source of truth for its architecture, and it gets updated in the same pass as the code that changes it — see [DOC-PROTOCOL.md](DOC-PROTOCOL.md). If you're using Claude Code in one of these repos, its `CLAUDE.md` already points there and it'll do this on its own.

## 12. Where to look next

- [embarch.md](embarch.md) — what the suite is, how the pieces fit, the sub-project index
- [embarch-roadmap.md](embarch-roadmap.md) — what's coming, in what order
- [embarch-features.md](embarch-features.md) — every feature and how far it's actually verified. Worth reading before relying on something: "shipped" and "validated against real hardware" are tracked separately, on purpose
- [embarch-token.md](embarch-token.md) — the auth token's full lifecycle
- A specific component: `embarch-core/design.md`, `embarch-api/design.md`, `embarch-umbrella/design.md`, and so on

---

## Appendix A — the pre-release manual path

Milestone 6 (Onboarding) shipped in `v0.1.0` — a real release archive and `embarch` binary exist now, and chapters 3–9 are the real, current procedure. This appendix is what the manual procedure looked like before that, for the Windows-Core + WSL2-API topology, kept for reference rather than deleted outright. Everything in it is now absorbed by `embarch setup`/`init`, except the one gap that's still genuinely manual: a separate-box Core has no shared filesystem for token discovery, so §9's "copy the token by hand" step still applies there.

1. **Clone the repos** as siblings under one `embarch/` parent (§11's layout), plus `embarch-doc`.

2. **Build Core natively on Windows** — a native checkout, not `\\wsl$`, and with the VS Build Tools C++ workload installed:
   ```
   cargo build --release
   ```

3. **Install and start Core**, from an elevated Windows shell:
   ```
   embarch-core.exe install
   ```
   Confirm it generated a token at `C:\ProgramData\embarch\token`. Core's default bind is `0.0.0.0:4884` — deliberately, so WSL2 can reach it.

4. **Build the API in WSL2**: `cargo build --release` in `embarch-api`.

5. **Find Core's address from WSL2.** `base_url = "auto"` doesn't exist yet, so you have to do this by hand:
   ```sh
   ip route show default | awk '{print $3}'
   ```
   That's your Windows host gateway IP. **It changes when WSL2 restarts**, and you'll have to redo this step when it does — this is the single most annoying thing about the current setup and the main reason `auto` is being built.

6. **Write the config by hand.** Copy `embarch-api/config.example.toml` and edit it. Set `base_url` to `http://<that IP>:4884`. Leave `token`/`token_env` unset — token-file discovery handles WSL2⟷Windows translation on its own. For each project set `source_path`, `build_command` (absolute path to `west` if it's in a venv), `artifact_path`, `chip` (from `probe-rs chip list`), and `flash_format`.

7. **Set `artifact_path_for_core`** — the `\\wsl.localhost\<distro>\...` form of the same artifact file, because Core reads the file from the Windows side. Verify it resolves to the same file rather than assuming; the path is not always where you'd guess (see §5.1's build-directory trap).

8. **Verify by hand**, in this order — each step isolates a different failure:
   ```sh
   embarch-api --config <path> list-projects     # config loads at all (no Core needed)
   embarch-api --config <path> status            # Core reachable and token accepted
   embarch-api --config <path> build <project>   # build works, artifact is fresh
   embarch-api --config <path> build-and-flash <project>
   ```

9. **Register the MCP server** for your firmware repo:
   ```sh
   claude mcp add embarch -- <abs path>/embarch-api --config <abs path>/embarch/embarch.toml
   ```
   Default scope is local to you, so nothing lands in the repo.

10. **Keep the config out of the repo yourself** — add `embarch/` to `.git/info/exclude` rather than the committed `.gitignore`, especially in a repo you don't own.

## Changelog

- 2026-08-17 — §11: `cargo build --release` changed to plain `cargo build` for day-to-day iteration (release mode is for actually shipping something, not every edit-compile-test cycle), and added a pointer to the new [embarch-dev-workflow.md](embarch-dev-workflow.md) — §11 told you to build each repo independently but never said how to wire a dev `embarch-api` to a dev `embarch-core`, or how to test an `embarch-umbrella` change without it overwriting a real install.
- 2026-08-17 — §3.1 updated for decision 28 (`embarch-umbrella/design.md` §3): the manual PATH-hint-translation workaround is now marked as a stopgap for releases predating that fix, with the real (source-implemented, not yet released) behavior — `setup` copies binaries to a canonical location and edits PATH for real — described as what a future release will do automatically.
- 2026-08-17 — Real Windows+WSL2 onboarding attempt surfaced three more real gaps in §3: (1) "download one archive" didn't say a WSL2 setup needs *two* — the Windows archive on Windows, a separate Linux archive unpacked inside WSL2 itself — leading directly to `embarch: command not found` when the Windows `.exe`s were tried from WSL2 via `/mnt/c`; (2) nothing explained that `Topology: local` from the correct first (Windows) leg is expected, not the already-documented wrong-order trap — indistinguishable from it without this note; (3) §3 claimed `setup` "puts `embarch-core` and `embarch-api` on your PATH," contradicted by `setup`'s own real output ("setup does not edit it for you") — corrected, and new §3.1 documents the printed hint plus the fact that it's POSIX-only even on native Windows `cmd.exe` (a real code gap, tracked in `embarch-umbrella/design.md` §10, not just a doc fix).
- 2026-08-17 — §3's install step gave one Unix-shell command (`./embarch setup`) for every platform; on Windows `cmd.exe` this fails outright (`'.' is not recognized...`) since `cmd.exe` doesn't understand `./`. Split into three explicit per-shell command blocks (`cmd.exe`, PowerShell, Linux/macOS). Found live — first real Windows user to reach this step hit it immediately.
- 2026-08-17 — Fixed a real staleness gap: the opening callout and Appendix A's intro still said the `embarch` setup tool was "designed but not yet built" and told readers to use the manual path — false since Milestone 6 (Onboarding) shipped real `v0.1.0` release binaries (`embarch-roadmap.md`'s Shipped foundation). Both now point at chapters 3–9 as the real, current procedure; Appendix A is relabeled as historical/reference. `embarch.md` §3's `embarch-umbrella` row (`In progress`) was disagreeing with this same fact and is corrected to `Shipped` in the same pass. Found while scoping Milestone 1 execution — the user's stated plan was to follow this guide directly, which would have hit this immediately.
- 2026-08-17 — Added §5.2 (Multi-board / Zephyr-west repos): the guide had never been updated for `discovery = "zephyr-west"` (`embarch-api/design.md` §3 decision 12, shipped 2026-08-14) even though it's exactly the shape the real `eight-sleep-healthband-fw` repo turned out to have (`embarch-umbrella/milestone-6.md`'s 2026-08-13 finding — four real boards, revision overlays only at `evt1`). Following old §5.1 literally on a repo like that would walk into the same "wrong board picked" trap Milestone 6 already hit. §5.1 now points here when `init` writes the smaller `zephyr-west` schema instead of the static one. Found while scoping [embarch-roadmap.md](embarch-roadmap.md)'s Milestone 1 execution ([embarch-api/milestone-7.md](embarch-api/milestone-7.md)).
- 2026-08-05 — Replaced the placeholder with the real getting-started guide, written for a firmware engineer new to EmbArch and written *ahead of* the `embarch` setup tool it describes, so it serves as [Milestone 6](embarch-roadmap.md#6---onboarding)'s specification and acceptance criteria ([embarch-umbrella/design.md](embarch-umbrella/design.md) §11). Appendix A carries the manual procedure that actually works today and is expected to shrink as that milestone lands. Both of `embarch-api`'s front-ends are presented as peers (§1, §6, §7) rather than treating the CLI as secondary to the agent path. Dev bench and studies are included per request but clearly marked unusable (§10).
