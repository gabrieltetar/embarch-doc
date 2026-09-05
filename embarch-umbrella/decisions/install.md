# embarch-umbrella decisions: Setup, install, and starting Core

**Status:** active, 2026-09-02.

Getting a machine from nothing installed to a running Core.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 3 — Core is always an installed, autostarting OS service — that, not a launcher, is the actual answer to "one button starts everything"

On every same-machine topology, if Core autostarts at boot **there is nothing for a human to start, ever**: `embarch-api` is invoked per use and finds a Core that is already up. **So the problem is a one-time setup problem plus an ongoing verification problem, not a process-management problem.** Core's own cross-platform service install already exists and already handles all three OSes; **umbrella's contribution is making sure it actually got run, with the right environment, on the right machine.**

**One refinement of this was later reversed as bad design.** It briefly held that `setup` does *not* edit `PATH`, because the single release archive puts all three binaries in one directory and umbrella could find Core as a sibling of itself with no environment surgery — editing a shell rc (which shell? which of four startup files?) or the Windows registry being invasive and awkward to undo. **Sibling lookup ties correct operation to wherever the archive happened to be unpacked staying put forever**, and a real onboarding run surfaced the confusion directly: the printed Core path reported the local Linux sibling instead of the Windows-side binary a `wsl-host` topology actually needs. Replaced by decision 28.

### 4 — `up`/`down` exist, but as a fallback, not the main path

They cover: the service is not installed, the service died, or a foreground Core is wanted for debugging. `up` prefers starting the installed service, because **a directly-spawned Core dies with the shell that started it, which is a confusing failure mode to hand someone as the default.**

**The foreground fallback is opt-in, not automatic.** Distinguishing "no service installed" from "start failed for some other reason" means **pattern-matching each backend's error text, which is exactly the per-OS fragility this decision exists to avoid.** So a failed `up` prints the three real options and does nothing else. `--foreground` then blocks in the caller's terminal rather than detaching, **so nobody ends up with a Core that vanished when they closed a window.** A `remote` topology refuses `up`/`down` outright rather than falling back to a local binary, **which would start a second, wrong Core.**

### 5 — Umbrella is deliberately *not* the process the MCP client spawns

The tempting alternative — register `embarch mcp` as the MCP server so that starting the agent brings the whole stack up — **puts umbrella permanently in the stdio hot path, makes every MCP-transport problem a two-binary debugging exercise, and buys little once Core is already running** (decision 3). MCP registration points straight at `embarch-api`.

### 14 — Distribution: one suite release archive containing all three binaries, published from this repo

So the getting-started path is one download rather than three, and **the three binaries in a user's hands are a version-tested set rather than an arbitrary combination.** Four targets: Windows x86-64, Linux x86-64, macOS aarch64, and Linux aarch64 for a future Pi Core. Per-repo releases still exist for developers working on one component; **the suite release is what the user guide points at.** A version mismatch against the suite manifest is a warning (decision 24).

Each repo has its own tag-triggered release workflow; this repo additionally assembles the suite archive by pulling one tagged release of each component and repackaging all three binaries plus a small JSON manifest per target, **which `doctor` reads only when one happens to sit next to the running binary** — absent for a per-repo release or a debug build, reported as skipped rather than failed.

**Both open questions the plan flagged had the same answer: GitHub already provides it.** macOS aarch64 builds natively because the runner is itself Apple Silicon (still unsigned — Gatekeeper is the guide's problem, not CI's), and Windows needs nothing extra. **The one genuine cross-compile is Linux aarch64**, and only Core needs more than a bare cross-linker for it, because its hardware crates pull in a C dependency — that leg uses a Docker-based cross build installing the arm64 dev package into the container.

**Verified against real tags, and two real bugs came out of the first run.** Core's first push failed **exactly where predicted as the risk** — the *native* Linux leg, because the C dev package had only been arranged for the cross leg, and the runner does not ship it the way a real Linux dev machine does. Then the assembly job caught a second bug on its first-ever run: a `ls a.tar.gz b.zip 2>/dev/null | head -n1` line to find whichever archive extension a target used **exits 2 whenever only one of the two globs matches — which is every target, since none ever has both.** `ls` still prints the real file, but `pipefail` turns the stderr complaint into a fatal error regardless. Fixed with `nullglob` and an array.

### 21 — `embarch setup --dry-run` prints the plan before an elevated run executes it

