# embarch-study-designer decisions: Study structure and execution

**Status:** active, 2026-09-02.

What a step is, how a study fails, and the fuzzing loop.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 13 — Per-step, not per-study, fail-continuation: `Step.continue_on_fail: bool`

A study's steps mix **"must pass or the rest is meaningless"** checks — nothing downstream works without a connection — with **"record and move on"** ones. **A single study-wide switch cannot express that mix; a per-step flag can.** Defaults to aborting immediately, **and an author opts a specific step out only where continuing past its failure is useful.**

This is also the knob for "attempt it but don't insist" wherever that comes up — decision 44 declined to add a second flag for exactly that reason.

### 14 — Correlation by array position (`step_index: u32`), not by `Step.name`

A step's name stays **purely a human-readable label, and nothing in the wire types uses it to locate a step.** The step list is already order-significant, **so a step's position is already a unique, stable-within-that-study identifier** — reusing it costs no new field and **sidesteps the ambiguity a name lookup would have if an author, or a fuzzer, gave two steps the same name.**

A fixed-width integer rather than a pointer-sized one: **that width is not fixed across the architectures this wire format actually crosses, and postcard would encode a mismatched one inconsistently between them.**

### 42 — `Step.delay_before_ms` — the "when" half of authoring a stimulus

Steps run strictly in sequence, so **until this the only expressible timing was "immediately after the previous step finished". That is not enough to author a stimulus:** letting a DUT settle after a connect, or **waiting inside an open capture window before writing so the transcript visibly separates unsolicited traffic from the response**, both need a delay **that is not a side effect of some other step's timeout.**

Deliberately **not folded into the timeout**: this is time spent *before* the action starts, **so a timed-out outcome keeps meaning "the action took too long" rather than "the delay was too long".** It also **replaced a workaround** — the UI's capture template held the run open with a second monitor step, **which re-subscribes inside an already-open window.**

Declared and encoded **last, on purpose**: postcard is field-order-sensitive with no field names on the wire and **the bench hand-decodes the step in C, so appending gave that decoder one extra trailing varint read instead of a reshuffled sequence.** Covered by the seal, **so the timing an engineer authored is inside the integrity check.**

### 51 — `Study.dev_bench_log_level` — how loud the bench should be is a property of the run

Dev-bench's log output reaching Core **reached it *always*, because the only knob was a compile-time level.** This is the type change that **moves the knob to the study**: a fieldless level enum, appended rather than inserted, **which dev-bench parses and acts on.**

Three shape decisions, each with a plausible alternative:

- **On the study, not a submission-time override.** A query parameter would have avoided touching this crate at all, **but would then need threading through the MCP tool, the CLI and the UI's submit path separately — and a saved study could not carry it.** On the study it works through every path that already exists, and **defaulting means every study file authored before the field still loads at the level those studies effectively already ran at: the default is *correct* rather than merely permissive.**
- **A scalar, not a property of the reserved log tap.** That tap looks like the more idiomatic home, **but it is synthesised by Core, never crosses the bench hop, and a scope window would drop precisely the lines emitted *between* steps.**
- **Outside every seal, deliberately** — decision 17's rule.

**Warning is the default rather than silent, and the asymmetry is the point:** an error or warning line is **rare by construction and is exactly what someone needs to read about the run that just failed.** Silent exists for the study that **genuinely needs a clear link and accepts being blind, including to the fatal-error dump.** The discriminant-to-severity mapping lives here rather than in the firmware **so it has one home, and the C side reads the same numbers rather than a translation table — small, but this project has already had two hand-mirrored constants go stale.**

---

### 9 — Async, job-based execution for the Core↔dev-bench-bridging HTTP surface, not a blocking call like `/flash`

A study's BLE steps (advertise, wait for a connection) can legitimately take unbounded time, unlike Core's existing bounded operations — a synchronous call would need an unreasonably long client-side timeout or risk truncating a study mid-run. Core accepts a `Study`, returns a `study_id` immediately, and reports progress via polling. Endpoint shapes in §5.1; this decision covers the *shape* of the interaction, a property of the whole study-execution flow rather than of Core's implementation.

### 16 — A crash mid-study on either side is catastrophic for that study, and dev-bench's needs a host-side watchdog to be detected at all

Each `Step.timeout_ms` self-bounds any single hung action, so dev-bench is never stuck past a step's own budget — but that says nothing about the *study* if Core disappears (crash, unplugged, restarted). That study is written off: Core's in-memory job registry doesn't survive a restart and Core is what persists `events.json`/`data.csv`, so a study in flight when Core dies never gets a `StudyResult`, and a caller polling that `study_id` afterwards gets `404`, indistinguishable from an id that never existed. Raw data already streamed to disk may still be sitting there — a partial diagnostic artifact, not a completed result — since decision 20 writes incrementally.

**A dev-bench crash or hang is symmetrically catastrophic and cannot use the same detection.** `Step.timeout_ms` is enforced *by dev-bench*; if dev-bench is what hung, nothing device-side is left to report `TimedOut`. So Core enforces its own watchdog: it expects a `StepResult` for the in-flight step within `timeout_ms` plus a small fixed grace margin [assumed], and treats that margin lapsing — or the serial connection dropping — as an immediate `"failed"` outcome, the same terminal state a device-reported `Fail` produces, just detected by Core.

Recovering the *connection* in either direction is decision 12's `Hello`-as-hard-reset: when Core reconnects, dev-bench aborts whatever it was still running and both sides start clean.

### 29 — The fuzz-testing loop is documented, not changed

Review item 40 flagged that a 64-step ceiling, no queue, and a `409 Conflict` on concurrent submission make a fuzzing driver look like an awkward N-round-trip loop against a rejection. Examined and left as-is deliberately: raising the ceiling doesn't help a fuzzer exploring many *distinct* short studies rather than one long one (§4.1 already frames a `Study` as fuzzing's *output*, one concrete value per run), and a queue is real new machinery — persistence, ordering, partial-failure semantics — this suite has avoided everywhere else (`embarch-api/decisions.md` §3.6's no-database stance).

The intended shape, stated explicitly: a fuzzing driver runs entirely client-side, generating one `Study` at a time, submitting it, polling `GET /study/{id}` to a terminal status, then generating the next. **The poll loop *is* the intended backpressure mechanism**, not a workaround for a missing one.

---

