# embarch-chat: open

**Status:** active, 2026-11-01.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

## Not done

- **The library has not been seeded** (decision 14): the plugin holds promptu's three pieces and `~/.claude/commands` is empty [measured 2026-10-23]. The `claude -p` grouping pass over past prompts, then the owner's ✓/✕, is what fills it.

## Waiting on the owner

- **Promptu in the chat (94–99) is installed** (spec status); three review rounds are done. **Decision 100 is not recorded as reviewed**: whether it was is his to say. Forks waiting for his pick in `embarch-promptu`'s docs/forks.md: P12 (one pass per task start) and P15 (smaller choices); P16–P19 are decided (94, 96, 99).

- **A send before the cards arrive is held** up to 4.5 s for a draft of six words or more, Enter again sending at once (decision 26). Built so; whether it stays is his call.
- **No row is focused when a 💡 or 📚 menu opens** (decision 86), where IntelliSense focuses the first, so Enter still sends until ↑/↓ move in. Built so, and recommended; his call.
- **"PR 7" with no `#` names a PR in a draft but not in Claude's prose** (decision 88): the draft matcher takes it in the chat's own repo, a prose link needs `PR #7`. Whether the two should agree is his call.
- **A reference carries its title into the draft, clipped at 90 characters** (decision 88). Whether 90 is the length he wants is his call.

## Not yet seen

- **The Usage icon against a real account** (99): read from the recorded sessions' shape and Claude Code 2.1.287's bundle; `unifiedWindows` is an `@internal` field of the CLI's, so a later version may drop it (the icon then reads the one limit an event names).
- **Promptu in the owner's window** (94–98): built and tested against a fake `promptu`, the real CLI offline, a scratch desk and headless Firefox; never run in VS Code, against the real Sonnet pass, or from a real Start work.

- **Remote Control from the phone** (decisions 83, 100): `/remote-control` links a chat in 0.25 s and prompts are still asked in the panel, but nobody has answered one from the phone side, nor seen whether a prompt sent from there shows in the panel.
- **Decisions 86–88 in the owner's window**: d998b2f installed 2026-10-25 17:08 by `./reinstall.sh` (the package's `dist` matches by md5), live only after his window reload; not yet confirmed.
- **A reference card against the live desk's real index** (decision 88): the desk serves it since 2026-10-25 17:07 (178 issues, 48 PRs) [measured], but no card has been seen in real use; measured only against a synthetic index, with real Haiku.
- **Slack's `app_redirect` link** (decision 87), for a channel a step names with no permalink, is untested.
- **One pick for every panel** (106): tested against a fake CLI and, for the wrapper, in a scratch home; not installed, never seen in a window, a Claude Code panel's resume included.

## Structural limits

- **A change dropped in a per-change diff is not reported to the CLI** (decision 64): the permission answer has no field for it, so Claude learns of it only by reading the file.
- **An MCP call cannot move to the background** (decision 70): the CLI never registers one as a foreground task, so a long `embarch-api` flash holds its turn.
- **The activity-bar count appears only once the list has been opened** (decision 35): VS Code builds a view lazily. The status-bar count always shows.
- **A new Claude Code panel session's login is recorded at its first resume, not at its start** (106): the panel gives the wrapper no session id for a new session. Until then it is on the window's pick, so a pick changed before that first resume moves it.
- **Two windows on one folder share one pick** (106): the wrapper follows the window last picked or focused, and the other window's item can say otherwise until it is focused.
