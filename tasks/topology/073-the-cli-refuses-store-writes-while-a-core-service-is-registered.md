# 073 — The CLI refuses store writes while a Core service is registered

**State:** done — CLI refuses store writes while a Core service is registered; fake-registry tests, Windows read type-checked in a scratch crate; real-service run is a debt
**Source:** `notes/hil/12-prevention.md` — the protected store bullet and item 3: the topology CLI refuses to write the identity store while a Core service is installed
**Issue:** EMB-322
**Scope:** topology
**Hardware:** verify-only
**Owner:** no

## What

`refuse_if_core_reachable` (`bin/main.rs`) probes the port `--core-port` names
(decisions 28, 45); when nothing answers, the mutating subcommands run
in-process. Nothing asks the OS whether a Core service is registered, so with
the service stopped, or listening elsewhere, the CLI writes the store itself.

When this is done a `ServiceRegistry` seam answers "is a Core service
registered, and what bind does it name": on Windows the `com.embarch.core` key
under `HKLM\SYSTEM\CurrentControlSet\Services` and its `ImagePath`; on Linux
the `embarch-core` systemd unit; under WSL2 the Windows side through
`sc.exe qc com.embarch.core`, as `embarch deploy-core` reads it
(`embarch-umbrella/src/deploy.rs`, read only). Then:

- **Registered**: every store write is refused (enrol, unenrol, set-board,
  set-dev-bench-link, validate's store update), naming the Core route that owns
  it and the decision.
- **Registered and answering**: refused as today (decision 28 kept), probing
  the bind the registration names as well as `--core-port`.
- **Registered and stopped**: store writes refused; a stopped Core holds no
  lease, so a hardware read is admitted.
- **Not registered**: local bootstrap as today.
- `list` and `alerts`, when the registration runs `--service`, say the store
  is Core's and name `GET /probes/enrolled` and Core's alerts instead of
  reading a stale file.

## Why now

The attested install makes Core the identity store's only writer, and the call
log claims to hold every hardware call made to Core (EMB-322). Nothing else in
the attested chain blocks this one.

**Burndown leg: no new numbered decision.** Amend decisions 23 and 28 in place.
If the work genuinely needs a new decision, stop and say so in this file.

**Decision sizes (dispatch note):** `decisions/storage.md`#23 is already
**over** the per-decision cap (4,612 B against 4,096); your amendment must not
grow it, so make room inside 23 (move rationale to `spec.md` or `cli.md`, which
restates nothing) or state the new rule where it fits and leave 23 a one-line
pointer to it. `decisions/enrollment.md`#35 has 14 B left and
`link-declares.md`#20 29 B; neither is this task's. `spec.md` (7,646 B) is not
in reserve.

## Done when

- [x] With a fake registry: registered and stopped refuses each store write,
      naming its Core route; not registered bootstraps as today.
- [x] Registered and answering on a non-default bind refuses, with no
      `--core-port` given.
- [x] Each arm's refusal happens before any probe or store is opened.
- [x] The Windows registry read type-checks for `x86_64-pc-windows-msvc`
      (`cargo check --target x86_64-pc-windows-msvc`; the target is installed).
- [x] Decisions 23 and 28 amended; `cli.md` and `spec.md` say what holds.
- [x] A hardware-verification debt in this file for the owner's bench session:
      a real registered service, stopped and running, on Windows and under WSL2.
- [x] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped.

## Hardware-verification debt

Owner's bench session, on a real registered service (nothing here ran against one):

- **Windows**: `reg query HKLM\SYSTEM\CurrentControlSet\Services\com.embarch.core /v ImagePath` parses (a `--bind` after a quoted exe path); `embarch-topology enroll`, `unenroll`, `set-board`, `validate`, `set-dev-bench-link` each refuse with the service stopped and running, and with Core on a non-default `--bind`, no `--core-port` given. After `embarch-core uninstall`, `enroll` bootstraps locally again.
- **WSL2**: the same five commands through `sc.exe qc com.embarch.core` and through an `embarch-core` systemd unit if one exists; and `list`/`alerts` against a service registered with `--service` (Core's installer writes no `--service` flag today, so this arm is exercised only by a hand-registered command line).
- **Not run**: `cargo check --target x86_64-pc-windows-msvc` of the whole binary dies in `hidapi`'s `build.rs` (no MSVC `cc` in WSL, the known debt). The Windows-only code in `bin/registry.rs` was type-checked in a scratch crate on that target instead, with `DEFAULT_CORE_PORT` stubbed.
- Core's `--service` flag is not in `embarch-core/src/main.rs` today; the parse is ready for it.
