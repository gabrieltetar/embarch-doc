# 036 — Three dead citations inside `embarch-topology`'s own source comments

**State:** done — leg 107, unit 2, 2026-09-13; see "Closed" at the bottom.
**Doc-size reserve for `topology`:** nothing in `embarch-topology`'s docs is in reserve. If your
work pushes a file into the last 10% of its cap, file `tasks/topology/<NNN>-compact-topology.md`
in the same commit.
**Source:** leg 106 refill sweep, 2026-09-13, scout-verified. Re-derive each target rather than
trusting the quotes. **"Scout-verified" is one reader, and it has already been wrong once:** the
same scout, in the same sweep, reported a quoted `state.rs` comment as never having existed
(`umbrella/058`) when it had existed and was later rewritten — caught only because that worker went
to the history. **Expect one framing in ten to be wrong**, and in particular expect
"was never right" and "was right and moved" to be confused, because they look identical to a grep.
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

- [x] `hardware_id.rs:45` cites decision **25**, with the number re-confirmed against
      `embarch-doc/embarch-topology/decisions.md`'s index, and the comment says the citation was
      wrong from the start rather than implying a renumber.
- [x] Both `bin/main.rs` citations resolve to a line that exists and carries the text the sentence
      is about. **A line number you could not identify is left un-guessed**: drop the citation to a
      file-and-section form, or say in your report that you could not resolve it. Never point a
      citation at a plausible-looking line.
- [x] `grep -rn 'decision [0-9]' embarch-topology/src embarch-topology/bin` — every hit checked
      against the owning repo's `decisions.md` index, and anything else wrong is fixed in the same
      pass or reported.
- [x] `grep -rnE '\.md:[0-9]+' embarch-topology/src embarch-topology/bin` — every hit's line number
      checked against the target's length.
- [x] Gate green (`cargo build`/`test`/`clippy --all-targets -- -D warnings`); `changelog.d/`
      fragment.

## Closed 2026-09-13, leg 107

All three named citations fixed, plus a fourth found by the required grep sweep (not named in the
task): `hardware/enrollment.rs:40` cited `embarch-core decision 21's port migration` — decision 21
is "Plain attach, not attach_under_reset", unrelated; the correct target is `embarch-core` decision
27, "`POST /dev-bench/link`, declaring the runtime link as its own fact" (`decisions/enrollment.md`).

Re-derivation, not trust, on both flagged targets:
- `platform.md:32` (the scout's unverified guess) — **confirmed**: `Arc<Mutex<()>>` appears
  literally only at that line, inside decision 14's paragraph ("`hw_lock` stayed `Arc<Mutex<()>>`;
  a second, plain `std::sync::Mutex<Option<String>>` field...").
- `surfaces.md:30` (never identified) — **resolved to `:17`**, decision 12's paragraph ("Plain-text
  errors suit a human... Still worth building, and deliberately not built here"), which is what "no
  message" in the source sentence is about (the deferred `{code, message, cause}` body).

Full sweep of every `decision [0-9]` and `.md:[0-9]+` hit in `embarch-topology/src` and
`embarch-topology/bin` (topology's own decisions plus cross-repo cites into `embarch-core`,
`embarch-ui`, `embarch-study-designer`, `embarch-outpost`) checked against each owning repo's
`decisions.md` index/headers. No other mismatch found. No decision renumbered anywhere; no
`embarch-core` doc touched. Gate green: `cargo build`/`test` (79 tests)/`clippy --all-targets
--all-features -- -D warnings` clean. `changelog.d/topology-dead-source-citations.fixed.md` filed.
Doc-size reserve untouched (comment-only fix, no doc file edited).

## Do not

Do not change a decision's number anywhere, and do not edit `embarch-core`'s docs to match a
citation — the citation is what is wrong.
