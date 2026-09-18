# 090 — Decision 36's erase paragraph overclaims what `no_backend_maps_erase_to_a_full_chip_erase` asserts

**State:** open
**Source:** reviewer finding on `core/073`, merge SHAs `embarch-doc@a070fccb`,
`embarch-core@b6774e0e` (the code branch carried zero commits — pre-existing code, reviewed here for
the first time against a *new* decision claim about it). Dropped in `inbox/` as
`core-decision-36-erase-test-coverage-overclaim.md`, drained and numbered by leg 144, 2026-09-17.
**Scope:** core
**Hardware:** none — a documentation/test-coverage discrepancy, not a hardware question.
**Owner:** no

## What

`embarch-core/decisions/flash-backend.md` decision 36, in the paragraph `core/073` added
(`embarch-doc@a070fccb`), states:

> `flash_backend.rs`'s `no_backend_maps_erase_to_a_full_chip_erase` test asserts both: the generated
> `--options` string for `nrfutil`, and the generated script text for `jlink`.

**That is false as written.** The test (`embarch-core/src/flash_backend.rs`, around lines 658-666)
calls only `jlink_script(...)` and asserts only on its output:

```rust
fn no_backend_maps_erase_to_a_full_chip_erase() {
    let script = jlink_script(Path::new("/tmp/x.hex"), "hex", None, true).unwrap();
    assert!(script.contains("erase\n"));
    assert!(!script.contains("erase_chip"));
    // And with erase off, nothing erases at all.
    let no_erase = jlink_script(Path::new("/tmp/x.hex"), "hex", None, false).unwrap();
    assert!(!no_erase.contains("\nerase\n"));
}
```

The `nrfutil` `--options` string (`chip_erase_mode=ERASE_RANGES_TOUCHED_BY_FIRMWARE` / `ERASE_NONE`,
around lines 392-396 of the same file) is built **inline on a `Command` inside `run()`** — no
function returns it as a string, and a repo-wide
`grep -rn "ERASE_RANGES_TOUCHED_BY_FIRMWARE\|chip_erase_mode" --include=*.rs` finds it only at those
two call sites in `run()`, in no test file anywhere.

**Re-derive every coordinate above before acting on it.** The line numbers and the grep result are a
reviewer's reading, and "this does not hold" is a correct outcome to report.

## Why this is a contradiction rather than a nitpick

Decision 36 is explicit that this paragraph exists *precisely* to keep the measured/stated boundary
honest — it says the property holds "by construction of the command line each arm generates, not by
an observation on hardware" — and cites the test as what makes the command-line claim reliable going
forward. But the test guards only the `jlink` arm. The `nrfutil` half is an unenforced claim about
source as it reads today: nothing fails the build if a future edit changes
`ERASE_RANGES_TOUCHED_BY_FIRMWARE` to `ERASE_ALL`. The decision asserts a **stronger evidentiary
basis (test-enforced) than exists (source-reading, for half the claim)** — the same overclaim shape
this suite's measured-vs-stated rule exists to stop, applied to test coverage rather than to hardware
behaviour.

## Why now

The correction is a sentence, and it is the same defect `core/073` was filed to fix, one level down.
Left alone it is a decision that reads as guaranteed and is not.

## Done when

- [ ] Decision 36's paragraph says the test covers only the `jlink` arm, and the `nrfutil` claim is
      either **(a)** demoted in the text to "true by source reading, unguarded by a test" or
      **(b)** backed by a real test — e.g. extracting the `--options` string construction into a
      function that returns it, the way `jlink_script` already is, and asserting on it.
      **(b) is the better outcome if it is small**; do not force it if extracting the string means
      restructuring `run()`.
- [ ] If you take (b), the new test lives beside `no_backend_maps_erase_to_a_full_chip_erase` and the
      decision text then says what it actually asserts, not what it aspires to.
- [ ] A `changelog.d/` fragment noting the correction.
- [ ] Gate green per `../../embarch-fleet/protocol.md` §10.

## Not yours

- **Do not change erase behaviour in either backend.** The underlying source fact — `nrfutil` is
  invoked with `ERASE_RANGES_TOUCHED_BY_FIRMWARE`, never `ERASE_ALL` — reads true today by
  inspection. This task is about what *backs* the claim, not about the claim being wrong on today's
  code.
- **Do not re-point the citation to another decision.** `core/073` already established by a fresh
  grep of the whole `decisions/` and `interfaces/` tree that no other decision asserts this
  property; decision 36 is where it lives.
