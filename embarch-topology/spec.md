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
     (enroll/validate/set-dev-bench-link) only when no Core answers on
     this machine — else it refuses and names Core's route (decision 28).
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
| **A bench instrument** (USB identity and line facts) | A bridge's VID:PID is shared by every device on it; line facts are learned on the bench (decision 49) |

Storage: one file under the machine-wide directory this crate owns, one level below `embarch-core`'s token file (decision 23); a store predating later facts still loads.

## Storage and roles

Moved to [spec/storage-and-roles.md](spec/storage-and-roles.md), 2026-09-17 (reserve split,
`tasks/topology/057`) — enrollment's write-time role uniqueness (decision 20), a declared link
serial/interface's guess-and-clear semantics (decisions 20, 27).

## What validation asserts, and what it cannot

- **A role:** the enrolled probe is enumerated and its live identity still matches the recorded one; runs on every flash, reset and handshake.
- **A same-chip link:** the board on the runtime link is the same silicon the JTAG probe verified, comparing its JTAG-read identity against its self-report. **An exact match settles it for any chip** — two mechanisms agreeing byte for byte on a factory-unique value is conclusive on its own. Two chip families additionally have a declared relation, for when the two mechanisms format that same value differently; every chip with neither an exact match nor a declared relation returns *undeclared*, never a pass.
- **A requested chip:** `validate_serial_for_chip` compares the chip a caller asks for with the enrolled row's, by name and ignoring case, **before the probe is opened**; a differing chip is a `RequestedChipMismatch` naming the probe, the enrolled board and the re-enroll call, and equal names fall through to the identity checks unchanged (decision 44).
- **A direct signal route:** the declared serial is enumerable. It **cannot** confirm the DUT's TX pin wire lands on that bridge.
- **A signal Core may write** is `host-to-dut` or `bidirectional` on a direct route (`SignalLink::host_can_write`, decision 37); a signal may declare its own `baud`, else Core's default applies.
- **A signal's origin** is a role or, through `origin_board`, an enrolled role-less bench board by its probe serial; `declare` resolves a board's name to that serial and refuses an unenrolled board, an ambiguous name or a role's probe (`SignalLink::origin`, `find_signal_origin_board`, decision 48).
- **An ID whose words are all the same** is retried once, then read with the core halted for microseconds, then a failed read, never a mismatch (decisions 38, 39). An STM32G0's UID is always read halted (decision 39).
- **Attaching to an ARMv6 STM32** (F0, L0, G0) goes through `hardware::attach::attach`, which never read-modify-writes RCC or DBGMCU on a running core (decision 39).
- **A via-bench route:** validates on the strength of being declared; its carrier is the bench link, whose liveness is the role check's job (decision 18).

**A signal mismatch is not written to the alert log** — an alert's shape is board-specific and a wire has none of them.

A validate call previously carried only the enrolled record's `confirmed_at_utc_ms` — enrolment time, not this check's. `validate_serial_timed`/`validate_role_timed` add `validated_at_utc_ms`, its own pass instant, beside unchanged `validate_serial`/`validate_role` (decision 26). `embarch-core`'s `POST /validate` exposes it via `validate_role_timed`, populating `ValidateOkResponse.validated_at_utc_ms` from the returned `Validation` (`embarch-core` decision 50). `Validation.halts` says how many times the identity gate halted the core (0 if already halted or the family reads without halting), so Core need not infer it (decision 47).

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

## Where it stands

Both real boards are enrolled; a real flash-plus-study has run clean.

**The mismatch path is exercised, not just designed:** two different nRF54L15 DUTs have alternated on one probe three times, each tripping the gate (decision 12).

**No agent can induce one.** Every route pointing a role at other silicon runs through `enroll`, overwriting the record; **no override on the store path** — its only variable is `ProgramData`, unsettable once the service runs.

The register pair those reads use is confirmed against real silicon independently (decision 21). Everything else open: [open.md](open.md).
