# 019 — `promptu week mark` records a verdict, and `week apply` turns each approved line into its change

**State:** done — week mark and week apply built; memory lines through the hook checks, pattern lines as a branch commit or a patch; tests on scratch folders and a scratch checkout
**Source:** decisions 30 and 43 (`decisions/learning.md`); `embarch-promptu` `docs/contract.md` §10 and §14; the sheet `week draft` writes (`promptu/017`)
**Issue:** EMB-279
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Decision 30 has the weekly sheet applied with `promptu week apply`, from the
Markdown file or from the Desk. `week draft` writes `sheet.json` and
`sheet.md`, and nothing yet records a verdict or acts on one. When this is
done:

- **`promptu week mark`** records a line's verdict (approve or cut) and note,
  a group's cut, and the week's feel. The Desk's routes (EMB-282) and the
  review skill (EMB-280) will call it.
- **`sheet.md` is read back**: a line marked ✕ is cut, and text written after
  a line is its note.
- **`promptu week apply`**, per approved line:
  - a **memory line** writes its topic file and its index line only if the
    hook's checks pass (`src/checks.rs`, `src/hook.rs`), after a backup;
  - a **pattern line** is committed on a branch in the checkout Promptu's
    config names, never pushed, with the pattern's version bumped, lint clean,
    its example renders updated and the configured public-safety command run
    first; with no checkout configured, it is written out as a patch
    (decision 43).
- A line that fails stays open with its error. Applying the same sheet twice
  changes nothing the second time. Apply is a command the owner runs (or, later,
  an HTTP route the Desk calls); it is never an agent tool.

Where to start: `src/checks.rs` (`topic` and the index checks), `src/hook.rs`,
`src/lint.rs`, `tests/golden/`, `docs/contract.md` §10 (`status`, `error`) and
§14. Test only in scratch folders and a scratch git checkout created by the
test: never against a real memory folder or the real pattern checkout.

## Why now

`week draft` landed as `promptu/017`. EMB-280 (the terminal review skill) and
EMB-282 (the desk's routes) wait on this.

**Burndown leg: no new numbered decision.** Amend decisions 30 and 43 in place
where they change. Where the contract leaves a choice open, record it as a fork
in `docs/forks.md` on a default. If the work needs a new decision, stop and say
so in this file and in your report.

## Done when

- [x] In a scratch memory folder, an approved memory line writes a file that `promptu memory check` passes, and a line that would fail writes nothing.
- [x] In a scratch checkout, an approved pattern line makes the change the contract describes, with the version bumped, and nothing is pushed.
- [x] With no checkout configured, an approved pattern line is written out as a patch.
- [x] A ✕ written in `sheet.md` is honoured by `week apply`.
- [x] Applying the same sheet twice changes nothing the second time.
- [x] Gate green (`../../embarch-fleet/gate.md`), with `cargo test --all-targets` and `cargo clippy --all-targets -- -D warnings`.
- [x] `spec.md`/`decisions.md`/`interfaces.md` updated where they change, `changelog.d/` fragment dropped.

## Notes

- Forks W17 (one commit per pattern, branch restored) and W18 (`external` lines are never applied by `mark`), and W4/W5's built defaults, are in `docs/forks.md`. Decisions 30 and 43 amended in place; no new decision.
- Verified only on scratch folders and a scratch git checkout; never a real memory folder or pattern checkout. Hardware: none. Feature row owed (EMB-292: no promptu section in `build_features.py`).
