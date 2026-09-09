# 021 — Two `decisions.md` files record a per-push CI that has never existed, in the two sub-projects the merge gate cannot reach either

**State:** open — **announced and parked, window running.**
**Announced:** 2026-09-08, leg 051, `#embarch-fleet` ts `1788917508.792199`
(posted 19:31 MDT). Per `embarch-fleet/ops.md` §4 this runs as a leg's **last**
unit, and only if no objection has arrived and **30 minutes** have passed since
that timestamp. **If leg 051 ends before the window closes, do not restart the
clock** — poll `slack_read_thread` on that `ts` and execute against the original
announcement. Intended direction as announced: retire both CI claims and state in
one place what actually checks each sub-project; do **not** build the missing
`native_sim` job.
**Source:** suite review pass 2026-09-06, dimension 3 (one philosophy). Code-confirmed by `find .github` and `git log --all` across all eight repos.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

Two decision records claim a CI that does not exist and never has.

- `embarch-core/decisions/platform.md:12-13`, in the decision headed *"1, 2, 7, 17 — Rust,
  probe-rs as a library, Axum, `spawn_blocking`, and **CI everywhere**"*: *"**CI runs
  `build`/`clippy -D warnings`/`test` per push on every repo that lacked it, plus a `native_sim`
  build for dev-bench**, which would have caught a real Zephyr API breakage before it was found by
  hand."*
- `embarch-dev-bench/decisions/platform.md:25-26`, decision 9 — *"CI, reversing 'no CI for
  now'"*: *"Superseded: a `west build -b native_sim app` job is worth having with one board … and
  would have caught a real Zephyr BLE API breakage before it was found by hand."*

Measured: `embarch-study-designer/.github/workflows/test.yml` and
`embarch-topology/.github/workflows/{test,release}.yml` are the **only** test/build workflows in
the suite. `embarch-api`, `embarch-core` and `embarch-umbrella` have `release.yml` only.
`embarch-dev-bench`, `embarch-outpost` and `embarch-ui` have **no `.github` directory at all**,
and `git log --all -- '.github/**'` in `embarch-dev-bench` and `embarch-ui` returns nothing —
neither repo has ever had one.

`suite/features.md` carries no row claiming per-push CI outside `embarch-study-designer`'s feature
matrix, so the honesty ledger is right and the two decisions are not.

Candidate direction: either build the `native_sim` job dev-bench decision 9 records, or retire and
amend both clauses to say what actually checks each sub-project — and state plainly that the two C
sub-projects have no mechanical check at all.

## Why now

This is `embarch-decision-reversals.md` shape 1 — *"documented as implemented, wasn't … the single
most common shape here, and it survives every kind of test suite"* — landing on the decision
records themselves, which that index already names as the worse variant: *"an amendment that reads
as shipped is indistinguishable from one that is."* And it matters most where it is least true:
the two sub-projects with no `Cargo.toml` are exactly the two the fleet's merge gate cannot reach
either. `check-decision-refs.py` resolves the reference and `check-doc-conventions.py` reads the
shape; neither can ask whether a workflow file exists.

For contrast, the suite *can* write this down when it notices:
`embarch-umbrella/decisions/release.md:48-51` is scrupulously honest about the four repos with no
release workflow.

## Done when

- [ ] Neither `decisions/platform.md` claims a CI that does not run.
- [ ] What actually checks each sub-project before a change lands is stated in one place, and the
      two sub-projects with no mechanical check say so.
- [ ] Gate green; `changelog.d/` fragments for both repos.

**Constraint for whoever takes it:** the replacement fact lives in
`embarch-fleet/protocol.md` §10, which is **owner-reserved and read-only here**. Cite it; never
edit it.
