# 042 — `schema-skew.md` cites `embarch-api/decisions/surface.md` for a decision that has moved

**State:** open
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

- [ ] `embarch-umbrella/decisions/schema-skew.md` line 42's citation points at
      `embarch-api/decisions/tool-wrapping.md` (decision 52) instead.
- [ ] No other file under `embarch-umbrella/` cites a decision at a path that
      the `surface.md` split moved — `grep -rn 'embarch-api/decisions/surface'
      embarch-umbrella/` comes back with nothing.
