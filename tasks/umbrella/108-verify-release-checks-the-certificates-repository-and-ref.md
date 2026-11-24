# 108 — verify-release checks the certificate's repository, ref and build config

**State:** open
**Source:** `embarch-release-signing-proposal.md` — "Still proposed: checking the certificate's source-repository and ref extensions against that identity too"
**Issue:** EMB-343
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`embarch verify-release` (`src/verify_release.rs`) checks the issuer and one
exact identity built from the manifest's version. When this is done it also
reads the leaf certificate's Source Repository URI, Source Repository Ref and
Build Config URI extensions (the provider-generic ones, from OID
`1.3.6.1.4.1.57264.1.8` on) and requires, as exact strings and never a
pattern: the repository URI is the umbrella repository the identity names; the
ref is `refs/tags/suite-v<version>`; the build config URI equals the identity.
A missing extension fails and names it; a value that differs fails and names
the extension, the expected value and the found one. So a bundle whose
identity matches but whose extensions name another repository or ref fails.

## Why now

The elevated install trusts what `verify-release` accepts, and the proposal
still lists this check as proposed (EMB-343). The issue notes the owner may
strike this unit; it is in Fleet Ready, so it runs.

**Burndown leg: no new numbered decision.** Say what is checked in
`interfaces/verify-release.md`; if a decision needs a sentence, amend the one
that owns `verify-release` in place. If the work genuinely needs a new
decision, stop and say so in this file.

**Doc-size reserve (dispatch note):** `embarch-umbrella/spec.md` is in reserve
(9,161 of 10,240 B, 1,079 B left) and its compaction, `tasks/umbrella/107`, is
parked on `In flux: yes`. This unit should not need `spec.md`; if it does, keep
the edit inside the headroom and say so. Umbrella decisions near their
per-decision cap: prune-policy#26 (19 B), deploy#32 (29 B), mirrors#20 (32 B),
probe-vendors#49, sticky-host#48, budgets#44; none is this task's.

## Done when

- [ ] Against a fixture bundle in `tests/fixtures/`, the three extensions are
      read, and a test asserts their values.
- [ ] An expected value that differs from the certificate's fails, naming the
      extension; a certificate without one of them fails, naming it.
- [ ] `interfaces/verify-release.md` says what is checked.
- [ ] A `status.d/` fragment asks the supervisor to remove the proposal's
      "still proposed" line in `embarch-release-signing-proposal.md`, which a
      worker may not edit.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped.
