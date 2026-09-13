# 036 — Three dead citations inside `embarch-topology`'s own source comments

**State:** open
**Source:** leg 106 refill sweep, 2026-09-13, scout-verified. Re-derive each target rather than
trusting the quotes.
**Scope:** topology
**Hardware:** none — three comments in two source files. No behaviour changes.
**Owner:** no

## What

**(a) A wrong decision number, and it was never right.** `src/hardware/hardware_id.rs:45` —
`ChipFamily`'s doc comment says *"One classifier decides both questions so they cannot disagree —
see topology decision 22 and task `topology/007`, which this type closes."*

Decision 22 is *"A remote Core's declared host stays with each consumer"*
(`embarch-doc/embarch-topology/decisions/scope.md:29`) — unrelated. The classifier is decision
**25** (`embarch-doc/embarch-topology/decisions/validation-classifier.md:9`), and it was 25 from
birth: `git log --oneline --follow -- embarch-topology/decisions/validation-classifier.md` →
`a40fd32 topology/007: decision 25 for the shared chip classifier`. So this is a mis-citation from
the first commit, **not** a number that moved — say so in the fix, because the two have different
implications for whether anything else is wrong nearby.

**(b) and (c) Two `file:line` citations past the end of their targets.** `bin/main.rs:147` cites
`embarch-core/decisions/platform.md:46` and `:150` cites `embarch-core/decisions/surfaces.md:30`.
Those files are **36** and **29** lines long (`wc -l`), so both point past the end. The scout
believes the `Arc<Mutex<()>>` hw-lock text (a)'s neighbour meant is now at `platform.md:32`,
**inferred from content and explicitly not verified** — re-derive it. The `surfaces.md` target was
not identified at all.

## Why now

Nothing mechanical can see any of these. `check-decision-refs.py` and `check-links.py` walk
`embarch-doc/*.md` only, so a decision number or a file citation inside a repo's own source
comments is unchecked by anything in the suite — which is also why this class keeps recurring
(`dev-bench/019`–`022`, `ui/033`/`039`, `core/008`, `outpost/019`). `tasks/doc/033` and
`tasks/doc/044` are the owner-reserved half of the general fix.

## Done when

- [ ] `hardware_id.rs:45` cites decision **25**, with the number re-confirmed against
      `embarch-doc/embarch-topology/decisions.md`'s index, and the comment says the citation was
      wrong from the start rather than implying a renumber.
- [ ] Both `bin/main.rs` citations resolve to a line that exists and carries the text the sentence
      is about. **A line number you could not identify is left un-guessed**: drop the citation to a
      file-and-section form, or say in your report that you could not resolve it. Never point a
      citation at a plausible-looking line.
- [ ] `grep -rn 'decision [0-9]' embarch-topology/src embarch-topology/bin` — every hit checked
      against the owning repo's `decisions.md` index, and anything else wrong is fixed in the same
      pass or reported.
- [ ] `grep -rnE '\.md:[0-9]+' embarch-topology/src embarch-topology/bin` — every hit's line number
      checked against the target's length.
- [ ] Gate green (`cargo build`/`test`/`clippy --all-targets -- -D warnings`); `changelog.d/`
      fragment.

## Do not

Do not change a decision's number anywhere, and do not edit `embarch-core`'s docs to match a
citation — the citation is what is wrong.
