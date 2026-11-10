# embarch: local dev workflow

**Status:** active, 2026-09-02.

How to iterate on `embarch-core`, `embarch-api` and `embarch-umbrella` locally **without cutting a release and without a debug build silently touching a real machine's install** — plus the opposite case: how a Core change actually reaches this machine's live Windows service (§4a).

## 1. Short answer

**Never develop against a release build, and you rarely need `--release` at all for iteration.** A debug build compiles faster and behaves identically for everything except raw speed. Reach for `--release` only when producing the thing you or CI will ship.

These three repos are **independent Cargo projects, not a workspace**. Build each on its own — but each `path`-depends on sibling repos, so **nothing cross-repo is needed beyond having those siblings on disk and current; stale ones compile fine and hand you a wrong binary** (§4a).

## 2. Wiring a dev Core and API together

Fully supported by existing config, no code changes:

```sh
cd embarch-core
EMBARCH_TOKEN=dev-token cargo run -- run --port 4885     # scratch port, not 4884
```

Then point a dev `embarch-api` config at it with a **literal** `base_url`, which **always wins outright over auto-detection**, and run it directly:

```sh
cd embarch-api
cargo run -- --config /path/to/dev-config.toml status
```

Or point an MCP client at the debug binary: `claude mcp add embarch-dev -- /path/to/target/debug/embarch-api --config /path/to/dev-config.toml`.

**Nothing here touches a real installed Core, a real token file, or `PATH`** — two foreground processes on a scratch port, talking over an explicit address.

## 3. Testing `embarch-umbrella` changes — the dangerous one

**`setup` writes real, shared machine state**: it copies binaries into the canonical per-user install location and **edits `PATH` for real** — the Windows user registry, or your actual shell rc files. **Running `cargo run -- setup` from a dev checkout with no precautions silently overwrites your real, working install with an untested debug build and mutates your real shell config.**

**Prefer unit tests first.** The install and locate logic is written to be tested without touching the real filesystem or registry at all. Reach for a live run only for what tests structurally cannot reach: a registry write actually taking effect, a real shell actually picking up the new `PATH`.

**If you do need a live run, sandbox it — on Unix, override both of these together:**

```sh
export XDG_DATA_HOME=/tmp/embarch-dev-test/data   # redirects the install dir
export HOME=/tmp/embarch-dev-test/home            # redirects which rc files get edited
mkdir -p "$XDG_DATA_HOME" "$HOME" && touch "$HOME/.bashrc"   # only existing rc files are touched
cargo run -- setup
```

**The data-dir override alone is not enough** — the rc-file editing reads the real `$HOME` directly, independent of it, **so overriding only one still edits your real shell config even though the binaries land somewhere harmless.**

**On Windows there is no equivalent sandbox.** The registry code always opens the real per-user hive; there is no env-var redirect the way Unix has. Treat a live Windows test as **reversible rather than harmless**: `setup --uninstall` removes exactly what `setup` added, so run it afterwards and confirm nothing unexpected remains.

**To exercise `up`/`down`/`status`/`doctor` without calling `setup`'s install step at all**, point umbrella straight at dev binaries with `EMBARCH_CORE_EXE` and `EMBARCH_API_BIN` rather than relying on `PATH`.

## 4. Windows-specific code, checked from Linux/WSL2

With no MSVC linker present, a full cross-build of `embarch-umbrella` fails on native-TLS C dependencies — **unrelated to any Windows-gated code you wrote.** To type-check Windows-only logic without a full build:

1. **Extract just the Windows-gated module into a standalone throwaway crate**, depending only on what that module needs rather than the whole tree.
2. `cargo check --target x86_64-pc-windows-msvc` against it — **type- and borrow-check only, no linking, so it works with no MSVC toolchain present.**
3. **It catches real API-usage mistakes and not runtime behaviour.** A real Windows machine is still the only way to confirm a registry write takes effect and a new shell picks it up.

