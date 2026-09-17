# 046 — Citation sweep: the 18 `embarch-topology` citations that live outside `src/`

**State:** done — leg 122, 2026-09-16; see "Closed" at the bottom.
**Source:** leg 117's refill sweep, 2026-09-16. Not from an `open.md` bullet — `embarch-topology/open.md`'s
six live questions are all hardware debts, upstream deferrals, or explicitly-recorded standing
limitations, none of them dispatchable. This came out of a mechanical census of citation-bearing
files across the scopes that had no dispatchable work.
**Scope:** topology
**Hardware:** none — comments in a binary's source, a manifest, and a README. Nothing is built for a
board, no probe, no live Core.
**Owner:** no

**Doc-size reserve for `topology`: nothing in reserve.** `topology/043` and `044` squeezed `spec.md`
out (9,825 → 9,001 B) and nothing has gone back in. If this unit's work pushes a `topology` file
into reserve, file `tasks/topology/<next free NNN>-compact-topology.md` in the same commit per
`tasks/README.md`.

## What

`topology/040` swept **`src/`** and reported *"103 src/ citations read, 3 false sentences fixed,
not one wrong number"*. Its scope was the directory, and three citation-bearing files sit outside it
and were never read:

```
9  Cargo.toml     (lines 10, 11, 13, 41, 59, 65, 89, 95, 97)
7  bin/main.rs    (lines 2, 7, 73, 97, 102, 143, 168)
2  README.md      (lines 38, 69)
```

Eighteen citations. Sweep them by the method the six `study-designer` sweeps and `umbrella/065`–`066`
used: for each, does the cited decision exist, is its form right for the repo it means, and does the
sentence around it state something the decision actually says.

## Why now

**Because `Cargo.toml` is the interesting one and nothing has ever looked at it.** Nine of the
eighteen are there, and they are not incidental — they are the manifest's own explanation of why the
crate is shaped the way it is: why the CLI is a `[[bin]]` (decision 5), why the local web UI half is
gone and `bin/ui.rs` with it (decision 5, dated 2026-08-24 in the comment), why a consumer forbidden
from linking `probe-rs` needs the hand-mirroring (decision 31), why the loopback POST was retired
(decision 19). **Those are exactly the sentences a sweep finds wrong**: prose that was true when a
decision was written and that a later decision made false. `topology/040`'s entire yield was that
shape — three false sentences, zero wrong numbers.

**And `Cargo.toml` comments carry a dated claim, which is rarer and more checkable than most.** Line
97 says the UI was retired *"2026-08-24 (decision 5)"*. `git log` can settle whether that date and
that decision number belong together; `study-designer/049` settled a comparable date claim with
`git log -S`, and `api/097`'s reviewer found a *different* comment conflating a decision's creation
date with an amendment to it. Check this one rather than assuming.

## Watch for

- **`check-decision-refs.py` walks `*.md` only.** It never reads `Cargo.toml` or `bin/main.rs`, so
  nothing fails today and nothing will. The two `README.md` citations are the only ones a gate could
  in principle see, and the script's scope is the doc repo, not this code repo — so treat all
  eighteen as unchecked.
- **`bin/main.rs` mixes three citation forms in seven lines** — bare (`decision 8`, `decision 20`),
  backtick-labelled (`` `embarch-topology` decision 28 ``), and bare-labelled inside a string literal
  (`(embarch-topology decision 28)` on line 168). All three mean this repo's own decisions, so the
  numbers are probably fine; the question is whether the **forms** should be consistent, and line 168
  is a **shipped user-facing string**, not a comment. `tasks/ui/038` is the open, owner-reserved
  question about exactly this — a same-repo citation in a shipped string using the cross-repo form —
  so **do not settle the general rule here.** Fix a wrong number or a false sentence; if the only
  problem with a line is its form, say so in your report and leave it for `tasks/doc/055`.
- **Do not introduce a bare cross-repo citation.** Line 2 of `bin/main.rs` mentions `embarch-core` in
  the same breath as `(decision 8)`; check which repo decision 8 belongs to before touching it.
  `api/091` closed this shape in a shared crate, `api/097` reintroduced it eight words away, and
  `api/099` is closing it again this leg.
- **Report counts, not just changes.** Wrong numbers and false sentences as separate numbers, plus
  the total checked. "Checked 18, found none" is a legitimate and useful result — three consecutive
  zero-defect sweeps were flagged in the 2026-09-12 handoff as possibly meaning refill has converged
  on always-clean files rather than that the corpus is clean, and nothing tracks the hit rate.

## Done when

- [x] All 18 citations in `Cargo.toml`, `bin/main.rs` and `README.md` checked for existence, repo
      label, and whether the sentence around each is true.
- [x] The `Cargo.toml` line 97 date claim (`2026-08-24`, decision 5) either confirmed against git
      history or corrected.
- [x] Wrong numbers and false sentences reported as separate counts, with the total checked.
- [x] No new bare cross-repo citation introduced anywhere in the diff.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Closed

**21 distinct citation instances checked** (the 18-line census, plus 3 more path-form citations
in `bin/main.rs`'s `refuse_if_core_reachable` doc comment — `decisions/platform.md:32`,
`decisions/enrollment.md:15` and `decisions/surfaces.md:17` — that `check-decision-refs.py`'s
`*.md`-only scope and the original grep both missed since they cite by file:line, not `decision N`).
**2 wrong numbers, 1 false sentence.**

- `bin/main.rs`'s `SetDevBenchLink` doc comment cited **decision 20** for the
  `--clear-serial`/`--clear-interface` fix ("a stale declared fact... re-enrolling by role carries
  it right back over... no way to clear it short of hand-editing `enrollment.toml`"). That content
  is **decision 27**'s, verbatim in places — decision 20 covers role uniqueness and the
  guessed-interface heuristic only, never mentions the clear flags. Repointed to decision 27.
- The same function's doc comment cited `embarch-core/decisions/surfaces.md:17` for "races Core's
  lock with no queue and no message". Line 17 of that file is decision 12's JSON-error-body text —
  unrelated. The real content ("a second process calling the same function does not share that
  lock") lived in `surfaces.md` until `embarch-core`'s `decisions/enrollment.md` split out of it on
  2026-09-11; the citation was written 2026-09-13 (`topology/036`, `e51f7ed`), two days after the
  split, so it was already wrong the day it landed. Repointed to `embarch-core/decisions/enrollment.md:10`.
- `README.md` called the crate's shared data directory "admin-owned". Decision 23 explicitly
  corrected that exact wording as an error (2026-09-07, `tasks/topology/013`): only
  `embarch-core`'s token *file* is admin-locked via `icacls`; the directory keeps `ProgramData`'s
  default, permissive ACL. Fixed the sentence.

`Cargo.toml`'s 9 citations (decisions 5×3, 8, 13, 19×2, 31×2) all check out, including the
`bin/ui.rs` retirement date — confirmed against `git log` (`7d13781`, 2026-08-24) rather than
assumed. `bin/main.rs`'s two other decision-20 citations (`guessed_among`, lines 97/102) check out
too. `Cargo.toml` and `README.md` stayed well clear of reserve; no compaction task filed.
`bin/main.rs`'s two citation-form issues (mixed bare/backtick/string-literal forms, and the
same-repo cross-repo-labelled form in the user-facing string on line 168) are left for
`tasks/doc/055` per this task's own instruction — not settled here.
