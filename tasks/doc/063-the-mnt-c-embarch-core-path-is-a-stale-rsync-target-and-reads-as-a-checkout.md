# 063 — `/mnt/c/.../embarch-core` is a stale rsync deploy target, and it reads as a checkout

**State:** open
**Source:** `tasks/topology/045` (leg 116, 2026-09-16). That worker was verifying a cross-repo claim
in `embarch-topology/src/hardware/validate.rs` — that `embarch-core`'s `resolve_probe` delegates to
`select_probe` with *"no selection-rule copy remains in either crate"* (`embarch-core` decision 61).
It checked `/mnt/c/Users/tmp12/source/repos/embarch-core`, **found the pre-decision-61 hand-rolled
duplicate still there, and was about to report a real shape-8 defect.** It then re-checked the
canonical checkout at `/home/gabriel/Github/embarch/embarch-core` (`src/hardware.rs:92-99`), where
the delegation is real and the comment is true. The false alarm cost a chunk of that unit's run and
was caught by the worker's own second look, not by anything mechanical.
**Scope:** doc
**Hardware:** none — this is a documentation and/or tooling change about paths on this machine. No
board, no probe, no live Core, no deploy.
**Owner:** required

**Why `Owner: required`:** the natural home for the warning is
[`embarch-dev-workflow.md`](../../embarch-dev-workflow.md) §4a, which is a standing-rule document
reserved to the owner, and the alternative home is a check under `scripts/`, also reserved. A leg
may not write either. So this is filed where the owner can see it rather than fixed by an agent.

## What

A worker verifying a cross-repo claim about `embarch-core` has two paths it can reach for, and
**only one of them is a git checkout**:

| path | what it is | safe to verify against? |
|---|---|---|
| `/home/gabriel/Github/embarch/embarch-core` | the canonical git checkout | **yes** |
| `/mnt/c/Users/tmp12/source/repos/embarch-core` | an **rsync deploy target**, no `.git` | **no — arbitrarily stale** |

The second is where the live Windows-service Core is built from, so it is a real and necessary path
— it is simply not a source of truth about what `main` says today. It contains a full, plausible,
compiling Rust tree. Nothing about opening it says "this is a snapshot of an older commit."

## Why now

**This is the fleet's own version of the failure the reversals page calls shape 5, "a guess
indistinguishable from an answer."** A worker reading the stale tree gets a wrong answer that looks
exactly like a right one, and the specific wrong answer it gets is *"this comment states an invariant
the code does not implement"* — i.e. **it manufactures a defect of precisely the class the sweep was
hunting.** A zero-defect sweep is hard enough to trust; a sweep that reports a fabricated finding
from a stale tree is worse than one that reports nothing.

It is also directly cross-repo: `embarch-topology`, `embarch-api` and `embarch-ui` all make claims
about `embarch-core` behaviour in their own comments, and the citation sweeps running through the
queue are exactly the work that reaches for a sibling repo to check one.

## Options, for the owner to pick between

1. **One sentence in `embarch-dev-workflow.md` §4a** naming the `/mnt/c` path as a deploy target and
   not a checkout, with the canonical path beside it. Cheapest; relies on a worker having read it.
2. **A line in the worker agent definition** (`.claude/agents/embarch-worker.md`) telling a worker to
   verify cross-repo claims only against `/home/gabriel/Github/embarch/<repo>`. Reaches every worker
   without depending on what it chose to read.
3. **A `scripts/` check** that refuses, or warns, when a report cites a path under `/mnt/c` as
   evidence. Most robust, most work, and possibly more machinery than the problem needs.

`ask-before-building-prefer-lightweight` applies: option 1 or 2 is probably right and option 3 is
probably not, but the pick is the owner's.

## Done when

- [ ] A worker reaching for `embarch-core` to verify a cross-repo claim is told, by something it will
      actually read, which path is the checkout.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
