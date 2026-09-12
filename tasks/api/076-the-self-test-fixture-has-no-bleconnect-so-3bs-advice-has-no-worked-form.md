# 076 — The self-test fixture has no `BleConnect`, so the guide's `target_address` advice has no worked form

**State:** open
**Source:** split out of `tasks/suite/012` by leg 094, 2026-09-12, which took the worked-example arm
and left this one. `suite/studies-guide.md` §3b: "a real study sets `target_address` or
`target_name`" — and no file in the tree shows one.
**Scope:** api
**Hardware:** none to author and round-trip the JSON. **Running it against a DUT is a bench matter
and is not this task.**
**Owner:** no

## What

`embarch-api/tests/fixtures/self_test_study.json` is now the suite's canonical worked study
(`suite/012`, `embarch-study-designer/interfaces/types.md`). It is two `BleAdvertise` steps, which
is exactly the study that has been run green — **and that is precisely why it does not show the one
thing a real study needs.** `studies-guide.md` §3a says so in as many words: no step in it
connects, so a green run is not evidence a study reaches a DUT.

So the guide's §3b advice — set `target_address` or `target_name`, and find the value by running a
`BleConnect` with a name no device could have — has no authored form anywhere.

**Do not add a `BleConnect` to `self_test_study.json` itself.** That file is consumed by two
committed tests and by the one study this fleet has actually run; changing what it exercises, on a
bench nothing here can reach, is the move `suite/012` declined. **Add a second fixture instead**,
round-tripped through `Study` by a test exactly as the first one is, and never submitted anywhere.

## Why now

The externally-tagged `Action` shape is now documented and the canonical example is named, so a
hand-author gets much further than before — and then stops at the first step that connects, which
is the first step of any study that does anything. A second fixture costs one file and one test.

## Done when

- [ ] A second fixture exists showing a `BleConnect` with an explicit `target_address` (and a
      commented or documented `target_name` alternative), with a test that deserializes it into
      `Study`, so it cannot drift from the type.
- [ ] `self_test_study.json` is **unchanged**.
- [ ] `suite/studies-guide.md` §3b names the new file where it gives the advice — **that file is at
      94.2% of its cap behind a blocked compaction task**, so this is one sentence, not a section.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green; gate green;
      `changelog.d/` fragment.
