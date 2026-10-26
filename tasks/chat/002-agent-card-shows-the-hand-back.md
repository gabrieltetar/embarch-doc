# 002 — A background Agent's card shows the subagent's report

**State:** done, agent/chat/002-agent-card-shows-the-hand-back, 2026-10-26
**Source:** owner, 2026-10-25 — a notification said "This agent's report was delivered to you as a message from <id> (its SubagentHandback call). Read it there; it is not repeated here", and the panel showed that report nowhere
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

A background Agent's card shows the subagent's report as its result. Today it shows the launch reply (`Async agent launched successfully…`, which the CLI itself marks as internal metadata), and the report never appears. The sources, from best established to least:

- **The hand-back.** In an owner's Opus session on 2026-10-25 (CLI 2.1.287), the report arrived as one `type: "user"`, `isMeta: true` line. Its `origin` was `{kind: "peer", handback: true, from: <task id>, senderTaskId, name, body: <the report>}`. Its content was `Another Claude session sent a message:` followed by `<agent-message from=…>` and a `[Subagent hand-back]` frame. `foldUser` drops `isMeta`, so this line has to be read before that drop. Map `origin.from` to the card through the reducer's existing `tasks` map (task id to `tool_use_id`, filled by `task_started`).
  **This was seen in the transcript, not yet on the live wire.** Two recordings (Haiku and Sonnet, `--setting-sources ""`, `--tools Agent,Bash`) never produced a hand-back. Finding out whether and how it reaches the wire is the first step.
- **The fallback:** the subagent's last assistant text. It streams on the wire with `parent_tool_use_id` set to the Agent card's id, as seen in the Sonnet recording.
- **On reload:** the transcript line above, which carries `origin.body` whole.

The card shows the report collapsed, like any long tool result, and shows the launch reply only until a report arrives. The notification's row (`chat-cli-turns-are-not-the-owners`) then points at a card that holds what it names.

## Why now

The panel shows a notice that the report was delivered while hiding the report itself. For a background review or research agent, that report is the whole point of having run it. The owner chose this on 2026-10-25 over leaving the report to Claude's next reply.

## Done when

- [x] The hand-back's live wire shape is recorded as a fixture with neutral prompts. If the CLI does not put it on the wire, the decision says so and says which source the card uses instead.
- [x] Wire test: the card's result is the report, and the launch reply no longer shows as the result.
- [x] Reload test from a transcript carrying the hand-back line: the same result.
- [x] Webview e2e: the card opens to the report.
- [x] Gate, the same list as `chat-cli-turns-are-not-the-owners`: `npm ci`, `npm run build`, `npm run typecheck`, `npm test`, `npm run test:webview`, `check-client-names.py --repo .`, `check-docs.py`, `check-ownership.py --scope chat`.
- [x] Decision in `embarch-chat/decisions/timeline.md`, `spec.md` updated, `changelog.d/` fragment with scope `chat`.
- [x] If both tasks are open, this one lands second. Both edit `foldUser`, and this one reads a line that one classifies.

## Result

Decision 90. Hand-back **not recorded on the wire**: three recordings produced none, and a fourth (asking the subagent to call SubagentHandback) was refused by the auto-mode classifier and not retried. The wire test uses `notifyidle` (the subagent's last reply under `parent_tool_use_id`, the fallback); the hand-back tests use a line built from the transcript shape in the task. Webview e2e and reload test added. This landed after chat/001 (89), as required.

**Debt (live-wire):** record a hand-back from a real session where a subagent calls SubagentHandback (an owner session with a worker agent definition; `--setting-sources ""` has none) and check `origin.from`/`body` and whether it arrives as `isMeta` on stdout; until then the primary source is assumed.
