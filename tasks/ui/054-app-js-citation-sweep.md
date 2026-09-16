# 054 — Citation sweep: `embarch-ui/assets/app.js`, the largest never-swept citation surface in the suite

**State:** open
**Source:** leg 117's refill sweep, 2026-09-16. Not from an `open.md` bullet — `embarch-ui/open.md`'s
six live questions are all hardware debts or upstream deferrals, none of them dispatchable without a
board. This came out of a mechanical census of citation-bearing source files across the four scopes
that had no dispatchable work.
**Scope:** ui
**Hardware:** none — source comments in a shipped JS asset. Nothing is built for a board, and the
UI is not launched.
**Owner:** no

**Doc-size reserve for `ui`: nothing in reserve.** `embarch-ui`'s files are all clear after
`ui/050` and `ui/053`. If this unit's work pushes a `ui` file into reserve, file
`tasks/ui/<next free NNN>-compact-ui.md` in the same commit per `tasks/README.md`.

## What

`embarch-ui/assets/app.js` is 4,855 lines and carries **72 lines matching `[Dd]ecision [0-9]`** —
more than `study_designer.rs` (69, swept by `ui/049`) and more than `embarch-umbrella/src/doctor.rs`
(swept by `umbrella/065`). **It has never had a sweep.** Four separate units have reached into it for
one citation each and left the rest untouched:

- `ui/047` — `delay_before_ms` comments cited decision 42, not 40.
- an earlier unit — `snapshot.rs`/`app.js`'s "decision 54" renumbered to 57 after `core/039`.
- two more that changed behaviour rather than citations (the outcome decoder, the row/stream caps).

Each of those found a real defect in the line it happened to open. Nothing has read the other ~68.

Sweep it the way `study-designer/044`–`050` and `umbrella/065`–`066` swept theirs. For each citation:

1. **Does the cited decision number exist**, in the repo the citation's form says it is in?
2. **Is the form right?** A bare `decision N` addresses the citing file's own sub-project — here,
   `embarch-ui`. A cross-repo referent must carry the `` `<repo>` `` label. `DOC-CONVENTIONS.md`,
   "Referring to a decision".
3. **Does the sentence around it state something the decision actually says?** This is the half a
   script cannot do and the half that finds false sentences.

## Why now

**Because this file is the one place in `embarch-ui` where a wrong citation is also shipped.**
`app.js` is served to the browser under decision 2's zero-build rule, so its comments travel with the
product rather than staying in a source tree. Every other `ui` sweep target is a `.rs` file that only
a developer reads.

It is also the largest single remaining sweep target anywhere in the suite. `embarch-umbrella` and
`embarch-outpost` source are both fully swept with 0 defects on their last passes;
`embarch-topology`'s `src/` was swept at 103 lines; `embarch-study-designer` is being finished by
`050`. This is what is left.

## Watch for

- **`check-decision-refs.py` does not walk `.js` at all** — it only reads `*.md`. So there is no
  mechanical backstop here and nothing will fail if a citation is wrong. Read every one.
- **Its attribution window is 44 characters** where it does run, which is the arithmetic behind the
  `api/097` defect: a `` `<repo>` `` label earlier in the same sentence does **not** carry to a
  second citation further along. If you correct a number, check the corrected citation's own label,
  and check the citations either side of it. `api/091` closed this shape in `client.rs`, `api/097`
  reintroduced it eight words away, and `api/099` is closing it again — do not make `app.js` the
  fourth instance.
- **`decision 2`, `decision 10` and the other low numbers in this file are `embarch-ui`'s own** and
  are correct bare. Do not "fix" a bare citation into a labelled one without checking which repo it
  actually means.
- **Report counts, not just changes.** Wrong labels and false sentences are separate numbers, and a
  file swept clean is a result worth recording — three consecutive zero-defect sweeps in a repo is
  itself evidence about whether this vein is exhausted, and nothing currently tracks the hit rate.

## Not in scope

`embarch-ui/src/main.rs` (26 citation lines) and `src/trace.rs` (25, of which `ui/048` fixed one) are
the next-largest unswept files in this repo. **Leave them** and say so in your report so the
remainder can be filed as its own task, exactly as the `study-designer` chain has been doing.

## Done when

- [ ] Every `decision N` citation in `embarch-ui/assets/app.js` has been checked for existence, repo
      label, and whether its sentence is true.
- [ ] Wrong labels and false sentences reported as separate counts, with the total citations covered.
- [ ] No new bare cross-repo citation introduced anywhere in the diff.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
