# 012 — The /btw side-question button moves to the chat rail

**State:** open
**Source:** Linear issue EMB-59, filed by the owner
**Issue:** EMB-59
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

The 💬 side-question button is a rail entry, with the same enable rule, the same toggle and the same Esc to leave, and it is gone from the input's bottom bar. The answers panel, `SideQuestions`, stays where it is, above the input.

Today `/btw` is the CLI's `side_question` (decision 57). Its 💬 mode button sits in the input's bottom bar (`.assist-slot` in `.bar`, class `icon btw`, disabled while it cannot ask). The rail holds Usage, Memory, Promptu, 📚 and 💡 (decision 94, which moved 📚 and 💡 there from the same bar).

## Why now

The owner asked for it, and `tasks/chat/014` (one-row input) assumes the 💬 has already left the bar.

## Where to look

- `webview/chat/composer.tsx` — the 💬 in the bar's `.assist-slot`; `toggleAside`, `askAside`; the rail block the composer portals into
- `webview/chat/index.tsx` — `canAsk`, which disables it
- `webview/shared/style.css` — `.btw`, `.aside-tag`, `textarea.aside`, the rail rules
- `test/webview.e2e.mjs` — the tests that find `.composer .assist-slot button.btw`

## Dispatch notes

- If `tasks/chat/009` (one-colour rail icons) has landed, the new entry follows its SVG approach; if not, it uses the 💬 like its neighbours and 009 converts it.
- When this lands, `tasks/chat/014` unparks: the folding supervisor sets it `open` in the same fold.
- No `embarch-chat` doc is in reserve at the split.

## Done when

- [ ] The 💬 is on the rail and gone from the input's bar; asking, Esc and the disabled state behave as before.
- [ ] Decision 94 lists it among the rail's entries, and `interfaces.md` and the comment in `composer.tsx` that place it "beside the 📚" are corrected.
- [ ] The e2e tests find it on the rail.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
