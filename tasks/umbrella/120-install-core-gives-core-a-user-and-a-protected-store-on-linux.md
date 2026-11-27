# 120 — `install-core` gives Core a user of its own and a protected store on Linux

**State:** claimed by agent/umbrella/120-install-core-gives-core-a-user-and-a-protected-store-on-linux, 2026-11-27 00:27
**Source:** EMB-340 — On Linux, Core has no account of its own and no protected store
**Issue:** EMB-340
**Scope:** umbrella
**Hardware:** verify-only
**Owner:** no

## What

On Linux, Core's `install` registers a systemd unit with no `User=`, and its
token files are `0600` for whoever created them, so the engineer could not read
them if Core ran as another user. The design this implements
(`embarch-doc/notes/hil/12-prevention.md`, "The root of trust"): on Linux, a
system service with a user of its own; the token file stays readable.
`embarch-token.md` §5 says the Linux service path ships as code and is not
service-validated.

When this is done, per the issue's direction (the owner moved it to Fleet Ready
with that direction, and says he may strike the Linux half; follow it, and
record any deviation in the decision): `install-core`'s privileged half on
Linux is a generated shell script run under `sudo`:

- A system user `embarch` with no login shell, when absent; added to the
  groups that own serial and USB devices where they exist (`dialout`,
  `plugdev`; distribution-dependent, so the script checks each exists).
- `/opt/embarch/core/<version>/`, root-owned, `0755`, with the verified binary
  from the staging copy.
- A group `embarch-users` holding the engineer (`$SUDO_USER`) and `embarch`.
- `/var/lib/embarch/` root-owned `0755`; `store/` `embarch:embarch` `0700`,
  empty; `staging/` (firmware, not `release-staging`) `root:embarch-users`
  `0770`.
- Token files written when absent, `embarch:embarch-users` `0640`.
- The binary's `install --service --bind <addr>` (Core decision 157), which
  writes the unit with `User=embarch`.
- Start, read `store/public-key`, write `core-fingerprint` root-owned `0644`
  (the SHA-256 of the key), print it.

**Step "install --service" refuses unless `installed-release.json` lists the
binary in `binary_sha256`** (`embarch-doc/embarch-core/interfaces/installed-release.md`).
`umbrella/119` adds that field to the record; if it has landed, use it, and if
it has not, add it as 119 describes rather than a second shape.

**Not yours:** `embarch-core` (whether its unit writer sets `User=embarch`
under `--service` is Core's; if it does not, write that into this file as a
finding for a Core task and stop short of it), the Windows half
(`umbrella/119`), `setup` and `doctor`'s wording (`umbrella/121`), and every
other repo. You never touch hardware and never run `sudo`: build the script
with a function, golden-test it, and drive the run through a fake host.

## Where to look

- `src/install_core.rs` (decision 61) and whatever `umbrella/119` added beside
  it; `src/deploy_dev.rs`'s `Host` seam
- `embarch-core/src/service.rs`, `src/token_store.rs` (read only)
- `embarch-doc/embarch-umbrella/decisions/install-core.md`,
  `decisions/install.md` (54), `interfaces/install-core.md`;
  `embarch-doc/embarch-token.md` §5; `embarch-doc/notes/hil/12-prevention.md`,
  `notes/hil/14-implementation-plan.md` (A.19)

## Where the doc goes

A new umbrella decision in `decisions/install-core.md`, with an index row (take
the next free number by scanning the headings, as `DOC-CONVENTIONS.md` says,
and cite only that number in code comments). `embarch-token.md` is a
suite-level doc: if its §5 is now false, write a `status.d/umbrella-*`
fragment saying what changed rather than editing it. **Over or near the
per-decision cap, do not grow:** `agent-runtime#67`, `agent-container#62`,
`deploy#32`, `prune-policy#26`. If `open.md` is still in reserve when you
start, keep your edit to it net-neutral or smaller.

## Done when

- [ ] The script is built by a function and golden-tested.
- [ ] A pre-existing `store/` not owned by `embarch` is refused before anything
      is written.
- [ ] `--dry-run` prints every command and changes nothing.
- [ ] A hardware-verification debt for the owner's run in a scratch distro is
      written into this file and `open.md`.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
