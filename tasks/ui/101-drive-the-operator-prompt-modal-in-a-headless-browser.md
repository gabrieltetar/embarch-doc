# 101 — Drive the operator-prompt modal in a headless browser against a stub Core

**State:** claimed by agent/ui/101-prompt-modal-headless-drive, 2026-10-28 22:17
**Reserve (dispatch note, 2026-10-28):** no `embarch-ui` file is in reserve (`check-doc-size.py --pressure`). If this unit pushes one past 90% of its cap, file `tasks/ui/<NNN>-compact-ui.md` in the same commit.
**Source:** `tasks/ui/100`'s debt (landed 2026-10-28, ui decision 69): "No `tests/browser` drive was written: extend `stub_core.py` with a prompting study and drive the modal." The feature row says the modal has never been rendered in a browser.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Ui decision 69 shipped a modal outside every tab, fed by `/api/prompts/events`, with the prompt text, a countdown, Confirm/Cancel, and a `409` path. Only Rust unit tests and a stub-Core route test cover it; nothing has rendered it. When this is done, `tests/browser/stub_core.py` can serve a host study that is `running` with a `pending_prompt` (and the `PromptPending`/`PromptResolved` events on its stream), and a `tests/browser/drive_prompt.py` drives headless Firefox through: the modal opens on a tab other than Live Study; the countdown shows and moves; Confirm posts `answered_by: "ui"` and the modal closes; a reload mid-prompt shows it again; a stub `409` shows the "already ended" text rather than closing silently; a resolve from another surface leaves the modal up saying who answered.

## Why now

The field operator who asked for this needs to see it from across the bench; a modal that has never been rendered is the part of `ui/100` most likely to be wrong, and the drive costs no hardware.

## Done when

- [x] `stub_core.py` serves a prompting host study; `drive_prompt.py` covers the six behaviours above and passes headless.
- [x] Any rendering bug it finds is fixed in this unit, and decision 69's "Not measured" sentence is updated to say what is now measured.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment dropped; the `features.d/ui-120-host-study-prompt-modal.md` row's "never rendered" status updated.

## Outcome

`stub_core.py` gained a prompting host study (`POST /_stub/prompt/{start,resolve,conflict,answers,reset}`, unauthenticated control surface; the study is absent from `/studies` until `start`, so no other drive changes). `drive_prompt.py` passes all six behaviours headless (ports 4611-4613, own target dir). No rendering bug found; decision 69 and the feature row updated. The stub's `list` value first read `"steps"` and the UI silently dropped the prompt: `HostList` serialises capitalised (`Steps`).

**Debt (not hardware):** no live Core prompt has been seen; beep and desktop notification not exercised headless. `window.__errs` is read like the other drives, but this page installs no handler for it, so that check is weak.
