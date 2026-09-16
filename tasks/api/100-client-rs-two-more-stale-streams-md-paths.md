# 100 — `client.rs` carries two more stale `decisions/streams.md` paths that `api/098` could not reach

**State:** open
**Source:** the `api/098` **reviewer**, leg 117, 2026-09-16, reviewing landed unit `api/098` (doc
`f78fe64`, no code commit). It confirmed `098`'s own fix was correct and complete *for the file
`098` was scoped to*, then went looking for the same defect elsewhere and found it twice in the code
repo. I verified both lines myself before filing.
**Scope:** api
**Hardware:** none — Rust doc-comments. No board, no probe, no live Core, no route called.
**Owner:** no

**Doc-size reserve for `api`:** `embarch-api/spec.md` 9,102/10,240 B, 1,138 B left, filed as
`tasks/api/083` and **blocked**. This task should not need to write it.

## What

`core/060` split `embarch-core/decisions/streams.md`: decisions 62 and 63 moved verbatim into a new
`embarch-core/decisions/stream-index.md`. `api/098` fixed the one stale mention in
`embarch-api/interfaces/studies.md`. **Two more are live in the code repo**, in
`crates/embarch-core-client/src/client.rs`:

```
 593:/// decision 62, `decisions/streams.md`) — field-for-field mirror of Core's
1724:    /// 62, `decisions/streams.md`) — an `OutpostTrace` tap's load
```

Both cite decision 62 with a file path that no longer holds it. Fix them the way `098` fixed its
one: **drop the file-path mention and keep the bare number**, per `DOC-CONVENTIONS.md`'s "Referring
to a decision" — verbatim, *"prefer the bare number"*, and the section's own stated reason is this
exact failure, a topic-file mention that goes on resolving after the decision moves. Do **not**
repoint them to `decisions/stream-index.md`; that just re-arms the same trap for the next split.

Check the repo label on each while you are there. Both are `embarch-api` files citing
`embarch-core`, so each needs the `` `embarch-core` `` label within
`scripts/check-decision-refs.py`'s **44-character** attribution window of its own `decision 62` —
a label further back in the sentence does not carry.

## Why now

**Because nothing can find these.** `check-decision-refs.py` walks `*.md` only and never reaches
Rust source, so no gate fails and no sweep script sees them. They surfaced because a reviewer went
one file further than its mandate required. `api/098` left them not by oversight but by scope: its
task named `interfaces/studies.md` and nothing else.

This is small, and it is the third `client.rs` citation item in two days (`api/097`, `api/099`,
this). **If a worker takes all three of `client.rs`'s outstanding citation defects in one pass it
should say so** — but `099` is a separate live task this leg and must not be duplicated.

## Done when

- [ ] `crates/embarch-core-client/src/client.rs` lines 593 and 1724 no longer name
      `decisions/streams.md`.
- [ ] Each surviving `decision 62` citation carries an `` `embarch-core` `` label inside the
      44-character window, or is already unambiguous and you say why.
- [ ] No other `decisions/streams.md` mention remains anywhere in `embarch-api` (doc repo or code
      repo) — grep both.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
