# 028 — The four unrendered protocol primitives produce a wrong layout instead of a named refusal

**State:** done — leg 076, worker on `agent/study-designer/028-primitives-fail-loudly`

## Finding: the premise was partly wrong

The renderer was read before anything was written, per the dispatch note. `open.md:20`'s own text
("a missing consumer") was already correct; the corrupted framing was in this task's own title and
`## What`, which claimed a **flat layout with wrong numbers** for all four. What `lower_layout` in
`src/eap_parse.rs` actually did, before this change:

- **`bitpack`, `crc32`, and `repeat` with `count_from`** (`src/eap_parse.rs`, the `_ => return None`
  catch-all, pre-change) produced **no layout at all** — the frame silently vanished from
  `struct_layouts()`, not a wrong flat one.
- **`repeat` with a literal count** (`AstField::Repeat { count: AstCount::Literal(_), .. }`, same
  file) already rendered correctly — this variant is not broken and needed no change.
- **`fixed`** (`src/eap_parse.rs`, the old `let _ = fixed;` line in the field-lowering loop) was the
  one genuine case matching the title: the scalar was carried through as a bare integer, silently
  dropping the scale — a plausible wrong number with no marker.

All four still "fail silently" in the sense the title cares about (no named error reaches a
caller), so the task proceeded as scoped, narrowed to what was actually true.
**Source:** `embarch-study-designer/open.md:20` — parse is pinned per primitive, but "the
bit-unpacker, the counted walker and the CRC check are the render half, and are not written".
Surfaced by leg 076's refill sweep. **The claim is doc-sourced; the renderer was not read.**
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`repeat`, `bitpack`, `crc32` and `fixed` parse — each is pinned by its own test — and then render
as though they were not there, producing a flat layout rather than an error. Make asking for one of
them say so.

**Read the renderer before writing anything**, and if the behaviour is not what `open.md` describes,
say that in this file and close the task on that finding — a corrected `open.md` bullet is a good
outcome. This repo's own standing rule applies with full force here: a rendering that silently
produces a plausible wrong layout is
[embarch-decision-reversals.md](../../embarch-decision-reversals.md)'s "a guess indistinguishable
from an answer", and it is the exact failure the crate's `SampleLayout` doc comment refuses on the
scaling/offset question one layer up.

**Implementing the render half is not what this asks for.** The four primitives are deferred on
purpose; the defect is that the deferral is silent. An explicit unsupported error naming the
primitive is the whole change.

## Why now

A decoder that returns a flat layout for a bitpacked frame returns numbers — wrong ones, with no
marker anywhere that they are wrong. Nothing in the suite can catch that downstream: the CSV parses,
the values are in range, and the only evidence is a DUT engineer noticing the figures are nonsense.

## Done when

- [x] Rendering a frame that uses `repeat` (`count_from`), `bitpack`, `crc32` or `fixed` returns an
      explicit unsupported/not-implemented error that names the primitive, rather than a layout —
      `ResolvedProtocol::render_layout(frame)` (`src/eap_parse.rs`), new `EapErrorKind::RenderUnimplemented`.
      `struct_layouts()` is unchanged (nothing in-repo calls it); this is an additive, loud
      alternative next to it. Literal-count `repeat` (already correct) is unaffected.
- [x] One test per primitive pins that error, plus a control test that the ordinary flat case still
      renders — `src/eap_parse.rs` `mod tests`, the five tests ending in
      `a_flat_frame_with_no_deferred_primitive_still_renders`.
- [x] `embarch-study-designer/open.md:20` narrowed — see the diff; states the gap is now a named
      refusal (`render_layout`, task 028) rather than a silent one, and corrects `repeat` to name
      only its `count_from` form.
- [x] `open.md` dropped 4,649 → 4,569 B, still in reserve; `026-compact-study-designer.md` stays
      the only compaction task against it, unchanged.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build`, `cargo test`,
      `cargo test --features eap-parse` (the new tests are behind that feature), and
      `cargo clippy --all-targets -- -D warnings` all clean in the code worktree.
- [x] `changelog.d/study-designer-render-primitives-refuse-loudly.fixed.md` added. No `status.d/`
      fragment: nothing suite-level changed — `render_layout` has no consumer in this repo or
      documented elsewhere in this crate's own interfaces docs yet. Decision 71 recorded in
      `decisions/protocols.md` (index row updated in `decisions.md`).
