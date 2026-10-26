# 127 — Build every commit of a range in each configuration, and prove a rewrite kept the tree

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 74 per-commit build runs in 15 sessions through about 12 hand-written build scripts (`percommit.sh` written in 4 sessions); re-verification was 6.4 % of review-loop cost and 7.2 active hours; two "byte-identical" checks on 2026-10-07 were invalid because a worktree build used the main checkout's module
**Scope:** api
**Hardware:** toolchain
**Owner:** no

## What

Add `embarch-api build --each <base>..<tip>` and a matching MCP tool. For every commit in the range, it builds each named variant (the project-config variants of `api-build-returns-a-verdict-and-takes-named-variants`, which this builds on) and reports per commit and variant, as that draft's verdict object: pass/fail, warnings new against the previous commit, flash and RAM with the delta, and headroom left in the code partition. Each commit is built from **its own module sources**. That means a detached checkout of the module at that commit, made visible to west in place of the workspace's module. It must not be a `git worktree` outside the west workspace, because west then silently builds the main checkout's boards and drivers, which invalidated two field checks. `--same-tree-as <ref>` asserts that the tip's tree equals a reference ref, the check every fold in the field did by hand. It also asserts that the tip image differs from the reference ref's image only in the embedded commit id. Output is JSON plus a short table, with an option to stop at the first failure.

## Why now

After every fold the field sessions rebuilt each commit in two or three configurations to prove nothing in the middle of the stack broke. Each session wrote its own loop, and the most common one was rewritten four times. Re-verification is the third-largest review-loop step, after reviewer rounds and fixes.

## Done when

- [ ] `build --each` CLI and MCP tool, with the JSON result in `interfaces.md`.
- [ ] A fixture commit that changes only a board file builds with that change: the module comes from the commit, not from the workspace checkout.
- [ ] `--same-tree-as` passes on an identical tree and fails, naming the paths, on a differing one. The image comparison tolerates only the commit-id bytes.
- [ ] Per-commit flash/RAM deltas and partition headroom are reported for each variant.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
