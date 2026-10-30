# 096 — The listener spawned a leg into a dry queue two minutes after a dream

**State:** open
**Source:** the leg started 2026-10-29 18:03 (`leg-start` in `.fleet/tick.log`), which found itself spawned against the gate. The leg before it posted a dream at 18:01:16 (`ts` `1793318476.457199`, `crystal_ball` on it), logged its close at 18:02:23 and ran `leg-end` at 18:02:30. The listener ticked at 18:02:59 and a leg started at 18:03:04. At that moment `queue-status.py --no-supervisor --count` was 0 (`main` at `178affa2` since 18:01:56, `inbox/` empty) and the `crystal_ball` marker was under two minutes old.
**Scope:** doc
**Hardware:** none
**Owner:** required — the gate is prose in `.claude/commands/fleet.md`, generated from `embarch-fleet`'s template, both reserved.

## What

`fleet.md` STEP 2 says: count zero, spawn a leg **only if** `crystal_ball` is absent or older than six hours. Both conditions for refusing held, and the listener spawned anyway. The spawned leg did what the dream's handoff said (ended after step 0, filed nothing but this), so the cost was one leg's step 0. The cost if it repeats on every leg death is a chain of empty legs a few minutes apart until the owner answers the dream, with no watchdog alarm, because each of them ticks.

Not verified: why. The wake was a leg's completion notification rather than the cron, five seconds before the spawn. One reading consistent with that: the pump section ("a leg's death wakes this window and the next leg is spawned") states the relay without the gate, and a completion wake followed it rather than STEP 2. The previous dream (2026-10-28 22:32) was followed by ten cron ticks and no spawn, so the gate has held at least once.

Possible fix, the owner's to choose: move the spawn predicate into a script the listener runs and obeys by exit code (count and marker age together), the same move `fleet-read.py` made for the message gate, so a prose gate cannot be skipped on one path and honoured on another.

## Done when

- [ ] A leg's death with a zero count and a `crystal_ball` under six hours old spawns nothing, on a completion wake as well as a cron tick.
- [ ] Either the predicate is a script's exit code, or the pump section states the gate where it states the relay.
