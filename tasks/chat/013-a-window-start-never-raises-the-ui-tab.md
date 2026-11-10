# 013 — Starting the UI at window start never opens or raises its browser tab

**State:** open
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
- No `embarch-chat` doc is in reserve at the split.

## Done when

- [ ] With `autoStart` on, starting or reloading a window starts the UI if needed and changes no browser tab.
- [ ] The Start command and the status-bar item still open or focus it.
- [ ] The setting's description says what it does.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `embarch-chat` docs updated, `changelog.d/` fragment dropped.
