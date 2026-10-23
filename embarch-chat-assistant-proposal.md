# Proposal: the chat's Haiku assistant

**Status:** proposal, 2026-10-22.

The Haiku assistant at the input of the owner's own Claude chat, split from [embarch-chat-proposal.md](embarch-chat-proposal.md) when that file reached its size cap. **Decision numbers are shared with it** and stay permanent; this part ships with the rest (decision 23). Not built: building waits for the owner's go.

## What is possible (measured 2026-10-22)

**Haiku thinks by default here** — 5–9 s for a one-line completion. With thinking off (`--max-thinking-tokens 0`), stripped (`--tools ""`, `--strict-mcp-config`, `--setting-sources ""`), unsaved (`--no-session-persistence`, which leaves no transcript in the owner's history) and streamed (`--include-partial-messages`), a `claude -p` call is ready in 0.37 s, sends its **first token at 0.86 s and finishes at 1.07 s** (three runs alike), for $0.0016 with a one-line context. `--prompt-suggestions` gives the CLI's own guess at the next prompt; the `get_context_usage` control request gives a chat's tokens by category.

## Decided

**19 —** **Quick replies follow the moment** — the owner's most-sent messages are one word (decision 14) — **and Haiku drafts them**. **Rejected:** a fixed row of chips; none; the CLI's `--prompt-suggestions` guess alone or with two hand rules (blind to the draft); a hand-written table of situations.

**24 —** **While the owner writes, Haiku offers ghost text and cards.** The completion shows in grey and Tab takes it; cards above the input suggest or warn. **Rejected:** a one-line note under the box (became the cards), a tighten-the-draft button.

**28 —** **Cards for missing context and prompt improvements**: what Claude will need and the draft lacks (which board, issue, file), and how the prompt could be better put. **Rejected:** a library entry that fits, a heads-up that auto mode will flash, push or move an issue, a warning that another thread is on it.

**36 —** **And a card for context handling**: Haiku judges whether the prompt calls for a **background agent**, **compacting first**, or **a handoff to a fresh chat**, so it also sees the chat's context usage (27). What each card's action does is still being shaped.

**25 —** **When Claude's turn ends, it drafts two to four replies as chips**, the CLI's own guess among them. **Rejected:** a checklist of what Claude asked, a one-line digest of the reply in the list.

**26 —** **It runs on a pause** — 700 ms after typing stops, and after each turn; the next keystroke cancels a stale call. Each call is one stripped, unsaved, streamed `claude -p` with thinking off, returning completion, cards and chips together: about 1.1 s and $0.002–0.004, so $1–2 a day at ~500 calls [estimate]. `EMBARCH_DESK_INTERNAL=1` keeps the desk out. **Rejected:** after turns only, only on a key.

**34 —** **It runs for the chat on screen only.** A background chat gets its chips when it is opened, one call then; the naming call (decision 12) still runs once per chat after its first turn. **Rejected:** every chat after every turn (cost grows with the chats running).

**27 —** **It sees the draft, Claude's last reply, the work item's card, the library's entry names and the chat's context usage** — 1–3K tokens. **Rejected:** the whole transcript (about 10× the cost), the draft and last reply only.

## Open questions

- **How ghost text should feel**: a layer that answers at once from local data before Haiku's 1.1 s, and how long the pause is.
- **What a context-handling card does on a click** (36): who writes a handoff, and what "background agent" starts.
- **Does a click on an improvement card rewrite the draft**, or only show the better wording?
