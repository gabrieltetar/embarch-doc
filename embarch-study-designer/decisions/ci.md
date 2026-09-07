# embarch-study-designer decisions: What CI checks

**Status:** active, 2026-09-07.

What this crate's own CI runs, why each cell exists, and what it deliberately does not check.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Shape: [crate.md](crate.md).

### 64 — The feature matrix is six cells run by this crate's own CI, and the two narrow ones are `cargo build`, not `cargo test`

Nothing built or tested a single feature cell of the most depended-on crate in the suite until 2026-09-05. That is what let decision 46's `alloc` cell ship broken: `alloc` did not imply `serde/alloc`, so `Backing<T, N>: Deserialize` did not exist, and **every real consumer also pulls something that turns on `serde/std`, so feature unification always supplied the missing half.** Only this crate's own single-feature build could ever see it, and no consumer's CI can — by construction, because a consumer is what hides it.

`.github/workflows/test.yml` now runs, on push and pull_request, one named step per cell a real consumer actually uses — deliberately not a `2^7` powerset, which would be job count mistaken for coverage:

| Cell | Why it is its own cell |
|---|---|
| default (no features) | dev-bench firmware's `no_std`, allocator-free shape (decisions 5, 15, 46). The one that must never break. |
| `alloc` alone | The cell that was broken and unseen. Its own step with its own name, permanently. |
| `std` | Implies `alloc`; what `embarch-core`/`embarch-api`/`embarch-ui` get. |
| `gatt-extract`, `study-ui`, `eap-parse` | Each is `std`-only, off by default, and pulls its own dependencies (`regex`/`serde_json`/`ignore`, `toml`), so each rots independently. Run separately so one feature's compile error is not reported as another's. |
| `ffi` | Below. |

**The load-bearing half is that `default` and `alloc` are checked with `cargo build`, not `cargo test`.** This crate's only dev-dependency is `serde_json`, which pulls `serde` with `std`; edition 2021 means resolver v2, and resolver v2 unifies dev-dependency features into the library whenever it builds a target needing dev-deps — which `cargo test` always does. Measured with `cargo tree -f "{p} {f}"`: for the `default` cell `serde_core` is `result` with `-e normal` and `result,std` with `-e normal,dev`; for `std` both columns read `alloc,result,std`. So on the two narrow cells `cargo test` compiles a *different library than any consumer links*.

**Verified rather than reasoned**: reintroducing the bug on a scratch copy, `cargo build --no-default-features --features alloc` fails with 16 errors while `cargo test --no-default-features --features alloc` passes 9/9. A matrix copied verbatim from `embarch-topology`'s all-`cargo test` shape would have been a step that cannot fail for the reason it was added — worse than an absent one, because it reads as coverage. The `std` and tool cells keep `cargo test` alone, since a `build` twin there is measurably the same build.

**`ffi` is a `build` with a stated ceiling, and the workflow says so in its own comment.** A host `cargo build --features ffi` does type-check `src/ffi.rs`'s `extern "C"` surface (decisions 7, 23) against the rest of the crate in dev-bench's real `no_std`, no-alloc configuration, which is a real regression class. It does **not** prove what dev-bench needs: that the crate links as a `--crate-type staticlib` on a cross target with a panic handler and `panic = "abort"`. That build root does not exist yet, and adding a cross-compile step before the toolchain does would be the same fake-coverage mistake in a different place.

Clippy `-D warnings` runs on `--all-features` (the widest set, and the only configuration asserting the tool features do not collide) and again on `default` and `alloc`, because a `no_std` build's lints are not a subset of a `std` build's. `--locked` throughout is honest here: `Cargo.lock` is committed, this crate being the FFI build root (decision 23).

**Every step was run locally before the workflow was pushed, and all fourteen were green** — no cell was red on arrival.

Not in scope here, and deliberately absent: a `release.yml` carrying `embarch-umbrella` decisions 27/29's `verify-version` job. Decision 65.

### 65 — This crate does not release, and the first tag pushed is what reverses that

`embarch-umbrella` decisions 27/29 gave `verify-version` to the four repos that publish a binary and named this one among the four with none — *"every repo" means every repo that releases*. [../open.md](../open.md) called that "unaddressed, not deferred" and pointed at a decision that did not exist. It is **no**. There are **no git tags at all** and `Cargo.toml` has read `0.1.0` since creation, so the assertion — a *pushed tag* agrees with the manifest — has nothing to assert. All five consumers spell it `{ path = "../embarch-study-designer", … }` with **no `version` key** (decision 8), so nothing reads that number. And there is **no artifact**: `extract-gatt-config` is authoring-time behind an off-by-default feature nothing outside this repo packages, and `study-designer-ui` was retired 2026-08-24. The drift 27/29 guards — a binary whose `--version` disagrees with its tag — has no binary here to happen to.

**Against writing `release.yml` anyway**: `verify-version` fires `on: push: tags:`, so in a repo that pushes none it never executes once — the *step that cannot fail for the reason it was added* decision 64 rejects one entry up, and worse, because *does every repo check version against tag?* would read **yes** for a check that never ran. Nor is a guard needed before the workflow: a bare tag builds and uploads nothing, so **the only way an unverified artifact leaves is that someone writes a `release.yml` — the moment the obligation binds.**

**Reversal, any one:** crates.io publication; a consumer depending by version or git ref instead of by path; or **a tag pushed for any reason**. Then copy `verify-version` from `embarch-umbrella`'s `release.yml` with its three deliberate choices intact: `awk` not `cargo metadata`, leading `v` stripped rather than required, `workflow_dispatch` exiting 0 with a printed reason. **`test.yml` enforces that rather than trusting a reader** — a step, verified locally against five shapes, that passes while no `release.yml` exists and fails if one appears without a `verify-version` job another job `needs:`.

### 68 — `cargo doc` warnings do not join the gate

`rustdoc::broken_intra_doc_links` caught a real stale fact (a doc comment naming a `crate::validation` module that decision 19 retired) only because a worker happened to run `cargo doc --no-deps --all-features` by hand — it is not part of `../../../embarch-fleet/protocol.md` §10's `build`/`test`/`clippy -D warnings` gate, so five warnings sat unseen across several units. Not added anyway: a `-D warnings` rustdoc step is a real per-unit cost (this crate's doc comments run long, by design — decision 64's own entries are near the 1,200 B ceiling) charged on every green run to catch a class of drift that is rare and low-stakes once seen — a broken cross-reference, not a wire or behavior bug. The two stale links here dated back to decision 19's retirement and were closed by inspection, not by CI, the moment they were noticed. If intra-doc rot starts recurring rather than showing up once every several months, that recurrence — not this entry — is the reversal condition.
