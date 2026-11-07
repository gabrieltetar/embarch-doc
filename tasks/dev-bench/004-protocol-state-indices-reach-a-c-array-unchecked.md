# Bound a protocol's `goto_state`/`otherwise` before it indexes `def->states[]`

**State:** done
**Source:** owner's repo survey, 2026-09-06 — `decisions/protocols.md` §41 states this rule; it is implemented for one index of three
**Scope:** dev-bench
**Hardware:** toolchain — host-side C plus `native_sim` ztests, no board. Reclassified from `required` 2026-09-06 (`tasks/doc/020`): the supervisor runs it in the **main checkout**, serialized like a `bench` task.
**Owner:** no

## NOT DISPATCHABLE, and the reason is a toolchain, not a board

`Hardware: required` here is honest about *dispatchability*, not about a bench. Nothing in this task
needs the DK plugged in — it is C plus ztests on `native_sim`, a host process. What is missing is
**`west`**: it is not on bare `PATH` on this machine and none of `workspaces/*` carries its own
`.venv` (`embarch-dev-bench/CLAUDE.md`), and a git worktree of this repo does not carry
`workspaces/native_sim`'s modules either. A worker cannot compile the change it makes, and a code
change nobody can build is not something to ship on an honest gate.

Filed rather than dropped because the defect is real and specific. See the companion `doc` drop on
giving a worker a runnable `west`; when that lands, reclassify this to `none`.

## What

`app/src/eap_interp.c:501` (`run->state = st->on_timeout.goto_state;`) and `:558` / `:564` / `:582`
(`target = arm->when[i].goto_state;` / `arm->otherwise` / `run->state = target;`) assign a raw wire
byte as a state index. `:485` and `:506` then do `run->def->states[run->state]`. The decoder does not
bound them either — `app/src/serial_protocol.c:452`, `:463`, `:547` read `goto_state`/`otherwise` as
`raw[(*pos)++]` with no check against `states_len`. The sibling index **is** guarded:
`eap_interp.c:456` refuses `entry_state >= def->states_len`.

Every state index that can reach `def->states[]` should be validated — refused by name at decode
alongside the existing `EAP_MAX_*` refusals, or checked at transition time so the run fails with a
named reason instead of reading past a 12-slot array. `remember[].var` at `eap_interp.c:548`, which
today silently discards an out-of-range write, should fail the same way rather than leaving the
session variable stale.

## Why now

`decisions/protocols.md` §41 states that both indices of a `RunProtocol` step are "checked before
they reach a C array subscript… which is exactly why it is checked twice and why this one fails the
step by name rather than trusting the other end". That rule is implemented for `protocol` and
`entry_state`, and not for the three indices inside a state machine.

## How to run it (`toolchain`, so these are the facts the task carries)

`west` is not on bare `PATH` and no `workspaces/*` carries a `.venv`, so the
fleet has its own, deliberately outside every repo and outside every client
workspace:

    W=/home/gabriel/Github/embarch/.west-venv/bin/west
    cd /home/gabriel/Github/embarch/embarch-dev-bench/workspaces/native_sim
    $W build -b native_sim -d <a scratch build dir> \
        /home/gabriel/Github/embarch/embarch-dev-bench/app/tests/serial_protocol
    <scratch>/zephyr/zephyr.exe        # 57 tests; exit 0 when green

Verified 2026-09-06, 57 of 57. `zephyr.exe` exits non-zero on any failure, so
its exit status is the gate — do not read the summary line and stop.

**In the main checkout, not a worktree**, and that is the whole reason this is
`toolchain`: `workspaces/*/{zephyr,modules,.west}` are gitignored, so a worktree
has no Zephyr tree to build against and a `west` binary alone buys nothing.

## Done when

- [x] A `.eap` protocol whose `when … goto`, `otherwise`, or `on_timeout.goto` names a state
      `>= states_len` is refused or fails by name, never indexed.
- [x] An out-of-range `remember` var fails the run rather than being silently dropped.
- [x] Three new ZTESTs in `app/tests/serial_protocol/src/main.c` cover each index, mirroring
      `test_an_out_of_range_entry_state_is_refused`.
- [x] The existing 50+ tests still pass under `west twister -p native_sim -T ../../app/tests`
      (met suite by suite, not by `twister`, which cannot start: see Done).
- [x] `spec.md`'s invariant list and `decisions/protocols.md` say which mechanism was chosen
      (decode-time refusal vs run-time failure).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Done (2026-11-07, the leg's own hands)

**Run-time failure, not decode-time refusal** — decision 50 in `decisions/protocols.md` says why:
a `StudyStart` the decoder refuses is dropped without a word on the link today, while a failed
run reaches Core as a named `Fail`. `eap_interp.c` checks the target before each of the three
`run->state =` assignments and a `remember`'s variable before its value is evaluated; on a bad
index the run ends as `Fail` without moving, so `final_state` names the state whose entry was
bad. The two reasons are `EAP_FAIL_NO_SUCH_STATE` and `EAP_FAIL_NO_SUCH_VARIABLE` in
`eap_interp.h`. Operand indices (`EAP_OP_SESSION`, `FIELD`, `SPAN_LEN`) were already bounded.

Four ztests, not three — one per state index plus the `remember` — each breaking one index of
the worked protocol to `states_len` (or `session_len`) and driving the machine to the move that
reads it. With the interpreter change reverted all four fail (59 of 63); with it, 63 of 63.
`twister` cannot start in the fleet venv (no `natsort`), so each suite ran on its own from the
main checkout's `workspaces/native_sim`: `serial_protocol` 63/63, `dev_bench_log` 15/15,
`scan_seen_mfg` 7/7, `scan_seen_names` 5/5. The nRF54L15DK image builds; the ESP32-C5 image was
not attempted (no `esptool` in the fleet venv, `EMB-83`).