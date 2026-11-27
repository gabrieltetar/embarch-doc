# 124 — install-core grants start and stop only when the engineer states a container, and `down` refuses under a study

**State:** open
**Source:** EMB-342 — every switch between the service and a development Core needs elevation
**Issue:** EMB-342
**Scope:** umbrella
**Hardware:** verify-only
**Owner:** no

## What

Where the agent runs in a container, the HIL design lets the engineer's account
start and stop the Core service without elevation, and never change it
(`embarch-doc/notes/hil/12-prevention.md`, "The root of trust": the grant is
written only by the elevated install, and a later change of the engineer's
statement never widens it). Nothing writes that grant today. When this is done:

- `install-core --agent-in-container` makes the elevated half write one grant:
  - **Windows:** one ACE added to the `com.embarch.core` service's security
    descriptor (`sc sdshow` then `sc sdset`) giving the engineer's SID start,
    stop and query status only, never change-config, write-DAC or write-owner.
    The SDDL rights for that are believed to be `RP` (start), `WP` (stop),
    `LC` (query status), plus `LO`/`CR` only if the service manager needs them;
    that list is from memory, so check it against the SDDL service-rights
    table and write in the decision which letters you chose and why. The
    descriptor edit is a **pure function** (descriptor text in, descriptor text
    out) that adds exactly one ACE for the given SID and keeps every other ACE
    in order, golden-tested.
  - **Linux:** a polkit rule letting the engineer's user start and stop the
    Core unit only (the unit name decision 70 assumes), golden-tested, naming
    no other unit and no other verb.
- Without the flag, the generated script has **no grant step at all** (tested
  on both platforms' scripts).
- The statement is recorded in `installed-release.json` with its date
  (`serde(default)` so an older record reads). Only a new elevated install
  changes it. Its home in Core's store and the report's label are a later pass
  and not this task's.
- `embarch down` refuses while Core's `/status` shows a study in flight, and
  `down --cancel-run` cancels it first, reusing `deploy_dev::clear_study`
  (which `deploy-core --cancel-run` already uses). Tested against a fake Core.

Core's own half — `start` and `stop` trying without elevation before they
elevate — is `tasks/core/190`, not this task. The two land independently: a
grant with no unelevated attempt changes nothing, and an unelevated attempt with
no grant is refused and elevates as today.

**Not yours:** every other repo. You never touch hardware, never run the
generated scripts elevated, and never edit a real service descriptor.

## Where to look

- `src/install_core.rs` (the Windows script, decision 69; the Linux script,
  decision 70; `parse_transcript`, the `Host` seam), `src/setup.rs` (`down`),
  `src/deploy_dev.rs` (`clear_study`, `CoreApi`), `src/main.rs` (`Down`)
- `embarch-doc/embarch-umbrella/decisions/install-core-platforms.md` (69, 70),
  `decisions/install-core.md` (61, 71), `interfaces/install-core.md`,
  `spec/commands.md`, `decisions/topology.md` (7)
- `embarch-doc/notes/hil/12-prevention.md`, "The root of trust"

## Where the doc goes

A new umbrella decision for the grant and the `down` refusal. No umbrella file
is in reserve; `install-core-platforms.md` is 6,794 B and `install-core.md`
5,855 B, so either has room. Name the passkey case as out of scope in the
decision: the design says a registered passkey also means no grant, and no
passkey registration exists yet.

## Done when

- [ ] The descriptor edit is a pure function, golden-tested: one ACE for the
      given SID with start, stop and query only; every other ACE kept.
- [ ] The polkit rule is golden-tested and names only start and stop of the
      one unit.
- [ ] Without `--agent-in-container`, neither generated script has a grant step.
- [ ] `installed-release.json` records the statement and its date; an older
      record still reads.
- [ ] Against a fake Core, `embarch down` refuses under a study and cancels it
      with `--cancel-run`.
- [ ] A hardware-verification debt in this file for the owner's machine:
      an elevated install with the flag, then an unelevated `sc stop` / `sc
      start` (or `systemctl stop` / `start`) as the engineer succeeds and an
      `sc config` (or unit edit) is refused.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); decision, `interfaces/install-core.md`, `spec/commands.md`
      updated; `changelog.d/` fragment.
