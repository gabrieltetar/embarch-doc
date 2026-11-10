# 105 — `embarch-ui`'s READMEs point at the launcher inside `embarch-chat`

**State:** open
**Source:** Linear issue EMB-69, filed by a session
**Issue:** EMB-69
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Neither of `embarch-ui`'s READMEs tells a reader to install its own `vscode-extension/`. Both say the launcher is part of `embarch-chat` (`embarch-ui` decision 3, amended; `embarch-chat` decision 29): its `embarchUi.start`, `embarchUi.stop` and `embarchUi.openInBrowser` commands and a three-state status bar item (ours, external, stopped), installed with `embarch-chat`. `embarch-ui/spec.md` already says so.

Today:

- `README.md` — the architecture sketch ("vscode-extension/ (thin, TypeScript) spawns/stops the binary, opens the system browser") and the section "The VS Code launcher" (install it with `./reinstall.sh`).
- `vscode-extension/README.md` — describes the status bar item with two states ("embarch-ui" / "embarch-ui (stopped)").

Following them installs the old launcher.

## Why now

A reader following the README installs a launcher that no longer runs.

## Dispatch notes

- **The README only.** Removing the old `vscode-extension/` copy is tracked separately (`embarch-chat/open.md`); do not delete it here.
- `embarch-chat`'s launcher was reworked on its `main` today (`bce5ac7`, "The UI launcher drives embarch-ui.service and spawns nothing"). Describe it from `embarch-chat`'s current docs, read only; if they and `embarch-ui/spec.md` disagree, say so in your report rather than editing `embarch-chat`.
- No `embarch-ui` doc is in reserve at the split. A doc change in `embarch-doc` is only owed if `spec.md` turns out to say something the README fix makes false.

## Done when

- [ ] Neither README tells a reader to install `vscode-extension/`; both point at `embarch-chat`'s launcher.
- [ ] The status bar is described with its three states.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
