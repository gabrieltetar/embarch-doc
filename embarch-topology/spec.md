# embarch-topology: spec

**Status:** active, 2026-09-02. Repo: [gabrieltetar/embarch-topology](https://github.com/gabrieltetar/embarch-topology).

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md).

## What it is

The suite's one abstraction for **topology**, meaning two things that were previously handled ad hoc across env vars, config files and doctor checks in three different repos:

- **Software topology** — where each process runs relative to the others: the API and Core on one machine, a WSL2-hosted API talking to a native-Windows Core, or Core moved to a headless box on the LAN.
- **Hardware topology** — what is physically wired to what: which USB port carries a board's debug probe versus its serial link, which physical board plays which role, and what that role's board identity currently is.

**The class of problem it exists to make impossible:** a stale port override winning silently over reality. Per decisions 2 and 3 **the override mechanism was removed rather than merely detected**, so nothing is left that can win; retired decision 9 carries the incident that proved it.

It is **not**:

- **A network service the other components query.** It ships as a library they compile in and call in-process — **nothing about it can be "down" the way a service call can fail.**
- **A daemon or watcher.** Nothing stays running for Core to get a live answer; **calling linked code directly *is* the live mechanism.**
- **A second implementation alongside Core's own enforcement.** Core's gate logic **moved into** this crate; Core's job became calling it, not maintaining a copy.
- **Scoped to multi-board or Pi-as-first-class modelling yet.** Both explicitly deferred until either is real.

## Shape

```
one codebase, two things built from it:

  1. the shared crate — every piece of topology logic:
       - software class detection (local/wsl-host/remote) + bind-address rules
       - hardware detection: VID/port heuristics, live identity reads
         over the debug port
       - enrollment storage: which hardware_id plays which role, and what
         is wired to what — a human's declared intent, which detection
         cannot determine, so this is the one thing genuinely persisted
       - live validation, the durable alert log, and the structured
         mismatch error with its fix-it URL
  2. a thin CLI over the same crate, for a human to inspect or fix
     directly. Its local web UI half is retired (decision 5).

embarch-core, embarch-api and embarch-umbrella all depend on the crate
and call it live, in-process, at their own moment of need — no shell-out,
no hand-off file, no env var:

  Core, mid-flash/reset/run_study:  resolve_dev_bench_port() -> fresh, every call
                                    validate(...) -> mismatch -> structured
                                      error + durable alert
  embarch-api, resolving "auto":    resolve_software_topology() -> every invocation
  umbrella's doctor:                resolve_*() / validate() -> pass/fail/warn
```

**The only state that persists anywhere is a human's declared intent, and it lives inside the crate.** Consumers call functions; **they never parse a topology-owned file directly.**

## The declared facts

Everything else is detected live. These four cannot be:

| Fact | Why detection cannot produce it |
|---|---|
| **Which board is enrolled as which role** | No software can derive which physical board a probe is wired to — only a person physically isolating it and saying so |
| **A link port's own USB serial** | The link can be a different physical USB device from the JTAG probe, and **no identity readback is possible over a plain UART** |
| **A link port's USB *interface*** | One probe can expose two VCOMs under one serial; **which one the console is wired to is a devicetree fact, not a USB one** [confirmed live 2026-09-06] |
| **A DUT signal's route** | A wire between two headers is invisible to software |

Storage is one file under a machine-wide directory this crate owns — the same one `embarch-core`'s token file uses, one level down (decision 23). A store predating any of the later facts still loads.

## Storage and roles

**A role is unique.** Enrolling displaces any other board holding that role, and the displaced row is **returned rather than dropped silently**, so the caller can say out loud that one board replaced another. Two rows claiming one role would leave the by-role lookup answering with whichever came first in the file — **the unplugged board, carrying a dead link serial that narrows resolution to a port that cannot exist** (decision 20).

**A detected port says whether it was guessed.** When several candidates were resolved by the lowest-interface rule, the result carries how many it was guessed among, **so a caller reports "COM16, guessed among 2" rather than "COM16"** — every bench with one VCOM declares nothing, **but a guess says so.** This crate's own CLI is one such caller.

**The declared *interface* is load-bearing, and is the only thing separating the two VCOMs a DK's onboard probe exposes under one serial:** `COM16` and `COM17` differ in nothing else a detector can read, and the console is wired to the **higher** one. Remove the declaration and resolution does not bail — it warns, sorts by interface, takes the lowest, and reports the wrong port **as a guess.** The failure signature is a bench that flashes, boots, runs, and times out waiting for a handshake (decision 20).

**`guessed_among`'s trigger is an *under-declared* bench, not a crowded one.** Adding probes cannot produce a guess while an interface is declared, so exercising the field takes a deliberate omission. Nothing has yet observed it set.

## What validation asserts, and what it cannot

- **A role:** the enrolled probe is currently enumerated and its live identity still matches the recorded one. Runs on every flash, reset and handshake.
- **A same-chip link:** the board answering on the runtime link is the same silicon the JTAG probe verified, by comparing the JTAG-read identity against the board's self-report. **Two chip families have a declared relation; every other chip returns *undeclared*, which is never treated as a pass — a comparison that could not be made is not a comparison that succeeded.**
- **A direct signal route:** the declared serial is currently enumerable. It **cannot** confirm the wire from the DUT's TX pin actually lands on that bridge.
- **A via-bench route:** validates on the strength of being declared; its carrier is the bench's link, whose liveness is the role check's job (decision 18 for why not both).

**A signal mismatch is deliberately not written to the durable alert log** — an alert's shape is board-specific and a wire has none of those fields.

## What each consumer owns now

- **`embarch-core`** keeps the hardware-I/O plumbing — actually opening a probe or port handle — and calls the crate for *which* port or probe, and whether it is still valid. It holds no copy of the identity-recheck logic, the board storage, the identity reads or the port heuristic, and **there is no dev-bench port override env var, with no replacement.**
- **`embarch-api`** links the crate **without the hardware feature — `cargo tree` confirms the probe and serial crates never appear.** Only its `base_url = "auto"` branch calls the crate; the declared-address fast path does not.
- **`embarch-umbrella`** does the same; its own env module is **just "am I under WSL2"**, still needed standalone by its Windows-binary lookup.

## Where it stands

Both real boards are enrolled and a real end-to-end flash plus study has completed clean.

**The mismatch path is exercised, and nothing had to inject anything.** The bench met the precondition — a second same-chip-family board — on its own: two physically different nRF54L15 DUTs have alternated on the one probe `000852006107`, and **three such swaps are on record, each tripping the gate** — three identity refusals naming the recorded ID and the live one, saying *"re-enroll if this is deliberate"*, the most recent answered a minute later by the re-enrolment it asked for [measured 2026-09-06, `GET /alerts`]. **The count is measured; the proportion is not** — a swap re-enrolled before any validate ran leaves no row. Of the log's six entries the other three are a *different* refusal, probe-not-attached, carrying no live ID.

Each row is an end-to-end refusal, not a log line beside one — decision 12.

**No agent can induce one.** Every route pointing a role at other silicon runs through `enroll`, which overwrites the record it would have to contradict; there is **no topology override on the store path**, its only variable being Windows' `ProgramData`, unsettable for an already-running service.

The register pair those reads go through is confirmed against real silicon by an independent mechanism — decision 21. Everything else still open: [open.md](open.md).
