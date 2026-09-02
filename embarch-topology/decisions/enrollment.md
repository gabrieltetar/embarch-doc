# embarch-topology decisions: Enrollment and board identity

**Status:** active, 2026-09-02.

The one thing in the suite that structurally requires a human, and what the bench taught it.

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

### 20 — A role is unique, and the link's USB *interface* is a third declared fact

Two independent gaps, one event: **the day the dev bench went back to being an nRF54L15DK.** Decision 10 anticipated *half* of the first, and **that half turned out to be harmless** — the hardware ID tells two same-family boards apart cleanly. **What it did not anticipate is that both would be the same probe vendor with the same kind of serial-over-USB VCOM**, which is where the real trouble was.

**Role uniqueness.** Upsert de-duplicated on probe serial only, so **moving a role onto different silicon left two rows both claiming the same role.** Nothing errored, and the file looked correct. **The damage is entirely downstream:** the by-role lookup returns the first match by file order, so validation, port resolution and the validate endpoint **would all have kept answering with the *unplugged* board**, leaving the newly enrolled one unreachable by the only name anything addresses it by. Concretely, it would have **inherited the old row's declared link serial — a bridge no longer attached to anything — which narrows *hard* and so resolves detection to a port that cannot exist.** A role now displaces any other board holding it, and upsert **returns** the displaced row rather than dropping it silently, so enrolling can say out loud that one board just replaced another.

**The link interface.** Decision 17 established that a link's own USB serial can be a fact no detection produces. **This is the case where a serial cannot help at all:** the DK's console goes through its own onboard probe, so the probe serial and the link serial are **the same string, and both narrow to a *pair*, because that one probe exposes two VCOMs under one serial.** Selection resolved such a pair by taking the lowest interface index — **a rule with no hardware evidence behind it, because no bench before this DK had ever had two VCOMs — and this board falsifies it:** the console UART's pins are wired to the *higher* one. **The lower interface accepts bytes and never answers.**

**What made it expensive was that the guess was invisible.** Selection logged a warning into Core's log and returned a result **indistinguishable from a determined answer**, reported with full confidence. **The observable symptom was a bench that flashed, booted, ran, and timed out waiting for a handshake — which says nothing about a port having been chosen at all.** Two hypotheses were checked and discarded before the port was suspected: that the identity gate's attach left the core halted (**refuted by reading the debug status register: halt clear, sleep set, i.e. running**) and that the overlay had not applied (**refuted in the generated devicetree**). What settled it was **writing a real handshake frame to each candidate by hand** — one returned nothing, the other returned an ack plus the bench's own log lines.

So a detected port now carries **how many candidates it was guessed among**, set only when the lowest-interface rule actually chose, **so a caller reports "COM16, guessed among 2" instead of "COM16".** The guess itself is **kept, not replaced by an error** — every bench before this DK had one VCOM and needs to declare nothing — **but it is now a guess that says so.** The declaration is exposed three ways, with serial and interface **independently optional on all of them, since they answer different questions.**

*Rejected: resolving it by handshake* — try each candidate and keep whichever answers. **Genuinely more automatic, and declined for the layering reason this module's own header states: nothing here opens a port.** It reads USB descriptors the OS already enumerated; opening the link and speaking the protocol is the consumer's job. **Moving protocol knowledge in here to save one declared fact would make the topology crate depend on the dev-bench wire schema, and the schema moves far more often than a bench's cabling does.**

### 21 — The self-reported-ID comparison gains a Nordic arm; the gate had never once run against Nordic silicon

Core's gate confirms the board answering on the runtime link is the same silicon its JTAG probe just verified. It shipped with **exactly one declared relation and a deliberate rule that every other chip returns undeclared** — *"not a pass: a comparison that could not be made is not a comparison that succeeded."* **That rule was right and it held. What it also meant is that the moment the bench stopped being that one chip, the gate stopped concluding anything**: it reported undeclared while showing two obviously-related IDs — **the same sixteen hex digits with their halves swapped.**

**The arm is derived, not fitted to that observation** — the standard the module sets is *both implementations' actual register reads, in view at once.* Zephyr's Nordic driver reads the pair in index order **and then emits it reversed on purpose**; the byte-emission and hex-encoding orders match on both sides, so **each half encodes identically and only their order differs. The observed pair is a confirmation of the derivation, not its source.**

One conditional branch in that driver covers both of Nordic's device-ID register layouts, **which is why a single relation serves the classic parts and the nRF54L series alike.** **The limit is written into the code rather than left implicit:** that file has fallbacks to other registers for parts where the device ID is inaccessible, **and those produce something this projection does not describe** — such a chip would come back *mismatch* rather than *undeclared*, **the one way this arm can be wrong**, and the same exposure the first arm already carries, accepted on the same terms.

**Why this matters more here than it did on the first chip**, and why it is a decision rather than a bug fix: decision 10 flagged the risk of a dev-bench sharing a chip family with the DUT, **and that is now the bench** — two boards of the same chip, two probes of the same vendor, two VCOMs each. **The gate that distinguishes them is the only thing standing between "the probe verified board A" and "board B answered on the link", and until this arm existed it was returning undeclared for both of them.**
