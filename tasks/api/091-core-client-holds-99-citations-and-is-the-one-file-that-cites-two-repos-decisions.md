# 091 — `embarch-core-client/src/client.rs` holds 99 citations and is the one file that cites two repos' decisions

**State:** claimed by agent/api/091-client-rs-citations, 2026-09-13 20:00
**Source:** the leg of 2026-09-13 18:3x, counting every repo's source citations while filling the
queue. **Filed as `089` and renumbered to `091` at 19:2x by the leg that filed it.** `api/088`'s
worker independently filed its own reserve task as `089` from a branch cut before the refill commit
landed, so two files claimed one number and both are in history —
`check-task-numbers.py` flags a number the tree holds whose history carries a different slug, so
`089` is burned and neither file may keep it. The worker's went to `090`, this one to `091`.
Nothing about either task changed. `embarch-api` carries **297** `decision[s] N` lines across `src/`, `crates/` and `tests/` —
the second-largest source citation surface in the suite after `embarch-study-designer` — and **no
sweep of it has ever been filed or run.** `client.rs` alone is a third of it.
**Scope:** api
**Hardware:** none — source comments only; no board, no live Core, no deploy.
**Owner:** no

## What

```
99  crates/embarch-core-client/src/client.rs
37  src/config.rs
32  src/resolve.rs
24  src/tools.rs
17  src/cli.rs
```
…and ~88 more across the rest of `src/`, `crates/` and `tests/`.

**`check-decision-refs.py` resolves decision numbers only inside `*.md`**, so a wrong number in a
source comment fails no gate and never has. Every sweep of this class run since 2026-09-10 has found
something real; the one that did not (`umbrella/065`, `doctor.rs`) is the only clean result so far.

## Why `client.rs` specifically, and why it is not just "the biggest file"

**`embarch-core-client` is the one crate in the suite whose comments legitimately cite two different
repos' decision sets.** It is `embarch-api`'s client *for `embarch-core`*, so a comment there may
correctly mean `embarch-core` decision 37 or `embarch-api` decision 37 — two different decisions
wearing the same number. That is exactly the silent same-number collision `umbrella/064` found in
`mirrors.md` on 2026-09-13, and `umbrella/065` then confirmed clean in `doctor.rs`. **Nothing
mechanical can tell the two apart**: a bare `decision 37` resolves against whichever set the reader
assumes.

Two things also make this file's citations likelier than average to have gone stale in *prose*
rather than in number:

- **`api/087` landed decision 73 here on 2026-09-13** — a `409`/`503` body with no `kind` field now
  converts to `kind: "unknown"` rather than defaulting to `"mismatch"`. Any comment in this file
  that describes the old conversion is now false, whatever number it cites.
- **`api/086` and `api/087` split `embarch-api`'s decisions twice in two hours**, moving 57, 67 and
  71 between files. A comment naming a *file* rather than an index has a good chance of naming a
  file that decision no longer lives in.

## What to do

Sweep in the order listed above and get as far as you honestly can — **this is expected to be a
partial pass, and a partial sweep with an accurate boundary is worth more than a rushed complete
one.** File `tasks/api/<next>` for the remainder, naming exactly which files you reached.

For each citation:

1. **Resolve the number, and say which repo's set it resolves against.** Where the referent is
   another repo's decision, write the labelled form `embarch-core decision N`. Same-repo citations
   stay bare. Do not invent a new form — the general question is owner-reserved (`tasks/doc/055`).
2. **Read the decision body against the sentence around the citation, not just the number.** The
   real yield of four consecutive sweeps this week was prose a decision had made false while its
   number still resolved. A citation that resolves is not yet a citation that is true.
3. **Do not manufacture findings.** "Ninety-nine checked, ninety-nine held" is a real and reportable
   outcome. Say how many you actually read versus how many you counted.

## Done when

- [ ] `client.rs` is swept end to end, and every citation in it either resolves and reads true, or
      is corrected with the correction argued.
- [ ] Every cross-repo citation in the swept files carries the labelled `<repo> decision N` form.
- [ ] Any remainder is filed as `tasks/api/<next>` naming the exact files not reached.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment. A numbered decision only if something was actually *decided* — a
      sweep that corrects citations usually decides nothing and needs none.

## Reserve, for planning

`embarch-api/spec.md` is 9,102/10,240 B — **1,138 B left, 88.9%** — filed against blocked
`tasks/api/083`. Nothing else in this scope is in reserve. If your work leaves any `embarch-api` doc
in the last 10% of its cap unfiled, file `tasks/api/<next>-compact-api.md` in the same commit —
**your own scope**, never `tasks/doc/`.
