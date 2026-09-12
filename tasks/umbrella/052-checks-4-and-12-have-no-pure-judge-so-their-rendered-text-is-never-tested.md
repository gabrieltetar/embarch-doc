# 052 — Checks 4 and 12 have no pure judge, so the guard that exists because a check shipped eighteen stray spaces cannot see them

**State:** done — leg 084, 2026-09-11
**Source:** leg 084's refill sweep off [`embarch-umbrella/open.md`](../../embarch-umbrella/open.md),
2026-09-11. Source-confirmed against `embarch-umbrella/src/doctor.rs`'s `pure_verdicts()` header
before filing.
**Scope:** umbrella
**Hardware:** none — the whole point is to reach these two checks **without** a live Core.
**Owner:** no

**Reserve in `embarch-umbrella` at dispatch (leg 084):** `decisions/bind.md` 11,447/12,288 B
(93.2%, `tasks/umbrella/009`, parked), `decisions/doctor.md` 11,082/12,288 B (90.2%,
`tasks/umbrella/048`, parked on `In flux: yes`), `open.md` 4,306/5,120 B (84.1%,
`tasks/umbrella/038`, parked). **If — and only if — this unit turns out to owe a numbered decision
that belongs in `decisions/doctor.md`**, you are the actor making that file's flux, so compact it as
part of this unit: carry `tasks/umbrella/048`'s `Must not delete:` list verbatim, close only that
file's item, and say what you cut. Otherwise leave all three alone. If your work leaves any
`embarch-umbrella` file in reserve that nothing has filed, file
`tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit.

## What

`doctor.rs`'s stray-space guard runs over the rendered text of every verdict `pure_verdicts()` can
build, and its own header says why it has to be a corpus rather than a per-arm assertion: a
`\`-continued literal wrapped without the `\` keeps the newline *and* the next line's indentation,
so the run of spaces lands in the rendered sentence while every `contains` assertion on a fragment
either side of the break still passes. **Check 14's two skip arms each shipped eighteen stray
spaces, and the second survived the first's fix** (`81e20f4`, then `umbrella/024`) for exactly that
reason.

The header then names its own blind spot, verbatim:

> **The two checks it cannot reach.** Checks 4 and 12 have no pure judge: both are `async` and
> decide nothing without a live Core, so their text is absent from this corpus and this test claims
> nothing about it.

So the two checks whose text nothing tests are the ones whose text nothing *can* test — and the
defect class this guard exists for is a text-rendering defect, which has nothing to do with whether
a Core is reachable.

## Why now

`umbrella/031` already normalised both checks' bodies at the interpolation points check 1 needed
fixed. That was the cheap half and it is done; what stayed open is the **untestability**, which is
the half that stops the next regression rather than the last one. `open.md`'s own bullet says this
in as many words.

Check 16 is the worked precedent sitting in the same file: it goes through `judge_growth` rather
than `check_growth`, because the wrapper resolves a real data directory that every test in the
module is forbidden to touch (decision 39), so the notes the wrapper composes are passed into the
judge instead. **Checks 4 and 12 want the same seam**, and it already has a name and a rationale in
this repo.

## Done when

- [x] Checks 4 and 12 each have a **pure judge** — a synchronous function taking the facts the
      `async` half gathers and returning the `Check`, with the `async` half reduced to gathering
      and calling it. Follow `judge_growth`/`check_growth` rather than inventing a second shape.
      Done as `judge_token(TokenAttempt)` and `judge_dev_bench(DevBenchAttempt)`: each attempt enum
      has one variant per outcome the `async` half can gather (a missing winner, a token-resolution
      error, one `authed_get` result), and `check_token`/`check_dev_bench` are reduced to gathering
      and matching straight into the judge.
- [x] **Both checks' verdict text is in `pure_verdicts()`**, every arm of it, so the stray-space
      guard covers them. All 7 arms of `TokenAttempt` and all 7 of `DevBenchAttempt` are pushed into
      the corpus (check 4's `Ok200` arm exercised once with well-formed JSON and once with a body
      that fails to parse, since both reach the same Pass text). No arm needed fabricating a fact —
      every one is reachable from data the gathering step could plausibly have produced.
- [x] The `pure_verdicts()` header's *"The two checks it cannot reach"* paragraph is **rewritten to
      match reality**, not deleted: it is the record of why the corpus is shaped this way, and a
      later reader who finds a blind-spot warning describing a blind spot that no longer exists
      will assume the guard is weaker than it is. Replaced with a paragraph naming `judge_token`/
      `judge_dev_bench` as the same gather-then-judge split `judge_growth` already uses.
- [x] `embarch-umbrella/open.md`'s bullet is closed or narrowed to whatever is genuinely left.
      Closed outright — the guard now reaches both checks and `umbrella/031`'s normalisation is
      already landed, so nothing about this bullet was still open.
- [x] A numbered decision **only if** the seam you choose differs materially from `judge_growth`'s;
      if it is the same shape applied twice more, that is an implementation, not a decision. Same
      shape applied twice more — no decision filed.
- [x] Gate green: `cargo build` / `test` / `clippy --all-targets -- -D warnings` in
      `embarch-umbrella`, and `python3 scripts/check-docs.py` in the doc repo. All green (226 tests
      pass, `no_check_renders_a_run_of_two_or_more_spaces` now covers checks 1-17 with no offenders
      found in checks 4 or 12's text — nothing was shipping a stray space).

## Result

No stray spaces were found in checks 4 or 12's rendered text once split out — the guard now covers
17 of 17 checks with a clean pass, so there was no pre-existing defect to fix here (unlike check 14's
history). `decisions/doctor.md` and `decisions/bind.md` were left alone: no numbered decision was
owed by this unit, so the reserve/compaction condition in the dispatch note did not trigger.

## What this may not do

- **Do not make either check reach a network, a Core or a bench in a test.** Decision 39 forbids
  it and the guard is worthless if buying coverage costs the test its purity — that trade is the
  reason check 16 got a judge instead of a fixture.
- **Do not relax the guard to make it pass.** If splitting these checks out surfaces stray spaces
  that are already shipping, that is the guard working: fix the text and say in the task file what
  it rendered as before.
