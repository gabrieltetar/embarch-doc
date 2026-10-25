# embarch-chat: open

**Status:** active, 2026-10-23.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

## Not done

- **Decisions 86–88 are built and not installed.** The installed extension is the 2026-10-23 21:58 package, b6996cc (decisions 1–85) [measured 2026-10-25]. Unblocked by `./reinstall.sh` and a window reload, after the desk's 8f06ba0 is deployed (88) and `embarch-ui` ab1b9f8 runs (87's card, study and board links land on the tab only until then).
- **`embarch-ui` still carries its own `vscode-extension/`**, the launcher's old copy (decision 29). Both register the `EmbArch UI:` commands, so this extension leaves them to the old one while both are installed. Removing the old copy from `embarch-ui` finishes the move.
- **The library has not been seeded** (decision 14): the plugin holds promptu's three pieces and `~/.claude/commands` is empty [measured 2026-10-23]. The `claude -p` grouping pass over past prompts, then the owner's ✓/✕, is what fills it.

## Waiting on the owner

- **A send before the cards arrive is held** up to 4.5 s for a draft of six words or more, Enter again sending at once (decision 26). Built so; whether it stays is his call.
- **No row is focused when a 💡 or 📚 menu opens** (decision 86), where IntelliSense focuses the first, so Enter still sends until ↑/↓ move in. Built so, and recommended; his call.
- **"PR 7" with no `#` names a PR in a draft but not in Claude's prose** (decision 88): the draft matcher takes it in the chat's own repo, a prose link needs `PR #7`. Whether the two should agree is his call.
- **A reference carries its title into the draft, clipped at 90 characters** (decision 88). Whether 90 is the length he wants is his call.

## Not yet seen

- **Remote Control from the phone** (decision 83): `/remote-control` links a chat in 0.25 s and prompts are still asked in the panel, but nobody has answered one from the phone side.
- **The desk's references against the live desk's real index** (decision 88): measured only against a synthetic index, with real Haiku, until the desk and this extension are deployed.
- **Slack's `app_redirect` link** (decision 87), for a channel a step names with no permalink, is untested.

## Structural limits

- **A change dropped in a per-change diff is not reported to the CLI** (decision 64): the permission answer has no field for it, so Claude learns of it only by reading the file.
- **An MCP call cannot move to the background** (decision 70): the CLI never registers one as a foreground task, so a long `embarch-api` flash holds its turn.
- **The activity-bar count appears only once the list has been opened** (decision 35): VS Code builds a view lazily. The status-bar count always shows.
