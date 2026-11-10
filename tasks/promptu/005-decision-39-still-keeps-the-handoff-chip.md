# 005 — Decision 39 still keeps the handoff chip the chat removed

**State:** claimed by agent/promptu/005-decision-39-still-keeps-the-handoff-chip, 2026-11-10 02:10
**Source:** Linear issue EMB-125, filed by the reviewer of `chat/018`
**Issue:** EMB-125
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

`embarch-promptu/decisions/chat.md` decision 39 ("The handoff card keeps the 'Fresh chat with this handoff' chip") states as live behaviour that the handoff pattern's prompt marks its message as a handoff request, so the answering turn offers a fresh chat with the brief, and it rests on `embarch-chat` decisions 36 and 97. Those two were amended in place on 2026-11-10 (EMB-66, the owner's call; embarch-doc `787c9cfb`, embarch-chat `b1802d6`): the 💡's handoff card, the handoff request, the chip, `freshChat` and the Promptu `handoff` origin are all removed. 39 now contradicts them.

Amend 39 in place, the way 40 was amended ("**Amended 2026-11-10 (EMB-66):** ..."): the chat no longer offers a handoff card, so the chip and the handoff-request marker are gone, and an agent's own handoff to a fresh session is `embarch-chat` decision 103. Keep the **Rejected** line as history. A tombstone is the other option the issue names; amending is preferred because 40 sets the pattern, and the heading should stop reading as a live rule either way.

## Why now

A reader of Promptu's decisions is told a chip exists that the code deleted.

## Where to look

- `embarch-doc/embarch-promptu/decisions/chat.md` decisions 39 and 40 (40 shows the amendment form)
- `embarch-doc/embarch-chat/decisions/assistant.md` decisions 36 and 97, as amended (read only, another scope)
- `embarch-doc/embarch-chat/decisions/sessions.md` decision 103 (read only; its own stale prose is `chat/022`)

## Dispatch notes

- Doc only: no `embarch-promptu` code worktree. `docs/forks.md` P9 in the code repo is the fork record and stays as history.
- Burndown is on: no new numbered decision. This is an amendment of 39 in place.
- `embarch-promptu/spec.md` is in reserve (677 B left) with its compaction task `promptu/004` blocked on `In flux: yes`. Leave `spec.md` alone; nothing here needs it.
- Check whether `embarch-promptu/spec.md`, `open.md` or `interfaces.md` also describe the chip or the handoff-request marker as live; if one does, say so in your report rather than editing `spec.md`.

## Done when

- [x] Decision 39 is amended or retired so it no longer contradicts `embarch-chat` decisions 36 and 97.
- [x] Gate green (`python3 scripts/check-docs.py`, `check-ownership.py --scope promptu`); `changelog.d/` fragment dropped.
