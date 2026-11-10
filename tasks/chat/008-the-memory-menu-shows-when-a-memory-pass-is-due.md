# 008 — The Memory menu shows when a memory pass is due, and starts one

**State:** done
**Source:** Linear issue EMB-86, filed by the owner
**Issue:** EMB-86
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

The chat's Memory menu (🧠, decision 98) has one line for a periodic memory pass: the date it last ran and whether it is due. The 🧠 rail icon carries a small marker while it is due. A click on that line opens a new chat in the window's folder with the pass's command as its first message.

The pass is a skill the owner runs outside EmbArch. It writes a stamp file whose first line is the `YYYY-MM-DD` date of the last pass. Today the only sign that it is due is one line a session-start hook prints after seven days, and nothing in the chat starts it.

## Why now

A missed pass leaves two Claude logins' memories drifting apart for another week, and the existing reminder is easy to miss in a busy window.

## Direction

- **Nothing about the pass is hard-coded**, because the pass is not part of EmbArch. Three machine-scope settings name the stamp file, the interval in days and the command to send. With them unset, the line and the marker are not shown.
- **Machine scope**, as the window's login and desk are (decision 101), so a repo's `.vscode/settings.json` cannot point the chat at another file or command.
- **A chat, not a background run:** the pass shows merges for the owner to approve, so it needs a conversation. The new chat uses the window's login and desk like any other.

## Where to look

- `webview/chat/promptu.tsx` — the Memory menu
- `webview/chat/rail.tsx` — the 🧠 icon
- `src/extension.ts` `startChat` — where a new chat with a first message starts
- `package.json` — the settings

## Dispatch notes

- `tasks/chat/009` replaces the rail's emoji with one-colour SVGs. If it has landed first, the marker goes on the SVG; if not, on today's emoji. Either is fine; do not do 009's work here.
- No `embarch-chat` doc is in reserve at the split.

## Done when

- [x] With the three settings set, the Memory menu shows the last pass's date and the 🧠 icon is marked once the interval has passed; with them unset, nothing shows.
- [x] A click starts a new chat in the window's folder with the command as its first message.
- [x] Decision 98 is amended to say so, and `embarch-chat/spec.md` describes it.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.

## Hardware-verification debt

None. A live window still needs to confirm: with the three settings set, the dot and the line show and a click opens a chat whose first message is the command (host tests are skipped here without a live `claude`).
