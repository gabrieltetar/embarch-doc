# 001 — No repo in the suite asserts `Cargo.toml` version against its pushed tag, though a decision says every one does

**State:** open — **window closed, cleared to run, not started.**
`embarch-parallel-agents-ops.md` §4. Announced in `#embarch-fleet`
(`C0BUKTL2FPC`) at ts `1788460873.097499`, 2026-09-03 12:41 MDT, by the leg that
filed it. **Leg 006 completed that window** at 13:11 MDT: read the thread, zero
replies, 30 minutes elapsed. So the announcement obligation is discharged — **do
not re-announce and do not restart the clock.** Leg 006 did not execute it
because a `fleet stop` arrived in the same minute and a stop dispatches nothing
new. The next supervisor to run may execute this directly as a unit.
**Source:** embarch-umbrella/002 (design-only decisions audit, 2026-09-03) — decisions 27/29 read against the source and found unbuilt everywhere
**Scope:** suite
**Hardware:** none

## What

`embarch-umbrella` decisions 27/29 (one decision, two numbers) say: "Every repo's
release workflow now asserts the two agree *before building any target*, failing
the release outright rather than shipping a binary whose `--version` disagrees
with the tag that produced it."

**No repo does this.** `embarch-umbrella`'s own `.github/workflows/release.yml`
goes tag push → checkout → toolchain → `cargo build` → package → upload with no
step that reads `Cargo.toml`'s version or `GITHUB_REF_NAME`. A read-only check of
`embarch-core`, `embarch-api` and `embarch-topology` found the same absence;
`embarch-study-designer`, `embarch-dev-bench`, `embarch-outpost` and `embarch-ui`
have no release workflow at all.

Add one step at the top of each existing release workflow, before the build
matrix does any work: parse the crate version, compare against the tag with the
`v` stripped, fail the job on a mismatch.

**This is suite scope, not umbrella scope** — it touches four repos. Filed here
rather than done by `umbrella/002`, which owned one of them and was a
build-nothing audit besides.

## Why now

The decision was prompted by a real drift that shipped: a `Cargo.toml` had moved
away from its `v0.1.1` tag and was caught only because someone compared
`--version` against the tag by hand that day. `doctor`'s check 1 compares binary
versions against the suite manifest and therefore **inherits** this gap — it can
only detect a mismatch the release process was supposed to make impossible.

## Done when

- [ ] `embarch-umbrella`, `embarch-core`, `embarch-api` and `embarch-topology`
      release workflows each fail before building when `Cargo.toml`'s version and
      the pushed tag disagree.
- [ ] Verified by a deliberate mismatch on a throwaway tag, or by whatever
      cheaper evidence the implementer can actually produce — **say which.**
- [ ] The implementation note under `embarch-umbrella` decisions 27/29 updated to
      say it shipped, and by what date.
- [ ] `status.d/` fragment for the `suite/features.md` row this creates.
- [ ] Gate green in every repo touched; `changelog.d/` fragment dropped.
