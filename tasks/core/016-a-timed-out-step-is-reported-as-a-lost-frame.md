# 016 — A timed-out step is reported as a lost frame, and Core's own result file is the disproof

**State:** claimed by agent/core/016-timed-out-step-names-its-step, 2026-09-06 20:28
**Source:** supervisor bench unit, leg 025, 2026-09-06 — measured against the real bench, then confirmed in source
**Scope:** core
**Hardware:** none
**Owner:** no

## Reserve (supervisor, leg 026)

`scripts/check-doc-size.py --pressure` at dispatch: **no `embarch-core` doc is in reserve.**
Write freely, but if your work pushes one into the last 10% of its cap, file
`tasks/core/<NNN>-compact-core.md` in the same commit per `tasks/README.md`.

## What

`src/study.rs:1413` builds a failed study's `reason` from `writer.last_failed_step()`, and
`last_failed_step` is only ever populated by the `if let Outcome::Fail { reason } = &result.outcome`
arm at `src/study.rs:2428`. **`Outcome::TimedOut` is not recorded.** So a study whose step times out
and stops the run takes the `None` arm and reports:

```
dev-bench stopped the study early, and the StepResult saying which step failed did not arrive
```

The comment above that arm says it plainly: *"which is what a **lost** `StepResult` looks like from
here (the undecodable-frame arm below). Said plainly rather than guessed at."* **It is not a guess,
it is a wrong statement of fact** — the `StepResult` arrived, was decoded, and was written to disk by
the same writer that then said it never came.

When this is done, a study stopped by a timed-out step names that step and says it timed out, and
the "did not arrive" wording is reserved for the case where a `StepResult` genuinely did not arrive.

## The measurement, so nobody has to reproduce it to believe it

Study `dd340b2a36a39aeba94f4f15b4da61f0`, 2026-09-06, one `BleConnect` step with
`target_address` set and `timeout_ms: 15000`, `continue_on_fail: false`.

- `study_status` returned `status: "failed"`, `result: null`, and the reason above.
- `core.log` at `01:12:21.719341Z`: `study run finished (StudyDone) completed=false`, exactly
  15.003 s after the step started.
- `C:\ProgramData\embarch\study_results\dd340b2a36a39aeba94f4f15b4da61f0\events.json.partial`
  holds, verbatim:

  ```json
  {"study_name":"leg025-attrib-7492db","steps":[{"step_name":"connect","outcome":"TimedOut",
   "captured_data":null,"gatt_services":null,"security_level":null,"protocol":null,
   "started_utc_ms":1788743526716,"ended_utc_ms":1788743541719,"delay_before_ms":0}
  ```

  (line broken here for width; it is one line in the file). **`step_name` and `outcome` are both
  present.** Nothing was lost.

- `dev-bench.log` for the same study carries no scan census, which is correct and separate —
  `report_scan_seen()` only runs on the name-filter path (`tasks/dev-bench/008`).

## Why now

This is the error a user meets the first time they aim a `BleConnect` at a `target_address` that has
gone stale, which on a random (resolvable private) address is a matter of minutes — measured on this
bench, an address present in one census was gone from the next five minutes later. **The message
sends them to look for a transport fault.** This suite has already paid, more than once, for a
confident wrong diagnosis pointing at the serial link (`embarch-decision-reversals.md`; the
"dev-bench resets mid-frame" sequence). `suite/studies-guide.md` §3b now carries a workaround
telling readers to distrust the message and read `events.json.partial`; that paragraph should be
deletable when this lands.

## Watch for

- **`TimedOut` is the only variant to add, and that is settled — do not go hunting.**
  `embarch-study-designer/src/result.rs`'s `Outcome` has exactly three variants: `Pass`, `Fail`,
  `TimedOut`. So the fix is bounded. **If a fourth is ever added, it lands in the same `None` arm
  silently**, which is worth a line in whatever you write.
- The `None` arm should still exist and should still say "did not arrive" — that case is real. What
  it must not do is claim it when a decoded result is sitting in the writer.
- A test can pin this without hardware: feed the writer a `TimedOut` `StepResult` and a
  `StudyDone { completed: false }` and assert the reason names the step. **Prove it fails against
  the current code** and quote the failure.

## Done when

- [ ] A study stopped by a timed-out step reports which step timed out.
- [ ] The "did not arrive" reason is produced only when no step result was recorded at all.
- [ ] A test covers both, and the timed-out one fails against the pre-fix code.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, and a
      `status.d/` fragment retiring `suite/studies-guide.md` §3b's last paragraph — it exists only
      as a workaround for this defect and is wrong once this lands.
