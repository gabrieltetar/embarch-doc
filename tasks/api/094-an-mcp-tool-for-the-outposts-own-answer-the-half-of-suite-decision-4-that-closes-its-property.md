# 094 — An MCP tool for the outpost's own answer: the half of suite decision 4 that closes its property

**State:** open
**Source:** `tasks/core/057`'s own "Sequencing" section, which named this follow-up and said
explicitly that it must **not** be filed until `core/057` landed, because a worker given it earlier
would be building against a route that did not exist. It landed 2026-09-13 (code `a131f63` in
`embarch-core`, doc `886a0bc` in `embarch-doc`), so it is filed now, in the same fold.
**Scope:** api
**Hardware:** none to build it. A live `embarch-core` is only needed to exercise it end to end, and
that is not required for this task — `embarch-api` has its own test surface and `core/057` shipped
a route with tests against a real firmware fixture.
**Owner:** no

## What

[Suite decision 4](../../suite/decisions.md) states the property this closes:

> An agent can obtain an outpost capture's **per-subject load shares and its coverage line**
> without re-implementing the timeline, and exactly one implementation of that timeline exists in
> the suite.

`core/057` built the first half — the computation, and `GET /study/{id}/stream/{name}/load` to
reach it (`embarch-core` decision 62, `decisions/streams.md`; documented in
`embarch-core/interfaces/studies.md` with its `400`/`404`/`422` cases). **Today an agent still
cannot ask for it**, because nothing in the MCP surface calls that route. Until that exists, the
decision's property is half-true: the computation is in one place, and the agent path to it is
missing.

Add the MCP tool, alongside the existing study-stream tools, and give it a CLI subcommand like
every other tool has.

## Why now

**This is the unit that makes suite decision 4 worth having.** The whole argument for moving the
computation into Core rather than leaving it in `embarch-ui` was that Core is on **both** paths —
the agent's, through `embarch-api`, and the human's, through the UI's Core client. Only one of
those two paths is built. The human already had an answer before any of this work started (the UI
renders it), so an agent reaching it is the entire new capability.

Note the sibling follow-up, deliberately ranked **below** this one: `tasks/ui/051`, retiring
`embarch-ui`'s own copy of the timeline arithmetic. The UI is correct today; the agent path does
not exist at all.

## Watch for

- **`list_study_streams` already describes `bytes_written: 0` as "a tap that was declared and
  produced nothing".** Whatever this tool returns for a capture with no usable rows should not
  collide with that wording — `tasks/suite/029` is open on exactly the ambiguity that phrasing
  creates.
- **The route can answer `422`** when the CSV's column list does not match the shared crate's
  header (`core/057` carried `embarch-ui` decision 10 (trace)'s check across deliberately). That
  refusal is load-bearing — reversals row 86 is why — so **relay it as a refusal, do not smooth it
  into an empty result.**
- **The MCP binary on this machine goes stale against a schema bump** and the running server keeps
  the old one. If this task changes any tool schema, say so in the changelog fragment; verifying it
  is the owner's, through the CLI, not an agent's through the live MCP server.

## Done when

- [ ] An MCP tool returns an outpost capture's per-subject load shares and coverage line for a
      study stream, by calling Core's route rather than computing anything.
- [ ] It has a CLI subcommand, like every other tool (`embarch-api` decision 40's own rule).
- [ ] `embarch-api/tools.md` documents it and the tool index count stays consistent.
- [ ] The `422` column-mismatch case reaches the caller as a refusal with its reason intact.
- [ ] A numbered `embarch-api` decision only if something was actually decided — wiring an
      existing route to an existing tool pattern decides nothing.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
