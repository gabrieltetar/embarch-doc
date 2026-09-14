# 061 — Implement decision 63: a `PowerFrontEnd` tap says so in the stream index

**State:** claimed by agent/core/061-power-tap-says-so-in-stream-index, 2026-09-13 23:43
**Source:** `suite/029` (leg 113, 2026-09-13), which chose the shape and recorded it as
[`embarch-core` decision 63](../../embarch-core/decisions/streams.md). This task is that decision's
implementation and nothing else — **the design question is settled; do not reopen it.**
**Narrowed to one repo by leg 114 (2026-09-13).** As filed it spanned `embarch-core` **and**
`embarch-api`, which no single worker may do (`../../embarch-fleet/protocol.md` §5:
one task, one repo, one branch). The `embarch-api` half — the `StudyStreamEntry` field in
`crates/embarch-core-client/src/client.rs` and the `list_study_streams` description in `src/tools.rs` —
is now **`tasks/api/096`**, running in parallel with this one. **This task is `embarch-core` only.**
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

Decision 63's shape. **Your part is the one in `embarch-core`; the other two are `tasks/api/096` and
are listed here only so you can see the whole:**

1. *(`api/096`, not you)* `embarch-api/crates/embarch-core-client/src/client.rs` — the fourth
   `#[serde(default)] Option<bool>` on the client crate's own `StudyStreamEntry`.
2. **`embarch-core` — yours.** Add the fourth `#[serde(default)] pub source_deferred: Option<bool>` to
   the stream-index entry this repo serves (`src/stream_store.rs` ~line 231 and the response struct in
   `src/study.rs` ~2923 both carry `self_excluded`; follow it exactly), **set it where the entry is
   built** from the tap's declared `StreamSource`, and set `note` with the prose for a person.
   **Cite `embarch-dev-bench` decision 24 at that site**: Core *states* this fact, it does not measure
   it, and decision 63 says so explicitly.
3. *(`api/096`, not you)* `embarch-api/src/tools.rs` — the `list_study_streams` description sentence.

**The field name is pinned: `source_deferred`.** Leg 114 pinned it rather than leaving it to whichever
half ran first, because `api/096` is being written against this spelling in parallel. Decision 63 left
the name open ("name it for the fact, not for power"); the roadmap's own word for power sampling is
*deferred, not cancelled*, so the name carries the general fact and a second deferred source later
fits the same field. **Do not rename it.**

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
- **Your repo is `embarch-core` only.** Do not edit `embarch-api` — not the client crate, not
  `tools.rs`. `api/096` is running in parallel and a second worker is in that repo.
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
- [ ] A test pins the distinction — a power tap and a genuinely-empty tap of another source do not
      produce the same entry.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment.
- *(`list_study_streams`' description is `api/096`'s box, not yours.)*
