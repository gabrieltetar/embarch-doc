# 068 — `check-decision-refs.py` reads a per-decision byte cap as a decision citation

**State:** open
**Source:** leg 122, 2026-09-16. Hit live: a supervisor-written task file
(`tasks/ui/058`) described a byte budget as a *per-decision* cap followed by the
number, and the claim commit `019181c` turned `check-decision-refs.py` red on `main`.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/`, which no agent may write.

## What

`scripts/check-decision-refs.py`'s citation pattern requires **no word boundary before
the word it keys on**, so a hyphenated compound ending in that word matches, and
whatever number follows is read as a decision number.

**Reproduce it** (do not paste the phrase into a tracked `.md`, or this task's own
gate fails the same way — which is the point):

```sh
printf 'the per-%s 4,096 B cap\n' decision > /tmp/refcheck.md
```

Run the checker over a doc containing that line. **It does not report 4096.** The comma
ends the number scan early, so the three digits *after* the thousands separator become
the number it thinks it found — a value no sub-project defines, so the check fails.
Note that the checker cannot even be told about this in prose: writing the misread
number next to the keyword in a tracked doc trips it a second time, which is why this
task describes the value instead of quoting it.

Adding a word boundary (or an explicit "not preceded by a word character or hyphen"
guard) before the keyword is the obvious shape of the fix. But the general form of a
citation is itself an open, owner-reserved question at `tasks/doc/055`, so the two are
better settled with each other in view than separately.

## Why now — the cost was not the red, it was who could clear it

The red landed on `main` in a **claim commit**, before any worker was dispatched.
Three workers (`study-designer/052`, `core/066`, `topology/046`) each hit it, each
correctly identified it as pre-existing and outside their own scope, and each carried
on. That is exactly what the ownership map asks for, and it means **a red introduced
by the supervisor sat on `main` for the whole dispatch window with nobody in a
position to clear it.** It cleared only incidentally, because the one worker whose
scope happened to contain the offending file reworded it in passing.

The false positive will recur: this suite writes byte-budget sentences constantly —
`DOC-BUDGET.md`, every compaction task, every dispatch note naming a reserve — and a
byte budget is exactly where the word appears as a hyphenated adjective next to a
number.

**Not this task, recorded here so it is not lost:** a supervisor's claim commit is a
commit like any other and should meet the doc gate before it is pushed. Nothing
currently requires that, and `.claude/leg.md` is owner-reserved.

## Done when

- [ ] A hyphenated compound ending in the keyword is no longer treated as a citation.
- [ ] A test or fixture covering the reproduction above, so the shape cannot come back.
- [ ] The comma-truncation behaviour checked too — a number scan that silently takes
      the digits after a thousands separator will misreport other things as well.
- [ ] Considered against `tasks/doc/055`'s open question about citation form generally,
      rather than fixed in isolation.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
