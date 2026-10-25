# embarch-chat decisions: What goes into a message

**Status:** active, 2026-10-23.

The input: cards that arrive while the owner types, pasted images and long pastes, side questions, a terminal's output, the keys and the menus' keys, the editor's selection, and a message sent while Claude works.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 55 — A card that comes while the owner types waits, quiet, and nothing typed answers it

Typing is Claude Code's own rule: a non-blank draft changed in the last 1.5 s; sending or clearing the draft, or leaving the input, ends it. Meanwhile the card is one muted line with Show; once forward it stays forward. A card never takes focus or moves the input. A draft sent while a card waits is queued, and the CLI delivers it after the answer, in the same turn [measured]. **Rejected:** the card replacing the input (Claude Code's layout), a sent draft becoming the card's answer, Claude Code's 500 ms key lock (these cards have no key shortcuts and never take focus).

### 56 — A pasted image is a thumbnail under the input and sends, alone if need be

8's "later" half. Raw image bytes WSL's clipboard hands over as text are refused with a notice. A paste over 800 characters or 2 line breaks goes in `inline_pastes` for the CLI to mark, and the echoed `<pasted_content>` is matched so it shows once [measured]. Invisible characters are stripped from pastes and drafts, with a notice. **Rejected:** raw clipboard text as-is, paste tags of the panel's own.

### 57 — `/btw` is the CLI's `side_question`

It answers from the conversation and the running turn, beside the timeline and never in it, cleared by hand or after Claude Code's 5 minutes [measured]. **Rejected:** a second process, a queued message.

### 58 — A terminal picked from @ goes as its last 100 lines

Read at send by select-copy with the clipboard put back, as Claude Code does; a failed copy sends nothing rather than the owner's clipboard. The terminal is picked by its process, not its name, and shown without focus so keys typed meanwhile cannot reach the shell; the chip says the clipboard is used and only text comes back. **Rejected:** shell-integration reads (only commands run afterwards), pasting the output into the draft.

### 59 — Claude Code's keys, on chords it does not hold

Ctrl+Alt+Esc focuses or leaves the input, Alt+Shift+K mentions the selection as `@path#Lx-y`, Ctrl+Shift+T reopens a chat tab when one was the last closed. **Rejected:** Claude Code's own chords (both extensions run; they race), no keys.

### 86 — A 💡 preview never moves what is under the pointer, and both menus go by keyboard as IntelliSense does

The menu sits on the composer's top edge and a card's preview grows the draft (37), so a row under a still pointer moved away, its preview ended, the draft shrank and the row came back [measured in headless Firefox: the menu jumped 73 px and the preview flipped 13 times in 500 ms; after the change, 0]. **While the 💡 shows, the field holds the height of its tallest preview** — every card's, and the draft as it shows — measured again when the cards, the draft or the field's width change; a card arriving while the menu shows moves the layout once. **The keys focus a row as in IntelliSense**: ↑/↓ within a category, ←/→ between categories, Enter or Tab picks, Esc closes — through the input, which keeps the focus so typing goes on. **The pointer's row only previews**, as IntelliSense's hover does, and only while no row is key-focused: Enter and Tab act only on a row ↑/↓ reached, and a key-focused row keeps its preview — what shows is what Enter applies, as VS Code's suggest details follow the selection — while the pointer only marks the row it is over; a click on any row applies it. No row is focused when a menu opens, so a 💡 the held send opens (26) under a still pointer leaves Enter sending the draft as it is. While a menu shows, Tab never leaves the input; with no row focused it takes the ghost text or nothing. **Rejected:** pinning the menu, a delay before a hover previews, the preview inside the menu instead of in the draft (37), the pointer's row taking Enter.

### 60 — The selection, else the open file, goes with each message

As Claude Code's `<ide_selection>` / `<ide_opened_file>` blocks: a chip with ×, sent once until it changes; `embarchChat.attachOpenFile` and `attachSelection`, machine scope, on. **Rejected:** @-mention only, application-scoped settings.

### 72 — A message sent while Claude works waits above the input until Claude takes it in

Then it joins the timeline there. It can be cancelled back to the draft, or sent now: foreground steps go to the background first, else the turn stops — the CLI's own `send_now` killed a foreground Bash on 2.1.287 [measured], against its changelog, and a canary test fails once a re-recording shows the CLI moving the step itself. While a card waits there is no Send now (55). **Rejected:** the message in the timeline at send time, `send_now` alone.
