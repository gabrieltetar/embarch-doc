# 042 — `schema-skew.md` cites `embarch-api/decisions/surface.md` for a decision that has moved

**State:** closed (leg 048)
**Source:** worker on `agent/api/036-dev-bench-hello-tool`, 2026-09-07, filed as an
`inbox/` drop while splitting `embarch-api/decisions/surface.md`
(`tasks/api/043`'s parked reserve, closed via `DOC-COMPACTION.md` §2's
split-first rule). Held out of the queue by leg 045 on the grounds that the
citation was only stale once `api/036` landed; **`api/036` landed 2026-09-07
(doc `8005396`), so the premise now holds** and this is filed.
**Scope:** umbrella
**Hardware:** none

## What

`embarch-umbrella/decisions/schema-skew.md` line 42 cites
`([embarch-api](../../embarch-api/decisions/surface.md) 52)`. Decision 52 (the
`versions` subcommand) moved **verbatim** to the new
`embarch-api/decisions/tool-wrapping.md` — verified on `main` after `api/036`
landed: `tool-wrapping.md` line 31 carries `### 52 — The compiled host type
schema version is its own subcommand, not a field on status`, and `surface.md`
no longer mentions it. The number still resolves, because
`check-decision-refs.py` falls back to "defined somewhere in the sub-project"
when no exact `decisions.md`/`design.md`-shaped path is nearby — so nothing in
the gate will ever flag this. The specific path the line points at is wrong.

This is `embarch-umbrella`'s own file, out of `api`'s ownership row, which is
why the `api` worker that caused the move could not fix it.

## Why now

A reader who follows that link today lands on `surface.md` and does not find
decision 52 there. The link is the only thing in `schema-skew.md` explaining
*why* check 11 shells out to a different binary, so a reader who loses it loses
the reasoning, not just a reference.

## Also, and deliberately out of this task's scope

`history/api.md` line 11 has the **same stale path** for the same decision
(`embarch-api/decisions/surface.md 52`). That file is `api`'s, not
`umbrella`'s, so it is not this task's to fix — recorded here so the next actor
who touches it has the pointer rather than rediscovering it.

## Done when

- [x] `embarch-umbrella/decisions/schema-skew.md` line 42's citation points at
      `embarch-api/decisions/tool-wrapping.md` (decision 52) instead.
- [x] No other file under `embarch-umbrella/` cites a decision at a path that
      the `surface.md` split moved — `grep -rn 'embarch-api/decisions/surface'
      embarch-umbrella/` comes back with nothing.

## Closed

Widened the second grep per the leg-048 dispatch note: `grep -rn 'embarch-api/decisions/'
embarch-umbrella/` finds exactly one citation of an `embarch-api/decisions/` path anywhere in
`embarch-umbrella/` — the line 42 one just fixed. No other file cites `shape.md` (decision 61,
landed this leg per the note) or any other `embarch-api/decisions/*` path, so there was nothing
else to widen the fix to. This was a one-line docs-only unit; no code change, no `embarch-umbrella`
(code repo) commit. `history/api.md`'s matching stale path is left untouched, as the task and the
leg-048 note both direct — it is `api`'s file.

## Dispatch note — leg 048

**This task's premise is now doubly true, and one of its own notes is out of date.** It was held
back by leg 045 on the grounds that the citation only goes stale once `api/036` lands. `api/036`
landed 2026-09-07. **A second split has happened since**: `api/048` landed this leg
(`embarch-doc` `13b5bf6`) and added `embarch-api` decision **61** to
`embarch-api/decisions/shape.md`. So when you run the second Done-when grep, widen it: check every
`embarch-api/decisions/` path this repo cites, not only `surface.md`, and confirm each cited
decision number is actually in the file the path names. `check-decision-refs.py` will not catch a
wrong-but-plausible path — it falls back to "defined somewhere in the sub-project" — which is
precisely why this defect reached `main` with a green gate in the first place.

**Do not fix `history/api.md`.** The task body names it as carrying the same stale path and
correctly rules it out of scope: it is `api`'s file, not `umbrella`'s, and `check-ownership.py`
will refuse it. Leave it, and leave the note that says so.

**If the whole unit turns out to be one line, that is the correct result — say so and stop.** Do not
find adjacent work to justify the run. A citation that points a reader at a file where the reasoning
is not is worth a unit on its own, and `schema-skew.md`'s link is the only thing in that file
explaining why check 11 shells out to a different binary.

**Doc-size reserve for `umbrella`, so you plan rather than discover.** `spec.md` is
9,784 / 10,240 B (456 B left) and `open.md` is 4,494 / 5,120 (626 B), both filed under
`tasks/umbrella/038`. `decisions/bind.md` (11,409 / 12,288) is parked under `tasks/umbrella/009`,
`In flux: yes` — **do not compact it and do not write into it**. `decisions/schema-skew.md`, the
file you are editing, is not in reserve.

**Reserve rule you owe:** if your work pushes any `umbrella` file into reserve, or leaves one there
that nothing has filed, file `tasks/umbrella/<next free NNN>-compact-umbrella.md` in the same
commit.
