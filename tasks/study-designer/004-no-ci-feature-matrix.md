# 004 — this crate has no CI at all, so nothing ever builds its feature cells

**State:** done, 2026-09-05 — agent/study-designer/004-no-ci-feature-matrix
**Source:** `embarch-study-designer/open.md` — "Nothing builds or tests the `alloc`-only
feature cell on a schedule … the hole that let it sit unnoticed is still open, since this
crate owns no CI of its own to close it." Swept 2026-09-05 by leg 014 when the queue hit
zero.
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`embarch-study-designer/.github/workflows/` **does not exist** — this crate has no CI of any
kind, while `embarch-topology`, `embarch-core`, `embarch-api` and `embarch-umbrella` all do.
It is the most depended-on crate in the suite (`embarch-core`, `embarch-api`, `embarch-ui`,
`embarch-umbrella` and dev-bench firmware all consume it), and it is the one with the largest
feature matrix.

**That gap has already cost something real, once, and the crate's own `Cargo.toml` says so in
prose.** `tasks/study-designer/003` fixed a `cargo test --features alloc` compile failure that
sat undetected on `main` because `alloc` did not turn on `serde/alloc`, so `Backing<T, N>`'s
`Deserialize` did not exist. Nobody saw it because **every real consumer also pulls something
that turns on `serde/std`, so feature unification always supplied the missing half** — the
crate's single-feature build was the only configuration that could see it. The comment above
the `alloc` feature ends: *"it is exactly the configuration the feature matrix is supposed to
check."* There is no feature matrix.

**Add one.** `embarch-topology/.github/workflows/test.yml` is the model to copy the shape
from — a `Test` job on push and pull_request, `dtolnay/rust-toolchain@stable` with clippy, and
one named `cargo test --locked …` step per feature cell that a real consumer actually uses,
plus clippy on the widest set. Read it; do not invent a different shape for this repo.

**Which cells, and why each is a cell rather than a combination:**

- **default (no features)** — dev-bench firmware's `no_std`, allocator-free configuration
  (decision 15, decision 46). The one that must never break.
- **`--no-default-features --features alloc`** — the cell that was broken and unseen. This is
  the whole reason the task exists; it must be its own step with its own name.
- **`--features std`** — implies `alloc`, and is what the host consumers get.
- The `std`-only tool features: **`gatt-extract`**, **`study-ui`**, **`eap-parse`**. Each
  pulls its own dependencies (`regex`/`serde_json`/`ignore`, `toml`) and each is off by
  default, so each can rot independently.
- **`ffi`** — the `extern "C"` surface dev-bench links against. If a cross-compile is what
  actually exercises it and a host `cargo build --features ffi` proves little, **say so in the
  workflow's own comment** rather than adding a step that looks like coverage and is not. A
  step that cannot fail for the reason you added it is worse than an absent one.

**Do not build a full powerset.** The point is the cells a consumer really uses plus the ones
feature unification hides, not `2^7` jobs. If two cells are genuinely the same build, say
which and run one.

**A `cargo test --locked` needs `Cargo.lock` committed.** Check whether it is; if it is not,
either commit it or drop `--locked` and note in the workflow why, but do not leave a step that
fails on a fresh runner for a reason unrelated to the code.

**Run every cell locally before you push it.** If one is red today, that is a finding of the
same class as `003` and it is in scope to fix if the fix is small — and if it is not small,
**leave the step in, mark the workflow's job `continue-on-error: false` anyway, and file a
follow-up task**, because a red CI that names a real break is the correct outcome. Say plainly
in the task file and the changelog fragment which cells were already broken when you arrived.

## Why now

`open.md` states it today, so it reconciles. The cost is one file. The thing it guards is a
class of failure the suite has already been bitten by once and can only ever detect this way —
no consumer's CI can see it, by construction, because a consumer is what hides it.

## Not in scope

The `verify-version` release job that `embarch-umbrella`'s decisions 27/29 put in four repos'
`release.yml`. **This repo has no `release.yml` either**, which is a separate absence with a
separate decision behind it. Name it in `open.md` if you like; do not build it here.

## Reserve

Nothing in `study-designer` is in reserve. The tightest files are `open.md`
**4.3K / 5K (86%)** and `spec.md` **8.6K / 10K (86%)**, both with real headroom, and the
sixteen `decisions/` files are all under 80%. If your edit puts a file at or above 90%, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit per
`tasks/README.md`.

## Done when

- [x] `embarch-study-designer/.github/workflows/test.yml` exists — 14 steps, one
      named per feature cell, clippy `-D warnings` on `--all-features` plus the
      two narrow cells.
- [x] Every step run locally. **All fourteen green; no cell was red on arrival.**
- [x] Decision 64 (`embarch-study-designer/decisions/crate.md`) records the cells,
      why those, and the `ffi` judgment call.
- [x] `open.md`'s `alloc` bullet rewritten — the section now names the two holes
      that remain (no staticlib cross-link, no `release.yml`) and no longer claims
      the crate owns no CI.
- [x] Gate green; `changelog.d/study-designer-feature-matrix-ci.added.md` and
      `features.d/study-designer-180-feature-matrix-ci.md` dropped.

## What was found

**The shape the task told me to copy would not have worked, and this was measured,
not reasoned.** `embarch-topology`'s workflow is all `cargo test`. This crate's
only dev-dependency is `serde_json`, which pulls `serde` with `std`; edition 2021
means resolver v2, which unifies dev-dependency features into the library for any
target needing dev-deps — and `cargo test` always does. `cargo tree -f "{p} {f}"`:

| cell | `serde_core`, `-e normal` | `serde_core`, `-e normal,dev` |
|---|---|---|
| default | `result` | `result,std` |
| `alloc` | `result` | `result,std` |
| `std` | `alloc,result,std` | `alloc,result,std` |

So on `default` and `alloc` a `cargo test` step compiles a different library than
any consumer links. **Proved by reintroducing 003's bug** (`alloc = []`) on a
scratch copy: `cargo build --no-default-features --features alloc` fails with 16
errors, `cargo test --no-default-features --features alloc` passes 9/9. A
`cargo test`-only matrix would have been exactly the fake-coverage step this task
warned against. Those two cells therefore get `cargo build` steps; `std` and the
three tool features keep `cargo test` alone, because the columns are identical
there and a `build` twin would be duplicated work pretending to be coverage.

`Cargo.lock` is committed, so `--locked` is honest. No `apt` step: unlike
`embarch-topology` nothing here needs libudev, and every optional dependency is
pure Rust. No `Cargo.toml` change was needed for any cell.

**Local results, all green:** `build`/`test` default; `build`/`test` alloc;
`build`/`test` std; `test` gatt-extract; `test` study-ui; `test` eap-parse;
`build` ffi; clippy `--all-features`, default and alloc, each `--all-targets
-- -D warnings`.

**`ffi` is a `build` with a stated ceiling** written into the workflow's own
comment: it type-checks the `extern "C"` surface on the host in dev-bench's real
`no_std`/no-alloc shape, and does **not** prove the `--crate-type staticlib`
cross-link, whose build root does not exist. That limit is now `open.md`'s first
bullet rather than an invisible gap.
