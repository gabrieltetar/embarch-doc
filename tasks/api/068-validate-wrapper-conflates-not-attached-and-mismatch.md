# 068 — `embarch-api`'s `validate` MCP tool and CLI both re-wrap `/validate`'s JSON under one `topology mismatch` lead, for both conditions

**State:** claimed
**Source:** `core/041`, 2026-09-11. Found while fixing the `embarch-core` half of the same defect
(`embarch-core` decision 59, `embarch-core/decisions/surfaces.md`).
**Scope:** api
**Hardware:** none — reachable by inspecting the wrapper's own formatting code and constructing
both `TopologyMismatch` shapes in a unit test, same as `core/041` did on the Core side.
**Owner:** no

## What

The MCP `validate` tool (used by `mcp__embarch-api__validate`) formats a human-readable string from
`POST /validate`'s JSON body, in `src/tools.rs` (`validate`, the `TopologyMismatchError` downcast
arm around line 979) and again, separately, in `src/cli.rs` (line 828, same literal format string)
— **two call sites, not one**, so a fix needs to land in both or the CLI keeps the old behaviour
after the MCP tool is fixed. The text a live incident actually produced was:

```
topology mismatch for role 'dev-bench' (probe 001057729826, chip 'nRF54L15'): probe '001057729826'
enrolled as role 'dev-bench' is not currently attached (recorded hardware_id 6fcddc36cb781b71,
live None) — fix it at http://127.0.0.1:4890/#topology
```

This is the wrapper's own lead ("topology mismatch for role '...' (probe ..., chip ...):"), not
`/validate`'s own JSON `reason` field, which never said "topology mismatch" as its first two words
— so the conflation this whole finding is about was introduced again, one layer up, after
`embarch-core` was fixed to distinguish the two conditions.

## Why now

`embarch-core` decision 59 (this task's own fix) added a `kind: "not_attached" | "mismatch"` field
to `/validate`'s `409`/`503` JSON body specifically so a caller could branch on a field rather than
on `reason`'s wording, and dropped `fix_it_url` (now `null`) on the `not_attached` arm. If
`embarch-api`'s wrapper still builds its lead from `reason`/`recorded_hardware_id`/`live_hardware_id`
without reading the new `kind` field, it will keep printing "topology mismatch" for a merely
unplugged probe — the exact defect `core/041` exists to fix, now one hop further from where a human
or an automated reader (the fleet's own `.claude/leg.md`, which routes on exactly this distinction)
actually sees it.

`/validate` now also answers `503` (not `409`) when `kind` is `"not_attached"` — worth checking
whether the wrapper's own status-code handling assumes `409` is the only non-`200` shape.

## Done when

- [ ] The wrapper's formatted string leads with a phrase distinguishable between `kind:
      "not_attached"` and `kind: "mismatch"`, branching on `kind`, not on `reason`'s wording.
- [ ] The wrapper does not offer `fix_it_url` (the Topology tab) for the `not_attached` case.
- [ ] The wrapper handles `503` the same way it already handles `409` (both are "the caller can act
      on this, not a Core failure").
- [ ] A test constructing both response shapes and asserting the two leads differ.
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
