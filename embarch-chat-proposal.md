# Proposal: the owner's own Claude chat, in VS Code

**Status:** draft, 2026-10-22. Shaping notes; becomes a proposal once its open questions are answered. May take over [`embarch-promptu`](embarch-promptu/design.md)'s place in the suite.

## The ask

A Claude Code chat of the owner's own — "its own Claude Code chat basically, with improvements tailored to my needs" — so that the Desk can start, show and answer sessions itself instead of handing off to claude.ai (`embarch-desk` decision 44).

## What is possible (measured 2026-10-22)

**One EmbArch-owned process held a real multi-turn Claude Code conversation on the owner's own login**: `claude -p --input-format stream-json --output-format stream-json`, two user messages fed in over time, one session id throughout, the second answer remembering the first; $0.004 on Haiku with a stripped context. From the docs: approvals can be routed to a tool of the chat's own (`--permission-prompt-tool`), and sessions started this way appear in VS Code's history, so any chat can still be opened in the Claude Code panel. **Costs:** the stream-json wire format is only partly documented (it is the transport Anthropic's SDK uses); the official SDK itself expects an API key, so this rides the `claude` CLI; and inside this chat there are none of the Claude Code panel's inline diffs.

## Decided so far (2026-10-22)

1. **It lives in a VS Code panel** — an extension of EmbArch's own, beside the code.
2. **It replaces the Claude Code panel for the owner's work.** VS Code stays for reading and editing code, and any chat can still open in Claude Code's panel.
3. **The first improvements that pull hardest:** it knows its **work item** (issue, comments, PRs, time) and starts briefed; it carries the owner's **prompt library** — `embarch-promptu`'s curated firmware prompts and skills — as one-click actions; **every thread at a glance**, waiting-on-you first; **bench-aware** — study output, flash results inline; and **atlas integration**.
4. **Tomorrow's workflow does not wait for it**: Start work opens the Claude Code panel (`embarch-desk` decision 43) until this exists.

## Open

Everything else — how chats are stored and named, what "prompt library" means concretely, how the bench and the atlas show inline, whether this is `embarch-promptu` renamed or a new sub-project beside it, and what of the Claude Code panel it must match on day one.
