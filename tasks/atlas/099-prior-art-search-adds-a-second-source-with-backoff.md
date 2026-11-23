# 099 — A prior-art search adds Google Patents as a second source, with backoff

**State:** blocked
**Unparks when:** tasks/atlas/097
**Source:** Fleet Ready issue: a hand-rolled Google Patents query answered HTTP 503 for every request after about ten
**Issue:** EMB-136
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The issue's author got good structured hits, family status included, from
Google Patents' JSON query endpoint, until every request (search and document
page alike) answered HTTP 503 after about ten queries. When this is done the
`atlas/097` search can take Google Patents as a second source, merged into the
same hit table with each hit marked by its source, and a 503 or 429 is retried
with backoff and then **reported** in the output and the exit status, never
dropped so that a partial table reads as a complete one.

## Constraints

- `atlas/097`'s constraints hold here unchanged: bounded live requests with
  generic terms, the source's terms for automated access read and recorded
  first, no network in tests.
- **If Google's terms forbid automated queries of that endpoint, do not wrap
  it.** Write that in this file, name the official alternative if there is
  one, and close the task `blocked` with `**Unparks when:**` the owner's word.
  The issue's third box is then answered by that record, not by code.
- The retry schedule is bounded and stated; a search never blocks for minutes
  on one source.

## Where

- The module `atlas/097` created.
- `embarch-atlas/DESIGN.md` and `embarch-doc/embarch-atlas/design.md`.

## Done when

- [ ] A Google Patents 503 is retried with backoff and reported, not silently
      dropped, or this file records why the source is not wrapped.
- [ ] Hits from two sources merge into one table with each hit's source.
- [ ] Tests cover the merge and the retry-then-report path from recorded
      responses, with no network.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `DESIGN.md` and `embarch-doc/embarch-atlas/design.md` updated,
      `changelog.d/` fragment dropped, `status.d/` fragment for anything
      suite-level it made false.
