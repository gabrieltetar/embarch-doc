# embarch-chat: open

**Status:** active, 2026-11-01.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

## Not done

- **The library has not been seeded** (decision 14): the plugin holds promptu's three pieces and `~/.claude/commands` is empty [measured 2026-10-23]. The `claude -p` grouping pass, then the owner's ✓/✕, fills it.
- **`last_session` does not write a `Handoff` desk line** from what it reads; it only prints. "Pending" is a reading of the transcript (a background call with no finished notification) not a live process; tested on synthetic transcripts.

## Waiting on the owner

- **Promptu in the chat (94–99) is installed** (spec status). **Decision 100 is not recorded as reviewed**; whether it was is his to say. Forks waiting for his pick in `embarch-promptu`'s docs/forks.md: P12 (one pass per task start) and P15 (smaller choices); P16–P19 are decided (94, 96, 99).

- **A send before the cards arrive is held** up to 4.5 s for a draft of six words or more, Enter again sending at once (decision 26). Whether it stays is his call.
- **No row is focused when a 💡 or 📚 menu opens** (decision 86), where IntelliSense focuses the first, so Enter still sends until ↑/↓ move in. His call.
- **"PR 7" with no `#` names a PR in a draft but not in Claude's prose** (decision 88): the draft matcher takes it in the chat's own repo, a prose link needs `PR #7`. Whether the two should agree is his call.
- **A reference carries its title into the draft, clipped at 90 characters** (decision 88). Whether 90 is right is his call.

## Not yet seen

- **A real limit hit over the panel's wire** (109): the made-up reply is read from a 2.1.322 transcript and the `rate_limit_event` from usage.ts's shape (99); neither seen in a chat's stream. Claude Code 2.1.322's own automatic continue (`autoContinueAtUsageLimit`, behind a server flag) may run in `stream-json` mode; if so the chat's wait ends when its turn starts, so the two never both send.
- **The Usage icon against a real account** (99): read from recorded sessions and Claude Code 2.1.287's bundle; `unifiedWindows` is an `@internal` field of the CLI's, so a later version may drop it (the icon then reads the one limit an event names).
- **Promptu in the owner's window** (94–98): tested against a fake `promptu`, a scratch desk and headless Firefox; never run in VS Code, against the real Sonnet pass, or from a real Start work.

- **Remote Control from the phone** (decisions 83, 100): a chat bridged at startup shows in the phone's list [owner, 2026-11-11], and Remote Control works from the phone [owner, 2026-11-17, EMB-62]. What is left: `test/fixtures/wire/remote.jsonl` was recorded from `/remote-control`, never from a live startup bridge.
- **Decisions 86–88 in the owner's window**: installed 2026-10-25 by `./reinstall.sh`, live only after his window reload; not yet confirmed.
- **A reference card against the live desk's real index** (decision 88): the desk serves it since 2026-10-25, but no card has been seen in real use; tested only against a synthetic index, real Haiku.
- **Slack's `app_redirect` link** (decision 87), for a channel a step names with no permalink, is untested.
- **A container login** (122): golden-tested against a stand-in runtime only; no container was started. First session on the owner's machine: a chat starts in the container, its transcript is found under the exchange folder, a handoff stays in the container, no host hook runs, and a stopped container names `embarch agent up`. Rewind and the rerun after a reload need the panel's two variables, which `exec` does not carry.
- **One pick for every panel** (106): tested against a fake CLI and, for the wrapper, in a scratch home; not installed, never seen in a window.

## Structural limits

Five limits that wait on no one (decisions 35, 64, 70, 106): [open/limits.md](open/limits.md).
