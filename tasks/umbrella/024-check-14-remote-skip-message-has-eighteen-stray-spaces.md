# Fix check 14's `Remote` skip message — eighteen stray spaces from a wrapped literal

**State:** done
**Source:** owner's repo survey, 2026-09-06 — the sibling arm of a defect commit `81e20f4` already fixed once
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`src/doctor.rs:2898` renders `"…can say which                  flashing program it would resolve
there"`. Commit `81e20f4` ("doctor check 14: the skip message loses eighteen stray spaces from a
wrapped literal") fixed the **`WslHost` arm one line below** and left this one. The existing test at
`src/doctor.rs:3721` asserts `detail.contains("another machine")`, so it passes straight over the
malformed string.

Make the `Remote` arm a `\`-continued literal like its sibling, and add a test that walks every
`Check` produced by the module's pure judges and **fails on any run of two or more spaces** in
`detail` or `fix` — so the next wrapped literal cannot reintroduce this in any of the seventeen
checks. `doctor` output is otherwise unchanged.

## Why now

`spec.md`'s check table makes check 14's skip text the only thing a `remote` operator gets from that
check, and `decisions/doctor.md` 31 and 38 exist precisely so a skip arm "says what is missing"
legibly. The same defect has already been fixed once in the same function, and nothing guards it.

## Done when

- [x] `doctor.rs:2898` is a `\`-continued literal; the rendered detail has no multi-space run.
- [x] A new test fails on `"  "` in any check's `detail` or `fix` —
      `doctor::tests::no_check_renders_a_run_of_two_or_more_spaces`, over a corpus of every
      verdict the module's pure judges emit for checks 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 14,
      15, 16 and 17. The covered set is asserted, so an emptied corpus fails rather than passes.
- [x] That test is shown to fail against the current string (reverted locally, confirmed,
      restored). It named `check 14 detail` and the exact eighteen-space string; the existing
      `check_14_says_why_it_cannot_run_without_pointing_at_check_1` stayed **green** against the
      same defect, which is the mistake this task named. That assertion now reads a fragment
      **spanning** the wrap.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md` and `open.md` updated, `changelog.d/` fragment dropped. **No `status.d/`
      fragment**: nothing suite-level states check 14's skip text or `doctor`'s message shape.
      **No `features.d/` row**: nothing shipped, retired or changed maturity.

## Two findings the guard turned up, and what was done

1. **Check 2's `local` fix line carried a hand-set three-space gap** —
   `sudo "…" install   (or, if already installed: …)`. Not a wrapped literal, but the guard
   cannot tell one from the other, and an exception spelled out in code is worth less than the
   guard. Narrowed to one space. **This is the one rendered change beyond check 14**, and it is
   whitespace only.
2. **Check 6's detail is exempt, pinned to check 6 alone.** It renders `{e:#}` of a `toml`
   parse error verbatim, caret diagram and all, whose alignment *is* multi-space runs. The
   exemption is "text containing a newline", justified by nothing in the module authoring a
   multi-line message and by the defect never producing a newline — and the test asserts the
   exempt set is exactly `[6]`, so it cannot widen quietly.

## Not covered, and why

**Checks 4 and 12 are outside the guard.** Both are `async` and decide nothing without a live
Core, so neither has a pure judge that can be handed inputs — no corpus assembled without a
network can reach their text. Recorded in [open.md](../../embarch-umbrella/open.md); splitting a
pure judge out of either is the fix.

**Check 16 goes through `judge_growth`, not `check_growth`.** The wrapper resolves a *real* data
directory, which every test in this module is forbidden to do (decision 39), so the three notes
the wrapper composes are passed to the judge instead. If someone edits one of those note strings
in `check_growth`, the copy in the test does not follow.
