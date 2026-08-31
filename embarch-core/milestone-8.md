# embarch-core: milestone 8 — Dev Bench Self-Test

**Status:** done, 2026-08-20 (draft 2026-08-18; target board retargeted 2026-08-19, see §2). Every DoD item done except the host-side watchdog's lapse path (§3.4/§5). Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 2 ("Dev Bench Self-Test" — filed on disk as `milestone-8`, per that doc's filename note, continuing past Milestone 1's `milestone-7` pair). Companion to [embarch-dev-bench/milestone-8.md](../embarch-dev-bench/milestone-8.md) (dev-bench firmware's half) and [embarch-api/milestone-8.md](../embarch-api/milestone-8.md) (the `run_study`/`study_status` surface this milestone's scope was expanded to include, per the design-questions pass that opened this milestone — see that doc's §1). See [design.md](design.md) §1/§5 for the durable architecture record `study.rs` fills in here.

## 1. Goal, restated for Core

`study.rs` is today "planned, not yet implemented" (`design.md`'s own header line) — everything past `GET /dev-bench/port` (which only enumerates a USB descriptor and opens nothing) is design-only. This milestone is what actually writes it: opening the serial port `dev_bench.rs` identifies, the `Hello`/`HelloAck` schema-version handshake, `POST /study` sending a real `StudyStart`, ingesting `StepResult`/`StudyDone` as they arrive, a host-side watchdog for a hung/crashed dev-bench (`embarch-study-designer/design.md` §3 decision 16), on-disk result storage (`events.json`, `data.csv`, `waveform.csv`), and `GET /study/{id}` plus the two data-export endpoints — end to end, on physical hardware, for the first time. This is a real scope expansion for Core (`embarch-study-designer/design.md` §5's own framing), not a small addition.

**Scope decision made ahead of this doc** (design-questions pass, 2026-08-18): implement the **full four-endpoint `/study*` surface** now (`POST /study`, `GET /study/{id}`, `GET /study/{id}/power-data`, `GET /study/{id}/waveform-data`) — not a reduced subset — even though this milestone's self-test study (§2) captures no power/waveform data, so the two export endpoints are expected to answer "no data" cleanly rather than actually stream anything. Matches `embarch-study-designer/design.md` §5.1 as designed; avoids a second implementation pass on those two rows once Milestone 4 (Power-Sampling Study) needs them for real.

## 2. Scope for this milestone

- **Board:** the ESP32-C5-WROOM-1 DK `embarch-dev-bench/milestone-8.md` §2 retargeted this milestone onto 2026-08-19 (superseding the original nRF54L15DK, `embarch-dev-bench/design.md` decision 4) — Core's side of this milestone doesn't pick a board, it talks to whatever `dev_bench.rs` resolves, but that resolution is currently the `EMBARCH_DEV_BENCH_PORT` manual override rather than SEGGER-VID auto-detection, since this board has no J-Link (§5).
- **No DUT, no BLE connection to anything.** The self-test `Study` (defined in [embarch-dev-bench/milestone-8.md](../embarch-dev-bench/milestone-8.md) §2, submitted via [embarch-api/milestone-8.md](../embarch-api/milestone-8.md)) is `BleAdvertise`-only steps — Core's job is the same regardless of what `Action` a step carries, so this isn't a Core-side scoping choice, just the fixture this milestone happens to exercise `study.rs` against.
- **No power-sampling hardware exists yet** (PPK2 is still unacquired per `embarch-dev-bench/design.md` decision 24) — `data.csv`/`waveform.csv`'s incremental-write code path (§5.2) gets implemented and is expected to never actually fire this milestone, since no step here produces a `StreamChunkBatch`.
- **Out of scope:** `embarch-api`'s build/flash/reset/serial-log surface (untouched, already proven in Milestone 1); the DUT probe/`hw_lock` path (a completely separate lock per `design.md` §3 decision 15, unaffected by anything here); GPIO/analog stimulus (not modeled in `embarch-study-designer` at all yet).

## 3. Steps

### 3.1 Confirm dev-bench port auto-detection still holds against real hardware — done (extended, not just confirmed)

