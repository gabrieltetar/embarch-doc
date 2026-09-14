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

**The only state that persists anywhere is a human's declared intent, inside the crate.** Consumers call functions and **never parse a topology file directly.**

## The declared facts

Everything else is detected live. These four cannot be:

| Fact | Why detection cannot produce it |
|---|---|
| **Which board is enrolled as which role** | No software can derive which board a probe is wired to — only a person isolating it and saying so |
| **A link port's own USB serial** | The link can differ from the JTAG probe's USB device, and **no identity readback is possible over a plain UART** |
| **A link port's USB *interface*** | One probe can expose two VCOMs under one serial; **which one the console is wired to is a devicetree fact, not a USB one** |
| **A DUT signal's route** | A wire between two headers is invisible to software |

Storage: one file under the machine-wide directory this crate owns, one level below `embarch-core`'s token file (decision 23); a store predating later facts still loads.

## Storage and roles

**A role is unique.** Enrolling displaces any other board holding that role; the displaced row is **returned, not dropped** (decision 20).

**A declared link serial or interface can also be *unset*** (`set-dev-bench-link --clear-serial`/`--clear-interface`): `NotFound` names which rule emptied the candidate list and routes to clearing it (decision 27).

**A detected port says whether it was guessed** — the result carries how many candidates the lowest-interface rule chose among, **so a caller reports "COM16, guessed among 2" rather than "COM16".**

**The declared *interface* decides which of the two VCOMs is the console** — `COM16` and `COM17` differ in nothing else a detector can read, and it is wired to the **higher** one. Remove the declaration and resolution does not bail — it warns, sorts by interface, takes the lowest, and reports the wrong port **as a guess** (decision 20).

**`guessed_among`'s trigger is an *under-declared* bench, not a crowded one** — adding probes cannot produce a guess while an interface is declared.

## What validation asserts, and what it cannot

- **A role:** the enrolled probe is enumerated and its live identity still matches the recorded one; runs on every flash, reset and handshake.
- **A same-chip link:** the board on the runtime link is the same silicon the JTAG probe verified, comparing its JTAG-read identity against its self-report. **Two chip families have a declared relation; every other chip returns *undeclared*, never a pass.**
- **A direct signal route:** the declared serial is enumerable. It **cannot** confirm the DUT's TX pin wire lands on that bridge.
- **A via-bench route:** validates on the strength of being declared; its carrier is the bench link, whose liveness is the role check's job (decision 18).

**A signal mismatch is not written to the alert log** — an alert's shape is board-specific and a wire has none of them.

A validate call previously carried only the enrolled record's `confirmed_at_utc_ms` — enrolment time, not this check's. `validate_serial_timed`/`validate_role_timed` add `validated_at_utc_ms`, its own pass instant, beside unchanged `validate_serial`/`validate_role` (decision 26). `embarch-core`'s `POST /validate` exposes it via `validate_role_timed`, populating `ValidateOkResponse.validated_at_utc_ms` from the returned `Validation` (`embarch-core` decision 50).

## What each consumer owns now

- **Probe selection is this crate's, not `embarch-core`'s.** `select_probe` (decision 32) is the
  suite's one implementation of which attached debug probe a caller gets; `embarch-core::resolve_probe`
  delegates to it rather than holding a copy, threading a caller `action` verb (`"enroll"`, `"flash"`,
  `"reset"`, …) through for its error text. Three observable behaviours a caller can rely on
  (decision 33): **zero probes attached** is checked first and always names the usbipd hint; **more
  than one probe attached with no serial given** refuses, naming the count and every attached probe's
  identifier and serial; **a given serial that matches nothing attached** refuses by name. Every error
  string is part of the contract — see decision 33 for the exact wording of each.
- **`embarch-core`** keeps the hardware I/O, calling the crate for which port or probe, and whether valid — no copy of that logic, and **no dev-bench port override env var.**
- **`embarch-api`** links the crate **without the hardware feature** — only its `base_url = "auto"` branch calls it; the declared-address fast path does not.
- **`embarch-umbrella`** does the same; its env module is **just "am I under WSL2"**, still needed standalone by its Windows-binary lookup.

**Three features, and the middle one is new** (decision 31). `software` (default) is topology-class detection and Core-reachability probing, needing `reqwest`/`tokio`. `wire` is `serde` and nothing else: the hardware module's plain data types — `EnrolledBoard`, `Alert`, `DetectedPort`, `SignalLink`, `Route`, `SignalDirection` — with every function that reads a probe, enumerates a port or writes `enrollment.toml` compiled out. `hardware` is those functions, implies `wire`, and needs `probe-rs`/`serialport`; `embarch-core` is its only consumer.

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
