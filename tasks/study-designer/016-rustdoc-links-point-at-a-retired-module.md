# `embarch-study-designer`'s doc comments link to a module that was retired

**State:** claimed by agent/study-designer/016-rustdoc-links-retired-module, 2026-09-07 09:30
**Source:** worker on `tasks/study-designer/014`, leg 026, 2026-09-06 — noticed while running
`cargo doc --no-deps --all-features` to confirm the new `BleAddress` intra-doc links resolved.
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`cargo doc --no-deps --all-features` on `embarch-study-designer` at
`agent/study-designer/014-bleaddress-byte-order` emits **5 `rustdoc::broken_intra_doc_links`
warnings**, all pre-existing (none from unit 014). Two of them are the interesting ones:

- `src/schema_version.rs:59` — ``/// [`crate::validation`], to `Study.requires`, or to any other
  host-side-only`` → *no item named `validation` in module `embarch_study_designer`*
- `src/schema_version.rs:246` — ``/// never sees: [`crate::validation`], `Study.requires`,
  `Study.gatt`.`` → same

There is no `crate::validation` module. Post-hoc content validation was moved to Core
(design.md §3 decision 19) and the shape §3 decision 54 retired is named in `src/result.rs:229`.
So two doc comments still cite a module by path that this crate does not have — a reader
following the link to find out what the schema version deliberately excludes lands nowhere.

The other three are cosmetic escaping, not stale facts, and are listed only so a fixer is not
surprised by them:

- ``[`embarch-dev-bench`]`` in the `eap` module preamble — a repo name in link brackets
- ``[`Event`]`` in the same area — an `Event` type that is not in scope there
- `src/schema_version.rs:182` — ``[`embarch-decision-reversals.md`][rev]`` with no `[rev]:`
  definition anywhere in the comment

## Why now

**`cargo doc` is not in the gate.** `../embarch-fleet/protocol.md` §10 runs `build`, `test` and
`clippy --all-targets -- -D warnings`; none of them evaluate intra-doc links, so this class of
staleness is invisible to every green run. That is the same shape as the finding unit 014 closed
— a doc claim nothing checks — one layer over.

### Why this is a drop and not a fix

In scope for `study-designer` but outside `tasks/study-designer/014`, whose whole instruction was
to state one byte order and stop. Filing rather than widening the unit.

## Done when

- [ ] The two `crate::validation` links name something that exists, or say in prose what they
      currently link to (Core's post-hoc validation, §3 decision 19) without a broken path.
- [ ] The three escaping warnings are resolved or deliberately left, said out loud.
- [ ] Decide whether `cargo doc` warnings belong in this sub-project's gate at all. **A `-D
      warnings` rustdoc step is a real cost on every unit** and this is 5 warnings in one file,
      so "no, and the doc comments get read by a human instead" is a legitimate answer — but it
      should be an answer, not a gap.
