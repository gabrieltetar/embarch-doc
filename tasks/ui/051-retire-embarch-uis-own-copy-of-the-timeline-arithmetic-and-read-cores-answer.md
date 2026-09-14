# 051 — Retire `embarch-ui`'s own copy of the timeline arithmetic and read Core's answer instead

**State:** claimed by agent/ui/051-retire-timeline-arithmetic, 2026-09-13 22:37
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

- [x] `embarch-ui` obtains per-subject load shares and the coverage line from Core's route, not
      from its own parse.
      `decode_trace` (`src/main.rs`) now calls `CoreClient::get_study_load` and passes its
      `LoadAnswer.summary` (`embarch_core_client::LoadSummary`, `api/094`'s mirror type) straight
      into `trace::parse`, which stores it on `TraceView::summary` unchanged rather than computing
      it.
- [x] The duplicated types and functions in `trace.rs` are **deleted**, not left unused — a dead
      second implementation is still a second implementation for anyone grepping.
      Deleted from `embarch-ui/src/trace.rs`: `struct LoadSubject`, `struct LoadSummary`, `fn
      summarize` (the repartition arithmetic), and `fn merged_gap_extent` (only `summarize`'s own
      helper — used nowhere else). `parse`/`parse_with_cap` gained one new parameter (`summary:
      embarch_core_client::LoadSummary`, supplied by the caller) in place of the local
      computation. The `#[cfg(test)] mod load_summary_tests` module (nine tests) that pinned
      `summarize`'s own arithmetic is deleted with it — that arithmetic no longer lives in this
      crate to pin. Two other tests (`a_capture_with_no_clock_at_all_is_drawn_against_frames`,
      `a_frame_boundary_is_not_a_time_boundary`) had a handful of assertions against
      `view.summary.*` trimmed to the `Lane`/`Span`-level flags they were actually exercising;
      every `parse`/`parse_with_cap` test call site (~35, mechanically) now passes a fixed,
      clearly-labelled `placeholder_summary()` fixture with no claim of correctness, since none of
      those tests have a stake in the repartition's content. Net, verified via `git diff --numstat`
      rather than estimated: `src/trace.rs` 95 insertions / 514 deletions, `src/main.rs` 27
      insertions / 6 deletions.
- [x] The chart geometry listed above is untouched and still renders.
      `bin_window`, `BinRun`, `BinnedLane`, `BinnedWindow`, `StepStamp`, `StepBand`, `StepRow` and
      `TraceView`'s payload shape are byte-for-byte what they were; `Lane`/`Span`/`PointEvent`/`Gap`
      and `parse`/`parse_with_cap` are **kept**, not retired — Core's `/load` answer carries only
      the aggregated `LoadSummary`, no per-span data, so the chart's own timeline still has to be
      built locally from the same CSV. All 91 non-ignored tests pass, including
      `binning_tests`/`browser_reference` (the bin-vs-browser-aggregation cross-check) unchanged.
- [x] The `422` column-mismatch refusal is surfaced to the user as a refusal, not as an empty
      chart. `embarch-ui` decision 10 (trace)'s own pin is what Core now enforces on the UI's
      behalf; the UI must not silently swallow it.
      `decode_trace` never substitutes a default/empty summary on a `get_study_load` failure — any
      error (network, or Core's own `422`) is propagated as `502 Bad Gateway` with Core's message
      text verbatim, the same status every other proxied Core round trip in that function already
      uses. In practice a `422` from Core's `/load` cannot silently diverge from what the UI itself
      renders: `trace::parse` still runs the identical `outpost::csv_header()` check against the
      identical bytes for its own chart parse, and independently refuses with its own `422`
      (`UNPROCESSABLE_ENTITY`) the same way it did before this task — both checks come from the
      same shared crate function on the same CSV, so neither route can accept what the other
      refuses.
- [x] `embarch-core` decision 62 and suite decision 4 can both be read as fully true afterwards.
      Say so explicitly in the task when closing it — that sentence is the point of the unit.
      **Both are now fully true.** `embarch-core` decision 62 ("an agent reaching the same answer a
      human already gets through `embarch-ui`'s Trace tab, without a second implementation of the
      timeline arithmetic on this side of the wire") holds for the human path too now: `embarch-ui`
      reads the same `/load` answer rather than recomputing it. Suite decision 4 ("the suite
      currently has two implementations of the same timeline" ending) is closed: the load
      repartition (`LoadSubject`/`LoadSummary`/`summarize`) is computed in exactly one place,
      `embarch-core/src/outpost_load.rs`; `embarch-ui/src/trace.rs` fetches that answer and keeps
      only the chart-geometry half (lanes/spans/gaps/markers/binning) suite decision 4 never
      claimed.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
      `embarch-ui`: `cargo build`, `cargo test` (95 tests, 91 pass + 4 `#[ignore]`d
      hardware/perf-measurement tests, 0 failed), `cargo clippy --all-targets -- -D warnings` all
      clean. `embarch-doc`: `check-docs.py` 11/11 green (had to trim `embarch-ui/decisions/
      trace-view.md`'s own decision 10 prose to fit back under its pinned 8192 B baseline after
      editing it — the net addition is one citation sentence, not new content weight),
      `check-ownership.py --scope ui` and `--code-repo` both green, `check-client-names.py` clean.
- [x] `changelog.d/` fragment.
      `changelog.d/ui-retire-load-repartition-duplicate.changed.md`.

## Finding: `get_study_load`'s errors are not status-code-typed

Not a blocker, and not this task's repo to fix (`embarch-api`/`embarch-core-client`), but worth
recording rather than only living in this leg's diff: `CoreClient::get_study_load` (`api/094`)
returns a plain `anyhow::Result<LoadAnswer>` — every non-2xx response (`400` wrong encoding, `404`
no such tap, `422` column mismatch, or a network failure) collapses to one formatted string via
`format_study_error`, with the numeric status embedded in the text but not exposed as a value a
caller can match on structurally (contrast `StudyConflictError`/`TopologyMismatchError`/
`DevBenchBusyError`, which are downcastable). `embarch-ui` cannot distinguish these here without
string-sniffing, which the rest of this codebase deliberately does not do, so `decode_trace` maps
every `get_study_load` failure to the same `502` regardless of cause — correct in the sense that
nothing is swallowed, imprecise in the sense that a genuine `422` reads to a caller identically to
Core being unreachable. Two things bound the practical cost: `decode_trace` only reaches this call
after `entry.rendered` already holds (ruling out Core's `404`) and this route only ever serves
`OutpostTrace` taps in practice (ruling out Core's `400`), and `embarch-ui`'s own `trace::parse`
runs the identical column-header check on the identical bytes moments later and refuses with a
proper `422` on the one remaining case that matters. If `get_study_load` ever grows a real second
caller that cannot lean on that coincidence, it should get a downcastable error type matching the
others in `embarch-core-client`.
