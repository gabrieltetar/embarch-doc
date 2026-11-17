# 029 — A key from the opening prompt must name a real issue before the desk adopts it

**State:** open
**Source:** EMB-110, filed by an audit while relaying a burndown leg's report from the listener window
**Issue:** EMB-110
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

A desk session takes an issue key from its opening prompt or a handoff and
adopts it as its work item with `desk_set_work_item`. The guard against a string
that only looks like a key (a version tag, a part number, a ticket from another
tracker shaped like `ABC-123`) is written in four places — the desk skill
(`plugin/skills/desk/SKILL.md`), the MCP server instructions, and two tool
replies in `src/mcp.rs` ("a lookalike in prose is not one") — and enforced in
none. The tool posts to `/sessions/{id}/assign`, whose card is "found or
created", so an unknown key is adopted on the session's own reading.

Make the desk refuse it. The issue's direction, which you may improve on and
must say so if you do: the assign path resolves an `issue_key` against the
connected workspaces before it adopts it, and refuses one no connected workspace
has with a reply naming the key and the workspaces it tried. Decide what happens
when Linear cannot be reached at all (a refusal that blames the key would be
wrong; adopting it unchecked is the old behaviour) and state it in `spec.md`.
`item_id`, `new_title` and `untracked` are unchanged.

**Burndown leg: no new numbered decision.** Describe the behaviour in
`spec.md`/`interfaces.md`. If the unreachable-Linear case or anything else needs a
real design choice that would normally be a numbered decision, write it under a
`## Withheld decision` heading in this file and leave `decisions.md` alone; the
supervisor files it.

**What you may change.** Only `embarch-desk` and `embarch-doc/embarch-desk/`.

**Doc reserve.** Nothing of `embarch-desk`'s is in reserve; `interfaces.md` is
about 520 B from it (13,296 of 15,360 B, reserve from 13,824 B).

## Why now

The owner moved it to Fleet Ready; a wrong work item puts a session's time and
notes on someone else's issue.

## Done when

- [ ] Adopting a key that no connected workspace has is refused by the desk, not by the session's reading of the text.
- [ ] A test covers one real key and one key-shaped string that is not an issue, without a live Linear (a fake or a recorded reply).
- [ ] The skill text and tool replies say the desk now checks, rather than asking the session to.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `spec.md`/`interfaces.md` updated, `changelog.d/` fragment dropped.
