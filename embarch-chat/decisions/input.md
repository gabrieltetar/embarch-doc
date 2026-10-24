# embarch-chat decisions: What goes into a message

**Status:** active, 2026-10-23.

The input: cards that arrive while the owner types, pasted images and long pastes, side questions, a terminal's output, the keys, the editor's selection, and a message sent while Claude works.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 55 — A card that comes while the owner types waits, quiet, and nothing typed answers it

Typing is Claude Code's own rule: a non-blank draft changed in the last 1.5 s; sending or clearing the draft, or leaving the input, ends it. Meanwhile the card is one muted line with Show; once forward it stays forward. A card never takes focus or moves the input. A draft sent while a card waits is queued, and the CLI delivers it after the answer, in the same turn [measured]. **Rejected:** the card replacing the input (Claude Code's layout), a sent draft becoming the card's answer, Claude Code's 500 ms key lock (these cards have no key shortcuts and never take focus).

### 56 — A pasted image is a thumbnail under the input and sends, alone if need be

8's "later" half. Raw image bytes WSL's clipboard hands over as text are refused with a notice. A paste over 800 characters or 2 line breaks goes in `inline_pastes` for the CLI to mark, and the echoed `<pasted_content>` is matched so it shows once [measured]. Invisible characters are stripped from pastes and drafts, with a notice. **Rejected:** raw clipboard text as-is, paste tags of the panel's own.

### 57 — `/btw` is the CLI's `side_question`

It answers from the conversation and the running turn, beside the timeline and never in it, cleared by hand or after Claude Code's 5 minutes [measured]. **Rejected:** a second process, a queued message.

### 58 — A terminal picked from @ goes as its last 100 lines

Read at send by select-copy with the clipboard put back, as Claude Code does; a failed copy sends nothing rather than the owner's clipboard. **Rejected:** shell-integration reads (only commands run afterwards), pasting the output into the draft.

### 59 — Claude Code's keys, on chords it does not hold

Ctrl+Alt+Esc focuses or leaves the input, Alt+Shift+K mentions the selection as `@path#Lx-y`, Ctrl+Shift+T reopens a chat tab when one was the last closed. **Rejected:** Claude Code's own chords (both extensions run; they race), no keys.

### 60 — The selection, else the open file, goes with each message

As Claude Code's `<ide_selection>` / `<ide_opened_file>` blocks: a chip with ×, sent once until it changes; `embarchChat.attachOpenFile` and `attachSelection`, machine scope, on. **Rejected:** @-mention only, application-scoped settings.

### 72 — A message sent while Claude works waits above the input until Claude takes it in

Then it joins the timeline there. It can be cancelled back to the draft, or sent now: foreground steps go to the background first, else the turn stops — the CLI's own `send_now` killed a foreground Bash on 2.1.287 [measured], against its changelog, and a canary test fails once a re-recording shows the CLI moving the step itself. While a card waits there is no Send now (55). **Rejected:** the message in the timeline at send time, `send_now` alone.
