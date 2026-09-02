# embarch-core: decisions

**Status:** active, 2026-09-02.

Why it is the way it is. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). Numbers are permanent identifiers, never renumbered or reused ([DOC-PROTOCOL.md](../DOC-PROTOCOL.md) §7.2–7.4); groups are topical, so numbers run out of order.

---

## Platform and process

### 1, 2, 7, 17 — Rust, probe-rs as a library, Axum, `spawn_blocking`, and CI everywhere
probe-rs is called as a library, not shelled out to: no subprocess or output-scraping, and typed errors. Axum for one toolchain across the stack and because its `State`/middleware model fits `AppState`. Both probe-rs and `serialport` are synchronous, so every hardware call goes through `spawn_blocking` — a slow flash must never stall the runtime. CI runs `build`/`clippy -D warnings`/`test` per push on every repo that lacked it, plus a `native_sim` build for dev-bench, which would have caught a real Zephyr API breakage before it was found by hand.

### 3 — `service-manager` for install; self-elevation here rather than in every caller
One code path registers `run` as a systemd unit, launchd job, or Windows Service. **Registration is not the whole job:** systemd and launchd accept "the process stayed alive", but Windows kills a start that has not called `StartServiceCtrlDispatcherW` and reported `SERVICE_RUNNING` within 30 s, however healthy the process — so `run` attempts the real SCM handshake first on Windows and falls back to foreground only when SCM did not launch it. All four subcommands **self-elevate**, because a human running `embarch-core install` and `embarch-umbrella` shelling out to it hit the same wall; fixing it here fixes both callers. Re-launching the *same already-running binary* adds no new trust step. Hence also `update <new-exe>`: stop, rename aside (Windows will not overwrite a running image), copy, start, roll back on failure.

*Rejected:* printing the command for a human to re-run elevated — a transcription-error opportunity, and it left updating an installed Core with no supported path at all.

---

## Auth, binding, configuration

### 5, 6 — Bearer-token auth, and a `127.0.0.1` default widened explicitly by `embarch-umbrella setup`
Core may be reachable over a real network, so an unauthenticated surface is unacceptable even at single-engineer scale; a plain exact-string compare, deliberately not OAuth or anything session-based. The bind default was originally `0.0.0.0`, since reachability is the point. Reversed: `0.0.0.0` plus no TLS plus a static token plus `/flash` reading an arbitrary local path, in a process that may run as `LocalSystem`, is a posture nobody had assessed **as a whole** — each piece was documented, never composed. Two gaps surfaced on implementation: the default had never changed in code, and `service::windows::run_service` **hardcoded `"0.0.0.0"`**, discarding whatever `--bind` a service was registered with, so every Windows deployment had been wide open regardless of any flag.

### 11 — An optional `core.toml`, narrowed to `bind`/`port`, still design-only
Every knob is env-var-only, and passing environment to an installed service is the bug class decision 3 already paid for. **Never written.** Narrowed when `embarch-topology` abandoned the four `dev_bench_*` knobs outright: a config value left stale wins over reality exactly as capably as an env var left stale, and enrollment is the fix either way.

---

## Locking

### 4, 14, 15 — One `hw_lock`, `503` on contention, `study_lock` for the bench
`hw_lock` is held for the whole handler body, so a `/flash` blocks a concurrent `/reset` from *starting* rather than serialising at the probe-rs call level. Contention returns `503` naming the holder: two `embarch-api` processes against one Core is normal, and the second caller used to block silently on the mutex, indistinguishable from Core being unresponsive. The dev-bench link is a different physical connection and is arbitrated by `study_lock`; port enumeration opens nothing and takes neither. No new lock was needed — the existing ones already covered it.

---

## Probe selection and board identity

### 9 — `open_probe(probe_serial)`, and ambiguity is a named error
Dev-bench *is* a second debug probe, so "more than one attached" is the normal state. More than one with no selector returns an error listing every candidate rather than picking — a wrong-target flash is worse than a loud failure. A `500` not a `400`, since the ambiguity is only discoverable once enumeration runs. This decision described itself as implemented for months while the code still had only single-probe selection; found the first time two probes were genuinely attached, when flashing picked the wrong one.

