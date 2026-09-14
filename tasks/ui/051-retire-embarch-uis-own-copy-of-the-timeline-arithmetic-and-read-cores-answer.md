# 051 — Retire `embarch-ui`'s own copy of the timeline arithmetic and read Core's answer instead

**State:** open
**Source:** `tasks/core/057`'s own "Sequencing" section, which named this follow-up, ranked it
**lowest of the three**, and said it must not be filed until `core/057` landed. It landed
2026-09-13 (code `a131f63` in `embarch-core`, doc `886a0bc` in `embarch-doc`), so it is filed now,
in the same fold.
**Scope:** ui
**Hardware:** none — host-side Rust and one doc file. No board, no probe, no deploy. Exercising it
against a live Core is the owner's, not this task's.
**Owner:** no

## What

`core/057` **ported** the CSV-to-lanes-to-gaps arithmetic into `embarch-core/src/outpost_load.rs`
— it did not share it, and it could not delete the original, because a worker owns exactly one
sub-project. So **the suite currently has two implementations of the same timeline**, which is
precisely the state [suite decision 4](../../suite/decisions.md) exists to end.

What is duplicated, in `embarch-ui/src/trace.rs` (~4,126 lines; **re-derive the line numbers, do
not trust any written here or in `core/057`** — every number in `tasks/suite/018` was 20–30 lines
out and its line count was 234 low):

| in `embarch-ui/src/trace.rs` | now also in `embarch-core/src/outpost_load.rs` |
|---|---|
| `Lane`, `Span`, `PointEvent`, `Gap` | the timeline |
| `LoadSubject`, `LoadSummary` | the answer |
| `parse` / `parse_with_cap` | CSV → timeline |
| the repartition — *"pure arithmetic over already-built lanes"* | the answer |

Replace that with a call to `GET /study/{id}/stream/{name}/load` through the existing Core client,
and delete what becomes dead.

## What must NOT be touched

Per suite decision 4, and this is the half that is easy to over-reach on: **the chart geometry
stays here.** `bin_window`, `BinRun`, `BinnedLane`, `BinnedWindow`, `StepStamp`, `StepBand`,
`StepRow` and the `TraceView` payload shape are `embarch-ui`'s and stay `embarch-ui`'s —
[`embarch-ui` decision 18](../../embarch-ui/decisions/trace-transfer.md)'s server-side-binning shape is
**preserved, not reopened.** If retiring the parse means the binning loses its input, the answer is
to feed the binning from Core's response, not to move the binning.

## Why it is ranked last of the three

**The UI is correct today.** It renders the right numbers and a human gets the right answer; the
duplication is a maintenance liability, not a defect a user can see. The other two follow-ups
(`tasks/api/094`, the MCP tool) close a capability that does not exist at all. So this one is real
work with a real payoff and no urgency — take it when the queue has room, not ahead of something
broken.

## Why it still has to happen

[Reversals row 86](../../reversals/rows-73-92.md): one wire change produced **two** independent
host failures — the UI's 46× load-share error *and* Core's own manifest-latching bug — because
there were two independent hosts. **A move that leaves two implementations behind has bought
nothing**, and until this lands, that is exactly what suite decision 4 has bought.

## Done when

- [ ] `embarch-ui` obtains per-subject load shares and the coverage line from Core's route, not
      from its own parse.
- [ ] The duplicated types and functions in `trace.rs` are **deleted**, not left unused — a dead
      second implementation is still a second implementation for anyone grepping.
- [ ] The chart geometry listed above is untouched and still renders.
- [ ] The `422` column-mismatch refusal is surfaced to the user as a refusal, not as an empty
      chart. `embarch-ui` decision 10 (trace)'s own pin is what Core now enforces on the UI's
      behalf; the UI must not silently swallow it.
- [ ] `embarch-core` decision 62 and suite decision 4 can both be read as fully true afterwards.
      Say so explicitly in the task when closing it — that sentence is the point of the unit.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
