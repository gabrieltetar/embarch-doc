# 043 — 68 citations in the `embarch-umbrella` crate point at a `design.md` this sub-project no longer has

**State:** claimed by agent/umbrella/043-design-md-citations, 2026-09-10 14:08

**Reclaimed after leg 062 was stopped mid-run.** That leg's worker was killed with the whole sweep
uncommitted in its worktree — 14 files, 60 insertions, never a commit and never pushed — so the
worktree was deleted per `ops.md` §3 and the work is being redone from scratch. Nothing of it
survives to build on; the convention section above is the only thing leg 062 left, and it is enough.
**Source:** found by the supervisor while landing `umbrella/035`, leg 060, 2026-09-09. The one line
`035` edited (`Cargo.toml`'s boundary comment) ended in `(design.md §1)`; fixing that one citation
in the fold turned up 67 more.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## The convention to adopt — settled by `api/052`, leg 061, 2026-09-09. Do not invent a second one.

This task's own body says to check whether `api/052` has landed first and use whatever convention it
settles. **It has landed** (`embarch-api` `5131ec7`, doc `97a19f0`) — 160 citations across 21 files,
5 of them real miscitations rather than dead pointers. Its convention, copied here verbatim by the
supervisor because `api/052`'s task file was deleted by its own fold:

> A same-repo citation drops both `design.md` and the section number and reads bare `` decision M ``,
> resolved against this repo's own `decisions/` index. A cross-repo citation drops `design.md`/`§N`
> too and adds the repo name as a plain qualifier before `decision`, e.g. `` `embarch-core` decision
> 22 `` — no repo-local section number, since none survived the split. A citation that named only a
> section, not a decision (`design.md §5`, `design.md §9`), was resolved to either the specific
> decision that section turned out to describe, or — where no decision covers it — that repo's
> `spec.md` (optionally with a section number, since `spec.md`'s own numbering is current). Where
> `embarch-ui` decision 10 is reused across three different topics in its own index
> (routing/trace/chart), the citation keeps that disambiguator, e.g.
> `` `embarch-ui` decision 10, routing half ``.

**Two things `api/052` learned that this sweep should not re-learn:**

- **The count in this task's title is stale and will be wrong.** `api/052` was filed for 320 and
  found 160; `study-designer/018` was filed for 290 in 23 files and landed 522 lines across 32.
  Re-count before starting, over the whole tree, and do not treat the table below as a checklist.
- **The bare form is the dangerous one.** Every citation that ends up as bare `decision M` is
  asserting "this repo's own", which silently absorbs a cross-repo number. `api/052` found 5 of
  exactly that, including two comments crediting `embarch-core` for `embarch-api`'s own decisions.
  Resolve each number against the index of the repo the *new* form names, and check the decision's
  subject matches what the comment claims.

**One caveat on the `embarch-ui` clause.** That disambiguator exists because `embarch-ui` decision 10
is deliberately one decision split into three halves across three topic files, with its index
qualifying them. Leg 061 also found that **nothing in the gate checks decision-number uniqueness**
(`inbox/doc-nothing-checks-that-a-decision-number-is-unique.md`), so a bare duplicate you meet in
some other repo may be a genuine collision rather than a split — in which case it is a finding to
drop, not a citation to qualify.

## What

`embarch-doc/embarch-umbrella/` holds `spec.md`, `open.md`, `decisions.md` and `decisions/` —
**there is no `design.md`**, and there has not been since the sub-project's docs were split. The
crate still cites it 68 times, almost all in the form `design.md §N.N decision M`:

| file | hits | | file | hits |
|---|---|---|---|---|
| `src/setup.rs` | 12 | | `src/main.rs` | 4 |
| `src/doctor.rs` | 11 | | `src/config.rs` | 4 |
| `src/init.rs` | 10 | | `src/deploy.rs` | 3 |
| `src/locate.rs` | 9 | | `src/state.rs` | 3 |
| `src/install.rs` | 6 | | `src/env.rs`, `src/manifest.rs`, `src/zephyr.rs` | 1 each |

(That accounts for 65 in `src/`; the remaining three are outside it — `Cargo.toml`'s was fixed in
`035`'s fold, so **re-count before starting** rather than trusting this table.)

Nothing catches it. `check-decision-refs.py` reads markdown, not Rust doc comments, and this crate
keeps `cargo doc` warnings out of its gate.

## This is the third instance of one class, and the earlier two teach it

- `study-designer/018` was filed for 290 occurrences in 23 files and **landed 522 lines across 32**.
  Expect more than a `src/` grep predicts.
- `api/052` is the same task for `embarch-api`'s 320 occurrences and is **still open** — check
  whether it has landed first, because whatever convention it settles on should be the one used here
  rather than a second one invented independently.
- **`api/031`'s fold found the failure mode that makes a mechanical sweep dangerous.** A citation
  stripped of its qualifier can land on a *real but wrong* decision: that unit's `probe_serial`
  comment cited "decision 9" meaning `embarch-core`'s, while `embarch-api`'s own decision 9 is
  unrelated — a citation that reads as authoritative and survives every check. **So resolve every
  `§N.N decision M` against the current `decisions/` index and confirm the decision it lands on is
  the one the comment is actually about, before rewriting it.** A `sed` over this is the wrong tool.

## Done when

- [ ] No occurrence of `design.md` remains in the `embarch-umbrella` repo, counted by grep over the
      whole tree and not only `src/`.
- [ ] Each rewritten citation names a file that exists **and** a decision whose subject matches what
      the comment claims — spot-check the substance, do not just re-point the path.
- [ ] Where a decision number is ambiguous across repos, the repo is named explicitly.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/umbrella-*` fragment.