### 22 — A probe/board identity gate, because a label can go stale with nothing to notice
`probe_serial` says *which probe*; it says nothing about whether that probe is still wired to the board its config **labels** it as. That label is, and can only be, a human's one-time act of physically isolating a board and noting its serial — nothing in a USB descriptor says "I'm wired to the DUT". It goes stale silently when a probe is moved during rework, and `attach(chip)` structurally cannot catch a same-family mismatch the way it catches the wrong architecture.

So a machine-local table keyed by probe serial, holding the chip's own factory-burned ID **read live over the debug port** — independent of which probe or cable answers, so it survives a probe being moved in a way a serial cannot. Enrollment refuses anything but exactly one attached probe: that refusal *is* the enforcement behind "plug in only the board you mean, then confirm". `flash`/`reset`/the handshake compare live against recorded and **fail closed**, naming both values. A role-keyed variant exists because a plain UART bridge has no JTAG capability, so it can never be an enrollment candidate.

*Rejected: an interactive popup at flash time* — Core is a service, so Session-0 isolation needs a second always-running helper plus IPC, and it degrades wrongly for a headless Pi. **Moved wholesale into `embarch-topology`**, because the stale-serial incident that motivated that crate *is* this mechanism's own override path going stale.

### 23 — The four dev-bench env overrides are gone, with no replacement knob
They were the mechanism behind the incident that motivated `embarch-topology`. Removed, not deprecated: decision 22's enrollment fallback was always the stronger signal — a live hardware-ID readback rather than an operator-typed string.

### 26 — Diagnose an unpowered target before attaching
An unpowered board failed every attach with a low-level ARM access-port chain a human has to already know how to read. Core reads the probe's own sensed target voltage before `attach` and fails fast naming the likely cause. Best-effort, not a gate — not every probe supports the reading.

---

## Chip mapping

### 8, 34 — The SoC→chip table lives here, plus `chip-list` as its human fallback
`embarch-api` is about to call `/flash` anyway, so resolving here costs nothing extra and keeps one copy in the one process that links probe-rs and can therefore validate a mapping against the real target database rather than trusting a hardcoded string. Matched case-insensitively and **exactly**: a plausible-but-wrong fuzzy match would silently pick the wrong physical target. A test checks every entry against the real registry, so drift fails a test run rather than a live call. `chip-list [filter]` exposes that same in-process database, because configuring an override for an unmapped SoC otherwise meant `cargo install probe-rs-tools` — a toolchain install in the middle of a download-a-binary onboarding. *Not a UI dropdown instead*: that needs an endpoint too, so it is strictly more work and can be layered on this.

---

## Flashing

### 10, 18 — Multipart upload, and `Format::Bin` at the merge address
`firmware_path` only works when caller and Core share a filesystem. Multipart is needed not just for a remote Core but for WSL2→Windows: the installed service runs as `LocalSystem` in Session 0 and **cannot reach `\\wsl.localhost` at all**, which is why the earlier UNC mechanism is retired — its "confirmed working" claim held only for a foreground Core. Separately, **`Format::Idf` does not work for a Zephyr image**, confirmed by inspection before attempting a flash: its loader requires an ESP-IDF app-descriptor section Zephyr does not emit, while Zephyr's runner merges bootloader+partition-table+app at build time and writes one `.bin` at a fixed offset. Hence `base_address`, meaningful only for `bin` and silently ignored otherwise so a caller passing it unconditionally need not special-case.

### 21 — Plain `attach`, not `attach_under_reset`; a best-effort reset pulse instead
A real hardware scare traced to two documented quirks rather than corruption: a target in low-power sleep can stop answering a plain SWD attach, and the ESP32-C5's USB-Serial/JTAG peripheral resets only the *core* without re-sampling boot-strap pins, so it can stay latched in ROM download mode — which also explains the earlier handshake decode failures, since a chip in its bootloader was never running the protocol.

**`attach_under_reset` made it worse and was reverted**: it needs the reset pin wired to the debug connector, which this board does not do. `reset` calls `target_reset()` first instead — a silent no-op on this probe, whose driver hardcodes `Err(NotImplemented)` regardless of wiring while its lower-level assert/deassert genuinely drive the line, so the fallback pulses manually. **The real pulse then reproduced the original symptom deterministically**, wedging the same device's CDC interface while JTAG stayed enumerated. **Resolved by moving the link to the board's second, dedicated UART port** rather than replicating the vendor's own watchdog-register hack.

