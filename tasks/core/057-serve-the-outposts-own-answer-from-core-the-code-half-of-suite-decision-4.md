# 057 — Serve the outpost's own answer from Core: the code half of suite decision 4

**State:** done — `agent/core/057-serve-outposts-own-answer` (code) /
`agent/core/057-serve-outposts-own-answer-doc` (doc), pushed 2026-09-13
**Source:** `tasks/suite/018`, executed by the supervisor's own hands on 2026-09-13 as
[suite decision 4](../../suite/decisions.md). That decision named the home and
**deliberately did not move the code**; this is the move.
**Scope:** core
**Hardware:** none — the analysis is pure computation over a rendered CSV. No board, no probe, no
live Core, no deploy. A committed capture fixture is enough, and `embarch-ui` already has one.
**Owner:** no

**Reserve (told at dispatch, 2026-09-13 20:33):** one `embarch-core` doc file is in reserve —
`decisions/auth.md`, **92.4%**, 932 B left, filed against `tasks/core/046` which is **`blocked`
on `In flux: yes`**. Nothing else in this sub-project is in reserve, so **the new numbered
decision this task owes must not go in `auth.md`** — it is a study/stream route decision and
belongs in the topic file that already holds the stream surface. If you find yourself forced into
`auth.md` anyway, `DOC-COMPACTION.md` §2 applies: compact that file as part of this unit, carrying
`tasks/core/046`'s `Must not delete:` list and closing only that file's item. And if your work
pushes any `embarch-core` doc file into its last 10%, file
`tasks/core/<next>-compact-core.md` in the same commit (`check-task-numbers.py --next core` for
the number — never `ls | tail`).

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

- [x] Core computes per-subject load shares and the coverage line for a capture it already holds.
      `src/outpost_load.rs`: `load_answer(csv: &str) -> Result<LoadAnswer, String>`, ported from
      `embarch-ui/src/trace.rs`'s `parse`/`parse_with_cap`/`summarize` — the CSV-to-lanes-to-gaps
      arithmetic only, not the chart geometry (`bin_window`, `BinRun`, `BinnedLane`, `BinnedWindow`,
      `StepStamp`, `StepBand`, `StepRow`, `TraceView`, all correctly re-derived as *not* moving:
      re-checked against the real file, which is 4,126 lines as the decision said, not the task's
      original 3,892). Verified against the same real firmware fixture
      `outpost_manifest.rs`'s own decoder test pins against
      (`tests/fixtures/outpost-native-sim.bin`/`-manifest.json`) — rendered through
      `outpost_manifest::render` unmodified, then fed to `load_answer`, in
      `outpost_load::tests::a_real_firmware_captures_load_answer_reports_a_named_us_axis_with_a_real_gap`.
- [x] It is reachable over HTTP, alongside the existing `/study/{id}/stream/{name}` surface:
      `GET /study/{id}/stream/{name}/load` (`study::stream_load_handler`, wired in `api.rs`,
      `// route:` comment matched, `AUTH_CASES` row added, `DOCUMENTED_ROUTE_COUNT` moved 22→23 —
      all four caught by `api.rs`'s own self-checking tests before this was findable any other way).
      `embarch-core/interfaces/studies.md` documents the route, its request/response shape and its
      `400`/`404`/`422` cases.
- [x] The column-list-against-shared-crate-header check came across and still refuses a mismatch:
      `load_answer` checks `header != outpost::csv_header()` and refuses (`422` at the route),
      same as `embarch-ui` decision 10 (trace)'s pin — covered by
      `a_mismatched_column_list_is_refused_not_guessed`.
- [x] A numbered `embarch-core` decision records the route's shape: decision 62, filed in
      `decisions/streams.md` (30, 38, 39, 62 — **not** `auth.md`, per the Reserve note below).
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) on Linux: `cargo build`, `cargo test`
      (205 passed, 2 ignored — both pre-existing, hardware/fixture-gated), `cargo clippy
      --all-targets -- -D warnings` (clean) in the code worktree; `scripts/check-docs.py` (11/11
      green after fixing two `decision 4` citations the checker itself caught pointing at the topic
      file instead of `suite/decisions.md` — `check-decision-refs.py`'s own rule, DOC-CONVENTIONS.md:
      link the index); `scripts/check-ownership.py --scope core` (doc worktree) and
      `--code-repo` (code worktree) both green; `scripts/check-client-names.py --repo <code
      worktree>` clean against 7 denylist entries.
      **Native Windows build not attempted** — same debt `tasks/core/015` already records (Windows
      `cargo.exe` cannot resolve this worktree's symlinked path-dep siblings over UNC); this task
      adds no new Windows-only surface (no `cfg(windows)` code), so the debt's shape is unchanged,
      just one change deeper.
- [x] `changelog.d/core-outpost-load-route.added.md`.

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
