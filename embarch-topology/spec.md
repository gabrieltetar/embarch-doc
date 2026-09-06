# embarch-topology: spec

**Status:** active, 2026-09-02. Repo: [gabrieltetar/embarch-topology](https://github.com/gabrieltetar/embarch-topology).

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md).

## What it is

The suite's one abstraction for **topology**, meaning two things that were previously handled ad hoc across env vars, config files and doctor checks in three different repos:

- **Software topology** — where each process runs relative to the others: the API and Core on one machine, a WSL2-hosted API talking to a native-Windows Core, or Core moved to a headless box on the LAN.
- **Hardware topology** — what is physically wired to what: which USB port carries a board's debug probe versus its serial link, which physical board plays which role, and what that role's board identity currently is.

**The incident that motivated it:** dev-bench's runtime serial link moved to a dedicated UART port, the migration was implemented and validated once, **and the Windows Core service still had a stale port override in its own registry environment.** Nobody cleared it. A study failed with a 404 naming the excluded candidate, and **diagnosing it took manually enumerating serial ports, reading service source, and reasoning by hand about which of two recognized-vendor ports was correct.** This crate makes that class of problem diagnosable from one place — and, per decisions 2 and 3, **structurally impossible, since the stale-override mechanism that caused it was removed rather than merely detected.**

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
| **A link port's USB *interface*** | One probe can expose two VCOMs under one serial; **which one the console is wired to is a devicetree fact, not a USB one** [confirmed live 2026-09-06 — see below] |
| **A DUT signal's route** | A wire between two headers is invisible to software |

Storage is one file under a machine-wide directory this crate owns. A store predating any of the later facts still loads.

## Storage and roles

**A role is unique.** Enrolling displaces any other board holding that role, and the displaced row is **returned rather than dropped silently**, so the caller can say out loud that one board replaced another. Two rows claiming one role would have left the by-role lookup answering with whichever came first in the file — **on this bench, the unplugged board, carrying a dead link serial that narrows resolution to a port that cannot exist.**

**A detected port says whether it was guessed.** When several candidates were resolved by the lowest-interface rule, the result carries how many it was guessed among, **so a caller reports "COM16, guessed among 2" rather than "COM16"** — the guess is kept, because every bench with one VCOM needs to declare nothing, **but it is a guess that says so.**

**The declared *interface* was exercised live on 2026-09-06, with two probes attached, and it was load-bearing.** The host had **three** SEGGER CDC UART ports visible [measured 2026-09-06, `Win32_PnPEntity` on the Core host]: `COM16` (`VID_1366&PID_1069&MI_00`) and `COM17` (`…&MI_02`) on **one** device instance, therefore one probe serial, plus `COM5` on the other J-Link. Resolution returned `COM17`, `interface` 2, **and no `guessed_among`**. `COM5` was eliminated by serial — but **by the decision 17 *fallback*, not by a declared one: this bench declares no `link_port_serial`**, so that narrowing ran on `probe_serial` with `serial_is_fallback` set. **The declared-serial path therefore still has no hardware evidence**, which is worth stating precisely because decision 17 exists to separate the two.

**Only the declared interface separates `COM16` from `COM17`**, which differ in nothing else a detector can read. Traced against `select`: with the interface removed, `one_probe && interfaces_known` both still hold, so resolution does not bail — it warns, sorts by interface, takes `candidates[0]` = `COM16`, **and sets `guessed_among = Some(2)`**. That is the wrong port, reported as a guess, and it fails the way this crate exists to prevent: a bench that flashes, boots, runs and times out.

**The corollary is the opposite of what a crowded bench suggests: adding probes cannot produce a guess while an interface is declared.** `guessed_among`'s trigger is an *under-declared* bench, not a busy one — so exercising the field takes a deliberate omission, not another board. Nothing here has yet observed it set.

## What validation asserts, and what it cannot

- **A role:** the enrolled probe is currently enumerated and its live identity still matches the recorded one. Runs on every flash, reset and handshake.
- **A same-chip link:** the board answering on the runtime link is the same silicon the JTAG probe verified, by comparing the JTAG-read identity against the board's self-report. **Two chip families have a declared relation; every other chip returns *undeclared*, which is never treated as a pass — a comparison that could not be made is not a comparison that succeeded.**
- **A direct signal route:** the declared serial is currently enumerable. It **cannot** confirm the wire from the DUT's TX pin actually lands on that bridge.
- **A via-bench route:** validates on the strength of being declared. Its carrier is the bench's link, whose liveness is the role check's job; **re-checking it through a second, weaker path would assert more than is known.**

**A signal mismatch is deliberately not written to the durable alert log** — an alert's shape is board-specific and a wire has none of those fields.

## What the consumers gave up to use it

- **`embarch-core`** deleted its own copies of the identity-recheck logic, its board storage, its identity reads, and the dev-bench port heuristic. It keeps the hardware-I/O plumbing — actually opening a probe or port handle — and calls the crate for *which* port or probe, and whether it is still valid. **The behaviour change beyond the move: every dev-bench port override env var is gone, with no replacement.**
- **`embarch-api`** deleted its own software-class detection for `base_url = "auto"`, and links the crate **without the hardware feature — confirmed by `cargo tree` that the probe and serial crates never appear.** Its declared-address fast path is unchanged; only the auto branch calls the crate.
- **`embarch-umbrella`** deleted the same detection; its env module **shrank to just "am I under WSL2"**, still needed standalone by its own Windows-binary lookup.

## Where it stands

Both real boards are enrolled against the redeployed Core, and a real end-to-end flash plus study has completed clean. Two things stayed deliberately open rather than blocking: **a deliberate-mismatch alert check** — there is no legitimate way to inject a stale identity record on today's bench without either a second same-chip-family board or writing the live enrollment file directly — and the items in [open.md](open.md).
