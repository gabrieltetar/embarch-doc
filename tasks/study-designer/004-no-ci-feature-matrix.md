# 004 — this crate has no CI at all, so nothing ever builds its feature cells

**State:** claimed by agent/study-designer/004-no-ci-feature-matrix, 2026-09-05 23:35
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

- [ ] `embarch-study-designer/.github/workflows/test.yml` exists, with one clearly named step
      per feature cell above and clippy `-D warnings` on the widest set.
- [ ] Every step has been run locally and its result is stated — green, or red with the reason.
- [ ] A decision entry records **which cells are covered and why those** (numbered per
      `DOC-CONVENTIONS.md`; numbers are permanent), including the `ffi` judgment call.
- [ ] `embarch-study-designer/open.md`'s `alloc` bullet is rewritten — the hole it describes is
      closed by this, and the bullet must not keep claiming the crate owns no CI.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/study-designer-*`
      fragment dropped.
