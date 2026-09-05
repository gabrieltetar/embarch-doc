# 011 — Decision 27's "which field, what limit" capacity error was never built

**State:** done
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

- [x] An oversized submission is rejected with a message naming the field and the
      limit, covered by a test.
- [x] Decision 27's implementation note updated to say it shipped (or the decision
      amended to say it was retired unbuilt, with the reason).
- [x] The `embarch-api/open.md` bullet answered and removed.
- [x] `changelog.d/` fragment dropped. **No `status.d/` fragment:** no suite-level doc
      states anything about this rejection, so nothing became false. `features.d/api-060`
      amended instead, since the caller-visible refusal changed.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Outcome

**Built, not retired.** `src/capacity.rs`: on a deserialize failure, the submitted
JSON is walked against a partial table of bounds and every field over one is named
with its count and its limit — the four lists by entry count, names by **byte**
length, since bytes are what `heapless::String<N>` bounds. It runs **only on the
error path**, after `serde` has already refused, so the table can be partial and a
wrong entry in it can only worsen a message, never reject a study `serde` would
accept. Both front-ends changed; `tools.rs` now deserializes from `&Value` so the
value survives the failure.

What the caller used to get, asserted in a test rather than remembered:
`sequence exceeds its bound at line 1 column 8785`.

**Decision 27 lives in `decisions/studies.md`, not `decisions/zephyr.md`** — the
reserve block's worry did not apply. `studies.md` was at 10,640/12,288 B and had
room; recording this cost 609 B and pushed it to 91.5%, into reserve, so it was
**added to `tasks/api/012-compact-api.md`** (`In flux: no`). Nothing was displaced
into a file it does not belong in. `spec.md`, the tight one, needed no change: the
new module is a row in `interfaces/modules.md`, which `spec.md` §5 already delegates
to. `open.md` fell to 89.2% when its bullet went, out of reserve, and that item in
012 is closed.