### 32 — `erase` must not be EmbArch's own guess: it bricked a real board
The first implementation set probe-rs's `do_chip_erase`. [Measured] two runs each way, same artifact and probe: without `erase` the DUT comes up and advertises, with it the board goes silent. A plain non-erase flash does *not* recover it; the vendor's own runner with `--erase`, on the same image, does. **The mechanism is not established and this decision does not invent one** — probe-rs models the part as one flat NVM region with a sequence implementing only `debug_device_unlock`. Four-for-four correlation and a known recovery path; the causal story stays a guess.

*Rejected, and it was the option already written and compiling:* sector-erasing the declared NVM regions — **another EmbArch-authored guess about what a Nordic part needs erased, the same class of guess that produced the brick.** *Not adopted: a post-flash liveness check.* Recorded because the cost was paid in full: a whole session went into BLE scan diagnostics to explain a DUT that Core's own flash had bricked, and nothing ever verified a board was running after a flash. Core reports what the flasher reports; liveness is a study's job.

### 36 — A flashing backend per chip family, refusing probe-rs where the vendor's semantics are not implemented
The defect in one sentence: **a Zephyr board declares how it is programmed, and Core overrode that declaration with one hardcoded backend.** The board file names three runners with the right device string already filled in; Core used none of them.

**Why this widens decision 32 rather than implementing it:** the nRF54L15 stores code in **RRAM**, which probe-rs models as one flat region with no erase/write granularity *for any operation* — and across a whole milestone **no image Core flashed to this DUT was ever demonstrably running**. Enough to stop writing bytes through a path that models the storage wrongly, without claiming proof.

**A refusal, not a preference:** family-prefix matching *refuses* an unheard-of nRF54L part rather than permitting it, because a wrong refusal costs an error message and a wrong permit costs a board. Selection order follows the board file's own include order, so Core reaches for the tool `west flash` would have used. **Tools are detected, never bundled — a licensing fact:** SEGGER's software is proprietary, one Nordic tool links it and inherits that, and the other downloads its command packages at runtime. **The tool must be on the machine running Core, not the one running the build.** Kept from the probe-rs path: the identity gate and the target-power pre-flight, with the probe **dropped before spawning**, since the vendor tool claims the same USB interface and two owners is a hang rather than an error.

**Two findings from the first real vendor flashes, both failing in the worst order:** a Windows Core launched from WSL2 inherits WSL's `PATH`, so discovery picked a **Linux ELF**; and a vendor tool infers format from a file extension, which an uploaded artifact lacks, so J-Link reports an unsupported format **after having already erased the chip**. Both found by erasing a real board and failing to reprogram it — **erase then fail leaves nothing running.**

---

## Errors and version handshakes

### 12, 13 — A structured error body and a contract version — designed, not built
Plain-text errors suit a human reading a CLI error, but `doctor --json` and a UI need to branch on error *kind*; a `{code, message, cause}` body would also retire the "finer CLI exit codes" idea, since a script branching on failure kind wants a field, not an exit code. Separately, the only cross-boundary version check is the study schema, so nothing can notice a materially different HTTP contract until a call breaks — `contract_version` would be hand-bumped only for a wire-visible change, and `embarch-api` would **warn, not refuse**, matching the suite's posture on skew. The endpoint table described all three fields as shipped for months when none were.

---

## Logging

### 16, 29 — One daily-rolling log file, one implementation, three front ends
`tracing` output used to go wherever stderr landed — a real file only for a foreground `run` a human is watching, which is why the SCM start failure was diagnosed from the Windows Event Log by luck rather than design. **Setting up the writer is allowed to fail** without taking the CLI down: an unprivileged human on a machine where the log directory is not writable must not lose a CLI that worked before. `init_tracing()` runs before subcommand dispatch, so the foreground and SCM paths are covered by construction.

The HTTP pair mediates the *same* file for `embarch-ui`'s Debug tab, which had proposed a second size-capped logfile without knowing this one existed. Deliberately **not** a custom `tracing` layer broadcasting each line, which would mean modifying `init_tracing` in a live service; served as plain text, because reformatting a deployed service's output into JSON for one client is a bigger change than this needs. This decision read as shipped for days while the CLI subcommand did not exist — the third instance of that drift in one session, after decisions 9 and 11.

