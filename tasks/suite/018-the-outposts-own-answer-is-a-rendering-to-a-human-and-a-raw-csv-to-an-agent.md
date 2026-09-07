# 018 — The one question `embarch-outpost` exists to answer is answerable by a human and not by an agent

**State:** open
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

- [ ] An agent can obtain per-subject load shares and the coverage line for an outpost capture
      without re-implementing the timeline.
- [ ] Whichever module holds the analysis is the only one that computes it, or the second copy is
      pinned against the first.
- [ ] Gate green; `changelog.d/` fragments for each repo touched.
