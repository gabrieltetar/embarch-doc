# 050 — Plural-citation re-check: the 12 lines every `topology` sweep was structurally blind to

**State:** done
**Source:** leg 125's refill sweep, 2026-09-16, acting on the measurement
`inbox/citation-census-grep-cannot-see-a-plural-citation.md` asked for and nobody had run.
`embarch-topology` was declared **completely** citation-swept after `topology/040`, `046` and `049`.
**Every one of those sweeps censused with `grep -cE '[Dd]ecision [0-9]'`, which cannot match
`decisions 3, 9` or `decisions 10/11`** — so these lines were never in any sweep's input at all.
This is not a re-read of checked work; it is the first read, and "completely swept" was measured
with an instrument that could not see this form.
**Scope:** topology
**Hardware:** none — doc comments and one workflow comment. Nothing is built for a board, no probe,
no live Core, no deploy, no study. Classified fresh at filing.
**Owner:** no

**Doc-size reserve for `topology`: nothing in reserve.** `embarch-topology`'s files are all clear
after `topology/043`, `044` and `048`. If your work pushes a `topology` doc into the last 10% of its
cap, file `tasks/topology/<next free NNN>-compact-topology.md` in the same commit per
`tasks/README.md`. **`tasks/doc/` is not yours.**

## What

Twelve lines, measured 2026-09-16 with `grep -rInE '[Dd]ecisions [0-9]'` over the repo excluding
`.git` and `target`:

```
src/lib.rs:11                     (decisions 5, 8)         bare — own repo
src/software.rs:3                 decisions 3, 4, 11       bare — own repo
src/hardware/mod.rs:131           (decisions 17, 18)       bare — own repo
src/hardware/mod.rs:148           (decisions 3, 9 — no env var overrides any more)
src/hardware/mod.rs:227           (decisions 8, ...)       check the full line, it wraps
src/hardware/signal.rs:29         matching decisions 10/11
src/hardware/signal.rs:199        (decisions 3, 9)
src/hardware/hardware_id.rs:6     (decisions 2, 4)
.github/workflows/release.yml:22  embarch-umbrella decisions 27/29
src/hardware/port.rs:3            (decisions 2, 4)
src/hardware/port.rs:590          (decisions 3, 9)
src/hardware/validate.rs:2        (decisions 2, 8)
```

**Twelve lines, roughly 25 distinct decision instances** — every line cites two or three numbers and
each number is its own claim. Treat the line count as a floor and report the instance count you
actually checked. `src/hardware/mod.rs:227` wraps; read the whole comment, not the grep hit.

**Eleven of the twelve are bare** — no repo prefix — and this repo is the one where that is most
likely to be right, since these sit in `embarch-topology`'s own source citing its own decisions.
Confirm rather than assume: the chain's standing rule is that a bare `decision NN` in another
sub-project's file means *that* sub-project's NN, and this repo is cited by four others.

## How

Same pass the chain has run eleven times, unchanged except for the census pattern:

1. **Re-census with `[Dd]ecisions? [0-9]`, case-insensitively.** `ui/054` found two sites spelled
   `Decision` at the start of a sentence that a case-sensitive grep skipped. Report your number
   against the twelve above.
2. **For each cited number, check the decision exists in the file the citation points at.**
3. **Then read the cited decision's current text and check the sentence around the citation is
   still true of it.** This is the half that finds real defects: `api/102` found a comment citing a
   real, existing, topically wrong decision, and `study-designer/054` found a citation that was
   correct when written and went false when another repo amended the decision it cited. A number
   that resolves is not the same as a sentence that holds. `src/hardware/mod.rs:148`'s parenthetical
   — *"no env var overrides any more"* — is a factual claim about current behaviour as well as a
   citation, so check it against the code too.
4. **Fix wrong numbers and false sentences. Do not widen.** A wrong number that is not a decision
   citation is a finding for `inbox/`, not an edit.

## Done when

