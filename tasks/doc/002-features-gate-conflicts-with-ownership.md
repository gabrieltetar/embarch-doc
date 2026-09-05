# 002 — A worker that adds a feature row cannot pass `check-docs.py`, because the two halves of the gate contradict each other

**State:** open
**Source:** umbrella/004 (2026-09-04) — the first worker to write a `features.d/` row under the assembled scheme, and it hit this on the first try
**Scope:** doc
**Hardware:** none
**Owner:** required

**Filed from `inbox/` by the supervisor, leg 009.** `Owner: required` is the
supervisor's classification, not the filer's: every candidate fix below writes
`scripts/`, `features.d/README.md` or `embarch-fleet/protocol.md`, all reserved
(`protocol.md` §3), so a worker sent at this fails on its first edit. It is filed here
rather than left in `inbox/` **so that it is visible in the queue** — `queue-status.py`
gates it out of dispatch, which is exactly the intent.

**Workaround in force meanwhile, and it works:** the supervisor runs
`python3 scripts/build_features.py` before `check-docs.py` when landing a unit and puts
`suite/features.md` in the fold's `--path` list. A worker must **not** commit that file
and should say in its report that it left it stale. Both umbrella/004 and the leg-009
supervisor did this and the fold was clean. Note `scripts/build_features.py` is mode
**644**, so it must be invoked as `python3 scripts/build_features.py`.

**A second, independent report of this same defect was filed and folded in here rather
than given its own number**: `ui/001`'s worker dropped
`inbox/doc-features-assembly-makes-every-worker-branch-red.md` two units later, having
hit it without knowing umbrella/004 had. Its one addition is the sharpest statement of
why this matters: *"a red that every unit of a certain shape produces is a red that
stops being read."* Its other detail worth keeping: it **assembled `suite/features.md`,
watched ownership reject it, and reverted** — so both workers independently reached the
same conclusion about which of the two reds to accept.

**Sibling: `tasks/doc/004`** — the same root cause with a different pair of scripts (the
compaction debt's path). Three worker-visible instances in leg 009 alone.

## What

`suite/features.md` is assembled from `features.d/`, and two gate checks now
disagree about who runs the assembler:

- `scripts/check-docs.py` runs `build_features.py --check`, which is **RED**
  whenever `suite/features.md` on disk does not match the fragments. Adding or
  editing any fragment makes it red until someone runs `build_features.py`.
- `scripts/check-ownership.py --scope <s>` **refuses** `suite/features.md` for
  every worker scope. Its own docstring says so: "notably not suite/features.md
  itself, which is assembled from those fragments and never hand-edited."

So a worker that ships a feature has exactly two moves and both fail a gate the
protocol requires of it (§10): commit the assembled file and fail the ownership
check, or don't and fail `check-docs.py`. umbrella/004 chose the second — a
boundary violation is worse than a mechanical red — and reported it, but the
next worker will hit it too and may well choose the other way.

Nothing has hit this before because commit `67a07dc` introduced `features.d/`
and assembled `suite/features.md` in the same commit, and no worker had written
a row since.

## Why now

This is the *first* real use of the mechanism `67a07dc` built, and the whole
point of that change was that "the row lands in the same commit as the work that
earned it" rather than depending on a supervisor honouring a request. As it
stands it still depends on the supervisor — but now silently, via a red gate the
worker is expected to explain away in prose. A red that every unit of a certain
shape produces is a red that stops being read.

Three shapes of fix, someone who owns `scripts/` should pick one:

1. **`build_features.py --check` learns a worker mode** — assert every fragment
   is well-formed and that `suite/features.md` differs from the fragments *only*
   by rows this branch touched, rather than requiring byte equality.
2. **`check-docs.py` assembles rather than checks** when it is not the
   supervisor, and the ownership check gains a narrow exemption for
   `suite/features.md` when the diff also contains a `features.d/<scope>-*`
   change. Cheap, but it puts a generated file in every worker's diff and
   reintroduces the merge collisions `features.d/` exists to remove.
3. **Drop `build_features.py --check` from `check-docs.py`** and make assembling
   part of the supervisor's fold, the way `build_changelog.py` already works —
   `changelog.d/` fragments do not make their gate red, because that check
   validates fragments rather than asserting the history file is up to date.
   This is the shape the rest of the repo already uses.

Whichever is chosen, `embarch-fleet/protocol.md` §10 should say it: it lists six
doc checks and does not mention `build_features.py --check` at all, so the
protocol and `check-docs.py` already disagree about what the gate *is*.

## Done when

- [ ] A worker that adds or edits one `features.d/<its own scope>-*` fragment,
      and nothing else outside its row, passes both `scripts/check-docs.py` and
      `scripts/check-ownership.py --scope <its scope>` on its own branch.
- [ ] `embarch-fleet/protocol.md` §10's list of doc checks matches what
      `check-docs.py` actually runs.
- [ ] `features.d/README.md` says who runs the assembler and when.
