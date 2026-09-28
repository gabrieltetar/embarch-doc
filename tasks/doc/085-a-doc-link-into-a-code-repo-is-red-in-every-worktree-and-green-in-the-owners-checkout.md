# 085 — A doc link into a code repo is red in every worktree and green in the owner's checkout

**State:** open
**Source:** leg of 2026-09-28, step 0 — the baseline gate on a fresh leg worktree, before any unit.
**Scope:** doc
**Hardware:** none — one template line in `.claude/leg.md` step 0, or one rule in `check-links.py`.
**Owner:** required — both candidate fixes are in `.claude/` or `scripts/`, which
`check-ownership.py --supervisor` reserves to the owner.

## What

`embarch-ui/decisions/study-authoring.md:21` (owner commit `685b691c`, 2026-09-17) links
[`tests/element_ids.rs`] as `../../../embarch-ui/tests/element_ids.rs` — a relative link out of
`embarch-doc` into the `embarch-ui` **code** repo. From the owner's checkout that resolves to
`/home/gabriel/Github/embarch/embarch-ui/tests/element_ids.rs`, which exists, and `check-links.py`
is green. From any worktree under `.worktrees/embarch-doc/<name>/` it resolves to
`.worktrees/embarch-doc/embarch-ui/tests/element_ids.rs`, which does not, and `check-links.py` is
**RED** — on the leg's own worktree and on every worker's doc worktree, before anyone has written
a byte.

It is the same shape `.claude/leg.md` step 0 already solves for one repo: *"Every cross-repo link
in the instance resolves to `<worktree parent>/embarch-fleet`, which does not exist until you make
it."* The step links `embarch-fleet` beside the leg worktree and nothing else, because until
2026-09-17 no doc linked into a code repo.

**What this leg did about it:** `ln -sfnT /home/gabriel/Github/embarch/embarch-ui
/home/gabriel/Github/embarch/.worktrees/embarch-doc/embarch-ui` — beside the worktrees, exactly as
the `embarch-fleet` link is — after which `check-links.py` passes from the leg worktree. That link
persists in `.worktrees/embarch-doc/` for later legs, but nothing *says* to make it, so a fresh
machine or a cleaned `.worktrees/` is red again, and the next doc that links into `embarch-api` or
`embarch-core` is red with no link to fix it.

## Why now

A red that is structural to the worktree and invisible from the owner's checkout is exactly the
kind a supervisor learns to discount — and `.claude/leg.md` spends a paragraph on why a discounted
red check is the real cost (`check-ownership.py`, legs 008–010). This one would make every unit's
doc gate red until someone noticed it was not the unit's.

## Done when

- [ ] Either `.claude/leg.md` step 0 links every sibling repo beside the leg and worker doc
      worktrees (the `embarch-fleet` line, generalised), **or** `check-links.py` resolves a
      `../../../embarch-<repo>/` link against the suite root rather than the worktree's parent,
      **or** DOC-PROTOCOL/DOC-CONVENTIONS says a doc cites code by a code span rather than a
      relative link — whichever the owner prefers.
- [ ] `check-docs.py` is green from a fresh `.worktrees/embarch-doc/<name>/` with no hand-made link.
