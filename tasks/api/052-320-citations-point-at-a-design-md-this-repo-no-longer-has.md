# 052 — 320 citations point at a `design.md` this repo no longer has

**State:** done — leg 061, worker on `agent/api/052-design-md-citations`

**Convention adopted:** a same-repo citation drops both `design.md` and the section number and
reads bare `` decision M ``, resolved against this repo's own `decisions/` index. A cross-repo
citation drops `design.md`/`§N` too and adds the repo name as a plain qualifier before `decision`,
e.g. `` `embarch-core` decision 22 `` — no repo-local section number, since none survived the
split. A citation that named only a section, not a decision (`design.md §5`, `design.md §9`), was
resolved to either the specific decision that section turned out to describe, or — where no
decision covers it — that repo's `spec.md` (optionally with a section number, since `spec.md`'s
own numbering is current). Where `embarch-ui` decision 10 is reused across three different topics
in its own index (routing/trace/chart), the citation keeps that disambiguator, e.g.
`` `embarch-ui` decision 10, routing half ``.
`tasks/umbrella/043` should adopt this convention rather than invent a second one.

**Dispatch note (supervisor, leg 061):** `tasks/umbrella/043` is the same sweep for
`embarch-umbrella` and is deliberately **not** dispatched alongside you — it is told to adopt
whatever citation convention you settle on. So **state the convention you used explicitly in your
`changelog.d/` fragment and in one line of the task file**: what a citation looks like after the
rewrite, and how you qualified a cross-repo decision. That sentence is the deliverable the next
sweep reads.

**Doc-size reserve for `api` — this scope is the tightest in the suite and every compaction task in
it is BLOCKED.** `decisions/tool-wrapping.md` 12,222/12,288 B (**66 B left**),
`decisions/core-link.md` 188 B left, `open.md` 261 B left, `spec.md` 815 B left,
`interfaces/tools.md` 1,008 B left, `decisions/build.md` 1,154 B left. This unit is a comment-only
code sweep, so plan to touch **no** `embarch-doc/embarch-api/` file other than dropping a
`changelog.d/api-*` fragment. If you find you need a doc edit, prefer the file with the most
headroom, keep it to a citation rather than prose, and file
`tasks/api/<NNN>-compact-api.md` in the same commit if you spend reserve.
**Source:** supervisor, leg 059, 2026-09-09 — found while fixing the miscitation the `api/031`
reviewer filed
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api`'s docs were split into `spec.md` / `open.md` / `decisions.md` / `decisions/*` /
`interfaces/*`; **there is no `embarch-api/design.md` and there has not been for days.** A grep
across the `embarch-api` code repo (excluding `target/`) finds **320 occurrences of `design.md`**,
overwhelmingly in the form `design.md §N.N decision M` — comments in `src/`, `crates/`, and
`config.example.toml`.

This is the same defect `tasks/study-designer/018` swept out of its own repo on 2026-09-09, where
the count was **522 changed lines across 32 files** against a task filed for 290 in 23 — so expect
this one to be larger than the number above too, and expect occurrences outside `src/`
(`Cargo.toml`, `tests/`, `tools/`, `.github/workflows/`) that a `src/`-scoped grep never reaches.

**The section numbers did not survive the split**, so every `§N.N` in those citations has been
pointing at nothing. Nothing catches it: `check-decision-refs.py` reads markdown, not code-repo
comments, and `embarch-api` keeps `cargo doc` warnings out of its gate.

## The half that is worse than a dead pointer

`api/031`'s reviewer found a **live misattribution** hiding inside this convention, which is why
this task is worth more than a mechanical sweep. `config.example.toml`'s `probe_serial` comment
cited `design.md §3 decision 9` for probe ambiguity. That content is **`embarch-core`'s decision
9** (`embarch-core/decisions/probes.md`); `embarch-api`'s *own* decision 9 is about locked
dependency choices and is entirely unrelated. Dropping the repo qualifier did not produce a dead
link — it produced a citation to a **real, permanent, wrong decision.** Fixed in place at leg 059
(`embarch-api` `61e2b42`), and it is the only one anybody has checked.

**So this sweep is not a find-and-replace.** Every citation has to be resolved against the current
decisions index before its `design.md §N` prefix is stripped, exactly as `study-designer/018`'s
reviewer did by sampling: stripping the prefix off an already-wrong number leaves a wrong number
that now reads as authoritative. Cross-repo content cited without a repo qualifier is the specific
thing to hunt.

## Done when

- [x] No `design.md` reference remains anywhere in the `embarch-api` repo — verified by a
      repo-wide grep at the merge SHA, not a `src/`-scoped one.
      `grep -rn "design\.md" --exclude-dir=target --exclude-dir=.git .` from the repo root
      returns nothing.
- [x] Every citation touched was resolved against the current decisions index, and any that named
      another repo's decision now says which repo. Found and fixed 5 real miscitations along the
      way (not just dead §N pointers): `config.rs`'s two `artifact_path_for_core` UNC-retrospective
      comments and `config.example.toml`'s `base_address` comment cited `embarch-core`/were
      mistagged when the decision is `embarch-api`'s own (15 and 42 respectively); `main.rs`'s
      `EnrollProbe`/`Validate`/`Alerts` doc comments cited bare (repo-less) numbers that actually
      belong to `embarch-core` (22, 28, 28); `cli.rs`/`tools.rs`'s reseal comment cited a bare
      number that belongs to `embarch-study-designer` (26).
- [x] The diff is comment-only where it touches `.rs` — the cheap structural proof is
      `git diff -U0 -- '*.rs' | grep` for changed non-comment lines returning nothing, which
      `study-designer/018` used and which this log recommends for any sweep this size.
      Two lines flagged by the Python equivalent of that check are inside `format!`/error-message
      *string literals* (a citation embedded in user-facing text, not code), not comment or logic
      changes — see below.

## In flux: no