The elevation friction decision 7 flags is partly a **"what is this about to do to my machine" problem, worse when the answer requires trusting a binary you just downloaded.** It runs every detection step exactly as `setup` does, then prints the concrete actions — which service calls, which files, whether elevation is needed — **reusing `setup`'s own detection path, not a second parallel implementation.**

**Built 2026-09-04, and it was not the one-flag-and-an-early-return it looked
like.** `make_plan` did already run every detection step before anything acted —
but two of the three side effects, decision 28's copy and `PATH` write,
**post-date this decision's text and only ever printed *while* acting**, so an
early return would have silently omitted them. So: every location a run may
write to is resolved once into a `Locations` passed down rather than read at
each write; `install.rs` gained a read-only `plan_install` built from the same
constants and predicates the real `install_into` uses, so the two cannot drift;
and one `apply_plan` walks both modes. A dry run names the canonical directory
and each binary as copy / already-there / absent, the env file and rc file
`PATH` would gain, the `embarch-core install --bind` line and its elevation, and
the state file it would write — and calls a Core it would put there **"would be
installed by this run"**, never "just installed here".

**What establishes that it changes nothing is a test, not the early return:**
`apply_plan` driven with every writable location pointed at a sandbox and
`embarch-core` a script that would leave a sentinel if ever executed, then the
sandbox asserted untouched. `--dry-run` conflicts with `--uninstall` rather than
being quietly ignored by it.

### 25 — `embarch setup --uninstall` reverses a machine setup

`init --uninstall` already reversed a repo integration; **nothing symmetric existed for `setup` itself.** It stops and unregisters the Core service, removes the machine-wide token file (a fresh `setup` regenerates one, matching normal first-run behaviour), and — per decision 28 — **removes the canonical install directory and the real `PATH` additions**, where it originally only printed the line to remove. It does not touch a firmware repo's own integration; that stays `init --uninstall`'s job.

### 28 — `setup` performs a real install: it copies all three binaries to a canonical per-user location and persists `PATH` for real

Reversing decision 3's sibling-lookup refinement, **prompted by a real `wsl-host` onboarding run reporting the wrong Core path**, with the repo owner directly requesting the reversal rather than accepting it as a cosmetic bug.

**The canonical location needs no elevation to write to** — a per-user directory under the platform's own data location — unlike a system-wide one, **keeping decision 7's "elevation is rare, only for the Core service" property intact for this new step too.**

**The copy step runs on every `setup`**, from the running `embarch` binary's own directory (wherever the archive was unpacked) into that location. **This is the *only* place "look at my own directory" logic remains** — a one-time install source at setup time, not an ongoing resolution mechanism. After one `setup`, the unpacked archive can be deleted.

**`PATH` mutation, done for real and idempotently, and the platform details are the decision:**

- *Windows*: edit the user-scope registry `Path` directly — **never `setx`, which silently truncates a `PATH` value over roughly 1024 characters, a real corruption risk rather than a hypothetical one.** The **raw** registry value is read and written back **with its original type intact**, because downgrading a `%VAR%`-expanding value to a plain string on write would be exactly the corruption this decision exists to avoid. Presence is checked case-insensitively before appending, and a settings-change broadcast lets open Explorer windows notice; **an already-open shell still needs restarting, which is an OS constraint no installer can work around.**
- *Unix*: write one small dedicated env file and add **one** idempotent sourcing line to whichever rc files already exist — never creating one that does not. **This is what resolves decision 3's original "which shell, which of four startup files?" objection**: only one line, sourcing one file, ever needs adding anywhere.

**Sibling lookup is deleted outright, not merely deprioritized.** Core and the API now resolve via env var → saved state → `PATH` → (WSL2 only) the real canonical Windows location, **found by shelling out for the real per-user path value, because WSL2 has no direct view of the Windows username needed to derive it by hand.**

**It fixes the `wsl-host` path misreport as a side effect:** locating the Windows-side binary becomes an **exact known constant instead of a bounded search.**

**Not fully verified, and the gap is named.** There is no Windows linker in this sandbox, so the Windows registry code was checked by **extracting it into a standalone throwaway crate** and type-checking it against the Windows target — real end-to-end behaviour (a registry write taking effect, a new shell picking up the change) still needs a real Windows machine. The Unix path and everything else is built, tested and clippy-clean on the host.

**The trade-off, accepted explicitly:** `setup` now writes outside the locations it already owned — a registry key and two dotfiles. Accepted because **every one of those writes is per-user, needs no elevation, and is idempotent and reversible**, which is materially less risk than the service install elevation was already required for.
