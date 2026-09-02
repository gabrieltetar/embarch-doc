# embarch: local dev workflow

**Status:** active, 2026-08-17. How to iterate on `embarch-core`/`embarch-api`/`embarch-umbrella` locally without cutting a release, and without a debug build silently touching a real machine's install — plus, since 2026-08-25, the opposite case: how a Core change actually reaches this machine's live Windows service (§4a).

## 1. Short answer

**No — never use a release build to develop against, and you rarely need `--release` at all for iteration.** A debug build (`cargo build`, no flag) is faster to compile and behaves identically for everything except raw speed. Reach for `--release` only when actually producing the thing you (or CI) will ship — the release-CI workflows already do this per-repo (`embarch-roadmap.md`'s Release section); it's not something a dev loop needs.

The three code-bearing repos — `embarch-core`, `embarch-api`, `embarch-umbrella` — are independent Cargo projects, not a workspace (`embarch-user-guide.md` §11's layout). Build each on its own: `cargo build` inside that repo, nothing cross-repo needed to compile.

## 2. Wiring a dev `embarch-core` + `embarch-api` together

This is already fully supported by existing config, no code changes needed:

1. Run a dev Core in the foreground, on a port that won't collide with a real installed service (default `4884`):
   ```sh
   cd embarch-core
   EMBARCH_TOKEN=dev-token cargo run -- run --port 4885
   ```
2. Point a dev `embarch-api` config at it explicitly — `base_url` set to a literal address, not `"auto"`, **always wins outright** over auto-detection (`embarch-api/design.md` §3.11, §7):
   ```toml
   [core]
   base_url = "http://127.0.0.1:4885"
   token = "dev-token"

   [[projects]]
   name = "scratch"
   source_path = "/tmp/scratch-fw"
   build_command = ["true"]
   artifact_path = "nonexistent.hex"
   chip = "nRF54L15"
   ```
3. Run the dev `embarch-api` directly against it, no install/PATH involved:
   ```sh
   cd embarch-api
   cargo run -- --config /path/to/dev-config.toml status
   ```
   Or point an MCP client at the debug binary directly, e.g. `claude mcp add embarch-dev -- /path/to/embarch-api/target/debug/embarch-api --config /path/to/dev-config.toml`.

Nothing here touches a real installed Core, a real token file, or `PATH` — it's two foreground processes on a scratch port, talking over an explicit `base_url`.

## 3. Testing `embarch-umbrella` changes — the dangerous one

`embarch-umbrella`'s `setup` (decision 28, `embarch-umbrella/design.md` §3) **writes to real, shared machine state**: it copies binaries into the canonical per-user install location, and edits `PATH` for real — the Windows registry (`HKCU\Environment\Path`) or your actual `~/.bashrc`/`~/.zshrc`. Running `cargo run -- setup` straight from a dev checkout, with no precautions, will silently overwrite your real, working install with an untested debug build and mutate your real shell config. Don't do that by default.

**Prefer unit tests first.** `install.rs`/`locate.rs`'s logic is written to be tested without touching the real filesystem/registry at all (`cargo test` — the pure functions and idempotent file operations are exactly what decision 28's own test suite exercises). This is how decision 28 was verified originally; reach for a live `setup` run only to confirm the parts unit tests structurally can't reach (an actual registry write taking effect, a real shell picking up the new `PATH`).

**If you do need a live run, sandbox it — on Unix, override both of these together:**
```sh
export XDG_DATA_HOME=/tmp/embarch-dev-test/data   # redirects canonical_bin_dir()
export HOME=/tmp/embarch-dev-test/home            # redirects which rc files get edited
mkdir -p "$XDG_DATA_HOME" "$HOME"
touch "$HOME/.bashrc"                              # ensure_sourced only touches rc files that already exist
cargo run -- setup
```
**`XDG_DATA_HOME` alone is not enough** — `install.rs`'s rc-file editing (`ensure_path_unix`) reads the real `$HOME` directly to find `.bashrc`/`.zshrc`, independent of `XDG_DATA_HOME`. Overriding only one of the two still edits your real shell config even though the binaries land somewhere harmless.

**On Windows, there is currently no equivalent sandbox.** `install.rs`'s registry code always opens the real `HKCU\Environment` — there's no env-var-style redirect the way Unix has via `HOME`. Until one exists (worth adding if this becomes frequent — a `EMBARCH_TEST_REGISTRY_ROOT`-style override, or reusing decision 21's still-unimplemented `--dry-run`), a live Windows test of the registry-write path means touching the real per-user registry. Treat it as reversible rather than harmless: `setup --uninstall` removes exactly what `setup` added, so run it after testing, and confirm with `reg query HKCU\Environment` (or the System Properties GUI) that nothing unexpected remains.

**To exercise `up`/`down`/`status`/`doctor` without ever calling `setup`'s install step at all**, point umbrella straight at dev binaries via the existing override env vars rather than relying on PATH or the canonical location:
```sh
export EMBARCH_CORE_EXE=/path/to/embarch-core/target/debug/embarch-core
export EMBARCH_API_BIN=/path/to/embarch-api/target/debug/embarch-api   # locate_api's own override, see locate.rs
cargo run -- status
```

## 4. Windows-specific code, checked from Linux/WSL2

This sandbox (and possibly yours) has no MSVC linker, so `cargo build --target x86_64-pc-windows-msvc` for the full `embarch-umbrella` binary fails on native-TLS dependencies (`aws-lc-sys`, pulled in via `reqwest`) that need a real C toolchain for that target — unrelated to any Windows-`cfg`-gated code you write yourself. To type-check Windows-only logic (registry code, anything behind `#[cfg(windows)]`) without a full build:

1. Extract just the Windows-`cfg`-gated module into a standalone throwaway crate (a `Cargo.toml` depending only on what that module needs — e.g. `winreg`, `anyhow` — not the whole `embarch-umbrella` dependency tree).
2. `cargo check --target x86_64-pc-windows-msvc` against that crate — this only type-checks and borrow-checks, no linking, so it works even without an MSVC toolchain present.
3. This catches real API-usage mistakes (wrong `winreg` signature, wrong types) but **not** runtime behavior — a real Windows machine is still the only way to confirm the registry write actually takes effect and a new shell actually picks up the change.

`rustup target list --installed` needs `x86_64-pc-windows-msvc` present for this to work at all; add it with `rustup target add x86_64-pc-windows-msvc` if it isn't.

## 4a. Getting a Core change onto the real Windows service

**Numbered `4a` rather than `5` deliberately.** This section belongs next to
§4 (it is the operational other half of "Windows code, checked from Linux"),
but §6 is referenced by name from nine `CLAUDE.md` files and from
[DOC-PROTOCOL.md](DOC-PROTOCOL.md) §6, so renumbering costs more than the odd
label does. `embarch-study-designer/design.md` §4.3a already sets that
precedent.

**`embarch deploy-core` now does all of this in one command — start there.**
[embarch-umbrella/design.md](embarch-umbrella/design.md) §3 decision 32. It
runs steps 1–3 below, and — the part worth having a command for — it
**verifies the installed binary actually changed** afterwards, which is the
one thing the manual procedure cannot do for you and the failure this section
warns about twice:

```sh
embarch deploy-core --windows-root /mnt/c/Users/<you>/source/repos   # first run
embarch deploy-core                                                  # thereafter
```

`--dry-run` prints the resolved plan and touches nothing; `--print-script`
does the unelevated half and hands you the privileged step.

**Be at the machine when you run it, and verify by hash afterwards (found 2026-08-27).** Self-elevation works, but the UAC dialog needs answering, and `deploy-core` reports **`landed`** whether or not it was — twice in one session it printed success after the elevated child was cancelled and nothing was installed ([embarch-umbrella/design.md](embarch-umbrella/design.md) §3 decision 32's amendment). Its own check compares byte *length*, and a release rebuild of one constant is the same size, so it cannot discriminate the most common development deploy. Confirm with

```sh
md5sum /mnt/c/Users/<you>/source/repos/embarch-core/target/release/embarch-core.exe \
       "$(/mnt/c/Windows/System32/sc.exe qc com.embarch.core | tr -d '\r' | sed -n 's/.*BINARY_PATH_NAME *: *//p' | cut -d' ' -f1)"
```

`--print-script` remains the fallback when you would rather run the privileged half yourself. Everything below
is still accurate and is what the command automates — read it to understand
what it is doing, or when it refuses and you need to do a step by hand.

**Why this section still exists in full, and why it read as pure prose for two
weeks.** It is *"the single most-repeated undocumented step in the suite"* —
two handoffs in a row pointed at "`embarch-dev-workflow.md`" for it while it
was not written down anywhere, and every session rediscovered it from scratch.
Writing it down fixed the forgetting and not the re-typing: every deploy after
that was still a hand-assembled `rsync` loop and a from-scratch PowerShell
script. That gap between "documented" and "automated" is the thing worth
noticing here.
§1–2 cover a *dev* Core on a scratch port, which is the right default and
touches nothing real. This section is the other case: a change to
`embarch-core` that has to reach the **installed Windows service** the whole
bench actually talks to.

### The shape of the problem

Three facts combine into a workflow that isn't obvious from any one of them:

1. The live Core is a **Windows service**, `com.embarch.core`, whose
   `BINARY_PATH_NAME` is
   `C:\Users\tmp12\embarch-setup\embarch-0.1.0-x86_64-pc-windows-msvc\embarch-core.exe run --bind 0.0.0.0`.
   The `0.1.0` is in the *directory* name only — the binary inside is
   whatever was last copied there, and its version tells you nothing.
2. **WSL2 cannot build it.** No MSVC linker here (§4), so the binary has to
   be produced by a native Windows `cargo.exe`.
3. The canonical git checkouts live on the **Linux** side
   (`/home/gabriel/Github/embarch/`). The Windows side has *source copies*,
   not clones.

So: sync source Linux → Windows, build on Windows, install the result into
the service's path, restart the service.

### Step 1 — sync the source, all three crates

`embarch-core`'s `Cargo.toml` has two `path` dependencies, so syncing Core
alone produces a build against stale siblings — which compiles, and is
wrong:

```toml
embarch-study-designer = { path = "../embarch-study-designer", features = ["std"] }
embarch-topology       = { path = "../embarch-topology", default-features = false, features = ["hardware"] }
```

Sync **shared crates first, Core last** — the same ordering §6 requires for
commits, for the same reason:

```sh
for r in embarch-study-designer embarch-topology embarch-core; do
  rsync -a --exclude '/target/' --exclude '/.git/' \
    /home/gabriel/Github/embarch/$r/ /mnt/c/Users/tmp12/source/repos/$r/
done
```

Excluding `/target/` matters in both directions: it keeps the sync fast, and
it keeps the Windows-side build cache (a *different* target triple's) from
being clobbered by Linux artifacts.

**`--delete` is deliberately not used here**, so a file deleted on the Linux
side lingers on the Windows side as an orphan. Cargo ignores a `.rs` file
nothing declares as a module, so this does not affect the build — but it
does mean **a grep of the Windows copy can turn up source that no longer
exists**. Treat the Linux checkout as the only thing worth reading; the
Windows copy is a build input, not a reference. Verify what drifted with:

```sh
diff -rq --exclude=target --exclude=.git \
  /home/gabriel/Github/embarch/embarch-core /mnt/c/Users/tmp12/source/repos/embarch-core
```

**These directories are not git clones — there is no `.git` at all.** That
is the hazard worth internalizing: an edit made directly on the Windows side
can reach a deployed binary without ever being version-controlled, and
`git status` on the Linux repo will look perfectly clean while it happens.
This has really occurred (`embarch-topology`'s `check_target_powered` shipped
that way and had to be recovered afterwards). **Never edit the Windows copy.
Edit on Linux, commit, then rsync.**

### Step 2 — build natively

```sh
cd /mnt/c/Users/tmp12/source/repos/embarch-core
/mnt/c/Users/tmp12/.cargo/bin/cargo.exe build --release
```

`cargo.exe` is not on the WSL `PATH`; give it the absolute path. The result
is `target/release/embarch-core.exe`.

Sanity-check that you built what you think you built, *before* deploying —
pick something the new commit adds and look for it:

```sh
./target/release/embarch-core.exe --help          # e.g. is `chip-list` there?
```

Running the fresh exe from WSL2 logs one benign warning first — `failed to
set up daily-rolling log file ... Access is denied` for
`C:\ProgramData\embarch\logs`, which only the service account can write.
It falls back to stderr and the command still runs. Not a symptom of
anything.

### Step 3 — install it into the service path

Two ways, and the supported one has a real footgun.

**`update` (supported, self-elevating).** It must be invoked **from the
currently-installed binary**, passing the new build as the argument:

```sh
/mnt/c/Users/tmp12/embarch-setup/embarch-0.1.0-x86_64-pc-windows-msvc/embarch-core.exe \
  update /mnt/c/Users/tmp12/source/repos/embarch-core/target/release/embarch-core.exe
```

**Never run the new build against itself** (`target/release/embarch-core.exe
update target/release/embarch-core.exe`). `service.rs::update` resolves the
binary it replaces via `std::env::current_exe()` — *whichever binary is
running the command* — so a self-update renames that file aside to `.bak`,
then tries to copy from the path it just renamed away, fails "file not
found", rolls the exe back, and **never reaches `start()`**. The binary
looks untouched and the service is left stopped. This has happened, and left
the live Core down for several minutes.

Two further properties of `update` worth knowing rather than rediscovering:
it **rolls back automatically** if the new binary fails to start (so a bad
build costs a restart, not a broken bench), and it deliberately **leaves its
own `.bak` behind** on success — the process doing the replacing is still
executing from that file — cleaned up by the *next* `update` call. A
lingering `.bak` is expected, not a failed run.

**A refusal is reported; a prompt that never appears is not — found 2026-08-26.** `update` prints `Error: elevation declined (UAC prompt cancelled)` when the user says no. But a launch where the consent dialog never renders at all **exits `0`, prints nothing but the benign log warning, and does nothing** — the exe is untouched, no `.bak` appears, and the service keeps running the old binary. So do not read a clean exit as a successful deploy: check the binary's size/timestamp, or probe a route only the new build has. There is no unelevated fallback to reach for either — `sc.exe sdshow com.embarch.core` grants Interactive Users `CCLCSWLOCRRC` (query only, no `RP`/`WP`), so a non-admin can neither stop nor start it, **even though the install directory itself is writable** because it lives under the user's own profile. The writable directory is a trap: you can swap the binary and still not be able to restart the service onto it.

When `update` will not go through, the reliable path is to do the elevation yourself around a script that logs from *inside* the elevated context — `Start-Process powershell -Verb RunAs -Wait` running a `.ps1` that `Tee-Object`s each step to a file. That gives one UAC prompt and a readable transcript of stop/copy/start, instead of a child console that vanishes.

**`stop` → copy → `start` (simpler when you want to see each step).** Same
outcome, no `current_exe()` subtlety, at the cost of doing the elevation
yourself.

Either way, if you need to see what the elevated child actually printed:
`ShellExecuteExW`'s relaunch gives it its own console, so a
`Start-Process -Wait -Redirect...` wrapped around the *unelevated* launcher
captures nothing. Do the elevation yourself (`Start-Process powershell -Verb
RunAs -Wait ...` running a script that redirects `*>` to a file from inside
the already-elevated context).

### Step 4 — verify, and mind two couplings

Confirm the service is back and serving:

```sh
/mnt/c/Windows/System32/sc.exe query com.embarch.core     # STATE : 4 RUNNING
```
then `GET /status` through `embarch-api` (or `curl` the bind address).

**Coupling 1 — the dev-bench wire schema.** If the redeploy carries a bump
to `DEV_BENCH_WIRE_SCHEMA_VERSION`
([embarch-study-designer/design.md](embarch-study-designer/design.md)), the
board's firmware **must be reflashed in the same sitting**. Core sends
`Hello { schema_version }`; a bench on the older version answers
`compatible: false` and Core refuses the link. There is no partial-upgrade
mode, by design — so check that constant against what the board is running
before you deploy, not after the handshake fails. `GET /dev-bench/hello`
reports what the bench claims, and `embarch deploy-core` prints the constant
out of the source it is about to deploy so the check happens before the build
rather than after the handshake fails.

**Setting an environment variable for the installed Core.** Core reads knobs
like `EMBARCH_SIGNAL_BAUD`, `EMBARCH_FLASH_BACKEND` and the tool-path overrides
from its process environment — and as a Windows service it gets none of your
shell's. Exporting the variable in WSL, or in the terminal you deploy from,
reaches nothing. Write it to the service's own registration instead:

```powershell
Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\com.embarch.core' `
  -Name Environment -Value @('EMBARCH_SIGNAL_BAUD=230400') -Type MultiString
```

`REG_MULTI_SZ`, one `KEY=VALUE` per element, and the SCM injects them at
service start — so **restart the service afterwards** or nothing changes. Needs
elevation, same as everything else here. It is deliberately per-service rather
than a system-wide environment variable: these knobs are Core's, and a
machine-wide `EMBARCH_*` would leak into every other process.

Verifying it took is the awkward part, because Core does not print its
configuration anywhere. `EMBARCH_FLASH_BACKEND` and the tool paths have a
direct read-out — `embarch-core.exe flash-backend` reports what it resolved.
For the others, provoke an error that quotes the value back: declaring a signal
against a port you hold open from another process makes Core's own failure
message name the baud it opened at.

**Coupling 1a — flashing does not reset the target.** `embarch-api`'s `flash`/`flash_dev_bench` (and so `build_and_flash`) write the image and leave the chip running whatever it was already running. Found 2026-08-26 on both boards at once: dev-bench reported `flashed: true` and kept answering the old schema version, and the DUT reported `flashed: true` and kept serving the previous build's GATT table. It presents as "I flashed it and nothing changed", which reads like a build going to the wrong place rather than like a missing reset. Call `reset`/`reset_dev_bench` after every flash before believing anything about the new image.

**And `run_study --reflash dut` does not do it for you (found 2026-08-27).** The dev-bench half of that call resets; the DUT half flashes and goes straight on to submitting the study, so the one call that exists to spare you this coupling walks into it — and records a successful reflash in the result's `provenance` while the board runs the old image. Until that is fixed ([embarch-api/design.md](embarch-api/design.md) §3 decision 44), reflash a DUT with `build_and_flash` + `reset` and submit the study with `reflash: none`.

**Coupling 2 — `embarch-api`'s MCP process is long-lived.** Rebuilding
`/home/gabriel/Github/embarch/embarch-api/target/debug/embarch-api` does not
affect the running MCP server; a client picks up the new binary only on a
**fresh Claude Code session**. Deploy order across the two is Core first,
then api ([embarch-core/design.md](embarch-core/design.md) §3 decision 30).

## 5. Agent-driven iteration — what's safe unsupervised, what isn't

**The general rule, on the repo owner's own real daily-use machine (global `CLAUDE.md`, 2026-08-17): full autonomy to build, test, flash, and develop — the only thing worth asking about is a physical action only the user can do** (plugging in a board/cable, pressing a physical button, swapping hardware). Everything below is that rule applied to this suite specifically, kept for the detail (which exact commands, which real files) rather than as a separate, narrower policy.

**Tier 1 — no real state touched at all:** everything in §1–2. Building, `cargo clippy`/`cargo test` on any of the three repos, and running dev `embarch-core`+`embarch-api` together via explicit `base_url`/scratch ports touch nothing but disposable local processes and a scratch config file.

**Tier 2 — writes real, shared machine state, but still no physical action needed:** any *live* invocation of `embarch setup`, `embarch up`/`down`, `embarch setup --uninstall`, or `embarch-core`'s own `install`/`start`/`stop`/`uninstall`. These touch a real OS service, the real per-user `PATH` (registry or rc files, §3), and a real system-wide token file (`/var/lib/embarch/token` on Linux, `%ProgramData%\embarch\token` on Windows — **not** redirectable by `HOME`/`XDG_DATA_HOME`, since it's a fixed system path, not per-user). Concretely, on a real `wsl-host` machine: `setup --uninstall`'s token-removal step resolves to `/mnt/c/ProgramData/embarch/token` — the real Windows-hosted Core's real token file, with no env-var override that redirects it anywhere else. Covered by the general rule above — no asking, on the owner's own machine.

**Tier 3 — needs a physical action, the one real checkpoint left:** attaching a debug probe or board to a USB port. Everything downstream of that — `probe-rs list`, chip resolution, `build`/`flash`/`build_and_flash`/`reset`/`serial_log` against the now-connected hardware, including Milestone 1's real reference-dut flash (`embarch-api/milestone-7.md`) — proceeds without asking once the hardware is physically present. The checkpoint is specifically "is it plugged in," not "may I flash it."

**Elsewhere** — a different machine, a different person, or anything where the owner's own standing authorization doesn't clearly apply — ask before running a Tier 2 command live, unless it's provably running inside a disposable environment built for exactly this, in which case asking isn't needed because nothing real is at stake:

- **[`dev-sandbox/`](../embarch-umbrella/dev-sandbox/) (in `embarch-umbrella`)** — a Docker container with its own `/root`/`/var/lib` and no WSL2 interop or `/mnt/c`, so a live `setup`/`up`/`down`/`uninstall` run inside it can't reach anything real. `./dev-sandbox/run.sh` builds the image and drops into a shell with all three repos bind-mounted. **Not yet verified** — written with no `docker` binary available in the session that wrote it; watch its first real run. It deliberately stops short of a real init system (no systemd/D-Bus), so `embarch-core install`/`start` will fail cleanly (service manager unreachable) inside it rather than persist a real service — enough to confirm the *code path* an agent is testing, without widening what the container can affect on the host by adding `--privileged`.
- **A CI runner is already this kind of sandbox, no new tooling needed.** If any of this ever gets scripted into a GitHub Actions workflow, a `setup`/`doctor` step running there is already unsupervised-safe — the runner is destroyed after, same property the dev-sandbox container is built to have locally.
- **Unit tests are the fully-autonomous default whenever they can reach the logic in question** — pure functions and idempotent file operations, as most of `install.rs`/`locate.rs` already are. This is how decision 28 itself was verified in the same session it was written (§4 also covers checking Windows-`cfg` code this way). Reach for the sandbox above only for what tests structurally can't reach — real registry/service-manager behavior.

## 6. Branching: don't, for now — work directly on `main`

**The rule, across every EmbArch repo (2026-08-25): commit straight to `main`. No feature branches, no PRs, no merges.** This includes `embarch-doc` — the docs move in the same pass as the code they describe (DOC-PROTOCOL.md §5), so putting them on a separate branch just splits one change in two.

**It ends when the repo owner says it ends, and on no other condition.** Not when a heuristic looks satisfied, not when someone judges the project "mature enough" — the trigger is an explicit call, and until it is made, an agent working here does not get to decide the moment has arrived. This is deliberately a *stated* trigger rather than an open-ended "for now," matching how the rest of these docs close things they aren't building yet.

**Why this is a real rule and not just laziness.** A branch exists to keep concurrent work from colliding. This suite has one engineer (`embarch.md` §5's single-engineer scope, and `embarch-api/design.md` §3.1's), CI reports but gates nothing, and no one downstream installs from `main`. There is nothing to collide with, so a branch buys isolation nobody needs and costs something real: the suite spans **eight repos that must move together**, and a schema change touching five of them turns into five branches, five merges, and five chances to leave one behind. That is not hypothetical — Milestone 7 Phase B ran exactly that way across six repos, and every one of the six merges turned out to be a fast-forward with no divergence to resolve. The branches recorded nothing the commit messages didn't already say.

**What this changes for an agent working here, concretely.** The default instruction "if you're on the default branch, branch first" is **overridden in this suite**. Commit to `main`. Push when the work is done and green, per §5's autonomy rule — the same standard as before, applied one commit at a time rather than one branch at a time.

**What does *not* change, and is what makes this safe:**

- **`main` still has to build.** Nothing about skipping branches licenses committing something red. Run the crate's own `cargo build`/`test`/`clippy --all-targets -- -D warnings` — plus a native Windows build where `embarch-core` is involved (§4) — *before* the commit, not after.
- **A cross-repo change still lands as one logical pass.** Sequence the repos so each one's `main` compiles on its own: the shared crate first (`embarch-study-designer`, `embarch-topology`), then its consumers. Deploy order is a separate question and is not always the same order (Milestone 7's is Core-before-api, `embarch-core/design.md` §3 decision 30).
- **Commit granularity is the thing carrying the history now.** With no branch name and no merge commit to hang a milestone off, the commit message is the only record of what a change was for. Write it accordingly.
- **Real, risky, or exploratory work can still take a branch.** This is a default, not a prohibition — a rewrite you might abandon is exactly what a branch is for. The rule is against branching *reflexively* for ordinary forward work.
