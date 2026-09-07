# `embarch-study-designer`'s doc comments link to a module that was retired

**State:** done, agent/study-designer/016-rustdoc-links-retired-module, 2026-09-07
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

- [x] The two `crate::validation` links name something that exists, or say in prose what they
      currently link to (Core's post-hoc validation, §3 decision 19) without a broken path.
      `src/schema_version.rs:59` and `:246` now say "Core's own post-hoc content validation
      (design.md §3 decision 19)" in prose, no link, since no `crate::validation` item exists to
      link to.
- [x] The three escaping warnings are resolved or deliberately left, said out loud. All three
      resolved, not left: `src/eap_interp.rs`'s `` [`embarch-dev-bench`] `` and `` [`Event`] ``
      became plain code spans (backtick-only, no brackets — both name things genuinely out of
      scope, not items this crate defines); `src/schema_version.rs:182`'s
      `` [`embarch-decision-reversals.md`][rev] `` had its stray `[rev]` reference-label removed
      so it resolves against the bare `[embarch-decision-reversals.md]: https://...` definition
      already present later in the same doc comment (the same pattern already used at line ~226
      of that file) — chosen over adding a `[rev]:` definition because the file already carries a
      working bare-reference convention for this exact string.
- [x] Decide whether `cargo doc` warnings belong in this sub-project's gate at all. **No.**
      Recorded as `embarch-study-designer` decision 68 in the new
      `embarch-doc/embarch-study-designer/decisions/ci.md`: a `-D warnings` rustdoc step is a
      real per-unit cost, this class of drift is rare and low-stakes once seen (a broken
      cross-reference, not a wire or behavior bug), and the fix here was by inspection in one
      sitting, not by CI. Reversal condition stated in the entry: if intra-doc rot starts
      recurring rather than showing up once every several months.

**`cargo doc --no-deps --all-features` warning count:** 5 before this unit (all pre-existing,
confirmed against `agent/study-designer/014-bleaddress-byte-order`'s head), **0 after**.

**Compaction note:** fixing decision 68 required writing to
`embarch-study-designer/decisions/crate.md`, which was in reserve
(`tasks/study-designer/006-compact-study-designer.md`, blocked on `In flux: yes`). Per that
task's own closing paragraph and `DOC-COMPACTION.md` §3, the compaction rode in this unit via
the mission split that task names as the cheaper move: `crate.md` keeps only the shape/boundary
decisions (1, 2, 5, 7, 8, 23); the CI mission (64, 65, and new 68) moved verbatim into
`decisions/ci.md`. `006`'s `Must not delete:` list survives untouched (a split moves text, it
does not restate it), and `006` stays `blocked` — only its `crate.md`-is-out-of-reserve item is
closed; the underlying in-flux content (dev-bench FFI staticlib cross-build absent) still blocks
a *shortening* pass on either resulting file. See `006`'s own updated `Done when` list.
