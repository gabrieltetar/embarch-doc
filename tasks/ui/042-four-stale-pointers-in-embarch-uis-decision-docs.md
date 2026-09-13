# 042 — Four stale pointers in `embarch-ui`'s decision docs: a marker count and three CSS line numbers

**State:** done — agent/ui/042-stale-pointers-in-decision-docs, 2026-09-13.
**Doc-size reserve for `ui`:** nothing in `embarch-ui`'s docs is in reserve. If your work pushes
a file into the last 10% of its cap, file `tasks/ui/<NNN>-compact-ui.md` in the same commit.
**Source:** leg 106 refill sweep, 2026-09-13, scout-verified. Re-derive each number.
**"Scout-verified" is one reader, and it has already been wrong once** — the same scout, same
sweep, reported a quoted source comment as never having existed when it had existed and was later
rewritten (`umbrella/058`). That matters most for (a) below, which turns on exactly that
distinction: a number that was true of an older fixture is not the same defect as one that was
never true.
**Scope:** ui
**Hardware:** none — four numbers in two decisions files. No rendered pixel changes.
**Owner:** no

## What

**(a) A marker count that is wrong by 23.** `embarch-doc/embarch-ui/decisions/trace-view.md:23` —
*"Markers began as full-height rules and **132** across 760 ms swamped every span"*, about *"a
committed `native_sim` capture"*. Both committed fixtures hold **155**:
`grep -c ',marker,' embarch-ui/tests/fixtures/*.csv` → `155`, `155`, and the test pins it —
`embarch-ui/src/trace.rs:2874`, `assert_eq!(view.markers.len(), 155);`.

**This one needs a judgement, not a substitution.** The sentence is past tense — *"markers
**began** as…"* — so it may be an honest historical observation about a fixture that has since been
regenerated, in which case the fix is to say which capture the 132 was measured on rather than to
overwrite it with 155. Read the surrounding entry and decide which it is; `tasks/ui/030` treated
this exact shape as a defect, which is the precedent, not the answer. **Say in the task file which
reading you took and why** — that reasoning is the durable half.

**(b), (c), (d) Three CSS line citations, each off by one.**
`embarch-doc/embarch-ui/decisions/shell.md:27` cites `style.css:124`, `style.css:44` (dark) and
`:73` (light). `grep -n -- '--brand' embarch-ui/assets/style.css` gives **123**, **43** and **72**.
The fourth citation in the same sentence, `index.html:34`, is correct — leave it.

An off-by-one is the worst version of this defect: it lands on a real line, so a reader does not
notice the citation is wrong, they just read the neighbouring rule and conclude something false.

## Why now

Nothing mechanical checks a `file:line` into a non-markdown asset — `check-links.py` resolves
links, and these are prose citations into CSS. The count in (a) has a test asserting the true
value, so the doc and the test suite already disagree in the repo.

## Done when

- [x] (a) resolved either way, with the reasoning written down and the number in the doc true of
      whatever capture it names.
- [x] (b), (c), (d) point at the lines that actually carry those `--brand` declarations, re-derived
      by running the grep rather than by applying "minus one".
- [x] `grep -rnE '\.(css|html|js|rs):[0-9]+' embarch-doc/embarch-ui/` — every other line citation in
      this sub-project's docs checked the same way, and anything else stale fixed in the same pass
      or named in the task file.
- [x] Gate green; `changelog.d/` fragment.

## Do not

Do not edit `style.css` to make a citation true, do not regenerate a fixture, and do not change the
`155` assertion in `trace.rs`. Every one of those makes the code follow the doc, which is backwards.

## Resolution — 2026-09-13, agent/ui/042-stale-pointers-in-decision-docs

**(a) — judgement taken: honest past-tense observation about a since-regenerated fixture, not a
never-true number.** Went to history rather than trusting the grep, per the dispatch note:

- `git log --follow --oneline -- embarch-ui/tests/fixtures/outpost-native-sim.trace.csv` shows
  exactly three commits: `fcf5c1e` (added), `d6877bd` (regenerated), `dc5de2b` (regenerated again,
  current).
- `git show <sha>:tests/fixtures/outpost-native-sim.trace.csv | grep -c ',marker,'` at each:
  `fcf5c1e` → **132**, `d6877bd` → 163, `dc5de2b` → **155** (today's value, matching `trace.rs:2874`
  and both committed fixtures).
- `git log --follow --format='%H %ci %s' -- embarch-ui/decisions/trace-view.md` (in this doc repo)
  shows the sentence containing "132" was present continuously since the file's creation
  (2026-09-02, itself a split of an older combined `decisions.md`) and every intermediate revision
  — it was never 155 and never edited to say otherwise. The 132 sentence and the 132 fixture commit
  (`fcf5c1e`, 2026-08-26, "Milestone 7 Phase D") line up in time; the two later regenerations
  (`d6877bd`, `dc5de2b`, both 2026-08-26/27, tied to the Layout 3 clock rework this same decision
  discusses two paragraphs later) postdate the prose and were never reflected back into it.

So this is `umbrella/058`'s shape exactly: a number true of an earlier state of the same committed
artifact, not a fabricated one. Fix applied: named which capture 132 was measured on, rather than
substituting 155 — `trace-view.md`:

> "Markers began as full-height rules and 132 across 760 ms swamped every span in the fixture as
> first committed — regenerated twice since, for Layout 3, to the 155 it holds now — so they became
> a tick in their own strip plus a faint rule;"

The `155` in `trace.rs:2874` and the fixtures are correctly left untouched — they were never the
defect.

**(b), (c), (d) — re-derived, all off-by-one confirmed and fixed.** `grep -n -- '--brand'
embarch-ui/assets/style.css` → `43:--brand: oklch(63%…)` (dark), `72:--brand: oklch(56%…)` (light),
`123:color: var(--brand);` (the sidebar-wordmark use). `shell.md` cited 124/44/73; corrected to
123/43/72. `index.html:34` checked and left — it does carry the header glyph's second (`--brand`)
path, as cited.

**Sweep:** `grep -rnE '\.(css|html|js|rs):[0-9]+' embarch-doc/embarch-ui/` returns exactly the one
`shell.md` line above (now corrected) — no other `file:line` citation into a non-markdown asset
exists anywhere else in this sub-project's docs.

**Gate:** `embarch-ui` `cargo build`/`test`/`clippy --all-targets -- -D warnings` green (doc-only
change, no code touched). `embarch-doc`'s `check-docs.py`: all green except
`check-doc-size.py`, which put `decisions/trace-view.md` into reserve (90.3%, 1,195 B left) as a
result of (a)'s added clause; filed as `tasks/ui/043-compact-ui.md` in this same commit, per
`tasks/README.md`'s compaction-task rule. `check-client-names.py --repo` and
`check-ownership.py --scope ui` (both worktrees) clean. `changelog.d/ui-stale-line-citations.fixed.md`
dropped.
