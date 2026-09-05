# 011 — Decision 27's "which field, what limit" capacity error was never built

**State:** open
**Source:** [embarch-api/open.md](../../embarch-api/open.md) — "Decision 27's friendlier capacity error was never built. Oversized submissions *are* rejected before the HTTP call, but by `serde`'s raw error, not the 'which field, what limit' message described."
**Scope:** api
**Hardware:** none

## What

`embarch-api` decision 27 describes a capacity error that names the field that
overflowed and the limit it exceeded. The rejection itself works — an oversized
submission is caught before the HTTP call — but what the caller sees is `serde`'s
raw error, which says neither.

Build the message decision 27 describes, or retire the decision. Building it is the
cheaper and better answer here: the limits are already known at the rejection site,
and the whole value of rejecting early is telling the author what to change.

## Why now

Small, self-contained, and it is a decision recorded as settled while unbuilt —
`embarch-decision-reversals.md` shape 1, the most common failure in this suite.
Good filler for a slot; not urgent on its own.

## Done when

- [ ] An oversized submission is rejected with a message naming the field and the
      limit, covered by a test.
- [ ] Decision 27's implementation note updated to say it shipped (or the decision
      amended to say it was retired unbuilt, with the reason).
- [ ] The `embarch-api/open.md` bullet answered and removed.
- [ ] `changelog.d/` fragment dropped; `status.d/` fragment for anything suite-level
      made false.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
