# 071 — decision 42's "matching decision 35's own record" is true of check 11's shapes and false of check 8's

**State:** claimed by agent/umbrella/071-decision-42-cites-35, 2026-09-16 17:15
**Source:** `inbox/umbrella-decision-42-cites-decision-35-for-a-shape-35-never-records.md`, filed by
leg 119 while folding `umbrella/070`, drained by leg 120. Flagged independently by that unit's worker
(no bytes to fix it) and its reviewer (pre-existing, correctly out of its scope); the supervisor is
the only actor that saw both reports, which is why it exists as a task at all.
**Scope:** umbrella
**Hardware:** none — doc prose only. No board, no probe, no live Core, no `doctor` run.
**Owner:** no

## What

`embarch-umbrella/decisions/locate-api.md`#42 ends:

> **Neither check 8 nor check 11 has run inside a live `doctor` yet** — that needs a live Core and
> stays in `open.md`. The CLI shapes **both checks** assume were observed directly
> against both binaries on this bench [2026-09-06], matching `decision 35` (`schema-skew.md`)'s own
> record.

(The two markdown links in that sentence are rendered here as plain code spans; they resolve from
`decisions/locate-api.md`, not from this file. Leave them as links when you edit the decision.)

**Check 8 runs `list-targets`. Check 11 runs `versions`. Decision 35 is entirely about `versions`.**
Two mechanical facts, re-run at merge `d56c7a0`:

```
$ grep -nic 'list-targets\|list_targets' embarch-umbrella/decisions/schema-skew.md
0

$ grep -o '2026-09-0[0-9]' embarch-umbrella/decisions/schema-skew.md | sort -u
2026-09-04
2026-09-05
```

Zero mentions of `list-targets`, and no 2026-09-06 record at all. The sentence cites decision 35 as
corroboration for a pair of shapes of which it corroborates one, on a date it does not contain.

## Why now

This sentence is the tail of a defect that has consumed parts of four units. `umbrella/068` cut the
`list-targets` shape paragraph from decision 42 justified as "duplicates decision 35" — true of the
paragraph's `versions`/clap sentences, false of its `list-targets` sentence. `umbrella/070` restored
the cut claim into `projects.md`#17. **The restoration is done and correct. What survives is the
sentence that made the original cut look justified**, and it is now the only place a reader is told
to look in decision 35 for something that is not there.

## Where it goes

**Narrow the claim, do not expand it.** Attribute decision 35 for check 11's shapes only, and point
check 8's at `projects.md`#17 where the shape now lives. Done carefully this is roughly byte-neutral
and may save a few.

## Watch for

- **Decision 42 has 77 B of margin (4,019/4,096 B)** — the thinnest entry leg 118 produced, and the
  binding constraint on every option here. Report before/after bytes.
- **Do not restate the shapes in decision 42** to make the sentence true. That re-creates the
  duplication `umbrella/068` was right to remove, and there is no room for it.
- **Do not weaken the live claim in the same sentence.** *"Neither check 8 nor check 11 has run
  inside a live `doctor` yet"* is a standing hardware debt that three legs have explicitly checked
  survives. It must still be there, in those terms, when you are done.
- **Do not add a pin to `scripts/decision-size-baseline.json`** — `scripts/` is owner-reserved and
  pinning is the papering-over move.
- **The 2026-09-06 observation itself is not in dispute** — `projects.md`#17's restored paragraph and
  `suite/features.md`:149 both carry it. Only the attribution to decision 35 is wrong.
- **Sweep inbound citations case-insensitively** (`grep -rni`); see `tasks/doc/065`.
- **Reserve for `umbrella`:** `embarch-umbrella/decisions/bind.md` is at 11,533/12,288 B (755 B left,
  PARKED under `tasks/umbrella/009`, blocked). You are not editing that file; if your work pushes any
  `embarch-umbrella` doc into its last 10% and nothing has filed it, file
  `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit.

## Dispatch note (leg 121, 2026-09-16)

**Reserve re-checked by me at dispatch and unchanged:** `embarch-umbrella/decisions/bind.md`
11,533/12,288 B (755 B left), PARKED under `tasks/umbrella/009`, blocked. Nothing else in the scope
is in reserve. You are not editing `bind.md`.

**77 B of margin is the whole difficulty of this unit.** Work out the replacement sentence and
measure it before you write it. If the narrowed attribution does not fit, the correct move is to
*shorten* the sentence — dropping the corroboration clause entirely leaves a true sentence — not to
find bytes elsewhere in entry 42 by rewriting a claim you were not sent to touch.

**You may not write `history/umbrella.md`** — it is `build_changelog.py` output and outside §3's
allowed paths for a worker. If your fix leaves a line there needing a change, report it; do not edit
it. A sister unit burned a cycle on this exact edge two legs ago.

## Done when

- [ ] Decision 42 no longer cites decision 35 for a `list-targets` shape decision 35 does not record.
- [ ] The "neither check has run inside a live `doctor` yet" debt survives verbatim in force.
- [ ] Decision 42 is still at or under 4,096 B, with before/after bytes reported.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
