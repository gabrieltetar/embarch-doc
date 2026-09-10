# umbrella — decisions/doctor.md's "Current truth" line still points at spec.md after the split

**State:** open
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

- [ ] `embarch-umbrella/decisions/doctor.md` line 7's "Current truth" pointer is repointed from
      `spec.md` at `interfaces/doctor-chain.md` (as a relative link from `decisions/`),
      matching the other five files that same commit updated.
