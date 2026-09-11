# 028 — The four unrendered protocol primitives produce a wrong layout instead of a named refusal

**State:** open
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

- [ ] Rendering a frame that uses `repeat`, `bitpack`, `crc32` or `fixed` returns an explicit
      unsupported/not-implemented error that names the primitive, rather than a layout.
- [ ] One test per primitive pins that error.
- [ ] `embarch-study-designer/open.md:20` narrows to "the render half is still deferred, and asking
      for it now says so".
- [ ] `open.md` is at 4,649/5,120 B — **in reserve, 471 B left**, with
      `tasks/study-designer/026-compact-study-designer.md` parked against it. If your edit leaves it
      in reserve, that task already exists; do not file a second one.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes false.
