# 012 — The /btw side-question button moves to the chat rail

**State:** claimed by agent/chat/012-the-side-question-button-is-on-the-rail, 2026-11-09 20:18
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
- **At dispatch (2026-11-09 20:18):** `tasks/chat/009` has landed, so the rail entry is a one-colour inline SVG in `currentColor` like its neighbours. **`embarch-chat/spec.md` is now in reserve**: 9,231 of 10,240 B, out of reserve at 9,039 B or less. Its compaction, `tasks/chat/019`, is `blocked` on `In flux: yes` because the rail is what is moving, and this unit is the one moving it. So: **if your change edits `spec.md`, bring it to 9,039 B or less in the same commit**, by compacting the rail lines you are rewriting or a verbatim move into a topic file, and keep chat/019's `Must not delete:` items readable (the Promptu bullet's pointer to decision 98's pass line, and the `embarchChat.memoryPass.*` settings). Say in this file whether you did; the supervisor closes chat/019 at the fold. If you do not touch `spec.md`, leave it alone.
- This leg runs in burndown: amending decision 94 in place is fine; a new numbered decision is not. If the change needs one, stop and say so here.
- Run the `test:webview` gate in the foreground: a backgrounded first run left a listener on its port for the last chat worker.

## Done when

- [ ] The 💬 is on the rail and gone from the input's bar; asking, Esc and the disabled state behave as before.
- [ ] Decision 94 lists it among the rail's entries, and `interfaces.md` and the comment in `composer.tsx` that place it "beside the 📚" are corrected.
- [ ] The e2e tests find it on the rail.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
