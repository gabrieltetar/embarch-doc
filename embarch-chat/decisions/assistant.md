# embarch-chat decisions: The Haiku assistant

**Status:** active, 2026-10-23.

The Haiku assistant at the input: quick replies, ghost text, cards and the desk's references in them, when it runs and what it sees. Where its 💡 sits beside the library's 📚 is decision 38 ([library.md](library.md)).

**What it rests on [measured 2026-10-22]:** Haiku thinks by default here — 5–9 s for a one-line completion. With thinking off (`--max-thinking-tokens 0`), stripped (`--tools ""`, `--strict-mcp-config`, `--setting-sources ""`), unsaved (`--no-session-persistence`, which leaves no transcript in the owner's history) and streamed (`--include-partial-messages`), a `claude -p` call is ready in 0.37 s, sends its first token at 0.86 s and finishes at 1.07 s (three runs alike), for $0.0016 with a one-line context. `--prompt-suggestions` gives the CLI's own guess at the next prompt; the `get_context_usage` control request gives a chat's tokens by category.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 19 — Quick replies follow the moment, and Haiku drafts them

The owner's most-sent messages are one word (14). **Rejected:** a fixed row of chips; none; the CLI's `--prompt-suggestions` guess alone or with two hand rules (blind to the draft); a hand-written table of situations.

### 24 — While the owner writes, Haiku offers ghost text and cards

The completion shows in grey and Tab takes it; cards suggest or warn, behind a 💡 (38). **Rejected:** a one-line note under the box (became the cards), a tighten-the-draft button.

### 28 — Cards for missing context and prompt improvements

What Claude will need and the draft lacks (which board, issue, file), and how the prompt could be better put. **Rejected:** a library entry that fits, a heads-up that auto mode will flash, push or move an issue, a warning that another thread is on it.

### 36 — And a card for context handling

Haiku judges whether the prompt calls for a **background agent**, **compacting first**, or **a handoff to a fresh chat**, so it also sees the chat's context usage (27). Like every card it only edits the draft (37): the background-agent card adds an instruction to run the work as a background subagent and report back; **the compact card adds a first line, `/compact focus on: <what the draft is about>`** — Claude cannot run `/compact` itself — and on Enter the panel sends that line, waits for the compaction to finish, then sends the rest — or, if the owner stops the compaction or it fails, marks the rest not sent and puts it back in the draft; **the handoff card turns the draft into a request that this chat write a handoff** for a fresh chat (its model has the whole context), and the chips after that turn offer **"Fresh chat with this handoff"** — a new chat on the same work item that starts with it, the old one left readable. **Rejected:** the draft replaced by `/compact` and restored after; no compact card (the header's button only); copying a handoff by hand, or a fresh chat opened unasked; a button starting a new chat or agent itself (cards never act outside the draft); Haiku writing the handoff (it sees 1–3K tokens); a `/handoff` library entry run by hand.

### 37 — A card is an edit to the draft, previewed in place

Hovering a card shows its change inside the draft, IntelliSense-style — added words in ghost grey, removed ones struck through; a click applies it (or ↑/↓ and Enter, 86), and Ctrl+Z restores the draft. **Rejected:** a Use-it button replacing the draft unseen, a rewrite in place with no preview, advice that leaves the editing to the owner.

### 88 — The chat mirrors its desk's reference index: a card names the real issue or PR, and one in Claude's prose is a link

A vague "the widget PR" got a card asking which PR [measured on a synthetic case: 6 of 6, 3.9 s median]. **The host mirrors the window's desk's index** (`embarch-desk` decision 56) — `GET /refs` for the desk `GET /view` is asked for, read once and again only when the view's `refs_ms` moves, handed whole to each chat page and never the token (20). **Before the cards call the draft is matched locally**: its significant words against the titles, a word few titles share counting most, plus any key, `owner/repo#N` or `PR #N` in the chat's own repo it names; the chat's own item is left out, its card already in the prompt (27). The best lines — an issue with up to two PRs naming it, or a PR alone; at most 8, about 600 tokens — go in a `<desk_references>` block of the cards prompt only: the same single call (26), nothing on a keystroke, ghost text untouched. **The reference is written by the extension, never by Haiku**: Haiku names a line by its id and the vague phrase exactly as the draft has it, and the replacement comes from the index — `PR owner/repo#7 "Widget" (ABC-12)`, or the issue first when the phrase says issue, ticket or card — spliced in as written (a `$` in a title is text) at the phrase's first whole-word occurrence, a combining mark counting as part of its word. Anyone can title a PR on a repo in the desk's scope, so a title is data: stripped of `<`, `>`, line breaks and what shows nothing, clipped at 90 characters, and any other card that would carry four of a title's words in a row into the draft is dropped [measured on the synthetic case: a replace naming the PR 8 of 8, 2.34 s median; a title written to steer the cards copied 0 of 4]. Several lines fitting give a card each, at most 3; none, a bracketed question. **In Claude's prose** `ABC-12`, `owner/repo#7` and `PR #7` in the chat's own repo are links only when the index knows them, as atlas citations are only with an atlas (16): an issue opens Linear, a PR GitHub, and the hover names it in full, `owner/repo#7 "Widget" · merged`, so a wrong one shows before the click. A bare `#7` never is — "step #3" is no PR. The chat's own repo — read from its folder's git config, regular files of 64 KB or less, as `gh` picks one with no terminal — is used for that `PR #7` and the draft matcher only, never for a step (87). **Rejected:** a resolve route on the desk called per card (Linear and GitHub on the cards' path), Haiku calling the desk's tools (a round-trip in a call stripped of tools, 26), feeding it only the desk's cards (a card holds its own item's PRs, and a Done issue never on a card was invisible), Haiku writing the reference, a bare `#N` linked because one PR in the index has it.

### 25 — When Claude's turn ends, it drafts two to four replies as chips

The CLI's own guess among them. **Rejected:** a checklist of what Claude asked, a one-line digest of the reply in the list.

### 26 — It comes in three waves, as an editor's completion does

**Instant, no model:** typing through the ghost text already shown, a prefix match over the owner's own prompts of the last 30 days (from the transcripts — `~/.claude/history.jsonl` holds only the terminal's), `/` for library commands and `@` for files. **About 1.2 s:** Haiku's ghost text, streamed, after a 300 ms pause. **On a 2 s pause or just before send:** the cards, because they judge the whole prompt, not half a sentence. Chips come after each turn. Every call is one stripped, unsaved, streamed `claude -p` with thinking off, $0.002–0.004 — **measured as built**: ghost text's first token at 0.82–0.89 s and done at 1.8–2.1 s (Haiku wraps its JSON in a code fence even when told not to), cards 3.8 s, chips and name 2.6 s — $1–2 a day at ~500 calls [estimate] — and the next keystroke cancels a stale one; `EMBARCH_DESK_INTERNAL=1` keeps the desk out. **A send before the cards arrive is held** for them, up to 4.5 s, for a draft of six words or more; Enter again sends at once — built so, and waiting on the owner's call ([open.md](../open.md)). **Rejected:** one Haiku call at 700 ms for ghost text and cards together, with or without the local layer (cards judging half-typed sentences); after turns only; only on a key.

### 34 — It runs for the chat on screen only

A background chat gets its chips when it is opened, one call then; the naming call (12) still runs once per chat after its first turn. **Rejected:** every chat after every turn (cost grows with the chats running).

### 27 — It sees the draft, Claude's last reply, the work item's card, the library's entry names and the chat's context usage

1–3K tokens. **Rejected:** the whole transcript (about 10× the cost), the draft and last reply only.
