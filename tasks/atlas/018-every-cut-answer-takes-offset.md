# 018 — Every lookup whose answer can be cut takes the `offset` its truncation line asks for

**State:** claimed by agent/atlas/018-every-cut-answer-takes-offset, 2026-10-29 16:45
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-atlas finding 5), verified by Opus against embarch-atlas@0cf93cec
**Scope:** atlas
**Hardware:** none — Query functions over fixture atlases, as `tests/test_query.py` already pages `doc_section`.
**Owner:** no

## What

`_cap` (`src/embarch_atlas/query.py:30-44`) cuts every lookup's answer at the tool's budget and ends it with "… truncated: call again with offset=N (next=N)". Only three lookups take that offset: `doc_section`, `net_trace` and `mismatch_report`. The other nine are `part_card`, `doc_toc`, `find_fact`, `register`, `pin_trace`, `config`, `dt_node`, `footprint` and `stacks`. They go through the same cut, but neither their `q` verbs (`query.py:785-799`) nor their MCP tools (`mcp_server.py:47-124`) accept an offset. An agent told to "call again with offset=N" has no way to do it, so it falls back to reading files by hand.

The cut is reachable in ordinary use. `doc_toc` of a reference manual of over a thousand pages has a 10,000-character budget. A `register` with many fields, enums, rules and firmware references has 6,000.

One possible direction: give each of the nine an `offset` on both doors and pass it through to `_cap`, the way `doc_section` does today. If a tool's answer truly cannot exceed its budget, the alternative is to make `_cap` never offer it a continuation.

## Why now

DESIGN.md "Query surface" (lines 266-267) says "Each answer starts with a `src:` line and is paged at a per-tool token budget with `next=<offset>`", and the `query.py` module docstring says the same. For nine of the twelve lookups, the page after the first cannot be fetched.

Several queued tasks change these same signatures: `tasks/atlas/012` (`part_card`'s `board`, `doc_toc`'s no-match answer), `003` (`config` and `dt_node` take a list and `vs=`, "capped at the tool budget with `next=`"), and `002` and `007` (new tools with `next=`). Landing the offset first gives each of them a working continuation to build on.

## Done when

- [ ] Every lookup that `_cap` can cut accepts `offset` on its MCP tool and its `embarch-atlas q` verb.
- [ ] For each of those lookups, a fixture answer larger than the budget, followed through `next=` until no truncation line remains, reproduces the uncut answer exactly once, with no line lost or repeated.
- [ ] A test fails if any tool's answer offers an offset that its MCP signature does not take.
- [ ] `atlas-use` SKILL.md says how to continue a cut answer, if it does not already.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `DESIGN.md` "Query surface" updated (embarch-atlas has no `spec.md`, so DESIGN.md is its contract). `changelog.d/` fragment dropped.
