# 005 — A worktree needs every sibling in the dependency *closure*, not just the ones its own Cargo.toml names

**State:** open

**Source:** hit at the first `cargo build` of `tasks/ui/001-trace-view-server-side-binning`.
**Scope:** doc
**Hardware:** none
**Owner:** required

**Filed from `inbox/` by the supervisor, leg 009.** `Owner: required` — the setup step
lives in `embarch-fleet/`'s `supervise.md` and `.claude/`, both reserved
(`protocol.md` §3).

**It happened twice in one leg, not once, which is why the title is generalised.**
`embarch-ui` and `embarch-api` both failed their very first `cargo build` for the same
reason: the supervisor linked only the siblings each crate's *own* `Cargo.toml` names,
and `embarch-core-client` path-depends on `embarch-topology` transitively. Both workers
diagnosed it, created the symlink themselves, and left it in place. **The rule
`supervise.md` states is "symlink each sibling the crate names"; the rule that actually
works is "symlink every sibling in the dependency closure"** — or, more simply, resolve
it from `cargo metadata` rather than by reading one manifest.

> **This is almost certainly the owner's, not a worker's.** The fix is in the
> fleet's own setup step (protocol §6 step 2, `embarch-fleet/`), which is
> outside every worker's *and* every supervisor's ownership row. Filed here
> rather than left in a report so it is not lost; **relay it rather than
> dispatching it**, unless the setup step turns out to live somewhere the fleet
> may write.

## What

A `ui` worker is dispatched with `../embarch-study-designer` and
`../embarch-api` symlinked beside its code worktree. That is not enough:
`embarch-api/crates/embarch-core-client` path-depends on `embarch-topology`, so
`cargo build` fails before compiling anything with

    failed to read .../.worktrees/embarch-ui/embarch-topology/Cargo.toml

`ui/001` worked around it by adding
`.worktrees/embarch-ui/embarch-topology -> embarch/embarch-topology` by hand.
**That symlink is left in place**, because the branch does not build without it
and the supervisor re-runs the gate in the same worktree.

Worth checking whether the same transitive gap exists for the other consumers of
`embarch-core-client` before assuming this is `ui`-only.

## Why now

It is the first thing a `ui` worker hits, before it has read anything, and the
error names a path inside the fleet's own scratch directory — which reads like a
broken worktree rather than a missing dependency link. A worker that took it at
face value would report its task as blocked on infrastructure.

## Done when

- [ ] Whatever creates a worker's worktrees links every path-dep the crate needs
      transitively, not only its direct ones.
- [ ] Verified by a clean `cargo build` in a freshly created `ui` worktree with
      no hand-added links.
