# 042 — Four stale pointers in `embarch-ui`'s decision docs: a marker count and three CSS line numbers

**State:** claimed — leg 107, unit 3, 2026-09-13.
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

- [ ] (a) resolved either way, with the reasoning written down and the number in the doc true of
      whatever capture it names.
- [ ] (b), (c), (d) point at the lines that actually carry those `--brand` declarations, re-derived
      by running the grep rather than by applying "minus one".
- [ ] `grep -rnE '\.(css|html|js|rs):[0-9]+' embarch-doc/embarch-ui/` — every other line citation in
      this sub-project's docs checked the same way, and anything else stale fixed in the same pass
      or named in the task file.
- [ ] Gate green; `changelog.d/` fragment.

## Do not

Do not edit `style.css` to make a citation true, do not regenerate a fixture, and do not change the
`155` assertion in `trace.rs`. Every one of those makes the code follow the doc, which is backwards.
