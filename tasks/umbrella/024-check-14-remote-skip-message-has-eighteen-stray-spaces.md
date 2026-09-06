# Fix check 14's `Remote` skip message — eighteen stray spaces from a wrapped literal

**State:** claimed by leg 020
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

- [ ] `doctor.rs:2898` is a `\`-continued literal; the rendered detail has no multi-space run.
- [ ] A new test fails on `"  "` in any check's `detail` or `fix`.
- [ ] That test is shown to fail against the current string (revert locally, confirm, restore)
      before it is committed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
