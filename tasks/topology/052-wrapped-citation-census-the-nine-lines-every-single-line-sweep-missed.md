# 052 — Wrapped-citation census: the nine lines every single-line sweep missed

**State:** done — leg 130 unit 1, 2026-09-16, `agent/topology/052-wrapped-citations`
**Source:** `tasks/doc/071` (`Owner: required`, open), second `Done when` bullet — *"each
sub-project already declared 'citation swept' end to end gets a follow-up task re-censusing with the
wrap-aware method"*. `embarch-topology` was swept by `topology/040` (`src/`), `046` (outside `src/`)
and `050` (the plural-form recheck), **all three of them single-line greps**. The same follow-up has
already run for `embarch-core` (`core/069`), `embarch-api` (`api/106`) and `embarch-umbrella`
(`umbrella/074`); this is `embarch-topology`'s.
**Scope:** topology
**Hardware:** none — source comments only. Nothing is built for a board, no probe, no live Core, no
study.
**Owner:** no

**Doc-size reserve for `topology`: nothing.** No `embarch-topology/*` doc is inside the last 10% of
its cap (`scripts/check-doc-size.py --pressure`, re-read fresh at this leg's top, 2026-09-16). If
your work pushes one into reserve, file `tasks/topology/<NNN>-compact-topology.md` in the same
commit — see `tasks/README.md`.

## What

A citation whose word `decision`/`decisions` sits at the end of a doc-comment line and whose
**number** sits on the next line is invisible to every census this suite has run, past and present:
they all match a single line. `core/068` found the class, `tasks/doc/071` named it, and the three
repos swept since have each turned up real instances of it — including `dev-bench/033`'s wrong
decision number and `umbrella/074`'s owed reversal row, neither of which any prior sweep could have
seen.

`grep -rnIE '[Dd]ecisions?[[:space:]]*$'` over `embarch-topology`, excluding `.git` and `target`,
returns exactly **nine** lines:

```
src/lib.rs:8                  //! no shell-out, no hand-off file, no env var (decisions
src/software.rs:22            //! call instead of wiring the pieces together themselves (decision
src/software.rs:268           /// Find Core, live, on every call — no cache, no write-ahead file (decision
src/hardware/alert.rs:1       //! The durable alert log behind [`super::validate`] (decision
src/hardware/signal.rs:13     //! enrollment storage, for the same reason enrollment itself is (decision
src/hardware/hardware_id.rs:81 /// prefix so it cannot reach either register pair by accident.** Decision
src/hardware/validate.rs:392  /// `embarch-core` can call it instead of keeping its own copy (decision
src/hardware/validate.rs:401  /// probe identifier are exactly what a same-probe-type ambiguity (decision
src/hardware/enrollment.rs:3  //! `embarch-core`'s own `known_boards.rs` / `known_boards.toml` (decisions
```

Re-run that grep yourself before you start — `main` moves — and report the count you actually got
rather than this one if they differ.

## What to check, per citation

For each one, read the **whole** wrapped citation (this line plus the next, and the line *above*
where the repo prefix may have wrapped off the front), then answer three separate questions. The
chain has found defects in all three categories, so do not collapse them:

1. **Does the number resolve?** Does a decision with that number exist in the repo the sentence
   names — `embarch-topology`'s own `decisions.md`/`decisions/*.md` when unlabelled, the named
   repo's when labelled?
2. **Is it the right repo?** A wrapped citation is exactly where a repo prefix goes missing, because
   the prefix is on the line before the one a census matched. `core/068` mis-filed two citations as
   "bare — own repo" for precisely this reason. A same-repo citation takes **no** prefix; a
   cross-repo one must carry it.
3. **Is the sentence true?** This is the one a resolution check cannot answer and the one that has
   produced the chain's real defects: `dev-bench/033` relabelled a comment to a decision that
   resolved fine and **contained nothing about the claim being made**. Read the cited decision's own
   body and check it actually says what the comment says it says.

## How to report

Report **every cited occurrence**, not deduplicated `(repo, number)` pairs — one line citing two
numbers is two instances, and the same number cited on two lines is two instances. This convention
is the chain's (`core/069` 15 lines/25 instances, `api/106` 18/20, `umbrella/073` 13/30) and
`umbrella/074` drifted from it; say `N lines / M instances` explicitly so the running tally stays
comparable.

## Done when

- [x] All nine wrapped citations read in full and answered against all three questions above.
- [x] Every wrong number fixed, every missing repo label added, every false sentence corrected or —
      if you cannot establish what the right referent is — **left alone and reported**, never guessed.
- [x] `N lines / M instances / W wrong / L labels / F false` stated in the report.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10): `cargo build --all-targets`, `cargo test`,
      `cargo clippy --all-targets -- -D warnings` in `embarch-topology`; `check-docs.py` in
      `embarch-doc`.
- [x] `changelog.d/` fragment. A zero-defect result is still a result and still gets one.

## Result

9 lines / 12 instances / 2 wrong / 1 label / 0 false.

- `src/hardware/validate.rs:401` — cited `decision 10` (scope.md, the dev-bench/DUT chip-family
  risk) for a claim about same-probe-type ambiguity that is actually decision 15's
  (`decisions/enrollment.md`: "two boards sharing an identical probe type still cannot be told
  apart by serial alone" — near-verbatim match to the comment). Fixed the number and reworded the
  parenthetical from "chip family" to "identical probe type" to match decision 15's actual content;
  kept the "e.g. two J-Links" illustration since it fits a same-probe-type example.
- `src/hardware/enrollment.rs:3-4` — cited bare `(decisions 2, 3, 7)` for "formerly `embarch-core`'s
  own `known_boards.rs`/`known_boards.toml`". None of `embarch-topology`'s own decisions 2, 3, 7
  discuss that migration; `embarch-core` decision 22
  (`embarch-core/decisions/probes.md`) does, verbatim: "nothing in a USB descriptor says 'I'm wired
  to the DUT'" and "Moved wholesale into `embarch-topology`". Fixed to `(`embarch-core` decision
  22)` — both the numbers and the missing cross-repo label.
- The other 7 lines (10 instances: `lib.rs:8` decisions 2,3; `software.rs:22` decision 1;
  `software.rs:268` decision 3; `hardware/alert.rs:1` decision 12; `hardware/signal.rs:13` decision
  14; `hardware/hardware_id.rs:81` decision 21; `hardware/validate.rs:392` decision 33) all resolve,
  are correctly bare/same-repo, and match their cited decision's body. No changes.

## Not yours

Do not widen this to single-line citations — those are swept, three times over, and re-reading them
is what this task exists to *avoid*. Do not amend a decision because a comment disagrees with it:
the comment is what this task may change. If a decision itself looks wrong, that is an `inbox/`
drop, written to `/home/gabriel/Github/embarch/embarch-doc/inbox/` by absolute path.
