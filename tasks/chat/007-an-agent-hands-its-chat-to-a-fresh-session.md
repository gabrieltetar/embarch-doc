# 007 — An agent hands its chat over to a fresh session in the same panel

**State:** open
**Source:** Linear issue EMB-61, filed by the owner; the design is `embarch-chat` decision 103 (owner, 2026-11-07)
**Issue:** EMB-61
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

An agent deep in a long chat can call `handoff(prompt)`. The panel keeps the whole visible history, adds a divider naming the handoff and showing its prompt, ends the old Claude Code process, and starts a fresh one **in the same panel** with the prompt as its first message. The desk keeps both sessions on the same work item. A setting `embarchChat.handoff` says how: `card` (default) shows the handoff as a card with the prompt editable and two buttons, Continue in a fresh session / Stay; `immediate` switches at once; `off` declares no tool.

Today only the owner can hand off: the 💡 handoff card (decision 36) asks for a fenced `handoff` block, `extractHandoff` reads it, and the "Fresh chat with this handoff" chip (`freshChat`) opens a **new** chat on the same item.

## Why now

Decision 103 is decided and not built. `embarch-promptu` decision 41 (EMB-65, `tasks/promptu/002`) names a handoff as one of its four ways to carry high-context work, and it waits for this tool to exist.

## Direction (decision 103 — read it first; it is the design, and this task needs no new decision)

- **The call:** a `handoff(prompt)` tool on the panel's own MCP server (decision 65), next to `getDiagnostics`. The server is declared whenever the handoff is on, not only with `embarchChat.diagnosticsTool`.
- **Stay** answers the tool call, so the agent carries on in the old session.
- **The fresh session** keeps the chat's mode, model, effort and work item, never a looser permission mode.
- **The switch** reuses `freshChat`'s start on the same item, but in the same panel and timeline.
- Decision 63 ("nothing reruns by itself") still holds: a handoff carries on started work, it does not rerun a step.

## Where to look

- `src/extension.ts` `freshChat` and the turn hook near it
- `src/hostHooks.ts`, `src/mcpServer.ts` — the panel's MCP server and where its tools are declared
- `src/assistant/edits.ts` `handoffRequest`, `extractHandoff`; `src/assistant/assistant.ts`
- `src/wire/chat.ts` — `ensureProcess`, `closeProcess`, the context-usage refresh
- `webview/chat/composer.tsx` `applyCard` — a new card for the agent's handoff

## Dispatch notes

- When this lands, `tasks/promptu/002` unparks: the folding supervisor sets it `open` in the same fold, or the gate refuses a `blocked` task naming a task no longer in the queue.
- No `embarch-chat` doc is in reserve at the split.

## Done when

- [ ] An agent's `handoff(prompt)` shows a card by default; Continue ends the old process, starts a fresh one in the same panel with the prompt as its first message, and the timeline keeps the old history above a divider.
- [ ] Stay answers the tool call and the agent carries on.
- [ ] With the setting `immediate`, the same happens without the card; with `off`, no tool is declared.
- [ ] The fresh session has the old chat's mode, model, effort and desk work item.
- [ ] `embarch-chat/spec.md` describes the handoff, and decision 103 drops its "not built".
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
