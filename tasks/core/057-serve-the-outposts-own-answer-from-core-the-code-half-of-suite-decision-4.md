# 057 — Serve the outpost's own answer from Core: the code half of suite decision 4

**State:** open
**Source:** `tasks/suite/018`, executed by the supervisor's own hands on 2026-09-13 as
[suite decision 4](../../suite/decisions.md). That decision named the home and
**deliberately did not move the code**; this is the move.
**Scope:** core
**Hardware:** none — the analysis is pure computation over a rendered CSV. No board, no probe, no
live Core, no deploy. A committed capture fixture is enough, and `embarch-ui` already has one.
**Owner:** no

## What

[Suite decision 4](../../suite/decisions.md) settles that an outpost capture's
**per-subject load shares and its coverage line** are computed exactly once, in `embarch-core`,
beside the decode that already lives in `src/outpost_manifest.rs`. Today they are computed in
`embarch-ui/src/trace.rs` (4,126 lines), which no agent path reaches and which
`assemble-suite.yml` does not ship.

**What moves** — the pure computation from CSV to answer:

| in `embarch-ui/src/trace.rs` | what it is |
|---|---|
| `Lane` `:124`, `Span` `:159`, `PointEvent` `:191`, `Gap` `:225` | the timeline |
| `LoadSubject` `:284`, `LoadSummary` `:333` | the answer |
| `parse` `:1295` (and `parse_with_cap` `:1314`) | CSV → timeline |
| the repartition at `:1187` — *"pure arithmetic over already-built lanes"* | the answer |

**What does not move**, per the decision: `bin_window` `:2151`, `BinRun` `:2014`,
`BinnedLane` `:2031`, `BinnedWindow` `:2043`, `StepStamp` `:404`, `StepBand` `:419`,
`StepRow` `:452` and the `TraceView` `:517` payload shape. That is chart geometry, and
[`embarch-ui` decision 18](../../embarch-ui/decisions/trace-transfer.md)'s server-side-binning
shape is preserved rather than reopened.

**Line numbers are from 2026-09-13 20:1x and will drift — re-derive them, do not trust them.**
`tasks/suite/018` cited this same file with every number 20–30 lines out and a line count 234 low.

## The one thing this task must not do

**Do not write a second decoder.** Core already decodes raw frames against the manifest and
**refuses a manifest whose `record_layout_version` differs from the shared crate's**
(`src/outpost_manifest.rs`). The analysis consumes the **rendered CSV** Core itself produces, and
it inherits `embarch-ui`'s existing pin: [`embarch-ui` decision 10 (trace)](../../embarch-ui/decisions/trace-view.md)
checks the CSV's column list against the shared crate's own header and **refuses if it differs**.
Carry that check across; do not re-implement it loosely.

[Reversals row 86](../../reversals/rows-73-92.md) is why: one wire change produced **two**
independent host failures — the UI's 46× load-share error *and* Core's own manifest-latching bug —
because there were two independent hosts. A move that leaves two implementations behind has bought
nothing.

## Done when

- [ ] Core computes per-subject load shares and the coverage line for a capture it already holds.
- [ ] It is reachable over HTTP, alongside the existing `/study/{id}/stream/{name}` surface, and
      `embarch-core/interfaces/studies.md` documents the route.
- [ ] The column-list-against-shared-crate-header check came across and still refuses a mismatch.
- [ ] A numbered `embarch-core` decision records the route's shape.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including a native Windows build if one
      can be had — this repo already owes `core/015`'s, fourteen changes deep.
- [ ] `changelog.d/` fragment.

## Sequencing — read this before filing anything downstream

**Two follow-ups exist and neither may be filed until this lands**, because both consume a route
that does not exist yet and a worker given one of them today would build against nothing:

1. `tasks/api/<next>` — an MCP tool so an agent can ask for the answer. That is the whole point of
   suite decision 4 and the unit that actually closes its property.
2. `tasks/ui/<next>` — `embarch-ui` stops computing the timeline and reads Core's answer.
   **Lowest priority of the three:** the UI is correct today, and the duplication it leaves is a
   known one with a decision pointing at it.

File them in the same fold that lands this, not before.

## Reserve, for planning

`embarch-core/decisions/auth.md` is 11,356/12,288 B — **932 B left, 92.4%** — filed against
**blocked** `tasks/core/046`, size debt due 2026-09-26. Nothing this task decides belongs in
`auth.md`; put the new decision in a topic file with headroom and check it first. If your work
leaves any `embarch-core` doc in the last 10% of its cap unfiled, file
`tasks/core/<next>-compact-core.md` in the same commit — **your own scope**, never `tasks/doc/`.
