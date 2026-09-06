# 007 — Decision 17's amendment says check 8 stopped maintaining a second scanner; it never did

**State:** claimed by agent/umbrella/007-doctor-target-count-shellout, 2026-09-05 22:50
**Source:** embarch-umbrella/002 (design-only decisions audit, 2026-09-03) — decision 17's amendment read against the source and found unbuilt
**Scope:** umbrella
**Hardware:** none

**Compacts:** ~~embarch-umbrella/spec.md~~ — **paid 2026-09-05 by `umbrella/006`**, which
compacted it 10,089 → 9,131 B (89.2%) as its own ride-along. Nothing is owed here: **write
your check-8 row and do not compact.** If your edit pushes `spec.md` back past 9,216 B you
are the one spending the reserve again, and the rule below applies to you afresh. Refresh
`009`'s counts either way if you change the table's shape.
**In flux:** yes — by this task, which is the point: `tasks/umbrella/009-compact-docs.md` is `blocked` on exactly
that, and a blocked compaction task parks the pass, not the reserve (`DOC-COMPACTION.md`
§2). You are the unit that rewrites a row of `spec.md`'s doctor table, so **compact both as part of this
commit**, honour `tasks/umbrella/009-compact-docs.md`'s `Must not delete:` list, and close only their item there.
**Headroom (stale, see above): `spec.md` 151 B of 10,240**, and it cannot be split — 10 KB is a role cap on a
single file (`DOC-COMPACTION.md` §2–3), so shortening is the only move. `open.md` was on
this line too and **is paid**: the owner's live-`doctor` pass took it 5,051 → 4,388 B while
adding what the run measured, which is this rule's first real use. `Must not delete:`, from
009: the doctor table's per-row **designed-and-unbuilt** distinction, which lives nowhere
else. Refresh 009's counts if you change the table's shape — a `Must not delete:` clause
that protects a table *by a count* is worse than useless once the count is stale.

---

## Dispatch note, leg 013 — the two blocks above contradict each other; this one wins

The `Compacts:` block says "nothing is owed here, do not compact" and the `In flux:`
block immediately below says "compact both as part of this commit". Both were written
against readings of `spec.md` that are now stale, in opposite directions. **Read neither
for its byte counts. Read this:**

`scripts/check-doc-size.py --pressure`, at dispatch:

- **`embarch-umbrella/spec.md` — 9,286 / 10,240 B, 954 B left (90.7%). In reserve.**
  It was paid on 2026-09-05 by `umbrella/006` and then `umbrella/011` put it straight
  back over the line. Filed against `tasks/umbrella/016-compact-umbrella.md`, `blocked`.
- **`embarch-umbrella/decisions/doctor.md` — no longer in reserve.** `umbrella/015`
  landed a few minutes before you started and took it **11,918 → 7,774 B** by a mission
  split: decisions 23 and 40 moved verbatim into a new `embarch-umbrella/decisions/mcp.md`.
  It has room now, but it is still not where your work goes, and `016`'s
  `decisions/doctor.md` item is **already closed** — do not re-close it.
- `embarch-umbrella/decisions/projects.md`, where decision 17 lives, is 9,752 / 12,288 B
  and under no pressure. That is where your decision-17 edit goes.

**So you owe a ride-along compaction of `spec.md`, inside this commit** — a blocked
compaction task parks the pass, not the reserve (`DOC-COMPACTION.md` §2). Get it back
under its 9,216 B reserve line, honour the `Must not delete:` clause in the `In flux:`
block *and* `tasks/umbrella/016`'s `spec.md` clause (the twenty-row doctor table and
which rows are designed-and-unbuilt), and say in your commit message that you closed
`016`'s `spec.md` item. `scripts/check-duplication.py embarch-umbrella` is **already
clean**, so there are no free bytes there — the room has to come from real shortening.

One more thing you should know before you choose: `spec.md`'s check-8 row currently
states the local-scanner behaviour *and* that decision 17's amendment asked for a
shell-out and it is unbuilt. **Whichever way you resolve this task, that row gets
shorter**, because it stops having to describe two states of the world.

## What

`embarch-umbrella` decision 17's amendment says the zephyr-west target-count
check "now shells out to `embarch-api`'s own listing instead of maintaining a
second scanner", on the argument that by the time check 8 runs there is no
bootstrapping problem — `init` has already run and a real config exists.

**Check 8 still calls this crate's own `zephyr::count_valid_targets`.** Its code
comment still records the deliberate approximation the amendment describes as
replaced: a revision counts as backed if *any* revision-suffixed file in the
board directory names it, which can overcount relative to `embarch-api`'s
per-tuple check. The crate's one mention of `list-targets` is a fix line telling
a human to run it.

Either build the shell-out, or retire the amendment paragraph and keep the
scanner with its overcount stated as intended behaviour. **Both are defensible**
— the amendment's own argument is sound, but the approximation only ever feeds a
pass/fail signal, and shelling out adds a subprocess to a check that currently
needs none.

## Why now

Everything else in decision 17 shipped and was verified as real cross-repo
interop, so this one paragraph is the only part of the entry that does not
describe the binary. The lightweight *shape* detection the amendment preserves is
genuinely still there, which is what makes the drift easy to miss.

## Done when

- [ ] Check 8's zephyr-west branch either shells out to `embarch-api`'s listing,
      or the amendment is retired per `DOC-CONVENTIONS.md` and the local scanner
      is documented as the intended answer.
- [ ] Decision 17's implementation note updated to match whichever was chosen.
- [ ] `status.d/` fragment for `suite/features.md`'s live-target-discovery row.
- [ ] Gate green; `changelog.d/` fragment dropped.
