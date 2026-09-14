# 059 — Three behaviours lost their only test when `embarch-ui` deleted `load_summary_tests`

**State:** done
**Source:** `ui/051`'s reviewer, leg 112, 2026-09-13, reported as a secondary observation rather than
a decision contradiction. `ui/051` deleted `embarch-ui/src/trace.rs`'s `summarize` and the
`load_summary_tests` module that pinned it, because `core/057` had already ported that arithmetic
verbatim into `embarch-core/src/outpost_load.rs`. **The arithmetic moved; three of its tests did
not.**
**Scope:** core
**Hardware:** none — a test module in a host-side Rust crate. No board, no probe, no live Core, no
deploy.
**Owner:** no

## What

`embarch-core/src/outpost_load.rs` has **8 tests**: a mismatched-column refusal, an empty capture, a
single uncontested thread's share, one gap's effect on `records_lost`/`gap_fraction`,
unnamed→named promotion, the row cap, a short-line refusal, and a real firmware capture.

**It has no counterpart for three behaviours `embarch-ui`'s deleted module pinned by name**, against
the identical logic:

| deleted test | what it pinned |
|---|---|
| `overlapping_gap_bands_are_counted_as_a_union` | overlapping gap bands merge into a union rather than double-counting the covered time |
| `idle_is_not_counted_twice` | the idle-record lane and the thread the manifest names idle are **not** added together |
| `subjects_are_sorted_by_measured_time` | the returned subject order |

**Add a test for each against `outpost_load.rs`.** They do not have to be ports — write whatever
pins the behaviour in this crate's own idiom.

## Why now, and why it is not urgent

**The logic was ported verbatim, so this is very unlikely to be a live bug.** It is a coverage gap,
not a defect: the behaviours are almost certainly correct today and nothing observable is broken.

**But two of the three are exactly the kind of thing that silently comes back.** The idle
double-count is documented in `embarch-ui/decisions/trace-view.md` as *"reported twice by
construction — found by building it, claimed by no other doc"*, and the whole reason it is written
down is that it is not obvious and was discovered the expensive way: a naive total over "threads plus
idle" claims nearly twice the window. **A behaviour that was found by building it, is counter-
intuitive, and is now untested is the one most likely to be re-broken by someone tidying the sum.**
The gap-band union has the same shape — it is the difference between a coverage figure that means
something and one that over-counts.

**And the sort order is the cheapest of the three**, worth doing in the same pass only because it is
one assertion.

## Watch for

- **Do not re-derive the expected values from the implementation.** That is how a test pins a bug.
  `embarch-ui`'s deleted module is in git history — `git log -p -- src/trace.rs` in `embarch-ui`
  around commit `87d01b4` — and its expectations were written against the behaviour when it was
  built, which is the better source.
- **`embarch-core/decisions/auth.md` is in reserve** (932 B left) and `tasks/core/046` is `blocked` on
  `In flux: yes`. A test module should not need it.
- **The outstanding native Windows build.** `core/015`'s debt now carries nine landed `embarch-core`
  changes. Tests add a tenth; say so in your report and **do not attempt a Windows build** — that is
  the owner's.

## Done when

- [x] `embarch-core/src/outpost_load.rs`'s test module covers all three behaviours above, each
      failing if the behaviour regresses.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment.

## Closed

Three tests added to `embarch-core/src/outpost_load.rs`'s existing `mod tests`:
`overlapping_gap_bands_are_counted_as_a_union`, `idle_is_not_counted_twice`,
`subjects_are_sorted_by_measured_time`. Expectations were taken from
`embarch-ui`'s deleted `load_summary_tests` (`git show 87d01b4^:src/trace.rs`
in `embarch-ui`), adapted to this crate's CSV-driven test idiom rather than
its fixture-based `stamped()`/`real()` views (this file has no such fixture
builder; a synthetic CSV pins the same behaviour). `merged_gap_extent`'s test
ported directly, since its simplified 2-field `Gap` already matches.

Each new test was verified to actually catch its regression, not just pass
vacuously: temporarily reverting `merged_gap_extent` to a naive sum broke
`overlapping_gap_bands_are_counted_as_a_union` (250 vs. expected 200), and
temporarily folding the `idle` kind into `thread_extent` broke
`idle_is_not_counted_twice` (200 vs. expected 100) once its assertion pinned
the exact split rather than only `thread_extent <= window_extent`. Both
mutations were reverted before the final commit.

Gate: `cargo build`, `cargo test` (208 passed, up from 205; 2 ignored,
unrelated), `cargo clippy --all-targets -- -D warnings` all clean in
`embarch-core`. `embarch-core` has no `Cargo.toml` below its root, so the root
gate is the whole gate. `scripts/check-docs.py` (11/11), `check-client-names.py
--repo`, and `check-ownership.py --scope core` / `--code-repo` all green (see
report). No `embarch-core` doc was touched, so `decisions/auth.md`'s reserve
status and `tasks/core/046` are unaffected. No native Windows build attempted
— `core/015`'s debt now carries a tenth landed `embarch-core` change (host-side
tests only, no behavior change to build).
