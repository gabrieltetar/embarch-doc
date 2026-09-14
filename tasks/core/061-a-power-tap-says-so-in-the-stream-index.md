# 061 — Implement decision 63: a `PowerFrontEnd` tap says so in the stream index

**State:** open
**Source:** `suite/029` (leg 113, 2026-09-13), which chose the shape and recorded it as
[`embarch-core` decision 63](../../embarch-core/decisions/streams.md). This task is that decision's
implementation and nothing else — **the design question is settled; do not reopen it.**
**Scope:** core
**Hardware:** none to build or test it. Confirming the end state against a real study needs the
dev-bench board, and that is not this task's business — say so in your report as a debt.
**Owner:** no

## What

A study may declare a `StreamSource::PowerFrontEnd` tap. `embarch-dev-bench` accepts it, parses it and
captures nothing, because its decision 24 defers the front end. Today the only evidence is
`bytes_written: 0`, which `list_study_streams`' own description defines as *"a tap that was declared
and produced nothing"* — an authoring outcome. Asking for hardware that does not exist is currently
indistinguishable from mis-naming a signal.

Decision 63's shape, in three parts:

1. **`embarch-api/crates/embarch-core-client/src/client.rs`** — add a fourth
   `#[serde(default)] pub <name>: Option<bool>` to `StudyStreamEntry`, beside `named`, `timed` and
   `self_excluded`, documented in the same voice: what `Some(false)` means, and that `None` is a Core
   that predates the field. Name it for the fact, not for power — a second deferred source later must
   fit the same field.
2. **`embarch-core`** — set it where the stream index entry is built, from the tap's declared
   `StreamSource`, and set `note` with the prose for a person. **Cite `embarch-dev-bench` decision 24
   at that site**: Core *states* this fact, it does not measure it, and decision 63 says so explicitly.
3. **`embarch-api/src/tools.rs`** — `list_study_streams`' `#[tool(description = ...)]` gains a sentence
   distinguishing this from a plain `bytes_written: 0`. The description already contains the sentence
   that creates the ambiguity (*"An entry with bytes_written 0 is a tap that was declared and produced
   nothing…"*); the new sentence sits with it, and `streams_json` in the same file is what surfaces the
   flag.

## Watch for

- **This is NOT a wire-schema bump, and that is already settled by two numbered decisions rather than
  by this task's judgement.** [`embarch-core` decision 50](../../embarch-core/decisions/enrollment.md)
  is the precedent in so many words — `POST /validate`'s body adding `validated_at_utc_ms` is
  *"additive, not a wire-schema bump"* — and
  [`embarch-api` decision 58](../../embarch-api/decisions/client-crate.md) states the crate-wide rule
  this field follows: every response field the client deserializes that Core may not yet send is
  `Option<T>` with `#[serde(default)]`. This is the fourth application of that pattern on this struct,
  after `named`, `timed` and `self_excluded`. **No `ops.md` §4 announcement is owed.** (Leg 113's
  supervisor flagged this as its one uncertainty; the reviewer found both decisions and resolved it.)
- **Do not refuse the tap and do not touch study submit.** Decision 63 fences this explicitly: the
  roadmap calls power sampling *deferred, not cancelled*, and a study file written today against a tap
  the firmware will support later is not a mistake to reject. Acceptance stays.
- **Do not implement power capture.** Nothing here changes what any tap captures.
- **`embarch-core/decisions/streams.md` is in reserve** (11,219 B, 160 B inside the floor) and
  `tasks/core/060` is filed against it, `open`, not blocked. Decision 63's entry is already written —
  you should be adding no doc prose there at all. If you must, take the bytes from 060's budget and say
  so in that task.
- **`suite/features.md`'s power-sampling row** (`features.d/dev-bench-125-power-sampling-deferred.md`)
  says power sampling is accepted, parsed and captures nothing. That stays true. Update it only if your
  change alters what a reader would conclude from it — and the fragment is yours, the assembled file is
  the supervisor's.
- **The outstanding native Windows build.** `core/015`'s debt carries ten-plus landed `embarch-core`
  changes; this adds another and it is the first in a while that is **behavioural**. Say so in your
  report and do not attempt a Windows build.

## Done when

- [ ] A study declaring a `PowerFrontEnd` tap produces evidence in `GET /study/{id}/streams`
      distinguishable from a tap that was declared correctly and captured nothing.
- [ ] `list_study_streams`' tool description says how to tell the two apart.
- [ ] A test pins the distinction — a power tap and a genuinely-empty tap of another source do not
      produce the same entry.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment per repo touched.
