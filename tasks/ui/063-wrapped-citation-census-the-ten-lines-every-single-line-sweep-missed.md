# 063 — Wrapped-citation census: the ten lines every single-line sweep missed

**State:** done — 10 lines / 16 instances checked; one wrong decision number found and fixed
(`src/study_designer.rs`, decision 57 → 56); no missing labels, no false sentences. Gate green.
See `## Result` for the full breakdown.
**Source:** `tasks/doc/071` (`Owner: required`, open), second `Done when` bullet — *"each
sub-project already declared 'citation swept' end to end gets a follow-up task re-censusing with the
wrap-aware method"*. `embarch-ui` was swept by `ui/054` (`assets/app.js`), `060` (`main.rs`,
`trace.rs`) and `061` (the plural-form recheck), **all of them single-line greps**. The same
follow-up has already run for `embarch-core` (`core/069`), `embarch-api` (`api/106`) and
`embarch-umbrella` (`umbrella/074`); this is `embarch-ui`'s.
**Scope:** ui
**Hardware:** none — source comments only. Nothing is built for a board, no probe, no live Core, no
study, no trace.
**Owner:** no

**Doc-size reserve for `ui`: nothing.** No `embarch-ui/*` doc is inside the last 10% of its cap
(`scripts/check-doc-size.py --pressure`, re-read fresh at this leg's top, 2026-09-16). If your work
pushes one into reserve, file `tasks/ui/<NNN>-compact-ui.md` in the same commit — see
`tasks/README.md`.

## What

A citation whose word `decision`/`decisions` sits at the end of a comment line and whose **number**
sits on the next line is invisible to every census this suite has run: they all match a single line.
`core/068` found the class, `tasks/doc/071` named it, and the three repos swept since have each
turned up real instances — including `dev-bench/033`'s wrong decision number and `umbrella/074`'s
owed reversal row, neither of which any prior sweep could have seen.

`grep -rnIE '[Dd]ecisions?[[:space:]]*$'` over `embarch-ui`, excluding `.git` and `target`, returns
exactly **ten** lines:

```
assets/app.js:1087         // Vendor-defined services (`embarch-study-designer` decision
assets/app.js:2706         /* One GATT-notify tap row (`embarch-study-designer` decisions
assets/app.js:3400         // Re-declaring the same name *is* the migration path the decision
src/config.rs:44           /// `embarch-api`'s own `base_url = "auto"` follows (`embarch-api` decision
src/trace.rs:3139          /// `assets/app.js` did this arithmetic on the whole capture until decision
src/study_designer.rs:65   /// A `Mutex`, not a plain field, and that is the whole shape of decision
src/study_designer.rs:430  /// One tap, as this tab authors it (`embarch-study-designer` decisions
src/study_designer.rs:828  /// The same, for services (`embarch-study-designer` decision
src/study_designer.rs:1123 // run far longer than 30s (`embarch-study-designer` decision
src/study_designer.rs:1228 /// `<firmware repo>/embarch/studies` (`embarch-study-designer` decision
```

Re-run that grep yourself before you start — `main` moves — and report the count you actually got
rather than this one if they differ.

**Three of these are the highest-risk shape in the whole chain**, and they are the unlabelled ones:
`app.js:3400`, `trace.rs:3139` and `study_designer.rs:65` carry no repo prefix on the matched line.
An unlabelled citation means *this repo's own* decision, and six of the other seven lines in the
same files are `embarch-study-designer`'s — so a bare number sitting among them is either correct
and easy to misread, or a dropped prefix. Check the line **above** each match before concluding
either way; that is exactly where `core/068` lost two prefixes.

## What to check, per citation

Read the whole wrapped citation (this line, the next, and the line above), then answer three
separate questions. The chain has found defects in all three categories, so do not collapse them:

1. **Does the number resolve?** Does a decision with that number exist in the repo the sentence
   names — `embarch-ui`'s own `decisions.md`/`decisions/*.md` when unlabelled, the named repo's when
   labelled?
2. **Is it the right repo?** See above. A same-repo citation takes **no** prefix; a cross-repo one
   must carry it.
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

- [x] All ten wrapped citations read in full and answered against all three questions above.
- [x] Every wrong number fixed, every missing repo label added, every false sentence corrected or —
      if you cannot establish what the right referent is — **left alone and reported**, never guessed.
- [x] `N lines / M instances / W wrong / L labels / F false` stated in the report.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10): `cargo build --all-targets`, `cargo test`,
      `cargo clippy --all-targets -- -D warnings` in `embarch-ui`; `check-docs.py` in `embarch-doc`.
      Remember `embarch-ui`'s worktree needs `embarch-study-designer`, `embarch-api` **and
      `embarch-topology`** symlinked beside it or `cargo build` fails on a path inside the fleet's
      scratch directory — the supervisor has done this for you; say so if a build still fails that way.
