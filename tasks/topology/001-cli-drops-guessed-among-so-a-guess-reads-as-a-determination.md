# Print `guessed_among` in the topology CLI's `dev-bench` output

**State:** done, agent/topology/001-guessed-among, 2026-09-06
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

- [x] `embarch-topology dev-bench` renders the guess on the port-name line when `guessed_among` is
      set, and is byte-for-byte unchanged when it is not.
- [x] The rendering lives in a testable function, with tests for both cases.
- [x] The `validate` arm prints `NotEnrolled`'s `Display` and still exits non-zero.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), including `cargo test --features bin`.
- [x] `spec.md` updated, `changelog.d/` + `features.d/` fragments dropped. No `status.d/` fragment:
      no suite-level doc states anything this made false (checked `embarch.md`, `suite/roadmap.md`,
      `suite/user-guide.md`, the glossary and the reversals index).

## Notes from the doing

**The rendered string is `COM16, guessed among 2`, not `COM16 (guessed among 2)`.** This task's box
asked for the parenthesised form, but **two canon docs state the comma form verbatim** —
`spec.md`'s "Storage and roles" and decision 20's closing paragraph — and a decision record's quoted
example is worse to rewrite than a task's paraphrase is to follow loosely. The behaviour asked for is
unchanged; only the punctuation differs.

**The line numbers in `## What` above were stale.** `bin/main.rs` is 161 lines, not 530; the arms are
at `DevBench` and `Validate` by name. Nothing else in the description was wrong.

**Hardware-verification debt.** `guessed_among` has still never been observed set on a bench —
`spec.md` says so, and this change does not alter that. Its trigger is an *under-declared* bench, so
seeing this rendering live means **deliberately clearing the dev-bench link interface**
(`embarch-topology set-dev-bench-link --interface` has no unset, so it means editing the enrollment
file), running `embarch-topology dev-bench` on the Core host with the nRF54L15DK attached, and
restoring interface 2 afterwards. Until then the guessed shape is unit-tested only, and the
`features.d` row says exactly that. **Do not run it casually**: the restore step is what keeps the
bench working, per decision 20.

**`validate`'s exit path is unverified end-to-end** — `render_error` is unit-tested against all three
error shapes, but nothing here ran the binary, so the `exit(1)` is unchanged code taken on trust.
