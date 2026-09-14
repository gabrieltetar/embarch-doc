# 091 — `embarch-core-client/src/client.rs` holds 99 citations and is the one file that cites two repos' decisions

**State:** done — `client.rs` and `config.rs` swept, `tasks/api/093` filed for the remainder
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

- [x] `client.rs` is swept end to end, and every citation in it either resolves and reads true, or
      is corrected with the correction argued.
- [x] Every cross-repo citation in the swept files carries the labelled `<repo> decision N` form.
- [x] Any remainder is filed as `tasks/api/<next>` naming the exact files not reached.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment. A numbered decision only if something was actually *decided* — a
      sweep that corrects citations usually decides nothing and needs none.

## Result

Swept `client.rs` (99 citations) and, having budget left, `config.rs` (37 citations) too — both
end to end, cross-checked against every cited decision's own body in `embarch-api`, `embarch-core`,
`embarch-study-designer`, `embarch-outpost`, `embarch-topology` and `embarch-ui`.

**`config.rs`: 37 checked, 37 held.** No wrong numbers, no false prose, no missing labels.

**`client.rs`: 99 checked, 6 fixed, the rest held.**

- **Wrong number (4 occurrences, one repo, both decisions genuinely exist).** `embarch-api`
  decision 59 (`dev_bench_hello`, and `link_identity` is a stable string) was cited for content
  that is actually decision 60's (`dev_bench_hello`'s three identity fields are optional, and
  absence renders as its own third state) — the "two rendering states" language, the "never
  computes a verdict of its own" sentence, and the reason the tool renders `"unavailable"` are all
  decision 60's own text, not 59's. Fixed at all four sites: the doc comment introducing
  `render_hello_ack`, two further doc-comment references, and — the one that matters most, since
  it reaches a caller rather than a maintainer — the `"unavailable"` message `render_hello_ack`
  itself builds at runtime, which named decision 59 as "why this tool renders unavailable" when
  that reason is decision 60's.
- **Ambiguous/unlabelled foreign citations (2 occurrences), both the same shape**: a bare
  `decision N` immediately after a differently-labelled sibling citation in the same sentence, so
  a reader has no cue it changed repos. `EnrollProbeRequest::probe_serial`'s doc comment cited
  `` `embarch-core` decision 22's, whose mechanism decision 14 moved`` — `embarch-core` decision 14
  is a real, unrelated decision (the `hw_lock`/503-naming-holder mechanism), and the "14" meant is
  `embarch-topology`'s (the same one labelled ten lines above, in the enclosing struct's doc
  comment). Labelled. `StudyRunOptions`'s doc comment cited `` (`embarch-core` decision 31's
  amendment, decision 40)`` — `embarch-core` decision 40 is also real and unrelated (an
  undecodable frame costs the frame, not the link); the "40" meant is `embarch-study-designer`'s,
  confirmed two lines later where the same citation is spelled out in full. Labelled.
- Left as bare, correctly, after checking: same-repo reuses within one already-labelled paragraph
  (e.g. `embarch-core` decision 59's several bare reuses inside `TopologyMismatchError`'s own doc
  block), and two same-*number*-different-repo collisions (`embarch-api` decision 15 vs.
  `embarch-topology` decision 15; `embarch-api` decision 59 vs. `embarch-core` decision 59) where
  every actual use was unambiguous in its local context.

Remainder — `resolve.rs` (~32), `tools.rs` (~24), `cli.rs` (~17) — filed as `tasks/api/093`.

## Reserve, for planning

`embarch-api/spec.md` is 9,102/10,240 B — **1,138 B left, 88.9%** — filed against blocked
`tasks/api/083`. Nothing else in this scope is in reserve. If your work leaves any `embarch-api` doc
in the last 10% of its cap unfiled, file `tasks/api/<next>-compact-api.md` in the same commit —
**your own scope**, never `tasks/doc/`.
