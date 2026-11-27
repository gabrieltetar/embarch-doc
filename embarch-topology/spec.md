# embarch-topology: spec

**Status:** active, 2026-09-07. Repo: [gabrieltetar/embarch-topology](https://github.com/gabrieltetar/embarch-topology).

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md).

## What it is

The suite's one abstraction for **topology**:

- **Software topology** — where each process runs relative to the others: API and Core on one machine, a WSL2-hosted API talking to native-Windows Core, or Core on a headless LAN box.
- **Hardware topology** — what is physically wired to what: which USB port carries a board's debug probe vs. its serial link, which board plays which role, and that role's current identity.

**The class of problem it exists to make impossible:** a stale port override winning silently over reality. Per decisions 2 and 3 **the override mechanism was removed, not merely detected** (decision 9, retired).

It is **not**:

- **A network service.** A library compiled in and called in-process — **nothing about it can be "down."**
- **A daemon or watcher.** Nothing stays running; **calling linked code directly *is* the live mechanism.**
- **A second implementation beside Core's enforcement.** Core's gate logic **moved into** this crate.
- **Scoped to multi-board or Pi-as-first-class yet.** Both deferred until either is real.

## Shape

```
one codebase, two things built from it:

  1. the shared crate — every piece of topology logic:
       - software class detection (local/wsl-host/remote) + bind-address rules
       - hardware detection: VID/port heuristics, live identity reads
         over the debug port
       - enrollment storage: which hardware_id plays which role, and what
         is wired to what — a human's declared intent, which detection
         cannot determine, so it's the one thing persisted
       - live validation, the durable alert log, and the structured
         mismatch error with its fix-it URL
  2. a thin CLI over the same crate: a human inspects always, and mutates
     (enroll/validate/set-dev-bench-link) only when no Core answers and
     no Core service is registered (OS read) — else it refuses and names Core's route (decision 28).
     Its local web UI half is retired (decision 5).

embarch-core, embarch-api and embarch-umbrella all depend on the crate
and call it live, in-process, at their own moment of need — no shell-out,
no hand-off file, no env var:

  Core, mid-flash/reset/run_study:  resolve_dev_bench_port() -> fresh every call
                                    validate(...) -> mismatch -> alert
  embarch-api, resolving "auto":    resolve_software_topology() -> every call
  umbrella's doctor:                resolve_*() / validate() -> pass/fail/warn
```

**The only state anything in this crate reads back as an input is a human's declared intent.** Consumers call functions and **never parse a topology file directly.** The durable alert log (Shape, above) is persisted too, but write-only from the crate's own point of view: nothing reads it back to resolve or validate anything, it exists for a human to review.

## The declared facts

Everything else is detected live. These cannot be:

| Fact | Why detection cannot produce it |
|---|---|
| **Which board is enrolled as which role** | No software can derive which board a probe is wired to — only a person isolating it and saying so |
| **What that board is called** | A name is a human's word for a physical object; `name` is recorded beside the role and interpreted by nothing here (decision 35) |
| **A link port's own USB serial** | The link can differ from the JTAG probe's USB device, and **no identity readback is possible over a plain UART** |
| **A link port's USB *interface*** | One probe can expose two VCOMs under one serial; **which one the console is wired to is a devicetree fact, not a USB one** |
| **A DUT signal's route** | A wire between two headers is invisible to software |
| **A DUT's bootload ports** (app and bootloader USB identities) | Zephyr's default VID:PID is shared by every board built from defaults (decision 36) |
| **A bench instrument** (USB identity, line facts, optional safe-off lines, optional metrology and calibration; a signal carries one safe-off line too) | A bridge's VID:PID is shared by every device on it; line facts are learned on the bench (decision 49); what a reading is worth is the person's declaration (decision 51) |

Storage: one file under the machine-wide directory this crate owns, one level below `embarch-core`'s token file by default; the linking process may set the folder once at start (decision 23), the directory resolved by one public resolver (decision 52); a store predating later facts still loads.

## Storage and roles

Moved to [spec/storage-and-roles.md](spec/storage-and-roles.md), 2026-09-17 (reserve split,
`tasks/topology/057`) — enrollment's write-time role uniqueness (decision 20), a declared link
serial/interface's guess-and-clear semantics (decisions 20, 27).

## What validation asserts, and what it cannot

Moved to [spec/validation.md](spec/validation.md), 2026-11-17 (reserve split,
`tasks/topology/070`) — the role, same-chip, requested-chip and signal-route checks, ID-read
retries, ARMv6 attach, `validate_*_timed` and `Validation.halts` (decisions 18, 26, 37-39, 44, 47, 48).

## What each consumer owns now

Moved to [spec/consumers.md](spec/consumers.md), 2026-10-26 (reserve split, `tasks/topology/060`) —
probe selection is this crate's (decisions 32, 33), what Core, `embarch-api` and `embarch-umbrella`
own, and the three features `software`, `wire` and `hardware` (decision 31).

## What a caller may assume across calls

**An answer is good only at the instant it was taken.** No cache, no watcher,
no invalidation signal — a caller may hold a result only for the one
operation it was taken for, never
across a retry or a later operation. A board unplugged, re-enrolled, or
moved between calls is invisible until the next call; **never cache a pass
as durable — re-call instead** (decision 29).

## What a release carries

A `v*.*.*` tag builds four archives (Windows `.zip`; Linux x86_64, Linux aarch64 and macOS arm64 `.tar.gz`). The build matrix holds no OIDC token and only uploads workflow artifacts; one `sign` job in `release.yml` itself, under the `release` environment (the owner approves, tag runs only) with `id-token: write`, signs each archive with cosign 3.0.4 or later (`cosign sign-blob --bundle`) and publishes every archive beside its `<archive>.sigstore.json` bundle. The signing stays in this file because the certificate's identity is the workflow at the tag. To check an asset:

```
cosign verify-blob <archive> \
  --bundle <archive>.sigstore.json \
  --certificate-identity https://github.com/gabrieltetar/embarch-topology/.github/workflows/release.yml@refs/tags/<tag> \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

Not yet run on a real tag: the first signed release is the first test (the suite assembly does not pull these archives today). Design: [release signing proposal](../embarch-release-signing-proposal.md).

## Where it stands

Both real boards are enrolled; a real flash-plus-study has run clean.

**The mismatch path is exercised, not just designed:** two different nRF54L15 DUTs have alternated on one probe three times, each tripping the gate (decision 12).

**No agent can induce one.** Every route pointing a role at other silicon runs through `enroll`, overwriting the record; **no override on the store path from outside** — the folder is the linking process's choice, set once at start (decision 23), and the default's only variable is `ProgramData`, unsettable once the service runs.

The register pair those reads use is confirmed against real silicon independently (decision 21). Everything else open: [open.md](open.md).