### 37 — A separate `dev-bench.log`, and a handshake that tolerates a log line before `HelloAck`
Once the bench turned `CONFIG_LOG` on, a log line stopped being a rare diagnostic and started carrying Zephyr's subsystem output and the fatal-error dump. **Why a third destination:** `core.log` is Core's account of what the *service* did, and interleaving a firmware's full output drowns what a reader opened it for; the study's reserved tap is scoped to one study by construction, so it cannot hold a line from a handshake that failed before the study started. A second *file*, not a second log *mechanism*.

**Two Core-side changes only running it surfaced, both of which would have made the firmware's half useless.** The handshake did one `recv` and failed anything that was not `HelloAck`, so turning firmware logging on would have broken every study and read as a protocol bug. And the boot record was reliably produced and reliably lost: the bench holds its boot log until the first `Hello` and flushes it after the ack — that flush *is* how a reboot becomes visible — but the handshake endpoint returned the instant it had the ack. **Core also writes the level each study asked for**, because otherwise a quiet file means either "the bench had nothing to say" or "this study asked for `Warn`", which are opposite conclusions about a study that just failed.

---

## Studies: execution and failure

### 19, 20 — A handshake with no study, and crash-mid-study confirmed rather than assumed
The handshake already ran on every submit and discarded the ack after logging it, so nothing could ask "what firmware is on this bench" without starting a real study; `/dev-bench/hello` guards an in-flight study with a `409` rather than racing to open the same port twice. Separately, killing the service outright mid-registry and restarting it confirmed the documented behaviour: a previously-real `study_id` `404`s, indistinguishable from one that never existed, by design, and a fresh study immediately after completed cleanly. No code changes — the behaviour was right and had never been run against a real crash.

### 24 — Core never materialises a `StudyResult` host-side
[Measured] `StudyResult` is **~1.3 MB** purely from `no_std` worst-case capacities, reserved unconditionally regardless of what a study populates. The old path accumulated every step result, converted once at the end, kept it resident forever, and cloned it by value on every `GET`. Two of those reproduced a real stack overflow on both Linux and Windows in `cargo test`; deserialising into the same type overflowed too, confirming it is the **type** that is unsafe to hold, not one code path. Fixed by writing one step result **by reference** the instant it arrives, finalising only at a real `StudyDone` and leaving `.partial` behind on an abort as a diagnostic artifact.

**The SSE route is the live-push companion**, one broadcast channel filtered to the URL's id — one suffices because `study_lock` never allows two studies. A slow subscriber gets an explicit `lagged` frame rather than silently missing messages. A deliberate reversal of the original polling-only framing: nothing about a result is held back until the study finishes, at any layer.

### 33 — The watchdog deadline includes `delay_before_ms` — a live defect, not a refinement
The deadline ignored the field while dev-bench honours it by sleeping *before* the step runs, so any step whose delay exceeded its own timeout plus grace failed a study whose bench was working perfectly — squarely on the intended path, since multi-second delays are the point of that field. Found by a design pass reading the function for another reason, never by a test, because every fixture used a zero delay.

*Declined:* moving the sleep host-side, which folds link jitter into authored timing; and rejecting such a step at submit, which forbids a legitimate long soak and leaks an internal constant into the authoring contract. `timeout_ms` means "how long this step may take", never "how long until I hear back".

### 40 — An undecodable frame costs the frame, not the link; and `completed: false` is no longer success
`recv` returned `Result<Option<_>>`, so a frame that arrived and failed to decode was indistinguishable from a read error and broke out of the run. The consequence was specific: **the step result carrying a failed step's reason is the longest message dev-bench sends, it is the one that gets truncated, and refusing it tore down the link and reported a connection error with no mention that a step had failed.**

**The resilience fix is what found the cause of the fault it was written to tolerate.** Reading past the bad frame showed thirteen seconds of silence, and the next handshake's uptime placed a bench **reset** within 150 ms of the truncation. It had been crashing mid-transmission all along, and every host-side reading of those bytes — including two well-evidenced wrong ones — had been describing the wreckage.

**`StudyDone { completed: false }` was reported as `"completed"`**, so a run that died at step 5 of 11 came back clean. A study that stops early now fails and names the step **in that step's own words**, because dev-bench sends the diagnosis exactly once. Two smaller findings: the shortfall arithmetic was out by one and **the wrong number had become the name of a bug** — corrected, the occurrences read 13/15/17/17/13/17, which is what a crash with variable timing produces and what a buffer boundary does not; and bytes that never formed a frame were invisible, which was exactly the evidence that mattered, since the bench's console *is* this UART and a timeout reported "no message received" while holding 699 bytes of boot banner.

