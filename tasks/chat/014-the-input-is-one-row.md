# 014 — The chat input is one row, its pills left of the box and Send an icon on its right

**State:** claimed by agent/chat/014-the-input-is-one-row, 2026-11-09 22:26 — unparked 2026-11-09 by `chat/012`'s fold: the 💬 is a rail entry and gone from the input's bar (embarch-chat `9fd3f0b`). `embarch-chat/spec.md` is then 9,037 B, two bytes under its reserve line, so a spec edit here likely puts it back in reserve and owes a compaction filing.
**Source:** Linear issue EMB-60, filed by the owner
**Issue:** EMB-60
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

The input is one row: `[mode][model · effort][MCP][Remote]  [typing box]  [send icon]`. The mode menu and the Remote pill sit with the model·effort and MCP pills, left of the box. Send is an icon button on the box's right, its title saying Send, Queue or Ask; while a turn runs it is a Stop icon in the same place. Nothing remains under the box. The pills' popovers still open within the pane, and the input and Send stay on screen at every pane height.

Today the textarea sits alone in `.field`, full width. Under it one `.bar` row holds, in order: the permission-mode `<select>`, the footer pills (`ModelPill` labelled `name · effort · Ultracode`, `McpPill` "MCP" with "✗N" on a failed server, `RemotePill`), the 💬, and a text button reading Send, Queue or Ask (Stop while a turn runs).

## Why now

The owner asked for it. The 💬 moves to the rail in `tasks/chat/012`, which is why this waits for it.

## Where to look

- `webview/chat/composer.tsx` — `.field` and `.bar`, the mode `<select>`, the `.send` span
- `webview/chat/index.tsx` — the `footer` it passes (the three pills)
- `webview/chat/footer.tsx` — `ModelPill`, `McpPill`, `RemotePill`
- `webview/shared/style.css` — `.composer`, `.field`, `.composer .bar`, `.bar .send`, `.pill`, `.pop`
- `test/webview.e2e.mjs` — pill selectors, `.composer .bar button.primary`, Stop's title, "Queue at the bar's right", and the test that finds Send by its text

## Done when

- [ ] The input is one row in the order above, at a narrow (400 px) and a wide pane.
- [ ] Send, Queue, Ask and Stop are icon buttons with titles, and keyboard send works as before.
- [ ] The pills' popovers open fully inside the pane.
- [ ] Decisions 81–83 and the comment in `footer.tsx` describe the new place; the e2e tests pass on the new layout.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
