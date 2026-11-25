# 118 — `deploy-core` installs a development Core beside the service, and one command restores the service

**State:** open
**Source:** EMB-341 — `deploy-core` replaces the service, so development turns the bench unattested
**Issue:** EMB-341
**Scope:** umbrella
**Hardware:** verify-only
**Owner:** no

## What

`deploy.rs` syncs four crates, builds with Windows `cargo.exe`, then one
elevated script stops the service, copies the build over its registered binary
and starts it, with a SHA-256 check (decisions 32 and 50). From the attested
phase on that is wrong: every development deploy turns the attested install
unattested. The HIL design (`embarch-doc/notes/hil/12-prevention.md`, "The root
of trust"): `deploy-core` installs a development Core beside the service, run as
a process in the engineer's logon session, with its own store and token pair in
the engineer's profile, on the same port; the service stays registered and
stopped, and the hash check moves to the development binary; the stop refuses
while a run holds the lease unless the run is cancelled first. When this is
done, with the names and the start method recorded in the decision as the
plan's recommendation, the owner's to strike:

- Sync and build as today.
- Copy the build to `%LOCALAPPDATA%\embarch\dev\core\embarch-core.exe`. The
  hash check compares the build, the copy, and the running development Core's
  `/status` `binary_sha256`.
- If `/status` shows a study in flight, refuse unless `--cancel-run`, which
  cancels it first.
- If the service is running, stop it (one elevation).
- Stop the previous development Core by the PID `deploy-core` recorded, never
  by name.
- Start the development Core hidden in the logon session (`Start-Process
  -PassThru`) with `run --store %LOCALAPPDATA%\embarch\dev --bind <the
  service's registered bind>`; record its PID; wait for `/status` to read
  `development` with the new hash.
- **`deploy-core --restore-service`**: stop the development Core, start the
  service, wait for `/status` to read `service` with a key matching
  `core-fingerprint`.
- **The service's registration and binary are never written.** When the
  registered service is a source install (no `--service`), `deploy-core` says
  once that it is no longer updated and names `embarch install-core`.

## Where to look

- `src/deploy.rs` — `resolve_plan`, `elevated_script`, `deploy_core`, `landed`
- `src/state.rs` — the saved paths, and where the PID goes
- `embarch-doc/embarch-umbrella/decisions/deploy.md` (32, 50)
- `embarch-doc/notes/hil/12-prevention.md`, "The root of trust"
- `embarch-doc/embarch-core/interfaces/` for `/status`'s `binary_sha256` and
  its service/development field, and the cancel route; read only

## Where the doc goes

**Decision 32 is pinned with 29 B left** (`check-doc-size.py --pressure`), so
it cannot be amended in place: write a new decision that supersedes the part of
32 it changes, and put a one-line pointer in 32 only if it fits. Do not grow
agent-runtime#67 or agent-container#62 (over their limits), prune-policy#26,
mirrors#20 or the other entries the pressure list names.

**`open.md` is in reserve** (4,634 of 5,120 B) and its compaction,
`tasks/umbrella/111`, is `blocked` with `In flux: yes` because the install
subsystem is still moving. If this unit writes `open.md` at all, compact it as
part of this unit, keeping 111's `Must not delete:` list, and close 111's item
for that file. If it does not, leave `open.md` alone. `embarch-dev-workflow.md`
§4a describes the deploy loop and is the owner's; say in your report what it
now gets wrong, and do not edit it.

## Hardware verification

**Not measured**: any of it on the Windows machine. Leave a
hardware-verification debt for the owner's bench session: one `deploy-core`
with the service running, one with a study in flight (refused, then
`--cancel-run`), and one `--restore-service`, each checked against `/status`.

## Done when

- [ ] The stop, start and restore scripts are built by functions and
      golden-tested.
- [ ] Against a fake Core, a study in flight refuses without `--cancel-run`
      and is cancelled with it.
- [ ] The hash check fails when the running development Core's hash differs
      from the build.
- [ ] No step writes the service's registered binary path, with a test.
- [ ] A decision records the change to 32; a hardware-verification debt is
      left for the owner's bench session.
- [ ] Gate green.
