# embarch-topology decisions: Enrollment and what a bench declares

**Status:** active, 2026-09-07.

What enrolment *records*: the one thing in the suite that structurally requires a human, and the facts detection cannot produce. What live validation then *asserts* is [validation.md](validation.md). What is declared about a board's *link* specifically, once role uniqueness is in play, is [link-declares.md](link-declares.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 14 — Hardware enrollment is the one interactive surface; software topology stays read-only

**The line is not arbitrary: hardware enrollment is the one place in this entire suite that structurally requires a human** — no software can derive which physical board a probe is wired to, only a person physically isolating it and saying so. **Everything else this crate resolves is already fully automatic, so there is nothing for a human to *submit* about any of it, only something to *watch*.** No software-topology equivalent exists and none is planned unless a genuinely undeterminable fact shows up.

Prompted by trying to actually use the UI against real hardware for the first time — plugging in both boards post-deploy and **discovering enrollment had not moved to this crate's own storage and needed redoing.**

**Reversed the same day on *where* that interaction lives.** It originally put the form in this crate's own standalone UI, calling the exact same enroll function the CLI and Core's endpoint already call. **Correct code, wrong place**, pointed out directly: real hardware I/O and the system-file write it produces should be done by Core, **which already does exactly that under its own hardware lock.** A second process calling the identical function **does not share that lock**, and makes a human start and stop a whole separate binary to reach something Core — already running, always, as an installed service — can serve directly. This crate's UI reverted to fully read-only.

**Net effect: enrollment now has exactly one route to it, not two independently-invokable ones that happened to agree today and could silently drift apart tomorrow** — decision 8's principle, honoured for enrolling as well as validating.

### 15 — Enroll takes an optional probe serial, so enrolling two visibly-different boards no longer requires isolating them one at a time

Prompted directly: a human enrolling both real boards, already both plugged in, **should not have to unplug either just because an "exactly one probe attached" check could not otherwise tell them apart.** When the probes are already distinguishable, **that requirement is stricter than the actual ambiguity problem it exists to solve.** Given a serial it selects that probe — **matching Core's own flash and reset disambiguation, extending an existing suite pattern rather than inventing one**; omitted, the original requirement is unchanged, so every existing caller keeps working.

**What this does not, and cannot, close:** two boards sharing an identical probe type still cannot be told apart by serial alone, **which is all a human or this parameter has to go on without physically isolating them.** The live hardware-ID readback still catches a wrong *chip name* for whichever probe got picked; **it cannot catch "right chip, wrong physical board" when both really are that chip.** No UI can enroll around that.

### 28 — The CLI's own enroll/validate/set-dev-bench-link refuse when a Core is reachable; only local-bootstrap still runs them in-process

**Decision 14 read as fully applied to this crate's UI and was not applied to this crate's CLI at all.** The UI reverted to read-only; `bin/main.rs`'s `Enroll`, `Validate` and `SetDevBenchLink` subcommands kept calling `hardware::enroll`/`validate_role`/`set_dev_bench_link_port_*` directly — the exact second, unlocked, un-synchronized route to the same store decision 14 closed for the UI. Found by suite review (2026-09-06, dimension 4), which read the two `#[cfg]` arms in `hardware/paths.rs`: on the suite's one validated `wsl-host` machine the CLI, run from WSL, writes `/var/lib/embarch/topology/enrollment.toml`, while the Windows-service Core it should agree with reads `%ProgramData%\embarch\topology\enrollment.toml` — not a race with a bad outcome, a write nothing downstream ever reads.

**The fix is a refusal, not a client.** Each of the three mutating subcommands now resolves the software topology (the same call `embarch-topology status` makes, live, every invocation) before touching hardware or the store. A reachable Core wins that resolution and the subcommand refuses, naming the resolved base URL, the Core route that owns the mutation (`POST /probes/enroll`, `POST /validate`, `POST /dev-bench/link` — `embarch-core/interfaces/topology.md`), and the two decisions that say why (this one; `embarch-core/decisions/surfaces.md:30`). **This crate does not gain an HTTP client to actually place that call** — `software`'s existing `reqwest` dependency, already linked for `resolve_software_topology`, is reused for the probe only; the mutation itself is left for the human to place against Core directly, exactly as decision 14 already asks of anyone using the retired UI's replacement.

**Local-bootstrap is the one case that still runs the mutation in this process**, and is why this is a property (a refusal that yields) rather than a hard error: no candidate answering is exactly what `status` reports as `core: not found`, and a machine with no Core installed yet has no other way to produce its first `enrollment.toml`. `set-dev-bench-link`'s `--clear-serial`/`--clear-interface` (decision 20) have no documented Core-side equivalent — `embarch-core/interfaces/topology.md`'s `/dev-bench/link` entry never mentions clearing — so today they refuse the same way as `--serial`/`--interface` on a reachable Core, without being able to point at a clearing curl command; closing that gap on Core's side is Core's decision to make, not this crate's.

### 16 — An early powered check, instead of the raw access-port error chain

**Found live:** the real DUT enrolled that session turned out to be **genuinely unpowered**, and every attach attempt failed with a generic error **a human has to already know how to read.** The probe's own sensed target-voltage pin is read immediately before attach at both of this crate's attach sites, and a reading under a threshold **fails fast naming the actual likely cause.** Not every probe type supports the reading, and an ambiguous or plausible one just proceeds — **best-effort diagnosis, not a new hard gate.**
