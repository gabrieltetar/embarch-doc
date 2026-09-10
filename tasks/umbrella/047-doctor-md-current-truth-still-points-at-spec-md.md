# umbrella — decisions/doctor.md's "Current truth" line still points at spec.md after the split

**State:** done — leg 068, `agent/umbrella/047-doctor-current-truth`. Filed
`tasks/umbrella/048-compact-umbrella.md` in the same commit: the fix's net growth
pushed `decisions/doctor.md` into the doc-size reserve (90.2%, 1,206 B left).

**Dispatch note, leg 068.** This is deliberately a one-line unit and it should stay one. Repoint
`decisions/doctor.md` line 7's `Current truth:` at `../interfaces/doctor-chain.md`, matching the
five siblings `umbrella/046` already updated. Do **not** re-word the surrounding sentence, do not
touch the other five files (they are already correct), and do not add a decision — nothing is being
decided here, a pointer is being corrected to match a move that already landed.

**Doc-size reserve in your scope, before you plan:** `embarch-umbrella/open.md` is 4,996/5,120 B
(**124 B left**, filed against blocked `tasks/umbrella/038`, due 2026-09-12) and
`embarch-umbrella/decisions/bind.md` is 11,447/12,288 B (841 B left, filed against blocked
`tasks/umbrella/009`). You should need neither. If your work spends a reserve — pushes a file into
it, or leaves one there that nothing has filed — file `tasks/umbrella/<NNN>-compact-umbrella.md` in
the same commit.
**Source:** review of umbrella/046 (embarch-doc merge `fc6f7386d20793e031931764f121b65c17c9c6d5`)
**Filed from `inbox/` by leg 067, 2026-09-10**, in the same fold as `umbrella/046`, the unit whose review produced it.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`umbrella/046` moved the eighteen-row `doctor` chain table out of `embarch-umbrella/spec.md`
into `embarch-umbrella/interfaces/doctor-chain.md`, and repointed the identical
"Index: .../ Current truth: ..." boilerplate line in five sibling decision files
(`bind.md`, `mcp.md`, `reporting.md`, `schema-skew.md`, `dev-bench-firmware.md`) from
`[../spec.md](../spec.md)` to `[../interfaces/doctor-chain.md](../interfaces/doctor-chain.md)`.

`embarch-umbrella/decisions/doctor.md` line 7 carries the same boilerplate —
`Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Four checks are their own groups: ...`
— and was **not** repointed, even though the same file's
line 5, one line above, was correctly edited in this same commit to say the table itself
is `[the table](../interfaces/doctor-chain.md)`'s job. `doctor.md` is specifically the
decisions file about the check chain (it names all four check groups by number in that same
sentence), so "Current truth: spec.md" is now the odd one out among the six files this unit
touched, and it is factually stale: `spec.md` no longer carries the check table, only a
three-line pointer to it.

This is not a broken link — `check-links.py` sees a resolvable target — so it is exactly the
class of miss the diff's own mechanical checks cannot catch, and it sits in a decisions file
this same commit edited on the very sentence above it.

## Why now

Caught during the required review of umbrella/046; cheap to fix while the context (which of
the six touched files got which line) is fresh.

## Done when

- [x] `embarch-umbrella/decisions/doctor.md` line 7's "Current truth" pointer is repointed from
      `spec.md` at `interfaces/doctor-chain.md` (as a relative link from `decisions/`),
      matching the other five files that same commit updated.
