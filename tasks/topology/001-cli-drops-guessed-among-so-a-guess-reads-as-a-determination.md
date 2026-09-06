# Print `guessed_among` in the topology CLI's `dev-bench` output

**State:** open
**Source:** `embarch-topology/spec.md:70` — "a caller reports 'COM16, guessed among 2' rather than 'COM16'"
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`bin/main.rs:523-530` prints `detected_by`, `serial`, `product` and `interface`, and never
`guessed_among` — so the CLI reports a guessed port exactly as it reports a determined one.
`spec.md:70` states the intended behaviour verbatim, and `src/hardware/port.rs:88-101` records that
the field exists precisely because "the guess used to be invisible".

The `validate` arm at `bin/main.rs:550-560` also prints `{e:?}` for a `NotEnrolled`, whose `Display`
(`src/hardware/validate.rs:175-184`) is the human sentence.

The rendering goes in a small pure function so it is unit-testable without a probe.

## Why now

Decision 20 is explicit that the invisible guess is what made the nRF54L15DK failure expensive — "a
bench that flashed, booted, ran, and timed out". The field exists, and the crate's own CLI is the
caller that drops it.

## Done when

- [ ] `embarch-topology dev-bench` renders "COM16 (guessed among 2)" when `guessed_among` is set,
      and is unchanged when it is not.
- [ ] The rendering lives in a testable function, with tests for both cases.
- [ ] The `validate` arm prints `NotEnrolled`'s `Display` and still exits non-zero.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including `cargo test --features bin`.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
