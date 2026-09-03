# embarch-core decisions: Running a study

**Status:** active, 2026-09-02.

The dev-bench link's lifecycle: the handshake, what happens when either side dies, why no result is held in memory, the watchdog, frame-level resilience, and the version gate.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Studies: execution and failure

### 19, 20 — A handshake with no study, and crash-mid-study confirmed rather than assumed
The handshake already ran on every submit and discarded the ack after logging it, so nothing could ask "what firmware is on this bench" without starting a real study; `/dev-bench/hello` guards an in-flight study with a `409` rather than racing to open the same port twice. Separately, killing the service outright mid-registry and restarting it confirmed the documented behaviour: a previously-real `study_id` `404`s, indistinguishable from one that never existed, by design, and a fresh study immediately after completed cleanly. No code changes — the behaviour was right and had never been run against a real crash.

### 24 — Core never materialises a `StudyResult` host-side
[Measured] `StudyResult` is **~1.3 MB** purely from `no_std` worst-case capacities, reserved unconditionally regardless of what a study populates. The old path accumulated every step result, converted once at the end, kept it resident forever, and cloned it by value on every `GET`. Two of those reproduced a real stack overflow on both Linux and Windows in `cargo test`; deserialising into the same type overflowed too, confirming it is the **type** that is unsafe to hold, not one code path. Fixed by writing one step result **by reference** the instant it arrives, finalising only at a real `StudyDone` and leaving `.partial` behind on an abort as a diagnostic artifact.

**The SSE route is the live-push companion**, one broadcast channel filtered to the URL's id — one suffices because `study_lock` never allows two studies. A slow subscriber gets an explicit `lagged` frame rather than silently missing messages. A deliberate reversal of the original polling-only framing: nothing about a result is held back until the study finishes, at any layer.

### 41 — `/study/{id}/events` stays a fresh subscription on reconnect, not a resumable one
The handler reads no `Last-Event-ID` and the broadcast channel keeps no backlog for a new subscriber to replay — a client that disconnects and resubscribes starts at "now," with no record of what it missed and no signal that anything was missed at all, unlike a lagged-but-connected subscriber, which `lagged` already covers. Stated here rather than left implicit, because `embarch-core/interfaces.md` is exactly the row a new client reads before deciding it can reconnect and carry on: `GET /study/{id}` is the authoritative record such a client falls back to. **Closed as not needed yet:** both current consumers (`embarch-api`'s `study-status --follow` and `study_watch`) already fall back to polling on a drop rather than assuming continuity, so nothing today asks Core to remember what a gone subscriber missed. A resumable stream — a per-event sequence number, a bounded replay buffer — is a real design if a future consumer needs one, not a gap in this one.

### 33 — The watchdog deadline includes `delay_before_ms` — a live defect, not a refinement
The deadline ignored the field while dev-bench honours it by sleeping *before* the step runs, so any step whose delay exceeded its own timeout plus grace failed a study whose bench was working perfectly — squarely on the intended path, since multi-second delays are the point of that field. Found by a design pass reading the function for another reason, never by a test, because every fixture used a zero delay.

*Declined:* moving the sleep host-side, which folds link jitter into authored timing; and rejecting such a step at submit, which forbids a legitimate long soak and leaks an internal constant into the authoring contract. `timeout_ms` means "how long this step may take", never "how long until I hear back".

### 40 — An undecodable frame costs the frame, not the link; and `completed: false` is no longer success
`recv` returned `Result<Option<_>>`, so a frame that arrived and failed to decode was indistinguishable from a read error and broke out of the run. The consequence was specific: **the step result carrying a failed step's reason is the longest message dev-bench sends, it is the one that gets truncated, and refusing it tore down the link and reported a connection error with no mention that a step had failed.**

**The resilience fix is what found the cause of the fault it was written to tolerate.** Reading past the bad frame showed thirteen seconds of silence, and the next handshake's uptime placed a bench **reset** within 150 ms of the truncation. It had been crashing mid-transmission all along, and every host-side reading of those bytes — including two well-evidenced wrong ones — had been describing the wreckage.

**`StudyDone { completed: false }` was reported as `"completed"`**, so a run that died at step 5 of 11 came back clean. A study that stops early now fails and names the step **in that step's own words**, because dev-bench sends the diagnosis exactly once. Two smaller findings: the shortfall arithmetic was out by one and **the wrong number had become the name of a bug** — corrected, the occurrences read 13/15/17/17/13/17, which is what a crash with variable timing produces and what a buffer boundary does not; and bytes that never formed a frame were invisible, which was exactly the evidence that mattered, since the bench's console *is* this UART and a timeout reported "no message received" while holding 699 bytes of boot banner.

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
