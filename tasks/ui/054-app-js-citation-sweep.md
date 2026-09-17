# 054 — Citation sweep: `embarch-ui/assets/app.js`, the largest never-swept citation surface in the suite

**State:** done — agent/ui/054-app-js-citation-sweep, 2026-09-16
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

- [x] Every `decision N` citation in `embarch-ui/assets/app.js` has been checked for existence, repo
      label, and whether its sentence is true.
- [x] Wrong labels and false sentences reported as separate counts, with the total citations covered.
- [x] No new bare cross-repo citation introduced anywhere in the diff.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Result

**Zero defects. 72 of 72 `[Dd]ecision [0-9]`-matching lines checked, plus one bonus (`decisions
53/55`, line 853, which the plural form makes the census regex miss) — 73 citations covered total.
0 wrong decision numbers, 0 wrong repo labels, 0 false sentences. No diff to `app.js`.**

Checked against the decisions.md index and the specific `decisions/*.md` entry for every number, in
every repo a citation named: `embarch-ui` (bare 2, 5, 6, 7, 10 ×4 distinct meanings — routing/trace/
chart/scope — 11, 13, 14, 15, 17, 18, 20, 23), `embarch-topology` (10, 17, 18, 19), `embarch-core`
(43, 57), `embarch-study-designer` (35, 36, 40, 41, 42, 43, 44, 52, 53, 55, 56), `embarch-api` (43),
`embarch-outpost` (19). Specifically re-verified, because each looked suspicious on first read and
turned out fine:

- Line 4780's `embarch-topology decision 19` citation for `fix_it_url` sits ~30 characters after its
  own `` `embarch-topology` `` label in the same sentence — inside the 44-char window, so it carries;
  not the fourth `client.rs`-shaped defect.
- Line 856/970's "`embarch-study-designer` decision 56, amended 2026-08-26" — decision 56's own file
  carries no explicit "amended" line, but `git log -S serviceLabel` and `-S charTitle` both land on
  2026-08-26 commits (`a534213`, `95305e1`), matching the decision text's "the same length of time"
  claim. True, just not restated as an amendment in the doc.
- Line 889's "`embarch-study-designer` decision 53 added two" (built-ins) — confirmed against
  `interfaces/types.md`/`decisions/wire.md`: decision 53 added exactly two `Action` variants,
  `GattMonitorSelected` (9) and `GattMonitorSelectedStart` (10).

**Not in scope, confirmed still unswept:** `embarch-ui/src/main.rs` (26 citation lines) and
`src/trace.rs` (25, one already fixed by `ui/048`) — left untouched per this task's own scope note.
Whoever refills the queue next should file `tasks/ui/<NNN>-main-rs-trace-rs-citation-sweep.md` (or
split in two) for those ~50 lines; not filed here since this task's own scope excluded them rather
than running out of room to do them.

No hardware, no doc-size reserve crossing (embarch-ui files stay clear), no code change in either
repo — `embarch-ui`'s `agent/ui/054-app-js-citation-sweep` branch carries no commit over `main`.
