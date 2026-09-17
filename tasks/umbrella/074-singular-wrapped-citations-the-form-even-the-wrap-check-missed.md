# 074 — The 9 singular-wrapped citations: the form even `core/068`'s wrap-check could not see

**State:** done — leg 129, 2026-09-16. All 9 lines checked, 0 defects.
**Source:** leg 128's refill sweep, 2026-09-16, measured directly rather than inferred. `core/068`
found on 2026-09-16 that a citation wrapped across a comment continuation is invisible to a
line-based census, and its fix was the grep `grep -rlIE '[Dd]ecisions[[:space:]]*$'` — **plural
only**. Re-running it with the singular alternation, `grep -rInE '[Dd]ecisions?[[:space:]]*$'`,
finds **9 lines in 4 files** in this repo, and `umbrella/073`'s plural re-check (which closed clean
at 30 instances, 0 defects) could not have seen any of them — the plural grep found **nothing** here
at all.
**Scope:** umbrella
**Hardware:** none — Rust doc comments and inline comments in `install.rs`, `config.rs`,
`doctor.rs` and `locate.rs`. Nothing is built for a board, no probe, no live Core, no deploy, no
study, and `doctor` is not executed. Classified fresh at filing.
**Owner:** no

**Doc-size reserve for `umbrella`:** `embarch-umbrella/decisions/bind.md` (11,533/12,288 B) is in
the last 10% of its cap, filed as `tasks/umbrella/009-compact-docs.md`, **blocked**, due 2026-10-06.
This is a source-comment sweep and should not need to write it; if a finding belongs in `bind.md`,
spend the bytes and say so in your report rather than filing it in whichever decisions file has room
— that exact failure is on record (`embarch-api`, 96 bytes left, 2026-09-05). If your work pushes
any other `umbrella` doc into reserve, file `tasks/umbrella/<next free NNN>-compact-docs.md` in the
same commit per `tasks/README.md`. **`tasks/doc/` is not yours.**

## What

Nine lines, measured 2026-09-16 with
`grep -rInE '[Dd]ecisions?[[:space:]]*$' embarch-umbrella --include='*.rs' --include='*.toml'`,
target excluded:

```
src/install.rs:5        (decision 3's 2026-08-05 refinement) — reversed by decision
src/install.rs:422      computed by reading only — decision
src/config.rs:56        (`embarch-api` decision
src/config.rs:107       (`embarch-api` decision
src/doctor.rs:1350      (decision
src/doctor.rs:1459      (decision
src/doctor.rs:5368      (decision
src/locate.rs:311       (decision
src/locate.rs:349       (decision
```

The number lives on the **next** line — verified at filing for `src/config.rs:56-57`
(`/// 12)`) and `src/config.rs:107-108` (`/// 53)`).

Re-check each citation the way every sweep in this chain has: does the number resolve, does it
resolve in the repo the line names, and does the sentence around it still assert something true.

## Why now

**This is the first read of these lines, not a re-read.** `embarch-umbrella` has been declared
citation-swept, `umbrella/073` included; every one of those censuses used a grep that could not
match this form, and here the plural wrap-check returned zero, so the whole class was reported as
absent from this repo when nine instances of it were sitting in `src/`.

`src/install.rs:5` is the most interesting line in the list before anyone reads it: it cites one
decision by number **and** says a second decision reversed it, with that second number on the
continuation line. A reversal claim that names the wrong number is the kind of error
`embarch-decision-reversals.md` exists to prevent, and it is exactly the shape the census could not
see.

## Careful of

- **The repo-prefix trap.** `src/config.rs:56` and `:107` both cite **`embarch-api`** decisions, not
  this repo's, and both sit in a file whose whole purpose is mirroring `embarch-api`'s shape — so
  every nearby line names the other repo. Read the code to decide whose decision a number is, never
  the grep column.
- **`src/doctor.rs` is a very large file and three of the nine are in it.** Check the number, not
  the check's behaviour; `doctor`'s own live behaviour is a standing unpaid debt
  (`umbrella/037` check 13, `umbrella/033`'s check-17 arms, check 5's permission-denied probe) and
  is **not** yours to settle here.
- Do **not** reflow comment blocks wholesale to "fix" the wrapping. The wrap is not the defect; an
  unchecked citation is.

