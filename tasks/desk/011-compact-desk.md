# 011 — `embarch-desk` decisions/agents.md is in reserve after decision 59's issue-read amendment

**State:** open
**Source:** `desk/007` amended decision 59 and crossed the reserve line; `DOC-COMPACTION.md` §2
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/decisions/agents.md
**Size debt due:** 2026-11-23
**In flux:** no — the agent-facing read tools (decisions 29, 59) were just worked and are settled.
**Must not delete:** decision 59's caps (2,000 / 500, chosen not measured), its "newest-first listing assumed, not measured" sentence, and its Rejected list.

## What

`decisions/agents.md` 11,455/12,288 B.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it; this is that filing.

## Done when

- [ ] The file is clear of its reserve line.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
