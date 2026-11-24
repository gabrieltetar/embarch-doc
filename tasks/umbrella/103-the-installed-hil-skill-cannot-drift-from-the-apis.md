# 103 — The installed HIL skill cannot drift from the api's

**State:** claimed by agent/umbrella/103-the-installed-hil-skill-cannot-drift-from-the-apis, 2026-11-24 03:19
**Source:** suite review audit, 2026-11-23: umbrella's pinned `embarch-hil` skill lags the api's copy
**Issue:** EMB-315
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`embarch-umbrella/src/skills/embarch-hil/SKILL.md` is a pinned copy of
`embarch-api/skills/embarch-hil/SKILL.md`, embedded by `include_str!` in
`src/init.rs` and written into a repo by `embarch init`. The two differ today
at lines 25 and 30: the api's copy sends the reader to the shared part of
`embarch-api guide hil` first (what every mode shares, what you are trusted
with, what you never do), and the pinned copy drops that. Decision 59
(`embarch-doc/embarch-umbrella/decisions/integration.md`) accepted the lag and
named its guard, a unit test that panics on drift when the sibling checkout
exists; an api change never runs umbrella's tests, so the api edit of
2026-11-23 drifted with nothing failing.

When this is done:

- A repo that runs `embarch init` gets exactly the api's skill text.
- Drift cannot recur silently. **Preferred:** the installer reads the one
  file — `include_str!` the api's `skills/embarch-hil/SKILL.md` through the
  same sibling path the crate already depends on
  (`../embarch-api/crates/embarch-core-client` in `Cargo.toml`, and
  `build-check.yml` checks `embarch-api` out beside it), and delete the copy.
  Check first that every build of umbrella (local, `build-check.yml`,
  `release.yml`, `assemble-suite.yml`) has that sibling; if one does not,
  fall back to re-pinning the copy and say in this file why, so the
  supervisor can file the api-side drift check (a test in `embarch-api`,
  which this task cannot write).
- Decision 59 is amended in place to say which of the two it now is.

## Why now

A repo that ran `init` after 2026-11-21 has the older skill, which skips the
trust rules the api's version tells an agent to read first. EMB-315.

**Burndown leg: no new numbered decision.** Amend decision 59 in place; if
the change seems to need a new one, stop and say so in this file.

**Doc-size reserve (dispatch note):** no `embarch-umbrella` file is in
reserve. Decisions near their per-decision limit: prune-policy#26 19 B,
deploy#32 29 B, mirrors#20 32 B, probe-vendors#49 140 B, sticky-host#48
186 B, budgets#44 200 B. Decision 59 is not among them.

## Done when

- [ ] The skill `embarch init` writes is byte-identical to
      `embarch-api/skills/embarch-hil/SKILL.md` on `main`, and a test says so.
- [ ] Either the copy is gone (installer reads the api's file), or it is
      re-pinned and this file says why the preferred route was not possible.
- [ ] Decision 59 amended in place.
- [ ] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
      green in `embarch-umbrella`.
- [ ] `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
