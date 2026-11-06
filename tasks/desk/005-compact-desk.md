# 005 — `embarch-desk/spec.md` is in reserve

**State:** claimed by agent/desk/005-compact-desk, 2026-11-06 12:51
**Source:** decision 68 (Linear through its MCP server) added the callback's bearer exception and the sign-in to §3 and §5, leaving spec.md at 9,110 B of 10,240 B (89.0%); `DOC-COMPACTION.md` §2
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/spec.md
**Size debt due:** 2026-11-28
**In flux:** no — the status paragraph's per-decision deploy history (59–68) is the cut, and history belongs in `changelog.d/`; 68's open items live in `open.md`, not here.
**Must not delete:** §2's invariants, each with its decision number; §4's measured figures with their dates (`claude -p` $0.0007 vs $0.20, 8.2 MB / 20 ms of notes, the reference index's 178 issues / 48 PRs / 2 ms / 1.9 s); §5's bearer and OAuth exceptions for `/oauth/linear/callback` (68).

## What

`spec.md` has 1,130 B of headroom. Compact it, most likely by folding the status paragraph's deploy history into one line of what is deployed.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; decision 68 is the change that spent it.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` no longer lists `spec.md`.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
