# 219 — verify judges a refused Exchange step under its recorded target

**State:** claimed by agent/api/219-verify-judges-a-refused-exchange-step-under-its-recorded-target, 2026-11-26 22:55
**Source:** EMB-589 — verify reads a refused Exchange step both ways though Core records its target
**Issue:** EMB-589
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`verify` check 3 (api decision 146) recomputes a Test run's verdicts through a
copy of Core's `judge_steps` in `src/verify_test.rs`. Its doc comment says why
it reads some steps both ways: "**A signal's target is Core's live topology and
is in no file of the zip**". `judge_with_targets` then judges the run under
every bench/DUT assignment of the signals whose step was refused, timed out or
`until`-not-seen, and answers partial when the readings disagree.

That is no longer true for a record Core wrote since core decision 155
(`core/180`). Quoted from `embarch-doc/embarch-core/interfaces/host-studies.md`:
"an `Exchange` row also `signal` (the name it addressed) and `target`
(`dut`|`bench`, what that signal addressed when the step ended, from the lookup
the Test run's verdict reads back; decision 155)". Those rows are the `steps`
of `events.json`, which a signed record covers. Both keys appear on `Exchange`
rows only and are absent from rows Core wrote before 155.

When this is done, an `Exchange` step row carrying `target` is judged under
that target alone, its signal never enters `unknown`, and a run whose every
ambiguous step carries one recomputes to one reading: pass or fail, never the
partial. A row without `target` keeps today's both-ways reading. An
`Instrument` step stays `Bench` as today. If a row's `signal` disagrees with the
step's action in `study.json`, say in the decision what check 3 does (fail
naming the step is the expected answer; a signed file contradicting itself is
not a reading to pick between).

**Not yours:** `embarch-core` and its docs; `embarch-core-client` needs no
change. The comment block's file header cites Core's `test_publish.rs` as read
on a date; re-read Core's `judge_steps` on `origin/main` (it now reads the row's
`target` first, `core/180`) and keep the copy in step with it.

## Where to look

- `src/verify_test.rs`: `judge_steps`, `judge_with_targets`,
  `MAX_AMBIGUOUS_SIGNALS`, and the fixture zips the check-3 tests build.
- `embarch-core/src/test_executor.rs` on `origin/main` (`judge_steps`,
  `target_of`), the source the copy follows.
- `embarch-doc/embarch-core/decisions/test-run-target.md` (155),
  `embarch-doc/embarch-api/decisions/verify-test-run.md` (146),
  `embarch-doc/embarch-api/interfaces/verify.md` (check 3's row).

## Where the doc goes

A new api decision (149 is the next free number at the time of writing; take the
next free one when you write it, found by scanning the headings as
`DOC-CONVENTIONS.md` says, and cite only that
number in code comments: three recent api units cited a task number or a
neighbour's decision instead), or an in-place amendment of 146 if it stays
under the per-decision cap. `interfaces/verify.md`'s check 3 row says a
recorded target is used. **`spec.md` is 9,066 B, 27 B into reserve**, and
`tasks/api/218` already carries that debt: do not add to `spec.md` unless a
sentence there is now false; if you must, the debt stays with 218 and you say so
in your report.

## Done when

- [ ] A fixture Test zip whose refused `Exchange` step row carries `target`
      verifies check 3 as pass or fail under that target, not partial; one
      fixture each for `dut` and `bench`.
- [ ] A row without `target` still reads both ways, as today (an existing test
      may already pin it; name it).
- [ ] Gate green (`cargo build --workspace`, `cargo test --workspace`,
      `cargo clippy --workspace --all-targets -- -D warnings`).
- [ ] Decision and index row (or 146 amended), `interfaces/verify.md` row,
      `changelog.d/` fragment.
