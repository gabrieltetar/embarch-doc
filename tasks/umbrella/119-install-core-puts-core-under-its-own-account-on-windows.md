# 119 — `install-core` puts Core under its own account on Windows

**State:** open
**Source:** EMB-339 — The Windows install cannot put Core under its own account
**Issue:** EMB-339
**Scope:** umbrella
**Hardware:** verify-only
**Owner:** no

## What

`embarch install-core` (decision 61, `src/install_core.rs`) verifies a signed
release in an admin-only `<data dir>/release-staging/<n>/` and writes
`installed-release.json`; nothing after that is built. Today's Windows service
runs from wherever its binary sits, under the default account, beside a store
the engineer can write. The design this implements
(`embarch-doc/notes/hil/12-prevention.md`, "The root of trust"): Core's binary
is installed where the engineer's account cannot write, Core's protected store
is readable and writable by Core's account alone, the token files stay
readable, and the fingerprint is written by the elevated install beside the
token files, readable by the engineer and writable only by an elevated step.

When this is done, per the issue's direction (the owner moved it to Fleet Ready
with that direction, and says he may strike it; follow it, and record any
deviation in the decision): `install-core`'s elevated Windows half is a
generated PowerShell script, logged from inside the elevated context as
`deploy-core`'s is, with the engineer's SID passed in from the unelevated half.
In order:

1. `%ProgramFiles%\EmbArch\core\<version>\`: Administrators and SYSTEM full,
   Users read and execute; the verified binary copied in from the staging copy.
2. `%ProgramData%\embarch\store\`: refused if it exists owned by anyone but
   Administrators, SYSTEM or the service account; otherwise created with
   inheritance removed, granting `NT SERVICE\com.embarch.core`, SYSTEM and
   Administrators full, nobody else. It starts empty.
3. `%ProgramData%\embarch\staging\` (the firmware staging folder, not
   `release-staging`): Administrators full, the service read, the engineer
   write.
4. The token files: written when absent; each grants the service account and
   Administrators full and the engineer read.
5. The installed binary's `install --service --bind <addr>` (Core decision
   157), which registers it under the virtual account, rewriting an existing
   registration in place.
6. Start, wait for `RUNNING`, read `store\public-key`, and write
   `core-fingerprint` (the SHA-256 of the key) beside the token files:
   Administrators write, Users read. Print the fingerprint.

**Step 5 refuses today, and that is yours to fix.** Core's `install --service`
registers only a binary whose SHA-256 is an entry of `binary_sha256`, an array
of lowercase hex, in `<data dir>/installed-release.json`
(`embarch-doc/embarch-core/interfaces/installed-release.md`). The record
`install-core` writes has a `binaries` map and no `binary_sha256`, so as built
the script would fail at step 5. Add `binary_sha256` to the record (additive;
keep `binaries`), and update `interfaces/install-core.md`.

**Not yours:** `embarch-core` (its `install --service`, token files and store
are as they are; if you find Core must change, write it into this file as a
finding and stop short of it), `setup` and `doctor`'s wording (`umbrella/121`),
the Linux half (`umbrella/120`), and every other repo. You never touch
hardware and never run anything elevated: build the script with a function and
golden-test it, and drive the run through a fake host, as `deploy-core`'s
tests do.

## Where to look

- `src/install_core.rs` (decision 61); `src/deploy.rs` and `src/deploy_dev.rs`
  — `RealHost::run_script` with its transcript, and the `deploy_dev::Host`
  seam, the pattern to follow
- `embarch-core/src/token_store.rs` (read only) — the token files' current
  `icacls` lockdown
- `embarch-doc/embarch-umbrella/decisions/install-core.md` (61, 3.5 KB),
  `decisions/deploy.md` (32), `decisions/topology.md` (7),
  `interfaces/install-core.md`; `embarch-doc/embarch-core/decisions/platform.md`
  (157, read only); `embarch-doc/notes/hil/12-prevention.md`,
  `notes/hil/14-implementation-plan.md` (A.19)

## Where the doc goes

A new umbrella decision in `decisions/install-core.md` beside 61, with an index
row (take the next free number by scanning the headings, as
`DOC-CONVENTIONS.md` says, and cite only that number in code comments).
**Over or near the per-decision cap, do not grow:** `agent-runtime#67`,
`agent-container#62`, `deploy#32` (29 B left), `prune-policy#26`.

**`open.md` is in reserve (4,634 of 5,120 B; out at 3,919 B or less), and its
compaction `umbrella/111` is parked on `In flux: yes` until the install-core
follow-ups land; this unit is one of them.** So compact `open.md` as part of
this unit under `DOC-COMPACTION.md`, keeping every line of 111's
`Must not delete:` list (the `install-core` debt, check 15's `binary_sha256`,
check 17's stopped arm, the desk steps of decision 58), and rewrite the
`install-core` line to say what is now built and what is not. Do not edit
`tasks/umbrella/111`; the supervisor closes it at the fold if `open.md` leaves
reserve.

## Done when

- [ ] The script is built by a function and golden-tested, step by step.
- [ ] The transcript parser names each failed step and exits non-zero; a
      missing transcript is a failure (decision 50's rule).
- [ ] A pre-existing store with a foreign owner is refused in the script
      before anything is written.
- [ ] `--dry-run` prints the plan, the paths and the ACLs it would set.
- [ ] `installed-release.json` carries `binary_sha256` in Core's shape, tested.
- [ ] Windows-gated code type-checks for `x86_64-pc-windows-msvc` (a
      throwaway crate is the known route, decision 61's note); a
      hardware-verification debt for the owner's first elevated install is
      written into this file and `open.md`.
- [ ] `open.md` is out of reserve with 111's list intact.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
