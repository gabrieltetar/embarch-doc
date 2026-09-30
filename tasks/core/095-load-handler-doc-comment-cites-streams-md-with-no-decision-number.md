# 095 — The `/load` handler's doc comment cites "`embarch-core` decision, `decisions/streams.md`" with no number, and the decision it means is in another file

**State:** claimed by agent/core/095-load-handler-decision-62-cite, 2026-09-29 21:23
**Source:** the `core/093` reviewer, 2026-09-28, while sweeping inbound citations of the decisions
that unit moved. Not caused by `core/093`: this comment names no number at all, so no split could
have broken it, and it predates the leg.
**Scope:** core
**Hardware:** none — one doc comment in one Rust file.
**Owner:** no

## What

`embarch-core/src/study.rs` (≈ line 4209, on `main` at `48dc591`), the doc comment on the outpost
load-repartition handler, reads:

> computed once here from the rendered CSV [`stream_data_handler`] would otherwise only serve as
> bytes for someone else to compute (`embarch-core` decision, `decisions/streams.md`; suite
> decision 4, `../../embarch-doc/suite/decisions.md`).

Two defects in one citation. It says "decision" with **no number**, which no reference check can
resolve; and the file it names does not hold the decision it evidently means. The `/load` route is
**decision 62** — `### 62 — GET /study/{id}/stream/{name}/load answers the outpost's own load
repartition` — which `tasks/core/060` moved verbatim from `decisions/streams.md` to
`decisions/stream-index.md` on 2026-09-16. So the comment was probably correct-but-unnumbered before
that split and has been wrong-file since.

**Re-derive it rather than trusting this**: read decision 62 and its neighbours in
`stream-index.md` and confirm 62 is what the comment means; if it is 62 plus another, cite both.

## Done when

- [ ] The comment cites the decision by number, in this repo's source-comment citation form (bare
      number, no topic-file path — the form the `study-designer` and `topology` citation sweeps
      converged on, so the next split cannot strand it again).
- [ ] `grep -rn 'decisions/streams\.md' embarch-core/src` checked for any other comment of the same
      shape, and the tally reported either way.
- [ ] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green (a comment-only
      change still has to pass the gate); no `changelog.d/` fragment — nothing reader-facing moved.
