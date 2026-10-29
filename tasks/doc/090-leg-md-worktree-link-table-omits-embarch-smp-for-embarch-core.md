# 090 — `.claude/leg.md`'s worktree link table omits `embarch-smp` for `embarch-core`

**State:** done — already fixed by `tasks/doc/037`'s table pass (fleet `039bd66`, owner/dispatch): the `embarch-core` row lists `embarch-smp`, and the count sentence says six
**Source:** `core/096`'s worker, 2026-10-25: a fresh `embarch-core` worktree failed `cargo build` until the worker symlinked `embarch-smp` into the worktree's parent itself.
**Scope:** doc
**Hardware:** none
**Owner:** required — the table is in `.claude/leg.md`, rendered from `embarch-fleet/templates/`, both owner-reserved.

## What

`.claude/leg.md`'s "link every sibling in the dependency closure" table lists `embarch-study-designer`
and `embarch-topology` for an `embarch-core` worktree. Since the bootload work (2026-09-30),
`embarch-core/Cargo.toml` also path-depends on `../embarch-smp` (lines 44 and 121, the second with
the `sim` feature), so a worktree created by the table alone fails its first build on a path inside
`.worktrees/`. The leg's own grep (`grep -rn 'path *= *"\.\.' --include=Cargo.toml`) finds it; the
table does not. No other suite crate path-depends on `embarch-smp` today (`embarch-api`,
`embarch-ui`, `embarch-umbrella` checked 2026-10-25).

When done, the table's `embarch-core` row names `embarch-smp`, and the "only three repos are ever a
link target" sentence is corrected to four.

## Why now

It is `tasks/doc/037`'s shape a second time (a table row that drifted from the manifests), and it
cost a worker a diagnosis and a self-made symlink. The 2026-10-25 leg left
`/home/gabriel/Github/embarch/.worktrees/embarch-core/embarch-smp` in place, so the next `core`
worktree builds anyway; the table is still wrong.

## Done when

- [x] The `embarch-core` row lists `embarch-smp`; the count sentence matches the table. It says
      six, not four: the same pass found `outpost` and `dev-bench` read siblings too.
