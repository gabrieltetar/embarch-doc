# 089 — consume `binary_sha256` in check 15, closing its same-version blind spot

**State:** open
**Source:** `embarch-umbrella/open.md`'s check-15 bullet, corrected by `tasks/umbrella/088`.
`embarch-core`'s `/status` now serves `binary_sha256` (`embarch-core` decision 68, citing
decision 67) — a lowercase-hex SHA-256 of the running Core binary's own bytes, cached once
at first request, `null` if the self-read fails.
**Scope:** umbrella
**Hardware:** verify-only
**Owner:** no

## What

Check 15 (`doctor.rs`'s `judge_core_build`/`check_core_build`, `embarch-umbrella` decision 34)
currently compares only `/status`'s `core_version` against the located `embarch-core` binary's
`--version` output — a comparison that is blind to a same-version stale deploy by construction
(`core_version` is `CARGO_PKG_VERSION`). Extend it (or add a companion check) to also hash the
*located* `embarch-core` binary on disk and compare that digest against the served
`binary_sha256`, closing the gap decision 34 names. This is a real behavior change and needs its
own decision entry in `embarch-umbrella/decisions/schema-skew.md` (or a new sibling topic file if
that one has no room — check `scripts/check-doc-size.py --pressure` first, it is already
94.0%/733 B left and blocked on `tasks/umbrella/009`).

Open questions to settle while implementing, not asserted here:

- Whether a same-version mismatch is a `Warn` (consistent with decision 13's "consumers warn,
  never refuse") or something stronger, given it is now a *positive* content disagreement rather
  than an unmeasurable gap.
- Whether hashing the located binary on every `doctor` run is cheap enough to always do, or
  whether it should be gated (e.g. only attempted when `core_version` already matched, since a
  version mismatch already fails/warns on its own and a same-version content hash only adds
  information in the matching case).
- What `AuthedStatus` needs to carry to make the comparison a pure, testable function the way
  `judge_core_build` already is (see `embarch-umbrella` decision 34's closing note: "a test
  asserts the blind spot rather than leaving it to the prose" — a new test should assert the
  *closed* case).

## Why now

Not urgent — check 15 already warns rather than fails, and the cross-version case it does catch
remains the common one. Filed so the gap `embarch-umbrella/open.md`'s check-15 bullet names has a
tracked home now that the field it needs exists, rather than the bullet re-growing prose about a
field embarch-core hadn't built yet.

## Done when

- [ ] `judge_core_build` (or a new check) compares `binary_sha256` when both sides have one,
      narrowing or eliminating the "blind to a same-version stale deploy" limit decision 34 states.
- [ ] A decision entry recording the choice (warn-level, when the hash is attempted, what a
      missing/`null` hash on either side means).
- [ ] `embarch-umbrella/open.md`'s check-15 bullet updated once this lands (retire or rewrite,
      not append).
- [ ] Unit tests covering: both hashes present and equal, both present and unequal, either side
      `null`/absent (pre-decision-67/68 Core, or a local binary whose own read failed).
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`,
      `scripts/check-docs.py`, `scripts/check-ownership.py --scope umbrella`).
