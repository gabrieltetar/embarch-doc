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

### 16 — An early powered check, instead of the raw access-port error chain

**Found live:** the real DUT enrolled that session turned out to be **genuinely unpowered**, and every attach attempt failed with a generic error **a human has to already know how to read.** The probe's own sensed target-voltage pin is read immediately before attach at both of this crate's attach sites, and a reading under a threshold **fails fast naming the actual likely cause.** Not every probe type supports the reading, and an ambiguous or plausible one just proceeds — **best-effort diagnosis, not a new hard gate.**
