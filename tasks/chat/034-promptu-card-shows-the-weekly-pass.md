# 034 — The Promptu card shows the weekly pass's last run, next run and waiting sheet

**State:** open
**Source:** Fleet Ready issue (owner): the chat's Promptu card says nothing about the weekly pass, so a waiting sheet can sit unread for a week
**Issue:** EMB-85
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`promptu week status --json` now exists (`embarch-promptu`'s `promptu/014`):
it prints the last run, the next run, `missed`/`missed_since`, `running`, and
the waiting sheet's week and open count, from Promptu's own state and without a
model or network call. Its JSON shape is in `embarch-promptu`'s
`docs/contract.md` §14.4.

When this is done:

- The Promptu card (`webview/chat/rail.tsx` `PromptuCard`) shows one line about
  the weekly pass: last run, next run, a run in progress, and a waiting sheet
  with its open count. An error from the binary shows as one line, not a
  broken card.
- The rail's ✨ icon (`RailIcon`) carries a small marker while a sheet waits or
  a run was missed, and not otherwise.
- The chat asks the binary and never reads Promptu's timer or files itself.
  `src/promptu/cli.ts` `PromptuCli` gains the call (and a `TIMEOUTS` entry);
  `src/promptu/service.ts` `PromptuService.state` reads the status with the
  card's other data and again every few minutes, as it does the pattern list.
- A `promptu` that has no `week status` verb hides the line and leaves the
  icon unmarked, rather than showing an error.

Opening the sheet or running the pass from the card is EMB-284, not this unit.

## Why now

The owner's call of 2026-11-07: the chat's card shows the weekly pass too
(`embarch-chat` decision 95, which this unit amends in place). The timer runs
whether or not a window is open, and today nothing in the chat says a sheet is
waiting.

**Burndown leg: no new numbered decision.** If a decision needs amending, amend
it in place. If the work needs a new decision, stop and say so in this file and
in your report.

**Doc size:** `embarch-chat/spec.md` is 9,003 of 10,240 B, 36 B short of its
reserve line (9,039 B). A spec sentence will likely push it in: move text
verbatim into `embarch-chat/spec/` first, or file
`tasks/chat/<NNN>-compact-chat.md` in the same commit (`tasks/README.md`).
`decisions/promptu.md` decision 96 is within 204 B of its limit; decision 95
is not listed.

## Done when

- [ ] With a fake `promptu`, the card shows last run, next run and a waiting sheet, and one line on an error.
- [ ] The ✨ marker shows for a waiting sheet and for a missed run, and not otherwise.
- [ ] A `promptu` without `week status` hides the line and leaves the icon unmarked.
- [ ] Decision 95 and the chat's `spec.md` describe the line.
- [ ] Gate green (`../../embarch-fleet/gate.md`): `npm run typecheck`, `npm test`, and the doc gate.
- [ ] `changelog.d/` fragment dropped.
