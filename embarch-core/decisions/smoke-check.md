# embarch-core decisions: The smoke check before a bench's first test

**Status:** active, 2026-11-26 (`tasks/core/167`, EMB-368; `notes/hil/03-test.md`, "Benches" and "A run" item 3). Index: [../decisions.md](../decisions.md). Builds on [test-run-executor.md](test-run-executor.md) (136: the failure policy), [test-run-setup.md](test-run-setup.md) (139), [image-readback.md](image-readback.md) (142) and [instrument-metrology.md](instrument-metrology.md) (140).

### 143 — A bench is smoke-checked before its first test, and a failing piece errors every test on it

**When.** `drive` calls `Env::smoke_check` before each bench's first test, the first bench included, after the setup prompt for a later one (the prompt still names nothing missing: the check runs on what the person set up). `smoke_check::check_bench` is the policy over a `BenchAccess`, so every failure is tested over a fake; `CoreBench` in `test_executor.rs` is the real access, each probe under `hw_lock`.

**What it checks.** (1) The signals the bench's studies' `Exchange` steps and its boards' part ids name, the roles those signals leave from (not the DUT's), and the instruments its `Instrument` steps name are declared. (2) `validate` passes for the DUT and each bench board. (3) Each bench board answers the `hello` line its bench entry carries: the echo alone is not an answer. (4) Each instrument answers `*IDN?`; the reply is kept. (5) `readback` runs for the DUT and each board. Every check runs, so the failures name every failing piece, as `piece: why`.

**Images.** The DUT's `differs` fails the check; its `claim` (Core declining to say) is recorded. A bench board's `unreleased`, `unknown` and `unverified` are **recorded, not failed**: a locally flashed board is a legitimate bench, and the status travels with the findings for the report to qualify. A DUT or board with no probe or no flash entry for its probe serial reads as `claim` or `unknown` (the log keeps one entry per chip, so another board of the chip does not stand in).

**A failure** makes **each** of the bench's tests an `error`, reason `smoke_check`, the note naming the pieces; the run goes on to the next bench (136). **Findings** are kept on `Progress.smoke` and `RunOutcome.smoke`, one per bench, and written into the run's `result.json` as `smoke_checks`; no route reads them yet (the run record is a later unit).

**The unit key** is the DUT's hardware ID from `validate`. The first bench's is kept; a later bench reading another fails with both IDs named, so bench A's results stand and bench B is refused. A DUT that validated with no readable ID carries the note `unit_identity_not_read` and keys nothing. `run.json` has a `dut.declared_serial`, but Core holds nothing to compare it with, so it is not a key here.

**Calibration.** The `*IDN?` reply is kept per instrument name (`instrument::note_identity`; forgotten when it did not answer). A calibration's `serial` matches when it equals one comma-separated field of the reply, exactly after trimming. A match is `serial_checked: true`, with `idn`; a difference is `applied: false`, `due: null` and a `note`, and `judge_measurements` reads the value as having no calibration declared, never expired. No reply kept leaves `serial_checked: false` as in 140. The reply outlives its run, since it is only the last answer.

**Measured:** unit tests over fakes (each of a missing signal, failed validate, silent hello, silent `*IDN?` and a differing DUT image erroring the bench as `smoke_check` naming its piece; a different unit refusing bench B with A standing; a pass recording every identity, reply and image status; the calibration mismatch). Timeouts (`SMOKE_WAIT_MS`, `SMOKE_PORT_WAIT_MS`) are **chosen, not measured**; the smoke check is not in `deadline` beyond each test's allowance.

**Not run (debt, `tasks/core/167`):** the check against a real bench, and a native Windows build.
