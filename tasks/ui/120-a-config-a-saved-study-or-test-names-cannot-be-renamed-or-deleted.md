# 120 — A config a saved study or test names cannot be renamed or deleted

**State:** claimed by agent/ui/120-a-config-a-saved-study-or-test-names-cannot-be-renamed-or-deleted, 2026-11-25 08:28
**Source:** EMB-385 — a config a saved study or test names can still be renamed or deleted
**Issue:** EMB-385
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Decision 96 (`decisions/bench-configs.md`) never refuses a config rename or
delete, on the premise that no saved host study can name one. The owner amended
that (`notes/hil/02-study.md`, "Where its files live", review round 2): once
host studies and tests are saved in the firmware repo, renaming or deleting a
config a saved study or test names is refused, naming them, as the Study
Designer already refuses a destructive edit that breaks a saved dev-bench
study. A host study's prompt names the config it wants through
`Prompt.bench_config` (`embarch-study-designer` decision 88). When this is
done:

- **On Rename and Delete**, the bench routes read the repo's saved host
  studies and tests: `embarch/studies/` and `embarch/tests/suites/`. **The
  tests layout is pinned by `api/196`, running in the same wave:**
  `embarch/tests/suites/<suite>/suite.json`, each test's file and its study
  inside the suite folder, a manifest's test `file` relative to its
  `suite.json` (the crate's suite format, `embarch-study-designer`
  `interfaces/hil-tests.md`). Read that layout; do not wait for 196 to land.
- **A config one of them names is refused `409`**, naming each study and test
  and the prompt that names the config; the dialog shows the list.
- **A config nothing names** renames and deletes as today.
- A file that does not parse is not silently skipped: say in the decision what
  the route does with it (refuse, or list it as unreadable), and test it.

## Why now

The HIL Test phase saves tests in the firmware repo (`api/196`), and a test's
prompt that names a config would point at nothing after a rename.

## Where to look

- `src/bench/check.rs`, `src/bench/routes.rs`, the bench dialog in the front
  end
- `embarch-doc/embarch-ui/decisions/bench-configs.md` (96)
- `embarch-doc/embarch-study-designer/decisions/host-prompt.md` (88),
  `interfaces/hil-tests.md`
- `embarch-doc/notes/hil/02-study.md`

## Where the doc goes

Amend decision 96 with a dated pointer to a new ui decision, or in place if it
has room; `interfaces/` gives the new `409`. **Decisions at their limit, do not
grow:** `trace-view.md` 10 (0 B left), `gatt-capture.md` 17 (4 B),
`bench-live.md` 90 (12 B), `trace-chart.md` 10 (14 B), `launcher.md` 28 (22 B).
If your work pushes a file into reserve, file `tasks/ui/<NNN>-compact-ui.md` in
the same commit per `tasks/README.md`.

## Done when

- [ ] A fixture test naming config `A` blocks its rename and its delete, the
      refusal naming the test.
- [ ] A fixture host study in `embarch/studies/` naming config `A` does the
      same.
- [ ] A config nothing names renames as before.
- [ ] Decision 96 amended.
- [ ] Gate green.
