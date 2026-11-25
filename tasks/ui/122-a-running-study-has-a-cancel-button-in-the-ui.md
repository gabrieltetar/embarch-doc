# 122 — A running study has a cancel button in the UI

**State:** open
**Source:** EMB-487 — no tool or button cancels a running study (the UI half; the tool is `api/198`)
**Issue:** EMB-487
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Core's `POST /study/{id}/cancel` stops a host or a device study (Core decision
128), and the UI has no control that calls it: the running study's view offers
no way to stop it short of its own end. When this is done, a cancel button sits
beside a running study, calls the route through the UI's Core client with the
lease the UI's session holds, and shows the study's end as Core records it, or
Core's refusal.

## Where to look

- `src/live_study.rs` and its assets — the running study's view and the prompt
  modal's call to Core, the pattern to follow
- `src/config.rs` — the Core client
- `src/bench/drive_fixture.rs` — driven tests against a fake Core
- `embarch-doc/embarch-core/decisions/stopping-a-study.md` (128)

## Where the doc goes

`decisions/live-study.md` or `spec.md`, whichever already describes the running
study's view. If your work pushes any file into reserve, file
`tasks/ui/<NNN>-compact-ui.md` in the same commit per `tasks/README.md`.

## Done when

- [ ] Against a fake Core, the button's route cancels a running study and the
      view shows its end.
- [ ] A refused cancel shows Core's reason.
- [ ] Gate green.
