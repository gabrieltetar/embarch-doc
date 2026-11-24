# 101 — One study walkthrough, and the human guides link the HIL guide

**State:** done — edit set delivered as status.d/doc-one-study-walkthrough.md; hil-guide.md untouched; guides applied at the fold
**Source:** the 2026-11-23 suite audit — `suite/studies-guide.md` and `suite/hil-guide.md` teach the same study material, and neither `user-guide.md` nor `agent-guide.md` links the HIL guide
**Issue:** EMB-316
**Scope:** doc
**Hardware:** none
**Owner:** no

## What

`user-guide.md` §9 sends a newcomer to `studies-guide.md` only, which opens "not
a tutorial you can follow end to end" and carries one bench's measured
addresses, study ids and probe serials. The runnable worked example and the
trust rules live in `hil-guide.md`, served by `embarch-api guide hil` and the
installed skill; neither `user-guide.md` nor `agent-guide.md` mentions
`guide hil`. The reflash semantics, the truncation warning, the MSB-first
address rule and the census-by-failed-`BleConnect` advice appear in both guides
in prose.

When this is done: `agent-guide.md` and `user-guide.md` §9 point at
`embarch-api guide hil` (and `hil-guide.md`); `studies-guide.md` §1 to §2
shrink to a pointer plus the bench and trace material; and the duplicated lore
lives once, **in `hil-guide.md`**, with `studies-guide.md` linking to it.
Planned Live and Test work is out of scope.

## Why now

A newcomer is sent to the guide that is not a tutorial, and the one that is
can only be found by already knowing it exists (EMB-316).

**How this unit lands — read before writing anything.** None of the four
guides is writable by a `doc` worker (`check-ownership.py --scope doc` allows
`embarch-doc/embarch-doc/**`, `tasks/doc/**` and the fragment directories).
So, as `doc/100` did: work out the exact edits and deliver them as
**`status.d/doc-one-study-walkthrough.md`**, one block per target file, each
quoting the text it replaces and giving the replacement verbatim. I apply them
at the fold. Check every fact you move against the code, as `doc/100`'s worker
did.

**Do not change `suite/hil-guide.md`.** `embarch-api` compiles a pinned copy
of it (`guide/hil-guide.md`) and its `tests/guide_cli.rs` fails when the two
differ, so an edit here turns another repo's gate red. Where `hil-guide.md`
already states a piece of lore, delete the `studies-guide.md` copy and link to
it; where only `studies-guide.md` states it, it stays there. If the work cannot
be done without editing `hil-guide.md`, say so in this file and stop.

**Sizes (dispatch note):** `suite/user-guide.md` is 22,948 B, **92 B under**
its reserve line; the §9 pointer must not grow it past that, so replace the
existing "Testing against a second board?" sentence rather than adding one.
`suite/studies-guide.md` is 23,029 B, 11 B under its line; this unit should
shrink it. `agent-guide.md` is 4,399 B.

## Done when

- [x] The fragment's edits give `agent-guide.md` and `user-guide.md` §9 a
      pointer to `embarch-api guide hil` and `hil-guide.md`.
- [x] After them, the reflash, truncation, MSB-first address and census lore
      each appears in one guide.
- [x] `studies-guide.md` §1 to §2 are a pointer plus the bench and trace
      material, and the file ends smaller than it started.
- [x] `suite/hil-guide.md` unchanged.
- [x] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment dropped.