- [x] `changelog.d/` fragment. A zero-defect result is still a result and still gets one.

## Result

Re-ran `grep -rnIE '[Dd]ecisions?[[:space:]]*$'` against `embarch-ui` (excluding `.git`, `target`)
and got the same 10 lines the task filed, across `assets/app.js` (3), `src/config.rs` (1),
`src/trace.rs` (1) and `src/study_designer.rs` (5) — **10 lines / 16 instances**.

Each wrapped citation was read with the line above and the line(s) after, and checked against all
three questions (resolves, right repo, sentence true):

- `app.js:1087` — `embarch-study-designer` decision 41 (vendor GATT service table). Resolves,
  correctly labelled, true (Nordic UART Service example matches the decision body verbatim).
- `app.js:2706` — `embarch-study-designer` decisions 52/55 (GATT-notify tap file + declared
  layout). Both resolve, correctly labelled, true.
- `app.js:3400` — unlabelled, no number on either line. Resolves by section header (`decision 10,
  first half` at line 3251) to `embarch-ui` decision 10's **routing half**
  (`decisions/topology-tab.md`), whose own text says "Re-declaring the same name *is* the migration
  path" almost verbatim. Correctly unlabelled (same repo), true. The highest-risk shape named in
  the task turned out to resolve cleanly here.
- `src/config.rs:44` — `embarch-api` decision 11 (`base_url = "auto"`, resolved per-process).
  Resolves, correctly labelled, true.
- `src/trace.rs:3139` — unlabelled, `embarch-ui` decision 18 (server-side binning,
  `?from&to&width`). Resolves, correctly unlabelled (same repo), true.
- `src/study_designer.rs:65` — unlabelled, `embarch-ui` decision 14 (opening a project moves three
  things together). Resolves, correctly unlabelled, true.
- `src/study_designer.rs:430` — `embarch-study-designer` decisions 39/52/55 + `embarch-outpost`
  decisions 11/12 (the `TapInput` shape). All five resolve, correctly labelled, all true against
  the enum's actual two variants.
- `src/study_designer.rs:828` — **wrong number.** Cited `embarch-study-designer` decision 57
  ("the extraction scans the repo, not two files it was told about" — unrelated). The claim made
  ("services get their own map because a merged map would have to guess which half a UUID wanted")
  is decision **56**'s own sentence verbatim ("Two maps rather than one, because a merged map would
  have to guess which lookup a UUID wanted"). Fixed in `src/study_designer.rs` to cite 56.
- `src/study_designer.rs:1123` — `embarch-study-designer` decision 9 (async job execution, unbounded
  BLE wait). Resolves, correctly labelled, true.
- `src/study_designer.rs:1228` — `embarch-study-designer` decision 38 (`<firmware-repo>/embarch/studies`
  saved-study library). Resolves, correctly labelled, true.

**10 lines / 16 instances / 1 wrong / 0 labels / 0 false.** One fix landed in `embarch-ui`
(`src/study_designer.rs`): decision 57 → 56. Nothing else needed a repo label added and no sentence
was false against its correctly-cited decision.

Gate: `cargo build --all-targets`, `cargo test` (91 passed, 4 ignored, plus 2 in
`tests/element_ids.rs`), `cargo clippy --all-targets -- -D warnings` all green in `embarch-ui`
(the `embarch-study-designer`/`embarch-api`/`embarch-topology` symlinks beside the worktree
resolved with no extra linking needed). `check-docs.py`, `check-client-names.py --repo`, and
`check-ownership.py` run from `embarch-doc`; results in the leg report.

## Not yours

Do not widen this to single-line citations — those are swept and re-reading them is what this task
exists to *avoid*. Do not amend a decision because a comment disagrees with it: the comment is what
this task may change. If a decision itself looks wrong, that is an `inbox/` drop, written to
`/home/gabriel/Github/embarch/embarch-doc/inbox/` by absolute path.
