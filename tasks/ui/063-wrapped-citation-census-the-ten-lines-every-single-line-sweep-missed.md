# 063 — Wrapped-citation census: the ten lines every single-line sweep missed

**State:** open
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

- [ ] All ten wrapped citations read in full and answered against all three questions above.
- [ ] Every wrong number fixed, every missing repo label added, every false sentence corrected or —
      if you cannot establish what the right referent is — **left alone and reported**, never guessed.
- [ ] `N lines / M instances / W wrong / L labels / F false` stated in the report.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10): `cargo build --all-targets`, `cargo test`,
      `cargo clippy --all-targets -- -D warnings` in `embarch-ui`; `check-docs.py` in `embarch-doc`.
      Remember `embarch-ui`'s worktree needs `embarch-study-designer`, `embarch-api` **and
      `embarch-topology`** symlinked beside it or `cargo build` fails on a path inside the fleet's
      scratch directory — the supervisor has done this for you; say so if a build still fails that way.
- [ ] `changelog.d/` fragment. A zero-defect result is still a result and still gets one.

## Not yours

Do not widen this to single-line citations — those are swept and re-reading them is what this task
exists to *avoid*. Do not amend a decision because a comment disagrees with it: the comment is what
this task may change. If a decision itself looks wrong, that is an `inbox/` drop, written to
`/home/gabriel/Github/embarch/embarch-doc/inbox/` by absolute path.