---

## Streams, manifests, rendering

### 30 — Core captures stream taps for a study's duration, including a port it opens itself
The consuming half of `embarch-study-designer` decision 39 and of `embarch-outpost`.

**A second serial port belongs to a wire, not a device.** A direct-route signal tap is a bridge with the DUT's TX pin on it and nothing else, so it takes **neither lock** — blocking a `/flash` on a read-only listener would invent contention that does not exist — while its lifetime stays bounded by the study.

**`streams/` replaces the three fixed CSVs as paths**, written incrementally with **raw bytes always before any decode**, which is what makes a run with a bad layout recoverable. `streams/index.json` exists because the aliases cannot otherwise resolve from disk: the old handlers read fixed filenames, while an alias must answer *which tap is the power tap* from a handler with no `Study` in hand, since Core keeps no resident copy.

**A manifest is bound by the study's own flash and verified by build ID** — **selection whose lifetime is that study**, never a persisted "current firmware" record. On mismatch Core writes the raw stream and **renders nothing**: rendering against the nearest available manifest produces a trace that is completely readable and completely wrong, relabelling every marker and thread. Loud beats plausible. It rides as a sibling of `firmware` on the call that already carries the artifact, parsed **before** the flash so a build problem is reported while the person who ran the build is watching, stored **after** it succeeds, and **keyed per chip** because `/flash` also writes the bench's firmware. Refusal costs the *names*, never the capture.

**Core is the trace's clock, and a join it cannot verify stamps nothing.** The frame index counts non-empty runs between delimiters on both sides, so a frame that later fails its CRC still consumes one — indexing by *successfully decoded* frames would silently shift every stamp after the first corrupt one. The raw file rotates and the arrival log does not, so each row carries its frame's length and the renderer checks the alignments agree: a trace shifted by three frames is readable, wrong, and indistinguishable from a correct one. Rendering is post-hoc from the complete file, which is what lets a late header name every record before it — a claim the code did not honour until the header was found in a pre-pass, leaving 488 of 9205 rows unnamed *and* untimed inside a stream whose index said `named: true`. What stays refused is *invention*.

Retention is two-segment rotation plus a count-based keep-last-N sweep, so it needs no clock, with the truncation marker firing on the **deletion** rather than the rotation. A stale prefix on a signal port is discarded on open — a TX-only DUT transmits whether or not anyone listens, and one study's first six records sat 195 s ahead of the seventh — though [the clear is not sufficient](open.md).

### 38 — Core renders a `Struct`-encoded tap and holds no more column knowledge than before
The store takes the study's declared decoders alongside its taps, because a struct tap's CSV *header* is the engineer's field list and cannot be derived from the encoding — the one place this differs from the encodings whose headers are compile-time constants of the shared crate. Core still knows no field name, width, or byte order. **The failed-decode row is Core's, and it is a row rather than a log line:** dropping it would leave a record that genuinely arrived indistinguishable from a notification that never came, and a warning in `core.log` is not visible to whoever opens the CSV.

### 39 — The third pre-flight seal, and the two indices a manifest cannot check about itself
`validate_study` recomputes `protocols_crc` too, and that seal exists for a reason the others make plain by contrast: `Study.decoders` is covered by **none** of them, because a layout only decides how Core *renders* a byte already captured, and re-rendering with a corrected layout must leave it the same study. A protocol is the opposite — dev-bench executes it — so corrupting one in flight would have firmware writing different bytes to a DUT's control point than the study said. Three sibling seals, checked independently, so a rejection names which third arrived wrong. **`validate_protocol` is called, not reimplemented.** The two indices it structurally cannot see are Core's, because they live on a `Step`: a `RunProtocol`'s protocol index and entry state, which nothing else in the suite resolves.

---

## The version gate

### 31 — Core enforces exactly what Core can verify, and records how every version was established
**What Core can verify, it verifies:** the bench's version against what it reports over the handshake, before `StudyStart` is sent, so no step ever runs. The gate and the send are **one function taking the send as a parameter**, deliberately — the property is an *ordering*, and an ordering is only worth asserting if a test can assert it. `StudyStart` is the only message that makes dev-bench execute anything, so "the closure was never called" and "no step ran" are the same statement.

