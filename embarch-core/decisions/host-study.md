# embarch-core decisions: Host-run studies

**Status:** active, 2026-10-26.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). HTTP surface: [../interfaces/host-studies.md](../interfaces/host-studies.md). Siblings: [signal-exchange.md](signal-exchange.md) (decisions 79, 85, whose code path a step runs), [studies.md](studies.md) (decision 19's `study_lock`). Design of record: [the proposal](../../embarch-host-study-proposal.md), [`embarch-study-designer`](../../embarch-study-designer/decisions.md) decisions 80, 86.

### 95 — `POST /host-studies`: Core runs `Exchange` and `Wait` steps itself, and the teardown on every way out

Field use on a USB PD charger board (2026-09-09 to 2026-10-20): the PD source sequence ran as a bash script, 441 shell exchanges in 16 e-load runs. Each script reimplemented abort and safe state, so a run that died part-way left the load sinking and the partner at 20 V, and two runs were lost to an empty reply the script could not tell from a dropped command.

**The route.** `POST /host-studies` takes a `HostStudy` (`embarch-study-designer`), checks it, takes `study_lock` (`409` while any study, bench or host, or a `/dev-bench/hello` holds it: one lock for both kinds), checks every `Exchange` signal against topology (declared, and a direct `host-to-dut` or `bidirectional` one: `400` by step), and runs the steps on one blocking thread. `202 {study_id}`; the record is the usual `events.json`, read unchanged by `GET /study/{id}`, `/steps` and `/studies`. Lease-gated (decision 93).

**`Exchange` is the exchange route's code.** The route's body became `api::run_signal_exchange` and both call it, under `hw_lock` taken per step, not for the run: a flash can interleave between steps and gets `503` naming the holder if a step holds it. The line goes out with `\n` appended, because a `HostStep.line` carries no terminator and the signal declares none (assumed: Zephyr's shell takes `\n`, as the field scripts sent it; a per-signal terminator is a topology change, not made here).

**Outcomes decide on markers only.** `refused_on` in the reply is `Fail` (the one marker `embarch-study-designer` decision 80 allows); else `until` seen is `Pass`; else a lost port is `Fail`; else **zero bytes back is `Fail` with `detail: empty_reply`**, and bytes without `until` is `TimedOut` with `detail: until_not_seen`. No step reads a number out of a reply. `HostStepResult.outcome`'s `Fail` reason is 64 bytes, so a longer account is the record's `note` (the port names seen, the error text). Rows also carry `list`, `detail`, `reply_bytes`, `elapsed_ms` and Core's start and end times; the reply is raw, escape codes kept, capped at `MAX_HOST_REPLY_LEN` (4,096) with `reply_truncated` set (fields: [interfaces](../interfaces/host-studies.md)).

**Teardown always runs.** After the last step, after a failed or timed-out step, after a cancel and after a panic inside a step (caught). It ignores the cancel flag, runs every step even when one fails, and records each; `continue_on_fail` has no effect in it. A study stops at the first non-`Pass` step without `continue_on_fail`; the job is still `completed`, with `completed: false` and a `stopped_reason` in `events.json`.

**`POST /study/{id}/cancel`.** `202` sets a flag. The step in flight finishes (an exchange cannot be interrupted, so within its `timeout_ms`, at most 10 s; a `Wait` and a `delay_before_ms` stop within 20 ms), the remaining steps are skipped, the teardown runs. `409` for a study that is not a running host study (a bench study has no cancel), `404` for an id Core never saw.

**Events.** The proposal says `StepCompleted` is reused; it is not. A bench `StepResult` has no reply field, so a host step is its own `HostStepCompleted {study_id, list, step_index, result, detail, started_utc_ms, ended_utc_ms, delay_before_ms}` on the same SSE channel.

**Not executed, refused by name `400` at submission:** `Prompt` and `Instrument` (later units of the proposal), `Repeat` and `line_counts` (`core/116`), a non-empty `streams` (`core/101`: a signal both tapped and exchanged is opened once). **Not changed:** `HOST_TYPE_SCHEMA_VERSION` stays 19 on this branch; the landing leg bumps it to 20. No dev-bench wire change.

**Measured vs assumed.** Every exit path is proven over a scripted fake port only. **Assumed:** the `\n` terminator against the PD bench, and teardown reaching a real partner after a forced failure (hardware debts, task `core/102`).

**Open:** a cancel waits out an exchange in flight (up to 10 s); whether that is too slow for a load that must stop is unknown until a bench run.
