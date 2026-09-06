# 014 — The "do not run `cargo fmt`" instruction has no home a leg can write

**State:** open
**Source:** leg 016's supervisor, 2026-09-06, running `tasks/suite/006`. Dropped in `inbox/` as
`workers-must-be-told-not-to-run-cargo-fmt.md` and drained here by leg 017.
**Scope:** doc
**Hardware:** none — re-checked at drain, prose in reserved files only.
**Owner:** required — the instruction belongs in `embarch-fleet/` (`protocol.md` §5 and/or
`.claude/agents/embarch-worker.md`), which no leg checks out. Its second item is
`scripts/check-doc-size.py`, also reserved.

## What was decided, and what is missing

`tasks/suite/006` is closed: **the suite does not enforce `rustfmt`, and nobody runs
`cargo fmt`.** Recorded in [embarch.md](../../embarch.md) §5 with the measured cost and a reversal
condition, and in `suite/roadmap.md`'s **Later**.

**The load-bearing half of that decision is the worker instruction, and it is yours.** The
posture only closes the trap if it reaches a worker *before* it types `cargo fmt`. Today it
does not: a worker reads its task file and its agent definition, and neither says anything
about formatting. Leg 016 pasted the sentence by hand into each of its two dispatches, which
is a per-leg act that any leg can forget and which no successor inherits.

Suggested text, wherever it belongs:

> **Never run `cargo fmt`.** The suite does not enforce `rustfmt` (`embarch.md` §5). In a code
> repo you own the whole tree, so `check-ownership.py` will *not* stop a formatting diff
> hundreds of files wide from landing under your one-line task's message.

## Why the ownership check cannot catch it

This is the part worth keeping regardless of what you do with the sentence.
`check-ownership.py --scope <s> --code-repo` prints *"code repo, worker for `<s>` owns the whole
tree — not path-checked."* That is correct and deliberate. It also means **the one check that
exists to stop out-of-scope writes is structurally blind to the largest out-of-scope diff a
worker can produce.** The only thing standing between the suite and a 1,881-line mechanical
commit landing under a one-line task message is a worker choosing not to type a normal command.

`api/019`'s worker typed it, watched it rewrite 18 files it had not touched, reverted all of it
and re-applied its change by hand — and then reported the fact instead of quietly working
around it. That is the only reason any of this is visible.

## The numbers, measured at `main` on 2026-09-06

The table in `tasks/suite/006` was wrong in two ways and both are worth correcting wherever it
gets cited. Its counts were **hunks labelled as files**, and it omitted two Rust crates —
including the largest.

**Corrected once more by this unit's reviewer** — see
`inbox/suite-rustfmt-cost-omits-a-path-dep-crate.md`, which has the authoritative table and the
method. Totals: **87 files, 1,288 hunks, 1,947 existing lines**, with `embarch-api` (24 files)
tying `embarch-study-designer` for largest. My first pass missed
`embarch-api/crates/embarch-core-client`, because **bare `cargo fmt --check` does not descend
into local path-dependency crates** — which matters far more than the 3.5% it adds to the
total: wired into §10 or CI as written, that command passes green with six files unformatted.

`embarch-outpost` (a Zephyr C module) and `embarch-dev-bench` have no `Cargo.toml` and are not
in scope at all, so "no repo in this suite is clean" is a statement about **six** crates.

## A second, smaller thing found on the way

**`embarch.md` is not tracked by `scripts/check-doc-size.py`.** It is 12 KB, it is where §5's
principles and §6's index live, and it has no cap and no reserve. Every other suite-level doc
has one. Not acted on — `scripts/` is yours — but it is the file this decision was just written
into, and a doc with no cap is the one that grows.

## Done when

- [ ] A worker is told not to run `cargo fmt` by something it reads every time, not by a
      sentence a supervisor remembers to paste.
- [x] `embarch.md` either has a size role or is deliberately exempt, on the record.
      **Given a role, 2026-09-06.** It had neither: `check-doc-size.py`'s legacy pattern was
      `^embarch-`, requiring a hyphen, so `embarch.md` matched nothing — 15 KB of suite index
      and status table with no cap and no row in `--report`, while every sibling beside it
      (`embarch-token.md`, `embarch-zephyr.md`, `README.md`) was capped at 25 KB. The pattern
      is now `^embarch[-.]` and it reports 14.9K/25K, legacy.
      **Worth keeping:** it *was* classified for ownership — `check-ownership.py --supervisor`
      asserts every tracked top-level `*.md` is reserved or fleet-writable and passed on it.
      Two lists over the same files, agreeing on membership and not on coverage, which is why
      nothing noticed.
