# 002 — The pass plans for work that will outgrow one context window

**State:** claimed by agent/promptu/002-the-pass-plans-for-high-context-work, 2026-11-09 17:52 — unparked 2026-11-09 by `chat/007`'s fold: the `handoff(prompt)` tool exists (embarch-chat `f823dc8`, decision 103), served on the panel's MCP server as `mcp__embarch-chat__handoff` while `embarchChat.handoff` is not `off`.
**Source:** Linear issue EMB-65, filed by the owner; the design is `embarch-promptu` decision 41 (owner, 2026-11-07)
**Issue:** EMB-65
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Before rendering, Promptu's pass judges whether the work a rough prompt describes will run at high context, and if so names one of four ways in the prompt's **Who does it**, with how to apply it and one line of why:

1. **Parallel background workers** — the `delegate-agents` shape inside the prompt.
2. **Handoff prompts** — stop at a named boundary and hand off with `embarch-chat`'s `handoff` tool (decision 103, built by `tasks/chat/007`).
3. **Scheduled compactions** — compact at named points, each with a focus.
4. **Task decimation** — split into smaller tasks, each one session's worth, in order.

A small task gets nothing added. The footer records the pick as `way=<name>` (decision 13).

This is the Promptu half of EMB-65. The chat half — `beginPromptu` passing the chat's context usage — is `tasks/chat/017`, and it waits for this task to define the input.

## Why now

Today nothing sizes a task: the pass picks a pattern, fills questions and marks relevance (`src/pass_system.md`), and a long session finds out at 80 % context, when the chat's bulb suggests a handoff. The pieces exist — `delegate-agents` (`split`, `contract`, `returns`, `stop`), `handoff` (`reader`, `scope`), the `heavy` question of `implement-issue` and `bench-session` — but nothing chooses between them.

## Direction (decision 41 — read it first; it is the design, and this task needs no new decision)

- **The pass judges**, from what it already reads plus the chat's context usage when it is given one. No code sizes the task. `embarch-chat` decision 36's thresholds (compact above about 60 %, handoff above about 80 % or unrelated work, background for a long self-contained job) are a starting point for the pass's instructions.
- **The Goal stays verbatim** (decision 9). Rewriting the prompt itself is a separate issue, not this task.
- **Define the context-usage input** in `docs/contract.md` so `tasks/chat/017` can pass it. Run without it (from Start work, say), the pass judges from the text alone.

## Where to look

- `src/pass.rs`, `src/pass_system.md` — the pass's inputs and instructions
- `src/prep.rs` `gather` — what is gathered
- `src/run.rs` — rendering, the Who does it section, the footer
- `patterns/implement-issue.md`, `delegate-agents.md`, `handoff.md`, `bench-session.md` — the shapes it reuses (bump `version` on any you change)
- `docs/contract.md` — the pass's input and the footer

## Dispatch notes

- **`embarch-chat` code is not yours.** Do not edit `beginPromptu` or `BeginOpts`; define the input on this side and stop.
- When this lands, `tasks/chat/017` unparks: the folding supervisor sets it `open` in the same fold.

## Done when

- [ ] For a rough prompt whose work will run at high context, Promptu's output names one of the four ways and how to apply it; for a small task it adds nothing.
- [ ] The pass accepts the chat's context usage as an input, documented in `docs/contract.md`, and works without it.
- [ ] The footer carries `way=<name>` when a way is picked.
- [ ] A golden test per way, and one for the small task.
- [ ] `embarch-promptu/spec.md` describes it, and decision 41 drops its "not built" for the Promptu side.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
