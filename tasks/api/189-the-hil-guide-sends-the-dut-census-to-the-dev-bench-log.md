# 189 — The HIL guide sends the DUT census to the dev-bench log

**State:** open
**Source:** `suite/studies-guide.md` §3a — `fail_reason` is capped and lists only advertisers that sent a name; the HIL guide's Study 1 offers it as a census beside `dev-bench.log`
**Issue:** EMB-402
**Scope:** api
**Hardware:** none
**Owner:** no

## What

The HIL guide's Study 1, the `steps` bullet, tells an agent to find the DUT's
address by reading "the census in its `fail_reason` and in `dev-bench.log`", as
equals. `suite/studies-guide.md` §3a measured that `fail_reason` is capped at
64 bytes and lists only advertisers that sent a name (10 on air, 2 named), so a
DUT with no name never appears there; `dev-bench.log` is the complete census.

When this is done the sentence says to read the census in `dev-bench.log`, and
that a `fail_reason` with no plausible DUT in it is not evidence the DUT is off
the air. Keep it to the one bullet; the HIL guide is embedded in the binary and
read whole by an agent.

**Two copies, one edit.** The guide lives in `embarch-doc/suite/hil-guide.md`,
which a worker may not write, and in this repo's pinned copy
`guide/hil-guide.md`, which `tests/guide_cli.rs` compares byte for byte with a
reachable `embarch-doc` (`EMBARCH_DOC_DIR`, else a sibling). So:

- Edit `guide/hil-guide.md` here.
- Write a `status.d/api-*` fragment on the doc branch quoting the old bullet and
  the new one exactly, so the supervisor applies the same bytes to
  `suite/hil-guide.md` in the fold.
- Run the drift guard against a scratch copy holding your edit: copy the doc
  worktree's `suite/hil-guide.md` to `<scratch>/suite/hil-guide.md`, apply the
  same edit there, and run `EMBARCH_DOC_DIR=<scratch> cargo test --test
  guide_cli`. Without the variable the test reads the sibling link, which is
  the owner's unedited checkout, and fails by design.

## Why now

The guide is what an agent reads before its first study (EMB-402, found by
`doc/101`). An agent following it can conclude a nameless DUT is not
advertising.

**Burndown leg: no new numbered decision.** None should be needed.

## Done when

- [ ] `guide/hil-guide.md` carries the corrected bullet and nothing else changed.
- [ ] A `status.d/` fragment gives the supervisor the exact old and new bullet
      for `suite/hil-guide.md`.
- [ ] `cargo test` green, with the drift guard run against the scratch copy as
      above.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped.
