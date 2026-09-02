# embarch-study-designer decisions: Study structure and execution

**Status:** active, 2026-09-02.

What a step is, how a study fails, and the fuzzing loop.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 13 — Per-step, not per-study, fail-continuation: `Step.continue_on_fail: bool`

A study's steps mix "must pass or the rest is meaningless" checks (a `BleConnect` — nothing downstream works without a connection) with "record and move on" ones (a `DataExchange` that is informational for a fuzzing run rather than fatal to it). A single study-wide switch can't express that mix; a per-step bool can. Defaults to `false` (abort immediately on this step's `Fail`/`TimedOut`), matching typical test-runner semantics; an author opts a specific step into `true` only where continuing past its failure is useful.

This is also the knob for "attempt it but don't insist" wherever that comes up — decision 44 declined to add a second flag for exactly that reason.

### 14 — Correlation by array position (`step_index: u32`), not by `Step.name`

`Step.name` stays purely a human-readable label — useful when a person reads `events.json` (§5.2) — and nothing in the wire types uses it to locate a step. `Study.steps` is already order-significant (§4.1), so a step's position is already a unique, stable-within-that-study identifier; reusing it costs no new field and sidesteps the ambiguity a name lookup would have if an author (or a fuzzer generating steps) gave two steps the same name.

Encoded as `u32`, not `usize`: `usize`'s width isn't fixed across the architectures this wire format actually crosses (a 64-bit host vs. a 32-bit nRF54 MCU, decision 7), and postcard would encode a mismatched-width `usize` inconsistently between them.

### 42 — `Step.delay_before_ms` — the "when" half of authoring a stimulus

Steps run strictly in sequence, so until this the only expressible timing was "immediately after the previous step finished". That isn't enough to author a stimulus: letting a DUT settle after a connect, or waiting inside an open `GattMonitorStart` window before writing so the transcript visibly separates unsolicited traffic from the response, both need a delay that isn't a side effect of some other step's `timeout_ms`.

Deliberately **not folded into `timeout_ms`**: this is time spent before the action starts, so it doesn't consume the action's budget, and `Outcome::TimedOut` keeps meaning "the action took too long" rather than "the delay was too long". It also **replaced a workaround** — the UI's capture template previously held the run open with a `GattMonitorAll` step, which re-subscribes inside an already-open window; a delay on the `GattMonitorStop` step does that job without a second action.

Declared and encoded **last**, on purpose: postcard is field-order-sensitive with no field names on the wire and dev-bench hand-decodes `Step` in C, so appending gave that decoder one extra trailing varint read instead of a reshuffled sequence. Wire v5 → v6 — appending is still a wire break in both directions, and the handshake refusing the mismatch outright is the point. Covered by `steps_crc`, so the timing an engineer authored is inside the integrity seal.

### 51 — `Study.dev_bench_log_level` — how loud the bench should be is a property of the run

[embarch-dev-bench/decisions.md](../../embarch-dev-bench/decisions.md) decision 38 made dev-bench's `CONFIG_LOG` output reach Core, and made it reach Core *always*, because the only knob was a compile-time Kconfig level. This is the type change that moves the knob to the study. `DevBenchLogLevel { Off, Error, Warn, Info, Debug }`, fieldless so postcard encodes a single varint discriminant, appended to `Study` and — after `streams_crc`, never inserted — to `StudyStart`. Wire v12 → v13, host v14 → v15: dev-bench parses the field and acts on it.

Three shape decisions, each with a plausible alternative:

- **On `Study`, not a submission-time override.** A `POST /study` query parameter would have avoided touching this crate at all, but would then need threading through `embarch-api`'s MCP tool, its CLI and the UI's submit path separately, and a saved study could not carry it. On `Study` it works through every path that already exists, and `#[serde(default)]` means every study file authored before the field still loads at `Warn` — which is what those studies effectively already ran at, so the default is *correct* rather than merely permissive.
- **A scalar, not a property of the reserved `DevBenchLog` tap.** That tap looks like the more idiomatic home (capture is declared, not implicit — decision 39), but it is synthesized by Core, never crosses the dev-bench hop (§4.8), and a `StreamScope` window would drop precisely the lines emitted *between* steps.
- **Outside both seals, deliberately** — decision 17's rule.

`Warn` is the default rather than `Off`, and the asymmetry is the point: an `<err>`/`<wrn>` line is rare by construction and is exactly what someone needs to read about the run that just failed. `Off` exists for the study that genuinely needs a clear link and accepts being blind, including to the fatal-error dump. `DevBenchLogLevel::zephyr_level()` lives here rather than in the firmware so the discriminant→severity mapping has one home; the C side reads the same numbers as `DBM_LOG_LEVEL_*`, which is why no translation table exists there — small, but this project has already had two hand-mirrored constants go stale (`embarch-dev-bench/app/CMakeLists.txt`'s own note on `STUDY_FFI_STUB_SCHEMA_VERSION`).

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

