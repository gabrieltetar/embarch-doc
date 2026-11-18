# 036 — `embarch-desk/interfaces.md` is in reserve

**State:** blocked
**Source:** desk 035 (EMB-173) added `github_draft_review_replies` to `interfaces.md`, leaving it at 14,133 of 15,360 B (1,227 B left).
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/interfaces.md
**Size debt due:** 2026-12-01
**In flux:** yes. The agent-tool list grew in each of the last four desk units (restack, review threads, review replies, notes) and EMB-205 will add how the Desk tab shows the new draft kind; a split now would be restated within a unit or two.
**Unparks when:** EMB-205 (the Desk tab renders `github_replies` drafts) lands, or the next desk unit that writes `interfaces.md` runs out of its 1,227 B, whichever is first; the compaction rides in that unit.
**Must not delete:** the route and MCP tool lists and their decision/EMB citations; move the agent-tool list to a sibling file as `interfaces/cli.md` was split off, verbatim.

## What

Bring `interfaces.md` out of reserve by moving the MCP tool inventory (the plugin paragraph's tool list) into `interfaces/` verbatim, leaving a link and the index row current.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-desk/interfaces.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
