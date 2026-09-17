# 069 — The 15 singular-wrapped citations: the form `core/068`'s own wrap-check could not see

**State:** done — 15 lines checked (25 distinct decision instances); one real defect found and
fixed (`src/outpost_load.rs`'s misattributed `embarch-ui` decision citation for the study-step
row); the three `decision 30(b)`/`30(c)` sub-letter citations verified cross-consistent and left
alone. Gate green. See `## Done when` for the full breakdown.
**Source:** leg 128's refill sweep, 2026-09-16, measured directly rather than inferred. `core/068`
is the unit that *discovered* the wrapped-citation blind spot and fixed it with
`grep -rlIE '[Dd]ecisions[[:space:]]*$'` — **plural only**. Re-running it with the singular
alternation, `grep -rInE '[Dd]ecisions?[[:space:]]*$'`, finds **15 lines in 6 files** in this repo,
and `core/068`'s own re-check (15 lines / 37 instances, 0 defects) could not have seen any line that
wraps after the singular word.
**Scope:** core
**Hardware:** none — Rust doc comments and inline comments. Nothing is built for a board, no probe,
no live Core, no deploy, no study. Classified fresh at filing.
**Owner:** no

**Doc-size reserve for `core`:** `embarch-core/decisions/auth.md` (11,356/12,288 B) is in the last
10% of its cap, filed as `tasks/core/046-compact-core.md`, **blocked**, due 2026-09-26. This is a
source-comment sweep and should not need to write it; if a finding belongs in `auth.md`, spend the
bytes and say so in your report rather than filing it in whichever decisions file has room — that
exact failure is on record (`embarch-api`, 96 bytes left, 2026-09-05). If your work pushes any other
`core` doc into reserve, file `tasks/core/<next free NNN>-compact-core.md` in the same commit per
`tasks/README.md`. **`tasks/doc/` is not yours.**

## What

Fifteen lines, measured 2026-09-16 with
`grep -rInE '[Dd]ecisions?[[:space:]]*$' embarch-core --include='*.rs' --include='*.toml'`, target
excluded:

```
src/outpost_load.rs:13        that file's own decision
src/outpost_manifest.rs:3     `embarch-outpost` decision 9, and this crate's own decision
src/stream_store.rs:60        (`embarch-study-designer` decision
src/stream_store.rs:737       (decision
src/api.rs:1161               this decision
src/elevate.rs:159            per decision
src/study.rs:408              the thing that decision
src/study.rs:460              `embarch-topology` decision 3 forbids and which decision
src/study.rs:629              since decision
src/study.rs:884              §3 decision
src/study.rs:1072             (`embarch-study-designer` decisions
src/study.rs:1084             (`embarch-study-designer` decisions
src/study.rs:1334             (decision
src/study.rs:2313             (`embarch-outpost` decisions
src/study.rs:3689             (`embarch-study-designer` decisions
```

The number lives on the **next** line. Nine of the fifteen are in `src/study.rs`, and five of those
cite a *different* repo.

Re-check each citation the way every sweep in this chain has: does the number resolve, does it
resolve in the repo the line names, and does the sentence around it still assert something true.

## Why now

**This is the first read of these lines, not a re-read.** `embarch-core` has been declared swept
repeatedly, `core/068` included; every one of those censuses used a grep that could not match this
form. `ui/061` found on the same day that a citation whose numbers all resolve can still assert a
false relationship, and `topology/050` found a false sentence two paragraphs above the file's own
correction of it — so a resolving number is not a clean line.

## Careful of

- **The repo-prefix trap, in its sharpest form.** `src/outpost_manifest.rs:3` and `src/study.rs:460`
  each name *two* repos' decisions in one wrapped sentence, so the prefix and the number sit on
  different lines with another repo's name between them. Read the code to decide whose decision a
  number is, never the grep column.
- `src/outpost_manifest.rs:3-4` continues `//! 30(c)` — a **sub-lettered** decision reference. Check
  that the sub-letter still exists in the decision as written today before treating the line as
  clean.
- Do **not** reflow comment blocks wholesale to "fix" the wrapping. The wrap is not the defect; an
  unchecked citation is.

## Done when

- [x] All 15 lines checked, with the count of distinct decision instances behind them reported.
      25 distinct decision instances behind the 15 lines (some lines cite 2-5 decisions in one
      sentence). See closing report.
- [x] Every wrong number, dead reference or false sentence fixed; every line deliberately left
      alone named with the reason.
      One real defect: `src/outpost_load.rs:13-14` attributed "the study-step row" to
      `embarch-ui` decision 18 (trace-transfer.md, server-side binning/payload) when it is actually
      decision 10's chart half (trace-chart.md: "Vertical scroll with the axis and step row
      pinned"). Fixed by splitting the citation between the two decisions. The other 14 lines
      resolved, matched their repo, and their sentences held up against the cited text —
      including the three `decision 30(b)`/`30(c)` sub-letter citations
      (`outpost_manifest.rs:3-4`, `study.rs:460-461`/`1334`, `stream_store.rs:737-738`), which have
      no literal `(a)/(b)/(c)` markup anywhere in `decisions/streams.md` (checked both the current
      text and the pre-`core/063`-compaction version) but are cross-consistent across four
      independent citations — three source sites plus `embarch-doc/reversals/rows-1-50.md` row 45
      — all landing on the same two paragraphs, so left as an observed fragility rather than a
      fix (see closing report).
- [x] The measurement repeated after the edits: `grep -rInE '[Dd]ecisions?[[:space:]]*$'` now finds
      **14 lines** (was 15) — the fix moved `outpost_load.rs`'s citation onto one line, so it no
      longer wraps.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build --all-targets`,
      `cargo test` (209 passed, 0 failed, 2 ignored), `cargo clippy --all-targets -- -D warnings`
      (clean) in `embarch-core`, and `check-docs.py` (11/11 green) in `embarch-doc`. The change is
      a doc-comment edit only, not platform-conditional; the native-Windows build debt
      (`core/015`) is untouched by this unit.
- [x] `changelog.d/core-singular-wrapped-citations.fixed.md` dropped. No decision created or
      amended — the one real defect found was a source-comment misattribution, not a wrong
      decision text, so nothing in `embarch-ui`'s or `embarch-core`'s decisions files needed
      touching.
