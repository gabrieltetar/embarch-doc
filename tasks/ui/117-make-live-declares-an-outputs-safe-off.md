# 117 — Make live declares an output's safe-off

**State:** done — Make live declares and carries a safe-off; decision 90 amended
**Source:** HIL implementation plan (`notes/hil/14-implementation-plan.md`, attested phase): the safe-off field landed on `Instrument` and `SignalLink` in `embarch-topology` (`topology/072`, `suite/059`), and Make live still sends it empty
**Issue:** EMB-337
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`embarch-topology` decision 49 now gives `Instrument.safe_off: Vec<String>`
(one command per line) and `SignalLink.safe_off: Option<String>`; Core's
`PUT /instruments` and `POST /signals` store them and answer `400` for a bad
line. Make live (decision 90, `src/bench/live.rs` and the Topology tab) declares
a bench's instruments and signals with the person's token, and since
`suite/059` it sends an empty safe-off on every declaration.

When this is done each instrument declaration on Make live takes an optional
safe-off (one line per command) and each signal declaration an optional one
line, sent with the person's token like the rest of the declaration; a
declaration without one shows "no safe-off declared" beside it. The terminal
path `embarch-ui bench make-live` (`ui/116`) sends the same field from the
saved bench.

**Carry a declared safe-off through a re-declare** (Finding comment on
EMB-337, 2026-11-24): `PUT /instruments` replaces an instrument by name, so a
Make live that sends an empty safe-off silently drops one declared by another
path (the api's tools gain the field in `api/187`, in flight beside this one).
Decide how Make live avoids that (for example, prefill from what Core already
holds, or from the saved bench), and record the rule by amending decision 90.

## Why now

The person setting up a bench is who declares what a Core start switches off.
EMB-337.

**Burndown leg: no new numbered decision.** Amend decision 90 in place. If the
change seems to need a new decision, stop and say so in this file.

**Doc-size reserve (dispatch note):** no `embarch-ui` file is in reserve.
Decisions near their per-decision limit are ones this task does not touch
(trace-view#10, gatt-capture#17, trace-chart#10, launcher#28, tab-folders#100,
topology-tab#10, trace-transfer#18, topology-tab#43). If the Topology tab's
decision 43 must change, it has 207 B.

## Done when

- [x] A declaration with a safe-off round-trips through the form to a fake
      Core with the person's token.
- [x] One without shows "no safe-off declared".
- [x] A re-declare does not drop a safe-off Core already holds, by the rule you
      chose, with a test.
- [x] Decision 90 amended; `spec/bench-live.md` updated.
- [x] Gate green (`../../embarch-fleet/gate.md`).
- [x] `changelog.d/` fragment dropped.

## Done

**Rule chosen (decision 90 amended, spec/bench-live.md):** what the bench states wins; a bench stating none keeps the safe-off Core already holds (read from `GET /instruments` / `GET /signals` before the writes), and the row says so. Make live never clears one; an instrument stating none is not declared while Core's list is unread. Entry: the part inspector's Safe-off box (saved as `Part.safe_off`) and a `safe_off` key on `[[signals]]`. Test: `make_live_declares_a_safe_off_and_carries_one_core_already_holds` (embarch-ui `src/main.rs`).

**Not done:** no signal editor in the page (signals have none today), so a signal's safe-off is a file key. The browser drive (`tests/browser`) was not run for the new textarea (no browser here); the textarea is only `node --check`ed. Token: the stub Core does not check bearer tokens, the declaration goes through the same client as before.