**What Core cannot verify, it must not pretend to.** There is no readback path from a DUT, so the result records the *source* of each version rather than presenting an unchecked declaration as a fact.

**The override and the flashed version arrive as query parameters**, not `Study` fields: reflash is a run parameter, and it leaves the body's bytes and both seals untouched. Query rather than a header for the same reason the override is recorded rather than honoured silently — it is visible in Core's request log and in a hand-typed `curl`, and only `1`/`true` counts, since a typo'd value is not permission. **The flashed version carries two facts in one parameter**, because a boolean saying "I flashed something" without saying what is exactly the assertion-without-content this area exists to remove — and its presence is what makes the DUT requirement checkable at all, which this decision claimed and had no mechanism for. **Permission is not an assertion:** a run given the override that then passes on its own merits records nothing.

**Core does not orchestrate the reflash** — that needs a build, which is `embarch-api`'s job. Flashed-this-run is structurally unreachable from Core alone, since `/flash` and `/study` are separate calls with nothing linking them, and the alternative would be a persisted "last thing I flashed" record. A study submitted straight to Core with a stale bench is still rejected.

---

## Handshake identity

### 35 — `HelloAck` carries dev-bench's own hardware ID
The runtime serial link is a *physically separate USB device* from the JTAG connection, and nothing observable over USB proved the two reach the same chip: Core could confirm "the enrolled probe is attached" and "some dev-bench answered" without either implying the other. `HelloAck` is the right frame because it is already where the schema and firmware versions get checked.

*Rejected:* recording it as structurally unclosable — declined on precedent, since `embarch-topology` exists at all because a stale serial once resolved to the wrong port undetected.

**The comparison half belongs to `embarch-topology`:** the two IDs arrive in different encodings, one read over JTAG and one from whatever Zephyr's per-SoC driver decides, so relating them is *chip knowledge* — and getting that boundary wrong would have put a vendor register layout in Core. **Only a declared disagreement refuses the link:** undeclared and not-reported both pass, because the tempting rule — refuse unless it matched — would refuse every healthy bench on any chip whose relation is not yet written down.

---

## The human enrollment surface

### 25 — `GET /enroll`, a static page served by Core (retired 2026-08-24, see `embarch-ui` decision 1)
Two lessons outlived it. **Real hardware I/O and the system-file write it produces belong in Core**, which already does that under `hw_lock` — a second process calling the same function does not share that lock. And a page a browser navigates to **cannot attach a bearer token**, so it had to ask a human to paste one; `embarch-ui` holds a server-side client instead, which is why it could replace this outright. No unauthenticated route is left.

### 27 — `POST /dev-bench/link`, declaring the runtime link as its own fact
Port detection came back genuinely ambiguous between dev-bench's bridge and the DUT's own J-Link VCOM, because the only signal it had — the enrolled bench probe's *JTAG* serial — can never match a bridge that is a different physical USB device. The endpoint reaches the crate-side setter against the live Core because the standalone CLI equivalent hit exactly the NTFS permission wall this pattern predicts.

**Then `interface` was added and `serial` became optional.** A serial was named as *the* declared fact because the ambiguity it was written for was between two USB devices, which serials distinguish perfectly. The nRF54L15DK is where a serial cannot help at all: its link is on the DK's onboard J-Link — the same device as its JTAG probe — exposing **two** VCOMs under one serial, so both serials narrow to a *pair* and stop. Detection resolved such a pair by silently taking the lowest, and on this DK the console is the higher one: the guess was wrong and the bench answered nothing while the endpoint reported a confident result. **Neither field is a `400`** rather than a silent no-op — an input that cannot be honoured must fail, not be ignored.

### 28 — `POST /validate` and `GET /alerts`, reachable without touching hardware
Every live-identity re-check only ran as a side effect of `flash`/`reset`/the handshake touching hardware, so there was no way to ask "is the board enrolled as this role still the one attached" on its own. Three outcomes, each a distinct named shape rather than one generic error — which needed a typed `NotEnrolled` in the topology crate, since that branch previously raised a non-downcastable error: enough for a CLI's generic fallback, not enough to tell "not configured yet" from "a real I/O error".
