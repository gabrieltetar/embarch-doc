# embarch-core decisions: Running a study

**Status:** active, 2026-09-18.

The study loop: the handshake route that needs no study, what happens when either side dies, the watchdog, frame-level resilience, and what a failure is told to blame. What a client can *read* about a study — during it and long after — is [study-record.md](study-record.md), split out 2026-09-18 when this file reached its cap; a split by mission, moving entries verbatim, per [../../DOC-BUDGET.md](../../DOC-BUDGET.md) §3. What Core *checks* at that handshake before any step runs — the version gate and the bench's hardware identity — is [handshake.md](handshake.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Studies: execution and failure

### 19, 20 — A handshake with no study, and crash-mid-study confirmed rather than assumed
The handshake already ran on every submit and discarded the ack after logging it, so nothing could ask "what firmware is on this bench" without starting a real study; `/dev-bench/hello` guards an in-flight study with a `409` rather than racing to open the same port twice. Separately, killing the service outright mid-registry and restarting it confirmed the documented behaviour: a previously-real `study_id` `404`s, indistinguishable from one that never existed, by design, and a fresh study immediately after completed cleanly. No code changes — the behaviour was right and had never been run against a real crash.

### 33 — The watchdog deadline includes `delay_before_ms` — a live defect, not a refinement
The deadline ignored the field while dev-bench honours it by sleeping *before* the step runs, so any step whose delay exceeded its own timeout plus grace failed a study whose bench was working perfectly — squarely on the intended path, since multi-second delays are the point of that field. Found by a design pass reading the function for another reason, never by a test, because every fixture used a zero delay.

*Declined:* moving the sleep host-side, which folds link jitter into authored timing; and rejecting such a step at submit, which forbids a legitimate long soak and leaks an internal constant into the authoring contract. `timeout_ms` means "how long this step may take", never "how long until I hear back".

### 40 — An undecodable frame costs the frame, not the link; and `completed: false` is no longer success
`recv` returned `Result<Option<_>>`, so a frame that arrived and failed to decode was indistinguishable from a read error and broke out of the run. The consequence was specific: **the step result carrying a failed step's reason is the longest message dev-bench sends, it is the one that gets truncated, and refusing it tore down the link and reported a connection error with no mention that a step had failed.**

**The resilience fix is what found the cause of the fault it was written to tolerate.** Reading past the bad frame showed thirteen seconds of silence, and the next handshake's uptime placed a bench **reset** within 150 ms of the truncation. It had been crashing mid-transmission all along, and every host-side reading of those bytes — including two well-evidenced wrong ones — had been describing the wreckage.

**`StudyDone { completed: false }` was reported as `"completed"`**, so a run that died at step 5 of 11 came back clean. A study that stops early now fails and names the step; where the step's outcome carries words of its own, those words are quoted, because dev-bench sends the diagnosis exactly once [the flat "in that step's own words" written here originally was true only of `Outcome::Fail` and is what decision 45 had to correct — a `TimedOut` step has no words]. Two smaller findings: the shortfall arithmetic was out by one and **the wrong number had become the name of a bug** — corrected, the occurrences read 13/15/17/17/13/17, which is what a crash with variable timing produces and what a buffer boundary does not; and bytes that never formed a frame were invisible, which was exactly the evidence that mattered, since the bench's console *is* this UART and a timeout reported "no message received" while holding 699 bytes of boot banner.

### 45 — A step that timed out stopped the study too, and the reason says so rather than blaming the link
`EventsJsonWriter` recorded a study-stopping step from `if let Outcome::Fail { reason }` only. `Outcome::TimedOut` fell straight through it, so a study killed by an exhausted `timeout_ms` reached decision 40's no-record arm and reported *"the StepResult saying which step failed did not arrive"* — **about a step the same writer had already serialized to `events.json.partial`, `step_name` and `outcome: "TimedOut"` and all.** Measured 2026-09-06, study `dd340b2a36a39aeba94f4f15b4da61f0`: one `BleConnect` at a `target_address` gone stale, 15.003 s to `StudyDone { completed: false }`, `events.json.partial` intact on disk. The message describes a lost frame, and this suite has already paid twice for a confident wrong diagnosis pointing at the serial link.

**The reason now branches, and each branch says a different thing.** A recorded `Fail` names the step and quotes dev-bench's reason verbatim; a recorded `TimedOut` names the step and says it timed out, there being no reason field to quote; and the "did not arrive" wording is now reached **only** when no study-stopping outcome was recorded at all — which is what an undecodable frame looks like from here, since it never reaches `write_step`. That arm is real and keeps its words. Built as `EventsJsonWriter::early_stop_reason`, one method rather than an expression inside the run loop, which is what let a test pin all three branches without hardware.

**The recording match is exhaustive with no wildcard arm**, so a fourth `Outcome` variant is a compile error there rather than a silent join with `Pass` in the nothing-stopped-the-study bucket. That silence *was* the defect: `Outcome` has exactly three variants today (`embarch-study-designer`'s `result.rs`), and the cost of the guard is zero.

*Consequences:* `suite/studies-guide.md` §3b's workaround paragraph — read the message as "a step timed out" and confirm against `events.json.partial` — is retired.

---
