# 084 — Narrow "never fetches" to the document pipeline, with `fetch-text` as the stated exception

**State:** claimed by agent/atlas/084-narrow-never-fetches-to-the-document-pipeline, 2026-11-18 15:55
**Source:** Fleet Ready issue (a reviewer's finding on `atlas/077`): `fetch-text` makes a network call while `DESIGN.md` and `README.md` still say the tool never fetches and makes no network call.
**Issue:** EMB-208
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The owner's call, given on the issue: **keep `fetch-text`.** "Never fetches" narrows to the document pipeline — the tool never fetches a document it distils, and nothing fetched becomes an atlas or library input. `fetch-text` is a standalone research verb outside that pipeline, so it does not reopen the 2026-11-17 decision, which rejected an opt-in fetcher *inside* the pipeline.

Make every standing statement say exactly that, and nothing more:

- `DESIGN.md` line 15 ("It is fully local. **The tool never fetches a document**"), the "Still no fetching" bullet (about line 1313) and the "Never" bullet (about line 1344, "no download, no network call").
- `README.md` line 34, which carries the same "never fetches a document" sentence.
- `embarch-doc/embarch-atlas/design.md`: the "never fetches" statements, and the `fetch-text` paragraph's **Unreconciled** sentence pointing at EMB-208, which is removed once the text is reconciled.

## Why now

The doc and the code disagree on main today, and the owner has answered the question the reviewer left open.

## Dispatch notes

- **Doc-only.** No code change and no revert of `ef79b2f` / `4a2b259a`. If a test asserts the "Never" bullet's wording (the bullet mentions one that runs `inventory`), keep its meaning true for the pipeline and say what you changed.
- Say why `fetch-text` does not reopen the 2026-11-17 decision in the narrowed "Still no fetching" bullet itself, in one sentence, so a reader of that bullet does not need this task.
- No file of this sub-project is in reserve.

## Done when

- [ ] `DESIGN.md`, `README.md` and `embarch-doc/embarch-atlas/design.md` no longer say the tool never fetches or makes no network call without naming `fetch-text` as the exception outside the document pipeline.
- [ ] The narrowed "Still no fetching" bullet says why `fetch-text` does not reopen the 2026-11-17 decision.
- [ ] The **Unreconciled** sentence in `embarch-doc/embarch-atlas/design.md` is gone.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
