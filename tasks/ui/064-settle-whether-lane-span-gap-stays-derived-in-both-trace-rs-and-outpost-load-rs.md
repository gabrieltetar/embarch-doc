# 064 — Settle whether `Lane`/`Span`/`Gap` and the four exclusion flags stay derived in both `trace.rs` and `outpost_load.rs`

**State:** open
**Source:** `embarch-ui/open.md`'s third bullet, swept by leg 134's refill. The bullet has been
half-closed since `ui/051` retired the aggregation — shares and coverage now come from
`.../stream/{name}/load` (`embarch-core` decision 62) — and it says in its own words what is left:
*"`Lane`/`Span`/`Gap` and the four exclusion flags are still derived in both `trace.rs` and
`outpost_load.rs`"*, and *"Closing it needs per-span data, or a decision it stays split."*
**Scope:** ui
**Hardware:** none. Nothing is flashed, no probe, no live Core, no study. This is a read of two
source files and a decision recorded in prose.
**Owner:** no

## What

The open question has been sitting in a state where **both of its exits are available and neither
has been taken**, which is the shape that keeps an open question open indefinitely. It names them
precisely:

- **per-span data** — the `/load` route answers with the rollup only, so `embarch-ui` cannot get
  spans and gaps from Core and must derive them; or
- **a decision it stays split**, which is a decision nobody has written.

`embarch-core` decision 62 already states the cost of the split: `RecordKind`, gap semantics or an
exclusion rule changes in *both* places. That cost is real and recorded. What is missing is a
`embarch-ui` decision saying whether that cost is accepted deliberately, and under what condition
it would be revisited.

## What this task is, and what it is not

**It is:** read both derivations, establish exactly what is duplicated today (the `Lane`, `Span`
and `Gap` types and the four exclusion flags — name them), and record a numbered `embarch-ui`
decision that either accepts the split with its cost and a stated reversal condition, or states
precisely what per-span shape from `/load` would close it. Then update `open.md`'s bullet to match
what was decided, rather than leaving the question phrased as unanswered.

**It is not** a change to `embarch-core`. `outpost_load.rs` is core's file and `/load`'s response
shape is core's call — `../../embarch-fleet/protocol.md` §3 makes it `never` for a `ui` worker. If
the right answer is that Core should grow per-span data, **that is an `inbox/` drop for `core`**
(absolute path `/home/gabriel/Github/embarch/embarch-doc/inbox/`), not an edit and not a
cross-repo branch. Writing a `ui` decision that asserts what Core will do is also out of scope:
a decision here may state what `embarch-ui` does and what it would need, never what another
sub-project has agreed to.

**Do not restate `embarch-core` decision 62.** Cite it. Its cost statement is already written and
duplicating it into `ui`'s corpus is the same defect this repo spends most of its time removing.

## Done when

- [ ] The duplication is stated from the code as it is today, not from the bullet — both file paths,
      the types, and the four exclusion flags by name. If the bullet is already stale (the
      duplication narrowed or widened since it was written), **say so and correct it**; that is a
      better result than a decision written against a description.
- [ ] One numbered `embarch-ui` decision records the outcome, per `DOC-CONVENTIONS.md`, with a
      reversal condition if it accepts the split.
- [ ] `embarch-ui/open.md`'s bullet reflects what was decided, and no longer reads as an unanswered
      question if it is now answered.
- [ ] An `inbox/` drop for `core` **only if** the analysis concludes Core should grow per-span data.
- [ ] A `changelog.d/` fragment; a `status.d/` fragment for any suite-level fact this made false.
- [ ] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`,
      `check-docs.py`, `check-ownership.py --scope ui`, `check-client-names.py --repo <code worktree>`.
