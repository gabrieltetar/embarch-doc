# 032 — `embarch-core/src` still cites a `design.md` this sub-project no longer has

**State:** claimed — leg 064

*Filed from `inbox/core-src-still-cites-a-design-md-embarch-core-no-longer-has.md` by leg 064,
2026-09-10; `Hardware: none` re-checked by the supervisor — a comment sweep over a Rust tree, no
board, no flash.*
**Source:** found by the supervisor in `core/008`'s fold, leg 063, 2026-09-10, while applying the
reviewer's citation finding — the very lines being repaired sat next to untouched `design.md`
citations
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-core/` holds `spec.md`, `open.md`, `decisions.md`, `decisions/` and
`interfaces/` — **there is no `design.md`**, and there has not been since the sub-project's docs were
split. `embarch-core/src` still cites it. One example, from `src/logs.rs`'s module header, three
lines away from a citation `core/008` did repair:

```rust
//! established shape (`embarch-topology/design.md` decisions 2/8/14) rather
//! than the CLI and HTTP paths growing separate copies of "find the current
//! log file." Moved out of `main.rs` unchanged (`embarch-ui/design.md` §3
//! decision 7) when the HTTP surface
```

That is two dead pointers in four lines, one of them cross-repo to `embarch-topology` and one to
`embarch-ui`, and `core/008` left both because its scope was `decision 48` and the `milestone-N.md`
references specifically.

## Why now

**This is the fourth instance of one class, and the first three all found more than their filed
count.** `study-designer/018` was filed for 290 occurrences in 23 files and landed 522 lines across
32. `api/052` was filed for 320 and found 160 — with **six real miscitations**, not merely dead
pointers, including two comments crediting `embarch-core` for `embarch-api`'s own decisions.
`umbrella/043` (leg 063, this same day) was filed for 68 and found **75**, with **four real
miscitations sharing one root cause**: `state.rs`, `setup.rs` and `deploy.rs` all credited umbrella
decision 37 (`reporting.md`, machine-readable check codes) for `deploy-core`'s subject, which is
decision 32.

`embarch-core` is the one remaining sub-project with a substantial Rust surface and no sweep, and it
is the repo the other three most often cite *into* — so a wrong bare number here is the failure mode
with the widest blast radius in the suite.

## The convention is settled — do not invent a second one

From `api/052`, adopted unchanged by `umbrella/043`:

> A same-repo citation drops both `design.md` and the section number and reads bare `decision M`,
> resolved against this repo's own `decisions/` index. A cross-repo citation drops `design.md`/`§N`
> too and adds the repo name as a plain qualifier before `decision`, e.g. `` `embarch-core` decision
> 22 `` — no repo-local section number, since none survived the split. A citation that named only a
> section, not a decision (`design.md §5`, `design.md §9`), was resolved to either the specific
> decision that section turned out to describe, or — where no decision covers it — that repo's
> `spec.md` (optionally with a section number, since `spec.md`'s own numbering is current). Where
> `embarch-ui` decision 10 is reused across three different topics in its own index
> (routing/trace/chart), the citation keeps that disambiguator, e.g.
> `` `embarch-ui` decision 10, routing half ``.

## Three things the earlier three sweeps paid for, so this one should not

- **Re-count over the whole tree, not `src/`, and do not trust any figure in this file.** Every
  filed count so far has been wrong in one direction or the other.
- **`sed` is the wrong tool.** Every citation you rewrite to the bare `decision M` form is asserting
  "this repo's own decision M", which silently absorbs a cross-repo number. That is 6 for 6 of
  `api/052`'s miscitations and 4 for 4 of `umbrella/043`'s.
- **Read the decision's *body*, not its heading, before you accept a number.** `core/008`'s fold hit
  this directly: `embarch-ui` decision 1 is titled "One consolidated process, not a shared library
  three separate binaries keep depending on" and reads like a packaging decision, and it is
  nonetheless the correct citation for Core's `/enroll` page retirement — because `shape.md`'s body
  says "Core's enroll page's HTML moves out of Core, which keeps the enroll endpoint it already had."
  A heading-only check would have rejected a correct citation, and the mirror of that mistake accepts
  a wrong one.

## Two things to leave alone

`umbrella/043` found and correctly left two look-alikes; expect the same class here.

- A **string constant** matched against real machines' files is data, not a citation. Changing one
  breaks existing installs.
- A **guard test** that asserts no production line names a deleted doc is the check, not a violation
  of it.

## Done when

- [ ] No occurrence of `design.md` remains in the `embarch-core` repo, counted by grep over the whole
      tree and not only `src/`.
- [ ] Each rewritten citation names a decision that exists **and** whose *body* matches what the
      comment claims — spot-check the substance, do not just re-point the path.
- [ ] Where a decision number is cross-repo, the repo is named explicitly as a plain qualifier.
- [ ] Any real miscitation found is reported separately from the mechanical ones — that distinction
      is the valuable half of this work.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/core-*` fragment.