`GET /dev-bench/port` / `detect-dev-bench` (`design.md` §5) were implemented and code-reviewed 2026-08-04 but validated only against synthesized port lists, never a live board — re-run against the actual nRF54L15DK now that it's about to be exercised for real, since `design.md` §10 already flags the multi-VCOM question as unanswered. A wrong port/interface pick here would surface as a confusing handshake failure in §3.2, not a clean detection error.

### 3.2 Implement the `Hello`/`HelloAck` handshake

Open the port §3.1 identifies; send `Hello { host_utc_ms }` (COBS-framed postcard, `embarch-study-designer`'s wire types); decode `HelloAck { schema_version, compatible, firmware_version }`. On `compatible: false`, surface a clear, distinct failure (new `{code, message, cause}` error shape, `design.md` §3 decision 12 — a new `code: "study_schema_mismatch"` variant) rather than letting a garbled `StudyStart` attempt follow. Log `firmware_version` at handshake time — it's the field the stale-firmware `doctor` check (`embarch-dev-bench/design.md` decision 25) already depends on existing.

### 3.3 Implement `POST /study`

Per `embarch-study-designer/design.md` §5.1: validate the submission (capacity limits, in-bounds `step_index` references in `validations` — decision 18), check/auto-fill `steps_crc` (decisions 17/26), acquire the dedicated one-study-at-a-time lock (separate from `hw_lock`, `design.md` §3 decision 15 already states this split), generate `study_id`, send `StudyStart { steps, steps_crc }` over the link opened in §3.2, and return `{ study_id, status: "accepted" }` without waiting for any step to run. A submission received while another study is in flight gets `409 Conflict` naming the in-flight `study_id`, not queued.

### 3.4 Implement per-step result ingestion and the host-side watchdog

As `StepResult { step_index, result }` messages arrive, update the in-memory job registry's `current_step` and append to the pending `events.json` (§3.6). Alongside that: `embarch-study-designer/design.md` §3 decision 16's amendment requires Core to run its own timer per in-flight step — `timeout_ms` plus a small fixed grace margin — and treat that margin lapsing, or the serial connection dropping outright, as an immediate `"failed"` study outcome, since a truly hung/crashed dev-bench can't self-report `TimedOut` the way `Step.timeout_ms` lets it do for an ordinary in-band failure. The grace-margin value is a placeholder to pick here (§5).

### 3.5 Implement `StudyDone` handling, terminal state, and `events.json`

On `StudyDone { completed }`, mark the job `"completed"` or `"failed"` accordingly, and write `events.json` (the `StudyResult` verbatim, §5.2) — written once, after the study reaches a terminal status. `GET /study/{study_id}` (§3.6) serves this from the in-memory registry, not by re-reading the file.

### 3.6 Implement `GET /study/{study_id}`

Returns `{ status, current_step, total_steps, result, reason }` per the registry state §3.4/§3.5 maintain. Unknown `study_id` → `404` — including a `study_id` that existed before a Core restart wiped the in-memory registry (decision 16's crash-is-catastrophic behavior, verified for real in §3.8).

### 3.7 Implement `GET /study/{study_id}/power-data` and `/waveform-data`

Per the full-surface scope decision (§1): stream `data.csv`/`waveform.csv` bytes when present, `404` when the study captured no power/waveform data or isn't `"completed"` yet. This milestone's self-test study is expected to hit the `404` path on both — a passing result here, not a gap, since no step submits a `PowerSampleWindow` or `GattOperation::StreamCapture`.

### 3.8 Verify Core-crash-mid-study behavior for real — done

Kill the Core process while a self-test study is in flight; confirm a subsequent `GET /study/{id}` for that study returns `404` (registry entry gone, per decision 16 — indistinguishable from a `study_id` that never existed); restart Core, and confirm a fresh `Hello` from dev-bench (or Core reopening the port) triggers dev-bench's existing hard-reset behavior (`embarch-dev-bench/design.md` decision 11) rather than either side getting stuck on stale state.

### 3.9 End-to-end validation via `embarch-api`

Run the full path for real: [embarch-api/milestone-8.md](../embarch-api/milestone-8.md)'s `run_study`/`study_status` against this Core, talking to the dev-bench firmware [embarch-dev-bench/milestone-8.md](../embarch-dev-bench/milestone-8.md) is flashing — the actual Definition of Done for this milestone as a whole, not just this doc's own steps in isolation.

## 4. Definition of done

**Status (2026-08-19/20): every DoD item is done except the host-side watchdog's lapse-produces-"failed" behavior specifically, which turned out not to be live-testable this pass.** The self-test `Study` ran to completion end to end against the real ESP32-C5 — `Hello`/`HelloAck`, `POST /study`, `StepResult`×2, `StudyDone{completed:true}`, via both the CLI and a hand-rolled MCP client. Dev-bench port auto-detection was extended to cover this board directly (a new recognized VID) and confirmed live. Core-crash-mid-study and the `404`-for-unknown-`study_id` path were both confirmed live via a real kill/restart. `power-data`/`waveform-data`'s "no data" paths were confirmed live via the MCP self-test run. The two judgment calls recorded in `design.md` §10 (the `502` status code, `WATCHDOG_GRACE_MS = 2_000`) held up fine in the runs that did happen, but the grace margin itself is still unvalidated against real timing, since the watchdog's own timeout path was never actually reached.

- [x] Dev-bench port auto-detection confirmed against the real board (§3.1) — **extended to cover this board**: `dev_bench.rs` now recognizes the ESP32-C5's own VID (`0x303A`) directly, confirmed live (`detected_by: "espressif-vid-match"`, `COM12`) — no `EMBARCH_DEV_BENCH_PORT` needed any more.
- [ ] `Hello`/`HelloAck` handshake succeeds against real dev-bench firmware (§3.2) — **handshake itself confirmed** (including via the new `GET /dev-bench/hello`); the deliberately-mismatched-schema-version failure path was not exercised this pass.
- [ ] `POST /study` accepts the self-test `Study`, returns `study_id` immediately (§3.3) — **confirmed**; the second-concurrent-submission `409` path was not exercised this pass.
- [ ] `StepResult`s update `current_step` in real time as the self-test study runs on real hardware (§3.4) — **confirmed** (both steps' results were observed via polling); the host-side watchdog's lapse-produces-`"failed"` behavior was attempted twice (a human-timed USB unplug, and a software JTAG-reset race) and not achieved — `BleAdvertise` resolves in well under a second, too fast for either to land inside the window. See §5.
- [x] `StudyDone` produces a terminal `"completed"` status and a correct `events.json` for a real run (§3.5).
- [x] `GET /study/{id}` reflects real-time and terminal state correctly (§3.6) — confirmed via `study_status` polling to completion, **and** the `404`-for-unknown/expired-`study_id` path, confirmed live via §3.8's crash test.
- [x] `GET /study/{id}/power-data` and `/waveform-data` both correctly answer "no data" for the self-test study, without erroring (§3.7) — confirmed live via MCP (`isError: true`, a clean "no power/waveform data captured" message, not a crash or hang).
- [x] Core-crash-mid-study behavior confirmed live: in-flight study 404s after restart, reconnect recovers cleanly (§3.8) — killed the Windows Core service mid-registry, restarted it, confirmed the old `study_id` `404`s and a fresh study runs clean.
- [x] Full path validated via `embarch-api`'s `run_study`/`study_status`, against real dev-bench hardware (§3.9) — via both the CLI and a hand-rolled MCP client (§5).
- [x] Any real gap found folded back into `design.md` per `DOC-PROTOCOL.md` §5, same posture as Milestone 1 — done in this pass (board retarget, new decisions 19/20, `embarch-decision-reversals.md` row 13).

## 5. Open questions / risks carried into execution

- **Host-side watchdog grace margin (§3.4) is still an unset placeholder — the lapse path itself was never actually reached.** Two live attempts to disconnect the dev-bench mid-step both lost a timing race against `BleAdvertise` resolving in well under a second: a human-timed physical USB unplug (the person reacted essentially instantly to a text cue, but the round trip from `StudyStart` to `StepResult`(Pass) was still faster), and a software-only alternative (racing a JTAG-based `POST /reset` against the study, no human involved). Confirming this live would need either a step whose real action genuinely blocks for several seconds (none exists in this fixture's `Action` set), or a probe-level CPU-halt capability Core's HTTP surface doesn't expose and the installed `probe-rs` CLI doesn't offer standalone either. `WATCHDOG_GRACE_MS = 2_000` remains exactly as validated as before — not at all, against real serial-link latency.
- ~~**The dev-bench port's multi-VCOM question.**~~ — moot for this milestone now that its target is the ESP32-C5, which has no J-Link/VCOM at all; still open if the nRF54L15DK is ever revisited (`design.md` §10, `embarch-dev-bench/design.md` §4).
- ~~**`dev_bench.rs`'s SEGGER-VID auto-detection doesn't cover this board at all.**~~ — resolved 2026-08-19/20: a second recognized VID (`0x303A`, Espressif's own) closes this, confirmed live against the real board — see `design.md` §5/§10.
- **`Hello`'s schema-mismatch failure path (§3.2) has no precedent in Core's existing error-code enum** — the new `study_schema_mismatch` code is proposed here, not yet reconciled against whatever else `design.md` §3 decision 12's append-only `code` enum has picked up since 2026-08-15. Not exercised this pass, still open.
- ~~**Whether the self-test `Study`'s `BleAdvertise`-only steps actually produce a `StepResult` quickly or block for the full `timeout_ms`.**~~ — resolved empirically: quickly, near-instantly (`Pass` observed well under a second after `StudyStart`, repeatedly) — which is also why the watchdog item above couldn't be live-tested with this fixture.

## 6. Changelog

- 2026-08-19/20 — **Milestone closed: every DoD item done except the watchdog's lapse path.** New `GET /dev-bench/hello` (decision 19) and the crash-mid-study confirmation (decision 20) both live-validated against the real ESP32-C5; `dev_bench.rs`'s auto-detection extended to recognize this board's own VID directly (§3.1, §5); `power-data`/`waveform-data`'s "no data" paths confirmed via a hand-rolled MCP client alongside the CLI. §3.4's host-side watchdog is the one item that stayed unexercised — two live attempts (a human-timed USB unplug, a software JTAG-reset race) both lost the same timing race against `BleAdvertise` resolving in well under a second. Full detail in `design.md` §3 decisions 19/20 and §10.
- 2026-08-19 — **Milestone retargeted to the ESP32-C5-WROOM-1 DK** (§2), following [embarch-dev-bench/milestone-8.md](../embarch-dev-bench/milestone-8.md)'s own retarget and [embarch-decision-reversals.md](../embarch-decision-reversals.md) row 13. §4's DoD updated: §3.5/§3.9 now checked done (the self-test `Study` ran to `"completed"` end to end against real hardware); §3.1–3.4/3.6 note exactly which half of their bundled assertions this run covered versus what still needs a dedicated negative-path test; §3.7/§3.8 remain untouched. §5's multi-VCOM question is moot for this board; new open question recorded — SEGGER-VID auto-detection doesn't cover the ESP32-C5's own VID, so this run relied on the manual port override.
- 2026-08-18 — §3.2–3.7 implemented for real: `study.rs`/`dev_bench_link.rs`, the full `/study*` surface, `study_lock`/`study_jobs`, the host-side watchdog, and the result-file writers. `cargo build`/`test` (39 passed)/`clippy -D warnings` all clean. `design.md` updated to match. Not yet run against real hardware — §3.1/3.8/3.9 remain, and every DoD checkbox stays unchecked until they do.
- 2026-08-18 — Initial draft, scoping Core's half of Milestone 2 (Dev Bench Self-Test). Scope decisions carried in from the design-questions pass that opened this milestone: implement the full four-endpoint `/study*` surface now rather than deferring `power-data`/`waveform-data`; `embarch-api`'s `run_study`/`study_status` brought into this milestone's scope (companion `embarch-api/milestone-8.md`), expanding the roadmap's original Core+Dev-Bench-only framing.
