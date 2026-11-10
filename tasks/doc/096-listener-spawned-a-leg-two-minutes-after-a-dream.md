# 096 — The listener spawned a leg into a dry queue two minutes after a dream

**State:** open
**Source:** the leg started 2026-10-29 18:03 (`leg-start` in `.fleet/tick.log`), which found itself spawned against the gate. The leg before it posted a dream at 18:01:16 (`ts` `1793318476.457199`, `crystal_ball` on it), logged its close at 18:02:23 and ran `leg-end` at 18:02:30. The listener ticked at 18:02:59 and a leg started at 18:03:04. At that moment `queue-status.py --no-supervisor --count` was 0 (`main` at `178affa2` since 18:01:56, `inbox/` empty) and the `crystal_ball` marker was under two minutes old.
**Scope:** doc
**Hardware:** none
**Owner:** required — the gate is prose in `.claude/commands/fleet.md`, generated from `embarch-fleet`'s template, both reserved.

## What

`fleet.md` STEP 2 says: count zero, spawn a leg **only if** `crystal_ball` is absent or older than six hours. Both conditions for refusing held, and the listener spawned anyway. The spawned leg did what the dream's handoff said (ended after step 0, filed nothing but this), so the cost was one leg's step 0. The cost if it repeats on every leg death is a chain of empty legs a few minutes apart until the owner answers the dream, with no watchdog alarm, because each of them ticks.

Not verified: why. The wake was a leg's completion notification rather than the cron, five seconds before the spawn. One reading consistent with that: the pump section ("a leg's death wakes this window and the next leg is spawned") states the relay without the gate, and a completion wake followed it rather than STEP 2. The previous dream (2026-10-28 22:32) was followed by ten cron ticks and no spawn, so the gate has held at least once.

**Seen again 2026-11-06, the same shape.** The leg that landed `atlas/035` posted a dream at 13:42 (`ts` `1793997725.841939`, `crystal_ball` on it), ran `leg-end` at 13:42:58; the listener woke at 13:43:16 and a leg started at 13:43:26. That leg's step 0 read Fleet Ready empty, `queue-status.py` 0 dispatchable on `main` at `47562d21`, no reply in the dream thread, and `fleet-read.py`'s `markers:` showing `crystal_ball` 2 minutes old. It ended after step 0, posted no second dream, and added only this paragraph. Two of two observed post-dream relays spawned an empty leg on a completion wake, so the "one reading" above is now the likely one. On 2026-10-29 the empty leg's own death (18:06:56) was followed by a listener tick at 18:07:26 and no spawn, so the chain stopped at one empty leg; the cost per dream is one step 0, not an unbounded chain.

**Seen a third time 2026-11-10, the same shape.** The leg that landed `chat/024` ended burndown on an empty queue, posted a dream at 13:21 (`ts` `1794342092.017879`, `crystal_ball` on it) and ran `leg-end` at 13:22:26; the listener ticked at 13:23:01 and a leg took the lock at 13:23:07. That leg's step 0 read Fleet Ready empty, `queue-status.py` 0 dispatchable on `main` at `cbdbe999`, no reply in the dream thread, and `crystal_ball` 2 minutes old. No refill source had changed since the previous leg's 13:18 sweep. It ended after step 0, posted no second dream, and added only this paragraph. Three of three observed post-dream relays now spawned an empty leg.

Possible fix, the owner's to choose: move the spawn predicate into a script the listener runs and obeys by exit code (count and marker age together), the same move `fleet-read.py` made for the message gate, so a prose gate cannot be skipped on one path and honoured on another.

## Done when

- [ ] A leg's death with a zero count and a `crystal_ball` under six hours old spawns nothing, on a completion wake as well as a cron tick.
- [ ] Either the predicate is a script's exit code, or the pump section states the gate where it states the relay.