## 4a. Getting a Core change onto the real Windows service

**Numbered `4a` rather than `5` deliberately:** this belongs next to §4 as the operational other half of it, but **§6 is referenced by name from nine `CLAUDE.md` files and from [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §6, so renumbering costs more than the odd label does.**

§1–2 cover a *dev* Core on a scratch port, which is the right default and touches nothing real. This is the other case: **a change that has to reach the installed Windows service the whole bench actually talks to.**

**`embarch deploy-core` does all of this in one command — start there.**

```sh
embarch deploy-core --windows-root /mnt/c/Users/<you>/source/repos   # first run
embarch deploy-core                                                  # thereafter
```

`--dry-run` prints the resolved plan and touches nothing; `--print-script` does the unelevated half and hands you the privileged step.

**Be at the machine when you run it, and verify by hash afterwards.** Self-elevation works, but **the consent dialog needs answering, and `deploy-core` reports `landed` whether or not it was** — twice in one session it printed success after the elevated child was cancelled and nothing was installed. **Its own check compares byte *length*, and a release rebuild of one constant is the same size, so it cannot discriminate the most common development deploy.** Confirm with:

```sh
md5sum /mnt/c/Users/<you>/source/repos/embarch-core/target/release/embarch-core.exe \
       "$(/mnt/c/Windows/System32/sc.exe qc com.embarch.core | tr -d '\r' | sed -n 's/.*BINARY_PATH_NAME *: *//p' | cut -d' ' -f1)"
```

### The shape of the problem

Three facts combine into a workflow that is not obvious from any one of them:

1. **The live Core is a Windows service** whose registered path names a versioned *directory* — **the binary inside is whatever was last copied there, and its version tells you nothing.**
2. **WSL2 cannot build it.** No MSVC linker, so the binary has to come from a native Windows `cargo.exe`.
3. **The canonical git checkouts live on the Linux side. The Windows side has *source copies*, not clones.**

So: sync source Linux → Windows, build on Windows, install into the service's path, restart the service.

### Step 1 — sync the source, all four crates

Core has three `path` dependencies (`embarch-smp` joined for `POST /bootload`), **so syncing Core alone produces a build against stale siblings — which compiles, and is wrong.** Sync **shared crates first, Core last** — the same ordering §6 requires for commits, for the same reason:

```sh
for r in embarch-study-designer embarch-topology embarch-smp embarch-core; do
  rsync -a --exclude '/target/' --exclude '/.git/' \
    /home/gabriel/Github/embarch/$r/ /mnt/c/Users/tmp12/source/repos/$r/
done
```

**Excluding `/target/` matters in both directions:** it keeps the sync fast, and it keeps the Windows-side build cache — a *different* target triple's — from being clobbered by Linux artifacts.

**`--delete` is deliberately not used**, so a file deleted on Linux lingers on Windows as an orphan. Cargo ignores a source file nothing declares as a module, so the build is unaffected — but **a grep of the Windows copy can turn up source that no longer exists.** Treat the Linux checkout as the only thing worth reading; **the Windows copy is a build input, not a reference.**

**These directories are not git clones — there is no `.git` at all, and that is the hazard worth internalizing.** An edit made directly on the Windows side **can reach a deployed binary without ever being version-controlled, while `git status` on the Linux repo looks perfectly clean.** This has really happened: one function shipped that way and had to be recovered afterwards. **Never edit the Windows copy. Edit on Linux, commit, then rsync.**

### Step 2 — build natively

```sh
cd /mnt/c/Users/tmp12/source/repos/embarch-core
/mnt/c/Users/tmp12/.cargo/bin/cargo.exe build --release
```

**`cargo.exe` is not on the WSL `PATH`; give it the absolute path.** Then **sanity-check that you built what you think you built, *before* deploying** — pick something the new commit adds and look for it in `--help`.

Running the fresh exe from WSL2 logs one **benign** warning first: it cannot open the service account's log directory, falls back to stderr, and runs anyway. **Not a symptom of anything.**

### Step 3 — install it into the service path

**The supported path is `update`, and it has a real footgun: it must be invoked *from the currently-installed binary*, passing the new build as the argument.**

**Never run the new build against itself.** `update` resolves the binary it replaces via **whichever binary is running the command**, so a self-update renames that file aside, then tries to copy from the path it just renamed away, fails, rolls back, and **never reaches the start step. The binary looks untouched and the service is left stopped.** This has happened, and **left the live Core down for several minutes.**

Two further properties worth knowing rather than rediscovering: **it rolls back automatically if the new binary fails to start** (so a bad build costs a restart, not a broken bench), and **it deliberately leaves its own backup copy behind on success** — the process doing the replacing is still executing from that file — cleaned up by the *next* call. **A lingering backup is expected, not a failed run.**

**A refusal is reported; a prompt that never appears is not.** `update` prints an error when the user declines. But a launch where the consent dialog **never renders at all exits `0`, prints nothing but the benign warning, and does nothing** — the exe untouched, no backup, the service still on the old binary. **So do not read a clean exit as a successful deploy:** check the binary's hash, or probe a route only the new build has.

**There is no unelevated fallback either.** The service's own ACL grants Interactive Users query rights only, **so a non-admin can neither stop nor start it — even though the install directory itself is writable**, because it lives under the user's own profile. **The writable directory is a trap: you can swap the binary and still not be able to restart the service onto it.**

When `update` will not go through, the reliable path is **to do the elevation yourself around a script that logs from *inside* the elevated context.** The relaunch gives the child its own console, **so a redirect wrapped around the *unelevated* launcher captures nothing.** One prompt, and a readable transcript of stop, copy and start.

### Step 4 — verify, and mind two couplings

Confirm the service is back (`sc.exe query com.embarch.core` → `RUNNING`), then `GET /status` through the API.

**Coupling 1 — the dev-bench wire schema.** If the redeploy carries a bump to the dev-bench wire version, **the board's firmware must be reflashed in the same sitting.** Core sends its version in the handshake; a bench on the older one answers incompatible and **Core refuses the link. There is no partial-upgrade mode, by design** — so check the constant against what the board is running **before you deploy, not after the handshake fails.** `deploy-core` prints the constant out of the source it is about to deploy, so the check happens before the build.

**Coupling 1a — flashing does not reset the target.** `flash` and `build_and_flash` write the image and **leave the chip running whatever it was already running.** Found on both boards at once: the bench reported `flashed: true` and **kept answering the old schema version**, and the DUT reported `flashed: true` and **kept serving the previous build's GATT table.** It presents as *"I flashed it and nothing changed"*, **which reads like a build going to the wrong place rather than like a missing reset.** Call `reset` after every flash before believing anything about the new image.

**And `run_study --reflash dut` does not do it for you.** The bench half of that call resets; the DUT half flashes and goes straight on to submitting the study — **so the one call that exists to spare you this coupling walks into it, and records a successful reflash in the result while the board runs the old image.** Until that is fixed, reflash a DUT with `build_and_flash` plus `reset` and submit with `reflash: none`.

**Coupling 2 — the API's MCP process is long-lived.** Rebuilding its debug binary **does not affect the running MCP server**; a client picks up the new one only on a **fresh session.** Deploy order across the two is **Core first, then the API.**

**Setting an environment variable for the installed Core.** Core reads knobs like `EMBARCH_SIGNAL_BAUD` and `EMBARCH_FLASH_BACKEND` from its process environment — and **as a Windows service it gets none of your shell's.** Exporting the variable in WSL, or in the terminal you deploy from, **reaches nothing.** Write it into the service's own registration instead:

```powershell
Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\com.embarch.core' `
  -Name Environment -Value @('EMBARCH_SIGNAL_BAUD=460800') -Type MultiString
```

One `KEY=VALUE` per element, injected at service start — **so restart the service afterwards or nothing changes.** Deliberately per-service rather than machine-wide: **these knobs are Core's, and a machine-wide `EMBARCH_*` would leak into every other process.**

**Verifying it took is the awkward part, because Core does not print its configuration anywhere.** The flash-backend override has a direct read-out. For the others, **provoke an error that quotes the value back** — declaring a signal against a port you hold open from another process makes Core's own failure message name the baud it opened at.

## 5. Agent-driven iteration — what is safe unsupervised

**The general rule, on the repo owner's own daily-use machine: full autonomy to build, test, flash and develop. The only thing worth asking about is a physical action only the user can do** — plugging in a board or cable, pressing a button, swapping hardware. Below is that rule applied to this suite specifically, kept for the detail rather than as a narrower policy.

- **Tier 1, no real state touched at all:** everything in §1–2. Builds, clippy, tests, and a dev Core plus API on scratch ports **touch nothing but disposable local processes.**
- **Tier 2, writes real shared machine state but needs no physical action:** any *live* `setup`, `up`/`down`, `setup --uninstall`, or Core's own `install`/`start`/`stop`/`uninstall`. These touch a real OS service, the real per-user `PATH`, and **a real system-wide token file that `HOME`/`XDG_DATA_HOME` do not redirect, because it is a fixed system path.** On a WSL-host machine the uninstall's token step resolves to **the real Windows-hosted Core's real token file, with no override anywhere.** Covered by the general rule — no asking, on the owner's own machine.
- **Tier 3, the one real checkpoint left:** attaching a probe or board to a USB port. **Everything downstream of that proceeds without asking once the hardware is physically present. The checkpoint is "is it plugged in", not "may I flash it".**

**Elsewhere** — a different machine, a different person, or anywhere the owner's standing authorization does not clearly apply — **ask before running a Tier 2 command live**, unless it is provably inside a disposable environment built for exactly this:

- **`dev-sandbox/` in `embarch-umbrella`** — a container with its own root and no WSL2 interop, so a live `setup`/`up`/`down` run inside it **cannot reach anything real.** **Not yet verified** — written with no container runtime available in the session that wrote it. It deliberately stops short of a real init system, so a service install **fails cleanly rather than persisting a real service** — enough to confirm the code path without widening what the container can affect.
- **A CI runner is already this kind of sandbox, no new tooling needed** — destroyed afterwards, the same property the container is built to have locally.
- **Unit tests are the fully-autonomous default whenever they can reach the logic in question.** Reach for the sandbox only for what tests structurally cannot: real registry and service-manager behaviour.

## 6. Branching: branches and worktrees, no PRs

**The rule, across every EmbArch repo (the owner's call, 2026-11-03): work on a branch in a worktree, and land on `main` when the owner asks. No PRs.** Use one branch name in every repo a change touches, `embarch-doc` included: the docs move with the code they describe, **so they belong on the same branch.** Changing this rule is the owner's call as well: **the trigger is an explicit call, and an agent working here does not get to decide it has been made.**

**What it replaced, and why.** From 2026-08-25 the rule was to commit straight to `main`, on the reasoning that one engineer has nothing to collide with. That stops holding once chats run side by side in one clone, each staging hunk by hunk around the others. The call came as EmbArch's work moved onto its own Linear workspace and Claude subscription. **The old rule's objection is now this rule's cost:** the suite spans eight repos that must move together, and a schema change touching five of them is five branches and five landings. One milestone phase ran that way across six repos, and every merge was a fast-forward with no divergence to resolve. One branch name and one landing request per change keep that cost down.

**Setting up.** Keep a change's worktrees side by side in a folder of their own, so `../embarch-doc` and the Cargo path dependencies resolve as they do in the main checkouts, and symlink each sibling the change is not touching to its main checkout, as the fleet's legs do. **On a suite desk, Start work makes this folder** at `.dev-worktrees/<key>/` from the issue's Project, and the `desk_add_repo` tool turns a symlink into a worktree on the same branch ([desk decision 70](embarch-desk/decisions.md)); without an issue, make it by hand. Push the branch as you commit, for backup. **A key from the owner's personal Linear workspace in a branch name is just a name:** nothing checks for one, and nobody outside can resolve it. A client's key or name is never allowed, in a branch name or anywhere else.

**Landing happens only when the owner asks**, repo by repo: rebase on `origin/main`; confirm it builds and its tests and `clippy --all-targets -- -D warnings` are clean; `merge --ff-only`; push; delete the remote branch. **Landing leaves the worktrees, their local branches and the folder in place** (owner's call, 2026-11-05): a chat Start work opened runs inside that folder, and one that removed it could no longer resume, its window left open on a folder that no longer existed. **Moving the issue to Done or Canceled removes them** ([desk decisions 83, 84](embarch-desk/decisions/closeout.md)): it ends the issue's chat, and once no window has shown the folder for three minutes the desk removes each worktree, its local branch and the folder, whose symlinks go while their targets stay; Canceled also deletes the branches on `origin`. Uncommitted files block it, and for Done so does a branch not on `origin/main`: the desk names each blocker and removes nothing. A folder made by hand, with no issue, is still the owner's to remove: `git worktree remove` each worktree, delete its local branch, `rm -r` the folder. A non-fast-forward means something else moved `main`: fetch and rebase, never force. This is the supervisor's method, so `main` stays linear.

**The sequencing rules**, which matter more than the branching question: **land shared crates before their consumers**, so a checkout of any single commit builds; **land a wire-schema bump and the firmware that speaks it in the same sitting** (§4a coupling 1); **land `embarch-doc` right after the code it describes**; and **push each repo as it lands** rather than batching, because **a path dependency that exists only locally makes another repo's CI fail for a reason its own diff cannot explain.**

**A change that does not pan out** is a branch you delete rather than land.

**The fleet is unaffected.** Its workers already work this way, and its supervisor lands them, and pushes its own fold commits to `main`, under [the protocol](../embarch-fleet/protocol.md).

**Linear's GitHub integration is set up for the PRs this rule does not open yet** (owner's call, 2026-11-10): PRs wait until EmbArch is stable, and once they start each one shows on its issue with nothing further to set up. It joins the owner's EmbArch Linear workspace to the `embarch-*` repos, each picked by name in the install of Linear's GitHub app, so **a new repo is added there by hand**. A PR links when its branch name or title carries the issue key — the branch Linear's *copy git branch name* gives, `tetargabriel/emb-91-…`, already does — or its description says `Fixes EMB-91`; **`Part of EMB-91` links a PR that must not close the issue**, one of several. **Merging a linked PR moves its issue to Done, and no other PR event moves it**, because the fleet moves EMB statuses itself. **Linkbacks are off**: a linkback posts the issue's title and description as a comment on the PR, and the repos are public while the workspace is private. **When PRs come, the owner's work opens them first**: a branch gets its PR at the first push and still lands by fast-forward and push, which GitHub should mark as the PR merged (not yet measured), never by GitHub's rebase button, which rewrites the SHAs the kept worktrees hold. **The fleet's landing would gain nothing from them**: its gate runs locally, a client-name denylist that is in no repo included, a unit's two branches land in a fixed order GitHub cannot keep across repos, and its fold is one commit a GitHub merge would split ([the protocol](../embarch-fleet/protocol.md) §11). What PRs would give it is a link from its units to their issues, opened as a record of a fast-forward landing, with `Part of`, since a fleet issue is split into several tasks and `fleet-linear.py finish` closes it. **Rejected:** PRs now, and status moves on a PR's opening or review.
