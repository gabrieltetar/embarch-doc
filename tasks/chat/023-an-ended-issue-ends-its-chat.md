# 023 — An ended issue ends its chat

**State:** open
**Source:** Linear issue EMB-73
**Issue:** EMB-73
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

The owner wants an issue's status to end its work: Done or Canceled ends the issue's chat with a message on top and one button that closes the window, and the desk removes the issue's folder once the window is closed. Nothing closes in front of the owner without a click.

EMB-73 is split three ways. **This task** is the chat's half. `tasks/desk/025` (running in parallel) makes the desk post the entries below; `tasks/desk/026` removes the folder after the window closes.

**What the chat does, decided at the split:**

- **On an `end` for one of the window's folders**, the issue's chat (the one on `item_id`) shows a message on top of the chat, exactly `Chat has ended because the issue is done`, or `Chat has ended because the issue is canceled`, with one button, Close window, which closes this VS Code window. The chat then takes no more input.
- **If a turn is running, the message and the closed input wait for the turn to end.**
- **If the issue's chat is not open in the window, the owner still sees the message without hunting for it**: open the chat, or show the same text and button another way. Your call; say which in the decision.
- **The ended state survives a window reload, and the chat never resumes the session after it** (`src/wire/chat.ts`: a resume starts `claude` in the issue's folder, which is about to be removed). An `end` for a chat already ended changes nothing.
- **On an `unfinished`**, the same place shows each blocker's repo and reason, and a Finish button that calls `POST /items/{item_id}/finish`. The chat stays live and takes input. A later `end` or `unfinished` replaces the message. A desk that answers 404 gets a plain error saying the desk has no Finish yet.

## The contract between the desk and the chat (fixed at the split; implement it as written)

Both halves are written against this in parallel, and either may land first. A chat that knows these kinds before any desk sends them does nothing new. An older chat takes an entry it does not know and drops it (`deskService.ts`'s poll takes every entry, and `extension.ts` acts only on the kinds it knows), so its window simply stays open. Change the contract in neither half; if it cannot be implemented as written, stop and say why in this file.

1. **Two new mailbox kinds, written only by the desk, server-side.** `POST /mailbox` refuses both, as it refuses `start` (desk decision 46).
   - `end`: `{"kind":"end","id","folder","item_id","issue_key","outcome"}`, `outcome` `"done"` or `"canceled"`. The issue is Done or Canceled and every check passed. The window on `folder` ends the issue's chat.
   - `unfinished`: the same fields plus `"blockers":[{"repo":"<repo folder name>","reason":"<one line>"}]`. The issue is Done or Canceled but a check failed: nothing closes and nothing is removed. The window shows each blocker and a Finish button.
   - Both carry the existing `created_ms`, `expires_ms` and `taken_ms`. Neither expires on the 10-minute launch clock: an entry waits until a window takes it or the folder is gone. A newer `end` or `unfinished` for a folder replaces an untaken older one.
2. **One new desk route, `POST /items/{id}/finish`.** It re-runs the checks for the item's issue, posts a fresh `end` or `unfinished` for its folder, and answers `{"ended":true}` or `{"ended":false,"blockers":[…]}`. The chat's Finish button calls it and then acts on the mailbox entry, not on the answer, so a Finish pressed anywhere reaches the window the same way.
3. **A window shows a folder while it polls `GET /mailbox?folder=` for it.** The chat already polls every 3 s per window folder, and backs off to 60 s while the desk is unreachable. The chat's Close window button only closes the window and calls no route; the desk reads the polls stopping as the window gone (`tasks/desk/026`).

## Why now

EMB-73: a landing that deleted the folder under a live chat left the chat unreachable on its next resume, and the window open on a folder that was gone.

## Where to look

- `src/extension.ts` — the mailbox handler (`desk.on("mail", …)`); `src/deskService.ts` — the poll; `src/desk/client.ts` — `MailboxEntry` and the desk calls
- `src/wire/chat.ts` — a chat's run and its resume; `src/chats.ts` — the chat records
- `src/views/` and `webview/` — the chat panel and its input
- `embarch-doc/embarch-chat/interfaces.md` (the mailbox rows), `decisions/desk.md`, `decisions/sessions.md`, `spec.md`

## Dispatch notes

- Normal mode: a new numbered `embarch-chat` decision is expected. Number it per `DOC-CONVENTIONS.md`.
- No `embarch-chat` doc is in doc-size reserve at the split. `decisions/promptu.md`'s decision 96 has 204 B left before its per-decision limit; leave it alone.
- Tests use a fake desk; never the real desk or a real folder removal.
- Do not edit `embarch-desk` or anything outside `embarch-chat` and `embarch-doc/embarch-chat/`.
- Edit files with your Edit and Write tools, not inline Python or shell redirects.

## Done when

- [ ] An `end` shows the exact message for its outcome on top of the issue's chat, with one Close window button, and the input closes; a test covers done and canceled.
- [ ] With a turn running, the message and the closed input wait for the turn to end; a test covers it.
- [ ] After a window reload the chat is still ended and does not resume its session; a second `end` changes nothing.
- [ ] An `unfinished` shows each blocker and a Finish button that calls `POST /items/{item_id}/finish`, and the chat stays live; a test covers it.
- [ ] A new `embarch-chat` decision records the behaviour; `interfaces.md` lists the two kinds and the route; `spec.md` updated.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the npm bullet); `changelog.d/` fragment dropped.
