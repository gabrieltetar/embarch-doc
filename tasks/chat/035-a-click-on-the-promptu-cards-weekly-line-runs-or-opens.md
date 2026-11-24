# 035 — A click on the Promptu card's weekly line runs the pass now, or opens the waiting sheet

**State:** open
**Source:** decision 95 (`decisions/promptu.md`, the Promptu card and its weekly line, which today rejects "opening the sheet or running the pass from the card (EMB-284)"); `embarch-promptu` decisions 30 and 45 and `docs/contract.md` §14.4 (`week run`, exit 4 while a run is live; `week status`)
**Issue:** EMB-284
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

The owner wants the card's weekly line to act when clicked. When this is done:

- **Run now.** With no sheet waiting, a click runs `promptu week run` in the
  background. The line says it is running (from `promptu week status`, as it
  reads today) and then shows the result. A run already going, such as the
  timer's, is shown and not started again: `week run` exits 4 while one is
  live, and a second click while this one runs starts nothing.
- **Open the sheet.** With a sheet waiting, a click opens a new chat with the
  review skill typed, unsent, the way Start work types `/promptu`, and runs
  nothing. Use the skill name `embarch-promptu`'s contract gives it (fixed by
  `promptu/023`; read the contract, do not guess). This is the owner's
  standing default for that choice (2026-11-23), recorded in
  `embarch-promptu`'s `docs/forks.md`.
- **A failed run shows one line on the card.**
- `week run` gets its own, much longer time limit in `src/promptu/cli.ts`
  `TIMEOUTS`; a pass packs and drafts a whole week.
- Decision 95 drops the click from its **Rejected** list and says what the
  click does; the chat's `spec.md` says it too.

Where to start: `webview/chat/rail.tsx` `PromptuCard` (the weekly line),
`src/promptu/cli.ts`, and `src/views/chatHost.ts` (the card's messages
between the page and the host). Read `embarch-promptu`; do not edit it.

## Why now

`week run` landed as `promptu/018` and the review skill as `promptu/023`.
EMB-284; the owner's need is EMB-85's.

**Burndown leg: no new numbered decision.** Amend decision 95 in place. If
the work needs a new decision, stop and say so in this file and in your
report.

**Doc size, a dispatch note (supervisor):** no `embarch-chat` file is in
reserve (`spec.md` 9,003 of 10,240 B, 36 B short of it, so a net addition
there may push it in: if it does, file `tasks/chat/<NNN>-compact-chat.md` in
the same commit per `tasks/README.md`). Decision 96, in the same file as 95,
is within 204 B of its limit; you should not need it.

## Done when

- [ ] With a fake `promptu`, one click runs `week run` once, and a click while it runs starts nothing.
- [ ] With a sheet waiting, a click opens it as decided and runs nothing.
- [ ] A failed run shows one line on the card.
- [ ] Decision 95 and the chat's `spec.md` say what the click does.
- [ ] Gate green (`../../embarch-fleet/gate.md`): `npm run build`, `npm run typecheck`, `npm test` and `npm run test:webview`.
- [ ] `changelog.d/` fragment dropped.
