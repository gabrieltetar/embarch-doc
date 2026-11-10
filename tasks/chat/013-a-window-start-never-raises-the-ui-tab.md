# 013 — Starting the UI at window start never opens or raises its browser tab

**State:** claimed by agent/chat/013-a-window-start-never-raises-the-ui-tab, 2026-11-09 22:02
**Source:** Linear issue EMB-64, filed by the owner
**Issue:** EMB-64
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

With `embarchUi.autoStart` on, starting or reloading a VS Code window starts the UI if it is not running and changes no browser tab. Only an explicit action shows the UI: the Open in Browser command, the status-bar item, or the Start command run by hand.

Today there is no separate "open" setting. The launcher runs `start()` when `autoStart` is on, and every path through `start()` ends in `reveal()`, which focuses the existing EmbArch tab or opens one with `openExternal` — also when the UI was already running (`external`). Starting and showing are one setting, and its description mentions only starting.

## Why now

The owner asked for it: every window start or reload brings the tab to the front or opens a new one.

## Where to look

- `src/launcher/launcher.ts` — `start`, `reveal`, the `autoStart` branch at activation
- `package.json` — the `embarchUi.autoStart` description

## Dispatch notes

- The launcher was just reworked on `main` (`bce5ac7`, "The UI launcher drives embarch-ui.service and spawns nothing"); read it as it is now, not as older docs describe it.
- No `embarch-chat` doc is in reserve at the split. At dispatch (2026-11-09 22:02) `embarch-chat/spec.md` is 9,034 B, 5 B under its reserve line (9,039 B): an edit there that grows it puts it in reserve and owes `tasks/chat/<NNN>-compact-chat.md` in the same commit.
- Burndown is on: no new numbered decision. Amending one in place is fine; if the change needs a new one, write its proposed text under `## Owed decision` in this file and the supervisor files it.

## Finding: already true on main

The premise was stale. `bce5ac7` (decision 102, `decisions/shape.md`) removed `embarchUi.autoStart` and the activation-time start: `activateLauncher` only reads the unit's state (`void refresh()`), and `reveal()` is reached only from the Start command and the status-bar click. No `autoStart` setting exists in `package.json`, so there is no description to fix. The only remaining mention is a hostile-settings fixture in `test/settings.test.mjs`, which pins that a repo's settings are ignored. Nothing in `src/` changed; one regression test was added (`test/host.test.mjs`, "window start opens no browser tab"). If the owner still saw a tab raised on window start, the cause is something else (another window's Start, or the old standalone launcher still installed) and needs a fresh report.

## Done when

- [x] With `autoStart` on, starting or reloading a window starts the UI if needed and changes no browser tab. (No `autoStart` any more; activation starts nothing and opens nothing. Test added.)
- [x] The Start command and the status-bar item still open or focus it. (Unchanged: both run `start()` -> `reveal()`.)
- [x] The setting's description says what it does. (Setting no longer exists.)
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `embarch-chat` docs updated, `changelog.d/` fragment dropped. (Docs needed no change; `npm test` has 5 failures that fail identically without my change.)
