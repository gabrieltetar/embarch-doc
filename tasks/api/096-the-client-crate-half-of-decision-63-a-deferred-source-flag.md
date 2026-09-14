# 096 — The `embarch-api` half of decision 63: carry and describe the deferred-source flag

**State:** claimed by agent/api/096-deferred-source-flag-client-half, 2026-09-13 23:44
**Source:** `tasks/core/061`, split by leg 114 (2026-09-13). That task was written as one unit spanning
**two code repos** — `embarch-core` (where the flag is set) and `embarch-api` (the client crate that
deserializes it, and the tool description that explains it). A worker gets one task in one repo
(`../../embarch-fleet/protocol.md` §5), so it is two tasks. This is
the `embarch-api` half; `tasks/core/061` is the `embarch-core` half and is now narrowed to that repo.
**Scope:** api
**Hardware:** none — a struct field and two doc strings. No board, no probe, no live Core, no deploy.
**Owner:** no

## What

[`embarch-core` decision 63](../../embarch-core/decisions/streams.md) says a tap declared against a
source this bench has no front end for must say so in the stream index, as **a fourth
`#[serde(default)] Option<bool>` on `StudyStreamEntry`** beside `named`, `timed` and `self_excluded` —
**not** a third meaning for `note`. Two sites in this repo:

1. **`crates/embarch-core-client/src/client.rs`** — add the field to `StudyStreamEntry` (near
   `self_excluded`, line ~559), documented in the same voice as its three neighbours: what `Some(true)`
   means, what `Some(false)` means, and that `None` is a Core that predates the field.
2. **`src/tools.rs`** — `list_study_streams`' `#[tool(description = ...)]` gains one sentence
   distinguishing a deferred-source tap from a plain `bytes_written: 0`. The description already
   carries the sentence that creates the ambiguity (*"An entry with bytes_written 0 is a tap that was
   declared and produced nothing…"*); the new sentence sits with it. Check whether `streams_json` in
   the same file needs to surface the flag for a reader to act on that sentence — if it renders the
   other three booleans, it renders this one.

**The field name is pinned: `source_deferred`.** Leg 114 pinned it so this half and the `embarch-core`
half agree without one waiting on the other. Decision 63 deliberately left the name open ("name it for
the fact, not for power"), and the roadmap's own word for power sampling is *deferred, not cancelled*,
so the name carries the general fact rather than this one source. **Do not rename it** — the other half
is being written against this spelling in parallel.

## Watch for

- **This is not a wire-schema bump and no announcement is owed.**
  [`embarch-core` decision 50](../../embarch-core/decisions/enrollment.md) is the precedent in so many
  words, and [`embarch-api` decision 58](../../embarch-api/decisions/client-crate.md) is the crate-wide
  rule this field follows: every response field the client deserializes that Core may not yet send is
  `Option<T>` with `#[serde(default)]`. This is the fourth application of that pattern on this struct.
- **Do not branch on `note`** and do not change what it says. Decision 63's whole argument is that
  `note` stays prose.
- **Your repo is `embarch-api` only.** Do not edit `embarch-core`; the flag's *setting* is `core/061`.
  A test here pins that the field round-trips and that its absence deserializes as `None` — not what
  Core puts in it.
- **`embarch-api/spec.md` is in reserve** (9,102/10,240 B, 1,138 B left, `tasks/api/083` filed and
  `blocked`). Add no prose there if you can avoid it; if you must, say so in your report.
- **`tasks/api/095`** sweeps citations in this same `client.rs`. It is not being dispatched beside you.
  Leave its citation surface alone — a field addition is not a citation sweep.

## Done when

- [ ] `StudyStreamEntry` carries `source_deferred: Option<bool>` with `#[serde(default)]`, documented
      in the voice of its three neighbours.
- [ ] `list_study_streams`' description says how to tell a deferred-source tap from a tap that was
      declared correctly and captured nothing.
- [ ] A test pins that the field deserializes as `None` when Core omits it, and as `Some(true)` when
      Core sends it.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment.
