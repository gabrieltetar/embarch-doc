# embarch-chat: open

**Status:** active, 2026-10-23.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

## Not done

- **Decisions 50–85 are built and not installed.** The installed extension is the 2026-10-23 13:41 package (decisions 1–49) [measured 2026-10-23]; everything since sits in the repo. Unblocked by `./reinstall.sh` and a window reload.
- **`embarch-ui` still carries its own `vscode-extension/`**, the launcher's old copy (decision 29). Both register the `EmbArch UI:` commands, so this extension leaves them to the old one while both are installed. Removing the old copy from `embarch-ui` finishes the move.
- **The library has not been seeded** (decision 14): the plugin holds promptu's three pieces and `~/.claude/commands` is empty [measured 2026-10-23]. The `claude -p` grouping pass over past prompts, then the owner's ✓/✕, is what fills it.

## Waiting on the owner

- **A send before the cards arrive is held** up to 4.5 s for a draft of six words or more, Enter again sending at once (decision 26). Built so; whether it stays is his call.

## Not yet seen

- **Remote Control from the phone** (decision 83): `/remote-control` links a chat in 0.25 s and prompts are still asked in the panel, but nobody has answered one from the phone side.

## Structural limits

- **A change dropped in a per-change diff is not reported to the CLI** (decision 64): the permission answer has no field for it, so Claude learns of it only by reading the file.
- **An MCP call cannot move to the background** (decision 70): the CLI never registers one as a foreground task, so a long `embarch-api` flash holds its turn.
- **The activity-bar count appears only once the list has been opened** (decision 35): VS Code builds a view lazily. The status-bar count always shows.