## Done when

- [x] All 9 lines checked, with the count of distinct decision instances behind them reported.
      9 lines cite 9 distinct (repo, number) decision instances: `install.rs:5` cites two —
      umbrella 3 and umbrella 28 — on one wrapped line; `install.rs:422` cites umbrella 21;
      `config.rs:56` cites `embarch-api` 12; `config.rs:107` cites `embarch-api` 53; `doctor.rs:1350`
      cites umbrella 17; `doctor.rs:1459` cites umbrella 23; `doctor.rs:5368` cites umbrella 8;
      `locate.rs:311` and `locate.rs:349` both cite umbrella 30 (the same instance twice, which is
      why 9 lines still total 9 distinct instances rather than 10). All 9 resolve, all in the repo
      the surrounding code actually means (the two `config.rs` lines are genuinely `embarch-api`'s,
      confirmed against `embarch-api/decisions/zephyr.md` decision 12 and
      `embarch-api/decisions/config-retirement.md` decision 53 — the repo-prefix trap did not fire),
      and every sentence around every citation is still true against the cited decision's text in
      `embarch-umbrella/decisions/{install,projects,mcp,topology}.md`.
- [x] `src/install.rs:5`'s reversal claim checked against `embarch-decision-reversals.md` as well as
      against this repo's own `decisions/` — both numbers, and the direction of the reversal.
      `decisions/install.md` decision 3 ("Replaced by decision 28") and decision 28 ("Reversing
      decision 3's sibling-lookup refinement... with the repo owner directly requesting the
      reversal") agree with each other and with the source comment's direction (3 reversed by 28,
      at the user's explicit request, over a `wsl-host` Core-path misreport) — both directions
      checked, no mismatch. `embarch-decision-reversals.md` and its four `reversals/rows-*.md` range
      files have no row citing umbrella decision 3 or 28 — this reversal is not one of the doc's
      catalogued shapes (its header: "every entry is handled correctly in its own owning doc; this
      page does not restate a correction's mechanism" — it collects instructive defect patterns
      found by a real build/install/capture or a documentation-pass review, not every ordinary
      superseded decision). Decision 3/28's reversal is fully and correctly recorded in its owning
      doc (`decisions/install.md`) already, same-day, by the repo owner's own request — nothing
      here matches the reversals doc's admission bar, so no row was added.
- [x] Every wrong number, dead reference or false sentence fixed; every line deliberately left
      alone named with the reason.
      All 9 lines left alone — 0 defects found. Reason, per line: `install.rs:5` (3→28 reversal
      verified correct both directions, see above); `install.rs:422` (decision 21 is exactly the
      `--dry-run` plan the comment describes); `config.rs:56` (`embarch-api` decision 12 is exactly
      the live-vs-static `Discovery` split the comment describes); `config.rs:107` (`embarch-api`
      decision 53 is exactly the `[[projects.targets]]` retirement the comment describes);
      `doctor.rs:1350` (decision 17 is exactly the "chip has nowhere to be written down, resolved
      per call" the comment describes); `doctor.rs:1459` (decision 23 is exactly the "timeout
      outcome reported distinctly" / "assumed, not measured" budget the comment describes);
      `doctor.rs:5368` (decision 8 is exactly the "no remote orchestration" the comment describes);
      `locate.rs:311` and `:349` (decision 30 is exactly the WSL2-guest Windows-service-first probe
      both comments describe).
- [x] The measurement repeated after the edits, so the closing report states a number rather than
      an impression. Re-run after review (no edits made, so unchanged):
      `grep -rInE '[Dd]ecisions?[[:space:]]*$' embarch-umbrella --include='*.rs' --include='*.toml'`
      still returns the same 9 lines in the same 4 files.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build --all-targets`,
      `cargo test`, `cargo clippy --all-targets -- -D warnings` in `embarch-umbrella`, and
      `check-docs.py` in `embarch-doc`.
- [x] `changelog.d/` fragment dropped. No decision is created or amended unless you find one that
      is actually wrong, in which case say so rather than editing quietly.
      No decision was wrong, so none was amended. Fragment:
      `changelog.d/umbrella-singular-wrapped-citation-sweep.changed.md`.