Every plural-form citation line in `embarch-topology` has had the existence-and-truth pass, the
report states the instance count checked against the twelve-line floor, and each defect found is
either fixed here or filed with its reason for not being fixed here.

## Result, 2026-09-16

Re-censused with `[Dd]ecisions? [0-9]` case-insensitively: same twelve lines, no additional
case-variant sites (no bare `Decision` sentence-openers here, unlike `ui/054`).

Ran `core/068`'s wrap-check, `grep -rlIE '[Dd]ecisions[[:space:]]*$'`, over this repo: **two hits**,
neither in the original twelve — `src/lib.rs:8-9` (wraps to `decisions\n2, 3`) and
`src/hardware/enrollment.rs:3-4` (wraps to `decisions\n2, 3, 7`). Both read and checked below.
`src/hardware/mod.rs:227` (already in the twelve) also wraps, as the task file noted; read in full.

**14 lines, 30 distinct decision instances checked** (12 lines / ~25 instances from the task,
plus the 2 wrapped lines the wrap-check found, 2 and 3 instances respectively).

Existence: every cited number resolves in `embarch-topology/decisions.md` and its
`decisions/*.md` group files (1 through 33 all present), and the one cross-repo citation —
`.github/workflows/release.yml:22`, `embarch-umbrella` decisions 27/29 — checked against
`embarch-umbrella/decisions/release.md`: both numbers exist, one entry ("A release-CI job
asserts each repo's `Cargo.toml` version matches its pushed tag"), and the comment's own words
match it closely. Zero wrong numbers.

Classification: eleven of the twelve original lines are genuinely bare/own-repo, confirmed by
reading the code around each, not the task file's column. One followed the trap the task file
named directly: `src/hardware/enrollment.rs:3-4` sits one line after `` `embarch-core`'s own
`known_boards.rs` / `known_boards.toml` `` — but decisions 2, 3 and 7 read against
`decisions/crate.md` and `decisions/scope.md` are `embarch-topology`'s *own* decisions about the
move (decision 3's "the only state that still needs writing is a human's declared intent... it
lives inside the crate's own storage" is close to verbatim the enrollment.toml sentence it
sits beside) — so the repo-prefix proximity does not make this a cross-repo citation, and the
existing bare classification (extended to this new line) holds.

**One false sentence, fixed.** `src/hardware/validate.rs:2-6` ("formerly `embarch-core`'s own
`board_gate.rs` (decisions 2, 8). One implementation, multiple call sites: ... and so does
`embarch-topology`'s own CLI/UI") claimed `embarch-topology` still has its own UI. It doesn't:
the UI (`bin/ui.rs`, the `Ui` subcommand) was retired outright 2026-08-24 (decision 5;
`bin/main.rs`'s own header says so), and the same `validate.rs` file's *own* later paragraph
(lines 12-14) correctly says `embarch-ui` polls the alert log instead — the file already knew,
two paragraphs down, that the sentence two paragraphs up was stale. Traced via `git log -L`: the
line dates to the 2026-08-21 scaffold commit, when a UI genuinely existed, and survived two later
sweeps (`2026-09-07`, `topology/040` on `2026-09-13`) that touched this exact doc-comment for
other reasons without catching it. Fixed to say "own CLI" and added a one-line pointer to
decision 5's retirement, so a future reader isn't left to notice the same contradiction. The two
decision numbers themselves (2, 8) were already correct and are untouched.

Everything else — all ten remaining bare lines, the wrapped `lib.rs:8-9`, and the cross-repo
`release.yml:22` line — checked existence and sentence-truth clean; no other edits.

Not fixed here, and not filed to `inbox/` either: `Cargo.toml:48`'s `` `bin` (this crate's own
CLI/UI binary) `` comment has the identical stale "CLI/UI" wording as the `validate.rs` line just
fixed, but it cites no decision number, so it falls outside this task's plural-citation-line
mandate; noting it here rather than widening the edit.

**Tally: 14 lines / 30 distinct decision instances / 0 wrong numbers / 1 false sentence (fixed).**
