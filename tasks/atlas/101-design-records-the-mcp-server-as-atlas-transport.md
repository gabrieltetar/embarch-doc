# 101 — The atlas design doc records its own MCP server as the transport it chose

**State:** claimed by agent/atlas/101-design-records-the-mcp-server-as-atlas-transport, 2026-11-23 15:01
**Source:** embarch-atlas/design.md — "Transport is unresolved: reachable over `embarch-api`'s existing MCP surface, or its own server."
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-atlas/design.md` still lists, under "Open questions,
recorded before resuming", that the atlas's transport is unresolved between a
tool on `embarch-api`'s MCP surface and a server of its own, followed by a
2026-08-25 status paragraph saying the question was left for whoever resumes the
work and naming the fact that would decide it: whether the analysis engine is
heavy enough that `embarch-api` should not link it. The work resumed and the
answer is built: `embarch-atlas mcp` is a stdio MCP server of its own
(`src/embarch_atlas/mcp_server.py`, the `mcp` extra in `pyproject.toml`),
registered per project in `.mcp.json`, and the same doc's later sections already
speak of "the atlas MCP server". When this is done the design doc states the
transport as settled (its own MCP server, as built), says what settled it, and
no longer carries the question or the status paragraph as open; the code repo's
`DESIGN.md` agrees with it.

## Why now

A refill sweep found the open question contradicted by shipped code, the case
`DOC-PROTOCOL.md` §4's "Open questions" check names: a resolved open question
has no mechanical signature, so only a read catches it. A reader
taking the open-questions section at its word would re-open a choice that has
been made, which is what the 2026-08-25 paragraph was written to prevent. Filed
by the supervisor from that sweep; no Linear issue.

## Constraints

- **Record what was built and what decided it; do not invent the reasoning.**
  Read `DESIGN.md` and the code for what they say about why the atlas runs its
  own server. Where neither says why, state the fact that is checkable from the
  repo (for example, what the engine is written in against what `embarch-api` is
  written in) and say plainly that the doc records the outcome, not a
  deliberation that is not written anywhere.
- **Keep what is still open.** If any part of the old paragraph is still a real
  open question (the C#/WPF GUI's debug-facing mode it mentions, a second
  process for a client to register), keep that part as an open question, in
  fewer words.
- `embarch.md` §2's "MCP is a plausible transport, not the defining shape" and
  its sub-project row are the supervisor's. If this change makes either false,
  drop a `status.d/` fragment saying which sentence and what is now true; do not
  edit them.
- `embarch-atlas/design.md` is 22,488 B and not in reserve. Write the settled
  statement shorter than the paragraph it replaces.

## Where

- `embarch-doc/embarch-atlas/design.md`, the "Open questions" section and its
  status paragraph.
- `embarch-atlas/DESIGN.md`, only if it says something about the transport that
  disagrees.

## Done when

- [ ] `embarch-atlas/design.md` states the transport as the atlas's own MCP
      server, with what settled it, and no longer lists it as unresolved.
- [ ] Anything still genuinely open from the old paragraph is kept as an open
      question, and nothing else is.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped; `status.d/` fragment for anything
      suite-level it made false.
