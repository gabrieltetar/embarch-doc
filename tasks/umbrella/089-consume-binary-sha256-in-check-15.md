# 089 — consume `binary_sha256` in check 15, closing its same-version blind spot

**State:** done
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

## Dispatch note (supervisor, 2026-09-28)

**One correction to the paragraph above: `decisions/schema-skew.md` is not in reserve.** It is
7,469 / 12,288 B, room for a decision. The "94.0% / 733 B left, blocked on `tasks/umbrella/009`"
figures belong to `decisions/bind.md`. Put the decision where its mission is — schema-skew.md
already holds 34, the decision this narrows — and check `python3 scripts/check-doc-size.py
--pressure` after, not before.

**The three open questions are yours to settle, and the decision records the answer and what was
rejected.** Two constraints bound them. `embarch-core` decision 13 ("consumers warn, never refuse"), which this repo's
decision 34 already follows, stands unless
the decision says why a positive content disagreement differs from an unmeasurable gap — do not
change a check's severity without that argument written down. And **no hardware, no live Core**:
`Hardware: verify-only` means the host-side change ships with pure-function unit tests on
`judge_core_build` (or its companion), and the real-machine confirmation — one `doctor` run
against the installed Core — is written as a hardware-verification debt in this file, not
attempted. Read `embarch-core` decision 68 (`embarch-core/decisions/surfaces.md`) for exactly what the served field is (when it is
computed, what `null` means) rather than inferring it from the name.

**Also in reserve in `umbrella`, not yours to write:** `decisions/install.md` 217 B left
(`tasks/umbrella/079`, blocked), `decisions/bind.md` 733 B left (`tasks/umbrella/009`, blocked),
`decisions/projects.md` 1,172 B left (`tasks/umbrella/084`, blocked). `open.md` left reserve one
unit ago (3,905 B, `umbrella/088`) — retiring or rewriting its check-15 bullet must not push it
back in; if your work pushes any `umbrella` file into reserve, file
`tasks/umbrella/<NNN>-compact-docs.md` in the same commit.

## Done when

- [x] `judge_core_build` (or a new check) compares `binary_sha256` when both sides have one,
      narrowing or eliminating the "blind to a same-version stale deploy" limit decision 34 states.
      Extended `judge_core_build` in place (not a new check number) with two more parameters,
      `served_sha256`/`located_sha256`; the comparison only runs once `core_version` already
      matches (open question 2 settled: gated on a version match, not attempted on every run).
- [x] A decision entry recording the choice — `embarch-umbrella` decision 56
      (`decisions/schema-skew.md`): still Warn, never Fail, even on a hash mismatch (decision 13 and
      decision 24 stand — "more actionable" is not "must refuse"); the located binary is hashed only
      when `core_version` already matched; a missing hash on either side silently falls back to the
      old version-only verdict rather than its own new warning. Decision 34's own text amended with a
      pointer, not deleted.
- [x] `embarch-umbrella/open.md`'s check-15 bullet updated once this lands (retire or rewrite,
      not append). Rewritten to name the two-run hardware debt below instead of the now-closed "not a
      hash comparison" gap. That rewrite pushed `open.md` back into reserve (4,048/5,120 B, 79.1%) —
      filed `tasks/umbrella/090-compact-docs.md` in this same commit per the dispatch note's
      instruction.
- [x] Unit tests covering: both hashes present and equal, both present and unequal, either side
      `null`/absent (pre-decision-67/68 Core, or a local binary whose own read failed).
      `matching_hashes_on_a_matching_version_close_the_blind_spot`,
      `mismatched_hashes_on_a_matching_version_warn_as_a_same_version_stale_deploy`,
      `a_missing_local_hash_falls_back_to_the_version_only_verdict`,
      `a_missing_served_hash_falls_back_to_the_version_only_verdict`, plus
      `a_cross_version_mismatch_warns_the_same_way_even_with_hashes_present` pinning that a version
      disagreement ignores the hashes entirely.
- [x] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`,
      `scripts/check-docs.py`, `scripts/check-ownership.py --scope umbrella`).

## Hardware-verification debt

**Not attempted here** — no hardware, no live Core, per this task's own `Hardware: verify-only` and
the dispatch note. Confirmed only against literals in `judge_core_build`'s unit tests. What still
needs a real machine, recorded in `embarch-umbrella/open.md`'s rewritten check-15 bullet:

1. One `doctor` run against the installed Core, same version, same binary, confirming a real match
   renders the new closed-gap Pass (`"matching the located binary bit-for-bit"`).
2. One `doctor` run against a deliberately stale same-version reinstall (rebuild the same tag,
   redeploy only half of it, or similar) confirming the new same-version-stale-deploy Warn actually
   fires and its fix line reads sensibly.

Tracked as an open item in `embarch-umbrella/open.md`, not as a separate task file — the pattern
check 13's `umbrella/034` bullet and decision 51's sticky-host bullet already use for a
fixed-but-unverified item.
