# Bound a protocol's `goto_state`/`otherwise` before it indexes `def->states[]`

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `decisions/protocols.md` §41 states this rule; it is implemented for one index of three
**Scope:** dev-bench
**Hardware:** required
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

## Done when

- [ ] A `.eap` protocol whose `when … goto`, `otherwise`, or `on_timeout.goto` names a state
      `>= states_len` is refused or fails by name, never indexed.
- [ ] An out-of-range `remember` var fails the run rather than being silently dropped.
- [ ] Three new ZTESTs in `app/tests/serial_protocol/src/main.c` cover each index, mirroring
      `test_an_out_of_range_entry_state_is_refused`.
- [ ] The existing 50+ tests still pass under `west twister -p native_sim -T ../../app/tests`.
- [ ] `spec.md`'s invariant list and `decisions/protocols.md` say which mechanism was chosen
      (decode-time refusal vs run-time failure).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
