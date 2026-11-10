# 020 — Two chat decisions still put the notice line and the thumbnails under the input

**State:** done
**Source:** Linear issue EMB-119, filed by the reviewer of `chat/014`
**Issue:** EMB-119
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

Since `chat/014` (`embarch-chat` `424c3cf`, decisions 81 and 83 amended) the input is one row and nothing sits under the box: `webview/chat/composer.tsx` renders the shared `notice` line (`.paste-notice`) and the attachments row **above** `.bar`. Two decisions left standing still place them under it:

- decision 56 in `embarch-chat/decisions/input.md`, "A pasted image is a thumbnail under the input and sends, alone if need be";
- the Promptu decision in `embarch-chat/decisions/promptu.md`, where a pass that is not installed, exits non-zero or times out "is one line under the input", and Desk Start work's failed pass has "one line" saying so.

That line is the same `notice` state the composer uses for paste, `/btw` and Promptu messages.

## Why now

The decisions describe a layout the composer no longer has, so a reader plans against the old one.

## Where to look

- `embarch-doc/embarch-chat/decisions/input.md` — decision 56, its heading and body
- `embarch-doc/embarch-chat/decisions/promptu.md` — "one line under the input"
- `embarch-chat/webview/chat/composer.tsx` — where `notice` and `.attachments` render relative to `.bar`; read it, the layout is not to change

## Dispatch notes

- **Doc only.** The layout is what EMB-60 asked for; fix the wording ("above the input"), not the composer. The `embarch-chat` worktree is there to read; leave it clean and do not push it.
- Amend both decisions in place, heading included; no new decision (burndown is on).
- Grep every `embarch-chat` doc for anything else saying something is under the input or the box, and fix what you find in the same commit.

## Done when

- [x] Decision 56 and the Promptu decision say where the thumbnails and the notice line render, and match the composer.
- [x] No other `embarch-chat` doc says the input has anything under it.
- [x] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
