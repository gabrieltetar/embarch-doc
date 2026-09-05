# 011 — Decision 27's "which field, what limit" capacity error was never built

**State:** claimed by agent/api/011-capacity-error-message, 2026-09-05 12:52
**Source:** [embarch-api/open.md](../../embarch-api/open.md) — "Decision 27's friendlier capacity error was never built. Oversized submissions *are* rejected before the HTTP call, but by `serde`'s raw error, not the 'which field, what limit' message described."
**Scope:** api
**Hardware:** none

**Doc-size reserve (supervisor, 2026-09-05, refreshed after `api/010` landed):** four
`api` files are in the last 10% of their caps and **all four are already filed against
`tasks/api/012-compact-api.md`**, so you owe **no new compaction task** — but two of
them are now genuinely tight and you must plan around them rather than discover them:

- `decisions/zephyr.md` **99.2%, 96 B left** — this is where decision 27 lives if it
  lives anywhere near build orchestration. `api/010` could not fit a new entry here at
  all and had to file decision 53 in `decisions/shape.md` instead. **Do not assume you
  can add an entry to this file.**
- `spec.md` **98.7%, 135 B left** — tightest file in the suite.
- `open.md` 93.2%, 348 B left. `interfaces/config.md` 92.9%, 873 B left.

Replace text rather than appending it. **Say in your report if you had to put something
somewhere it does not belong because of a cap** — `api/010` did exactly that and saying
so is what made it visible.

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
