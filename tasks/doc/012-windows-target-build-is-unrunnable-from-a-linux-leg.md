# 012 — §10's native Windows build cannot run from any Linux worktree, and every `embarch-core` unit is told to run it

**State:** open
**Source:** `core/004`'s worker (leg 014, 2026-09-05), dropped in `inbox/` as
`core-windows-target-build-unrunnable-in-wsl.md` and drained here by leg 015. The
supervisor of leg 014 reproduced the failure itself on the unmodified base rather than
taking the worker's word, and merged `core/004` with this gate item red — see that
unit's log entry, whose "least sure about" is exactly this.
**Scope:** doc
**Hardware:** none
**Owner:** required — the drop arrived labelled `Scope: core`, and **reclassified at
drain**: every remedy in its own *Done when* is either `../../embarch-fleet/protocol.md`
§10 (reserved from workers *and* supervisors, protocol §3) or installing a cross-compile
toolchain on this machine. A `core` worker handed it would go red on
`check-ownership.py` on its first write, so leaving it in the `core` queue would have put
a permanently-undispatchable task where a leg would dispatch it.

## What

`protocol.md` §10 requires "a native Windows build where `embarch-core` is involved". From
a Linux checkout `cargo build --target x86_64-pc-windows-msvc` fails in a **dependency's
build script**, before any `embarch-core` code compiles:

    error occurred in cc-rs: command did not execute successfully (status code exit
    status: 1): LC_ALL="C" "cc" ... "-I" "etc/hidapi/hidapi" ... "-c"
    "etc/hidapi/windows/hid.c"

`hidapi`'s `build.rs` compiles `windows/hid.c` with the host `cc`; WSL has no
MSVC-flavoured C compiler or Windows SDK headers, and the MSVC link step would fail next
even if the C compile did not. The rustup target alone supplies neither.

`embarch-core/.github/workflows/release.yml` builds this target on a native
`windows-latest` runner, and `Cross.toml` configures `cross` only for
`aarch64-unknown-linux-gnu` — so **there is no configured path for a Linux checkout to
produce this target at all.** The gate item asks every Linux worker and every leg for
something the repo has never been set up to do locally.

## Measured 2026-09-06 (owner's session), and it narrows the claim

**"There is no configured path for a Linux checkout to produce this target at all" is
false, and the true statement is sharper.** Three results, all run on this machine:

| what | result |
|---|---|
| Linux `cargo build --target x86_64-pc-windows-msvc` | **fails** in `hidapi`'s `build.rs`, as recorded above |
| Windows `cargo.exe build --target x86_64-pc-windows-msvc --manifest-path <UNC to the **main checkout**>` | **works — 52 s, links, 37 MB `embarch-core.exe`** |
| Windows following a **Linux symlink** over UNC | **False** |

The second row uses the same `/mnt/c/Users/tmp12/.cargo/bin/cargo.exe` that `deploy-core`
already depends on, over `\\wsl.localhost\...`. Windows reads the WSL manifest, runs every
build script including `hidapi`'s, resolves both path-dep siblings and links. So the
capability exists, is already installed, and takes under a minute.

**The third row is why the gate item is still unsatisfiable for a leg, and it is a different
reason than the one filed.** A worker's worktree does not contain its path-dep siblings — the
supervisor **symlinks** them in (`supervise.md`'s closure table), and Windows cannot traverse
a Linux symlink over UNC. So the native build succeeds from the main checkout and fails in
every worker and leg worktree, at path-dep resolution rather than at `hidapi`.

**What that changes about the remedy.** The requirement is not impossible and should not be
dropped; it is **unsatisfiable in the place §10 asks for it and satisfiable in the place the
owner works.** That makes it the same shape as a hardware-verification debt (§7): the worker
ships the host-side half and records that the native Windows build is owed, and the owner
runs it from the main checkout in one command. Dropping it outright would lose a real check —
`embarch-core` is Windows-only in production, and CI only builds it on push to `main`.

Whoever lands this should re-measure the second row rather than trusting this table; it was
`cargo build` at debug, not `--release`, and the probe target directory (2.4 GB) was deleted
afterwards.

## Why now

The outcomes available today are all bad. A worker reports a red it did not cause and
burns a merge slot being re-checked; or it learns to wave the item through, which is
worse, because `#[cfg(windows)]` service code is real compiled code and a native-target
break is a real break. **Leg 014 took the third path — merged over it after reproducing
it — which normalises skipping the item one unit at a time.** That leg's own entry says
the honest position is that this suite has never gate-checked a Windows build from a leg
and should say so out loud rather than let each supervisor re-make the judgement call
privately.

## Done when

- [ ] It is decided whether a Linux worktree can build `x86_64-pc-windows-msvc` at all.
      Try `cargo-xwin`; note `hidapi`'s C source is the specific obstacle, not just the
      linker, so a linker-only solution is not enough.
- [ ] If it can: the tooling is installed and §10 names the exact command.
- [ ] If it cannot: §10 says so in as many words, and says what an `embarch-core` worker
      and a supervisor do instead — e.g. assert no `#[cfg(windows)]`/`#[cfg(unix)]` code
      was touched, cite the release workflow, and record that assertion in the unit's log
      entry.
- [ ] Either way, no `embarch-core` worker is left reporting a red it cannot act on, and
      no supervisor is left deciding per-unit whether to merge over it.
