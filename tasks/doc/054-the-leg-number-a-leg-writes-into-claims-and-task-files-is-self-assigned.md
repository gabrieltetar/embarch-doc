# 054 — The leg number a leg writes into claims, task files and parked windows is self-assigned, and it has collided

**State:** open
**Source:** `inbox/doc-leg-number-is-self-assigned-and-collides.md`, dropped by the leg of
2026-09-13 16:20 while writing its own claim commits. Filed by the leg of 2026-09-13 17:0x.
**Scope:** doc
**Hardware:** none
**Owner:** required — every plausible fix lives under `scripts/`, in `.claude/leg.md`, or in
`../../../embarch-fleet/ops.md`, all of which [protocol.md](../../../embarch-fleet/protocol.md) §2/§3
reserve to the owner. No agent may run this, a supervisor included.

## What

Legs identify themselves by number in three places a later actor reads — claim commit subjects
(`claim umbrella/061 (leg 108 unit 2)`), task file `Source:` lines, and parked `suite`
announcements — and **nothing assigns that number**. There is no counter in
`embarch-fleet/scripts/`, nothing in `fleet.toml`, and no field in `supervisor-log.md`'s entry
shape. Each leg picks one by reading what a previous leg happened to write, and a leg starts cold.

Measured on `main` on 2026-09-13 over the last 40 task-touching commits: `leg 107` ×4, `leg 108`
×31, `leg 110` ×3, `leg 111` ×13 — not four legs in sequence. The leg that landed `core/052`,
`ui/047`, `api/085` and `umbrella/061` called itself **108**, while a leg two before it called
itself **111**, and `tasks/suite/038` carried **both** `108` (who announced it) and `110` (whose
sweep found it) in the same file.

## Why now

Nothing mechanical parses it, so nothing fails — the cost is entirely to the **handoff**. A `suite`
task parked with a live 30-minute window names the leg that announced it; a task file names the
leg whose sweep found it; a log entry says what "leg 108" decided. When two different legs are both
108, every one of those pointers resolves to the wrong predecessor, and the relay's whole premise
is that a successor reconstructs intent from what it reads.

## Options, cheapest first

1. **Drop the number, standardise on the timestamp.** The log heading's `<yyyy-mm-dd HH:MM>` is
   already stamped from the machine clock by `fold-commit.py` — the one field with a single writer,
   and already the key `fold-day.py` groups by. Costs a wording change in `.claude/leg.md`'s
   examples. The leg of 2026-09-13 16:20 already worked around the collision this way, writing
   `the leg of 2026-09-13 16:20` into its four task files.
2. **Give it a real counter** beside `.fleet/tick`, incremented at step 0 and printed by the script
   that already writes the tick. Cheap, but new fleet state with its own failure mode (a killed leg
   that incremented and did nothing).
3. **Leave it and accept the collisions**, and say so plainly in `.claude/leg.md` so a leg stops
   trying to be accurate about a decorative field.

## Done when

- [ ] One of the three is chosen and written down where a leg reads it.
- [ ] If the number stays, `.claude/leg.md` says how a leg is meant to derive it.
