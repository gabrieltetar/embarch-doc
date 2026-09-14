# 061 — Implement decision 63: a `PowerFrontEnd` tap says so in the stream index

**State:** done
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

- [x] A study declaring a `PowerFrontEnd` tap produces evidence in `GET /study/{id}/streams`
      distinguishable from a tap that was declared correctly and captured nothing.
- [x] A test pins the distinction — a power tap and a genuinely-empty tap of another source do not
      produce the same entry.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment.
- *(`list_study_streams`' description is `api/096`'s box, not yours.)*

## Shipped

Added `pub source_deferred: Option<bool>` (fourth in the `named`/`timed`/`self_excluded`
pattern) to `embarch-core/src/stream_store.rs`'s `StreamIndexEntry` and to
`embarch-core/src/study.rs`'s `StreamIndexEntryResponse`, wired straight through in
`stream_index_response`. Set in `StreamStore::create` — before any byte arrives, same as every
other index field — from the tap's declared `StreamSource`: `Some(true)` only for
`StreamSource::PowerFrontEnd`, `None` for every other source. `note` is set alongside it with
prose citing `embarch-dev-bench` decision 24 (the front end is deferred, not built). No refusal,
no change to study submit, no capture behaviour touched — exactly decision 63's fence.

New test `stream_store::tests::a_power_tap_says_source_deferred_and_an_empty_tap_of_another_source_does_not`
pins the distinction the task asks for: a `PowerFrontEnd` tap and a `GattTranscript` tap, both with
`bytes_written: 0` at `create()` time, only the former carries `source_deferred: Some(true)` and a
note naming decision 24. Updated the existing literal `StreamIndexEntry`/`StreamIndexEntryResponse`
constructions in `study.rs`'s test module for the new field (no behavioural change to those tests).

Docs: `embarch-core/interfaces/studies.md`'s `GET /study/{id}/streams` response shape and
`embarch-core/interfaces/result-layout.md`'s `index.json` field list and boolean-field prose both
now name `source_deferred`, in the same body-edit these files already carried the other three
booleans in. No `decisions.md` prose added — decision 63's entry was already written and
`embarch-core/decisions/streams.md` is in reserve (`tasks/core/060`, open). No `ops.md`
announcement — this is additive per `embarch-core` decision 50 / `embarch-api` decision 58, not a
wire-schema bump. `suite/features.md`'s power-sampling row stays true as written; not touched.

**Debts, not gaps:**
- **Hardware-verification debt.** Nothing here was run against a real study or the dev-bench
  board — confirming a `PowerFrontEnd` tap actually reads `source_deferred: true` off a live
  `GET /study/{id}/streams` needs the dev-bench board and is out of this task's scope.
- **Adds to `core/015`'s outstanding native Windows build debt.** This is a behavioural change
  (a new response field, populated from tap-declared source) landing on top of that debt, the
  first behavioural addition to it in a while. Not built or tested on native Windows; per protocol
  §10 that build is unrunnable from a worktree and is the owner's to run from the main checkout.

## Gate

`cargo build`, `cargo test` (209 passed, 0 failed, 2 pre-existing ignored), and
`cargo clippy --all-targets -- -D warnings` all green in the code worktree.
`python3 scripts/check-docs.py` in the doc worktree: 10 of 11 checks green;
`check-links.py` is red, but identically red with this unit's changes stashed out — a
pre-existing artifact of this worktree's `embarch-fleet` stub (only `spec.md` present, no
`protocol.md`/`ops.md`), unrelated to this task. `check-client-names.py --repo <code worktree>`
and `check-ownership.py` (both `--scope core` in the doc worktree and `--code-repo --scope core`
in the code worktree) all green.

**Environment note, not part of this task's work:** both worktrees for this unit were found
nested *inside* their own repos' trees
(`embarch-core/.worktrees/embarch-core/061-power-tap-says-so-in-stream-index`,
`embarch-doc/.worktrees/embarch-doc/061-power-tap-says-so-in-stream-index`) rather than at
`embarch/.worktrees/<repo>/<NNN-slug>/` outside every repo tree, as `../../embarch-fleet/protocol.md`
§5 requires — the same class of problem `embarch-study-designer` decision 57 named. The
sibling path-dep symlinks for `embarch-core`'s build (`embarch-study-designer`,
`embarch-topology`) were only set up at the "outside" location
(`/home/gabriel/Github/embarch/.worktrees/embarch-core/`), not beside the actual nested worktree,
so `cargo build` failed until this worker added matching symlinks beside its own worktree.
Both worktrees were otherwise clean (no other worker's dirt) and on the correct branches, so this
was worked rather than stopped on — flagged here and in the `inbox/` drop below for whoever owns
the dispatch scripts.
