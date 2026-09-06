# EmbArch: getting started

**Status:** active, 2026-09-02. For a firmware engineer who has never used EmbArch.

This describes the real, released binaries. If you are setting up a machine right now, this is the path to follow.

## 1. What EmbArch gives you

EmbArch lets you build and flash your firmware, reset your board, and read its serial console **from wherever your code lives** — including from an AI coding agent — **without fighting over who owns the USB port.**

The concrete problem it was built for: your firmware builds in WSL2, but your debug probe is a Windows USB device, and forwarding USB into WSL2 is miserable. **EmbArch splits the job in two so the boundary stops mattering.**

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

Typing the command yourself is often faster; **the agent path matters when the agent needs to see a compiler error or a serial log to fix its own change.**

## 2. Pick your setup

Find your row. You configure none of this — setup detects it — but it tells you what to expect.

| Your machine | Core runs | API runs | Status |
|---|---|---|---|
| **Windows + WSL2**: code in WSL2, probe on Windows | Windows, natively | WSL2 | **Best supported.** The topology in daily use |
| **Mac**: everything on the Mac | macOS | macOS | Supported, **never tested on a real Mac** |
| **Linux**: everything on one box | Linux | Linux | Supported, mechanically simplest |
| **Windows only**, no WSL2 | Windows | Windows | Supported, untested |
| **Probe on a separate box** (a Pi on your wifi) | that box | your laptop | **Partial** — status, reset and serial work; flashing needs the artifact uploaded, see §8 |

Prerequisites, all topologies:

- **A debug probe your board supports** — J-Link, ST-Link, CMSIS-DAP and FTDI all work, as does an on-board debugger like a DK's.
- **Your existing firmware toolchain, working.** EmbArch runs *your* build command; it does not install or replace `west`, `idf.py`, or anything else.
- **An elevated shell, once**, to install Core as a service that starts at boot: Administrator on Windows, root on Linux and macOS. **Every OS needs this — it is what installing a system service costs — and it is the only step that ever does.**

## 3. Install

