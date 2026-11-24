# 118 — Make live skips a signal whose stored safe-off it cannot read

**State:** open
**Source:** the reviewer of `ui/117` (Make live declares an output's safe-off), below its bar, filed as a bug
**Issue:** EMB-401
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Since `ui/117`, Make live (`src/bench/live.rs`, `apply_bench`) reads
`GET /instruments` and `GET /signals` before declaring, so a declaration whose
bench entry states no safe-off keeps the one Core already holds (decision 90).
For an **instrument**, a failed read means the instrument is not declared and a
failed row says why. For a **signal** it does not: when `GET /signals` fails,
the carry-over is skipped and every signal is still posted, so a signal whose
bench entry states no safe-off is declared with none, dropping Core's. A
leftover row reports the unread list, but the signal is declared anyway.

When this is done a signal is treated as an instrument is: with the signal list
unreadable and no safe-off on the bench entry, the signal is not posted and a
failed row names the reason. A signal whose bench entry states a safe-off is
unaffected, since it does not need Core's. The terminal path
(`embarch-ui bench make-live`) shares the code and gets the same behaviour.

## Why now

A safe-off is what a Core start switches an output to, so silently dropping one
is the failure decision 90's carry-over rule exists to prevent. EMB-401.

**Burndown leg: no new numbered decision.** Amend decision 90 in place to state
the signal case. If the change seems to need a new decision, stop and say so in
this file.

**Doc-size (dispatch note):** no `embarch-ui` file is in reserve. **Decision 90
(`decisions/bench-live.md`) is already 332 B over the 4 KB per-decision cap**
(unpinned, so the gate reports it rather than failing). State the signal case
without growing it: fold the signal into the sentence that states the
instrument case, and if you can, bring it back under 4,096 B. Other `embarch-ui`
decisions near their limit (launcher#28, tab-folders#100, topology-tab#10 and
#43, trace-* and gatt-capture#17) are ones this task does not touch.

## Done when

- [ ] With `GET /signals` failing and no safe-off on the bench entry, the signal
      is not posted and a failed row names the reason, in a test against a fake
      Core.
- [ ] A signal whose bench entry states a safe-off is still posted in that case.
- [ ] Decision 90 states the signal case, no larger than it is now.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `changelog.d/` fragment dropped.
