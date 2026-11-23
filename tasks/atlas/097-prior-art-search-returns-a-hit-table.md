# 097 — A prior-art search returns one hit table

**State:** open
**Source:** Fleet Ready issue: agents running a patent prior-art scan rewrite throwaway scrapers against public patent databases every time
**Issue:** EMB-136
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

A session doing a technology or freedom-to-operate scan before a hardware
design choice today hand-writes `curl` and inline Python against public patent
databases, rediscovering each one's endpoints, query syntax and rate limits.
When this is done one atlas command (the issue suggests `prior-art search`)
takes keyword queries, optional CPC/IPC classes and optional applicant names,
and returns one table of hits — publication number, title, applicant, filing
and priority dates, family status where the source gives it, abstract — as
markdown and as JSON, from **DEPATISnet's** expert search at least (the source
the issue found usable without a rate limit).

It is a **standalone research verb outside the document pipeline**, the shape
`fetch-text` already has (owner decision 2026-11-18, EMB-208): nothing it
fetches is distilled or enters the library or an atlas, and no atlas is needed
to run it. The verb's name, its module, whether it is also an MCP tool, and the
JSON shape the follow-ups (`atlas/098` claims text, `atlas/099` a second
source) will extend are the worker's to decide and record in an atlas
decision.

What the issue's author learnt by hand, for the worker to verify rather than
trust: a POST to the expert search with `action=treffer`, then
`action=download_treffer_csv` on the same cookie jar for the hit list, and
`action=bibdat&docid=...` for an abstract; `ti=`, `ab=` and `ic=<class>` field
codes work, while a parenthesised `TI=(...)` and a multi-word `pa=` value
failed.

## Constraints

- **Live requests are allowed, bounded.** The owner moved this issue to the
  fleet, and it is about online sources, so the worker may query them — but at
  most about fifteen requests per source in this unit, at least two seconds
  apart, stopping a source at its first 429 or 503. Generic technology terms
  only in every query: no client, product, project or person name.
- **Read the source's published terms for automated access first**, and record
  what they say in the decision. A source whose terms forbid automated queries
  is not wrapped: write that in this file, name the source's official API (and
  what it needs, such as a key the owner would register), and close the task
  `blocked` with `**Unparks when:**` the owner's word.
- **Tests never touch the network.** Record a few trimmed responses from
  generic queries as fixtures; a live smoke test, if any, runs only when an
  environment variable asks for it.
- No new runtime dependency beyond the standard library without a line in the
  decision saying why.

## Where

- `embarch-atlas/src/embarch_atlas/`: a new module, and `cli.py`;
  `fetchtext.py` for the existing blocked-page and timeout handling to reuse.
- `embarch-atlas/DESIGN.md`: the command table, the network exception next to
  `fetch-text`, and a decision.
- `embarch-doc/embarch-atlas/design.md`.

## Done when

- [ ] One command returns a hit table for a keyword plus class query from
      DEPATISnet, with title, applicant, dates and abstract per hit, as
      markdown and JSON.
- [ ] The source's terms for automated access are recorded in the decision.
- [ ] Tests cover the parse from recorded responses and a blocked or
      rate-limited answer, with no network.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `DESIGN.md` and `embarch-doc/embarch-atlas/design.md` updated,
      `changelog.d/` fragment dropped, `features.d/` row if it is a new
      user-facing command, `status.d/` fragment for anything suite-level it
      made false.
