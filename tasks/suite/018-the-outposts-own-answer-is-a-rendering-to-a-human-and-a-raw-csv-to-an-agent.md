# 018 — The one question `embarch-outpost` exists to answer is answerable by a human and not by an agent

**State:** done — executed 2026-09-13 20:2x by leg 111's supervisor as
[suite decision 4](../../suite/decisions.md), under the window below, which had already
closed unanswered. The code move is `tasks/core/057`.

**Previously:** open — **announced and parked, 2026-09-13 19:21, `ts` `1789348880.412099`**
(`#embarch-fleet`, `C0BUKTL2FPC`). The 30-minute window opened at that post and is **not to be
restarted**: `.claude/leg.md` and `../../embarch-fleet/ops.md` §4 both say a leg that ends before
the window closes leaves the `ts` here and the *next* leg completes it. Poll with
`python3 ../../embarch-fleet/scripts/fleet-read.py --thread 1789348880.412099`.

**What was announced, which bounds what may be executed under this window:** settle *where the
outpost's trace analysis lives* as a numbered decision, naming the property below — **not** move
`trace.rs`'s 3,892 lines. The code move follows as separately queued tasks. A reply saying go runs
it immediately; a cancel drops this back to plain `open` with the reply quoted here.

**The window CLOSED UNANSWERED at 2026-09-13 19:51** — 30 minutes elapsed, thread polled four times
(19:22, 19:34, 19:47, 19:51), no reply from `U0AGQGSHM2P` and nothing actionable in the channel.
**So the next leg to pick this up does not wait at all: the condition is already met and it may
execute immediately.** Do not re-announce and do not restart the clock — `ops.md` §4 is explicit
that the relay must not restart a 30-minute window every twenty minutes, or a `suite` task never
runs.

The leg that announced it had all four of its units already dispatched and reached its cap, so it
did **not** execute it. That is the only reason this is still open.
**Source:** suite review pass 2026-09-06, dimension 3 (one philosophy). Code-confirmed.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`embarch-outpost/spec.md:16` states the capability as *"the study passed, but what was the CPU
doing while it did?"* The analysis that answers it — lanes, spans, gap coverage, per-subject load
shares — lives entirely in `embarch-ui/src/trace.rs`, **3,892 lines**: `LoadSummary` at `:334`,
`parse` at `:1287`, the repartition at `:1187` (*"Pure arithmetic over already-built lanes"*),
`bin_window` at `:2122`. Every `std::fs` call in that file is above the `#[cfg(test)]` at `:2145`
— **there is no I/O in it outside its own tests**, so it is pure computation that simply lives in
one consumer. The shared crate's half
(`embarch-study-designer/src/outpost.rs`) stops at `chunks` / `decode_frame` / cycle-unwrap / CSV
rendering.

An agent gets `study_stream_data` and a CSV that has run to 225,606 rows, and must re-derive all
of it. `embarch-api/interfaces/studies.md` serves *"one declared tap's capture"*; nothing in the
23 tools analyses one. And `embarch-ui/open.md` records that the UI's copy is structurally
unreachable from the agent path — reaching it would mean *"giv[ing] `embarch-ui` a dependency on
`embarch-api` (a direction the suite has nowhere)"*.

Candidate direction: name the property — **an agent can obtain the outpost's own answer
(per-subject load shares plus the coverage line) without re-deriving the timeline** — and let
whoever takes it choose the home. One warning for them: `embarch-study-designer/spec.md` §1's
membership rule (*"anything every consumer must agree on byte-for-byte or column-for-column
belongs here"*) argues **against** the shared crate, so that route should not be assumed. Core,
which already decodes against the manifest and writes `streams/index.json`, is the other candidate.

## Why now

`embarch.md` §5: *"Every hardware-facing capability is reachable both by an agent and directly by
a human, **converging on the same underlying modules**."* The analysis landed where its first
consumer was, which was reasonable, and no decision ever asked where it should live — I read
`embarch-ui/decisions/trace-view.md`, `trace-chart.md`, `trace-transfer.md` and
`embarch-study-designer/decisions/removed.md`, and the only placement clause is about *vocabulary*
(`trace-view.md:15`: the column list is checked against the shared crate's header).

**The suite has already measured what a second consumer computing this independently costs.**
`embarch-decision-reversals.md` row 86: a consumer re-deriving the timeline reported the outpost's
own drain thread at 78.1% against a true 1.6% — a **46× error on the single number the next
session was briefed to reduce.** An agent handed a raw CSV is exactly that second consumer.

## Done when

- [x] An agent can obtain per-subject load shares and the coverage line for an outpost capture
      without re-implementing the timeline. — **named as the property suite decision 4 buys.** The
      announced scope was to settle the home, not to build the route; the build is `tasks/core/057`
      and the tool that actually closes this box is filed when that lands.
- [x] Whichever module holds the analysis is the only one that computes it, or the second copy is
      pinned against the first. — **settled as the first**, with the pin that already exists
      (`embarch-ui` decision 10 (trace), CSV header against the shared crate) carried across.
- [x] Gate green; `changelog.d/` fragments for each repo touched. — doc repo only; nothing else
      was touched, because no code moved.

## What this found that the task itself had wrong

Both recorded in the decision, because each resolves to a real sentence in a real file:

1. **`embarch-ui/open.md`'s *"a direction the suite has nowhere"* is from the reflash-selector
   bullet** (`embarch-ui` decision 11, about `run_study --reflash` orchestration), **not** a
   statement that the trace analysis is unreachable from the agent path. The conclusion holds on
   other grounds; the evidence cited for it was about something else.
2. **`embarch-ui` is already a server**, not a thick client — `src/main.rs` serves
   `GET /api/trace/{study}/{tap}/bins` and decision 18 already puts the aggregation server-side.
   The analysis was never "computation that happens to live in one consumer"; it is behind an HTTP
   surface the agent path does not reach and the release archive does not ship. That reframing is
   what made `embarch-core` the answer rather than a toss-up.
3. `trace.rs` is **4,126** lines, not 3,892, and every line number this task cites is 20–30 out.
