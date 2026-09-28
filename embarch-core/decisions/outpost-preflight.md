# embarch-core decisions: The outpost mode pre-flight

**Status:** active, 2026-09-28. Split out of [handshake.md](handshake.md) on 2026-09-28 when that file reached its cap — a split by mission, entries moved verbatim, per [../../DOC-BUDGET.md](../../DOC-BUDGET.md) §3.

Whether the DUT is running firmware built for the outpost trace mode a study declares, checked before step 1 by reading a serial port and the firmware's own header frame — a different mechanism from `HelloAck`'s handshake and the JTAG probe's hardware identity, which is why this split off on its own rather than staying folded into their mission. The version gate and the bench's hardware identity are still [handshake.md](handshake.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## The outpost mode pre-flight

### 74 — The DUT's outpost mode is read off the wire before step 1, needing no reset and no reordering

`embarch-study-designer` decision 77 lets a study declare which trace mode the DUT must be in. This is the check, and it runs **before the version gate**, hence before `StudyStart` — decision 31's own ordering property: a refusal leaves a bench that never started a step.

**Two checks at two places.** `validate_study` runs the crate's rules on `requires.build` and refuses a mode declared with no outpost trace tap — the flags byte arrives in that capture's header, so it would have no subject. Both are pure, so they fail at submit. The live half opens the trace signal's port, reads a header, and compares.

***The plan this replaces was: reset the DUT, wait for its power-on header, and move the outpost tap's open ahead of `StudyStart` to catch it.*** That reordering is real — `gate_then_start` sends `StudyStart` well before `sync_signal_taps` opens anything, so by the time a tap is open dev-bench has already started step 0 — and it was named as the thing most likely to be got wrong.

**It was not needed: the header is not only a power-on event.** `embarch-outpost` emits it at startup and then every `CONFIG_EMBARCH_OUTPOST_HEADER_INTERVAL_MS`, 1000 by default, precisely so a host attaching mid-stream can decode. So the pre-flight *listens* — 3 s, three times that interval — on a port it opens and closes itself, and the run's opening sequence is untouched.

**`0` is a legal build** that emits the header once at startup and never again — unverifiable exactly when it matters, since a run that just reflashed sent its power-on header before Core's port was open. So an empty listen is followed by **one** reset, port already open, and a 6 s wait: one reboot, only where it is the only way to get an answer, with `after_reset` in the log and in every refusal so a run is never silently a reboot.

**A failed input-buffer clear is fatal here, where the capture treats it as a warning.** There a stale prefix is a bad first row; here a header buffered from before the reflash would answer the check about firmware no longer on the board. **The hardware lock is held across the listen, not only the reset**, or a `POST /flash` could land a different image between the header this reads and the study that starts on it. The reset goes through `hardware::reset` directly rather than `POST /reset`, which would take the lock this holds, and the board it resets is the trace signal's declared `origin_role`, not a hardcoded `"dut"`.

**Only the flags byte is compared.** The header's `build_id` is `<app describe>+op<module describe>+m<hash>` from `git describe --always --dirty --tags`, while `requires.firmware_version` is `embarch-core-client`'s `--abbrev=8` form: the two do not match for the same commit and no comparison rule between them has been stated. Guessing one is the class of thing this suite refuses, so the build id is reported in the log and named in every refusal, and version verification stays with `Provenance`.

A refusal is a `412` naming both bytes — what is missing, what is present and must not be — plus the build id, the outpost version, the signal and the port: an engineer reading it is deciding whether to change the study or rebuild the firmware.

**Measured on a real nff_dev@7, 2026-09-19.** Three reads returned the header in **171-258 ms, every one with `after_reset=false`** — so on ordinary firmware the listen costs a fifth of a second and the DUT is never rebooted, and the 3 s budget is ~12x the observed worst case. The flags read off the wire (`0x1b`) matched the generated `.config` exactly, and a deliberately unsatisfiable declaration was refused before step 1 while a satisfiable one ran to completion.
