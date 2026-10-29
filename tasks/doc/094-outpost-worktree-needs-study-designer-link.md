# 094 — `.claude/leg.md`'s sibling table omits `embarch-study-designer` for an `embarch-outpost` worktree

**State:** open
**Source:** supervisor leg started 2026-10-29 14:24, `outpost/018`'s fold (log entry `2026-10-29 14:42 — outpost/018`); filed from an inbox drop at the leg started 2026-10-29 15:03
**Scope:** doc
**Hardware:** none
**Owner:** required

## What

`.claude/leg.md`'s "link every sibling in the dependency closure" table (generated from `embarch-fleet/scripts/install.py`'s template) gives the `embarch-outpost` row `embarch-core`, `embarch-ui` only. `embarch-outpost/tests/vocab_check.py` also reads `../embarch-study-designer/src/outpost.rs`, and without that link it prints `SKIP: embarch-study-designer not checked out beside this repo` and exits 0 — a gate that reads green while comparing two of its three sources. Add `embarch-study-designer` to the row, with `vocab_check.py` as the reader. `check-dispatch.py --created` reads Cargo only, so it cannot catch this one.

## Why now

The leg that landed `outpost/018` made the link by hand and re-ran it green; every future outpost worktree built from the table will skip the check again.

## Done when

- [ ] The `embarch-outpost` row names `embarch-study-designer` and why.
- [ ] `install.py --check` green after the template change.