Download **one archive per operating system you are setting up** from [embarch-umbrella releases](https://github.com/gabrieltetar/embarch-umbrella/releases). Each contains all three binaries as a **version-tested set**, built for that one OS.

**On Windows + WSL2 this means two archives, not one** — the Windows `.zip` *and* the Linux `.tar.gz` — **because WSL2 is a separate Linux environment, not another shell into the same binaries.** Unpack the Windows one on the Windows filesystem, and the Linux one **inside WSL2's own filesystem** (your WSL2 home, not a `/mnt/c/...` path). Running the Windows executables from WSL2 through interop is not the intended flow and will not work: **the WSL2-side API has to run as a native Linux process.**

Then, from the unpacked directory, in an elevated shell:

```sh
./embarch setup          # Linux, macOS
embarch setup            :: Windows cmd.exe — no ./ prefix
.\embarch setup           # Windows PowerShell
```

**On Windows + WSL2, run it twice, in this order:** the elevated Windows shell first, against the Windows archive — that installs and starts Core — then inside WSL2 against the **Linux** archive, which sets up the API side and finds the Core you just started.

**Order matters, and getting it backwards has a confusing symptom.** Run the WSL2 leg first — easy, if that is the shell you already have open — and with no Core installed anywhere, `setup` cannot tell your machine from a plain single-OS one: it reports `Topology: local` and fails with `embarch-core: not found`, **which does not point you back at the Windows-first step.** If you see that, it is this trap and not a broken archive.

**`Topology: local` from the elevated Windows leg itself, with no failure alongside it, is expected.** From native Windows alone, before the WSL2 leg has run, **`setup` has no way to see that a WSL2 side exists at all.** Confirm Core started and the token file is present, then run the WSL2 leg — that is the step that reports the real topology.

**On macOS the binaries are not code-signed yet**, so Gatekeeper blocks them on first run: right-click → Open, or `xattr -d com.apple.quarantine ./embarch`.

`setup` works out which row of §2 you are on, installs Core as a boot service, ensures the shared token exists, puts the binaries on your `PATH`, and finishes by running `doctor`.

**Core stays running from now on.** It starts at boot; you do not launch it, and neither does the agent. **That is the whole reason there is nothing to start up every morning.**

**One `PATH` caveat depending on how old your release is.** Current `setup` copies the three binaries to a canonical per-user location and edits `PATH` for real. **A release predating that only *prints* the line — and prints it in POSIX `export` syntax unconditionally, including on `cmd.exe` where it is not valid.** Translate it for the shell you are in (`$env:Path += ";<dir>"` in PowerShell), or on native Windows use **System Properties → Environment Variables** to add it durably — **a scripted registry edit risks truncating an already-long `PATH`.** Either way, **a shell that was already open when `setup` ran still needs restarting**, which is an OS constraint no installer works around.

## 4. Check it worked

```sh
embarch doctor
```

**Every line is a check, and every failure comes with the command that fixes it.** Run it any time something behaves oddly — it is the first thing to try, always.

For a quick "is the stack alive", use the cheap version:

```sh
embarch status
# Core: up at http://127.0.0.1:4884 (local)
#   auth: not checked (this probe is unauthenticated)
```

**Probe count, model and bench connection are not `status`'s job** — those need an authenticated call, and only `doctor` makes one. Both accept `--json`.

## 5. Add your firmware project

From inside your firmware repo:

```sh
cd ~/src/my-firmware
embarch init
```

That creates an `embarch/` folder holding `embarch.toml`. **`embarch/build/` is not created** — it appears the first time you actually build, because **an empty directory at that path would be a lie about having built something.**

Three things worth knowing about what just happened:

- **Nothing tracked by your repo was modified.** The folder is excluded via `.git/info/exclude`, local to your clone — your committed ignore file is untouched and `git status` stays clean. **Safe to run in a repo you do not own.** `embarch init --uninstall` reverses everything.
- **EmbArch builds into its own directory**, separate from wherever your interactive `west build` goes. **Without this, you and EmbArch clobber each other's build tree** — different board revisions, different pristine-vs-incremental state — and you spend an afternoon confused.
- **Your project is scoped to this repo.** An agent working here can only see and flash this repo's project, **not the unrelated board on your other USB port.**

### 5.1 Finish the config

**If `init` detected a Zephyr/west repo it wrote a smaller, discovery-based config with no `chip` or `build_command` at all — skip to §5.2.** Otherwise it derived what it safely could and left the rest as placeholders:

```toml
[core]
base_url = "auto"          # don't replace this with an IP — see below

[[projects]]
name = "my-firmware"
source_path = "/home/me/src/my-firmware"
build_command = ["west", "build", "-b", "my_board", "--build-dir", "embarch/build", "app/firmware"]
artifact_path = "embarch/build/zephyr/zephyr.hex"
chip = "CHANGE-ME"    # <- you have to fill this in
flash_format = "hex"
build_timeout_secs = 900
```

**`chip` is a probe-rs target name, which is not your Zephyr board name** — `roadrunner@1/nrf54l15/cpuapp` is a board, `nRF54L15` is a chip. **There is no mechanical mapping between the two, so EmbArch will not guess: a wrong guess would flash the wrong target instead of erroring.** Find yours with `embarch-core chip-list nrf54`, which needs no extra tooling.

**`base_url = "auto"` means "find Core wherever it is, every time". Leave it alone.** If you are on WSL2 and tempted to write in the gateway IP you found with `ip route`: **don't — that IP changes every time WSL2 restarts, and hardcoding it is a bug you will rediscover in two weeks.**

**`build_command` is an argv array with no shell involved.** If your build genuinely needs shell features, use the escape hatch explicitly: `["bash", "-lc", "source .venv/bin/activate && west build ..."]`. And if `west` is not on the `PATH` the API inherits — common when it lives in a workspace venv — **give the absolute path rather than fighting your environment.**

> **The one trap worth knowing about.** `west`'s build directory is relative to **the directory west runs in**, not to the app path you pass it. If your real invocation is `west build -b <board> app/firmware` from the repo root, the output lands in `<repo-root>/build`, **not** `<repo-root>/app/firmware/build`. Get this wrong and **EmbArch reports a "fresh" artifact that is actually a stale leftover — the worst possible failure during hardware bring-up.** `init` reads the metadata west itself writes to get this right when you have built at least once. Passing an explicit build directory, as `init` does, sidesteps the question entirely.

Then re-run `embarch doctor`.

### 5.2 Multi-board and Zephyr-west repos

Some real firmware repos do not have one board — **they have several real boards, each with several variants, some of which only have real hardware-revision overlays for *some* revisions, not every one their board file declares.** A single hand-written config cannot represent that safely: **it either picks one board and hides the rest, or risks silently building against a revision that has no real overlay and falls back to un-revisioned base files without telling you.**

`init` picks this schema automatically; you do not ask for it. It writes a source path, the `west` binary, a build-directory root, the flash format and a timeout — **and no `chip`, `build_command` or `artifact_path`, because there is nowhere safe to write those down once a repo has more than one real board.** Every board/variant/revision/app combination is **scanned live on every call, never cached, so it cannot go stale.**

**See what is actually there:**

```sh
embarch-api list-targets my-firmware
```

That prints every combination that is **file-backing-validated right now** — not what the board file *declares*, but what actually has the files a build needs. **This is the step that catches a revision overlay existing for only one variant out of four.**

**Then pick one.** `build`, `flash`, `build-and-flash` and `reset` all take the same four optional selection flags:

```sh
embarch-api build-and-flash my-firmware --board roadrunner --variant os_5led --revision evt1
```

- Narrow to **exactly one** match and the call proceeds.
- Match **more than one** and the call **errors instead of guessing**, listing the narrowed remainder.
- Give **none** and it lists everything, rather than guessing a default.
- `--snippet` and `--extra-arg` (both repeatable) layer on top of a resolved target — **additive, not narrowing.** Omitting `--snippet` uses the project's `default_snippets`; **`--snippet none`, alone, forces zero snippets** over that default (2026-09-04). Mixing the literal with real snippet names, or using it where the app genuinely declares a snippet called `none`, is refused naming the ambiguity rather than guessed at.
- **`[projects.default_target]`** gives a `zephyr-west` project a base board/variant/revision/app selection, and a call narrows it **per field** — so overriding the revision does not make you restate the other three. An error names which axes came from the default, and `list-targets` reports it. **Not accepted for a `static` project — and since 2026-09-05 nor are `default_snippets`, `default_extra_args`, `west_binary` or `build_dir_root`**: all five now fail at *config load*, in one message naming every one you set, rather than four of them loading silently into a project that can never honour them.
- **All six of these flags are for a `zephyr-west` project.** Pass any of them to a `discovery = "static"` project and the call now **fails naming which were given** (`embarch-api` decision 51) — until 2026-09-03 they were accepted, discarded, and the build reported success.
- `flash --firmware-path` still needs enough flags to resolve a **chip**: the override bypasses picking which *build*, not chip resolution.

**There is no interactive picker.** `list-targets` shows the options; you re-run with more flags.

## 6. Using it yourself, from a terminal

**Every invocation needs to know which config to use — there is no auto-discovery the way `doctor` and `init` have.** Point at it once per shell, or pass `--config` every time:

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

Without either, **every one of these — including `list-projects` — exits immediately** with `no config path given`.

**Note the naming split**: CLI subcommands are kebab-case, the MCP tools in §7 are snake_case. Each front end follows its own convention; `--help` is authoritative. Add `--json` to any of them for machine-readable output.

**Why all three of build, flash and build-and-flash exist:** the combined one is what you want most of the time, and **it refuses to flash a stale or failed artifact.** But **iterating on compiler errors should not touch hardware every time**, and **re-flashing the same binary after a manual board reset should not rebuild.**

**Failures print the full error chain**, not just a summary line — **the actual cause is usually several lines down. Read the whole thing.**

## 7. Using it from Claude Code

`embarch init` already registered the MCP server for this repo, at local scope — **nothing was written into the repo for your teammates to trip over.** Open Claude Code in the repo and the tools are there.

**You do not call them by name.** You say what you want:

- *"Build this and flash it to the board."*
- *"Flash it, then show me the serial log for the first 5 seconds after reset."*
- *"This won't compile — build it and fix the errors."* ← **the one that pays for the whole setup**, because the agent sees the real compiler output and iterates without you relaying it.

### 7.1 Which operations should need your approval

**Reading and building are safe and frequent; anything that touches the board should be a decision you make.** A reasonable split in `.claude/settings.local.json`: allow `list_projects`, `status`, `build` and `serial_log`; ask for `flash`, `build_and_flash` and `reset`.

If your `CLAUDE.md` tells the agent never to build firmware on its own — **a sensible rule when a stray `west build` can blow away a build tree** — note the exemption explicitly, or the agent will keep asking:

```markdown
Never build firmware or flash devices autonomously — ask me to run it.
  Exception: builds routed through EmbArch's `build` tool, which uses its own
  build directory and can't disturb my interactive build tree.
```

## 8. When something breaks

**Run `embarch doctor` first.** What each failure actually means:

| What you see | What it means |
|---|---|
| **Core unreachable** | Core is not running, or not reachable from here. Try `embarch up`. On Windows+WSL2, check Core is running on the *Windows* side — **WSL2 restarts do not restart it, but they do change the address, which is why `base_url` must stay `"auto"`** |
| **Core bound where you cannot reach it** | `doctor` check 17 says `bound-narrow`: Core **is** running, and its registered `--bind` is loopback. A WSL2 guest reaches its Windows host over the gateway and never over loopback, so nothing answers anywhere. `embarch up` will not fix this — reinstall elevated with `embarch-core install --bind 0.0.0.0`, or re-run `embarch setup`, which bakes the right address in. `bind-not-the-cause` means the bind is wide and the row above still applies |
| **401 Unauthorized** | Core *is* running and **the token does not match. Different problem, different fix** — see §9 |
| **No probes found** | Not plugged in, or the OS has not enumerated it. **Check it appears on the machine Core runs on, not the one you are typing on** |
| **`chip` is still a placeholder** | §5.1 — fill it in from `embarch-core chip-list` |
| **`build_command[0]` not found** | Your toolchain is not on the `PATH` the API inherits. **Use an absolute path rather than trying to fix the environment** |
| **Artifact not fresh** | The build succeeded but did not write where the config says. **Almost always §5.1's west build-directory trap** |
| **Flashing on a separate-box Core** | Works, by uploading the artifact's bytes rather than naming a path. If it fails, check the API can reach Core at all |
| **Wrong board flashed** | **You are past what EmbArch checks.** `chip` goes to the flashing backend verbatim, and only the first probe found is used unless you name one. Unplug the other one |
| **The bench's log is there but says nothing useful** | **By default the bench reports only warnings and errors** — a shared link is not the place for the BLE stack's full commentary. Re-run with `"dev_bench_log_level": "Info"` or `"Debug"` in the study, and **the bench turns the volume up for that run only.** The debug file records which level each study asked for, **so a quiet run is never ambiguous** |
| **A study fails and Core's log does not say why** | **Ask the bench.** `embarch-core dev-bench-logs --tail 100` prints what its own firmware logged over the link — its boot record, whatever the BT host complained about, and any fatal dump. **A short uptime in the handshake line means the bench rebooted, which used to be invisible.** Run it on the machine Core runs on |

## 9. The token

Core protects its endpoints with a single shared secret, and **in the normal case you never see or handle it**: Core generates one on first start and writes it to a machine-wide file, and `embarch-api` finds it on its own — **including across the WSL2⟷Windows boundary, since that is one physical machine with one filesystem to reach.**

**The exception is a Core on a separate box: no shared filesystem, so no discovery.** Copy the value across by hand once — `embarch doctor` prints the exact line. To rotate: delete the file, restart Core, restart anything talking to it. Full lifecycle: [embarch-token.md](../embarch-token.md).

**Worth knowing: there is no TLS**, so the token crosses your network in cleartext. **Fine on localhost or a WSL2 loopback; think twice on shared wifi.**


**Testing against a second board?** Studies, the dev bench, and capturing a DUT trace are their own guide: [studies-guide.md](studies-guide.md).

## 10. Working on EmbArch itself

**Skip this unless you are changing EmbArch, not just using it.** Everything above needs only the release archive.

All the repos live as siblings under one parent — **the docs cross-reference each other by relative path, so this layout matters.** Build any of the Rust ones with a plain `cargo build`; `cargo clippy --all-targets -- -D warnings` and `cargo test` are expected clean before you commit.

**Iterating across repos** — wiring a dev Core, API and umbrella together, or safely testing an umbrella change without it overwriting your real install — **is its own doc: [embarch-dev-workflow.md](../embarch-dev-workflow.md).** Its §4a covers the deploy direction: syncing, building and installing a Core change onto a real Windows service.

Two platform notes that will cost you time otherwise: **building on Windows natively needs Visual Studio Build Tools' "Desktop development with C++" workload** — a `rustup` toolchain alone has no linker for that target — and **do not build Core from a `\\wsl$`-mounted source tree**; use a native checkout.

**Docs are part of the work, not a follow-up.** Each sub-project's `spec.md` and `decisions.md` in `embarch-doc` are the source of truth for its architecture, **updated in the same pass as the code that changes them** — see [DOC-PROTOCOL.md](../DOC-PROTOCOL.md).

## 11. Where to look next

- [embarch.md](../embarch.md) — what the suite is, how the pieces fit, the sub-project index
- [suite/roadmap.md](roadmap.md) — what is coming, in what order
- [suite/features.md](features.md) — every feature and **how far it is actually verified.** Worth reading before relying on something: **"shipped" and "validated against real hardware" are tracked separately, on purpose**
- [embarch-token.md](../embarch-token.md) — the auth token's full lifecycle
- A specific component: its `spec.md` for what is true now, its `decisions.md` for why
