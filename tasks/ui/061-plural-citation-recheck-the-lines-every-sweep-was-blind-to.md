# 061 — Plural-citation re-check: the 7 lines every `ui` sweep was structurally blind to

**State:** claimed by agent/ui/061-plural-citation-recheck, 2026-09-16 20:57
**Source:** leg 125's refill sweep, 2026-09-16, acting on the measurement
`inbox/citation-census-grep-cannot-see-a-plural-citation.md` asked for and nobody had run.
`embarch-ui`'s citation surface was swept across `ui/049`, `ui/052` and `ui/054`, and `ui/060` takes
the last two source files. **Every one of those sweeps censused with
`grep -cE '[Dd]ecision [0-9]'`, which cannot match `decisions 53/55` or `decisions 34/36/53/54`** —
so these lines were never in any sweep's input at all, with one exception noted below.
**Scope:** ui
**Hardware:** none — doc comments in one Rust source file, one CSS comment and one `Cargo.toml`
comment. Nothing is built for a board, the UI is not launched, no probe, no live Core. Classified
fresh at filing.
**Owner:** no

**Doc-size reserve for `ui`: nothing in reserve.** If your work pushes a `ui` doc into the last 10%
of its cap, file `tasks/ui/<next free NNN>-compact-ui.md` in the same commit per `tasks/README.md`.
**`tasks/doc/` is not yours.**

## What

Eight lines matched, measured 2026-09-16 with `grep -rInE '[Dd]ecisions [0-9]'` over the repo
excluding `.git` and `target`. **Seven are yours; `assets/app.js:853` is the eighth and `ui/054`
already found and checked it** — it is the line that made this defect visible in the first place, so
confirm and move on rather than re-deriving it.

```
Cargo.toml:26              `embarch-api` decisions 37/38
assets/style.css:739       Decisions 10 and 11      CAPITALIZED, bare — see the warning below
src/study_designer.rs:431  ...39/52/55, `embarch-outpost` decisions 11/12   — the line wraps
src/study_designer.rs:538  `embarch-study-designer` decisions 34/36/53/54
src/study_designer.rs:734  (`embarch-study-designer` decisions 53/55)
src/study_designer.rs:2323 (`embarch-study-designer` decisions 52/55)
src/study_designer.rs:2372 `embarch-study-designer` decisions 34/36/53/54
assets/app.js:853          (`embarch-study-designer` decisions 53/55)       — already checked by ui/054
```

**Seven unchecked lines, roughly 22 distinct decision instances** — treat the line count as a floor
and report the instance count you actually checked.

Two warnings, both earned:

- **`assets/style.css:739` reads `Decisions 10 and 11`, capitalized and bare, and a bare
  `decision 10` cannot be resolved by number in this repo at all.** `ui/054`'s reviewer found six
  bare `decision 10` sites in `assets/app.js` resolving four different ways: `embarch-topology`'s,
  plus `embarch-ui`'s **own decision 10 in three different files** — `decisions/topology-tab.md`
  (routing), `decisions/trace-view.md` (trace) and `decisions/trace-chart.md` (chart).
  `embarch-ui`'s `decisions.md` documents that collision deliberately with the tags `10 (routing)`,
  `10 (trace)`, `10 (chart)`. **Resolve this one by reading what the surrounding CSS block is
  about**, and say in your report which referent you landed on and why. It is also a shipped asset
  under decision 2's zero-build rule, so the comment travels with the product.
- **`src/study_designer.rs:431` wraps**, and the numbers before `embarch-outpost` — `39/52/55` —
  belong to whatever repo the previous line names. Read the whole doc comment, not the grep hit.

## How

1. **Re-census with `[Dd]ecisions? [0-9]`, case-insensitively.** Report your number against the
   seven above.
2. **For each cited number, check the decision exists in the file the citation points at**, and
   remember a bare `decision NN` in another sub-project's file means *that* sub-project's NN —
   except where the `decision 10` collision above makes number-resolution impossible.
3. **Then read the cited decision's current text and check the sentence around the citation is
   still true of it.** `study-designer/054` found a citation that was correct when written and went
   false when `embarch-topology` amended the decision it cited; `embarch-study-designer` is the
   repo cited most here and it has been amended repeatedly. The two `decisions 34/36/53/54` sites
   both make the same claim about a failure mode — check it once against the decisions and then
   check both sites say it the same way.
4. **Fix wrong numbers and false sentences. Do not widen.** A wrong number that is not a decision
   citation is a finding for `inbox/`, not an edit.

## Done when

Every plural-form citation line in `embarch-ui` has had the existence-and-truth pass, the report
states the instance count checked against the seven-line floor, the `style.css` `Decisions 10 and
11` referent is named with its reasoning, and each defect found is either fixed here or filed with
its reason for not being fixed here.
