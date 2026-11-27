# 052 — chat records the VS Code launcher's decisions

**State:** done — chat decision 123 records the launcher; 29 and 102 point at it; focus.ts cites it
**Source:** EMB-303 — The launcher's decisions sit in embarch-ui while its code lives in embarch-chat
**Issue:** EMB-303
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

The VS Code launcher moved into `embarch-chat` (chat decision 29, 2026-10-23;
its code is `src/launcher/launcher.ts` and `src/launcher/focus.ts`), but the
decisions that govern it are still `embarch-ui`'s:
`embarch-doc/embarch-ui/decisions/launcher.md` holds decision 3 (VS Code
integration is a thin launcher), decision 28 (Start shows the window and tab
already open, and pre-flights the address; four PowerShell and focus
invariants) and decision 101 (the UI runs as a systemd user service and the
launcher drives the unit). Chat's decisions 29 and 102
(`decisions/shape.md`) only point back at ui, and `src/launcher/focus.ts`
repeats decision 28's invariants as a code comment (around lines 52 to 96).

This is the first of two units. When it is done, chat's own decisions carry
what governs the launcher's behaviour, written once:

- A new chat decision (or several, if 28's content splits naturally) restates
  ui decision 28's launcher behaviour and its invariants in chat's voice, and
  says it was moved from `embarch-ui` decision 28. Take what of decision 3 and
  101 is about the launcher's own behaviour too, and leave what is about the
  UI service (the unit itself, its port, what the UI serves) to ui. Say in the
  decision which ui numbers it carries and which parts stayed.
- Chat decisions 29 and 102 point at the new decision instead of at ui.
- `focus.ts`'s comment cites the chat decision and keeps only what a reader of
  that function needs at that line; the invariants live in the decision.

**Not yours, and the reason this is two units:** `embarch-doc/embarch-ui/`.
Decision 28 stays in ui's file as written until `tasks/ui/129` (blocked on this
task) turns it into a pointer to your decision and fixes decision 3's first
paragraph. So put the new decision's number in your report and in this task
file's closing note: 129 reads it from there. The untracked
`embarch-ui/vscode-extension/` directory on disk is the owner's; do not touch it.

## Where to look

- `embarch-doc/embarch-ui/decisions/launcher.md` (3, 28, 101), read only
- `embarch-doc/embarch-chat/decisions/shape.md` (29, 102),
  `embarch-doc/embarch-chat/decisions.md` (the index; its row for
  `decisions/shape.md` lists 29 and 102)
- `embarch-chat/src/launcher/focus.ts`, `launcher.ts`
- `DOC-CONVENTIONS.md` on numbers (a new entry takes the next free number found
  by scanning the headings) and on a moved decision's pointer

## Where the doc goes

Ui decision 28 alone is 4,074 B, so it does not fit in `decisions/shape.md`
(8.9 of 12 KB): a new topic file, `decisions/launcher.md`, with a row in
`decisions.md`'s index, is the expected home. Keep each decision under the
4,096 B per-decision cap (`DOC-COMPACTION.md` §5); restating 28 is a chance to
shorten it. **`spec.md` is 9,015 B, 24 B under its reserve line, and `open.md`
3,913 B**: no edit is expected in either; if one puts a file into reserve, file
`tasks/chat/<NNN>-compact-chat.md` in the same commit (`tasks/README.md` has the
shape; number from `scripts/check-task-numbers.py --next chat`).

## Done when

- [x] The launcher's invariants are recorded once in chat's decisions, in a
      decision that says which `embarch-ui` decisions it carries.
- [x] Chat decisions 29 and 102 point at it, not at ui.
- [x] `focus.ts`'s comment cites it rather than restating the invariants.
- [x] Gate green for `embarch-chat` (its bullet in `gate.md`) and
      `python3 scripts/check-docs.py`.
- [x] The new decision's number is written in this file's closing note;
      `changelog.d/` fragment.

## Closing note

New decision: **embarch-chat decision 123** (`embarch-chat/decisions/launcher.md`, 4,060 B). It carries `embarch-ui` decision 28 whole, decision 3's thin-launcher stance and rejected alternatives, and 101's status-bar states; 101's behaviour of driving the unit stays in chat decision 102. Left in `embarch-ui` for `tasks/ui/129`: 101's unit (`embarch-ui.service`, environment, one instance) and 3's old `vscode-extension/` packaging and distribution paragraphs. Chat 29 and 102 now point at 123; `focus.ts` cites it (comment only, no behaviour change).
